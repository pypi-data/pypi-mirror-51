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
__date__ = "07/12/2016"

from Orange.widgets import widget
from silx.gui import qt
from tomwer.core.FolderTransfert import FolderTransfert, logger as FTLogger
from .utils import (convertInputsForOrange, convertOutputsForOrange)
from tomwer.web.client import OWClient
import logging

logger = logging.getLogger(__name__)


class FolderTransfertWidget(widget.OWWidget, FolderTransfert, OWClient):
    """
    A simple widget managing the copy of an incoming folder to an other one

    :param parent: the parent widget
    """
    name = "data transfert"
    id = "orange.widgets.tomwer.foldertransfert"
    description = "This widget insure data transfert of the received data "
    description += "to the given directory"
    icon = "icons/folder-transfert.svg"
    priority = 30
    category = "esrfWidgets"
    keywords = ["tomography", "transfert", "cp", "copy", "move", "file",
                "tomwer", 'folder']

    inputs = convertInputsForOrange(FolderTransfert.inputs)
    outputs = convertOutputsForOrange(FolderTransfert.outputs)

    want_main_area = False
    resizing_enabled = False
    compress_signal = False

    def __init__(self, parent=None):
        FolderTransfert.__init__(self)
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, (logger, FTLogger))

    def _requestFolder(self):
        """Launch a QFileDialog to ask the user the output directory"""
        dialog = qt.QFileDialog(self)
        dialog.setWindowTitle("Destination folder")
        dialog.setModal(1)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)

        if not dialog.exec_():
            dialog.close()
            return None

        return dialog.selectedFiles()[0]

    def signalTransfertOk(self, scanID):
        self.send("data", scanID)

