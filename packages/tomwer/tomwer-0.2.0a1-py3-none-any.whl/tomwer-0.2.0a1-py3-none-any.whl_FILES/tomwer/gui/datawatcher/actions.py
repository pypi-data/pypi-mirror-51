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
__date__ = "18/02/2018"


from tomwer.gui import icons as tomwericons
from silx.gui import qt


class _PlaceboDialog(qt.QDialog):
    """Simple dialog, not affecting contained data or widget"""

    def __init__(self, parent, title, containedWidget):
        qt.QDialog.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self.setWindowTitle(title)

        types = qt.QDialogButtonBox.Close
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self._buttons.button(
            qt.QDialogButtonBox.Close).clicked.connect(self.accept)
        self.layout().addWidget(containedWidget)
        self.layout().addWidget(self._buttons)


class _HistoryAction(qt.QAction):
    """
    Action displaying the history of finished scans
    """

    def __init__(self, parent, historyWidget):
        icon = tomwericons.getQIcon('history')
        qt.QAction.__init__(self, icon, 'history', parent)
        self.setCheckable(True)
        self.dialog = _PlaceboDialog(parent=None,
                                     title='last found scans',
                                     containedWidget=historyWidget)
        self.toggled[bool].connect(self._triggered)
        self.dialog.finished.connect(self.uncheck)

    def _triggered(self):
        self.dialog.setVisible(self.isChecked())

    def uncheck(self):
        self.setChecked(False)


class _ConfigurationAction(qt.QAction):
    """
    Action to show the configuration dialog
    """

    def __init__(self, parent, configWidget):
        icon = tomwericons.getQIcon('parameters')
        qt.QAction.__init__(self, icon, 'configuration', parent)
        self.setCheckable(True)
        self.dialog = _PlaceboDialog(parent=None,
                                     title='data watcher configuration',
                                     containedWidget=configWidget)
        self.toggled[bool].connect(self._triggered)
        self.dialog.finished.connect(self.uncheck)

    def _triggered(self):
        self.dialog.setVisible(self.isChecked())

    def uncheck(self):
        self.setChecked(False)


class _ObservationAction(qt.QAction):
    """
    Action to show the observation dialog
    """

    def __init__(self, parent, obsWidget):
        icon = tomwericons.getQIcon('loop')
        qt.QAction.__init__(self, icon, 'observations', parent)
        self.setCheckable(True)
        self.dialog = _PlaceboDialog(parent=None,
                                     title='on going observation',
                                     containedWidget=obsWidget)
        self.toggled[bool].connect(self._triggered)
        self.dialog.finished.connect(self.uncheck)

    def _triggered(self):
        self.dialog.setVisible(self.isChecked())

    def uncheck(self):
        self.setChecked(False)
