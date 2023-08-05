#/*##########################################################################
# Copyright (C) 2016-2017 European Synchrotron Radiation Facility
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

__author__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "10/01/2018"


from silx.gui import qt
from tomwer.gui.H5StructEditor import H5StructEditor
from tomwer.core.ReconsParams import ReconsParam
from tomwer.core.utils import pyhstutils
import logging

logger = logging.getLogger(__name__)


class PyHSTWidget(H5StructEditor, qt.QWidget):
    """
    Definition of the PyHST tab to edit the PyHST parameters
    """

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        H5StructEditor.__init__(self, structID='PYHSTEXE')

        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self.__buildPYHSTVersion())
        self.layout().addWidget(self.__buildPYHSTOfficialVersion())

        self._qcbverbose = qt.QCheckBox('verbose',
                                        parent=self)
        self.layout().addWidget(self._qcbverbose)
        self.linkCheckboxWithH5Variable(self._qcbverbose, 'VERBOSE', invert=False)

        self.layout().addWidget(self.__buildVerboseFile())
        self.layout().addWidget(self.__buildMakeOAR())

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)

        self._qcbverbose.setChecked(False)
        self._versoseFileWidget.setVisible(True)
        self._qcbverbose.toggled.connect(self._versoseFileWidget.setDisabled)

        self._makeConnection()

    def _makeConnection(self):
        self._qcbverbose.toggled.connect(self._verboseChanged)
        self._qcbPyHSTVersion.currentIndexChanged.connect(self._pyHSTVersionChanged)
        self._qleVerboseFile.editingFinished.connect(self._verboseFileChanged)
        self._makeOARFileCB.toggled.connect(self._makeOARChanged)

    def _verboseChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='PYHSTEXE',
                                               paramID='VERBOSE',
                                               value=int(b))

    def __buildPYHSTVersion(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QHBoxLayout())

        # create the PyHST version combobox
        widget.layout().addWidget(qt.QLabel("PyHST version : ", parent=widget))
        self._qcbPyHSTVersion = qt.QComboBox(parent=self)
        widget.layout().addWidget(self._qcbPyHSTVersion)
        self.linkComboboxWithH5Variable(self._qcbPyHSTVersion,
                                        'EXE',
                                        fitwithindex=False,
                                        setDefault=False)

        # try to get the PyHST dir
        d = pyhstutils._getPyHSTDir()
        if d is None:
            raise logger.warning("""Can't find the directory containing the PyHST
                directory. Please set the environment variable
                PYHST_DIR and run again""")

        availablePyHSTVersion = pyhstutils._findPyHSTVersions(d)
        if len(availablePyHSTVersion) == 0:
            self.__warmNoPyHSTFound(d)
            pass
        else:
            [self._qcbPyHSTVersion.addItem(exe) for exe in availablePyHSTVersion]

        return widget

    def __buildMakeOAR(self):
        self._makeOARFileCB = qt.QCheckBox('make OAR file', parent=self)
        self.linkCheckboxWithH5Variable(qcheckbox=self._makeOARFileCB,
                                        h5ParamName='MAKE_OAR_FILE')
        self._makeOARFileCB.toggled.connect(self._makeOARChanged)
        return self._makeOARFileCB

    def _pyHSTVersionChanged(self):
        if self._isLoading is False:
            value = self._qcbPyHSTVersion.currentText()
            ReconsParam().setValue(structID='PYHSTEXE',
                                               paramID='EXE',
                                               value=value)

    def _makeOARChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='PYHSTEXE',
                                               paramID='MAKE_OAR_FILE',
                                               value=int(b))

    def __buildPYHSTOfficialVersion(self):
        """build the official version QLine edit and update the _qcbPyHSTVersion
        combobox so should always be called after.
        """
        widget = qt.QWidget(self)
        widget.setLayout(qt.QHBoxLayout())
        widget.layout().addWidget(qt.QLabel('PyHST official version',
                                            parent=widget))
        self._qlOfficalVersion = qt.QLabel('', parent=widget)
        widget.layout().addWidget(self._qlOfficalVersion)
        self.linkGroupWithH5Variable(self._qlOfficalVersion,
                                     'OFFV',
                                     getter=self._qlOfficalVersion.text,
                                     setter=self._qlOfficalVersion.setText)

        return widget

    def __warmNoPyHSTFound(self, directory):
        """Simple function displaying a MessageBox that PyHST haven't been found
        """
        text = "No executable of PyHST have been found in %s." % directory
        text += " You might set the environment variable PYHST_DIR "
        text += " or install PyHST."
        logger.info(text)

    def __buildVerboseFile(self):
        self._versoseFileWidget = qt.QWidget(self)
        self._versoseFileWidget.setLayout(qt.QHBoxLayout())
        self._versoseFileWidget.layout().addWidget(
            qt.QLabel('name of the PyHST information output file', parent=self))
        self._qleVerboseFile = qt.QLineEdit('', parent=None)
        self._versoseFileWidget.layout().addWidget(self._qleVerboseFile)
        self.LinkLineEditWithH5Variable(self._qleVerboseFile, 'VERBOSE_FILE')
        return self._versoseFileWidget

    def _verboseFileChanged(self):
        if self._isLoading is False:
            value = self._qleVerboseFile.text()
            ReconsParam().setValue(structID='PYHSTEXE',
                                               paramID='VERBOSE_FILE',
                                               value=value)
