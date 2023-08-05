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
__date__ = "09/02/2018"


from tomwer.core.darkref.DarkRefCopy import DarkRefCopyP
from tomwer.core.darkref.DarkRefs import DarkRefs
from tomwer.test.utils import UtilsTest, rebaseParFile
from tomwer.core import utils
import fabio
import unittest
import logging
import tempfile
import shutil
import os
import numpy

logging.disable(logging.INFO)


class TestRefCopy(unittest.TestCase):
    """
    Test that RefCopy process is correct
    """

    def setUp(self):
        self.topDir = tempfile.mkdtemp()
        self.datasetWithRef = 'scan_3_'
        dataTestDir = UtilsTest.getDataset(self.datasetWithRef)
        self.folderWithRef = os.path.join(self.topDir, self.datasetWithRef)
        shutil.copytree(dataTestDir, self.folderWithRef)
        assert len(DarkRefs.getRefHSTFiles(self.folderWithRef)) > 0
        assert len(DarkRefs.getDarkHSTFiles(self.folderWithRef)) > 0

        self.datasetWithNoRef = 'test10'
        dataTestDir = UtilsTest.getDataset(self.datasetWithNoRef)
        self.folderWithoutRef = os.path.join(self.topDir, self.datasetWithNoRef)
        shutil.copytree(dataTestDir, self.folderWithoutRef)
        [os.remove(f) for f in DarkRefs.getRefHSTFiles(self.folderWithoutRef)]
        [os.remove(f) for f in DarkRefs.getDarkHSTFiles(self.folderWithoutRef)]
        # TODO : remove permanemtly darkHST0000 from the dataset
        _darkHST = os.path.join(self.folderWithoutRef, 'darkHST0000.edf')
        if os.path.isfile(_darkHST):
            os.remove(_darkHST)
        assert len(DarkRefs.getRefHSTFiles(self.folderWithoutRef)) is 0
        assert len(DarkRefs.getDarkHSTFiles(self.folderWithoutRef)) is 0

        self.refCopyObj = DarkRefCopyP()
        self.refCopyObj.setForceSync(True)

        for _file in os.listdir(self.folderWithoutRef):
            if _file.startswith('ref') or _file.startswith('dark'):
                os.remove(os.path.join(self.folderWithoutRef, _file))

    def tearDown(self):
        shutil.rmtree(self.topDir)

    def testAutoMode(self):
        """Check behavior of the auto mode"""
        self.refCopyObj.setModeAuto(True)
        self.refCopyObj.process(self.folderWithRef)
        # TODO : remove permamently the darkHST0000.edf file
        # make sure the refCopy is correctly initialized
        self.assertTrue(self.refCopyObj.hasRefStored() is True)
        self.assertTrue('dark.edf' in self.refCopyObj.worker._getRefList())
        self.assertTrue('refHST0000.edf' in self.refCopyObj.worker._getRefList())
        self.assertTrue(len(self.refCopyObj.worker._getRefList()) is 2)
        # check process is doing the job
        self.refCopyObj.process(self.folderWithoutRef)
        self.assertTrue(len(DarkRefs.getRefHSTFiles(self.folderWithoutRef)) > 0)
        self.assertTrue(len(DarkRefs.getDarkHSTFiles(self.folderWithoutRef)) > 0)

    def testManualMode(self):
        """Check behavior of the manual mode"""
        self.refCopyObj.setModeAuto(False)
        self.refCopyObj.setRefsFromScan(self.folderWithRef)
        # make sure the refCopy is correctly initialized
        self.assertTrue(self.refCopyObj.hasRefStored() is True)
        self.assertTrue('dark.edf' in self.refCopyObj.worker._getRefList())
        self.assertTrue('refHST0000.edf' in self.refCopyObj.worker._getRefList())
        self.assertTrue(len(self.refCopyObj.worker._getRefList()) is 2)
        # check process is doing the job
        self.refCopyObj.process(self.folderWithoutRef)
        self.assertTrue(len(DarkRefs.getRefHSTFiles(self.folderWithoutRef)) > 0)
        self.assertTrue(len(DarkRefs.getDarkHSTFiles(self.folderWithoutRef)) > 0)

    def testNormalizationSRCurrent(self):
        """Make sure the srCurrent is taking into account"""
        self.refCopyObj.setModeAuto(False)
        self.refCopyObj.setRefsFromScan(self.folderWithRef)

        self.assertTrue(os.path.isfile(
            os.path.join(self.folderWithRef, 'dark.edf')))
        originalRefData = fabio.open(
            os.path.join(self.folderWithRef, 'refHST0000.edf')).data
        assert utils.getSRCurrent(scan=self.folderWithRef, when='start') == 200.36
        assert utils.getSRCurrent(scan=self.folderWithRef, when='end') == 199.63
        normRefData = fabio.open(
            os.path.join(self.refCopyObj.worker._savedir, 'refHST0000.edf')).data
        self.assertFalse(numpy.array_equal(originalRefData, normRefData))

        self.refCopyObj.process(self.folderWithoutRef)
        self.assertTrue(
            os.path.isfile(os.path.join(self.folderWithoutRef, 'dark.edf')))
        self.assertTrue(
            os.path.isfile(os.path.join(self.folderWithoutRef, 'refHST0000.edf')))
        copyRefData = fabio.open(
            os.path.join(self.folderWithoutRef, 'refHST0000.edf')).data
        assert utils.getSRCurrent(scan=self.folderWithoutRef, when='start') == 101.3
        assert utils.getSRCurrent(scan=self.folderWithoutRef, when='end') == 93.6
        self.assertFalse(numpy.array_equal(originalRefData, copyRefData))
        self.assertFalse(numpy.array_equal(normRefData, copyRefData))

    def testInverseOperation(self):
        """Make sure we will found back the original flat field reference
        if the process is forced to take the default value for SRCurrent
        two time"""
        def rewriteRefHSTFile(_file):
            _handler = fabio.open(_file)
            _data, _header = _handler.data, _handler.header

            # add some extra information on the header
            _header['SRCUR'] = 200.0
            file_desc = fabio.edfimage.EdfImage(data=_data,
                                                header=_header)
            file_desc.write(_file)
            file_desc.close()

        self.refCopyObj.setModeAuto(False)
        os.remove(os.path.join(self.folderWithRef,
                               os.path.basename(self.folderWithRef) + '.info'))
        os.remove(os.path.join(self.folderWithRef,
                               os.path.basename(self.folderWithRef) + '.xml'))
        os.remove(os.path.join(self.folderWithoutRef,
                               os.path.basename(self.folderWithoutRef) + '.xml'))
        self.refCopyObj.setRefsFromScan(self.folderWithRef)
        rewriteRefHSTFile(
            _file=os.path.join(self.folderWithRef, 'refHST0000.edf'))

        originalRefData = fabio.open(
            os.path.join(self.folderWithRef, 'refHST0000.edf')).data
        self.refCopyObj.process(self.folderWithoutRef)
        copyRefData = fabio.open(
            os.path.join(self.folderWithoutRef, 'refHST0000.edf')).data
        self.assertTrue(originalRefData.shape == copyRefData.shape)
        self.assertTrue(numpy.allclose(originalRefData, copyRefData))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestRefCopy, ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
