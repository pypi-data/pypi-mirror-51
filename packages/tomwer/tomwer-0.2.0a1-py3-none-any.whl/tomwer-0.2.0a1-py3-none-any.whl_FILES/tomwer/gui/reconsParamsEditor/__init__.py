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
__date__ = "09/02/2017"

from silx.gui import qt
from tomwer.gui.H5StructsEditor import H5StructsEditor
from tomwer.core.OctaveH5Editor import OctaveH5Editor
from tomwer.core.ftseries.FastSetupDefineGlobals import FastSetupAll
from tomwer.gui.reconsParamsEditor.BeamGeoWidget import BeamGeoWidget
from tomwer.gui.reconsParamsEditor.DisplayWidget import DisplayWidget
from tomwer.gui.reconsParamsEditor.DKRFWidget import DKRFWidget
from tomwer.gui.reconsParamsEditor.ExpertWidget import ExpertWidget
from tomwer.gui.reconsParamsEditor.FTAxisWidget import FTAxisWidget
from tomwer.gui.reconsParamsEditor.FTWidget import FTWidget
from tomwer.gui.reconsParamsEditor.PaganinWidget import PaganinWidget
from tomwer.gui.reconsParamsEditor.PyHSTWidget import PyHSTWidget
from tomwer.core.ReconsParams import ReconsParam
import logging

logger = logging.getLogger(__name__)


class ReconsParamsEditor(OctaveH5Editor, qt.QTabWidget):
    """
    Build the Widget allowing edition of the fields of the h5 file.

    :param QObject parent: the QObject parent
    """

    def __init__(self, parent=None):
        OctaveH5Editor.__init__(self)
        qt.QTabWidget.__init__(self, parent)
        self.__buildGUI()
        self._isLoading = False

    def __buildGUI(self):
        self._mainWidget = FTWidget(self)
        self.addTab(self._mainWidget, 'Main')

        self._displayWidget = DisplayWidget(self)
        self.addTab(self._displayWidget, 'Display')

        self._axisWidget = FTAxisWidget(self)
        self.addTab(self._axisWidget, 'Axis')

        self._PaganinWidget = PaganinWidget(self)
        self.addTab(self._PaganinWidget, 'Paganin')

        self._PyHSTWidget = PyHSTWidget(self)
        self.addTab(self._PyHSTWidget, 'PyHST')

        self._beamGeoWidget = BeamGeoWidget(self)
        self.addTab(self._beamGeoWidget, 'Geometry')

        self._dkRefWidget = DKRFWidget(self)
        self.addTab(self._dkRefWidget, 'Dark and refs')

        self._expertWidget = ExpertWidget(self)
        self.addTab(self._expertWidget, 'Expert')

        self._otherWidget = OtherWidget(self)
        self.addTab(self._otherWidget, 'Other')

        # TODO : volume selection should also be in axis ???
        self._axisWidget._qcbHalfAcq.toggled.connect(
            self._mainWidget._enableVolumeSelection)

    # implementation of OctaveH5Editor function
    def getStructs(self):
        structs = {}
        for itab in range(self.count()):
            widgetStructs = self.widget(itab).getStructs()
            for structID in widgetStructs:
                if structID not in structs:
                    structs[structID] = {}
                structs[structID].update(widgetStructs[structID])

        return structs

    def loadStructures(self, structures):
        """Load the H5File amd update all the widgets."""
        if self._isLoading is True:
            return
        self._isLoading = True
        OctaveH5Editor.loadStructures(self, structures)
        tabs = (
            self._mainWidget,
            self._displayWidget,
            self._axisWidget,
            self._PaganinWidget,
            self._PyHSTWidget,
            self._beamGeoWidget,
            self._expertWidget,
            self._dkRefWidget
        )

        # load all tabs except 'other tab'
        for tab in tabs:
            tab.load(self.getLoadedStructures())

        self._refreshOther()
        missingStructures = self.__getUnknowH5Params(self.getLoadedStructures())
        if len(missingStructures) > 0:
            self._otherWidget.load(missingStructures)

        self._isLoading = False

    def _refreshOther(self):
        self.removeTab(8)
        self._otherWidget = OtherWidget(self)
        self.addTab(self._otherWidget, 'Other')
        assert(self.widget(8) is self._otherWidget)

    def __getUnknowH5Params(self, structs):
        missing = {}
        for structID in structs:
            for parameter in structs[structID]:
                if not self.isParamH5Managed(structID, parameter):
                    if structID in missing:
                        missing[structID][parameter] = structs[structID][parameter]
                    else:
                        missing[structID] = {parameter: structs[structID][parameter]}

        return missing

    def isParamH5Managed(self, structID, parameter):
        """

        :param str structID: ID of the h5 group
        :param str parameter: name of the parameter

        :return bool: true if one of the tab widget is dealing with the couple
            structID/parameter
        """
        for itab in range(self.count()):
            if self.widget(itab).isParamH5Managed(structID, parameter):
                return True

        return False


class OtherWidget(H5StructsEditor, qt.QScrollArea):
    """
    Group all h5 parameter which doesn't fit to any other widget.

    .. warning: this widget can execute only one load. If multiple load please
                recreate this widget each time.
    """
    def __init__(self, parent=None):
        qt.QScrollArea.__init__(self, parent)
        H5StructsEditor.__init__(self)
        self.setLayout(qt.QVBoxLayout())
        self.widgetsGroup = {}   # create one group per structure
        self.paramType = {}

    def load(self, structures):
        for st in structures:
            assert st not in self.widgetsGroup
            self.widgetsGroup[st] = qt.QGroupBox(title=st, parent=self)
            self.widgetsGroup[st].setLayout(qt.QVBoxLayout())
            # add the group to the main widget
            self.layout().addWidget(self.widgetsGroup[st])
            self.paramToWidget[st] = {}
            self.paramType[st] = {}
            self.structsManaged[st] = []
            for param in structures[st]:
                widget = qt.QWidget(parent=self.widgetsGroup[st])
                widget.setLayout(qt.QHBoxLayout())
                # add the widget ot the group box
                self.widgetsGroup[st].layout().addWidget(widget)

                widget.layout().addWidget(qt.QLabel(param, parent=widget))

                self.paramType[st][param] = type(structures[st][param])
                widgetEditor = qt.QLineEdit(parent=widget,
                                            text=str(structures[st][param]))
                widgetEditor.editingFinished.connect(self._atLeastOneParamChanged)

                self.paramToWidget[st][param] = widgetEditor
                self.structsManaged[st].append(param)
                widget.layout().addWidget(widgetEditor)

        self.spacer = qt.QWidget(self)
        self.spacer.setSizePolicy(qt.QSizePolicy.Minimum,
                                  qt.QSizePolicy.Expanding)
        self.layout().addWidget(self.spacer)

    def getParamValue(self, structID, paramID):
        if not self.isParamH5Managed(structID, paramID):
            return None
        else:
            value = self.paramToWidget[structID][paramID].text()
            return self.paramType[structID][paramID](value)

    # inheritance of H5StructsEditor
    def getStructs(self):
        structs = {}
        for st in self.paramToWidget:
            structs[st] = {}
            for param in self.paramToWidget[st]:
                structs[st][param] = self.getParamValue(st, param)
        return structs

    def _atLeastOneParamChanged(self):
        for st in self.paramToWidget:
            for param in self.paramToWidget[st]:
                value = self.getParamValue(st, param)
                ReconsParam().setValue(structID=st, paramID=param, value=value)


def main():
    import sys
    app = qt.QApplication([])
    if len(sys.argv) == 2:
        reader = FastSetupAll()
        reader.readAll(sys.argv[1], 3.8)
        structures = reader.structures
    else:
        structures = FastSetupAll.getAllDefaultStructures()

    tabs = ReconsParamsEditor()
    tabs.loadStructures(structures)
    tabs.show()

    app.exec_()


if __name__ == "__main__":
    main()
