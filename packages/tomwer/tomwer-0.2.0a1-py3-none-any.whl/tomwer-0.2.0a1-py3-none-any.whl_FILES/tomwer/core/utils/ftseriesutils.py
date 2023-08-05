# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017 European Synchrotron Radiation Facility
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
__date__ = "20/01/2017"

import os
from tomwer.core.utils import getTomo_N
import operator
from tomwer.core.ftseries.FastSetupDefineGlobals import FastSetupAll
from silx.io.octaveh5 import Octaveh5
from tomwer.core.utils import getScanRange
import shutil
from glob import glob
import re
import logging

logger = logging.getLogger(__file__)

def getRadioPaths(scanID):
    """Return the dict of radios for the given scanID.
    Keys of the dictionary is the slice number
    Return all the file on the root of scanID starting by the name of scanID and
    ending by .edf

    :param scanID: is the path to the folder of acquisition
    """
    if(scanID is None) or not(os.path.isdir(scanID)):
        return []

    files = dict({})
    if os.path.isdir(scanID):
        for f in os.listdir(scanID):
            if isARadioPath(f, scanID):
                gfile = os.path.join(scanID, f)
                files[getIndexReconstructed(f, scanID)] = gfile

    return files


def isARadioPath(fileName, scanID):
    """Return True if the given fileName can fit to a Radio name
    """
    fileBasename = os.path.basename(fileName)
    folderBasename = os.path.basename(scanID)

    if fileBasename.endswith(".edf") and fileBasename.startswith(folderBasename) :
        localstring = fileName.rstrip('.edf')
        # remove the scanID
        localstring = re.sub(folderBasename, '', localstring)
        if 'slice_' in localstring:
            # case of a reconstructed file
            return False
        if 'refHST' in localstring:
            return False
        s = localstring.split('_')
        if s[-1].isdigit():
            # check that the next value is a digit
            return True

    return False


global counter_rand
counter_rand = 1

def getIndexReconstructed(reconstructionFile, scanID):
    """Return the slice reconstructed of a file from her name

    :param str reconstructionFile: the name of the file
    """
    folderBasename = os.path.basename(scanID)
    if reconstructionFile.endswith(".edf") and reconstructionFile.startswith(
            folderBasename):
        localstring = reconstructionFile.rstrip('.edf')
        # remove the scanID
        localstring = re.sub(folderBasename, '', localstring)
        s = localstring.split('_')
        if s[-1].isdigit():
            return int(s[-1])
        else:
            logger.warning("Fail to find the slice reconstructed for "
                           "file %s" % reconstructionFile)
    else:
        global counter_rand
        counter_rand = counter_rand + 1
        return counter_rand

        logger.warning("reconstructionFile and scanID doesn't fit with the "
                       "fast tomo serie pattern. "
                       "Can't find slice reconstructed")


def getReconstructionsPaths(scanID, withIndex=False):
    """
    Return the dict of files:
    * fitting with a reconstruction pattern and ending by .edf
    * .vol files

    :param scanID: is the path to the folder of acquisition
    """
    def containsDigits(input):
        return any(char.isdigit() for char in input)

    if (scanID is None) or (not os.path.isdir(scanID)):
        if withIndex is True:
            return {}
        else:
            return []

    if _getPYHST_ReconsFile(scanID) is not None:
        return _getReconstructedFilesFromParFile(_getPYHST_ReconsFile(scanID), withIndex)
    else:
        folderBasename = os.path.basename(scanID)
        files = {} if withIndex is True else []
        if os.path.isdir(scanID):
            for f in os.listdir(scanID):
                if f.endswith(".edf") and f.startswith(folderBasename) and 'slice_' in f:
                    localstring = f.rstrip('.edf')
                    if 'slice_' in localstring:
                        localstring = f.rstrip('.edf')
                        if 'slice_pag_' in localstring:
                            indexStr = localstring.split('slice_pag_')[-1].split('_')[0]
                        else:
                            indexStr = localstring.split('slice_')[-1].split('_')[0]
                        if containsDigits(indexStr):
                            gfile = os.path.join(scanID, f)
                            assert(os.path.isfile(gfile))
                            if withIndex is True:
                                files[getIndexReconstructed(f, scanID)] = gfile
                            else:
                                files.append(gfile)
                if f.endswith(".vol"):
                    if withIndex is True:
                        files[getIndexReconstructed(f, scanID)] = os.path.join(scanID, f)
                    else:
                        files.append(os.path.join(scanID, f))
        return files


def _getShapeForVolFile(filePath):
    ddict = {}
    f = open(filePath, "r")
    lines = f.readlines()
    for line in lines:
        if not '=' in line:
            continue
        l = line.replace(' ', '')
        key, value = l.split('=')
        ddict[key.lower()] = value

    dimX = None
    dimY = None
    dimZ = None

    if 'num_z' in ddict:
        dimZ = int(ddict['num_z'])
    if 'num_y' in ddict:
        dimY = int(ddict['num_y'])
    if 'num_x' in ddict:
        dimX = int(ddict['num_x'])

    return (dimZ, dimY, dimX)


def _getReconstructedFilesFromParFile(parFile, withIndex):
    """Return the path to the reconstructed file by PyHST from the
    PyHST reconstruction file
    """
    def _getStartVoxel(text):
        for line in text:
            if 'START_VOXEL_3' in line:
                return line.split('=')[1].replace(' ', '').split('#')[0]
        raise ValueError('Can\'t find \'START_VOXEL_3\' parameters from %s' %parFile )

    def _getEndVoxel(text):
        for line in text:
            if 'END_VOXEL_3' in line:
                return line.split('=')[1].replace(' ', '').split('#')[0]
        raise ValueError('Can\'t find \'END_VOXEL_3\' parameters from %s' %parFile )

    def _getOutputFile(text):
        for line in text:
            if 'OUTPUT_FILE' in line:
                return line.split('=')[1].replace(' ', '').split('#')[0]
        raise ValueError('Can\'t find \'OUTPUT_FILE\' parameters from %s' %parFile )

    if not (os.path.isfile(parFile) and os.path.exists(parFile)):
        logger.warning(parFile + ' is not a file')
        return {}
    
    _parfile = parFile
    if type(_parfile) in (tuple, list):
        _parfile = _parfile[0]
    if _parfile is None:
        return {}
    if type(_parfile) is not str:
        logger.warning('given parfile should be str. Given is %s: %s'
                       '' % (type(_parfile), _parfile))
        return {}

    with open(_parfile) as inputfile:
        text = inputfile.readlines()
        startVoxel = _getStartVoxel(text)
        endVoxel = _getEndVoxel(text)
        outputFile = _getOutputFile(text).split('\n')[0]

    files = {} if withIndex is True else []
    for sliceReconstructed in range(int(startVoxel), int(endVoxel) +1):
        if withIndex is True:
            files[sliceReconstructed-1] = outputFile + format((sliceReconstructed-1), '04d') + '.edf'
        else:
            files.append(outputFile + format((sliceReconstructed-1), '04d') + '.edf')
            "-1 because during pyHST start indexing from 0 and the par file start from 1"

    return files


def _getPYHST_ReconsFile(scanID):
    """Return the .par file used for the current reconstruction if any.
    Otherwise return None """
    if scanID == "":
        return None

    if scanID is None:
        raise RuntimeError('No current acquisition to validate')
    assert(type(scanID) is str)
    assert(os.path.isdir(scanID))
    folderID = os.path.basename(scanID)
    # look for fasttomo files ending by slice.par
    parFiles = glob(os.path.join(scanID + folderID) + '*_slice.par')
    if len(parFiles) > 0:
        return orderFileByLastLastModification(scanID, parFiles)[-1]
    else:
        return None


def orderFileByLastLastModification(folder, fileList):
    """Return the list of files sorted by time of last modification.
    From the oldest to the newest modify"""
    res = {}
    for f in fileList:
        res[os.path.getmtime(os.path.join(folder, f))] = f

    return sorted(res.items(), key=operator.itemgetter(0))


def generateDefaultH5File(path):
    """Write a h5 file for reconstruction with the default parameters values"""
    ft = FastSetupAll()
    ft.writeAll(path, 3.8)


def getOrCreateH5File(scanID):
    """Try to get the h5 file containing reconstruction parameters.
    If not existing create it from a set of rule.

    :param str scanID: path to the folder containing the reconstruction to run
    :param defaultOctave: If no file found then create one from our own default
        setting. This require a call to OctaveH5 and t define the targetted 
        octave version
    """
    # TODO : create a setting file ?
    f = getThH5FilePath(scanID)
    if os.path.isfile(f):
        return f
    else:
        default = os.path.expanduser('~')+'/.octave/mytomodefaults.h5'
        if default and os.path.isfile(default):
            shutil.copyfile(default, f)
            assert(os.path.isfile(f))
            return f
        else:
            generateDefaultH5File(f)
            assert(os.path.isfile(f))
            return f


def getThH5FilePath(scanID):
    """Return the theoretical path for the h5 file used for reconstruction for
    the given folder (scanID)

    :param str scanID: the path of the folder
    """
    octave_h5_param = "octave_FT_params.h5"
    assert(os.path.isdir(scanID))
    return os.path.join(scanID, octave_h5_param)


def tryToFindH5File(folder, politic):
    """Return a file in the given folder if any, if more than one, follows
    defined politic.

    :param folder: the folder to explore
    :param str politic: return the newest or oldest file if more than one file
    """
    assert(os.path.isdir(folder))
    assert(type(politic) is str)
    assert(politic.lower() in ('newest', 'oldest'))

    result = None
    age = None
    for f in os.listdir(folder):
        if f.endswith(".h5"):
            fPath = os.path.join(folder, f)
            if age is None :
                age = os.path.getmtime(fPath)
                result = fPath
            else:
                currentFileAge = os.path.getmtime(fPath)
                if currentFileAge > age and politic is 'oldest':
                    age = currentFileAge
                    result = f
                if currentFileAge < age and politic is 'newest':
                    age = currentFileAge
                    result = f

    return result


def saveH5File(structs, h5File, displayInfo=True):
    """Function to write the reconstruction parameters into the h5 file
    
    :param dict structs: the reconstruction parameters
    :param str h5File: the path to the file to create
    :param bool displayInfo: add information in the log ?
    """

    if not h5File.lower().endswith('.h5'):
        h5File = h5File + '.h5'

    # check that the file exists
    if displayInfo is True:
        mess = 'try to save .h5 file ()%s ...' % h5File
        logger.info(mess)

    writer = Octaveh5(3.8)
    try:
        writer.open(h5File, 'w')

        for structID in structs:
            writer.write(structID, structs[structID])

    finally:
        writer.close()


def getSampleEvolScan(scan):
    """Return the 'extra scan of scan which are used to see if the scan
    moved during the acquisition."""
    def orderImg(radios):
        radios = list(radios.values())
        radios.sort()
        return radios[waitedImgs - len(radios):]

    def _getAllRadios(radios):
        res = {}
        for radio in radios:
            res[os.path.basename(radios[radio])] = radios[radio]
        return res

    assert os.path.isdir(scan)
    waitedImgs = getTomo_N(scan)
    radios = getRadioPaths(scan)

    extraImg = 0
    if waitedImgs and waitedImgs < len(radios):
        extraImg = len(radios) - waitedImgs

    if extraImg is 4:
        res = orderImg(radios)
        scanRange = getScanRange(scan)
        if scanRange != 360:
            logger.warning('incoherent data information to retrieve scan'
                           ' evolultion (sample moved widget) ')
            return _getAllRadios(radios)
        radios = list(radios.values())
        radios.sort()
        return {
            '0':radios[0],
            '90':radios[waitedImgs//4-1],
            '180':radios[waitedImgs//2-1],
            '270':radios[waitedImgs//4*3-1],
            '360': radios[waitedImgs-1],
            '270(1)': res[0],
            '180(1)': res[1],
            '90(1)': res[2],
            '0(1)': res[3]}
    elif extraImg is 5:
        res = orderImg(radios)
        scanRange = getScanRange(scan)
        if scanRange != 360:
            logger.warning('incoherent data information to retrieve scan'
                           'evolultion (sample moved widget) ')
            return _getAllRadios(radios)

        radios = list(radios.values())
        radios.sort()
        return {
            '0':radios[0],
            '90':radios[waitedImgs//4-1],
            '180':radios[waitedImgs//2-1],
            '270':radios[waitedImgs//4*3-1],
            '360': radios[waitedImgs-1],
            '360(1)': res[0],
            '270(1)': res[1],
            '180(1)': res[2],
            '90(1)': res[3],
            '0(1)': res[4]}
    elif extraImg is 3:
        res = orderImg(radios)
        scanRange = getScanRange(scan)
        if scanRange != 180:
            logger.warning('incoherent data information to retrieve scan'
                           'evolultion (sample moved widget) ')
            return _getAllRadios(radios)
        radios = list(radios.values())
        radios.sort()
        return {
            '0': radios[0],
            '90': radios[(waitedImgs - 2)//2],
            '180': radios[waitedImgs-1],
            '180(1)': res[0],
            '90(1)': res[1],
            '0(1)': res[2]
        }
    elif extraImg is 2:
        res = orderImg(radios)
        scanRange = getScanRange(scan)
        if scanRange != 180:
            logger.warning('incoherent data information to retrieve scan'
                           'evolultion (sample moved widget) ')
            return _getAllRadios(radios)
        radios = list(radios.values())
        radios.sort()
        return {
            '0': radios[0],
            '90': radios[(waitedImgs - 2)//2],
            '180': radios[waitedImgs-1],
            '90(1)': res[0],
            '0(1)': res[1]
        }
    elif extraImg is 0:
        return {}
    else:
        logger.warning("find unusual number of scans to check if moved. "
                       "Can't deduce any angle pattern.")
        return _getAllRadios(radios)
