# /*##########################################################################
# Copyright (C) 2017 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
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
"""Some widget construction to check if a sample moved"""

__author__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "19/03/2018"


from silx.gui import qt
import functools


class SelectionTable(qt.QTableWidget):
    """Table used to select the color channel to be displayed for each"""
    LABELS = ('radio', 'R', 'G', 'B')

    sigSelectionChanged = qt.Signal()
    """Signal emitted when the selection change"""

    def __init__(self, parent=None):
        qt.QTableWidget.__init__(self, parent)
        self.clear()

    def clear(self):
        qt.QTableWidget.clear(self)
        self.setRowCount(0)
        self.setColumnCount(len(self.LABELS))
        self.setHorizontalHeaderLabels(self.LABELS)
        self.verticalHeader().hide()
        if hasattr(self.horizontalHeader(), 'setSectionResizeMode'):  # Qt5
            self.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        else:  # Qt4
            self.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)

        self.setSortingEnabled(True)
        self._checkBoxes = {}

    def addRadio(self, name):
        row = self.rowCount()
        self.setRowCount(row + 1)
        _item = self._getWidgetItemConstructor()(type=qt.QTableWidgetItem.Type)
        _item.setText(name)
        _item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
        self.setItem(row, 0, _item)

        widgetR = qt.QCheckBox(self)
        self.setCellWidget(row, 1, widgetR)
        callbackR = functools.partial(self._activeRChanged, name)
        widgetR.toggled.connect(callbackR)

        widgetG = qt.QCheckBox(self)
        self.setCellWidget(row, 2, widgetG)
        callbackG = functools.partial(self._activeGChanged, name)
        widgetG.toggled.connect(callbackG)

        widgetB = qt.QCheckBox(self)
        self.setCellWidget(row, 3, widgetB)
        callbackB = functools.partial(self._activeBChanged, name)
        widgetB.toggled.connect(callbackB)

        self._checkBoxes[name] = {'R': widgetR, 'G': widgetG, 'B': widgetB}

    def _activeRChanged(self, name):
        self._updatecheckBoxes('R', name)

    def _activeGChanged(self, name):
        self._updatecheckBoxes('G', name)

    def _activeBChanged(self, name):
        self._updatecheckBoxes('B', name)

    def _updatecheckBoxes(self, color, name):
        assert name in self._checkBoxes
        assert color in self._checkBoxes[name]
        if self._checkBoxes[name][color].isChecked():
            for radioName in self._checkBoxes:
                if radioName != name:
                    self._checkBoxes[radioName][color].blockSignals(True)
                    self._checkBoxes[radioName][color].setChecked(False)
                    self._checkBoxes[radioName][color].blockSignals(False)

        self.sigSelectionChanged.emit()

    def getSelection(self):
        """
        
        :return: dict selected images. Key is the name of the radio, values is
                 the list of active channel.
        """
        res = {}
        for radioName in self._checkBoxes:
            active = []
            for color in ('R', 'G', 'B'):
                if self._checkBoxes[radioName][color].isChecked():
                    active.append(color)
            if len(active) > 0:
                res[radioName] = active
        return res

    def setSelection(self, ddict):
        """

        :param ddict: key: radio name, values: list of active channels
        """
        for radioName in self._checkBoxes:
            for color in ('R', 'G', 'B'):
                self._checkBoxes[radioName][color].blockSignals(True)
                self._checkBoxes[radioName][color].setChecked(False)
                self._checkBoxes[radioName][color].blockSignals(False)
        for radioName in ddict:
            for color in ddict[radioName]:
                self._checkBoxes[radioName][color].blockSignals(True)
                self._checkBoxes[radioName][color].setChecked(True)
                self._checkBoxes[radioName][color].blockSignals(False)
        self.sigSelectionChanged.emit()

    def _getWidgetItemConstructor(self):
        return qt.QTableWidgetItem


class IntAngle(str):
    """Simple class used to order angles"""
    def __new__(cls, *args, **kw):
        return str.__new__(cls, *args, **kw)

    def getAngle(self):
        """Return the acquisition angle as an int"""
        val = self
        if '(' in self:
            val = self.split('(')[0]
        if val.isdigit() is False:
            return False
        else:
            return int(val)

    def getAngleN(self):
        """Return the second information if the acquisition is the first
        one taken at this angle or not."""
        if '(' not in self:
            return 0
        return int(self.split('(')[1][:-1])

    def __lt__(self, other):
        if self.getAngle() == other.getAngle():
            return self.getAngleN() < other.getAngleN()
        else:
            return self.getAngle() < other.getAngle()


class AngleSelectionTable(SelectionTable):
    class _AngleItem(qt.QTableWidgetItem):
        """Simple QTableWidgetItem allowing ordering on angles"""

        def __init__(self, type=qt.QTableWidgetItem.Type):
            qt.QTableWidgetItem.__init__(self, type=type)

        def __lt__(self, other):
            a1 = IntAngle(self.text())
            a2 = IntAngle(other.text())
            return a1 < a2

    def _getWidgetItemConstructor(self):
        return self._AngleItem