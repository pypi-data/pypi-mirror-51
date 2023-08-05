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
__date__ = "02/08/2017"


import unittest
from tomwer.core import utils
from tomwer.core.utils import ftseriesutils
from tomwer.core.utils import mockScan
import tempfile
import fabio
import numpy
import os
import shutil
from tomwer.test.utils import UtilsTest


class TestScanValidatorFindFiles(unittest.TestCase):
    """Function testing the getReconstructionsPaths function is correctly
    functioning"""

    DIM_MOCK_SCAN = 10

    N_RADIO = 20
    N_RECONS = 10
    N_PAG_RECONS = 5

    def setUp(self):
        # create scanID folder
        self.scanID = tempfile.mkdtemp()
        mockScan(scanID=self.scanID,
                 nRadio=self.N_RADIO,
                 nRecons=self.N_RECONS,
                 nPagRecons=self.N_PAG_RECONS,
                 dim=self.DIM_MOCK_SCAN)
        basename = os.path.basename(self.scanID)

        # add some random files
        tempfile.mkstemp(prefix=basename,
                         suffix=str('gfdgfg' + str(1) + ".edf"),
                         dir=self.scanID)
        tempfile.mkstemp(prefix=basename,
                         suffix=str('slicetest'+str(1)+".edf"),
                         dir=self.scanID)
        tempfile.mkstemp(prefix=basename,
                         suffix=str('slice_ab.edf'),
                         dir=self.scanID)

    def tearDown(self):
        if os.path.isdir(self.scanID):
            shutil.rmtree(self.scanID)

    def testGetRadioPaths(self):
        nFound = len(ftseriesutils.getRadioPaths(self.scanID))
        self.assertTrue(nFound == self.N_RADIO)

    def testGetReconstructionsPaths(self):
        nFound = len(ftseriesutils.getReconstructionsPaths(self.scanID))
        self.assertTrue(nFound == self.N_RECONS + self.N_PAG_RECONS)

    def testGetSliceReconstruction(self):
        self.assertTrue(
            ftseriesutils.getIndexReconstructed('dfadf_slice_32.edf', 'dfadf') == 32)
        self.assertTrue(
            ftseriesutils.getIndexReconstructed('dfadf_slice_slice_002.edf', 'dfadf') == 2)
        self.assertTrue(
            ftseriesutils.getIndexReconstructed('scan_3slice_0050.edf', 'scan_3') == 50)
        self.assertTrue(
            ftseriesutils.getIndexReconstructed('scan3slice_012.edf', 'scan3') == 12)


class TestPaganinPath(unittest.TestCase):
    def setUp(self):
        self.tmpDir = tempfile.mkdtemp()

        self.dir = os.path.join(self.tmpDir, 'scan25')
        os.mkdir(self.dir)

    def tearDown(self):
        shutil.rmtree(self.tmpDir)

    def testPagFile(self):
        open(os.path.join(self.dir, 'scan25slice_pag_db0500_0115.edf'), 'a').close()
        self.assertTrue(len(ftseriesutils.getReconstructionsPaths(self.dir)) is 1)
        self.assertTrue(
            ftseriesutils.getIndexReconstructed('scan25slice_pag_db0500_0115.edf',
                                                scanID=self.dir)  is 115)

class TestGetReconstructionPath(unittest.TestCase):
    def setUp(self):
        self.tmpDir = tempfile.mkdtemp()
        self.dir = os.path.join(self.tmpDir, 'scan_3')
        os.mkdir(self.dir)
        file_desc = fabio.edfimage.EdfImage(data=numpy.random.random((100, 100)))

        file_desc.write(os.path.join(self.dir, 'scan_3slice_0050.edf'))
        file_desc.write(os.path.join(self.dir, 'scan_3slice_0000.edf'))
        file_desc.write(os.path.join(self.dir, 'scan_3slice_0010.edf'))
        assert len(os.listdir(self.dir)) is 3

    def tearDown(self):
        shutil.rmtree(self.tmpDir)

    def test(self):
        self.assertTrue(len(ftseriesutils.getReconstructionsPaths(os.path.join(self.tmpDir, 'scan_3'))) is 3)


class TestRadioPath(unittest.TestCase):

    def test(self):
        files = [
          'essai1_0008.edf',
          'essai1_0019.edf',
          'essai1_0030.edf',
          'essai1_0041.edf',
          'essai1_0052.edf',
          'essai1_0063.edf',
          'essai1_0074.edf',
          'essai1_0085.edf',
          'essai1_0096.edf',
          'essai1_.par',
          'refHST0100.edf',
          'darkend0000.edf',
          'essai1_0009.edf',
          'essai1_0020.edf',
          'essai1_0031.edf',
          'essai1_0042.edf',
          'essai1_0053.edf',
          'essai1_0064.edf',
          'essai1_0075.edf',
          'essai1_0086.edf',
          'essai1_0097.edf',
          'essai1_.rec',
          'essai1_0000.edf',
          'essai1_0010.edf',
          'essai1_0021.edf',
          'essai1_0032.edf',
          'essai1_0043.edf',
          'essai1_0054.edf',
          'essai1_0065.edf',
          'essai1_0076.edf',
          'essai1_0087.edf',
          'essai1_0098.edf',
          'essai1_slice_1023.edf',
          'essai1_0001.edf',
          'essai1_0011.edf',
          'essai1_0022.edf',
          'essai1_0033.edf',
          'essai1_0044.edf',
          'essai1_0055.edf',
          'essai1_0066.edf',
          'essai1_0077.edf',
          'essai1_0088.edf',
          'essai1_0099.edf',
          'essai1_slice.info',
          'essai1_0001.par',
          'essai1_0012.edf',
          'essai1_0023.edf',
          'essai1_0034.edf',
          'essai1_0045.edf',
          'essai1_0056.edf',
          'essai1_0067.edf',
          'essai1_0078.edf',
          'essai1_0089.edf',
          'essai1_0100.edf',
          'essai1_slice.par',
          'essai1_0002.edf',
          'essai1_0013.edf',
          'essai1_0024.edf',
          'essai1_0035.edf',
          'essai1_0046.edf',
          'essai1_0057.edf',
          'essai1_0068.edf',
          'essai1_0079.edf',
          'essai1_0090.edf',
          'essai1_0101.edf',
          'essai1_slice.xml',
          'essai1_0003.edf',
          'essai1_0014.edf',
          'essai1_0025.edf',
          'essai1_0036.edf',
          'essai1_0047.edf',
          'essai1_0058.edf',
          'essai1_0069.edf',
          'essai1_0080.edf',
          'essai1_0091.edf',
          'essai1_0102.edf',
          'essai1_.xml',
          'essai1_0004.edf',
          'essai1_0015.edf',
          'essai1_0026.edf',
          'essai1_0037.edf',
          'essai1_0048.edf',
          'essai1_0059.edf',
          'essai1_0070.edf',
          'essai1_0081.edf',
          'essai1_0092.edf',
          'essai1_0103.edf',
          'histogram_essai1_slice',
          'essai1_0005.edf',
          'essai1_0016.edf',
          'essai1_0027.edf',
          'essai1_0038.edf',
          'essai1_0049.edf',
          'essai1_0060.edf',
          'essai1_0071.edf',
          'essai1_0082.edf',
          'essai1_0093.edf',
          'essai1_0104.edf',
          'machinefile',
          'essai1_0006.edf',
          'essai1_0017.edf',
          'essai1_0028.edf',
          'essai1_0039.edf',
          'essai1_0050.edf',
          'essai1_0061.edf',
          'essai1_0072.edf',
          'essai1_0083.edf',
          'essai1_0094.edf',
          'essai1_.cfg',
          'pyhst_out.txt',
          'essai1_0007.edf',
          'essai1_0018.edf',
          'essai1_0029.edf',
          'essai1_0040.edf',
          'essai1_0051.edf',
          'essai1_0062.edf',
          'essai1_0073.edf',
          'essai1_0084.edf',
          'essai1_0095.edf'
          ]

        nbRadio = 0
        for f in files:
            nbRadio += ftseriesutils.isARadioPath(f, 'essai1_')
        self.assertTrue(nbRadio == 105)


class TestGetClosestEnergy(unittest.TestCase):
    def setUp(self):
        self.topSrcFolder = tempfile.mkdtemp()
        self.dataSetID = 'scan_3_'
        self.dataDir = UtilsTest.getDataset(self.dataSetID)
        self.sourceS3 = os.path.join(self.topSrcFolder, self.dataSetID)
        shutil.copytree(src=os.path.join(self.dataDir),
                        dst=self.sourceS3)

        self.sourceT01 = os.path.join(self.topSrcFolder, 'test01')
        shutil.copytree(src=UtilsTest.getDataset('test01'),
                        dst=self.sourceT01)
        self.S3XMLFile = os.path.join(self.sourceS3, 'scan_3_.xml')
        self.S3Ref0000 = os.path.join(self.sourceS3, 'ref0000_0000.edf')
        self.S3Ref0010 = os.path.join(self.sourceS3, 'ref0000_0010.edf')

    def tearDown(self):
        shutil.rmtree(self.topSrcFolder)

    def testEnergyFromEDF(self):
        os.remove(self.S3XMLFile)
        self.assertTrue(
            utils.getClosestEnergy(scan=self.sourceS3,
                                   refFile=self.S3Ref0000) == 61)
        self.assertTrue(
            utils.getClosestEnergy(scan=self.sourceS3,
                                   refFile=self.S3Ref0010) == 61)

    def testEnergyFromXML(self):
        os.remove(self.S3Ref0000)
        os.remove(self.S3Ref0010)
        self.assertTrue(utils.getClosestEnergy(scan=self.sourceS3,
                                               refFile=self.S3Ref0000) == 10)
        self.assertTrue(utils.getClosestEnergy(scan=self.sourceS3,
                                               refFile=self.S3Ref0010) == 10)

    def testEnergyFromInfo(self):
        self.assertTrue(
            utils.getClosestEnergy(scan=self.sourceT01, refFile=None) == 19)

    def testDefaultEnergy(self):
        os.remove(self.S3XMLFile)
        os.remove(self.S3Ref0000)
        os.remove(self.S3Ref0010)
        self.assertTrue(utils.getClosestEnergy(scan=self.sourceS3,
                                               refFile=self.S3Ref0000) == None)
        self.assertTrue(utils.getClosestEnergy(scan=self.sourceS3,
                                               refFile=self.S3Ref0010) == None)


class TestGetClosestSREnergy(unittest.TestCase):
    def setUp(self):
        self.topSrcFolder = tempfile.mkdtemp()
        self.dataSetID = 'test10'
        self.dataDir = UtilsTest.getDataset(self.dataSetID)
        self.sourceT10 = os.path.join(self.topSrcFolder, self.dataSetID)
        shutil.copytree(src=os.path.join(self.dataDir),
                        dst=self.sourceT10)
        self.T10XMLFile = os.path.join(self.sourceT10, 'test10.xml')
        self.T10InfoFile = os.path.join(self.sourceT10, 'test10.info')
        self.T10Ref0000 = os.path.join(self.sourceT10, 'ref0000_0000.edf')

    def tearDown(self):
        shutil.rmtree(self.topSrcFolder)

    def testIntenistyFromInfo(self):
        self.assertTrue(
            utils.getClosestSRCurrent(scan=self.sourceT10, refFile=None) == 201)

    def testDefaultIntensity(self):
        os.remove(self.T10XMLFile)
        os.remove(self.T10InfoFile)
        self.assertTrue(utils.getClosestSRCurrent(scan=self.sourceT10) == None)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestRadioPath, TestScanValidatorFindFiles, TestGetClosestEnergy,
               TestGetReconstructionPath, TestPaganinPath):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
