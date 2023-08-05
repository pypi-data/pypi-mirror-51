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
This module provides global definitions and functions to manage dark and flat fields
especially for tomo experiments and workflows
"""

__authors__ = ["C. Nemoz", "H.Payno"]
__license__ = "MIT"
__date__ = "06/09/2017"

import logging
import os
import re
from glob import glob
import fabio
import numpy
from queue import Queue
from silx.gui import qt
from tomwer.core import settings
from tomwer.core.BaseProcess import BaseProcess
from tomwer.core.ReconsParams import ReconsParam
from tomwer.web.client import OWClient
from tomwer.core.RSyncManager import RSyncManager
from tomwer.core.utils import getDARK_N
from tomwer.core import utils
import functools


logger = logging.getLogger(__name__)


class DarkRefs(BaseProcess, Queue, qt.QObject):
    """Compute median/mean dark and ref from originals (dark and ref files)
    """

    inputs = [
        {
            'name': "data",
            'type': str,
            'handler': 'process'
        }
    ]

    outputs = [
        {
            'name': "data",
            'type': str
        }
    ]

    CALC_NONE = 'None'

    CALC_MEDIAN = 'Median'

    CALC_AVERAGE = 'Average'

    CALC_MODS_DICT = {
        0: CALC_NONE,
        1: CALC_AVERAGE,
        2: CALC_MEDIAN
    }
    """calc is the methos(none=0, average=1, median = 2),
    if not none default is to keep original files"""

    CALC_MODS = CALC_MODS_DICT.values()

    WHAT_REF = 'refs'
    WHAT_DARK = 'dark'

    VALID_WHAT = (WHAT_REF, WHAT_DARK)
    """Tuple of valid option for What"""

    REFHST_PREFIX = 'refHST'

    DARKHST_PREFIX = 'dark.edf'
    """Warning: here define the extension to in order to make difference
    between darkendXXXX.edf and dark.edf. dark only is not enough"""

    info_suffix = '.info'

    sigScanReady = qt.Signal(str)

    sigUpdated = qt.Signal()
    """Emitted when updated when reconstruction parameters are changed"""

    def __init__(self, file_ext='.edf'):
        """

        :param what:
        :param file_ext:
        :param list or tuple calcMod: For each what (ref, dark) specify the way
                                      to compute it
        """
        self.reconsParams = ReconsParam()

        BaseProcess.__init__(self, logger)
        Queue.__init__(self)
        qt.QObject.__init__(self)
        self._forceSync = False
        self.reconsParams.sigChanged.connect(self._updateReconsParam)

        self.currentParams = _DarkRefParam()
        self._updateReconsParam()

        self.currentParams.file_ext = file_ext

        self.setRemoveOption(self.currentParams.rm)
        self.setSkipIfExisting(self.currentParams.skipIfExist)

        self.worker = self._createThread()

    def _createThread(self):
        return DarkRefsWorker()

    def _updateReconsParam(self):
        self.currentParams.darkMode = self.reconsParams.getValue(structID='DKRF',
                                                                 paramID='DARKCAL')
        self.currentParams.refMode = self.reconsParams.getValue(structID='DKRF',
                                                                paramID='REFSCAL')
        self.currentParams.patternDark = self.reconsParams.getValue(structID='DKRF',
                                                                    paramID='DKFILE')
        self.currentParams.patternRef = self.reconsParams.getValue(structID='DKRF',
                                                                   paramID='RFFILE')
        self.currentParams.rm = self.reconsParams.getValue(structID='DKRF',
                                                           paramID='REFSRMV')
        self.currentParams.skipIfExist = not bool(
            self.reconsParams.getValue(structID='DKRF', paramID='REFSOVE'))
        self.sigUpdated.emit()

    def disconnect(self):
        self.reconsParams.sigChanged.disconnect(self._updateReconsParam)

    def connect(self):
        self.reconsParams.sigChanged.connect(self._updateReconsParam)

    def setRemoveOption(self, rm):
        """
        Define the _rm option, If true then will remove the dark and/or ref if
        already exist before processing
        """
        self.currentParams.rm = rm
        self.reconsParams.setValue(structID='DKRF', paramID='REFSRMV', value=rm)
        self.reconsParams.setValue(structID='DKRF', paramID='DARKRMV', value=rm)

    def setSkipIfExisting(self, skip):
        """
        Define the _skipIfExists option, If true then will skip the processing
        of dark and/or ref files if are already in there.
        """
        self.currentParams.skipIfExist = skip
        self.reconsParams.setValue(structID='DKRF',
                                   paramID='REFSOVE',
                                   value=int(not skip))
        self.reconsParams.setValue(structID='DKRF',
                                   paramID='DARKSOVE',
                                   value=int(not skip))

    def setDarkMode(self, mode):
        assert mode in self.CALC_MODS
        self.currentParams.darkMode = mode
        self.reconsParams.setValue(structID='DKRF',
                                   paramID='DARKCAL',
                                   value=mode)

    def setRefMode(self, mode):
        assert mode in self.CALC_MODS
        self.currentParams.refMode = mode
        self.reconsParams.setValue(structID='DKRF',
                                   paramID='REFSCAL',
                                   value=mode)

    def setPatternDark(self, pattern=None):
        if pattern is None:
            return
        self.currentParams.patternDark = pattern
        self.reconsParams.setValue(structID='DKRF',
                                   paramID='DKFILE',
                                   value=pattern)

    def setPatternRef(self, pattern=None):
        if pattern is None:
            return
        self.currentParams.patternRef = pattern
        self.reconsParams.setValue(structID='DKRF',
                                   paramID='RFFILE',
                                   value=pattern)

    def setPatternRecons(self, pattern):
        self._patternReconsFile = pattern

    def _signalScanReady(self, scanID):
        self.sigScanReady.emit(scanID)
        self.execNext()

    def process(self, scanID):
        if scanID is None:
            return
        Queue.put(self, (scanID, self.currentParams))
        if self.canExecNext():
            self.execNext()

    def execNext(self):
        """Launch the next reconstruction if any
        """
        if super(DarkRefs, self).empty():
            return

        assert(self.worker is None or not self.worker.isRunning())
        scanID, params = Queue.get(self)
        self._initWorker(scanID=scanID, params=params)
        self._launchWorker()

    def _launchWorker(self):
        callback = functools.partial(self._signalScanReady,
                                     self.worker.directory)
        self.worker.finished.connect(callback)
        self.worker.start()
        if self._forceSync is True:
            self.worker.wait()

    def _initWorker(self, scanID, params):
        self.worker.init(directory=scanID, params=params)

    def canExecNext(self):
        """
        Can we launch an ftserie reconstruction.
        Reconstruction can't be runned in parallel

        :return: True if no reconstruction is actually running
        """
        return not self.worker.isRunning()

    def setForceSync(self, b):
        self._forceSync = True
        self.worker._forceSync = True

    @staticmethod
    def getRefHSTFiles(directory, file_ext='.edf', prefix=REFHST_PREFIX):
        """

        :return: the list of existing refs files in the directory according to
                 the file pattern.
        """
        res = []
        if os.path.isdir(directory) is False:
            logger.error(directory + ' is not a directory. Cannot extract '
                                     'RefHST files')
            return res

        for file in os.listdir(directory):
            if file.startswith(prefix) and file.endswith(
                    file_ext):
                res.append(os.path.join(directory, file))
                assert os.path.isfile(res[-1])
        return res

    @staticmethod
    def getDarkHSTFiles(directory, file_ext='.edf', prefix=DARKHST_PREFIX):
        """

        :return: the list of existing refs files in the directory according to
                 the file pattern.
         """
        res = []
        if os.path.isdir(directory) is False:
            logger.error(directory + ' is not a directory. Cannot extract '
                                     'DarkHST files')
            return res
        for file in os.listdir(directory):
            _prefix = prefix
            if prefix.endswith(file_ext):
                _prefix = prefix.rstrip(file_ext)
            if file.startswith(_prefix) and file.endswith(file_ext):
                _file = file.lstrip(_prefix).rstrip(file_ext)
                if _file == '' or _file.isnumeric() is True:
                    res.append(os.path.join(directory, file))
                    assert os.path.isfile(res[-1])
        return res

    @staticmethod
    def getDarkPatternTooltip():
        return 'define the pattern to find, using the python `re` library.\n' \
               'For example: \n' \
               '   - `.*conti_dark.*` to filter files containing `conti_dark` sentence\n' \
               '   - `darkend[0-9]{3,4}` to filter files named `darkend` followed by three or four digit characters (and having the .edf extension)'

    @staticmethod
    def getRefPatternTooltip():
        return 'define the pattern to find, using the python `re` library.\n' \
               'For example: \n' \
               '   - `.*conti_ref.*` for files containing `conti_dark` sentence\n' \
               '   - `ref*.*[0-9]{3,4}_[0-9]{3,4}` to filter files named `ref` followed by any character and ending by X_Y where X and Y are groups of three or four digit characters.'


class _DarkRefParam(object):
    def __init__(self):
        self.darkMode = None
        self.refMode = None
        self.skipIfExist = None
        self.rm = None
        self.patternDark = None
        self.patternRef = None


class DarkRefsWorker(OWClient, qt.QThread):
    """Worker of the Dark refs"""

    TOMO_N = "TOMO_N"

    def __init__(self):
        OWClient.__init__(self, logger)
        qt.QThread.__init__(self)
        self.params = None
        self._forceSync = False
        self.directory = None

    def init(self, directory, params):
        self.directory = directory
        self.params = params

    def run(self):
        self.process()

    def process(self):
        if settings.isOnLbsram() and utils.isLowOnMemory(
                settings.LBSRAM_ID) is True:
            mess = 'low memory, do compute dark and flat field mean/median ' \
                   'for %s' % self.directory
            logger.processSkipped(mess)
            return

        if not(self.directory and
               os.path.exists(self.directory) and
               os.path.isdir(self.directory)):
            logger.warning("folder %s is not existing" % self.directory)
            return

        assert self.params is not None
        whats = (DarkRefs.WHAT_REF, DarkRefs.WHAT_DARK)
        modes = (self.params.refMode, self.params.darkMode)
        for what, mode in zip(whats, modes):
            self._originalsDark = []
            self._originalsRef = []
            self.compute(directory=self.directory, what=what, mode=mode)

    def compute(self, directory, what, mode):
        """Compute the requested what in the given mode for `directory`

        :param str directory: path of the scan
        :param what: what to compute (ref or dark)
        :param mode: how to compute it (median or average...)
        """

        def removeFiles():
            """Remove orignals files fitting the what (dark or ref)"""
            if what is DarkRefs.WHAT_DARK:
                # In the case originals has already been found for the median
                # calculation
                if len(self._originalsDark) > 0:
                    files = self._originalsDark
                else:
                    files = getOriginals(DarkRefs.WHAT_DARK)
            elif what is DarkRefs.WHAT_REF:
                if len(self._originalsRef) > 0:
                    files = self._originalsRef
                else:
                    files = getOriginals(DarkRefs.WHAT_REF)
            else:
                logger.error(
                    'the requested what (%s) is not recognized. '
                    'Can\'t remove corresponding file' % what)
                return

            _files = set(files)
            if len(files) > 0:
                logger.info('ask RSyncManager for removal of %s files in %s' % (what, directory))
                # for lbsram take into account sync from tomodir
                if directory.startswith(settings.LBSRAM_ID):
                    for f in files:
                        _files.add(f.replace(settings.LBSRAM_ID,
                                             settings.DEST_ID,
                                             1))
                RSyncManager().removeSyncFiles(dir=directory,
                                              files=_files,
                                              block=self._forceSync)

        def getOriginals(what):
            if what is DarkRefs.WHAT_REF:
                pattern = re.compile(self.params.patternRef)
            elif what is DarkRefs.WHAT_DARK:
                pattern = re.compile(self.params.patternDark)
            filelist_fullname = []
            for file in os.listdir(directory):
                if pattern.match(file) and file.endswith(self.params.file_ext):
                    if (file.startswith(DarkRefs.REFHST_PREFIX) or
                            file.startswith(DarkRefs.DARKHST_PREFIX)) is False:
                        filelist_fullname.append(os.path.join(directory, file))
            return sorted(filelist_fullname)

        def setup():
            """setup parameter to process the requested what

            :return: True if there is a process to be run, else false
            """
            def getNDigits(_file):
                file_without_scanID = _file.replace(os.path.basename(directory), '')
                return len(re.findall(r'\d+', file_without_scanID))

            def dealWithPCOTomo():
                filesPerSerie = {}
                if self.nfiles % self.nacq is 0:
                    assert self.nacq < self.nfiles
                    self.nseries = self.nfiles // self.nacq
                    self.series = self.fileNameList
                else:
                    logger.warning('Fail to deduce series')
                    return None, None

                linear = getNDigits(self.fileNameList[0]) < 2
                if linear is False:
                    # which digit pattern contains the file number?
                    lastone = True
                    penulti = True
                    for first_files in range(self.nseries - 1):
                        digivec_1 = re.findall(r'\d+', self.fileNameList[
                            first_files])
                        digivec_2 = re.findall(r'\d+', self.fileNameList[
                            first_files + 1])
                        if lastone:
                            lastone = (
                            (int(digivec_2[-1]) - int(digivec_1[-1])) == 0)
                        if penulti:
                            penulti = (
                            (int(digivec_2[-2]) - int(digivec_1[-2])) == 0)

                    linear = not penulti

                if linear is False:
                    digivec_1 = re.findall(r'\d+', self.fileNameList[
                        self.nseries - 1])
                    digivec_2 = re.findall(r'\d+',
                                           self.fileNameList[self.nseries])
                    # confirm there is 1 increment after self.nseries in the uperlast last digit patern
                    if ((int(digivec_2[-2]) - int(digivec_1[-2])) != 1):
                        linear = True

                # series are simple sublists in main filelist
                # self.series = []
                if linear is True:
                    is_there_digits = len(
                        re.findall(r'\d+', self.fileNameList[0])) > 0
                    if is_there_digits:
                        serievec = set(
                            [re.findall(r'\d+', self.fileNameList[0])[-1]])
                    else:
                        serievec = set(['0000'])
                    for i in range(self.nseries):
                        if is_there_digits:
                            serie = re.findall(r'\d+',
                                                    self.fileNameList[
                                                             i * self.nacq])[
                                                  -1]
                            serievec.add(serie)
                            filesPerSerie[serie] = self.fileNameList[i * self.nacq:(i+1)*self.nacq]
                        else:
                            serievec.add('%04d' % i)
                # in the sorted filelist, the serie is incremented, then the acquisition number:
                else:
                    self.series = self.fileNameList[0::self.nseries]
                    serievec = set(
                        [re.findall(r'\d+', self.fileNameList[0])[-1]])
                    for serie in serievec:
                        # serie = re.findall(r'\d+', self.fileNameList[i])[-1]
                        # serievec.add(serie)
                        filesPerSerie[serie] = self.fileNameList[0::self.nseries]
                serievec = list(sorted(serievec))

                if len(serievec) > 2:
                    logger.error('DarkRefs do not deal with multiple scan.'
                                     ' (scan %s)' % directory)
                    return None, None
                assert len(serievec) <= 2
                if len(serievec) > 1:
                    key = serievec[-1]
                    tomoN = self.getInfo(self.TOMO_N)
                    if tomoN is None:
                        logger.error("Fail to found information %s. Can't "
                                     "rename %s" % (self.TOMO_N, key))
                    del serievec[-1]
                    serievec.append(str(tomoN).zfill(4))
                    filesPerSerie[serievec[-1]] = filesPerSerie[key]
                    del filesPerSerie[key]
                    assert len(serievec) is 2
                    assert len(filesPerSerie) is 2

                return serievec, filesPerSerie

            # start setup function
            if mode == DarkRefs.CALC_NONE:
                return False
            if what == 'dark':
                self.out_prefix = DarkRefs.DARKHST_PREFIX
                self.info_nacq = 'DARK_N'
            else:
                self.out_prefix = DarkRefs.REFHST_PREFIX
                self.info_nacq = 'REF_N'

            # init
            self.nacq = 0
            """Number of acquisition runned"""
            self.files = 0
            """Ref or dark files"""
            self.nframes = 1
            """Number of frame per ref/dark file"""
            self.serievec = ['0000']
            """List of series discover"""
            self.filesPerSerie = {}
            """Dict with key the serie id and values list of files to compute
            for median or mean"""
            self.infofile = ''
            """info file of the acquisition"""

            # sample/prefix and info file
            self.prefix = os.path.basename(directory)
            extensionToTry = (DarkRefs.info_suffix, '0000' + DarkRefs.info_suffix)
            for extension in extensionToTry:
                infoFile = os.path.join(directory, self.prefix + extension)
                if os.path.exists(infoFile):
                    self.infofile = infoFile
                    break

            if self.infofile == '':
                logger.debug('fail to found .info file for %s' % directory)

            """
            Set filelist
            """

            # do the job only if not already done and overwrite not asked
            self.out_files = sorted(
                glob(directory + os.sep + '*.' + self.params.file_ext))

            self.filelist_fullname = getOriginals(what)
            self.fileNameList = []
            [self.fileNameList.append(os.path.basename(_file)) for _file in self.filelist_fullname]
            self.fileNameList = sorted(self.fileNameList)
            self.nfiles = len(self.filelist_fullname)
            # if nothing to process
            if self.nfiles == 0:
                logger.info('no %s for %s, because no file to compute found' % (what, directory))
                return False

            self.fid = fabio.open(self.filelist_fullname[0])
            self.nframes = self.fid.getNbFrames()
            self.nacq = 0
            # get the info of number of acquisitions
            if self.infofile != '':
                #self.nacq = getTomo_N(directory) # from tomwer.core.utils import getTomo_N
                self.nacq = self.getInfo(self.info_nacq)

            if self.nacq == 0:
                self.nacq = self.nfiles

            self.nseries = 1
            if self.nacq > self.nfiles:
                # get ready for accumulation and/or file multiimage?
                self.nseries = self.nfiles
            if self.nacq < self.nfiles and getNDigits(self.fileNameList[0]) < 2:
                self.nFilePerSerie = self.nseries
                self.serievec, self.filesPerSerie = dealWithPCOTomo()
            else:
                self.series = self.fileNameList
                self.serievec = _getSeriesValue(self.fileNameList)
                self.filesPerSerie, self.nFilePerSerie = groupFilesPerSerie(self.filelist_fullname, self.serievec)

            if self.filesPerSerie is not None:
                for serie in self.filesPerSerie:
                    for _file in self.filesPerSerie[serie]:
                        if what == 'dark':
                            self._originalsDark.append(serie)
                        elif what == 'ref':
                            self._originalsRef.append(serie)

            return self.serievec is not None and self.filesPerSerie is not None

        def _getSeriesValue(fileNames):
            assert (len(fileNames) > 0)
            is_there_digits = len(re.findall(r'\d+', fileNames[0])) > 0
            series = set()
            i = 0
            for fileName in fileNames:
                if is_there_digits:
                    name = fileName.rstrip(self.params.file_ext)
                    file_index = name.split('_')[-1]
                    rm_not_numeric = re.compile(r'[^\d.]+')
                    file_index = rm_not_numeric.sub('', file_index)
                    series.add(file_index)
                else:
                    series.add('%04d' % i)
                    i += 1
            return list(series)

        def groupFilesPerSerie(files, series):
            def findFileEndingWithSerie(poolFiles, serie):
                res = []
                for _file in poolFiles:
                    _f = _file.rstrip('.edf')
                    if _f.endswith(serie):
                        res.append(_file)
                return res

            def checkSeriesFilesLength(serieFiles):
                length = -1
                for serie in serieFiles:
                    if length == -1:
                        length = len(serieFiles[serie])
                    elif len(serieFiles[serie]) != length:
                        logger.error('Series with inconsistant number of ref files')

            assert len(series) > 0
            if len(series) is 1:
                return {series[0]: files}, len(files)
            assert len(files) > 0

            serieFiles = {}
            unattributedFiles = files.copy()
            for serie in series:
                serieFiles[serie] = findFileEndingWithSerie(unattributedFiles, serie)
                [unattributedFiles.remove(_f) for _f in serieFiles[serie]]

            if len(unattributedFiles) > 0:
                logger.error('Failed to associate %s to any serie' % unattributedFiles)
                return {}, 0

            checkSeriesFilesLength(serieFiles)

            return serieFiles, len(serieFiles[list(serieFiles.keys())[0]])

        def process():
            """process calculation of the what"""
            if mode is DarkRefs.CALC_NONE:
                return
            shape = fabio.open(self.filelist_fullname[0]).getDims()

            for i in range(len(self.serievec)):
                largeMat = numpy.zeros((self.nframes * self.nFilePerSerie,
                                        shape[1],
                                        shape[0]))

                if what == 'dark' and len(self.serievec) is 1:
                    fileName = self.out_prefix
                    if fileName.endswith(self.params.file_ext) is False:
                        fileName = fileName + self.params.file_ext
                else:
                    fileName = self.out_prefix.rstrip(self.params.file_ext) \
                               + self.serievec[i] + self.params.file_ext
                fileName = os.path.join(directory, fileName)
                if os.path.isfile(fileName):
                    if self.params.skipIfExist is True:
                        logger.info(
                            'skip creation of %s, already existing' % fileName)
                        continue

                if self.nFilePerSerie == 1:
                    fSerieName = os.path.join(directory, self.series[i])
                    header = {'method': mode + ' on 1 image'}
                    header['SRCUR'] = utils.getClosestSRCurrent(scan=directory,
                                                                refFile=fSerieName)
                    if self.nframes == 1:
                        largeMat[0] = fabio.open(fSerieName).data
                    else:
                        handler = fabio.open(fSerieName)
                        dShape = (self.nframes, handler.dim2, handler.dim1)
                        largeMat = numpy.zeros(dShape)
                        for iFrame in range(self.nframes):
                            largeMat[iFrame] = handler.getframe(iFrame).data
                else:
                    header = {'method': mode + ' on %d images' % self.nFilePerSerie}
                    header['SRCUR'] = utils.getClosestSRCurrent(scan=directory,
                                                                refFile=
                                                                self.series[i][
                                                                    0])
                    for j, fName in zip(range(self.nFilePerSerie), self.filesPerSerie[self.serievec[i]]):
                        file_BigMat = fabio.open(fName)
                        if self.nframes > 1:
                            for fr in range(self.nframes):
                                jfr = fr + j * self.nframes
                                largeMat[jfr] = file_BigMat.getframe(
                                    fr).getData()
                        else:
                            largeMat[j] = file_BigMat.data

                if mode == DarkRefs.CALC_MEDIAN:
                    data = numpy.median(largeMat, axis=0)
                elif mode == DarkRefs.CALC_AVERAGE:
                    data = numpy.mean(largeMat, axis=0)
                else:
                    assert mode != DarkRefs.CALC_NONE
                    logger.error(
                        'Unrecognized calculation type request %s' % mode)
                    return
                self.nacq = getDARK_N(directory) or 1
                if what == 'dark' and self.nacq > 1: # and self.nframes == 1:
                    data = data / self.nacq
                    # add one to add to avoid division by zero
                    # data = data + 1
                file_desc = fabio.edfimage.EdfImage(data=data,
                                                    header=header)
                i += 1
                _ttype = numpy.uint16 if what == 'dark' else numpy.int32
                file_desc.write(fileName, force_type=_ttype)

        if directory is None:
            return
        if setup():
            logger.info('start proccess darks and flat fields for %s' % self.directory)
            process()
            logger.info('end proccess darks and flat fields')
        if self.params.rm == 1:
            removeFiles()

    def getInfo(self, what):
        with open(self.infofile) as file:
            infod = file.readlines()
            for line in infod:
                if what in line:
                    return int(line.split('=')[1])
        # not found:
        return 0

    def getDarkFiles(self, directory):
        """

        :return: the list of existing darks files in the directory according to
                 the file pattern.
         """
        patternDark = re.compile(self.params.patternDark)

        res = []
        for file in os.listdir(directory):
            if patternDark.match(file) is not None and file.endswith(
                    self.params.file_ext):
                res.append(os.path.join(directory, file))
        return res

    def getRefFiles(self, directory):
        """

        :return: the list of existing refs files in the directory according to
                 the file pattern.
         """
        patternRef = re.compile(self.params.patternRef)

        res = []
        for file in os.listdir(directory):
            if patternRef.match(file) and file.endswith(self.params.file_ext):
                res.append(os.path.join(directory, file))
        return res
