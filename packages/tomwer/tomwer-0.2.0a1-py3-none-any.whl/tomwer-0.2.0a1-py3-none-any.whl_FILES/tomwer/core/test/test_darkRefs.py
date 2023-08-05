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
__date__ = "11/12/2017"


import os
import numpy
import fabio
import shutil
import tempfile
import unittest
from tomwer.core.darkref.DarkRefs import DarkRefs
from silx.gui.test.utils import TestCaseQt
from tomwer.test.utils import UtilsTest


class TestDarkRefsBehavior(TestCaseQt):
    """Test that the Darks and reference are correctly computed from the
    DarksRefs class
    """
    def setUp(self):
        TestCaseQt.setUp(self)
        self.datasetsID = ('test10', 'D2_H2_T2_h_')
        self.tmpDir = tempfile.mkdtemp()
        self.foldersTest = []
        self.thRef = {}
        """number of theoretical ref file the algorithm should create"""
        self.thDark = {}
        """number of theoretical dark file the algorithm should create"""
        for dataset in self.datasetsID:
            folderTest = os.path.join(self.tmpDir, dataset)
            self.foldersTest.append(folderTest)
            dataDir = UtilsTest.getDataset(dataset)
            shutil.copytree(dataDir, folderTest)
            files = os.listdir(folderTest)
            for _f in files:
                if _f.startswith(('refHST', 'darkHST', 'dark.edf')):
                    os.remove(os.path.join(folderTest, _f))

        self.darkRef = DarkRefs()
        self.darkRef.setForceSync(True)
        self.darkRef.DARKHST_PREFIX = 'darkHST'
        self.darkRef.setRemoveOption(False)

    def tearDown(self):
        shutil.rmtree(self.tmpDir)
        self.qapp.processEvents()
        TestCaseQt.tearDown(self)

    def testDarkCreation(self):
        """Test that the dark is correctly computed"""
        self.darkRef.setRefMode(DarkRefs.CALC_NONE)
        self.darkRef.setDarkMode(DarkRefs.CALC_MEDIAN)

        for folderTest in self.foldersTest:
            datasetName = os.path.basename(folderTest)
            with self.subTest(dataset=datasetName):
                self.darkRef.process(folderTest)
                # + TODO: add name
                if os.path.basename(folderTest) == 'test10':
                    self.assertTrue('darkend0000.edf' in os.listdir(folderTest))
                    self.assertTrue('dark.edf' in os.listdir(folderTest))
                    self.assertTrue(len(self.darkRef.getDarkHSTFiles(folderTest)) is 1)
                    self.assertTrue(len(self.darkRef.getRefHSTFiles(folderTest)) is 0)
                elif os.path.basename(folderTest) == 'D2_H2_T2_h_':
                    self.assertTrue('darkend0000.edf' in os.listdir(folderTest))
                    # check ref are not deleted
                    for ref in ('ref0000_3600.edf', 'ref0028_3600.edf',
                                'ref0044_0000.edf'):
                        self.assertTrue(ref in os.listdir(folderTest))
                    self.assertTrue('dark0000.edf' in os.listdir(folderTest))
                    self.assertFalse('refHST0000.edf' in os.listdir(folderTest))
                    self.assertFalse('refHST3600.edf' in os.listdir(folderTest))

    def testRefCreation(self):
        """Test that the dark is correctly computed"""
        self.darkRef.setRefMode(DarkRefs.CALC_MEDIAN)
        self.darkRef.setDarkMode(DarkRefs.CALC_NONE)

        for folderTest in self.foldersTest:
            datasetName = os.path.basename(folderTest)
            with self.subTest(dataset=datasetName):
                self.darkRef.process(folderTest)
                if os.path.basename(folderTest) == 'test10':
                    self.assertTrue('darkend0000.edf' in os.listdir(folderTest))
                    self.assertFalse('dark0000.edf' in os.listdir(folderTest))
                    self.assertTrue('refHST0000.edf' in os.listdir(folderTest))
                    self.assertTrue('refHST0020.edf' in os.listdir(folderTest))
                    self.assertTrue('ref0000_0000.edf' in os.listdir(folderTest))
                    self.assertTrue('ref0000_0020.edf' in os.listdir(folderTest))
                    self.assertTrue('ref0001_0000.edf' in os.listdir(folderTest))
                    self.assertTrue('ref0001_0020.edf' in os.listdir(folderTest))
                elif os.path.basename(folderTest) == 'D2_H2_T2_h_':
                    # check ref are not deleted
                    for ref in ('ref0000_3600.edf', 'ref0028_3600.edf',
                                'ref0044_0000.edf'):
                        self.assertTrue(ref in os.listdir(folderTest))
                    self.assertTrue('darkend0000.edf' in os.listdir(folderTest))
                    self.assertTrue('refHST0000.edf' in os.listdir(folderTest))
                    self.assertTrue('refHST3600.edf' in os.listdir(folderTest))

    def testRemoveOption(self):
        """Test that the remove option is working"""
        self.darkRef.setRefMode(DarkRefs.CALC_NONE)
        self.darkRef.setDarkMode(DarkRefs.CALC_NONE)
        self.darkRef.setRemoveOption(True)
        for folderTest in self.foldersTest:
            datasetName = os.path.basename(folderTest)
            with self.subTest(dataset=datasetName):
                self.darkRef.process(folderTest)
                self.qapp.processEvents()
                if os.path.basename(folderTest) == 'test10':
                    self.assertFalse('darkend0000.edf' in os.listdir(folderTest))
                    self.assertFalse('dark0000.edf' in os.listdir(folderTest))
                    self.assertFalse('refHST0000.edf' in os.listdir(folderTest))
                    self.assertFalse('refHST0020.edf' in os.listdir(folderTest))
                    self.assertFalse('ref0000_0000.edf' in os.listdir(folderTest))
                    self.assertFalse('ref0000_0020.edf' in os.listdir(folderTest))
                    self.assertFalse('ref0001_0000.edf' in os.listdir(folderTest))
                    self.assertFalse('ref0001_0020.edf' in os.listdir(folderTest))
                elif os.path.basename(folderTest) == 'D2_H2_T2_h_':
                    # check ref are not deleted
                    for ref in ('ref0000_3600.edf', 'ref0028_3600.edf',
                                'ref0044_0000.edf'):
                        self.assertFalse(ref in os.listdir(folderTest))
                    self.assertFalse('darkend0000.edf' in os.listdir(folderTest))
                    self.assertFalse('refHST0000.edf' in os.listdir(folderTest))
                    self.assertFalse('refHST3600.edf' in os.listdir(folderTest))
                    self.assertFalse('dark0000.edf' in os.listdir(folderTest))

    def testSkipOption(self):
        """Test that the overwrite option is working"""
        self.darkRef.setRefMode(DarkRefs.CALC_NONE)
        self.darkRef.setDarkMode(DarkRefs.CALC_NONE)
        self.darkRef.setSkipIfExisting(True)

        for folderTest in self.foldersTest:
            datasetName = os.path.basename(folderTest)
            with self.subTest(dataset=datasetName):
                iniRefNFile = len(self.darkRef.getRefHSTFiles(folderTest))
                iniDarkNFile = len(self.darkRef.getDarkHSTFiles(folderTest))
                self.darkRef.process(folderTest)
                self.assertTrue(len(self.darkRef.getRefHSTFiles(folderTest)) == iniRefNFile)
                self.assertTrue(len(self.darkRef.getDarkHSTFiles(folderTest)) == iniDarkNFile)


class TestRefCalculationOneSerie(unittest.TestCase):
    """
    Make sure the calculation is correct for the dark and flat field
    according to the method used.
    """

    def setUp(self):
        self.tmpDir = tempfile.mkdtemp()
        reFiles = {}
        data1 = numpy.zeros((20, 10))
        data2 = numpy.zeros((20, 10)) + 100
        reFiles['ref0000_0000.edf'] = data1
        reFiles['ref0001_0000.edf'] = data2
        reFiles['ref0002_0000.edf'] = data2
        reFiles['ref0003_0000.edf'] = data2
        for refFile in reFiles:
            file_desc = fabio.edfimage.EdfImage(data=reFiles[refFile])
            file_desc.write(os.path.join(self.tmpDir, refFile))
        assert len(os.listdir(self.tmpDir)) is 4
        self.darkRef = DarkRefs()
        self.darkRef.setForceSync(True)
        self.darkRef.setPatternRef('ref*.*[0-9]{3,4}_[0-9]{3,4}')

    def tearDown(self):
        shutil.rmtree(self.tmpDir)

    def testRefMedianCalculation(self):
        self.darkRef.setRefMode(DarkRefs.CALC_MEDIAN)
        self.darkRef.setDarkMode(DarkRefs.CALC_NONE)
        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, 'refHST0000.edf')
        self.assertTrue(os.path.isfile(refHST))

        self.assertTrue(numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 100))

    def testRefMeanCalculation(self):
        self.darkRef.setRefMode(DarkRefs.CALC_AVERAGE)
        self.darkRef.setDarkMode(DarkRefs.CALC_NONE)
        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, 'refHST0000.edf')
        self.assertTrue(os.path.isfile(refHST))
        self.assertTrue(numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 75))


class TestRefCalculationThreeSerie(unittest.TestCase):
    """
    Make sure the calculation is correct for the dark and flat field
    according to the method used.
    """

    def setUp(self):
        self.tmpDir = tempfile.mkdtemp()
        reFiles = {}
        self.series = (0, 10, 200)
        for serie in self.series:
            data1 = numpy.zeros((20, 10)) + serie
            data2 = numpy.zeros((20, 10)) + 100 + serie
            reFiles['ref0000_' + str(serie).zfill(4) + '.edf'] = data1
            reFiles['ref0001_' + str(serie).zfill(4) + '.edf'] = data2
            reFiles['ref0002_' + str(serie).zfill(4) + '.edf'] = data2
            reFiles['ref0003_' + str(serie).zfill(4) + '.edf'] = data2
            for refFile in reFiles:
                file_desc = fabio.edfimage.EdfImage(data=reFiles[refFile])
                file_desc.write(os.path.join(self.tmpDir, refFile))

        self.darkRef = DarkRefs()
        self.darkRef.setForceSync(True)
        self.darkRef.setPatternRef('ref*.*[0-9]{3,4}_[0-9]{3,4}')

    def tearDown(self):
        shutil.rmtree(self.tmpDir)

    def testRefMedianCalculation(self):
        self.darkRef.setRefMode(DarkRefs.CALC_MEDIAN)
        self.darkRef.setDarkMode(DarkRefs.CALC_NONE)
        self.darkRef.process(self.tmpDir)
        for serie in self.series:
            refHST = os.path.join(self.tmpDir, 'refHST' + str(serie).zfill(4) + '.edf')
            self.assertTrue(os.path.isfile(refHST))
            self.assertTrue(numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 100 + serie))

    def testRefMeanCalculation(self):
        self.darkRef.setRefMode(DarkRefs.CALC_AVERAGE)
        self.darkRef.setDarkMode(DarkRefs.CALC_NONE)
        self.darkRef.process(self.tmpDir)
        for serie in self.series:
            refHST = os.path.join(self.tmpDir, 'refHST' + str(serie).zfill(4) + '.edf')
            self.assertTrue(os.path.isfile(refHST))
            self.assertTrue(numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 75 + serie))


class TestDarkCalculationOneFrame(unittest.TestCase):
    """Make sure computation of the Dark is correct"""
    def setUp(self):
        self.tmpDir = tempfile.mkdtemp()
        file_desc = fabio.edfimage.EdfImage(data=numpy.zeros((20, 10)) + 10)

        file_desc.write(os.path.join(self.tmpDir, 'darkend0000.edf'))
        assert len(os.listdir(self.tmpDir)) is 1
        self.darkRef = DarkRefs()
        self.darkRef.setForceSync(True)

    def tearDown(self):
        shutil.rmtree(self.tmpDir)

    def testDarkMeanCalculation(self):
        self.darkRef.setRefMode(DarkRefs.CALC_NONE)
        self.darkRef.setDarkMode(DarkRefs.CALC_AVERAGE)

        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, 'dark.edf')
        self.assertTrue(os.path.isfile(refHST))
        self.assertTrue(numpy.array_equal(fabio.open(refHST).data,
                                          numpy.zeros((20, 10)) + 10))

    def testDarkMedianCalculation(self):
        self.darkRef.setRefMode(DarkRefs.CALC_NONE)
        self.darkRef.setDarkMode(DarkRefs.CALC_MEDIAN)

        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, 'dark.edf')
        self.assertTrue(os.path.isfile(refHST))

        self.assertTrue(numpy.array_equal(fabio.open(refHST).data,
                                          numpy.zeros((20, 10)) + 10))


class TestDarkCalculation(unittest.TestCase):
    """Make sure computation of the Dark is correct"""

    def setUp(self):
        self.tmpDir = tempfile.mkdtemp()
        file_desc = fabio.edfimage.EdfImage(data=numpy.zeros((20, 10)))
        file_desc.appendFrame(data=(numpy.zeros((20, 10)) + 100))
        file_desc.appendFrame(data=(numpy.zeros((20, 10)) + 100))
        file_desc.appendFrame(data=(numpy.zeros((20, 10)) + 100))

        file_desc.write(os.path.join(self.tmpDir, 'darkend0000.edf'))
        assert len(os.listdir(self.tmpDir)) is 1
        self.darkRef = DarkRefs()
        self.darkRef.setForceSync(True)

    def tearDown(self):
        shutil.rmtree(self.tmpDir)

    def testDarkMeanCalculation(self):
        self.darkRef.setRefMode(DarkRefs.CALC_NONE)
        self.darkRef.setDarkMode(DarkRefs.CALC_AVERAGE)

        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, 'dark.edf')
        self.assertTrue(os.path.isfile(refHST))
        self.assertTrue(numpy.array_equal(fabio.open(refHST).data,
                                          numpy.zeros((20, 10)) + 75))

    def testDarkMedianCalculation(self):
        self.darkRef.setRefMode(DarkRefs.CALC_NONE)
        self.darkRef.setDarkMode(DarkRefs.CALC_MEDIAN)

        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, 'dark.edf')
        self.assertTrue(os.path.isfile(refHST))

        self.assertTrue(numpy.array_equal(fabio.open(refHST).data,
                                          numpy.zeros((20, 10)) + 100))


class TestDarkAccumulation(unittest.TestCase):
    """
    Make sure computation for dark in accumulation are correct
    """
    def setUp(self):
        self.dataset = 'bone8_1_'
        dataDir = UtilsTest.getDataset(self.dataset)
        self.outputdir = tempfile.mkdtemp()
        shutil.copytree(src=dataDir, dst=os.path.join(self.outputdir, self.dataset))
        self.darkFile = os.path.join(self.outputdir, self.dataset, 'dark.edf')
        assert os.path.isfile(self.darkFile)
        with fabio.open(self.darkFile) as dsc:
            self.dark_reference = dsc.data
        # remove dark file
        os.remove(self.darkFile)

        self.darkRef = DarkRefs()
        self.darkRef.setForceSync(True)
        self.darkRef.setRefMode(DarkRefs.CALC_NONE)
        self.darkRef.setDarkMode(DarkRefs.CALC_MEDIAN)
        self.darkRef.setPatternDark('darkend*')
        self.darkRef.DARKHST_PREFIX = 'dark.edf'

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testComputation(self):
        """Test data bone8_1_ from id16b containing dark.edf of reference
        and darkend"""
        self.darkRef.process(os.path.join(self.outputdir, self.dataset))
        self.assertTrue(os.path.isfile(self.darkFile))
        with fabio.open(self.darkFile) as dsc:
            self.computed_dark = dsc.data
        self.assertTrue(
                numpy.array_equal(self.computed_dark, self.dark_reference))


class TestPCOTomo(TestCaseQt):
    """Test processing of DKRF are correct"""
    def setUp(self):
        TestCaseQt.setUp(self)
        self.tmpDir = tempfile.mkdtemp()

        self.darkRef = DarkRefs()
        self.darkRef.setForceSync(True)
        self.darkRef.setRefMode(DarkRefs.CALC_NONE)
        self.darkRef.setDarkMode(DarkRefs.CALC_NONE)
        self.darkRef.setPatternDark('.*_dark_.*')
        self.darkRef.setPatternRef('.*_ref_.*')
        self.darkRef.DARKHST_PREFIX = 'darkHST'
        self.darkRef.setRemoveOption(True)

    def copyDataset(self, dataset):
        self.folder = os.path.join(self.tmpDir, dataset)
        shutil.copytree(os.path.join(UtilsTest.getDataset(dataset)),
                        self.folder)

    def tearDown(self):
        shutil.rmtree(self.tmpDir)
        TestCaseQt.tearDown(self)

    def testDark3Scan(self):
        """
        Make sure the processing dark field for
        pcotomo_3scan_refdarkbeg_end_download are correct
        """
        self.dataset = "pcotomo_3scan_refdarkbeg_end_download"
        self.copyDataset(self.dataset)
        _file = os.path.join(self.tmpDir,
                             'pcotomo_3scan_refdarkbeg_end_download',
                             'dark.edf')
        if os.path.isfile(_file):
            os.remove(_file)
        self.darkRef.setDarkMode(DarkRefs.CALC_MEDIAN)
        self.darkRef.process(self.folder)
        darkHSTFiles = self.darkRef.getDarkHSTFiles(self.folder)
        self.assertTrue(len(darkHSTFiles) is 2)
        dark0000 = os.path.join(self.folder, 'dark0000.edf')
        dark1000 = os.path.join(self.folder, 'dark1000.edf')
        self.assertTrue(dark0000 in darkHSTFiles)
        self.assertTrue(dark1000 in darkHSTFiles)

    def testRef3Scan(self):
        """
        Make sure the processing flat field for
        pcotomo_3scan_refdarkbeg_end_download are correct
        """
        self.dataset = "pcotomo_3scan_refdarkbeg_end_download"
        self.copyDataset(self.dataset)
        self.darkRef.setRefMode(DarkRefs.CALC_MEDIAN)
        self.darkRef.process(self.folder)
        refHSTFiles = self.darkRef.getRefHSTFiles(self.folder)
        self.assertTrue(len(refHSTFiles) is 2)
        f0000 = os.path.join(self.folder, 'refHST0000.edf')
        self.assertTrue(f0000 in refHSTFiles)
        f1000 = os.path.join(self.folder, 'refHST1000.edf')
        self.assertTrue(f1000 in refHSTFiles)

    def testDark2x2Scan(self):
        self.dataset = "pcotomo_2x2scan_refdarkbeg_end_conti"
        self.copyDataset(self.dataset)
        self.darkRef.setDarkMode(DarkRefs.CALC_MEDIAN)
        self.assertRaises(ValueError, self.darkRef.process(self.folder))

    def testRef2x2Scan(self):
        self.dataset = "pcotomo_2x2scan_refdarkbeg_end_conti"
        self.copyDataset(self.dataset)
        self.darkRef.setRefMode(DarkRefs.CALC_MEDIAN)
        self.assertRaises(ValueError, self.darkRef.process(self.folder))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestDarkRefsBehavior, TestRefCalculationOneSerie,
               TestRefCalculationThreeSerie,  TestDarkCalculationOneFrame,
               TestDarkCalculation, TestPCOTomo, TestDarkAccumulation):

        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
