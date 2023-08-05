# coding: utf-8
#/*##########################################################################
# Copyright (C) 2017 European Synchrotron Radiation Facility
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
This module is used to define the process of the reference creator.
This is related to the issue #184
"""

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "05/02/2018"


from tomwer.core.darkref.DarkRefs import DarkRefsWorker, DarkRefs
from silx.gui import qt
import tempfile
import numpy
from tomwer.core import utils
import fabio
import shutil
import os
import logging

logger = logging.getLogger(__file__)


class DarkRefsCopy(DarkRefs):
    """
    Reimplement Dark ref to deal with copy when there is no median/mean files
    """
    def __init__(self):
        super(DarkRefsCopy, self).__init__()
        self.refPrefix = DarkRefs.REFHST_PREFIX
        self.darkPrefix = DarkRefs.DARKHST_PREFIX

        # API exposition
        self.setModeAuto = self.worker.setModeAuto
        self.hasRefStored = self.worker.hasRefStored
        # self.sigRefSetted = self.worker.sigRefSetted
        # self.sigRefRemoved = self.worker.sigRefRemoved
        self.setRefsFromScan = self.worker.setRefsFromScan
        self._hasRef = self.worker._hasRef
        self.getRefHstPrefix = self.worker.getRefHstPrefix
        self.isOnModeAuto = self.worker.isOnModeAuto
        self.setProcessOnlyDkRf = self.worker.setProcessOnlyDkRf
        self.setProcessOnlyCopy = self.worker.setProcessOnlyCopy
        self.clearRef = self.worker.clearRef

    def _createThread(self):
        return DarkRefsCopyWorker()

    def setModeAuto(self, auto):
        self.worker.setModeAuto(auto)

    def _initWorker(self, scanID, params):
        self.worker.init(directory=scanID, params=params,
                         refPrefix=self.refPrefix, darkPrefix=self.darkPrefix)


class DarkRefsCopyWorker(DarkRefsWorker):
    """
    Add to DarkRef the copy of reference if not existing in the given directory
    """
    DEFAULT_SRCURRENT = 200.0  # mA

    sigRefSetted = qt.Signal(str)
    """Signal emitted when some reference are recorded from the given directory
    """
    sigRefRemoved = qt.Signal()
    """Signal emitted when the reference are removed"""

    def __init__(self, *args, **kwargs):
        DarkRefsWorker.__init__(self, *args, **kwargs)
        self._modeAuto = True
        self._savedir = tempfile.mkdtemp()
        info = 'Ref copy will store files in ' + self._savedir
        logger.info(info)
        """directory saved to store the dark and refHST reference files"""
        self._refHstPrefix = DarkRefs.REFHST_PREFIX
        self._darkHstPrefix = DarkRefs.DARKHST_PREFIX
        self._refHST = None
        self._darkHST = None
        self._processOnlyCopy = False
        self._processOnlyDkRf = False
        self._refScan = ''

    def init(self, directory, params, refPrefix, darkPrefix):
        self.refPrefix = refPrefix
        self.darkPrefix = darkPrefix
        DarkRefsWorker.init(self, directory=directory, params=params)

    def setProcessOnlyDkRf(self, value):
        # TODO: rework this part
        self._processOnlyCopy = False
        self._processOnlyDkRf = value

    def setProcessOnlyCopy(self, value):
        # TODO: rework this part. Maybe having the two process (DarkRef
        # creation and copy) separated would be better and easier to manage
        self._processOnlyDkRf = False
        self._processOnlyCopy = value

    def setRefsFromScan(self, scanID):
        if os.path.isdir(scanID) is False:
            w = 'given path (%s) is not a directory. Can\'t extract ref' % scanID
            logger.warning(w)
            return False

        self.directory = scanID
        self._refScan = scanID
        if self._hasRef(scanID) is False:
            self._noticeUserNoRefMessage(fileType='flat field', dir=scanID)
            return False
        else:
            self.cleanSaveFiles()
            darkHSTFiles = sorted(DarkRefs.getDarkHSTFiles(scanID,
                                                           prefix=self.getDarkHstPrefix()))
            refHSTFiles = sorted(DarkRefs.getRefHSTFiles(scanID,
                                                         prefix=self.getRefHstPrefix()))
            if len(darkHSTFiles) is 0:
                self._noticeUserNoRefMessage(fileType='dark', dir=scanID)
            else:
                self._createDarkRef(darkHSTFiles[0])

            if len(refHSTFiles) is 0:
                self._noticeUserNoRefMessage(fileType='flat field', dir=scanID)
            else:
                self._createFlatFieldRef(refHSTFiles[0])

            """warning: dark should always be saved first because used for
            saving ref
            """
            self.sigRefSetted.emit(scanID)
            return True

    def _copyTo(self, scanID):
        if os.path.isdir(scanID) is False:
            logger.warning(scanID + ' is not a directory. Cannot copy '
                                    'reference to it.')
            return
        if self.hasRefStored() is False:
            logger.error('No reference registred to be copy in %s' % scanID)
            return

        # warning: get information if there is ref or dark before copying
        # because can bring interferences.
        _hasRef = self._hasRefHSTRef(scanID)
        _hasDark = self._hasDarkHSTRef(scanID)
        if _hasDark is False:
            self._copyDarkTo(scanID)
        if _hasRef is False:
            self._copyRefTo(scanID)

    def _copyDarkTo(self, scanID):
        """The dark is copied without normalization"""
        assert self._darkHST is not None
        if os.path.isfile(self._darkHST) is False:
            logger.error(self._darkHST + ' is not a file. Cannot be used as '
                                         'reference for dark')
            return
        if os.path.isdir(scanID) is False:
            logger.error(scanID + ' is not a directory, cannot copy dark.')
            return
        else:
            # do never copy on an existing file (meaning ref already here)
            dst = os.path.join(scanID, os.path.basename(self._darkHST))
            if os.path.isfile(dst) is False:
                shutil.copy(src=self._darkHST, dst=dst)

    def _copyRefTo(self, outputdir):
        assert os.path.isdir(outputdir)
        assert self._darkHST is not None

        def normalize(data, when):
            """normalize from dark_end and getting the SRCurrent at start or
            end"""
            assert when in ('start', 'end')
            assert os.path.isfile(self._darkHST)

            with fabio.open(self._darkHST) as file_desc:
                darkData = file_desc.data
            srCurrent = utils.getSRCurrent(outputdir, when=when)
            if srCurrent is None:
                logger.warning('Can\'t find information about srCurrent,'
                               'set to default value')
                srCurrent = self.DEFAULT_SRCURRENT
            if data.shape != darkData.shape:
                logger.warning('Image and dark have different shapes.'
                               'Cannot normalize. (Dark ref file in %s)'
                               '' % self._darkHST)
                return data, srCurrent
            return (data * srCurrent).astype(numpy.float32) + darkData, srCurrent

        data = fabio.open(self._refHST).data
        header = fabio.open(self._refHST).header
        tomo_N = utils.getTomo_N(outputdir)
        if tomo_N in (None, -1):
            logger.error('Can\'t find the number of projection. '
                         'Fail to create reference')
        end_acqui = str(utils.getTomo_N(outputdir)).zfill(4)
        indexRefFile = {'start': '0000', 'end': end_acqui}
        for when in ('start', 'end'):
            fileName = DarkRefs.REFHST_PREFIX + indexRefFile[when] + '.edf'
            filePath = os.path.join(outputdir, fileName)
            # do never copy on an existing file (meaning ref already here)
            if os.path.isfile(filePath):
                continue
            _data, _srCurrent = normalize(data, when)

            _header = header.copy()
            # add some extra information on the header
            _header['SRCUR'] = _srCurrent
            file_desc = fabio.edfimage.EdfImage(data=_data, header=_header)
            file_desc.write(filePath, force_type=numpy.int32)

    def _noticeUserNoRefMessage(self, fileType, dir):
        logger.warning(self._getNoRefMessage(fileType, dir))

    def _getNoRefMessage(self, fileType, dir):
        mess = "No %s found in the given directory %s. Won't be able to copy" \
               " them" % (fileType, dir)
        return mess

    def _createFlatFieldRef(self, _file):
        """
        Copy the data contained in _file in the given file to the `_savedir`
        and normalize the data from SRCurrent (intensity
        )"""
        def normalize(data):
            assert os.path.isfile(self._darkHST)
            with fabio.open(self._darkHST) as file_desc:
                darkData = file_desc.data
            srCurrent = utils.getClosestSRCurrent(scan=os.path.dirname(_file),
                                                  refFile=_file)
            if data.shape != darkData.shape:
                err = 'cannot normalize data from %s, has different ' \
                      'dimensions' % (self._darkHST)
                logger.error(err)
                return data, srCurrent
            if srCurrent in (None, -1):
                logger.warning('Can\'t find information about srCurrent,'
                               'set to default value for normalization')
                srCurrent = self.DEFAULT_SRCURRENT
            return (data - darkData).astype(numpy.float32) / srCurrent, srCurrent

        with fabio.open(_file) as file_desc:
            data = file_desc.data
            header = file_desc.header
        data, srCurrent = normalize(data)

        # add some extra information on the header
        header['tomwer info'] = 'copied using refCopy'
        header['original srcurrent'] = srCurrent
        header['original scan'] = self._refScan
        header['SRCUR'] = -1

        file_desc = fabio.edfimage.EdfImage(data=data,
                                            header=header)
        self._refHST = os.path.join(self._savedir, os.path.basename(_file))
        file_desc.write(self._refHST, force_type=numpy.float32)

    def _createDarkRef(self, _file):
        self._darkHST = os.path.join(self._savedir, os.path.basename(_file))
        shutil.copy(src=_file,
                    dst=self._darkHST)
        # add origin of the dark file
        with fabio.open(self._darkHST) as dsc:
            _header = dsc.header
            _header['original scan'] = self._refScan
            _data = dsc.data

        dsc = fabio.edfimage.EdfImage(data=_data, header=_header)
        dsc.write(self._darkHST)

    def __del__(self):
        shutil.rmtree(self._savedir)

    def cleanSaveFiles(self):
        for f in os.listdir(self._savedir):
            if os.path.isfile(f) and os.path.exists(f):
                os.remove(f)

    def process(self):
        """
        This is function triggered when a new scan / data is received.
        As explained in issue #184 the behavior is the following:

        * if the scan has already ref files files won't be overwrite
        * if the mode is in `auto` will register last ref file met
        * if the scan has no ref files and refCopy has some register. Will
          create a copy of those, normalized from srCurrent (for flat field)
        """
        if self.directory is None:
            return
        if self._processOnlyCopy is False:
            DarkRefsWorker.process(self)
        if self._processOnlyDkRf is False:
            if self._hasRef(self.directory) is True:
                if self._modeAuto is True:
                    self.setRefsFromScan(self.directory)
            if self._hasMissingRef(self.directory) is True:
                self._copyTo(self.directory)

    def hasRefStored(self):
        return self._refHST is not None and self._darkHST is not None

    def _hasDarkHSTRef(self, scanID):
        return len(DarkRefs.getDarkHSTFiles(scanID,
                                            prefix=self.getDarkHstPrefix())) > 0
    def _hasRefHSTRef(self, scanID):
        return len(DarkRefs.getRefHSTFiles(scanID,
                                           prefix=self.getRefHstPrefix())) > 0

    def _hasRef(self, scanID):
        return self._hasDarkHSTRef(scanID) or self._hasRefHSTRef(scanID)

    def _hasMissingRef(self, scanID):
        return not self._hasDarkHSTRef(scanID) or not self._hasRefHSTRef(scanID)

    def _signalDone(self, scanID):
        raise NotImplementedError('Abstract class')

    def setModeAuto(self, b):
        self._modeAuto = b

    def isOnModeAuto(self):
        return self._modeAuto

    def _getRefList(self):
        return os.listdir(self._savedir)

    def getRefHstPrefix(self):
        return self._refHstPrefix

    def getDarkHstPrefix(self):
        return self._darkHstPrefix

    def setRefHstPrefix(self, prefix):
        self._refHstPrefix = prefix

    def setDarkHstPrefix(self, prefix):
        self._darkHstPrefix = prefix

    def clearRef(self):
        self._refHST = None
        self._darkHST = None
        self._refScan = ''
        self.sigRefRemoved.emit()


class DarkRefCopyP(DarkRefsCopy, qt.QObject):
    """QObject used for test and for the no-gui workflow"""

    sigScanReady = qt.Signal(str)

    def __init__(self):
        DarkRefsCopy.__init__(self)
        qt.QObject.__init__(self)
