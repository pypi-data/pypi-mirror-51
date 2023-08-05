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

__authors__ = ["C. Nemoz", "H. Payno"]
__license__ = "MIT"
__date__ = "25/05/2018"

from Orange.widgets import widget, gui
from Orange.canvas.registry.description import InputSignal, OutputSignal
from tomwer.web.client import OWClient
from tomwer.gui.ScanSelectorWidget import ScanSelectorWidget
import logging

logger = logging.getLogger(__file__)


class ScanListWidget(widget.OWWidget, OWClient):
    name = "data selector"
    id = "orange.widgets.tomwer.scanselector"
    description = "List all received scan. Then user can select a specific" \
                  "scan to be passed to the next widget."
    icon = "icons/scanselector.svg"
    priority = 42
    category = "esrfWidgets"
    keywords = ["tomography", "selection", "tomwer", 'folder']

    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    inputs = [InputSignal(name="data", handler='addScan', type=str)]
    outputs = [OutputSignal(name="data", type=str)]

    def __init__(self, parent=None):
        """
        """
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, (logger))

        self.widget = ScanSelectorWidget(parent=self)
        self.widget.sigSelectionChanged.connect(self.changeSelection)
        layout = gui.vBox(self.mainArea, 'scanselectorBox').layout()
        layout.addWidget(self.widget)

    def addScan(self, scanID):
        if scanID:
            self.widget.add(scanID)

    def changeSelection(self, scanID):
        if scanID:
            self.send("data", scanID)
