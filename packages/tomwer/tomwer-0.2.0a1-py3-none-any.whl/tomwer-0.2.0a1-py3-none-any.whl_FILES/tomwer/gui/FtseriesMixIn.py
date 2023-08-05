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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "05/01/2018"


from silx.gui import qt
from tomwer.gui.reconsParamsEditor import ReconsParamsEditor
from tomwer.gui.H5FileDialog import H5FileDialog
from tomwer.core.ftseries.Ftseries import Ftseries
from tomwer.core.ftseries.ReconstructionStack import ReconstructionStack
from tomwer.core.ReconsParams import ReconsParam


class _FtseriesMixIn(Ftseries):
    """
    MixIn class to avoid redefinition of code between the orange widget
    :class:`FtseriesWidget` and the qt widget :class:`_FtseriesWidget` used
    for the ftserie application
    """

    _sizeHint = qt.QSize(700, 600)

    def __init__(self):
        # TODO : should be included in the Ftserie class but here to avoid cyclic
        # import
        self.reconsStack = ReconstructionStack()
        self.reconsStack.sigReconsMissParams.connect(self.updateReconsParam)
        self.reconsStack.sigReconsFinished.connect(self._signalReconsReady)

        self._fileEditor = None
        self.__buildGUI()
        self._useThread = True

        Ftseries.__init__(self)

    def isReconsParamsSaved(self):
        """

        :return: True if some previous reconstruction parameters have been
                 saved previously.
        """
        return not (self.reconsParams.params == {})

    def __buildGUI(self):
        """Main function to call the GUI"""
        self.layout().addWidget(self.getFileEditor())
        self.layout().addWidget(self.__buildH5Exploration())
        self.layout().addWidget(self.__buildControl())

    def __buildH5Exploration(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QVBoxLayout())
        widget.layout().setContentsMargins(0, 0, 0, 0)

        self._optH5Exploration = qt.QCheckBox('Explore dataset for .h5', parent=widget)
        tooltip = 'If activated, will explore the dataset to check if a *.h5 file exists. \n'
        tooltip += 'If such a file exists then we will load parameters from this file '
        tooltip += 'to run reconstruction. \n'
        tooltip += 'If none of this file exists then we will use the '
        tooltip += 'recontruction parameters defined from FTSerieWidget.'
        self._optH5Exploration.setToolTip(tooltip)
        widget.layout().addWidget(self._optH5Exploration)
        self._optH5Exploration.toggled.connect(self.setH5Exploration)

        spacer = qt.QWidget(widget)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        widget.layout().addWidget(spacer)

        return widget

    def __buildControl(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QVBoxLayout())
        widget.layout().setContentsMargins(0, 0, 0, 0)

        widgetLoadSave = qt.QWidget(self)
        widgetLoadSave.setLayout(qt.QHBoxLayout())
        widgetLoadSave.layout().setContentsMargins(0, 0, 0, 0)

        self._loadButton = qt.QPushButton('Load')
        self._loadButton.setToolTip('Will load reconstruction parameters existing in the given file')
        style = qt.QApplication.style()
        self._loadButton.setIcon(style.standardIcon(qt.QStyle.SP_FileIcon))
        self._loadButton.pressed.connect(self.askUserAndLoad)
        widgetLoadSave.layout().addWidget(self._loadButton)
        self._loadButton.setShortcut(qt.QKeySequence.Open)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        widgetLoadSave.layout().addWidget(spacer)

        self._saveAs = qt.QPushButton('Save as')
        self._saveAs.setToolTip('Store the current reconstruction parameters into a .h5 file')
        style = qt.QApplication.style()
        self._saveAs.setIcon(style.standardIcon(qt.QStyle.SP_DialogSaveButton))
        self._saveAs.pressed.connect(self._saveAsCallBack)
        widgetLoadSave.layout().addWidget(self._saveAs)
        self._saveAs.setShortcut(qt.QKeySequence.Save)

        widgetValidateCancel = qt.QWidget(self)
        widgetValidateCancel.setLayout(qt.QHBoxLayout())
        widgetValidateCancel.layout().setContentsMargins(0, 0, 0, 0)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        widgetValidateCancel.layout().addWidget(spacer)

        self._validateButton = qt.QPushButton('Validate')
        style = qt.QApplication.style()
        self._validateButton.setIcon(style.standardIcon(
            qt.QStyle.SP_DialogApplyButton))
        self._validateButton.pressed.connect(self._validated)
        widgetValidateCancel.layout().addWidget(self._validateButton)

        self._cancelButton = qt.QPushButton('Cancel')
        self._cancelButton.setIcon(style.standardIcon(
            qt.QStyle.SP_DialogCancelButton))
        self._cancelButton.pressed.connect(self.__canceled)
        widgetValidateCancel.layout().addWidget(self._cancelButton)

        widget.layout().addWidget(widgetLoadSave)
        widget.layout().addWidget(widgetValidateCancel)
        # the cancel action is undefined so we don't wan't to show this button
        self._cancelButton.setVisible(False)

        return widget

    def getFileEditor(self):
        if self._fileEditor is None:
            self._fileEditor = ReconsParamsEditor(parent=None)
            self._reconsParamChanged()
            ReconsParam().sigChanged.connect(self._reconsParamChanged)
        return self._fileEditor

    def _reconsParamChanged(self):
        assert self._fileEditor is not None
        self._fileEditor.loadStructures(ReconsParam().params)

    def _updateh5Editor(self, b):
        if self.ftserieReconstruction and self.ftserieReconstruction.h5File:
            self.reload()

    def askUserH5File(self, save=False):
        """
        Ask user path to a h5File

        :param save: True if the file is used to saved the data. If False then
                     try to open one.
        """
        return H5FileDialog.askForH5File(save=save)

    def _saveAsCallBack(self):
        f = H5FileDialog.askForH5File(save=True)
        if f is not None:
            self.save(h5File=f, displayInfo=True)

    def showValidationButtons(self):
        """Set the buttons for reconstruction parameters visible"""
        self._validateButton.setVisible(True)
        self._cancelButton.setVisible(True)

    def hideValidationButtons(self):
        """Set the buttons for reconstruction parameters not visible"""
        self._validateButton.setVisible(False)
        self._cancelButton.setVisible(False)

    def __canceled(self):
        self.reject()

    def _validated(self):
        self.accept()

    def sizeHint(self):
        """Return a reasonable default size"""
        return self._sizeHint

    def processReconstruction(self):
        """Call the core function 'run_reconstruction' of the ftseries script
        which will call octave to process reconstruction
        """
        self.getFileEditor().setEnabled(False)
        Ftseries.processReconstruction(self)
        self.getFileEditor().setEnabled(True)
