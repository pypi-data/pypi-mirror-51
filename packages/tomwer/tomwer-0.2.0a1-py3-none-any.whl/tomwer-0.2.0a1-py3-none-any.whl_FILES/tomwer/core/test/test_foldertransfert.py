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
__date__ = "24/01/2017"


from tomwer.core.FolderTransfert import FolderTransfertP
from silx.gui.test.utils import TestCaseQt
from glob import glob
import unittest
import os
import tempfile
import shutil
import logging

logging.disable(logging.INFO)


class TestFolderTransfert(TestCaseQt):
    """
    Test that the folder transfert process is valid
    """

    def setUp(self):
        TestCaseQt.setUp(self)
        self.nbFile = 10
        self.nbFolder = 1
        self.sourcedir = tempfile.mkdtemp()
        assert(os.path.isdir(self.sourcedir))
        self.targettedir = tempfile.mkdtemp()
        assert(os.path.isdir(self.targettedir))
        self.setFiles()

        self.folderTrans = FolderTransfertP()
        self.folderTrans.turn_off_print = True
        self.folderTrans._forceDestinationDir(self.targettedir)
        self.folderTrans._copying = False

    def setFiles(self):
        if not os.path.isdir(self.sourcedir):
            os.mkdir(self.sourcedir)
        self.files = []
        for iFile in list(range(self.nbFile)):
            self.files.append(
                tempfile.mkstemp(prefix="test_file", suffix=(str(iFile) + ".txt"),
                                 dir=self.sourcedir)[1])
            assert(os.path.isfile(self.files[-1]))

        # create a sub folder
        for iFile in list(range(self.nbFolder)):
            self.files.append(tempfile.mkdtemp(dir=self.sourcedir))

    def tearDown(self):
        del self.folderTrans
        for f in self.files:
            if os.path.isfile(f):
                os.unlink(f)
            if os.path.isdir(f):
                shutil.rmtree(f)

        if os.path.isdir(self.sourcedir):
            shutil.rmtree(self.sourcedir)
        if os.path.isdir(self.targettedir):
            shutil.rmtree(self.targettedir)
        TestCaseQt.tearDown(self)

    def testMoveFiles(self):
        """
        simple test that files are moved
        """
        self.folderTrans._transfertLocally(self.sourcedir,
                                           move=True,
                                           noRsync=True)

        outputdir = os.path.join(self.targettedir, os.path.basename(self.sourcedir))

        self.assertTrue(os.path.isdir(outputdir))
        self.assertTrue(self.checkDataCopied())

    def testCopyFiles(self):
        """
        Simple test that file are copy and deleted
        """
        self.folderTrans._transfertLocally(self.sourcedir,
                                           move=False,
                                           noRsync=True)

        outputdir = os.path.join(self.targettedir, os.path.basename(self.sourcedir))

        self.assertTrue(os.path.isdir(outputdir))
        self.assertTrue(self.checkDataCopied())

    def testMoveFilesForce(self):
        """
        Test the force option of folderTransfert
        """
        out = os.path.join(self.targettedir, os.path.basename(self.sourcedir))
        assert(not os.path.isdir(out))
        os.mkdir(out)
        assert(os.path.isdir(out))
        self.folderTrans._transfertLocally(self.sourcedir,
                                           move=True,
                                           force=False,
                                           noRsync=True)

        self.setFiles()
        with self.assertRaises(shutil.Error):
            self.assertRaises(
                self.folderTrans._transfertLocally(self.sourcedir,
                                                   move=True,
                                                   force=False,
                                                   noRsync=True))

        self.folderTrans._transfertLocally(self.sourcedir,
                                           move=True,
                                           force=True,
                                           noRsync=True)
        self.assertTrue(self.checkDataCopied())

    def testCopyFilesForce(self):
        """
        Test the force option for the copy files process
        """
        out = os.path.join(self.targettedir, os.path.basename(self.sourcedir))
        assert(not os.path.isdir(out))
        os.mkdir(out)
        assert(os.path.isdir(out))
        self.folderTrans._transfertLocally(self.sourcedir,
                                           move=False,
                                           force=False,
                                           noRsync=True)
        self.assertTrue(self.checkDataCopied())

        shutil.copytree(out, self.sourcedir)
        with self.assertRaises(FileExistsError):
            self.assertRaises(
                self.folderTrans._transfertLocally(self.sourcedir,
                                                   move=False,
                                                   force=False,
                                                   noRsync=True))

        self.folderTrans._transfertLocally(self.sourcedir,
                                           move=False,
                                           force=True,
                                           noRsync=True)
        self.assertTrue(self.checkDataCopied())

    def checkDataCopied(self):
        outputdir = os.path.join(self.targettedir, os.path.basename(self.sourcedir))
        outputFiles = os.listdir(outputdir)
        inputFile = glob(self.sourcedir)

        return (len(inputFile) == 0) and (len(outputFiles) == self.nbFile+self.nbFolder) and \
            (not os.path.isdir(self.sourcedir))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestFolderTransfert, ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
