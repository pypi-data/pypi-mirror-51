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
from tomwer.web.client import OWClient
from tomwer.core.utils import logconfig

logger = logging.getLogger("TomoGUIreconsWidget")

try:
    from silx.gui import qt
except ImportError as e:
    logger.error("Module %s requires silx", __name__)
    raise e

try:
    from tomoGUI.gui.QFreeARTReconstructionManager import QFreeARTReconstructionManager
except ImportError as e:
    logger.info("Module %s requires tomoGUI", __name__)
    QFreeARTReconstructionManager = None

if QFreeARTReconstructionManager is not None:

    class TomoGUIreconsWidget(widget.OWWidget, OWClient):
        name = "tomoGUI reconstruction"
        id = "orange.widgets.tomwer.tomoGUIrecons"
        description = "Interface to create a compatible file for freeart"
        icon = "icons/tomogui.png"
        priority = 98
        category = "esrfWidgets"
        keywords = ["freeart", "tomoGUI", "fluorescence", "reconstruction", "tomwer"]

        inputs = [("freeartConfigurationFile", str, "setCfgFile")]
        # TODO : outputs : list of reconstructed phantom, with IDs ?
        outputs = [widget.OutputSignal(
            "reconstructions", dict,
            doc="list of all reconstructed phantom")]

        want_main_area = True
        resizing_enabled = True
        compress_signal = False

        def getWidgetForInvalidConf(self):
            return qt.QLabel("unable to treat the given configuration file")

        def __init__(self,  parent=None):
            """Constructor"""
            widget.OWWidget.__init__(self, parent)
            OWClient.__init__(self, logger)

            # self.setFixedWidth(500)
            # self.setFixedHeight(800)

            self.__freeartWidget = None
            self.__info = self.getWidgetForInvalidConf()

            layout = qt.QVBoxLayout()
            layout.addWidget(self.__info)
            layout.addWidget(self.__freeartWidget)
            self.setLayout(layout)

        def setCfgFile(self, cfgFile):
            """Set the configuration file to the QFreeARTWidget
            """
            try:
                self.__freeartWidget = QFreeARTReconstructionManager(self, cfgFile)
                self.__info.hide()
                layout = qt.QVBoxLayout()
                layout.addWidget(self.__info)
                layout.addWidget(self.__freeartWidget)
                self.__freeartWidget.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)

                # here : strange behavior if no size defined !!!
                self.__freeartWidget.setFixedWidth(1200)
                self.__freeartWidget.setFixedHeight(1200)
                self.setFixedWidth(1200)
                self.setFixedHeight(1200)

                self.setLayout(layout)

                # TODO : avoid creation each time and set None as a valid value ??? => difficult for the reconstruction
                self.__freeartWidget.show()
                self.__freeartWidget._rightMenu._qpbQuit.hide()
                self.__freeartWidget.sigReconstructionEnded.connect(self.reconstructionEnded)

            except (RuntimeError, ValueError):
                # TODO henri : que faire si le sinogram a des valeurs negatives ?
                self.__freeartWidget = None
                self.__info.show()
                mess = 'The given cfg file %s is not runnable by freeart recons' % cfgFile
                _logger.warning(mess,
                                extra={logconfig.DOC_TITLE: self._scheme_title})

        def reconstructionEnded(self):
            assert(self.__freeartWidget is not None)
            assert(self.__freeartWidget.freeartInterpreter is not None)

            reconstructions = {}
            algos = self.__freeartWidget.freeartInterpreter.getReconstructionAlgorithms()
            for algo in algos:
                reconstructions[algo] = algos[algo].getPhantom()

            self.send("reconstructions", reconstructions)
