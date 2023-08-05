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
__date__ = "22/03/2018"

import logging
import os
import shutil
import tempfile
import unittest
from tomwer.core.qtApplicationManager import QApplicationManager
from orangecontrib.tomwer.test.OrangeWorkflowTest import OrangeWorflowTest
from tomwer.test.utils import UtilsTest

app = QApplicationManager()
logging.disable(logging.INFO)


class TestScanListSampleMovedWorkflow(OrangeWorflowTest):
    """Make sure the sample moved is correctly connecting to the orange-canvas
    and that it will display requested scans
    """

    def setUp(self):
        super(TestScanListSampleMovedWorkflow, self).setUp()
        dataset = 'D2_H2_T2_h_'
        self.dataTestDir = UtilsTest.getDataset(dataset)

    def tearDow(self):
        super(TestScanListSampleMovedWorkflow, self).tearDow()

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        nodeScanList = cls.addWidget(cls,
            'orangecontrib.tomwer.widgets.ScanListWidget.ScanListWidget')
        nodeSampleMoved = cls.addWidget(cls,
            'orangecontrib.tomwer.widgets.OWSampleMovedWidget.OWSampleMovedWidget')
        cls.processOrangeEvents(cls)

        cls.link(cls, nodeScanList, "data", nodeSampleMoved, "data")
        cls.processOrangeEvents(cls)

        cls.scanListWidget = cls.getWidgetForNode(cls, nodeScanList)
        cls.sampleMovedWidget = cls.getWidgetForNode(cls, nodeSampleMoved)

    @classmethod
    def tearDownClass(cls):
        del cls.scanListWidget
        del cls.sampleMovedWidget
        OrangeWorflowTest.tearDownClass()

    def test(self):
        self.assertTrue(len(self.sampleMovedWidget._mainWidget._images) is 0)

        self.scanListWidget.add(self.dataTestDir)
        self.scanListWidget._sendList()
        app.processEvents()
       

def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestScanListSampleMovedWorkflow,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
