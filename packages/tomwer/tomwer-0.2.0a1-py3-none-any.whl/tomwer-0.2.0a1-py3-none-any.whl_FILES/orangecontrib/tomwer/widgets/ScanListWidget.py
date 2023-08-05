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
__date__ = "01/12/2016"

from Orange.widgets import widget, gui
from silx.gui import qt
from collections import OrderedDict
from tomwer.core.utils import logconfig
from tomwer.core.ScanList import ScanList, logger as SLLogger
from Orange.widgets.settings import Setting
from tomwer.gui.QFolderDialog import QScanDialog
from .utils import (convertInputsForOrange, convertOutputsForOrange)
from tomwer.web.client import OWClient
import os
import logging
logger = logging.getLogger("ESRFScanList")


class ScanListWidget(widget.OWWidget, ScanList, OWClient):
    name = "data list"
    id = "orange.widgets.tomwer.scanlist"
    description = "List path to reconstructions/scans. Those path will be send to the next box once validated."
    icon = "icons/scanlist.svg"
    priority = 50
    category = "esrfWidgets"
    keywords = ["tomography", "file", "tomwer", 'folder']

    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    inputs = convertInputsForOrange(ScanList.inputs)
    outputs = convertOutputsForOrange(ScanList.outputs)

    _scanIDs = Setting(list())

    def __init__(self, parent=None):
        """A simple annuary which register all folder containing completed scan

        .. warning: the widget won't check for scan validity and will only
            emit the path to folders to the next widgets

        :param parent: the parent widget
        """
        widget.OWWidget.__init__(self, parent)
        ScanList.__init__(self)
        OWClient.__init__(self, (logger, SLLogger))

        self.items = OrderedDict()
        self.__generateList()
        self.setScanIDs(self._scanIDs)

    def __generateList(self):
        """ Generate the list widget"""
        def getAddAndRmButtons():
            lLayout = qt.QHBoxLayout()
            w = qt.QWidget(self)
            w.setLayout(lLayout)
            self._addButton = qt.QPushButton("Add")
            self._addButton.clicked.connect(self._callbackAddFolder)
            self._rmButton = qt.QPushButton("Remove")
            self._rmButton.clicked.connect(self._callbackRemoveFolder)

            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
            lLayout.addWidget(spacer)
            lLayout.addWidget(self._addButton)
            lLayout.addWidget(self._rmButton)

            return w

        def getSendButton():
            lLayout = qt.QHBoxLayout()
            widget = qt.QWidget(self)
            widget.setLayout(lLayout)
            self._sendButton = qt.QPushButton("Send")
            self._sendButton.clicked.connect(self._sendList)

            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
            lLayout.addWidget(spacer)
            lLayout.addWidget(self._sendButton)

            return widget

        self.listWidget = qt.QListWidget(self)
        layout = gui.vBox(self.mainArea, 'scanlistBox').layout()
        layout.addWidget(self.listWidget)

        layout.addWidget(getAddAndRmButtons())
        layout.addWidget(getSendButton())

    def remove_item(self, item):
        """Remove a given folder
        """
        del self.items[item.text()]
        itemIndex = self.listWidget.row(item)
        self.listWidget.takeItem(itemIndex)
        ScanList.remove(self, item.text())

    def _callbackAddFolder(self):
        """"""
        dialog = QScanDialog(self, multiSelection=True)

        if not dialog.exec_():
            dialog.close()
            return

        foldersSelected = dialog.filesSelected()
        for folder in foldersSelected:
            assert(os.path.isdir(folder))
            self.add(folder)

    def _callbackRemoveFolder(self):
        """"""
        selectedItems = self.listWidget.selectedItems()
        if selectedItems is not None:
            for item in selectedItems:
                self.remove_item(item)

    def add(self, d):
        """Add the folder d in the scan list
        :param d: the path of the directory to add
        :type d: str
        """
        self._addScanIDItem(d)
        ScanList.add(self, d)

    def _addScanIDItem(self, d):
        if(not os.path.isdir(d)):
            warning = "Skipping the observation of %s, directory not existing on the system" % d
            logger.info(warning,
                           extra={logconfig.DOC_TITLE: self._scheme_title})
        elif d in self.items:
            warning = "The directory %s is already in the scan list" % d
            logger.info(warning,
                           extra={logconfig.DOC_TITLE: self._scheme_title})
        else:
            self.items[d] = qt.QListWidgetItem(d, self.listWidget)

    def setScanIDs(self, scanIDs):
        [self._addScanIDItem(item) for item in scanIDs]
        ScanList.setScanIDs(self, scanIDs)

    def clear(self):
        """Remove all items on the list"""
        self.listWidget.clear()
        self.items = OrderedDict()
        ScanList.clear(self)

    def _sendList(self):
        """Send a signal for each list to the next widget"""
        for d in self.items:
            mess = "sending one scan %s" % d
            logger.debug(mess,
                         extra={logconfig.DOC_TITLE: self._scheme_title,
                                logconfig.SCAN_ID: d})
            self.send("data", d)


def main():
    app = qt.QApplication([])
    s = ScanListWidget()
    s.show()
    app.exec_()


if __name__ == "__main__":
    main()
