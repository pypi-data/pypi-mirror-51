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


__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "15/05/2017"

import os
# env variable used for tomwer unit test using xvfb-run. Failed to load openGLX
# when import AnyQt. Don't know why for now
if os.environ.get("USE_WEB_ENGINE") and \
                os.environ.get("USE_WEB_ENGINE", "") == 'False':
        USE_WEB_ENGINE = False
        QWebView = None
        from AnyQt.QtNetwork import QNetworkDiskCache
else:
    # warning the QWebEngine need to be loaded before a QApplication is runned
    try:
        from AnyQt.QtWebEngineWidgets import QWebEngineView
        USE_WEB_ENGINE = True
    except ImportError:
        try:
            from AnyQt.QtWebKitWidgets import QWebView
        except ImportError:
            QWebView = None
        from AnyQt.QtNetwork import QNetworkDiskCache
        USE_WEB_ENGINE = False

# import os
import unittest

from ..gui import test as test_gui
from ..core import test as test_core
from ..simpleworkflow import test as test_simpleworkflow
from . import test_scripts

def suite(loader=None):
    # test_dir = os.path.dirname(__file__)
    # if loader is None:
    #     loader = unittest.TestLoader()

    test_suite = unittest.TestSuite()
    test_suite.addTest(test_core.suite())
    test_suite.addTest(test_gui.suite())
    test_suite.addTest(test_simpleworkflow.suite())
    test_suite.addTest(test_scripts.suite())

    return test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
