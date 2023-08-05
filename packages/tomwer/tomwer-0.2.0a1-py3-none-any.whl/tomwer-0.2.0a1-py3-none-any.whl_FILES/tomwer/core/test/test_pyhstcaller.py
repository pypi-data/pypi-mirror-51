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

__authors__ = ["PJ. Gouttenoire", "H. Payno"]
__license__ = "MIT"
__date__ = "23/04/2018"


from tomwer.core.ReconsParams import ReconsParam
from tomwer.core.PyHSTCaller import PyHSTCaller
from tomwer.test.utils import UtilsTest, rebaseParFile
from tomwer.core.utils.pyhstutils import _findPyHSTVersions, _getPyHSTDir
import unittest
import logging
import tempfile
import shutil
import os

logging.disable(logging.INFO)

pyhstVersion = _findPyHSTVersions(_getPyHSTDir())


@unittest.skipIf(len(pyhstVersion) is 0, "PyHST2 missing")
class TestRecHST(unittest.TestCase):
    """
    Test that rec HST file are correctly processing
    """

    def setUp(self):
        self.topDir = tempfile.mkdtemp()
        self.dataset = 'scan_3_'
        dataTestDir = UtilsTest.getDataset(self.dataset)
        self.targetFolder = os.path.join(self.topDir, self.dataset)
        shutil.copytree(dataTestDir, self.targetFolder)

        self.parFile = os.path.join(self.targetFolder, self.dataset + '.par')
        self.parSliceFile = os.path.join(self.targetFolder,
                                         self.dataset + 'slice.par')

        for pFile in (self.parFile, self.parSliceFile):
            rebaseParFile(filePath=pFile,
                          scanOldPath='/lbsram/data/visitor/mi1226/id19/nemoz/henri/',
                          scanNewPath=os.path.join(self.topDir))
            rebaseParFile(filePath=pFile,
                          scanOldPath='/data/visitor/mi1226/id19/nemoz/henri/',
                          scanNewPath=os.path.join(self.topDir))

    def tearDown(self):
        shutil.rmtree(self.topDir)

    def testRecFileCreation(self):
        """Check if the PyHST caller is able to create the .rec file"""
        recCreator = PyHSTCaller()
        assert recCreator.isvalid()
        recCreator.makeRecFile(dirname=self.targetFolder)
        refFile = os.path.join(self.targetFolder, self.dataset + '.rec')
        self.assertTrue(os.path.isfile(refFile))


class TestParFile(unittest.TestCase):
    """Test the behavior of the `makeParFile` function"""
    def setUp(self):
        self.recCreator = PyHSTCaller()
        self.topdir = tempfile.mkdtemp()
        self.outputdir = os.path.join(self.topdir, '001_0.28_19keV_Al63')
        os.mkdir(self.outputdir)

        assert self.recCreator.isvalid()
        self.parfile = os.path.join(self.outputdir,
                                    os.path.basename(self.outputdir) + '.par')

    def tearDown(self):
        shutil.rmtree(self.topdir)

    def testParFileWithoutOptions(self):
        """Make sure the creation of .par file without any options works"""
        reconsParams = ReconsParam()
        reconsParams.setValue('FT', 'NUM_LAST_IMAGE', 1999)
        reconsParams.setValue('FT', 'FILE_PREFIX', '001_0.28_19keV_Al63')
        reconsParams.setValue('FT', 'NUM_IMAGE_1',
                              2048)  # Number of pixels horizontally
        reconsParams.setValue('FT', 'NUM_IMAGE_2',
                              2048)  # Number of pixels vertically
        reconsParams.setValue('FT', 'IMAGE_PIXEL_SIZE_1',
                              0.280000)  # Pixel size horizontally (microns)
        reconsParams.setValue('FT', 'CORRECT_FLATFIELD', 'NO')
        reconsParams.setValue('FT', 'FF_FILE_INTERVAL', 2000)
        reconsParams.setValue('FT', 'OFFSET', 0)
        self.recCreator.makeParFile(self.outputdir)
        self.assertTrue(os.path.exists(self.parfile))

    def testParFileWithOptions(self):
        """Make sure the creation of .par file with creation works"""
        reconsParams = ReconsParam()
        reconsParams.setValue('FT', 'NUM_LAST_IMAGE', 1999)
        reconsParams.setValue('FT', 'FILE_PREFIX', '001_0.28_19keV_Al63')
        reconsParams.setValue('FT', 'NUM_IMAGE_1',
                              2048)  # Number of pixels horizontally
        reconsParams.setValue('FT', 'NUM_IMAGE_2',
                              2048)  # Number of pixels vertically
        reconsParams.setValue('FT', 'IMAGE_PIXEL_SIZE_1',
                              0.280000)  # Pixel size horizontally (microns)
        reconsParams.setValue('FT', 'CORRECT_FLATFIELD', 'NO')
        reconsParams.setValue('FT', 'FF_FILE_INTERVAL', 2000)
        reconsParams.setValue('FT', 'OFFSET', 0)

        options = {}
        options['doubleffcorrection'] = 'yez'
        options['half_acquisition'] = 1
        options['do_projection_median'] = 'YES'
        options['ft_jp2'] = 1
        options['correct'] = 1
        options['extra_output_file'] = 'test'
        self.recCreator.makeParFile(self.outputdir, options)
        self.assertTrue(os.path.exists(self.parfile))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestParFile, TestRecHST):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite
