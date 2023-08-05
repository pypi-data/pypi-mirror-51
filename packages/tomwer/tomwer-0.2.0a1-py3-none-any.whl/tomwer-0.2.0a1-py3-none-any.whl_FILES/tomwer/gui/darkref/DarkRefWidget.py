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
__date__ = "10/01/2018"


import logging
from silx.gui import qt
from tomwer.core.darkref.DarkRefs import DarkRefs
from tomwer.core.ReconsParams import ReconsParam

logger = logging.getLogger(__name__)


class DarkRefWidget(qt.QWidget):
    """
    A simple widget managing the copy of an incoming folder to an other one

    :param parent: the parent widget
    """
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self.mainWidget = DarkRefTab(parent=self)
        self.layout().addWidget(self.mainWidget)

        self._darkRef = self._getDarkRefCoreInstance()

        self.mainWidget.setRemoveOption(self._darkRef.currentParams.rm)
        self.mainWidget.setSkipOption(self._darkRef.currentParams.skipIfExist)
        self.mainWidget.setDarkMode(mode=self._darkRef.currentParams.darkMode)
        self.mainWidget.setRefMode(mode=self._darkRef.currentParams.refMode)
        self.mainWidget.setRefPattern(self._darkRef.currentParams.patternRef)
        self.mainWidget.setDarkPattern(self._darkRef.currentParams.patternDark)

        self.mainWidget.tabGeneral.sigDarkChanged.connect(self._darkRef.setDarkMode)
        self.mainWidget.tabGeneral.sigRefChanged.connect(self._darkRef.setRefMode)
        self.mainWidget.tabGeneral.sigRmToggled.connect(self._darkRef.setRemoveOption)
        self.mainWidget.tabGeneral.sigSkipToggled.connect(
            self._darkRef.setSkipIfExisting)

        self.mainWidget.tabExpert.sigDarkPatternEdited.connect(
            self._darkRef.setPatternDark)
        self.mainWidget.tabExpert.sigRefPatternEdited.connect(
            self._darkRef.setPatternRef)

        self.sigScanReady = self._darkRef.sigScanReady
        self._darkRef.sigUpdated.connect(self._updateReconsParam)

    def process(self, scanID):
        """Overwrite by the some widget like DarkRefCopyWidget we want to
        check if the folder is valid to be take as a reference"""
        return self._darkRef.process(scanID)

    def _updateReconsParam(self):
        self._darkRef.disconnect()
        self._darkRef.reconsParams.blockSignals(True)
        if hasattr(self, 'mainWidget'):
            self.mainWidget.loadStructs(self._darkRef.reconsParams.params)
        self._darkRef.reconsParams.blockSignals(False)
        self._darkRef.connect()

    def _getDarkRefCoreInstance(self):
        return DarkRefs()

    def setForceSync(self, sync):
        self._darkRef.setForceSync(sync)


class DarkRefTab(qt.QTabWidget):
    class WhatCheckBox(qt.QWidget):
        """
        Widget grouping a checkbox and a combobox to know the requested mode
        (None, median, average) for a what (ref, dark)
        """
        sigChanged = qt.Signal(str)
        """Signal emitted when the calculation mode change"""
        def __init__(self, parent, text):
            qt.QWidget.__init__(self, parent)
            self.setLayout(qt.QHBoxLayout())
            self._checkbox = qt.QCheckBox(text=text, parent=self)
            self.layout().addWidget(self._checkbox)
            self._modeCB = qt.QComboBox(parent=self)
            for mode in (DarkRefs.CALC_MEDIAN, DarkRefs.CALC_AVERAGE):
                self._modeCB.addItem(mode)
            self.layout().addWidget(self._modeCB)
            self.layout().setContentsMargins(0, 0, 0, 0)
            self._checkbox.setChecked(True)
            self._checkbox.toggled.connect(self._modeCB.setEnabled)
            self._checkbox.toggled.connect(self._modeChange)
            self._modeCB.currentIndexChanged.connect(self._modeChange)
            self._updateReconsParam = True
            """Boolean used to know if we have to apply modifications on
            the ReconsParam() (in the case user made modification)
            or not (in the case we are simply reading structure and to avoid
            looping in signals with other QObject)"""

        def getMode(self):
            if self._checkbox.isChecked() is True:
                return self._modeCB.currentText()
            else:
                return DarkRefs.CALC_NONE

        def _modeChange(self, *a, **b):
            self.sigChanged.emit(self.getMode())

        def setMode(self, mode):
            assert mode in DarkRefs.CALC_MODS
            self._checkbox.toggled.disconnect(self._modeChange)
            self._modeCB.currentIndexChanged.disconnect(self._modeChange)
            self._checkbox.setChecked(mode not in (DarkRefs.CALC_NONE, None))
            if mode not in (DarkRefs.CALC_NONE, None):
                index = self._modeCB.findText(mode)
                if index < 0:
                    logger.error('index for %s is not recognized' % mode)
                else:
                    self._modeCB.setCurrentIndex(index)
            self._checkbox.toggled.connect(self._modeChange)
            self._modeCB.currentIndexChanged.connect(self._modeChange)
            self.sigChanged.emit(self.getMode())


    class TabGeneral(qt.QWidget):
        """Widget with the general information for dark and ref process"""
        def __init__(self, parent):
            qt.QWidget.__init__(self, parent)
            self.setLayout(qt.QVBoxLayout())

            self._grpWhat = qt.QGroupBox('what', parent=self)
            self._grpWhat.setLayout(qt.QVBoxLayout())
            self._darkWCB = DarkRefTab.WhatCheckBox(parent=self._grpWhat,
                                                    text='dark')
            self._refWCB = DarkRefTab.WhatCheckBox(parent=self._grpWhat,
                                                   text='ref')
            self._grpWhat.layout().addWidget(self._darkWCB)
            self.sigDarkChanged = self._darkWCB.sigChanged
            self._grpWhat.layout().addWidget(self._refWCB)
            self.sigRefChanged = self._refWCB.sigChanged
            self.layout().addWidget(self._grpWhat)

            self._grpOptions = qt.QGroupBox('options', parent=self)
            self._grpOptions.setLayout(qt.QVBoxLayout())
            self._rmOptionCB = qt.QCheckBox(parent=self._grpOptions,
                                            text='remove raw files when done')
            self.sigRmToggled = self._rmOptionCB.toggled
            self._skipOptionCB = qt.QCheckBox(parent=self._grpOptions,
                                              text='skip if already existing')
            self.sigSkipToggled = self._skipOptionCB.toggled
            self._grpOptions.layout().addWidget(self._rmOptionCB)
            self._grpOptions.layout().addWidget(self._skipOptionCB)
            self.layout().addWidget(self._grpOptions)

            spacer = qt.QWidget(parent=self)
            spacer.setSizePolicy(qt.QSizePolicy.Minimum,
                                 qt.QSizePolicy.Expanding)

            self.layout().addWidget(spacer)


    class TabExpert(qt.QWidget):
        """Expert process for dark and ref"""

        def __init__(self, parent):
            qt.QWidget.__init__(self, parent)
            self.setLayout(qt.QVBoxLayout())

            self._patternsWidget = qt.QWidget(parent=self)
            self._patternsWidget.setLayout(qt.QGridLayout())

            self._patternsWidget.layout().addWidget(qt.QLabel('dark file pattern',
                                                    parent=self._patternsWidget),
                                                    0,
                                                    0)
            self._darkLE = qt.QLineEdit(parent=self._patternsWidget)
            self._darkLE.setToolTip(DarkRefs.getDarkPatternTooltip())
            self.sigDarkPatternEdited = self._darkLE.editingFinished
            self._patternsWidget.layout().addWidget(self._darkLE, 0, 1)
            self._patternsWidget.layout().addWidget(qt.QLabel('ref file pattern',
                                                    parent=self._patternsWidget),
                                                    1,
                                                    0)
            self._refLE = qt.QLineEdit(parent=self._patternsWidget)
            self._refLE.setToolTip(DarkRefs.getRefPatternTooltip())
            self.sigRefPatternEdited = self._refLE.editingFinished
            self._patternsWidget.layout().addWidget(self._refLE, 1, 1)

            self.layout().addWidget(self._patternsWidget)

            textExtraInfo = "note: to have more information about pattern usage \n" \
                            "see tooltips over dark and flat field patterns." \
                            "\nYou can also see help to have advance" \
                            "information"
            labelNote = qt.QLabel(parent=self, text=textExtraInfo)
            labelNote.setSizePolicy(qt.QSizePolicy.Preferred,
                                    qt.QSizePolicy.Minimum)
            self.layout().addWidget(labelNote)

            spacer = qt.QWidget(parent=self)
            spacer.setSizePolicy(qt.QSizePolicy.Minimum,
                                 qt.QSizePolicy.Expanding)

            self.layout().addWidget(spacer)

    def __init__(self, parent):
        self.reconsParams = ReconsParam()
        self._updateReconsParam = False
        qt.QTabWidget.__init__(self, parent)
        self.tabGeneral = DarkRefTab.TabGeneral(parent=self)
        self.addTab(self.tabGeneral, 'general')
        self.tabExpert = DarkRefTab.TabExpert(parent=self)
        self.addTab(self.tabExpert, 'expert')

        self._makeConnection()

    def _makeConnection(self):
        self.tabGeneral._refWCB.sigChanged.connect(self._refCalcModeChanged)
        self.tabGeneral._darkWCB.sigChanged.connect(self._darkCalcModeChanged)
        self.tabGeneral._rmOptionCB.toggled.connect(self._rmOptChanged)
        self.tabGeneral._skipOptionCB.toggled.connect(self._skipOptChanged)
        self.tabExpert._darkLE.editingFinished.connect(self._darkPatternChanged)
        self.tabExpert._refLE.editingFinished.connect(self._refPatternChanged)

    def loadStructs(self, structs):
        def warningKeyNotHere(key):
            logger.warning('%s key not present in the given struct, '
                           'cannot load value for it.' % ket)

        self._updateReconsParam = False
        assert isinstance(structs, dict)
        if 'DKRF' not in structs:
            logger.warning('failed to load DarkRefWidget no DKRF structure')
            return

        dkrfStruct = structs['DKRF']
        if 'DARKCAL' not in dkrfStruct:
            warningKeyNotHere('DARKCAL')
        else:
            self.setDarkMode(dkrfStruct['DARKCAL'])

        if 'REFSCAL' not in dkrfStruct:
            warningKeyNotHere('REFSCAL')
        else:
            self.setRefMode(dkrfStruct['REFSCAL'])

        if 'REFSOVE' not in dkrfStruct:
            warningKeyNotHere('REFSOVE')
        else:
            self.setSkipOption(not dkrfStruct['REFSOVE'])

        if 'REFSRMV' not in dkrfStruct:
            warningKeyNotHere('REFSRMV')
        else:
            self.setRemoveOption(dkrfStruct['REFSRMV'])

        if 'RFFILE' not in dkrfStruct:
            warningKeyNotHere('RFFILE')
        else:
            self.setRefPattern(dkrfStruct['RFFILE'])

        if 'DKFILE' not in dkrfStruct:
            warningKeyNotHere('DKFILE')
        else:
            self.setDarkPattern(dkrfStruct['DKFILE'])

        self._updateReconsParam = True

    def setRemoveOption(self, rm):
        self.tabGeneral._rmOptionCB.setChecked(rm)

    def setSkipOption(self, skip):
        self.tabGeneral._skipOptionCB.setChecked(skip)

    def setDarkMode(self, mode):
        self.tabGeneral._darkWCB.setMode(mode)

    def setRefMode(self, mode):
        self.tabGeneral._refWCB.setMode(mode)

    def setRefPattern(self, pattern):
        self.tabExpert._refLE.setText(pattern)

    def setDarkPattern(self, pattern):
        self.tabExpert._darkLE.setText(pattern)

    def _rmOptChanged(self):
        if self._updateReconsParam is True:
            # The interface control both REFSRMV and DARKRMV
            value = int(self.tabGeneral._rmOptionCB.isChecked())
            self.reconsParams.setValue(structID='DKRF',
                                       paramID='REFSRMV',
                                       value=value)
            self.reconsParams.setValue(structID='DKRF',
                                       paramID='DARKRMV',
                                       value=value)

    def _skipOptChanged(self):
        if self._updateReconsParam is True:
            # The interface control both REFSRMV and DARKRMV
            value = int(not self.tabGeneral._skipOptionCB.isChecked())
            self.reconsParams.setValue(structID='DKRF',
                                       paramID='REFSOVE',
                                       value=value)
            self.reconsParams.setValue(structID='DKRF',
                                       paramID='DARKOVE',
                                       value=value)

    def _refPatternChanged(self):
        if self._updateReconsParam is True:
            value = self.tabExpert._refLE.text()
            self.reconsParams.setValue(structID='DKRF',
                                       paramID='RFFILE',
                                       value=value)

    def _darkPatternChanged(self):
        if self._updateReconsParam is True:
            value = self.tabExpert._darkLE.text()
            self.reconsParams.setValue(structID='DKRF',
                                       paramID='DKFILE',
                                       value=value)

    def _darkCalcModeChanged(self):
        if self._updateReconsParam is True:
            value = self.tabGeneral._darkWCB.getMode()
            self.reconsParams.setValue(structID='DKRF',
                                       paramID='DARKCAL',
                                       value=value)

    def _refCalcModeChanged(self):
        if self._updateReconsParam is True:
            value = self.tabGeneral._refWCB.getMode()
            self.reconsParams.setValue(structID='DKRF',
                                       paramID='REFSCAL',
                                       value=value)
