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
from tomwer.gui.H5StructEditor import H5StructsEditor
import logging
from tomwer.core.ReconsParams import ReconsParam

logger = logging.getLogger(__name__)


class FTAxisWidget(H5StructsEditor, qt.QWidget):
    """
    Definition of the Main tab to edit the AXIS parameters
    """

    ACCURATE = 'accurate'

    HIGHLOW = 'highlow'

    MANUAL = 'manual'

    FIXED = 'fixed'

    EXCENTRATED = 'excentrated'

    NEAR = 'near'

    READ = 'read'

    DEFAULT_POS = ACCURATE

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        H5StructsEditor.__init__(self, structsManaged=('FTAXIS', 'FT'))

        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self.__buildPosition())
        self.layout().addWidget(self.__buildCenterReconstructedRegion())
        self.layout().addWidget(self.__buildCOR())
        self.layout().addWidget(self.__buildUseImagesDuringScan())
        self.layout().addWidget(self.__buildCORError())
        self.layout().addWidget(self.__buildPlotFigure())

        line = qt.QFrame(self)
        line.setFrameShape(qt.QFrame.HLine)
        self.layout().addWidget(line)

        self.layout().addWidget(self.__buildHA())
        self.layout().addWidget(self.__buildOversampling())
        self.layout().addWidget(self.__buildHalfAcq())
        self.layout().addWidget(self.__buildForceHalfAcq())

        self._qcbHalfAcq.stateChanged.connect(self.__HalfAcqStateChanged)
        self._qcbHalfAcq.toggled.connect(self._updateHAView)
        self._qcbHA.toggled.connect(self._oversampWidget.setVisible)

        # spacer
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)

        self._makeConnection()

    def _makeConnection(self):
        self._qcbCenterReconsRegion.toggled.connect(self._centerReconsRegionChanged)
        self._qrbCOR_0_180.toggled.connect(self._CORPositionChanged)
        self._qcbuseImgsDuringScan.toggled.connect(self._useImageDuringScanChanged)
        self._qsbOversampling.valueChanged.connect(self._oversamplingChanged)
        self._qcbPosition.currentIndexChanged.connect(self._positionChanged)
        self._qlePositionValue.editingFinished.connect(self._positionValueChanged)
        self._qcbPlotFigure.toggled.connect(self._plotFigureChanged)
        self._qcbHA.toggled.connect(self._HAChanged)
        self._qcbHalfAcq.toggled.connect(self._HALFACQChanged)
        self._qcbForceHA.toggled.connect(self._forceHALFACQChanged)

    def __buildCOR(self):
        self._grpCOR = qt.QGroupBox('Angles used for COR calculation ', parent=self)
        self._grpCOR.setLayout(qt.QHBoxLayout())
        self._qrbCOR_0_180 = qt.QRadioButton('0-180', parent=self._grpCOR)
        self._grpCOR.layout().addWidget(self._qrbCOR_0_180)
        self._qrbCOR_90_270 = qt.QRadioButton('90-270', parent=self._grpCOR)
        self._grpCOR.layout().addWidget(self._qrbCOR_90_270)

        self.linkGroupWithH5Variable(group=self._grpCOR,
                                     structID='FTAXIS',
                                     h5ParamName='COR_POSITION',
                                     setter=self._setCORPosition,
                                     getter=self._getCORPosition)

        return self._grpCOR

    def _CORPositionChanged(self):
        if self._isLoading is False:
            value = self._getCORPosition()
            ReconsParam().setValue(structID='FTAXIS',
                                               paramID='COR_POSITION',
                                               value=value)

    def __buildCenterReconstructedRegion(self):
        self._qcbCenterReconsRegion = qt.QCheckBox(
                                        'Center reconstructed region on rotation axis',
                                        parent=self)
        self.linkCheckboxWithH5Variable(self._qcbCenterReconsRegion,
                                        structID='FTAXIS',
                                        h5ParamName='TO_THE_CENTER')
        return self._qcbCenterReconsRegion

    def _centerReconsRegionChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='FTAXIS',
                                               paramID='TO_THE_CENTER',
                                               value=int(b))

    def __buildCORError(self):
        self._grpCORError = qt.QGroupBox('systematic error on COR calculation',
                                         parent=self)
        self._grpCORError.setCheckable(True)
        self._grpCORError.setChecked(True)
        self._grpCORError.setLayout(qt.QHBoxLayout())

        self._qleCORError = qt.QLineEdit('1', parent=self)
        validator = qt.QIntValidator(parent=self._qleCORError)
        validator.setBottom(1)
        self._qleCORError.setValidator(validator)
        self._grpCORError.layout().addWidget(self._qleCORError)

        self.linkGroupWithH5Variable(self._grpCORError,
                                     structID='FTAXIS',
                                     h5ParamName='COR_ERROR',
                                     setter=self.setCORError,
                                     getter=self.getCORError)

        self._grpCORError.toggled.connect(self._qleCORError.setEnabled)
        return self._grpCORError

    def setCORError(self, val):
        if val == 0:
            self._grpCORError.setChecked(False)
        else:
            self._grpCORError.setChecked(True)
            self._qleCORError.setText(str(val))

    def getCORError(self):
        if self._grpCORError.isChecked():
            return float(self._qleCORError.text())
        else:
            return 0

    def __buildUseImagesDuringScan(self):
        self._qcbuseImgsDuringScan = qt.QCheckBox('use images during scan for axis calculation',
                                                  parent=self)
        self.linkCheckboxWithH5Variable(self._qcbuseImgsDuringScan,
                                        structID='FTAXIS',
                                        h5ParamName='FILESDURINGSCAN')
        return self._qcbuseImgsDuringScan

    def _useImageDuringScanChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='FTAXIS',
                                               paramID='FILESDURINGSCAN',
                                               value=int(b))

    def __buildOversampling(self):
        self._oversampWidget = qt.QWidget(self)
        self._oversampWidget.setLayout(qt.QHBoxLayout())
        self._oversampWidget.layout().addWidget(qt.QLabel('Oversampling '))

        self._qsbOversampling = qt.QSpinBox(parent=self._oversampWidget)
        self._qsbOversampling.setMinimum(1)
        self._oversampWidget.layout().addWidget(self._qsbOversampling)
        self.linkGroupWithH5Variable(group=self._qsbOversampling,
                                     structID='FTAXIS',
                                     h5ParamName='OVERSAMPLING',
                                     setter=self._setOversampling,
                                     getter=self._getOversampling)
        return self._oversampWidget

    def _oversamplingChanged(self):
        if self._isLoading is False:
            ReconsParam().setValue(structID='FTAXIS',
                                               paramID='OVERSAMPLING',
                                               value=self._getOversampling())

    def __buildPosition(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QHBoxLayout())
        # CB rotation axis
        widget.layout().addWidget(qt.QLabel('rotation axis'))
        self._qcbPosition = qt.QComboBox(self)
        self._qcbPosition.addItem(self.ACCURATE)
        self._qcbPosition.addItem(self.HIGHLOW)
        self._qcbPosition.addItem(self.MANUAL)
        self._qcbPosition.addItem(self.FIXED)
        self._qcbPosition.addItem(self.EXCENTRATED)
        self._qcbPosition.addItem(self.NEAR)
        self._qcbPosition.addItem(self.READ)
        widget.layout().addWidget(self._qcbPosition)
        self.linkComboboxWithH5Variable(self._qcbPosition,
                                        structID='FTAXIS',
                                        h5ParamName='POSITION')
        self._updateHAView(False)

        self.indexesAllowingValue = [self._qcbPosition.findText(self.FIXED),
                                     self._qcbPosition.findText(self.NEAR)
                                     ]
        # LineEdit position value
        self._qlePositionValue = qt.QLineEdit('0', parent=widget)
        widget.layout().addWidget(self._qlePositionValue)
        validator = qt.QDoubleValidator(parent=widget)
        self._qlePositionValue.setValidator(validator)
        self._qlePositionValue.hide()
        self.linkGroupWithH5Variable(group=self._qlePositionValue,
                                     structID='FTAXIS',
                                     h5ParamName='POSITION_VALUE',
                                     setter=self._setPositionValue,
                                     getter=self._getPositionValue)

        self._qcbPosition.currentIndexChanged.connect(self._showPositionValue)
        return widget

    def _positionChanged(self):
        if self._isLoading is False:
            value = self._qcbPosition.currentText()
            ReconsParam().setValue(structID='FTAXIS',
                                               paramID='POSITION',
                                               value=value)

    def _positionValueChanged(self):
        if self._isLoading is False:
            ReconsParam().setValue(structID='FTAXIS',
                                               paramID='POSITION_VALUE',
                                               value=self._getPositionValue())

    def _updateHAView(self, b):
        self._qcbPosition.model().findItems(self.EXCENTRATED)[0].setEnabled(b)
        # if excentrated is activated and is not enabled them set accurate as
        # the default value
        if not b and self._qcbPosition.currentText() == self.EXCENTRATED:
            info = 'Unselecting excentrated as the rotation axis, '
            info += 'unvalid for full acquisition'
            logger.warning(info)
            # print will be displayed in Orange window
            index = self._qcbPosition.findText(self.DEFAULT_POS)
            assert(index >= 0)
            self._qcbPosition.setCurrentIndex(index)

    def __buildPlotFigure(self):
        self._qcbPlotFigure = qt.QCheckBox('display image in case of highlow',
                                           parent=self)
        self.linkCheckboxWithH5Variable(self._qcbPlotFigure,
                                        structID='FTAXIS',
                                        h5ParamName='PLOTFIGURE')
        return self._qcbPlotFigure

    def _plotFigureChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='FTAXIS',
                                               paramID='PLOTFIGURE',
                                               value=int(b))

    def __buildHA(self):
        self._qcbHA = qt.QCheckBox('Use all projections to calculate rotation axis',
                                   parent=self)
        self.linkCheckboxWithH5Variable(self._qcbHA,
                                        structID='FTAXIS',
                                        h5ParamName='HA')
        return self._qcbHA

    def _HAChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='FTAXIS',
                                               paramID='HA',
                                               value=int(b))

    def _showPositionValue(self):
        self._qlePositionValue.setVisible(
            self._qcbPosition.currentIndex() in self.indexesAllowingValue)

    def _setOversampling(self, val):
        self._qsbOversampling.setValue(val)

    def _getOversampling(self):
        return self._qsbOversampling.value()

    def _setCORPosition(self, val):
        assert(type(val) in [int, float])
        assert(int(val) in [0, 1])
        if val == 0:
            self._qrbCOR_0_180.setChecked(True)
        else:
            self._qrbCOR_90_270.setChecked(True)

    def _getCORPosition(self):
        return int(not self._qrbCOR_0_180.isChecked())

    def _setPositionValue(self, value):
        self._qlePositionValue.setText(str(float(value)))

    def _getPositionValue(self):
        return float(self._qlePositionValue.text())

    def __buildHalfAcq(self):
        self._qcbHalfAcq = qt.QCheckBox('Half acquisition (HA)',
                                        parent=self)
        self.linkCheckboxWithH5Variable(self._qcbHalfAcq,
                                        structID='FT',
                                        h5ParamName='HALF_ACQ')
        return self._qcbHalfAcq

    def _HALFACQChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='FT',
                                               paramID='HALF_ACQ',
                                               value=int(b))

    def __buildForceHalfAcq(self):
        self._qcbForceHA = qt.QCheckBox('Force HA if rotation is not 360 deg',
                                        parent=self)
        self.linkCheckboxWithH5Variable(self._qcbForceHA,
                                        structID='FT',
                                        h5ParamName='FORCE_HALF_ACQ')
        self._qcbForceHA.setCheckState(qt.Qt.Checked)
        self._qcbForceHA.hide()
        return self._qcbForceHA

    def __HalfAcqStateChanged(self):
        self._qcbForceHA.setVisible(self._qcbHalfAcq.isChecked())

    def _forceHALFACQChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='FT',
                                               paramID='FORCE_HALF_ACQ',
                                               value=int(b))
