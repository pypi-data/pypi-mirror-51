# coding: utf-8
# /*##########################################################################
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
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "05/07/2017"

from .BaseProcess import BaseProcess
import logging
import os
import shutil
from tomwer.core.RSyncManager import RSyncManager
from tomwer.core.utils import logconfig
from tomwer.core.settings import LBSRAM_ID, DEST_ID
from silx.gui import qt

logger = logging.getLogger(__name__)


class FolderTransfert(BaseProcess):
    """Manage the copy of dataset.

    .. warning : the destination directory is find out from the file system
                 if /lbsramxxx exists for example...
                 In the case we couldn't found the output directory then we
                 will ask for the user to set it.
    """

    inputs = [{'name': "data",
               'type': str,
               'handler': '_transfertLocally'}]
    outputs = [{'name': "data",
                'type': str}]

    scanready = qt.Signal(str)

    def __init__(self):
        BaseProcess.__init__(self, logger)
        self.turn_off_print = False
        self._forceDestDir = None  # Forced output directory
        self.turn_off_print = False
        self._forceDestDir = None  # Forced output directory
        self._copying = False
        self._block = False

    def setProperties(self, properties):
        # No properties stored for now
        pass

    def _getDefaultOutputDir(self):
        """Return the default output dir based on the computer setup
        """
        if 'TARGET_OUTPUT_FOLDER' in os.environ:
            return os.environ['TARGET_OUTPUT_FOLDER']

        if os.path.isdir('/data/visitor'):
            return '/data/visitor'

        return ''

    def _transfertLocally(self, scanPath, move=False, force=True, noRsync=False):
        """Launch the transfert process

        :param scanPath: the path to the file we want to move/transfert
        :param move: if True, directly move the files. Otherwise copy the files
        :param force: if True then force the copy even if the file/folder already
            exists
        :param bool noRSync: True if we wan't do sue shutil instead of rsync.
        """
        if (scanPath is None) or (not os.path.isdir(scanPath)):
            return

        assert move in (True, False)
        if scanPath is None:
            self.warning('scan path given is None. Avoid tranfert.')
            return

        if not os.path.isdir(scanPath):
            logger.warning('scan path given is not a directory (%s).' % scanPath)
            return

        logger.info('synchronisation with scanPath')
        outputdir = self.getDestinationDir(scanPath)
        if outputdir is None:
            return
        # as we are in the workflow we want this function to be bloking.
        # so we will not used a thread for folder synchronization
        # for now rsync is not delaing with force option
        if noRsync is True or RSyncManager().canUseRSync() is False:
            logger.info("Can't use rsync, copying files")
            try:
                if move is True:
                    self._moveFiles(scanPath=scanPath,
                                    outputdir=outputdir,
                                    force=force)
                else:
                    self._copyFiles(scanPath=scanPath,
                                    outputdir=outputdir,
                                    force=force)
            except shutil.Error as e:
                raise e
            else:
                self.__noticeTransfertSuccess(scanPath, outputdir)
        else:
            source = scanPath
            if not source.endswith(os.path.sep):
                source = source + os.path.sep
            target = outputdir

            if not target.endswith(os.path.sep):
                target = target + os.path.sep

            self._signalCopying(scanID=source, outputdir=target)

            RSyncManager().syncFolder(source=source,
                                                  target=target,
                                                  block=self._block,
                                                  delete=True,
                                                  handler=self.__noticeTransfertSuccess,
                                                  setAllRights=True)

    def __noticeTransfertSuccess(self, scanPath, outputdir):
        self._signalCopySucceed()
        logger.processEnded('transfert succeed',
                            extra={logconfig.DOC_TITLE: self._scheme_title,
                                   logconfig.FROM: scanPath,
                                   logconfig.TO: outputdir})
        self.signalTransfertOk(outputdir)

    def signalTransfertOk(self, scanID):
        self.scanready.emit(scanID)

    def _copyFiles(self, scanPath, outputdir, force):
        """Copying files and removing them"""
        assert(os.path.isdir(scanPath))
        if force is False:
            assert(os.path.isdir(outputdir))

        # create the destination dir
        if not os.path.isdir(outputdir):
            os.mkdir(outputdir)
        # we can't copy directly the top folder because he is already existing
        for f in os.listdir(scanPath):
            file = os.path.join(scanPath, f)
            fileDest = os.path.join(outputdir, f)
            if force is True:
                if os.path.isdir(fileDest):
                    shutil.rmtree(fileDest)
                if os.path.isfile(fileDest):
                    os.remove(fileDest)
            if os.path.isdir(file):
                shutil.copytree(src=file, dst=fileDest)
            else:
                shutil.copy2(src=file, dst=fileDest)

        info = 'Removing directory at %s' % scanPath
        logger.info(info)
        shutil.rmtree(scanPath)
        info = 'sucessfuly removed file at %s !!!' % scanPath
        logger.info(info)

    def _moveFiles(self, scanPath, outputdir, force):
        """Function simply moving files"""
        assert(os.path.isdir(scanPath))
        if force is False:
            assert(os.path.isdir(outputdir))

        logger.debug('synchronisation with scanPath',
                     extra={logconfig.DOC_TITLE: self._scheme_title})

        if force is True and os.path.isdir(outputdir):
            shutil.rmtree(outputdir)

        shutil.move(scanPath, outputdir)

    def _requestFolder(self):
        out = None
        while(out is None):
            out = input('please give the output directory : \n')
            if not os.path.isdir(out):
                warning = 'given path ' + out
                warning += ' is not a directory, please give a valid directory'
                logger.warning(warning)
                out = None
        return out

    def _getOutputDirSpec(self):
        return None

    def _getOutputDirLBS(self, scanPath):
        if scanPath.startswith(LBSRAM_ID):
            return scanPath.replace(LBSRAM_ID, DEST_ID)
        else:
            return None

    def getDestinationDir(self, scanPath):
        """Return the destination directory. The destination directory is the
        root directory"""
        if self._forceDestDir is not None:
            return os.path.join(self._forceDestDir, os.path.basename(scanPath))

        # try to get outputdir from spec
        scanIDPath = os.path.abspath(scanPath)

        outputdir = self._getOutputDirSpec() or self._getOutputDirLBS(scanIDPath)
        if outputdir is None:
            outputdir = self._requestFolder()

        return outputdir

    def _forceDestinationDir(self, dist):
        """Force the outpudir to dist.

        :param str dist: path to the folder. If None remove force behavior
        """
        self._forceDestDir = dist
        if self._forceDestDir is not None:
            assert(os.path.isdir(self._forceDestDir))

    # some function to print the output in the terminal #

    def _signalCopying(self, scanID, outputdir):
        self._copying = True
        if self.turn_off_print is False:
            print('######################################')
            print('###')
            print('###')
            print('### copying files ', scanID, " to ", outputdir)
            print('### ...')

        info = 'start moving folder from %s to %s' % (scanID, outputdir)
        logger.info(info,
                    extra={logconfig.DOC_TITLE: self._scheme_title})

    def _signalCopyFailed(self):
        self._copying = False
        if self.turn_off_print is False:
            print('###')
            print('### copy failed')
            print('###')
            print('######################################')

    def _signalCopySucceed(self):
        self._copying = False
        if self.turn_off_print is False:
            print('###')
            print('### copy succeeded')
            print('###')
            print('######################################')

    def isCopying(self):
        """

        :return: True if the folder transfert is actually doing a copy
        """
        return self._copying

    def setIsBlocking(self, b):
        """

        :param bool b: if True then folderTransfert will wait until transfert
            is done to be released. Otherwise will launch a 'free' thread wich
            will notice transfert end later.
        """
        self._block = b


class FolderTransfertP(FolderTransfert, qt.QObject):
    """For now to avoid multiple inheritance from QObject with the process widgets
    we have to define two classes. One only for the QObject inheritance
    """
    def __init__(self):
        FolderTransfert.__init__(self)
        qt.QObject.__init__(self)
