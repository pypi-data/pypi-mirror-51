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
__date__ = "17/05/2017"

import fabio.edfimage
import tempfile
import numpy
import os
import psutil
import logging
from tomwer.core import settings
from lxml import etree

logger = logging.getLogger(__name__)

MOCK_LOW_MEM = False    # if True will simulate the case the computer run into low memory


_RECONS_PATTERN = '_slice_'

_PAG_RECONS_PATTERN = '_slice_pag_'


def mockReconstruction(folder, nRecons=5, nPagRecons=0, volFile=False):
    """
    create reconstruction files into the given folder
    
    :param str folder: the path of the folder where to save the reconstruction
    :param nRecons: the number of reconstruction to mock
    :param nPagRecons: the number of paganin reconstruction to mock
    :param volFile: true if we want to add a volFile with reconstruction
    """
    assert type(nRecons) is int and nRecons >= 0
    basename = os.path.basename(folder)
    dim = 200
    for i in range(nRecons):
        f = tempfile.mkstemp(prefix=basename,
                             suffix=str(_RECONS_PATTERN + str(i) + ".edf"),
                             dir=folder)
        data = numpy.zeros((dim, dim))
        data[::i+2, ::i+2] = 1.0
        edf_writer = fabio.edfimage.EdfImage(data=data,
                                             header={"tata": "toto"})
        edf_writer.write(f[1])

    for i in range(nPagRecons):
        f = tempfile.mkstemp(prefix=basename,
                             suffix=str(_PAG_RECONS_PATTERN + str(i) + ".edf"),
                             dir=folder)
        data = numpy.zeros((dim, dim))
        data[::i+2, ::i+2] = 1.0
        edf_writer = fabio.edfimage.EdfImage(data=data,
                                             header={"tata": "toto"})
        edf_writer.write(f[1])

    if volFile is True:
        volFile = os.path.join(folder, basename + '.vol')
        infoVolFile = os.path.join(folder, basename + '.vol.info')
        dataShape = (nRecons, dim, dim)
        data = numpy.random.random(nRecons*dim * dim).reshape(nRecons, dim, dim)
        data.astype(numpy.float32).tofile(volFile)
        _createVolInfoFile(filePath=infoVolFile, shape=dataShape)


def _createVolInfoFile(filePath, shape, voxelSize=1, valMin=0.0, valMax=1.0,
                       s1=0.0, s2=1.0, S1=0.0, S2=1.0):
    assert len(shape) is 3
    f = open(filePath, 'w')
    f.writelines("\n".join([
        '! PyHST_SLAVE VOLUME INFO FILE',
        'NUM_X =  %s' % shape[2],
        'NUM_Y =  %s' % shape[1],
        'NUM_Z =  %s' % shape[0],
        'voxelSize =  %s' % voxelSize,
        'BYTEORDER = LOWBYTEFIRST',
        'ValMin =  %s' % valMin,
        'ValMax =  %s' % valMax,
        's1 =  %s' % s1,
        's2 =  %s' % s2,
        'S1 =  %s' % S1,
        'S2 =  %s' % S2
    ]))
    f.close()


def mockAcquisition(folder, nScans=20):
    """
    Simple function creating an acquisition into the given directory
    """
    assert type(nScans) is int and nScans > 0
    basename = os.path.basename(folder)
    dim = 200
    # create scan files
    for i in range(nScans):
        f = tempfile.mkstemp(prefix=basename,
                             suffix=str('_' + str(i) + ".edf"),
                             dir=folder)
        data = numpy.random.random(dim * dim).reshape(dim, dim)
        edf_writer = fabio.edfimage.EdfImage(data=data,
                                             header={"tata": "toto"})
        edf_writer.write(f[1])


def isLowOnMemory(path=''):
    """

     :return: True if the RAM usage is more than MAX_MEM_USED (or low memory
        is simulated)
    """
    if path == settings.LBSRAM_ID:
        if settings.MOCK_LBSRAM is True:
            return MOCK_LOW_MEM
        else:
            assert os.path.isdir(path)
            return psutil.disk_usage(path).percent > settings.MAX_MEM_USED
    else:
        return (MOCK_LOW_MEM is True) or psutil.disk_usage(path).percent > settings.MAX_MEM_USED


def mockLowMemory(b=True):
    """Mock the case the computer is running into low memory
    """
    global MOCK_LOW_MEM
    MOCK_LOW_MEM = b
    return psutil.virtual_memory().percent > settings.MAX_MEM_USED


def mockScan(scanID, nRadio, nRecons, nPagRecons, dim):
    """
    Create some random radios and reconstruction in the folder

    :param str scanID: the folder where to save the radios and scans
    :param int nRadio: The number of radios to create
    :param int nRecons: the number of reconstruction to mock
    :param int nRecons: the number of paganin reconstruction to mock
    :param int dim: dimension of the files (nb row/columns)
    """
    assert type(scanID) is str
    assert type(nRadio) is int
    assert type(nRecons) is int
    assert type(dim) is int

    mockAcquisition(folder=scanID,nScans=nRadio)
    mockReconstruction(folder=scanID,
                       nRecons=nRecons,
                       nPagRecons=nPagRecons)


def _getInformation(scan, refFile, information, _type, aliases=None):
    """
    Parse files contained in the given directory to get the requested
    information

    :param scan: directory containing the acquisition. Must be an absolute path
    :param refFile: the refXXXX_YYYY which should contain information about the
                    scan.
    :return: the requested information or None if not found
    """
    def parseRefFile(filePath):
        header = fabio.open(filePath).header
        for k in aliases:
            if k in header:
                return _type(header[k])
        return None

    def parseXMLFile(filePath):
        try:
            for alias in info_aliases:
                tree = etree.parse(filePath)
                elmt = tree.find("acquisition/" + alias)
                if elmt is None:
                    continue
                else:
                    info = _type(elmt.text)
                    if info == -1:
                        return None
                    else:
                        return info
        except etree.XMLSyntaxError as e:
            logger.warning(e)
            return None

    def parseInfoFile(filePath):
        def extractInformation(text, alias):
            text = text.replace(alias, '')
            text = text.replace('\n', '')
            text = text.replace(' ', '')
            text = text.replace('=', '')
            return _type(text)
        info = None
        f = open(filePath, "r")
        line = f.readline()
        while line:
            for alias in info_aliases:
                if alias in line:
                    info = extractInformation(line, alias)
                    break
            line = f.readline()
        f.close()
        return info

    info_aliases = [information]
    if aliases is not None:
        assert type(aliases) in (tuple, list)
        [info_aliases.append(alias) for alias in aliases]

    if not os.path.isdir(scan):
        return None

    if refFile is not None and os.path.isfile(refFile):
        info = parseRefFile(refFile)
        if info is not None:
            return info

    baseName = os.path.basename(scan)
    infoFiles = [os.path.join(scan, baseName + '.info')]
    infoOnDataVisitor = infoFiles[0].replace('lbsram', '')
    # hack to check in lbsram, would need to be removed to add some consistency
    if os.path.isfile(infoOnDataVisitor):
        infoFiles.append(infoOnDataVisitor)
    for infoFile in infoFiles:
        if os.path.isfile(infoFile) is True:
            info = parseInfoFile(infoFile)
            if info is not None:
                return info

    xmlFiles = [os.path.join(scan, baseName + '.xml')]
    xmlOnDataVisitor = xmlFiles[0].replace('lbsram', '')
    # hack to check in lbsram, would need to be removed to add some consistency
    if os.path.isfile(xmlOnDataVisitor):
        xmlFiles.append(xmlOnDataVisitor)
    for xmlFile in xmlFiles:
        if os.path.isfile(xmlFile) is True:
            info = parseXMLFile(xmlFile)
            if info is not None:
                return info

    return None


def getClosestEnergy(scan, refFile=None):
    """
    Parse files contained in the given directory to get information about the
    incoming energy for the serie `iSerie`

    :param scan: directory containing the acquisition
    :param refFile: the refXXXX_YYYY which should contain information about the
                    energy.
    :return: the energy in keV or none if no energy found
    """
    return _getInformation(os.path.abspath(scan), refFile, information='Energy',
                           aliases=['energy', 'ENERGY'], _type=float)


def getClosestSRCurrent(scan, refFile=None):
    """
    Parse files contained in the given directory to get information about the
    incoming energy for the serie `iSerie`

    :param scan: directory containing the acquisition
    :param refFile: the refXXXX_YYYY which should contain information about the
                    energy.
    :return: the energy in keV or none if no energy found
    """
    return _getInformation(os.path.abspath(scan), refFile, information='SRCUR',
                           aliases=['SrCurrent', 'machineCurrentStart'],
                           _type=float)

def getSRCurrent(scan, when):
    assert when in ('start', 'end')

    xmlFiles = [os.path.join(os.path.abspath(scan), os.path.basename(scan) + '.xml')]
    xmlOnDataVisitor = xmlFiles[0].replace('lbsram', '')
    # hack to check in lbsram, would need to be removed to add some consistency
    if os.path.isfile(xmlOnDataVisitor):
        xmlFiles.append(xmlOnDataVisitor)
    for xmlFile in xmlFiles:
        if os.path.isfile(xmlFile):
            try:
                tree = etree.parse(xmlFile)
                key = 'machineCurrentStart' if when == 'start' else 'machineCurrentStop'
                elmt = tree.find("acquisition/" + key)
                if elmt is None:
                    return None
                else:
                    info = float(elmt.text)
                    if info == -1:
                        return None
                    else:
                        return info
            except etree.XMLSyntaxError as e:
                logger.warning(e)
                return None
    return None


def getTomo_N(scan):
    return _getInformation(os.path.abspath(scan), refFile=None,
                           information='TOMO_N', _type=int,
                           aliases=['tomo_N', 'Tomo_N'])

def getScanRange(scan):
    return _getInformation(os.path.abspath(scan), refFile=None,
                           information='ScanRange', _type=int)



def getDARK_N(scan):
    return _getInformation(os.path.abspath(scan), refFile=None,
                           information='DARK_N', _type=int)
                           # aliases=['tomo_N', 'Tomo_N'])
