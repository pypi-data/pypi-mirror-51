# coding: utf-8
# ##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
# ###########################################################################

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "18/06/2017"

from .BaseProcess import BaseProcess
from tomwer.core.ftseries.FtserieReconstruction import FtserieReconstruction
from tomwer.core import settings
from tomwer.core import utils
from tomwer.core.WaiterThread import WaiterThread
from tomwer.core.utils import logconfig
from silx.gui import qt
from collections import OrderedDict
import logging

logger = logging.getLogger(__file__)


class ScanValidator(BaseProcess):
    """
    Simple workflow locker until the use validate scans

    :param int memReleaserWaitLoop: the time to wait in second between two
                                    memory overload if we are in lbsram.
    """

    inputs = [{'name': "data",
               'type': str,
               'handler': 'addScan'}
              ]
    outputs = [
        {'name': "change recons params",
         'type': FtserieReconstruction,
         'doc': "signal emitted when the used ask for setting new reconstruction parameters"},
        {'name': "data",
         'type': str,
         'doc': "signal emitted when the scan is completed"},
        # {'name': "scanCanceledAt",
        #  'type': str,
        #  'doc': "signal emitted when the scan is canceled"},
    ]

    WAIT_TIME_MEM_REL = 20
    """Time (in sec) to wait to check if the scan validator has to release his
    stack of scans. This is a securitu to make sure we are not keeping
    unecessary data during an acquisition in lbsram"""

    def __init__(self, memReleaserWaitLoop=WAIT_TIME_MEM_REL):
        BaseProcess.__init__(self, logger)
        self._scansToValidate = OrderedDict()
        self._manualValidation = True
        self._hasToLimitScanBlock = settings.isOnLbsram()
        """If we are on lbsram we want to look each n seconds if we have to
        release scan in the case of a disk overload."""
        if self._hasToLimitScanBlock:
            self._memoryReleaser = WaiterThread(memReleaserWaitLoop)
            self._memoryReleaser.finished.connect(self._loopMemoryReleaser)
            self._memoryReleaser.start()
        else:
            self._memoryReleaser = None

    def __del__(self):
        if self._memoryReleaser is not None:
            self._memoryReleaser.should_be_stopped = True
            self._memoryReleaser.wait()

    @property
    def lastReceivedRecons(self):
        return list(self._scansToValidate.values())[0]

    def addScan(self, ftserie):
        """
        Return the index on the current orderred dict

        :param ftserie:
        :return:
        """
        _ftserie = ftserie
        if type(ftserie) is str:
            _ftserie = FtserieReconstruction(_ftserie)
        info = 'Scan %s has been added by the Scan validator' % _ftserie.scanID
        logger.info(info)

        _ftserie = ftserie
        if type(ftserie) is str:
            _ftserie = FtserieReconstruction(_ftserie)
        self._scansToValidate[_ftserie.scanID] = _ftserie
        index = len(self._scansToValidate) -1

        self._freeStackIfNeeded()
        return index

    def _freeStackIfNeeded(self):
        # if we are low in memory in lbsram: we will automatically validate the current scan
        isLowMemoryLbs = (settings.isOnLbsram() and utils.isLowOnMemory(settings.LBSRAM_ID) is True)
        if isLowMemoryLbs or (not self.isValidationManual()):
            if isLowMemoryLbs:
                mess = 'low memory, free ScanValidator stack '
                logger.processSkipped(mess)
            self._validateStack()

    def _loopMemoryReleaser(self):
        """
        simple loop using the _memoryReleaser and calling the
        _freeStackIfNeeded function
        """
        self._freeStackIfNeeded()
        if self._memoryReleaser and not hasattr(self._memoryReleaser,
                                                'should_be_stopped'):
            self._memoryReleaser.start()

    def _validateStack(self):
        """Validate all the scans in the stack."""
        for scanID in list(self._scansToValidate.keys()):
            self._validated(scanID)

        assert(len(self._scansToValidate) == 0)

    def _validateScan(self, scanID):
        """This will validate the ftserie currently displayed

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate.
            Execution order in this case is not insured.
        """
        if scanID is not None:
            self._validated(scanID)

    def _cancelScan(self, scanID):
        """This will cancel the ftserie currently displayed

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate.
            Execution order in this case is not insured.
        """
        if scanID is not None:
            self._canceled(scanID)

    def _redoAcquisitionScan(self, scanID):
        """This will emit a signal to request am acquisition for the current
        ftSerieReconstruction

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate.
            Execution order in this case is not insured.
        """
        if scanID is not None:
            self._redoacquisition(scanID)

    # ------ callbacks -------
    def _validated(self, scanID):
        """Callback when the validate button is pushed"""
        if scanID is not None:
            info = '%s has been validated' % scanID
            logger.processEnded(info,
                                extra={
                                    logconfig.DOC_TITLE: self._scheme_title,
                                    logconfig.SCAN_ID: scanID})
            self._sendScanReady(scanID)
            # in some case the scanID can not be in the _scansToValidate
            # (if the signal) come from an other window that 'scan to treat'
            if scanID in self._scansToValidate:
                del self._scansToValidate[scanID]

    def _canceled(self, scanID):
        """Callback when the cancel button is pushed"""
        if scanID is not None:
            info = '%s has been canceled' % scanID
            logger.processEnded(info,
                                extra={
                                    logconfig.DOC_TITLE: self._scheme_title,
                                    logconfig.SCAN_ID: scanID})
            # self._sendScanCanceledAt(scanID)
            # in some case the scanID can not be in the _scansToValidate
            # (if the signal) come from an other window that 'scan to treat'
            if scanID in self._scansToValidate:
                del self._scansToValidate[scanID]

    def _redoacquisition(self, ftserie):
        """Callback when the redo acquisition button is pushed"""
        raise NotImplementedError('_redoacquisition not implemented yet')

    def _changeReconsParam(self, ftserie):
        """Callback when the change reconstruction button is pushed"""
        if ftserie is None:
            return

        _ftserie = ftserie
        if type(ftserie) is str:
            _ftserie = FtserieReconstruction(_ftserie)

        if _ftserie.scanID in self._scansToValidate:
            del self._scansToValidate[_ftserie.scanID]
        self._sendUpdateReconsParam(_ftserie)

    def setProperties(self, properties):
        # no properties/settings to be loaded
        pass

    def setManualValidation(self, b):
        """if the validation mode is setted to manual then we will wait for
        user approval before validating. Otherwise each previous and next scan
        will be validated

        :param boolean b: False if we want an automatic validation
        """
        self._manualValidation = b
        if not self.isValidationManual():
            self._validateStack()

    def isValidationManual(self):
        """

        :return: True if the validation is waiting for user interaction,
                 otherwise False
        """
        return self._manualValidation

    def _sendScanReady(self):
        raise RuntimeError("ScanValidator is a pure virtual class.")

    def _sendScanCanceledAt(self):
        raise RuntimeError("ScanValidator is a pure virtual class.")

    def _sendUpdateReconsParam(self):
        raise RuntimeError("ScanValidator is a pure virtual class.")


class ScanValidatorP(ScanValidator, qt.QObject):
    """
    For now to avoid multiple inheritance from QObject with the process widgets
    we have to define two classes. One only for the QObject inheritance.

    :param int memReleaserWaitLoop: the time to wait in second between two
                                    memory overload if we are in lbsram.
    """

    scanReady = qt.Signal(str)
    """Signal emitted when a scan is ready"""
    scanCanceledAt = qt.Signal(str)
    """Signal emitted when a scan has been canceled"""
    updateReconsParam = qt.Signal(FtserieReconstruction)
    """Signal emitted when a scan need to be reconstructed back with new
    parameters"""


    def __init__(self, memReleaserWaitLoop=ScanValidator.WAIT_TIME_MEM_REL):
        ScanValidator.__init__(self, memReleaserWaitLoop)
        qt.QObject.__init__(self)

    def _sendScanReady(self, scanID):
        self.scanReady.emit(scanID)

    def _sendScanCanceledAt(self, scanID):
        self.scanCanceledAt.emit(scanID)

    def _sendUpdateReconsParam(self, ftserie):
        self.updateReconsParam.emit(ftserie)
