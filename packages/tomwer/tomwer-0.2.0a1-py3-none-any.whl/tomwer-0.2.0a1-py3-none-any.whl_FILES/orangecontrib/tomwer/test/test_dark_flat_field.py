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

import logging
import time
import os
import shutil
import tempfile
import unittest
from tomwer.core import utils
from tomwer.core.qtApplicationManager import QApplicationManager
from tomwer.core.settings import mock_lsbram
from tomwer.core.darkref.DarkRefs import DarkRefs
from orangecontrib.tomwer.test.OrangeWorkflowTest import OrangeWorflowTest
from tomwer.test.utils import UtilsTest

logging.disable(logging.INFO)

app = QApplicationManager()


class TestConstructionDarkAndFlatField(OrangeWorflowTest):
    """
    test the workflow composed of the following widgets :
        - TomoDirWidget
        - RefCopy : Make sure the refCopy is correctly make
        - DarkRefs : Make sure dark and flat field are skipped if already
                     existing
    """

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        nodeTomodir = cls.addWidget(cls,
                                    'orangecontrib.tomwer.widgets.TomoDirWidget.TomoDirWidget')
        nodeDarkRefs = cls.addWidget(cls,
                                     'orangecontrib.tomwer.widgets.DarkRefAndCopyWidget.DarkRefAndCopyOW')

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls,
                 nodeTomodir, "data",
                 nodeDarkRefs, "data")

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.tomodirWidget = cls.getWidgetForNode(cls, nodeTomodir)
        cls.darkRefsWidget = cls.getWidgetForNode(cls, nodeDarkRefs)

        # set mock mode for FTSerieWidget
        # set tomodir ready for observation
        cls.tomodirWidget.displayAdvancement = False
        # force Dark ref to be sync
        cls.darkRefsWidget.setForceSync(True)

    @classmethod
    def tearDownClass(cls):
        del cls.tomodirWidget
        del cls.darkRefsWidget
        OrangeWorflowTest.tearDownClass()

    def setUp(self):
        def prepareRefFolder():
            datasetID = 'test10'
            self.inputFolder = tempfile.mkdtemp()
            self.scanFolder = os.path.join(self.inputFolder, datasetID)
            shutil.copytree(src=UtilsTest().getDataset(datasetID),
                            dst=self.scanFolder)

            [os.remove(f) for f in DarkRefs.getRefHSTFiles(self.scanFolder)]
            [os.remove(f) for f in DarkRefs.getDarkHSTFiles(self.scanFolder)]

        def prepareScanToProcess():
            self._refParentFolder = tempfile.mkdtemp()
            datasetRef = 'test01'
            self.refFolder = os.path.join(self._refParentFolder, datasetRef)
            shutil.copytree(src=UtilsTest().getDataset(datasetRef),
                            dst=self.refFolder)
            # copy .info file to have coherent REf_N values
            shutil.copyfile(
                    src=os.path.join(self._refParentFolder, 'test01',
                                     'test01.info'),
                    dst=os.path.join(self.scanFolder, 'test10.info'))

        OrangeWorflowTest.setUp(self)
        prepareRefFolder()
        prepareScanToProcess()

        self.tomodirWidget.setFolderObserved(self.inputFolder)
        self.darkRefsWidget.setSkipIfExisting(True)
        self.darkRefsWidget.setRefsFromScan(self.refFolder)
        self.darkRefsWidget.setModeAuto(False)
        utils.mockLowMemory(False)
        mock_lsbram(True)

    def tearDown(self):
        shutil.rmtree(self._refParentFolder)
        shutil.rmtree(self.inputFolder)
        OrangeWorflowTest.tearDown(self)

    def testWorkflow(self):
        self.tomodirWidget._widget.mockObservation(self.scanFolder)

        # let dark ref process time to end
        for _t in (1, 1):
            app.processEvents()
            time.sleep(_t)

        self.assertTrue(len(DarkRefs.getDarkHSTFiles(self.scanFolder)) > 0)
        self.assertTrue(len(DarkRefs.getRefHSTFiles(self.scanFolder)) > 0)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestConstructionDarkAndFlatField, ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
