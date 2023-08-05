# coding: utf-8
#/*##########################################################################
# Copyright (C) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/

"""This module analyze headDir data directory
   to detect scan to be reconstructed
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "30/05/2017"

from ..BaseProcess import BaseProcess
from tomwer.core.utils import logconfig
from tomwer.core import tomodir
from tomwer.core.tomodir.TomoDirObserver import _TomoDirObserver, _TomoDirFixObserver
from tomwer.core.WaiterThread import WaiterThread
from tomwer.core.settings import LBSRAM_ID, DEST_ID
from collections import OrderedDict
from silx.gui import qt
import datetime
import logging
import os

logger = logging.getLogger(__file__)


class TomoDir(BaseProcess):
    """TomoDir is the class use to mange observation of scans
    
    It basically have one TomoDirObserver thread which is dealing with the
        observations. It parse all folder contained under the RootDir.
    
    This TomoDirObserver is runned every `maxWaitBtwObsLoop`. The call to the
    TomodirObserver is managed by the `loopObservationThread` which is calling
    back `_launchObservation`
    
    TomoDir can run infinite search or stop observation after the discovery of
    the first valid scan (`setInfiniteIteration`)
    """
    inputs = []
    outputs = [{'name': "data",
                'type': str,
                'doc': "signal emitted when the scan is completed"}]

    folderObserved = None

    NB_STORED_LAST_FOUND = 20
    """All found acquisition are stored until we reach this number. In this
    case the oldest one will be removed"""

    DEFAULT_OBS_METH = tomodir.DET_END_XML


    def __init__(self):
        BaseProcess.__init__(self, logger)
        """use to know if we want to continue observation when the finished
        scan is found ?"""
        self.lastFoundScans = _LastReceivedScansDict(self.NB_STORED_LAST_FOUND)
        self.isObserving = False
        self._initClass()

        # get ready observation
        self._setCurrentStatus('not processing')
        self._launchObservation()

    def _initClass(self):
        self.srcPattern = LBSRAM_ID
        self.destPattern = DEST_ID

        self.observationThread = None
        """Thread used to parse directories and found where some 
        :class`TomoDirFixObserver` have to be launcher"""
        self.loopObservationThread = None
        """Thread used to launch an observation thread each n second"""
        self.obsThIsConnected = False
        self.maxWaitBtwObsLoop = 5  # TODO : should be stored in settings
        self.obsMethod = self.DEFAULT_OBS_METH
        """Pattern to look in the acquisition file to know of the acquisition
         is ended or not"""
        self.startByOldest = False

    def _switchObservation(self):
        """Switch the status of observation
        """
        if self.isObserving is True:
            self.stopObservation()
        else:
            self.startObservation()

    def setObsMethod(self, obsMethod):
        """Set the observation method to follow.
        
        .. Note:: For now this will be apply on the next observation iteration.
                  We don't wan't to stop and restart an observation as sometimes
                  It can invoke a lot of start/stop if the user is editing the
                  pattern of the file for example. But this might evolve in the
                  future.
        """
        assert type(obsMethod) in (str, tuple)
        if type(obsMethod) is tuple:
            assert len(obsMethod) is 1 or (type(obsMethod[1]) is dict and len(obsMethod) is 2)
        self.obsMethod = obsMethod
        if self.isObserving:
            self._restartObservation()

    def setObservation(self, b):
        """Start a new observation (if none running ) or stop the current
        observation

        :param bool b: the value to set to the observation
        """
        self.startObservation() if b else self.stopObservation()

    def stopObservation(self, sucess=False):
        """
        Stop the thread of observation

        :param bool sucess: if True this mean that we are stopping the
                            observation because we found an acquisition
                            finished. In this case we don't want to update the
                            status and the log message
                            
        """
        if self.isObserving is False:
            return False

        self._setIsObserving(False)
        if self.loopObservationThread is not None:
            self.loopObservationThread.wait(self.maxWaitBtwObsLoop + 2)
        if self.observationThread is not None:
            # remove connection
            self.observationThread.quit()
            self._disconnectObserverThread()

        if sucess is False:
            self._setCurrentStatus(str("not processing"))

        return True

    def startObservation(self):
        """Start the thread of observation

         :return bool: True if the observation was started. Otherwise this
            mean that an observation was already running
        """
        if self.isObserving is True:
            return False
        else:
            self._setIsObserving(True)
            self._setCurrentStatus('not processing')
            self._launchObservation()

            return True

    def isObserving(self):
        """
        
        :return bool: True if the widget is actually observing the root
                      directory
        
        """
        return self.isObserving

    def _setIsObserving(self, b):
        self.isObserving = b

    def resetStatus(self):
        """
        Reset the status to not processing. Needed to restart observation,
        like when the folder is changing
        """
        self._setCurrentStatus('not processing')

    def getFolderObserved(self):
        return self.folderObserved

    def setFolderObserved(self, path):
        assert(type(path) is str)
        if not os.path.isdir(path):
            warning = "Can't set the observe folder to ", path, " invalid path"
            logger.warning(warning,
                           extra={logconfig.DOC_TITLE: self._scheme_title})
        else:
            self.folderObserved = path

    def getTimeBreakBetweenObservation(self):
        """

        :return: the duration of the break we want to do between two
            observations (in sec)
        """
        return self.maxWaitBtwObsLoop

    def setWaitTimeBtwLoop(self, time):
        if not time > 0:
            err = 'invalid time given %s' % time
            raise ValueError(err)
        self.maxWaitBtwObsLoop = time

    def setStartByOldest(self, b):
        """
        When parsing folders, should we start by the oldest or the newest file
        
        :param bool b: if True, will parse folders from the oldest one
        """
        self.startByOldest = b

    def setSrcAndDestPattern(self, srcPattern, destPattern):
        """Set the values of source pattern and dest pattern

        :param str srcPattern: the value to set to the source pattern
            (see tomodir)
        :param str destPattern: the value to set to the destination pattern
            (see tomodir)
        """
        self.srcPattern = srcPattern
        self.destPattern = destPattern

    def _initObservation(self):
        """Init the thread running the tomodir functions"""
        if self.observationThread is None:
            self.observationThread = _TomoDirObserver(
                                        obsMethod=self.obsMethod,
                                        srcPattern=self.srcPattern,
                                        destPattern=self.destPattern)
            self._connectObserverThread()

        headDir = self.getFolderObserved()
        if headDir is None or not os.path.isdir(headDir):
            message = "Given path (%s) isn't a directory." % headDir
            logger.warning(message,
                           extra={logconfig.DOC_TITLE: self._scheme_title})

            self.statusBar.showMessage('!!! ' + message + '!!!')
            self.stopObservation()
            return False

        # update information on the head folder and the start by the oldest
        self.observationThread.setHeadFolder(headDir)
        self.observationThread.setObservationMethod(self.obsMethod)

        return True

    def _launchObservation(self):
        """Main function of the widget"""
        if self.isObserving is False:
            return

        # manage tomodir observation
        if self.observationThread is None or not self.observationThread.isRunning():
            if self._initObservation() is False:
                self.currentStatus = self._setCurrentStatus('failure')
                logger.info('failed on observation',
                            extra={
                                logconfig.DOC_TITLE: self._scheme_title})
                return

        # starting the observation thread
        self.observationThread.start()

        # manage observation loop
        if self.loopObservationThread is None:
            self.loopObservationThread = WaiterThread(self.getTimeBreakBetweenObservation())
            self.loopObservationThread.finished.connect(self._launchObservation)

        if not self.loopObservationThread.isRunning():
            self._connectObserverThread()
            self.loopObservationThread.start()

    def _restartObservation(self):
        """Reset system to launch a new observation
        """
        if self.loopObservationThread is not None:
            self.loopObservationThread.quit()
            self._setCurrentStatus('not processing')
            self._launchObservation()

    def _statusChanged(self, status):
        assert(status[0] in tomodir.OBSERVATION_STATUS)
        self._setCurrentStatus(status[0], status[1] if len(status) == 2 else None)

    def informationReceived(self, info):
        logger.info(info)

    def _setCurrentStatus(self, status, info=None):
        """Change the current status to status"""
        assert(type(status) is str)
        assert(status in tomodir.OBSERVATION_STATUS)
        self.currentStatus = status
        self._updateStatusView()
        self.sigTMStatusChanged.emit(status)

        _info = status
        if info is not None:
            _info += " - " + info

        self.informationReceived(_info)

        if status == 'acquisition ended':
            # info should be the directory path
            assert(info is not None)
            assert(type(info) is str)
            logger.processEnded('Find a valid scan',
                        extra={logconfig.DOC_TITLE: self._scheme_title,
                               logconfig.SCAN_ID: info})
            self._signalScanReady(scanID=info)

    def _signalScanReady(self, scanID):
        self.lastFoundScans.add(scanID)
        self.sigScanReady.emit(scanID)

    def mockObservation(self, folder):
        # simple mocking emitting a signal to say that the given folder is valid
        self._setCurrentStatus(status='acquisition ended', info=folder)

    def _updateStatusView(self):
        pass

    def _setMaxAdvancement(self, max):
        """"""
        pass

    def _advance(self, nb):
        """Update the progress bar"""
        pass

    def _connectObserverThread(self):
        if self.observationThread is not None and self.obsThIsConnected is False:
            self.observationThread.sigScanReady.connect(self._signalScanReady)
            self.obsThIsConnected = True

    def _disconnectObserverThread(self):
        if self.observationThread is not None and self.obsThIsConnected is True:
            self.observationThread.sigScanReady.disconnect(self._signalScanReady)
            self.obsThIsConnected = False

    def setProperties(self, properties):
        pass

    def _updateLastScanFound(self, scanID):
        """Will make sure that we are registring the last NB_STORED_LAST_FOUND
        found scans with the time of discovery"""

    def waitForObservationFinished(self):
        if self.observationThread is not None:
            self.observationThread.waitForObservationFinished()
            self.observationThread.wait()

    def getIgnoredFolders(self):
        if self.observationThread is None:
            return []
        else:
            return self.observationThread.observations.ignoredFolders


class TomoDirP(TomoDir, qt.QObject):
    """For now to avoid multiple inheritance from QObject with the process
    widgets
    we have to define two classes. One only for the QObject inheritance
    """

    sigTMStatusChanged = qt.Signal(str)
    sigScanReady = qt.Signal(str)

    def __init__(self):
        qt.QObject.__init__(self)
        TomoDir.__init__(self)


class _LastReceivedScansDict(OrderedDict):
    """List the received scan from the first received to the last received
    """
    def __init__(self, limit=None):
        """Simple structure in order to store the received last elements and
        the time of acquisition
        """
        assert limit is None or (type(limit) is int and limit > 0)
        OrderedDict.__init__(self)
        self.limit = limit

    def add(self, scanID):
        self[scanID] = datetime.datetime.now()
        if self.limit is not None and len(self) > self.limit:
            self.pop(list(self.keys())[0])
