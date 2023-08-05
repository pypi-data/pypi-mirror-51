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
__date__ = "25/10/2016"

from Orange.widgets import widget
import logging
from silx.gui import qt
from tomwer.web.client import OWClient

logger = logging.getLogger("TomoGUIprojectWidget")

try:
    from tomoGUI.gui.QFreeARTWidget import QFreeARTWidget
except ImportError as e:
    logger.info("Module %s requires tomoGUI", __name__)
    QFreeARTWidget = None

if QFreeARTWidget is not None:

    class TomoGUIprojectWidget(widget.OWWidget, OWClient):
        name = "tomoGUI project"
        id = "orange.widgets.tomwer.tomoGUIproject"
        description = "Interface to create a compatible file for freeart"
        icon = "icons/tomogui.png"
        priority = 99
        category = "esrfWidgets"
        keywords = ["freeart", "tomoGUI", "fluorescence", "reconstruction", "tomwer"]

        inputs = []
        outputs = [widget.OutputSignal(
            "freeartConfigurationFile", str,
            doc="path of the freeart interpretable file")]

        # TODO : give a phantom file for orange ? => no backup

        want_main_area = True
        resizing_enabled = True
        compress_signal = False

        def __init__(self,  parent=None):
            """Constructor"""
            widget.OWWidget.__init__(self, parent)
            OWClient.__init__(self, logger)
            self.__freeartWidget = QFreeARTWidget(parent)

            layout = qt.QVBoxLayout()
            layout.addWidget(self.__freeartWidget)
            self.setLayout(layout)

            # hide the 'run reconstruction button'
            self.__freeartWidget._qbReconstruct.hide()
            spacer = qt.QWidget()
            spacer.setSizePolicy(qt.QSizePolicy.Expanding,
                                 qt.QSizePolicy.Minimum)
            self._okButton = qt.QPushButton("ok")
            lWidget = qt.QWidget(self)
            layoutH = qt.QHBoxLayout()
            layoutH.addWidget(spacer)
            layoutH.addWidget(self._okButton)
            lWidget.setLayout(layoutH)
            layout.addWidget(lWidget)

            self._okButton.clicked.connect(self.validated)
            self._okButton.clicked.connect(self.hide)

        def leaveEvent(self, _):
            pass

        def validated(self):
            import tempfile
            outFile = tempfile.mkstemp(suffix=".cfg")

            try:
                self.__freeartWidget.saveConfiguration(outFile[1])
                self.send("freeartConfigurationFile", outFile[1])
            except RuntimeError:
                _logger.warning("The given configuration file is not valid",
                                extra={
                                    logconfig.DOC_TITLE: self._scheme_title})
            # if no file setted : create a temporary file and send it 

            # if one setted : just save on it
            # callback when the user press validate on the gui
            # TODO : check all values are valid
            # TODO : si on y laisse ainsi alors il faut rajouter une box pour sauvegerder la configuration a une adresse pour conserver un backup du fichier d econfiguration
