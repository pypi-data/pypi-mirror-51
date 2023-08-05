# coding: utf-8
###########################################################################
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
#############################################################################

"""This module is a translation of octave ftseries developped by ESRF ID19 team
It contains the fasttomo global definitions, equivalent to
octave/defineGLOBALS.m
"""

__authors__ = ["C.Nemoz", "H.Payno"]
__license__ = "MIT"
__date__ = "09/02/2017"

import logging
import os
import datetime

from glob import glob

from silx.gui import qt
from silx.test.utils import temp_dir
from tomwer.core import settings
from tomwer.core import utils
from tomwer.core.ReconsParams import ReconsParam
from tomwer.core.ftseries.FastSetupDefineGlobals import FastSetupAll
from tomwer.core.settings import LBSRAM_ID
from tomwer.core.utils import logconfig
from .FtserieReconstruction import FtserieReconstruction
from ..BaseProcess import BaseProcess
from ..utils import ftseriesutils
from tomwer.core.RSyncManager import RSyncManager
import subprocess

logger = logging.getLogger(__name__)


def _subprocess_run(*popenargs, _input=None, timeout=None, check=False, **kwargs):
    if _input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(_input)
    except:
        process.kill()
        if timeout is not None:
            process.wait(timeout)
        else:
            process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr)
    return retcode, stdout, stderr


class Ftseries(BaseProcess):
    """
    Ftseries is the class managing the reconstructions.
    Reconstructions are launched calling the octave fastomo3 scripts.

    Ftseries is able to run one reconstruction at the time only.
    Every requested recosntruction will be stored in a queue (`reconsStack`)
    and be launched one at the time on a dedicated thread.
    """

    inputs = [
        {
            'name': "change recons params",
            'type': FtserieReconstruction,
            'handler': 'updateReconsParam'
        },
        {
            'name': "data",
            'type': str,
            'handler': "pathReceived"
        },
    ]
    # Note : scanReady don't intend to find an 'octave_FT_params.h5' file at
    # the folder level.
    # But updateReconsParam should always have a .h5 file defined
    outputs = [{'name': "data", 'type': str}]

    scanReady = qt.Signal(str)

    reconsParams = ReconsParam()

    def __init__(self):
        BaseProcess.__init__(self, logger)
        self.ftserieReconstruction = None
        self._exploreForH5File = False
        """If True then look in the scan folder and if contain a .h5 try to
        load to update the reconstruction parameters fron it"""

    def setProperties(self, properties):
        assert('_rpSetting' in properties)
        ReconsParam().setStructs(properties['_rpSetting'])

    def setH5Exploration(self, b):
        self._exploreForH5File = b

    def setDefaultValues(self):
        self.reconsParams.params = FastSetupAll().defaultValues

    def updatePath(self, path):
        """Change the path of the acquisition folder we want to reconstruct.
        But doesn't launch the reconstruction

        :param path:the path to the new folder to observe

        """
        if self._exploreForH5File:
            h5file = ftseriesutils.tryToFindH5File(path, 'newest')
            "h5 file is the file to load to update the reconstruction parameters"
            if h5file is not None:
                try:
                    self.load(h5file)
                except:
                    logger.warning('Fail to load reconstruction parameters '
                                   'from %s' % h5file)
                else:
                    logger.info('Reconstruction parameters loaded from '
                                '%s' % h5file)

        self.ftserieReconstruction = FtserieReconstruction(scanID=path)

    def pathReceived(self, pathToTheScanCompleted):
        """Callback function when the path of the file to scan is modify
        The default behavior here is to run a first reconstruction without
        waiting any user modifications

        :param pathToTheScanCompleted:the path to the new folder to observe"""
        if pathToTheScanCompleted is None:
            return

        logger.info('%s received' % pathToTheScanCompleted)

        self.updatePath(pathToTheScanCompleted)
        # behavior : when receiving a new scanID, recontruct it right away
        self.processReconstruction()

    def updateCurrentFTSeries(self, ftSerieReconstruction):
        """Change the Ftseries we want to reconstruct"""
        if ftSerieReconstruction is not None:
            info = 'ask for FTSerie scanID %s' % ftSerieReconstruction.scanID
            logger.info(info,
                        extra={
                            logconfig.DOC_TITLE: self._scheme_title,
                            logconfig.SCAN_ID: self.ftserieReconstruction.scanID})

            self.ftserieReconstruction = ftSerieReconstruction

    def processReconstruction(self):
        """Call the core function 'run_reconstruction' of the ftseries script
        which will call octave to process reconstruction
        """

        if (self.ftserieReconstruction is not None and
                self.ftserieReconstruction.scanID is not None and
                os.path.isdir(self.ftserieReconstruction.scanID)):

            self.reconsStack.add(slices=[0],
                                 scanID=self.ftserieReconstruction.scanID,
                                 reconsParams=ReconsParam().params,
                                 schemeTitle=self._scheme_title
                                 )

    def _infoMissingStrucVar(missingStructures, missingVariables):
        m = "File is missing some structures and/or variables."
        m += "Values of those has been setted to default values."
        m += "Please make sure they are correct."
        m += "\nMissing structures: " + missingStructures
        m += "\nMissing variables: " + missingVariables
        print(m)

    def _signalReconsReady(self, scanID):
        scan = scanID
        if type(scanID) is FtserieReconstruction:
            scan = scanID.scanID

        info = 'scan %s reconstructed' % scan
        logger.processEnded(info,
                            extra={
                                logconfig.DOC_TITLE: self._scheme_title,
                                logconfig.SCAN_ID: scan})

        # if some volraw or volfloat are present at the same level, let
        # synchronize them.
        if settings.isOnLbsram() is True:
            volfloat = os.path.join(os.path.dirname(scan), 'volraw')
            volraw = os.path.join(os.path.dirname(scan), 'volfloat')

            for _folder in (volraw, volfloat):

                if os.path.exists(_folder) and os.path.isdir(_folder):
                    target = _folder.replace(settings.LBSRAM_ID, settings.DEST_ID, 1)
                    logger.info('start synchronization between %s and %s' % (_folder, target))
                    if os.path.exists(target) is False:
                        os.mkdir(target)
                        os.chmod(target, 0o774)

    def __mockReconstruction(self):
        """Run the mocked reconstruction
        Simply create some adapted files
        """
        assert(self.ftserieReconstruction is not None)
        assert(self.ftserieReconstruction.scanID is not None)
        assert(os.path.isdir(self.ftserieReconstruction.scanID))
        logger.info('mocking reconstruction',
                    extra={
                        logconfig.DOC_TITLE: self._scheme_title,
                        logconfig.SCAN_ID: self.ftserieReconstruction.scanID})
        utils.mockReconstruction(self.ftserieReconstruction.scanID)

    def askUserH5File(self):
        filePath = None
        while(filePath is None):
            out = input('please give the path to the h5 file : \n')
            if not os.path.isfile(filePath):
                warning = 'given path ' + out
                warning += ' is not a directory, please give a valid directory'
                logger.warning(warning)
                out = None
        return out

    def askUserAndLoad(self):
        """Process launch by activing the Load button"""
        f = self.askUserH5File()
        if f is not None:
            self.load(f)

    def load(self, h5file):
        assert(os.path.isfile(h5file))
        fsdg = FastSetupAll()
        fsdg.readAll(h5file, 3.8)
        ReconsParam().setStructs(fsdg.structures)

    def save(self, h5File, displayInfo=True):
        """Function to overwrite the reconstruction parameters into the h5 file
        """
        ftseriesutils.saveH5File(structs=ReconsParam().params,
                                 h5File=h5File,
                                 displayInfo=displayInfo)

    def setMockMode(self, b):
        """If the mock mode is activated then during reconstruction won't call
        Octave script for reconstruction but will generate some output files
        according to convention

        :param boolean b: True if we want to active the mock mode
        """
        self._mockMode = b

    def updateReconsParam(self, ftserie):
        if ftserie is None:
            return

        reconstruction = ftserie
        if(type(ftserie) is str):
            reconstruction = FtserieReconstruction(ftserie)

        self.updateCurrentFTSeries(reconstruction)

        # if on lbsram and in low memory then skip it
        if settings.isOnLbsram() and utils.isLowOnMemory(settings.LBSRAM_ID) is True:
            # if computer is running into low memory in lbsram skip reconstruction
            mess = 'low memory, skip reconstruction for ' + reconstruction.scanID
            logger.processSkipped(mess)
            self._signalReconsReady()
        else:
            self.showValidationButtons()
            res = self.exec_()
            self.hideValidationButtons()
            if res == qt.QDialog.Accepted:
                self.processReconstruction()

    def setForceSync(self, b):
        """
        Force synchronisation of the reconstruction

        :param b: True if we want to block ftseries during reconstruction
        """
        self.reconsStack.setForceSync(b)


class H5NoFileException(Exception):
    """Exception launch when no .h5 is found by ftseries"""
    pass


def getInfoFile(dir):
    files = glob(dir + '*.info')
    if dir.startswith(LBSRAM_ID):
        seconddir = dir.rstrip(LBSRAM_ID)
        if os.path.isdir(seconddir):
            files += glob(seconddir + '*.info')
    return files


def run_reconstruction(slices, directory, h5file):
    """Launch a reconstruction

    :param slices: seems unused TODO: check
    :param str directory: the acquisition directory
    :param str h5file: the h5 file containing the reconstruction parameters
    """
    with temp_dir() as tmp:
        # initialise global structures with default values
        assert(os.path.isdir(directory))

        # manage all sub directories
        dirs = []

        aux = glob(directory)
        laux = len(aux)
        for i in range(laux):
            dirs.append(aux[i])

        # now : new behavior : each directory for which we are running a
        # reconstruction should have an .h5 file

        if h5file is None or not os.path.isfile(h5file):
            raise H5NoFileException('No h5 file found for reconstruction')

        # version march python2/3 avec octave 3.6
        # fail avec octave 3.8

        octavexe = tmp+'/octseries'
        try:
            file = open(octavexe, 'wb')
            file.write(bytes('#!/usr/bin/octave\n', 'UTF-8'))
            file.write(bytes('\n', 'UTF-8'))
            file.write(bytes('load_pars ' + h5file + '\n', 'UTF-8'))
            file.write(bytes('global GET_MY_FT\n', 'UTF-8'))
            file.write(bytes('global GENERATOR\n', 'UTF-8'))
            file.write(bytes('GET_MY_FT = 0;\n', 'UTF-8'))
            file.write(bytes('global GENERATOR\n', 'UTF-8'))
            file.write(bytes('GENERATOR = \'tomwer\';\n', 'UTF-8'))
            file.write(bytes('cd '+dirs[0]+'\n', 'UTF-8'))
            file.write(bytes('fasttomo3\n', 'UTF-8'))
            file.write(bytes('\n', 'UTF-8'))
            file.close()
            logger.info("creation of %s succeded" % octavexe)
        except:
            logger.error("fail writing of %s" % octavexe)
            raise

        timeout = 15 * 60 # in sec
        try:
            # TODO : set write only to the current user security issue.
            os.chmod(octavexe, 0o775)
            octave_log = directory + '/octave.log'
            with open(octave_log, 'ab') as _file:
                mydate = datetime.datetime.now()
                _file.write(bytes(
                    "\n\n\n===== OCTAVE process started on " + str(mydate),
                    'UTF-8'))
                
            with open(octave_log, 'ab') as _file:
                retcode, stdout, stderr = _subprocess_run(octavexe,
                                                          timeout=timeout,
                                                          stdout=_file,
                                                          stderr=subprocess.PIPE)
                if retcode > 0:
                    _file.write(stderr)
                    logger.error('error append during execution of %s' % octavexe)
                    logger.error(stderr.decode('utf-8'))
                else:
                    logger.info('succeeded execution of %s' % octavexe)
        except subprocess.TimeoutExpired:
            logger.warning('reconstruction for %s take too long (%s)' % (octavexe, timeout))
        except:
            logger.error('fail execution of %s' % octavexe)
            raise

        return h5file


class FtseriesP(Ftseries, qt.QObject):
    """For now to avoid multiple inheritance from QObject with the process widgets
    we have to define two classes. One only for the QObject inheritance
    """
    def __init__(self):
        Ftseries.__init__(self)
        qt.QObject.__init__(self)
