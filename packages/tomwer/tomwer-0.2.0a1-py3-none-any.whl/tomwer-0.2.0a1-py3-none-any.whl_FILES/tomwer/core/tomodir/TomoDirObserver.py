# coding: utf-8
#/*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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

"""
This module is used to manage observations. Initially on files.
Observations are runned on a thread and run each n seconds.
They are manage by thread and signals
"""

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "09/02/2017"


from silx.gui import qt
import logging
import os
from ._TomoDirProcess import _TomoDirProcessParseInfo, _TomoDirProcessUserFilePattern, _TomoDirProcessXML
from tomwer.web.client import OWClient
from tomwer.core import tomodir
from collections import OrderedDict

logger = logging.getLogger("tomodirThread")


class _TomoDirFixObserver(OWClient, qt.QThread):
    """Observe one specific directory and signal when the state of this
    directory change"""

    sigStatusChanged = qt.Signal(int, str)
    """signal emitted when the status for a specific directory change
    """

    def __init__(self, scanID, obsMethod, srcPattern, destPattern, patternObs):
        OWClient.__init__(self, loggers=logger)
        qt.QThread.__init__(self)

        self.obsMethod = obsMethod
        self.srcPattern = srcPattern
        self.destPattern = destPattern
        self.patternObs = patternObs
        """The pattern to use for the DET_END_USER_ENTRY method"""
        self.setDirToObserve(scanID)
        self.tomodirProcess = self._getTomoDirProcess()
        self.status = 'not processing'

    def setDirToObserve(self, directory):
        self.scanID = directory
        if hasattr(self, 'tomodirProcess') and self.tomodirProcess:
            self.tomodirProcess.RootDir = directory
            self.tomodirProcess.parsing_dir = ''

    def quit(self):
        if self.tomodirProcess is not None:
            self.tomodirProcess.quitting = True
        qt.QThread.quit(self)

    def run(self):
        if not os.path.isdir(self.scanID):
            logger.info('can\'t observe %s, not a directory' % self.scanID)
            self.status = 'failure'
            self.sigStatusChanged.emit(tomodir.OBSERVATION_STATUS[self.status],
                                       self.scanID)
            self.validation = -1
            return


        if self.tomodirProcess.acquisitionAborted():
            if self.status != 'aborted':
                logger.info("Acquisition %s has been aborted" % self.scanID)
                self.tomodirProcess._removeAcquisition(
                    scanID=self.scanID,
                    reason='acquisition aborted by the user')

                self.status = 'aborted'
            self.sigStatusChanged.emit(tomodir.OBSERVATION_STATUS[self.status],
                                       self.scanID)
            self.validation = -2
            return

        dataComplete = self.tomodirProcess.is_data_complete()

        if dataComplete is True:
            self.status = 'acquisition ended'
            self.sigStatusChanged.emit(tomodir.OBSERVATION_STATUS[self.status],
                                       self.scanID)
            self.validation = 1
        else:
            self.status = 'waiting for acquisition ending'
            self.sigStatusChanged.emit(tomodir.OBSERVATION_STATUS[self.status],
                                       self.scanID)
            self.validation = 0
        return

    def _getTomoDirProcess(self):
        if self.obsMethod == tomodir.DET_END_XML:
            return _TomoDirProcessXML(dataDir=self.scanID,
                                      srcPattern=self.srcPattern,
                                      destPattern=self.destPattern)
        elif self.obsMethod == tomodir.PARSE_INFO_FILE:
            return _TomoDirProcessParseInfo(dataDir=self.scanID,
                                            srcPattern=self.srcPattern,
                                            destPattern=self.destPattern)
        elif self.obsMethod == tomodir.DET_END_USER_ENTRY:
            return _TomoDirProcessUserFilePattern(dataDir=self.scanID,
                                                  srcPattern=self.srcPattern,
                                                  destPattern=self.destPattern,
                                                  pattern=self.patternObs)
        else:
            raise ValueError('requested observation method not recognized')

    def setSourceToDestinationPatterns(self, srcPattern, destPattern):
        """set the patterns to replace strings sequence in directories path.

        For example during acquisition in md05 acquisition files are stored
        in /lbsram/data/visitor/x but some information (as .info) files are
        stored in /data/visitor/x.
        So we would like to check information in both directories.
        Furthermore we would like that all file not in /data/visitor/x will be
        copied as soon as possible into /data/visitor/x (using RSyncManager)

        To do so we can define a srcPattern ('/lbsram' in our example) and
        destPattern : a string replacing to srcPattern in order to get both
        repositories. ('' in out example)
        If srcPattern or destPattern are setted to None then we won't apply
        this 'two directories' synchronization and check

        :param str srcPattern: the pattern to change by destPattern.
        :param str destPattern: the pattern that will replace srcPattern in the
            scan path
        """
        self.srcPattern = srcPattern
        self.destPattern = destPattern

    def setObservationMethod(self, obsMeth, info=None):
        """
        Set if we are looking for the .xml file

        :param str or tuple obsMeth:
        :param dict info: some extra information needed for some observation
                          method
        """
        assert info is None or type(info) is dict
        assert type(obsMeth) in (tuple, str)
        if type(obsMeth) is str:
            self.obsMethod = obsMeth
            if self.obsMethod == tomodir.DET_END_USER_ENTRY:
                assert 'pattern' in info
                self.patternObs = info['pattern']
            else:
                self.patternObs = None
        else:
            assert len(obsMeth) > 0
            assert type(obsMeth[0]) is str
            self.obsMethod = obsMeth[0]
            if self.obsMethod == tomodir.DET_END_USER_ENTRY:
                assert len(obsMeth) is 2
                assert type(obsMeth[1]) is dict
                assert 'pattern' in obsMeth[1]
                self.patternObs = obsMeth[1]['pattern']
            else:
                self.patternObs = None


class _TomoDirObserver(OWClient, qt.QThread):
    """Thread launching the tomodir process (observation of acquisition)

    :param str headDir: the root dir to make to fin dacquisition
    :param bool startByOldest: if True then we parse folder from the oldest to
        the newest
    :param funcAdvancementHandler: handlers of the signals sended by tomoDIR
        (one for sigNbDirExplored and one for sigAdvanceExploration)
    :param str obsMethod: is True then will the creation of the xml file will
        notice the end of the acquisition. Otherwise we will look for .info
        file and for all .edf file to be copied
    :param str srcPattern: see tomodir
    :param str destPattern: see tomodir
    """

    sigScanReady = qt.Signal(str)
    """Emitted when a scan is ready"""

    def __init__(self, obsMethod,
                 headDir=None, startByOldest=False,
                 srcPattern=None, destPattern=None,
                 ignoredFolders=None):
        OWClient.__init__(self, loggers=logger)
        qt.QThread.__init__(self)
        self.observations = _OngoingObservation()
        self.observations.sigScanReady.connect(self._signalScanReady)
        self.observations.ignoredFolders = [] if ignoredFolders is None else ignoredFolders
        """dict of observer on one specific scanID. Key is the directory,
        value the :class:`TomoDirFixObserver`"""
        self.setHeadFolder(headDir)
        self.setObservationMethod(obsMethod)
        self.srcPattern = srcPattern
        self.destPattern = destPattern
        self.tomodirProcess = None
        self._patternObs = None
        """The pattern to use for the DET_END_USER_ENTRY method"""

    def resetObservations(self):
        self.observations.reset()

    def run(self):
        def process(directory):
            if self.observations.isObserving(directory) is False and \
                    self.tomodirProcess._isScanDirectory(directory) and \
                    directory not in self.observations.ignoredFolders:
                self.observe(directory)

            for f in os.listdir(directory):
                if os.path.isdir(os.path.join(directory, f)):
                    process(os.path.join(directory, f))

        if not os.path.isdir(self.headDir):
            logger.warning('can\'t observe %s, not a directory' % self.headDir)
            return
        self.tomodirProcess = self._getTomoDirProcess()
        process(self.headDir)

        self._processObservation()
        return

    def _signalScanReady(self, scanID):
        self.sigScanReady.emit(scanID)

    def _processObservation(self):
        for dir, thread in self.observations.dict.items():
            thread.start()

    def quit(self):
        for dir, thread in self.observations.dict.items():
            thread.quitting = True

        if self.tomodirProcess is not None:
            self.tomodirProcess.quitting = True
            self.lastObsDir = None
        qt.QThread.quit(self)

    def setObservationMethod(self, obsMeth, info=None):
        """
        Set if we are looking for the .xml file

        :param str or tuple obsMeth:
        :param dict info: some extra information needed for some observation
                          method
        """
        assert info is None or type(info) is dict
        assert type(obsMeth) in (tuple, str)
        if type(obsMeth) is str:
            self.obsMethod = obsMeth
            if self.obsMethod == tomodir.DET_END_USER_ENTRY:
                assert 'pattern' in info
                self._patternObs = info['pattern']
            else:
                self._patternObs = None
        else:
            assert len(obsMeth) > 0
            assert type(obsMeth[0]) is str
            self.obsMethod = obsMeth[0]
            if self.obsMethod == tomodir.DET_END_USER_ENTRY:
                assert len(obsMeth) is 2
                assert type(obsMeth[1]) is dict
                assert 'pattern' in obsMeth[1]
                self._patternObs = obsMeth[1]['pattern']
            else:
                self._patternObs = None

        for dir, thread in self.observations.dict.items():
            thread.setObservationMethod(obsMeth, info=info)

    def setHeadFolder(self, headDir):
        self.headDir = headDir

    def setSourceToDestinationPatterns(self, srcPattern, destPattern):
        """set the patterns to replace strings sequence in directories path.

        For example during acquisition in md05 acquisition files are stored
        in /lbsram/data/visitor/x but some information (as .info) files are
        stored in /data/visitor/x.
        So we would like to check information in both directories.
        Furthermore we would like that all file not in /data/visitor/x will be
        copied as soon as possible into /data/visitor/x (using RSyncManager)

        To do so we can define a srcPattern ('/lbsram' in our example) and
        destPattern : a string replacing to srcPattern in order to get both
        repositories. ('' in out example)
        If srcPattern or destPattern are setted to None then we won't apply
        this 'two directories' synchronization and check

        :param str srcPattern: the pattern to change by destPattern.
        :param str destPattern: the pattern that will replace srcPattern in the
            scan path
        """
        self.srcPattern = srcPattern
        self.destPattern = destPattern
        for dir, thread in self.observations.items():
            thread.setSourceToDestinationPatterns(self.srcPattern,
                                                  self.destPattern)

    def observe(self, scanID):
        observer = _TomoDirFixObserver(scanID=scanID,
                                       obsMethod=self.obsMethod,
                                       srcPattern=self.srcPattern,
                                       destPattern=self.destPattern,
                                       patternObs=self._patternObs)
        self.observations.add(observer)

    def cancelObservation(self, scanID):
        if self.observations.isObserving(scanID) is False:
            logger.warning('Can\'t cancel observation on %s, no observation '
                           'registred' % scanID)
            return

        self.observations.ignoredFolders.append(scanID)
        if scanID in self.observations.dict:
            self.observations.remove(self.observations.dict[scanID])

    def isObserve(self, scanID):
        return self.observations.isObserving(scanID)

    def _getTomoDirProcess(self):
        if self.obsMethod == tomodir.DET_END_XML:
            return _TomoDirProcessXML(dataDir=self.headDir,
                                      srcPattern=self.srcPattern,
                                      destPattern=self.destPattern)
        elif self.obsMethod == tomodir.PARSE_INFO_FILE:
            return _TomoDirProcessParseInfo(dataDir=self.headDir,
                                            srcPattern=self.srcPattern,
                                            destPattern=self.destPattern)
        elif self.obsMethod == tomodir.DET_END_USER_ENTRY:
            return _TomoDirProcessUserFilePattern(dataDir=self.headDir,
                                                  srcPattern=self.srcPattern,
                                                  destPattern=self.destPattern,
                                                  pattern=self._patternObs)
        else:
            raise ValueError('requested observation method not recognized')

    def waitForObservationFinished(self, timeOut=10):
        for dir, thread in self.observations.dict.items():
            thread.wait(timeOut)


class _OngoingObservation(qt.QObject):
    """
    Simple container of observed directory
    """
    sigScanReady = qt.Signal(str)
    """Emitted when a finished acquisition is detected"""

    sigObsAdded = qt.Signal(str)
    """Signal emitted when an observation is added"""
    sigObsRemoved = qt.Signal(str)
    """Signal emitted when an observation is removed"""
    sigObsStatusReceived = qt.Signal(str, str)
    """Signal emitted when receiving a new observation status"""

    def __init__(self):
        qt.QObject.__init__(self)
        self.dict = OrderedDict()
        self.ignoredFolders = []

    def add(self, observer):
        if self.isObserving(observer.scanID) is False:
            assert isinstance(observer, _TomoDirFixObserver)
            self.dict[observer.scanID] = observer
            observer.sigStatusChanged.connect(self._updateStatus)
            self.sigObsAdded.emit(observer.scanID)

    def remove(self, observer):
        assert isinstance(observer, _TomoDirFixObserver)
        if self.isObserving(observer.scanID) is True:
            observer.sigStatusChanged.disconnect(self._updateStatus)
            observer.quit()
            del self.dict[observer.scanID]
            self.sigObsRemoved.emit(observer.scanID)

    def _updateStatus(self, status, scanID):
        if self.isObserving(scanID) is True:
            self.sigObsStatusReceived.emit(scanID,
                                           tomodir.DICT_OBS_STATUS[status])
            if status == tomodir.OBSERVATION_STATUS['acquisition ended']:
                self.ignoredFolders.append(scanID)
                observer = self.dict[scanID]
                self.remove(observer)
                # TODO : disconnect the thread and delete it if finisehd
                #  add the scanID to the one to ignore. Those ignore
                # should be removed at each start and stop of the observation
                self.sigScanReady.emit(scanID)
            if status in (tomodir.OBSERVATION_STATUS['failure'],
                          tomodir.OBSERVATION_STATUS['aborted']):
                observer = self.dict[scanID]
                self.remove(observer)

    def isObserving(self, scanID):
        return scanID in self.dict

    def reset(self):
        # self.ignoreFolders = []
        for scanID, observer in self.dict:
            observer.sigStatusChanged.disconnect(self._updateStatus)
            observer.quit()
        self.dict = {}

    def __len__(self):
        return len(self.dict)
