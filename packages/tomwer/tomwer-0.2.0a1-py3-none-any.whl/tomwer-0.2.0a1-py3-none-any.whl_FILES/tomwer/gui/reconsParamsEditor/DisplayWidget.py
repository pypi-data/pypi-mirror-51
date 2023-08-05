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
import logging

logger = logging.getLogger(__name__)


class DisplayWidget(H5StructEditor, qt.QWidget):
    """
     Create the widget inside the of the Display tab
     """

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        H5StructEditor.__init__(self, structID='FT')

        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self.__buildShowProj())
        self.layout().addWidget(self.__buildShowSlice())
        self.layout().addWidget(self.__buildAngleOffset())

        # spacer
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)

        self._makeConnection()

    def _makeConnection(self):
        self._qcbShowProj.toggled.connect(self._showProjChanged)
        self._qcbShowSlice.toggled.connect(self._showSliceChanged)
        self._qleAngleOffset.editingFinished.connect(self._angleOffsetValueChanged)
        self._qleAngleOffset.editingFinished.connect(self._angleOffsetChanged)

    def __buildShowProj(self):
        self._qcbShowProj = qt.QCheckBox('show graphical proj during reconstruction',
                                         parent=self)
        self.linkCheckboxWithH5Variable(self._qcbShowProj, 'SHOWPROJ')
        return self._qcbShowProj

    def _showProjChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='FT',
                                               paramID='SHOWPROJ',
                                               value=int(b))

    def __buildShowSlice(self):
        self._qcbShowSlice = qt.QCheckBox('show graphical slice during reconstruction',
                                          parent=self)
        self.linkCheckboxWithH5Variable(self._qcbShowSlice, 'SHOWSLICE')
        return self._qcbShowSlice

    def _showSliceChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='FT',
                                               paramID='SHOWSLICE',
                                               value=int(b))

    def __buildAngleOffset(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QHBoxLayout())
        widget.layout().addWidget(qt.QLabel('Final image rotation angle (degree):',
                                            parent=widget))

        self._qleAngleOffset = qt.QLineEdit('', widget)
        validator = qt.QDoubleValidator(parent=self._qleAngleOffset)
        self._qleAngleOffset.setValidator(validator)
        widget.layout().addWidget(self._qleAngleOffset)
        self.LinkLineEditWithH5Variable(self._qleAngleOffset, 'ANGLE_OFFSET_VALUE', float)

        # Since the OctaveH5 has to have the ANGLE_OFFSET parameter we are
        # defining it in regards of ANGLE_OFFSET_VALUE
        # this parameter is hidden and the user can't interacte with it
        self.linkGroupWithH5Variable(group=None,
                                     h5ParamName='ANGLE_OFFSET',
                                     setter=None,
                                     getter=self._getAngleOffsetParamVal)

        return widget

    def _getAngleOffsetParamVal(self):
        """

        :return: True if ANGLE_OFFSET_VALUE != 0
        """
        return int(float(self._qleAngleOffset.text()) != 0.0)

    def _angleOffsetChanged(self):
        if self._isLoading is False:
            value = self._getAngleOffsetParamVal()
            ReconsParam().setValue(structID='FT',
                                               paramID='ANGLE_OFFSET',
                                               value=value)

    def _angleOffsetValueChanged(self):
        if self._isLoading is False:
            value = float(self._qleAngleOffset.text())
            ReconsParam().setValue(structID='FT',
                                               paramID='ANGLE_OFFSET_VALUE',
                                               value=value)
