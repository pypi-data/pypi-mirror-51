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
__date__ = "10/01/2018"


from Orange.widgets import widget, gui
from silx.gui import qt
from tomwer.gui.darkref.DarkRefCopyWidget import DarkRefAndCopyWidget
from tomwer.core.darkref.DarkRefs import DarkRefs, logger as DRLogger
from tomwer.web.client import OWClient
from orangecontrib.tomwer.widgets.utils import (convertInputsForOrange, convertOutputsForOrange)
import logging

logger = logging.getLogger(__name__)


class DarkRefAndCopyOW(widget.OWWidget, OWClient):
    """
        A simple widget managing the copy of an incoming folder to an other one

        :param parent: the parent widget
        """
    # note of this widget should be the one registred on the documentation
    name = "dark and flat field construction"
    id = "orange.widgets.tomwer.darkrefs"
    description = "This widget will generate dark refs for a received scan "
    icon = "icons/darkref.svg"
    priority = 25
    category = "esrfWidgets"
    keywords = ["tomography", "dark", "darks", "ref", "refs"]

    inputs = convertInputsForOrange(DarkRefs.inputs)
    outputs = convertOutputsForOrange(DarkRefs.outputs)

    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    def __init__(self, parent=None):
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, (logger, DRLogger))

        self.widget = DarkRefAndCopyWidget(parent=self)
        self._layout = gui.vBox(self.mainArea, 'boxStackViewer').layout()
        self._layout.addWidget(self.widget)
        self.setForceSync = self.widget.setForceSync

        # expose API
        self.hasRefStored = self.widget.hasRefStored
        self.setModeAuto = self.widget.setModeAuto
        self.setRefsFromScan = self.widget.setRefsFromScan
        self.setSkipIfExisting = self.widget.setSkipIfExisting

        # connect DarkRef with the widget
        self.widget.sigScanReady.connect(self.signalReady)

    def process(self, scanID):
        return self.widget.process(scanID)

    def signalReady(self, scanID):
        self.send("data", scanID)


def main():
    app = qt.QApplication([])
    s = DarkRefAndCopyOW()
    s.show()
    app.exec_()


if __name__ == "__main__":
    main()
