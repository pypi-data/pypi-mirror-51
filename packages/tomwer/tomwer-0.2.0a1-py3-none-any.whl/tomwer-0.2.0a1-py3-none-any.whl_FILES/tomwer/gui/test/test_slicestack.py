# coding: utf-8
#/*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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
#############################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "22/01/2017"

from tomwer.gui.SlicesStack import SlicesStack
from tomwer.test.utils import UtilsTest
from silx.gui import qt
import unittest
import logging
import time
from tomwer.core.qtApplicationManager import QApplicationManager


_qapp = QApplicationManager()

logging.disable(logging.INFO)


class TestSliceStack(unittest.TestCase):
    """ unit test for the :class:SlicesStack widget"""
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._widget = SlicesStack()
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)

    def tearDown(self):
        self._widget.close()
        unittest.TestCase.tearDown(self)

    def test(self):
        """Make sur the addLeaf and clear functions are working"""
        self._widget._viewer.setLazyLoading(False)
        folder = UtilsTest.getDataset("D2_H2_T2_h_")
        self.assertTrue(self._widget._viewer.getActiveImage() is None)

        self.assertTrue(len(self._widget._scans) is 0)
        self._widget.addLeafScan(folder)
        self.assertTrue(len(self._widget._scans) is 1)
        # some delay to wait for the ImageLoaderThread
        time.sleep(0.3)
        _qapp.processEvents()
        self.assertTrue(self._widget._viewer.getActiveImage() is not None)
        self._widget.clear()
        self.assertTrue(len(self._widget._scans) is 0)
        self.assertTrue(self._widget._viewer.getActiveImage() is None)

        self._widget.addLeafScan(folder)
        self.assertTrue(len(self._widget._scans) is 1)
        # some delay to wait for the ImageLoaderThread
        time.sleep(0.3)
        _qapp.processEvents()
        self.assertTrue(self._widget._viewer.getActiveImage() is not None)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSliceStack, ):
        test_suite.addTest(
            unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")


