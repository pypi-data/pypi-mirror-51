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


from silx.gui import qt
from tomwer.gui.QFolderDialog import QScanDialog
from collections import OrderedDict
import logging
import os

logger = logging.getLogger(__file__)


class ScanSelectorWidget(qt.QWidget):
    """Widget used to select a scan on a list"""

    sigSelectionChanged = qt.Signal(str)
    """Signal emitted when the selection changed"""

    def __init__(self, parent=None):
        def getAddAndRmButtons():
            lLayout = qt.QHBoxLayout()
            w = qt.QWidget(self)
            w.setLayout(lLayout)
            self._addButton = qt.QPushButton("Add")
            self._addButton.clicked.connect(self._callbackAddFolder)
            self._rmButton = qt.QPushButton("Remove")
            self._rmButton.clicked.connect(self._callbackRemoveFolder)

            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Expanding,
                                 qt.QSizePolicy.Minimum)
            lLayout.addWidget(spacer)
            lLayout.addWidget(self._addButton)
            lLayout.addWidget(self._rmButton)

            return w

        def getSendButton():
            lLayout = qt.QHBoxLayout()
            widget = qt.QWidget(self)
            widget.setLayout(lLayout)
            self._sendButton = qt.QPushButton("Select")
            self._sendButton.clicked.connect(self._selectActiveScan)

            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Expanding,
                                 qt.QSizePolicy.Minimum)
            lLayout.addWidget(spacer)
            lLayout.addWidget(self._sendButton)

            return widget

        qt.QWidget.__init__(self, parent)
        self._scanIDs = list()
        self.items = OrderedDict()
        self.setLayout(qt.QVBoxLayout())
        self.listWidget = qt.QListWidget(self)
        self.listWidget.setSortingEnabled(True)
        self.layout().addWidget(self.listWidget)
        self.layout().addWidget(getAddAndRmButtons())
        self.layout().addWidget(getSendButton())

    def add(self, scanID):
        """
        Add given scan from the list

        :param scanID: path to the acquisition
        """
        if (not os.path.isdir(scanID)):
            warning = "Skipping the observation of %s, directory not " \
                      "existing on the system" % scanID
            logger.warning(warning)
        elif scanID in self.items:
            warning = "The directory %s is already in the scan list" % scanID
            logger.warning(warning)
        else:
            self.items[scanID] = qt.QListWidgetItem(scanID, self.listWidget)
            self._scanIDs.append(scanID)

    def remove(self, scanID):
        """
        Remove given scan from the list

        :param scanID: path to the acquisition
        """
        if scanID in self._scanIDs:
            self._scanIDs.remove(scanID)

        item = self.items[scanID]
        del self.items[scanID]
        itemIndex = self.listWidget.row(item)
        self.listWidget.takeItem(itemIndex)

    def removeItem(self, item):
        self.remove(str(item.text()))

    def _callbackAddFolder(self):
        """"""
        dialog = QScanDialog(self, multiSelection=True)

        if not dialog.exec_():
            dialog.close()
            return

        for folder in dialog.filesSelected():
            assert (os.path.isdir(folder))
            self.add(folder)

    def _selectActiveScan(self):
        sItem = self.listWidget.selectedItems()
        if sItem and len(sItem) is 1:
            scanID = sItem[0].text()
            self.sigSelectionChanged.emit(scanID)
        else:
            logger.warning('No active scan detected')

    def _callbackRemoveFolder(self):
        """"""
        selectedItems = self.listWidget.selectedItems()
        if selectedItems is not None:
            for item in selectedItems:
                self.removeItem(item)


if __name__ == '__main__':
    qapp = qt.QApplication([])
    widget = ScanSelectorWidget()
    widget.show()
    widget.add('/nobackup/linazimov/payno/datasets/id19')
    widget.add('/nobackup/linazimov/payno/datasets/id16b')
    widget.add('/nobackup')
    widget.remove('/nobackup')
    qapp.exec_()