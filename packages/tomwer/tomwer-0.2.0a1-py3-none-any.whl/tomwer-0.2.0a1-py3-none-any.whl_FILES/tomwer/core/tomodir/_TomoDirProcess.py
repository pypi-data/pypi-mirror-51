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

"""
This module analyze headDir data directory to detect scan to be reconstructed
"""

__authors__ = ["C. Nemoz", "H. Payno"]
__license__ = "MIT"
__date__ = "14/10/2016"


import sys
if sys.version_info[0] < 3:
    from commands import getstatusoutput as myux
else:
    from subprocess import getstatusoutput as myux
from glob import glob
import time
from silx.third_party.EdfFile import EdfFile
from silx.gui import qt
from tomwer.core.ftseries.FastSetupDefineGlobals import *
from tomwer.core.RSyncManager import RSyncManager
from tomwer.web.client import OWClient
from ..tomodir import OBSERVATION_STATUS

logger = logging.getLogger(__name__)


"""
Useful tools
"""

def get_dir_size(dir):
    if not os.path.isdir(dir):
        err = "%s is not a directory, can't get size" % dir
        raise ValueError(err)
    else:
        aux = myux('du -ms ' + dir.replace(' ', '\ '))
        if len(aux) < 2:
            return 0
        return (float((aux[1].split('\t'))[0]))


def get_info_val(l, key):
    r = range(len(l))
    key = key + '='
    for i in r:
        if key in l[i]:
            val = float(l[i].split('=')[1])
    return val


class _TomoDirProcess(OWClient, qt.QObject):
    """
    TomoDirProcess is the process managing the observation of acquisition.
    Since we want to loop infinitly on a root folder we have to ignore the
    folder we previously detected. Otherwise if those folders are not removed
     we will loop infinitly. That is why we now have the ignoredFolders
     parameter.
    
    Example of usage of srxPattern and destPattern:

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

    :param  str dataDir: Root directory containing data
    :param  bool waitXML: if True then we will be waiting for the XML of
        the acquisition to be writted. Otherwise we will look for the .info
        file and wait until all file will be copied
    :param str srcPattern: the pattern to change by destPattern.
    :param str destPattern: the pattern that will replace srcPattern in the
        scan path
    :param list ignoredFolders: the list of folders to ignored on parsing
                                 (them and sub folders)
    """

    sigNbDirExplored = qt.Signal(int)
    """Signal emitted to notice the number of directory at the top level"""
    sigAdvanceExploration = qt.Signal(int)
    """signal emitted each time a top level directory is parsed"""
    sigNewObservation = qt.Signal(tuple)
    """used to signal a new step on the acquisition (first element of the tuple
        should be on eof OBSERVATION_STATUS, second element can be extra
        information to be displayed )"""

    sigNewInformation = qt.Signal(str)
    """Signal used to communicate some random information (will originally be
        displayed in TomoDirWidget)"""

    XML_EXT = '.xml'

    SLICE_WC = 'slice'

    INFO_EXT = '.info'

    ABORT_FILE = '.abo'

    INITIAL_STATUS = 'not processing'

    FILE_INFO_KEYS = ['TOMO_N', 'REF_ON', 'REF_N', 'DARK_N']

    DEFAULT_DETECTOR = 'Frelon'

    DATA_EXT = '0000.edf'


    def __init__(self, dataDir, srcPattern=None,
                 destPattern=None):

        OWClient.__init__(self, logger)
        qt.QObject.__init__(self)
        self.RootDir = dataDir
        self.parsing_dir = dataDir
        self.oldest = 0

        self.expected_dirsize = 0
        self.dirsize = 0
        self.curdir = ''
        self.scan_name = ''
        self.file_rec_ext = '.rec'  # never used
        self.scan_completed = False
        self.reconstructed = False
        self.status = self.INITIAL_STATUS
        """contains the step of acquisition we are looking for and the
        status on this step"""
        self.quitting = False
        self.detector = self.DEFAULT_DETECTOR
        self._removed = None

        srcPatternInvalid = srcPattern not in [None, ''] and not os.path.isdir(srcPattern)
        destPatternInvalid = destPattern not in [None, ''] and not os.path.isdir(destPattern)

        if srcPatternInvalid or destPatternInvalid:
            srcPattern = None
            destPattern = None

        self.srcPattern = srcPattern if destPattern is not None else None
        self.destPattern = destPattern if srcPattern is not None else None

    def _setStatus(self, status, info=None):
        assert(status in OBSERVATION_STATUS)
        self.status = status
        if info is None:
            self.sigNewObservation.emit((status, ))
        else:
            self.sigNewObservation.emit((status, info))

    def _removeAcquisition(self, scanID, reason):
        if os.path.exists(scanID) and os.path.isdir(scanID):
            if self._removed is None:
                logger.info("removing folder %s because %s" % (scanID, reason))
                RSyncManager().removeDir(scanID)
                # avoid multiple removal as removal is asynchronous and might
                # fail
                self._removed = scanID

    def dir_explore(self):
        """
        Explore directory tree until valid .file_info_ext file is found.
        Tree explored by ascending order relative to directory date depending
        self.oldest

        :return: True if the acquisition as started else False
        """
        self.status = 'start acquisition'

    def _isScanDirectory(self, directory):
        aux = directory.split('/')
        scan_name = aux[len(aux) - 1]
        dataname = os.path.join(directory, aux[-1]+self.DATA_EXT)
        dataname = os.path.abspath(dataname)
        infoname = os.path.join(directory, aux[-1] + self.INFO_EXT)

        if self.srcPattern:
            infoname = infoname.replace(self.srcPattern,
                                        self.destPattern,
                                        1)

        """
        assume 1st it is standard info filename
        """
        gd = glob(os.path.join(directory, infoname))
        if len(gd) == 0:
            """
            To detect if it is PCO like, check if info filename contains 0000
            """
            gd = glob(os.path.join(directory, self.INFO_EXT))
            if len(gd) > 0:
                self.detector = 'Dimax'

        """
        Dimax: add 0000 to scan name
        """
        if self.detector == 'Dimax' and scan_name[len(scan_name) - 4:] != '0000':
            scan_name = scan_name + '0000'

        if len(gd) > 0:
            if self.acquisitionAborted() is True:
                self._removeAcquisition(scanID=directory,
                                        reason='acquisition aborted by the user')
                return False
            self._setStatus('starting')
            valid = self.info_validate(infoname=infoname)
            if valid is True:
                self._setStatus('started', directory)
                return True

    def info_validate(self, infoname):
        """
        Check that file found is a valid one.

        :return: True if the file is valid
        """
        assert os.path.isfile(infoname)
        try:
            fd = open(infoname, 'r')
            lines = fd.read()
            fd.close()

            lg = len(self.FILE_INFO_KEYS)
            vali = 0
            for i in range(lg):
                vali = vali + (self.FILE_INFO_KEYS[i] in lines)

            return vali == lg
        except Exception as e:
            e = sys.exc_info()[0]
            logger.error('fail to get info from %s' % infoname)
            raise e

    def _sync(self):
        """Start to copy files from /lbsram/path to path if on lbsram

        :return: True if the synchronization starts
        """
        if self.srcPattern:
            assert(os.path.isdir(self.srcPattern) or self.srcPattern == '')
            assert(os.path.isdir(self.destPattern) or self.destPattern == '')
            if self.RootDir.startswith(self.srcPattern):
                source = os.path.join(self.RootDir, self.parsing_dir)
                target = source.replace(self.srcPattern, self.destPattern, 1)
                info = 'Start synchronization between %s and %s' % (source, target)
                self.sigNewInformation.emit(info)

                RSyncManager().syncFolder(source, os.path.dirname(target))
                return True
        else:
            return False

    def is_data_complete(self):
        """
        Check that data file is found and complete

        :return: - 0 if the acquisition is no finished
                 - 1 if the acquisition is finished
                 - -1 observation has been stopped
        """
        raise NotImplementedError('_TomoDirProcess is a pure virtual class')

    def getCurrentDir(self):
        """Return the current dircetory parsed absolute path"""
        return os.path.join(self.RootDir, self.parsing_dir)

    def acquisitionAborted(self):
        """
        Check if the acquisition have been aborted. In this case the directory
        should contain a [scanID].abo file
        :return: True if the acquisition have been abort and the directory
                 should be abort
        """
        aux = self.parsing_dir.split('/')
        abortFile = os.path.join(self.parsing_dir, aux[-1] + self.ABORT_FILE)
        if self.srcPattern:
            abortFile = abortFile.replace(self.srcPattern,
                                          self.destPattern,
                                          1)
        return os.path.isfile(abortFile)


class _TomoDirProcessXML(_TomoDirProcess):
    """
    This method will parse the [scanID].info file and look if all .edf file
    specified in the .info file are recorded and complete.
    """
    def __init__(self, dataDir, srcPattern, destPattern):
        _TomoDirProcess.__init__(self, dataDir, srcPattern, destPattern)

    def is_data_complete(self):
        self._sync()
        aux = self.parsing_dir.split('/')
        xmlfilelbsram = os.path.join(self.RootDir, self.parsing_dir,
                                     aux[len(aux) - 1] + self.XML_EXT)

        if self.srcPattern is None:
            self.scan_completed = os.path.isfile(xmlfilelbsram)
        else:
            xmlfilenice = xmlfilelbsram.replace(self.srcPattern,
                                                self.destPattern)
            self.scan_completed = os.path.isfile(xmlfilenice) or os.path.isfile(xmlfilelbsram)

        return self.scan_completed


class _TomoDirProcessUserFilePattern(_TomoDirProcess):
    """
    This method will look for a specific pattern given by the user.
    If a file in the given folder exists then we will consider the acquisition
    ended

    :param str pattern: the pattern we are looking for
    """
    def __init__(self, dataDir, srcPattern, destPattern, pattern):
        _TomoDirProcess.__init__(self, dataDir, srcPattern, destPattern)
        self.pattern = pattern

    def is_data_complete(self):
        self._sync()
        fullPattern = os.path.join(self.getCurrentDir(), self.pattern)
        self.scan_completed = len(glob(fullPattern)) > 0
        return self.scan_completed


class _TomoDirProcessParseInfo(_TomoDirProcess):
    """
    This method will look for a '[scanID].xml' pattern
    """

    TYPES = {
        'SignedByte': 1,
        'UnsignedByte': 1,
        'SignedShort': 2,
        'UnsignedShort': 2,
        'SignedInteger': 4,
        'UnsignedInteger': 4,
        'SignedLong': 4,
        'UnsignedLong': 4,
        'Signed64': 8,
        'Unsigned64': 8,
        'FloatValue': 4,
        'Float': 4,
        'DoubleValue': 8
    }

    TIME_LOOP_DATA_INCOMPLETE = 4
    """Time in second between two iterations to check if the data are complete
    or not"""

    def __init__(self, dataDir, srcPattern, destPattern):
        _TomoDirProcess.__init__(self, dataDir, srcPattern, destPattern)
        self.Dim1 = None
        self.Dim2 = None
        self.Tomo = None

    @staticmethod
    def get_data_size(edfType):
        if edfType in _TomoDirProcessParseInfo.TYPES:
            return (_TomoDirProcessParseInfo.TYPES[edfType])
        else:
            return 2

    def info_validate(self):
        """
        Check that file found is a valid one and set acquisition information

        :return: True if the file is valid
        """
        if _TomoDirProcess.info_validate(self):
            assert os.path.isfile(self.infoname)
            try:
                fd = open(self.infoname, 'r')
                lines = fd.read()
                fd.close()

                self.curdir = os.path.join(self.RootDir, self.parsing_dir)
                if not os.path.isdir(self.curdir):
                    return False
                self.dirsize = get_dir_size(self.curdir)

                lines = lines.split('\n')

                self.Dim1 = int(get_info_val(lines, 'Dim_1'))
                self.Dim2 = int(get_info_val(lines, 'Dim_2'))
                self.Tomo = int(get_info_val(lines, 'TOMO_N'))
            except:
                e = sys.exc_info()[0]
                logger.error('fail to get info from %s' % self.infoname)
                raise e
            else:
                return True

    def is_data_complete(self):
        self._sync()

        try:
            limit = True
            while limit:
                try:
                    filno = os.open(self.dataname, os.O_RDONLY)
                    limit = False
                except:
                    if self.quitting is True:
                        return -1
                    time.sleep(self.TIME_LOOP_DATA_INCOMPLETE)

            os.close(filno)

            old_size = 0
            datafile1_ready = False
            while datafile1_ready is False:
                if self.quitting is True:
                    return -1
                time.sleep(self.TIME_LOOP_DATA_INCOMPLETE)
                mystat = os.stat(self.dataname)
                fstat_st_size = mystat.st_size
                if fstat_st_size > old_size:
                    old_size = fstat_st_size
                else:
                    datafile1_ready = True

            edf = EdfFile(self.dataname).Images[0]
            self.dataType = _TomoDirProcessParseInfo.get_data_size(edf.DataType)
            headerLength = edf.DataPosition
            multif = 1
            if self.detector == 'Dimax':
                multif = self.Tomo

            deltas = multif * (
            self.Dim1 * self.Dim2 * self.dataType + headerLength) - fstat_st_size
            if (deltas == 0) and (self.detector == 'Dimax'):
                self.scan_completed = True
                return 1

            """
            1st data file has been completed. Wait all data files are present, i.e. check if > nprojections
            """
            limit = True
            while limit:
                r = glob(self.curdir + '/*')
                if len(r) > self.Tomo:
                    limit = False
                else:
                    if self.quitting is True:
                        return -1

                    logger.info('waiting for more data')
                    self._sync()
                    time.sleep(1)

            self.scan_completed = True
            return 1
        except Exception as e:
            logger.error('fail during is_data_validate')
            raise e

