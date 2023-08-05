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
from tomwer.gui.viewerQWidget import ImageStackViewerValidator
from tomwer.gui.QFolderDialog import QScanDialog
from orangecontrib.tomwer.widgets.utils import (convertInputsForOrange, convertOutputsForOrange)
from tomwer.core.ScanValidator import ScanValidator, logger as SVLogger
from tomwer.core.ftseries.FtserieReconstruction import FtserieReconstruction
from tomwer.web.client import OWClient
import os
import logging

logger = logging.getLogger(__name__)


class ScanValidatorWidget(widget.OWWidget, ScanValidator):
    name = "data validator"
    id = "orange.widgets.tomwer.scanvalidator"
    description = """Widget displaying results of a reconstruction and asking to
    the user if he want to validate or not the reconstruction. User can also ask
    for some modification on the reconstruction parameters"""
    icon = "icons/validator.png"
    priority = 23
    category = "esrfWidgets"
    keywords = ["tomography", "file", "tomwer", "acquisition", "validation"]

    inputs = convertInputsForOrange(ScanValidator.inputs)
    outputs = convertOutputsForOrange(ScanValidator.outputs)

    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    _warnValManualShow = False
    """
    used to know if the message to inform user about `validate manually` has
    already been displayed.
    This informative message will be show under the following conditions:

        * the scanValidator contains at least `_NB_SCAN_BF_WARN`
        * this dialog have never been showed in the current session.
    """

    _NB_SCAN_BF_WARN = 10
    """
    Limit of stored scans before displaying the informative message about
    `validate manually` checkbox
    """

    def __init__(self, parent=None, ftserie=None):
        """a simple viewer of image stack

        :param parent: the parent widget
        :param ftserie: an ftserie to validate
        """
        widget.OWWidget.__init__(self, parent)
        ScanValidator.__init__(self)
        OWClient.__init__(self, (logger, SVLogger))

        self._buildGUI(ftserie)

    def _buildGUI(self, ftserie):
        self.tabsWidget = {}
        # building GUI
        self._scanWidgetLayout = gui.hBox(self.mainArea, 'boxStackViewer').layout()
        self._scanWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = ImageStackViewerValidator(self)
        self._scanWidgetLayout.addWidget(self.widget)

        lateralWidget = qt.QWidget(parent=self)
        lateralWidget.setLayout(qt.QVBoxLayout())
        lateralWidget.layout().setContentsMargins(0, 0, 0, 0)

        # build the slider
        sliderWidget = qt.QWidget(parent=lateralWidget)
        sliderWidget.setLayout(qt.QHBoxLayout())

        self._qslider = qt.QSlider(qt.Qt.Vertical, parent=sliderWidget)
        self._qslider.valueChanged.connect(self.updateStackView)
        sliderWidget.layout().addWidget(self._qslider)

        sliderWidget.layout().addWidget(_VerticalLabel('stack of received scan',
                                                       parent=sliderWidget,
                                                       revert=True))
        lateralWidget.layout().addWidget(sliderWidget)

        # add scan button
        self._addSlideButton = qt.QPushButton('Add scan', parent=lateralWidget)
        self._addSlideButton.pressed.connect(self._addScanCallBack)

        lateralWidget.layout().addWidget(self._addSlideButton)
        self._scanWidgetLayout.addWidget(lateralWidget)

        self.addScan(ftserie)
        self._connectValidationWidget()

    def _connectValidationWidget(self):
        validationWidget = self.widget.validationWidget
        validationWidget.sigValidateScan.connect(self._validateCurrentScan)
        validationWidget.sigCancelScan.connect(self._cancelCurrentScan)
        validationWidget.sigChangeReconstructionParametersScan.connect(self._changeReconsParamCurrentScan)
        validationWidget.toggled.connect(self.setManualValidation)

    def getValidationWidget(self, tab):
        return self.widget.validationWidget

    def addScan(self, ftserie):
        if ftserie is None:
            return
        ScanValidator.addScan(self, ftserie)
        self.updateStackView()
        id = ftserie if type(ftserie) is str else ftserie.scanID
        # in the case the memory is full, the scan can have been already
        # validated and so not accessible
        if id in self._scansToValidate:
            self.setActiveScan(self._scansToValidate[id])

        if self._warnValManualShow is False and \
                len(self._scansToValidate) >= self._NB_SCAN_BF_WARN:
            mess = "Please note that the scanValidator is actually storing %s " \
                   "scan(s). \n" \
                   "Scan need to be validated manually in order to continue " \
                   "the workflow processing. \n" \
                   "you can either validate scan manually or uncheck the " \
                   "`validate manually` check box." % self._NB_SCAN_BF_WARN

            mess = qt.QMessageBox(parent=self, icon=qt.QMessageBox.Information,
                                  text=mess)
            mess.setModal(False)
            mess.show()
            self._warnValManualShow = True

    def updateStackView(self):
        """
        Update the stack view.
         If active is given then this will be the new active value of the stack
        """
        currentDisplayed = self.getCurrentScan()
        if currentDisplayed is None and len(self._scansToValidate) > 0:
            currentDisplayed = list(self._scansToValidate.keys())[0]

        self._qslider.setRange(0, len(self._scansToValidate) -1)
        self.setActiveScan(currentDisplayed)

    def setActiveScan(self, scan):
        _scanID = scan
        if isinstance(_scanID, FtserieReconstruction):
            _scanID = scan.scanID

        self.widget.clear()
        if _scanID is None or _scanID not in self._scansToValidate:
            return
        else:
            self.widget.updateData(self._scansToValidate[_scanID])
            self.widget.validationWidget.setEnabled(True)
            index = list(self._scansToValidate.keys()).index(_scanID)
            self._qslider.valueChanged.disconnect(self.updateStackView)
            index = self._qslider.setValue(index)
            self._qslider.valueChanged.connect(self.updateStackView)

    def getCurrentScan(self):
        """

        :return: the scan currently displayed on the viewer 
        """
        index = self._qslider.value()
        if index >= len(self._scansToValidate):
            return None
        else:
            return list(self._scansToValidate.keys())[index]

    def _validateCurrentScan(self):
        """This will validate the ftserie currently displayed

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate. Execution order in this case is
            not insured.
        """
        ScanValidator._validateScan(self, self.getCurrentScan())
        self.updateStackView()

    def _cancelCurrentScan(self):
        """This will cancel the ftserie currently displayed

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate. Execution order in this case is
            not insured.
        """
        ScanValidator._cancelScan(self, self.getCurrentScan())
        self.updateStackView()

    def _changeReconsParamCurrentScan(self):
        """This will emit a signal to request am acquisition for the current
        ftSerieReconstruction

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate. Execution order in this case is
            not insured.
        """
        ScanValidator._changeReconsParam(self, self.getCurrentScan())
        self.updateStackView()

    def _addScanCallBack(self):
        dialog = QScanDialog(self, multiSelection=True)

        if not dialog.exec_():
            dialog.close()
            return

        foldersSelected = dialog.filesSelected()
        for folder in foldersSelected:
            assert(os.path.isdir(folder))
            self.addScan(FtserieReconstruction(folder))

        if len(dialog.filesSelected()) > 0:
            activeScan = dialog.filesSelected()[-1]
            self.setActiveScan(activeScan)

    def _validateStack(self):
        ScanValidator._validateStack(self)
        self.updateStackView()

    def _sendScanReady(self, scanID):
        self.send("data", scanID)

    def _sendScanCanceledAt(self, scanID):
        self.send('scanCanceledAt', scanID)

    def _sendUpdateReconsParam(self, ftserie):
        self.send('change recons params', ftserie)


class _VerticalLabel(qt.QLabel):
    """Display vertically the given text
    """
    def __init__(self, text, parent=None, revert=False):
        """

        :param text: the legend
        :param parent: the Qt parent if any
        """
        qt.QLabel.__init__(self, text, parent)
        self.revert=revert
        self.setLayout(qt.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def paintEvent(self, event):
        painter = qt.QPainter(self)
        painter.setFont(self.font())

        painter.translate(0, self.rect().height())
        painter.rotate(90)
        if self.revert:
            newRect = qt.QRect(-self.rect().height(), -self.rect().width(), self.rect().height(), self.rect().width())

        painter.drawText(newRect, qt.Qt.AlignHCenter, self.text())

        fm = qt.QFontMetrics(self.font())
        preferedHeight = fm.width(self.text())
        preferedWidth = fm.height()
        self.setFixedWidth(preferedWidth)
        self.setMinimumHeight(preferedHeight)


def main():
    import tempfile
    from tomwer.core import utils

    folder = tempfile.mkdtemp()
    utils.mockAcquisition(folder)
    utils.mockReconstruction(folder)

    app = qt.QApplication([])
    s = ScanValidatorWidget(parent=None,
                            ftserie=FtserieReconstruction(folder))

    for f in range(3):
        folder = tempfile.mkdtemp()
        utils.mockAcquisition(folder)
        utils.mockReconstruction(folder, volFile=True)
        s.addScan(FtserieReconstruction(folder))
    s.show()
    app.exec_()


if __name__ == "__main__":
    main()
