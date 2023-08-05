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

from tomwer.core.qtApplicationManager import QApplicationManager
from orangecontrib.tomwer.widgets.ImageStackViewerWidget import ImageStackViewerWidget
from tomwer.core.ftseries.FtserieReconstruction import FtserieReconstruction
from tomwer.core import utils
from silx.gui import qt
import tempfile
import unittest
import shutil
import logging

logging.disable(logging.INFO)

# Makes sure a QApplication exists
_qapp = QApplicationManager()


class TestFilePatterns(unittest.TestCase):
    """Make sure the viewer recognize each possible file pattern"""

    N_ACQUI = 20
    """number of acquisition runned"""

    N_RECONS = 4
    """Number of non Paganin reconstruction"""

    N_PAG_RECONS = 2
    """Number of Paganin reconstructions"""

    @classmethod
    def setUpClass(cls):
        cls.stackViewer = ImageStackViewerWidget()
        cls.stackViewer.setAttribute(qt.Qt.WA_DeleteOnClose)

    @classmethod
    def tearDownClass(cls):
        cls.stackViewer.close()
        del cls.stackViewer

    def setUp(self):
        self._folder = tempfile.mkdtemp()
        utils.mockAcquisition(self._folder, nScans=self.N_ACQUI)

    def tearDown(self):
        shutil.rmtree(self._folder)

    def testAcquisition(self):
        """
        Make sure the viewer is able to found and load the acquisition files
        """
        self.stackViewer.addScan(FtserieReconstruction(self._folder))

        radioDict = self.stackViewer.viewer._stackImageViewerRadio._indexToFile
        self.assertTrue(len(radioDict) == self.N_ACQUI)

    def testReconsNotPag(self):
        """
        Make sure the viewer is able to found and load the reconstruction files
        """
        utils.mockReconstruction(self._folder, nRecons=self.N_RECONS)
        self.stackViewer.addScan(FtserieReconstruction(self._folder))

        scanDict = self.stackViewer.viewer._stackImageViewerScan._indexToFile
        self.assertTrue(len(scanDict) == self.N_RECONS)

    def testReconsPaganin(self):
        """
        Make sure the viewer is able to found and load the paganin recons files
        """
        utils.mockReconstruction(self._folder,
                                 nRecons=0,
                                 nPagRecons=self.N_PAG_RECONS)
        self.stackViewer.addScan(FtserieReconstruction(self._folder))

        scanDict = self.stackViewer.viewer._stackImageViewerScan._indexToFile
        self.assertTrue(len(scanDict) == self.N_PAG_RECONS)

    def testAllRecons(self):
        """
        Make sure the viewer is able to found and load the paganin and the
        not paganin reconstruction and display both
        """
        utils.mockReconstruction(self._folder,
                                 nRecons=self.N_RECONS,
                                 nPagRecons=self.N_PAG_RECONS)
        self.stackViewer.addScan(FtserieReconstruction(self._folder))

        scanDict = self.stackViewer.viewer._stackImageViewerScan._indexToFile
        self.assertTrue(len(scanDict) == self.N_RECONS + self.N_PAG_RECONS)

    def testReconsVolFile(self):
        """Make sure the viewer is able to detect .vol file"""
        utils.mockReconstruction(self._folder,
                                 nRecons=self.N_RECONS,
                                 nPagRecons=0,
                                 volFile=True)
        self.stackViewer.addScan(FtserieReconstruction(self._folder))
        scanDict = self.stackViewer.viewer._stackImageViewerScan._indexToFile
        self.assertTrue(len(scanDict) == self.N_RECONS * 2)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestFilePatterns,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
