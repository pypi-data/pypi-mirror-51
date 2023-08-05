# /*##########################################################################
# Copyright (C) 2017 European Synchrotron Radiation Facility
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
"""Some widget construction to check if a sample moved"""

__author__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "19/03/2018"

from silx.gui import qt
from silx.gui.plot import Plot2D
from silx.gui.plot.Colormap import Colormap
from collections import OrderedDict
from tomwer.gui.samplemoved.SelectionTable import AngleSelectionTable, IntAngle
import numpy
import fabio
import os
import logging

_logger = logging.getLogger(__file__)


class SampleMovedWidget(qt.QMainWindow):
    """
    Widget used to display two images with different color channel.
    The goal is to see if the sample has moved during acquisition.
    """
    CONFIGURATIONS = OrderedDict([
        ('0-0(1)', ('0', '0(1)')),
        ('90-90(1)', ('90', '90(1)')),
        ('180-180(1)', ('180', '180(1)')),
        ('270-270(1)', ('270', '270(1)')),
        ('360-0', ('360', '0'))
    ])

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self._isConnected = False
        self._images = {}
        self._symmetricalStates = {'first': False, 'second': False}
        self._plot = Plot2D(parent=self)
        self._plot.getColormapAction().setVisible(False)
        self._plot.getColorBarWidget().setVisible(False)
        self._plot.getProfileToolbar().setVisible(False)
        self._plot.setAxesDisplayed(False)
        self._plot.setKeepDataAspectRatio(True)
        self._plot.getYAxis().setInverted(True)

        self._topWidget = self.getControlWidget()

        # make sure the two plot will have the same colormap object
        self._colormap = Colormap()

        self._dockWidgetMenu = qt.QDockWidget(parent=self)
        self._dockWidgetMenu.layout().setContentsMargins(0, 0, 0, 0)
        self._dockWidgetMenu.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._dockWidgetMenu.setWidget(self._topWidget)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self._dockWidgetMenu)

        self._plotsWidget = qt.QWidget(parent=self)
        self._plotsWidget.setLayout(qt.QHBoxLayout())

        self._plotsWidget.layout().addWidget(self._plot)
        self.setCentralWidget(self._plotsWidget)

        if hasattr(self._selectorCB, 'currentTextChanged'):
            self._selectorCB.currentTextChanged.connect(self.setConfiguration)
        else:
            self._selectorCB.currentIndexChanged['QString'].connect(
                self.setConfiguration)

        self._selectionTable.sigSelectionChanged.connect(self._setConfigManual)

    def getControlWidget(self):
        if hasattr(self, '_topWidget'):
            return self._topWidget
        self._topWidget = qt.QWidget(parent=self)

        self._configWidget = qt.QWidget(parent=self._topWidget)
        self._configWidget.setLayout(qt.QHBoxLayout())

        self._configWidget.layout().addWidget(qt.QLabel('Configuration:',
                                                         parent=self._topWidget))
        self._selectorCB = qt.QComboBox(parent=self._topWidget)
        self._configWidget.layout().addWidget(self._selectorCB)

        self._selectionTable = AngleSelectionTable(parent=self._topWidget)
        self._topWidget.setLayout(qt.QVBoxLayout())
        self._topWidget.layout().setContentsMargins(0, 0, 0, 0)

        self._topWidget.layout().addWidget(self._configWidget)
        self._topWidget.layout().addWidget(self._selectionTable)

        self._selectionTable.sigSelectionChanged.connect(self._updatePlot)
        return self._topWidget

    def clear(self):
        self._plot.clear()
        self._selectorCB.clear()
        self._selectionTable.clear()
        self._images = {}

    def setImages(self, images):
        """
        Set the images in a key value system. Key should be in
        (0, 90, 180, 270) and the value should be the image.

        images value can be str (path to the file) or data
        :param dict images: images to set. key is index or file name, value
                            the image.
        """
        self.clear()
        self._images = images

        # update the default config
        self._selectorCB.clear()

        self._selectorCB.blockSignals(True)
        for config in self.CONFIGURATIONS:
            addConfig = True
            for elemt in self.CONFIGURATIONS[config]:
                if elemt not in images:
                    addConfig = False
                    break
            if addConfig is True:
                self._selectorCB.addItem(config)
        self._selectorCB.addItem('manual')

        # convert it back to into to order correctly the keys
        keys = []
        [keys.append(IntAngle(key)) for key in list(images.keys())]
        keys.sort()
        [self._selectionTable.addRadio(key) for key in keys]
        self._selectorCB.setCurrentIndex(0)
        self._selectorCB.blockSignals(False)
        if hasattr(self._selectorCB, 'currentTextChanged'):
            self._selectorCB.currentTextChanged.emit(self._selectorCB.currentText())
        else:
            self._selectorCB.currentIndexChanged['QString'].emit(
                self._selectorCB.currentText())
        self._plot.resetZoom()

    def _updatePlot(self):
        def loadData(key):
            if key not in self._images:
                _logger.warning(
                    "Can't set configuration. %s hasn't be set." % key)

            if type(self._images[key]) is str:
                path = self._images[key]
                assert os.path.isfile(path)
                self._images[key] = fabio.open(self._images[key]).data
            return self._images[key]

        def applyColorFilter(data, channels):
            if 'R' not in channels:
                data[:, :, 0] = numpy.zeros((data.shape[0], data.shape[1]))
            if 'G' not in channels:
                data[:, :, 1] = numpy.zeros((data.shape[0], data.shape[1]))
            if 'B' not in channels:
                data[:, :, 2] = numpy.zeros((data.shape[0], data.shape[1]))
            return data

        selection = self._selectionTable.getSelection()
        globalRGBImg = None
        for name in selection:
            img = loadData(name)
            if globalRGBImg is None:
                globalRGBImg = numpy.zeros((img.shape[0], img.shape[1], 3),
                                           dtype=numpy.uint8)
            rgb = numpy.zeros((img.shape[0], img.shape[1], 3),
                              dtype=numpy.uint8)
            rgb[:, :, 0] = img / img.max() * 255.
            rgb[:, :, 1] = img / img.max() * 255.
            rgb[:, :, 2] = img / img.max() * 255.

            rgb = applyColorFilter(rgb, selection[name])
            globalRGBImg = globalRGBImg + rgb

        self._plot.clear()
        if globalRGBImg is not None:
            self._plot.addImage(data=globalRGBImg, replace=False,
                                colormap=self._colormap, legend=name,
                                resetzoom=False)

    def setConfiguration(self, config):
        if config == 'manual':
            return
        if config not in self.CONFIGURATIONS:
            _logger.warning('Undefined configuration: %s' % config)
            return
        selection = {
            self.CONFIGURATIONS[config][0]: 'R',
            self.CONFIGURATIONS[config][1]: 'G',
        }
        self._selectionTable.blockSignals(True)
        self._selectionTable.setSelection(selection)
        self._updatePlot()
        self._selectionTable.blockSignals(False)

    def _setConfigManual(self):
        indexItemManual = self._selectorCB.findText('manual')
        if indexItemManual >= 0:
            self._selectorCB.setCurrentIndex(indexItemManual)
