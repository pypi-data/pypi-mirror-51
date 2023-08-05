# coding: utf-8
#/*##########################################################################
# Copyright (C) 2017 European Synchrotron Radiation Facility
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

"""
This module is used to define a set of folders to be emitted to the next box.
"""

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "05/07/2017"


from tomwer.core.BaseProcess import BaseProcess
from silx.gui import qt
import logging

logger = logging.getLogger(__file__)


class ScanList(BaseProcess):
    """Simple class listing the scan ID to process"""
    _scanIDs = list()
    # list of all the scansID to be processed
    inputs = []
    outputs = [{'name': "data",
                'type': str,
                'doc': "signal emitted when the scan is completed"}]

    scanReady = qt.Signal(str)

    def __init__(self):
        BaseProcess.__init__(self, logger)

    def start(self):
        """function to launch if is the first box to be executed
        """
        self._sendList()

    def setProperties(self, properties):
        if '_scanIDs' in properties:
            self.setScanIDs(properties['_scanIDs'])
        else:
            raise ValueError('scansID no included in the widget properties')

    def setScanIDs(self, setScanIDs):
        self._scanIDs = setScanIDs

    def add(self, folder):
        """Add a folder to the list

        :param str folder: the path to the folder for the scan to add
        """
        self._scanIDs.append(folder)

    def remove(self, folder):
        """Remove a folder to the list

        :param str folder: the path to the folder for the scan to add
        """
        if folder in self._scanIDs:
            self._scanIDs.remove(folder)

    def clear(self):
        """clear the list"""
        self._scanIDs.clear()

    def _sendList(self):
        for folder in self._scanIDs:
            self.scanReady.emit(folder)


class ScanListP(ScanList, qt.QObject):
    """For now to avoid multiple inheritance from QObject with the process widgets
    we have to define two classes. One only for the QObject inheritance
    """

    data = ScanList.scanReady

    def __init__(self):
        ScanList.__init__(self)
        qt.QObject.__init__(self)
