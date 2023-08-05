#/*##########################################################################
# Copyright (C) 2016-2017 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
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

__author__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "08/06/2017"


from tomwer.core.utils import ftseriesutils
from tomwer.core import settings
from tomwer.core.utils import logconfig
from tomwer.core import utils
from tomwer.core.ftseries import FastSetupDefineGlobals
from tomwer.core.ftseries import Ftseries
from tomwer.web.client import OWClient
from tomwer.core.utils.Singleton import singleton
from silx.gui import qt
from queue import Queue
import logging
import shutil
import os
import tempfile

logger = logging.getLogger(__file__)


@singleton
class ReconstructionStack(Queue, OWClient, qt.QObject):
    """
    Manage a stack of ftseries reconstruction
    """

    sigReconsFinished = qt.Signal(str)
    sigReconsFailed = qt.Signal(str)
    sigReconsMissParams = qt.Signal(str)

    def __init__(self):
        Queue.__init__(self)
        OWClient.__init__(self, logger)
        qt.QObject.__init__(self)
        self.reconsThread = _ReconsFtSeriesThread()
        self.reconsThread.sigThReconsFinished.connect(self._dealWithFinishedRecons)
        self.reconsThread.sigThReconsFailed.connect(self._dealWithFailedRecons)
        self.reconsThread.sigThMissingParams.connect(self._dealWithThMissingParams)
        self._forceSync = False

    def add(self, slices, scanID, reconsParams, schemeTitle):
        """
        add a reconstruction and will run it as soon as possible

        :param list slices: the list of slices to reconstruct
        :param str scanID: the folder of the acquisition to reconstruct
        :param dict reconsParams: parameters of the reconstruction
        """
        Queue.put(self, (slices, scanID, reconsParams, schemeTitle))
        if self.canExecNext():
            self.execNext()

    def execNext(self):
        """Launch the next reconstruction if any
        """
        if Queue.empty(self):
            return

        assert(not self.reconsThread.isRunning())
        slices, scanID, reconsParams, schemeTitle = Queue.get(self)
        self.reconsThread.init(slices, scanID, reconsParams, schemeTitle)
        self.reconsThread.start()
        if self._forceSync is True:
            self.reconsThread.wait()

    def canExecNext(self):
        """
        Can we launch an ftserie reconstruction.
        Reconstruction can't be runned in parallel

        :return: True if no reconstruction is actually running
        """
        return not self.reconsThread.isRunning()

    def _dealWithFinishedRecons(self, scanID):
        info = 'reconstruction %s is finished' % scanID
        logger.info(info)
        self.sigReconsFinished.emit(scanID)
        self.execNext()

    def _dealWithThMissingParams(self, scanID):
        self.sigReconsMissParams.emit(scanID)
        self.execNext()

    def _dealWithFailedRecons(self, scanID):
        self.sigReconsFailed.emit(scanID)
        self.execNext()

    def setMockMode(self, b):
        self.reconsThread.setMockMode(b)
        self.execNext()

    def setForceSync(self, b):
        self._forceSync = True


class _ReconsFtSeriesThread(OWClient, qt.QThread):
    """
    Simple thread launching ftseries reconstructions
    """

    copyH5FileReconsIntoFolder = False
    """if True then copy the file used for reconstruction into the dataset
    folder under the copyH5ReconsName"""

    copyH5ReconsName = "octave_FT_params.h5"
    """Name under wich the reconstruction parameters will be saved if
    'copyH5FileReconsIntoFolder' is active"""

    sigThReconsFinished = qt.Signal(str)
    "Emitted if reconstruction ended with success"
    sigThReconsFailed = qt.Signal(str)
    "Emitted if reconstruction failed"
    sigThMissingParams = qt.Signal(str)
    "Emitted if missing some reconstruction parameters"

    def __init__(self):
        OWClient.__init__(self, logger)
        qt.QThread.__init__(self)
        self.slices = None
        self.scanID = None
        self.reconsParam = None
        self.schemeTitle = None

    def run(self):
        if self.scanID is None or self.reconsParam is None or \
           self.slices is None:
            mess = 'reconstruction not initialized. Can\' reconstruct'
            logger.warning(mess)
            self.sigThReconsFailed.emit(mess)
            return

        if not os.path.isdir(self.scanID):
            mess = '%s is not a valid fodler, can\'t reconstruct'
            self.sigThReconsFailed.emit(mess)
            return

        self._processRecons()

    def init(self, slices, scanID, reconsParam, schemeTitle):
        assert(type(scanID) is str)
        assert (type(reconsParam) is dict)
        self.slices = slices
        self.scanID = scanID
        self.reconsParam = reconsParam
        self.schemeTitle = schemeTitle

        # save the reconstruction parameters in a temporary .h5 file
        self._mockMode = False

    def _processRecons(self):
        self._noticeStart()
        tmpH5File = tempfile.mkstemp(prefix='tmp_workflow',
                                     suffix=".h5",
                                     dir=self.scanID)[1]

        ftseriesutils.saveH5File(h5File=tmpH5File,
                                 structs=self.reconsParam,
                                 displayInfo=False)

        # check is on low memory in lbsram
        if settings.isOnLbsram() and utils.isLowOnMemory(
                settings.LBSRAM_ID) is True:
            # if computer is running into low memory in lbsram skip reconstruction
            mess = 'low memory, skip reconstruction for ' + self.scanID
            logger.processSkipped(mess)
            self.sigThReconsFinished.emit(self.scanID)
        else:
            if self.copyH5FileReconsIntoFolder is True:
                destFile = _ReconsFtSeriesThread.getH5FileCopyName(
                    self.scanID)
                shutil.copyfile(tmpH5File, destFile)
            try:
                # deal with mock reconstruction
                if self._mockMode is True:
                    self.__mockReconstruction()
                else:
                    Ftseries.run_reconstruction(slices=self.slices,
                                                directory=self.scanID,
                                                h5file=tmpH5File)
            except Ftseries.H5NoFileException as e:
                logger.error('Issue : No h5 file found. Shouldn\'t append.',
                             extra={
                                 logconfig.SCAN_ID: self.scanID})

                self.sigThReconsFailed.emit('No h5 file')

            except FastSetupDefineGlobals.H5MissingParameters as e:
                self.sigThMissingParams.emit(self.scanID)
            else:
                os.unlink(tmpH5File)
                self.sigThReconsFinished.emit(self.scanID)

    def _noticeStart(self):
        info = 'start reconstruction of %s' % self.scanID
        logger.info(info,
                    extra={logconfig.SCAN_ID: self.scanID})

    @staticmethod
    def getH5FileCopyName(folderPath):
        return os.path.join(folderPath, _ReconsFtSeriesThread.copyH5ReconsName)

    def __mockReconstruction(self):
        """Run the mocked reconstruction
        Simply create some adapted files
        """
        assert(self.scanID is not None)
        assert(os.path.isdir(self.scanID))
        logger.info('mocking reconstruction',
                    extra={logconfig.SCAN_ID: self.scanID})
        utils.mockReconstruction(self.scanID)

    @staticmethod
    def setCopyH5FileReconsIntoFolder(b):
        global copyH5FileReconsIntoFolder
        copyH5FileReconsIntoFolder = b

    def setMockMode(self, b):
        """If the mock mode is activated then during reconstruction won't call
        Octave script for reconstruction but will generate some output files
        according to convention

        :param boolean b: True if we want to active the mock mode
        """
        self._mockMode = b
