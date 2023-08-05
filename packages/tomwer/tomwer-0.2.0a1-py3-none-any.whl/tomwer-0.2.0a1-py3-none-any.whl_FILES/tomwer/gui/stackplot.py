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

__author__ = ["P. Paleo", "H. Payno"]
__license__ = "MIT"
__date__ = "24/05/2016"

from silx.gui import qt
from silx.gui.plot import Plot2D
import numpy
import os
from collections import OrderedDict
from orangecontrib.tomwer.widgets import icons
from tomwer.core.ImageLoaderThread import ImageLoaderThread
from tomwer.core.utils import ftseriesutils
import functools
import logging

logger = logging.getLogger(__name__)


class _QImageStackPlot(qt.QWidget):
    """
    Widget to display a stack of image

    :param parent: the Qt parent widget
    """
    _sizeHint = qt.QSize(400, 400)

    IMG_NOT_FOUND = numpy.load(icons.getResource('imageNotFound.npy'))

    def __init__(self, parent, withQSlider=True, sliderVertical=False):
        qt.QWidget.__init__(self, parent)
        layout = qt.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        mainwidget = qt.QWidget(self)
        mainLayout = qt.QHBoxLayout() if sliderVertical else qt.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainwidget.setLayout(mainLayout)
        layout.addWidget(mainwidget)

        self._plot = Plot2D(self)
        if hasattr(self._plot, "setAxesDisplayed"):
            # by default we want to have a full screen display
            self._plot.setAxesDisplayed(False)

        colormap = self._plot.getDefaultColormap()
        if(type(colormap) is dict):
            colormap['autoscale'] = True
        else:
            assert(hasattr(colormap, 'setVRange'))
            colormap.setVRange(None, None)
        self._plot.setDefaultColormap(colormap)
        self._plot.setKeepDataAspectRatio(True)

        # removing some plot action to clear toolbar
        self._plot.getMaskAction().setVisible(False)
        self._plot.getCopyAction().setVisible(False)
        # if has the option medianFilter, active it
        if hasattr(self._plot, 'getMedianFilter2DAction'):
            self._plot.getMedianFilter2DAction().setVisible(True)

        mainLayout.addWidget(self._plot)

        if withQSlider:
            if sliderVertical is True:
                lLayout = qt.QVBoxLayout()
            else:
                lLayout = qt.QHBoxLayout()

            self._controlWidget = qt.QWidget(self)
            self._controlWidget.setLayout(lLayout)
            lLayout.setContentsMargins(0, 0, 0, 0)
            mainLayout.addWidget(self._controlWidget)

            self._qspinbox = qt.QSpinBox(parent=self._controlWidget)
            self._qspinbox.valueChanged.connect(self.showImage)
            self._qslider = qt.QSlider(
                qt.Qt.Vertical if sliderVertical is True else qt.Qt.Horizontal,
                parent=self._controlWidget)
            self.setRange(0, 0)
            self._qslider.setTickPosition(0)
            self._qslider.valueChanged.connect(self.showImage)
            if sliderVertical:
                lLayout.addWidget(self._qspinbox)
                lLayout.addWidget(self._qslider)
            else:
                lLayout.addWidget(self._qslider)
                lLayout.addWidget(self._qspinbox)

        else:
            self._qslider = None

        self.setLayout(layout)

        self.setImages(None)
        self.getActiveImage = self._plot.getActiveImage

    def sizeHint(self):
        """Return a reasonable default size for usage in :class:`PlotWindow`"""
        return self._sizeHint

    def setImages(self, images):
        """
        Set the images to display
        """
        if images is None:
            self. images = OrderedDict()
            self._plot.clear()
            if self._qslider:
                self._qslider.setRange(0, 0)
                self._qspinbox.setRange(0, 0)
            return
        else:
            self.images = OrderedDict(sorted(images.items(),
                                             key=lambda t: t[0]))
            if len(self.images) > 0:
                self.showImage(0)

            if self._qslider:
                if len(self.images) > 0:
                    self.setRange(min(self.images.keys()),
                                  max(self.images.keys()))
                else:
                    self.setRange(0, 0)

    def showImage(self, index):
        """
        Show the image of index 'index' as the current image displayed

        :param int index: the index of the image to display.
        """
        # update gui
        self._qspinbox.setValue(index)
        self._qslider.setValue(index)
        if (self.images is not None) and (index in self.images.keys()):
            self._plot.addImage(data=self.images[index],
                                legend=str(index),
                                replace=True)
            self._updatefileName()
        else:
            logger.info(
                "image not found, can't display it. Maybe data have been moved ?")
            self._plot.addImage(data=_QImageStackPlot.IMG_NOT_FOUND,
                                legend='Not found',
                                replace=True)

    def setImage(self, index, data):
        """
        Set the given data as the image for the given index

        :param int index: the index of the image to set
        :param numpy.ndarray data: the image
        """
        _data = data
        if data is None:
            _data = self.IMG_NOT_FOUND
        self.images[index] = _data

    def isEmpty(self):
        """

        :return bool: True if no reconstruction has been set yet
        """
        return (self.images is None or len(self.images) == 0)

    def clear(self):
        self.setImages(None)

    def setRange(self, _min, _max):
        """Set the range of the spin box

        :param _min: the minimal value of the slice. If equal None, not set
        :param _max: the maximal value of the slice. If equal None, not set
        """
        self._qslider.setRange(_min, _max)
        self._qspinbox.setRange(_min, _max)

    def getControlWidget(self):
        return self._controlWidget


class _QImageFileStackPlot(_QImageStackPlot):
    """
    Widget based on QImageStackPlot but managing images from a stack of path to
    file
    """

    IMG_LOADING = numpy.load(icons.getResource('hourglass.npy'))

    loadingStatus = {'loading': 0, 'loaded': 1, 'notLoaded': 2}

    def __init__(self, parent):
        """
        Constructor
        :param parent: the Qt parent widget
        """
        _QImageStackPlot.__init__(self, parent, withQSlider=True)

        self._lazyLoadingForImg = True
        self._lazyLoadingCB = qt.QCheckBox('Lazy loading',
                                           parent=self._controlWidget)
        self._lazyLoadingCB.setToolTip('If active will load image only '
                                       'when the slider is released or '
                                       'when the spinBox edition is '
                                       'finished')
        self._lazyLoadingCB.setChecked(True)
        self.getControlWidget().layout().addWidget(self._lazyLoadingCB)
        self._lazyLoadingCB.toggled.connect(self.setLazyLoading)
        self.addFolderName(False)
        self.launchedThread = {}
        self.clear()

        # connect the qslider with the GUI
        self._sliderConnected = False

        style = qt.QApplication.style()
        self.waitingIcon = style.standardIcon(qt.QStyle.SP_BrowserReload)

        # add some toolbar information
        self._qslider.setToolTip('The loading of the image will start when the \
            slider will be released')
        self._qspinbox.setToolTip('To start the loading press enter on the spin\
             box or release the slider')

        self.layout().addWidget(self.__buildFileInfo())

        self._qslider.valueChanged.connect(self._updatefileName)

        self._connectControl()

    def __buildFileInfo(self):
        self._fileInfoWidget = qt.QWidget(parent=self)
        layout = qt.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._fileInfoWidget.setLayout(layout)

        layout.addWidget(qt.QLabel('file :', self._fileInfoWidget))
        self._qlFileName = qt.QLabel('', parent=self._fileInfoWidget)
        layout.addWidget(self._qlFileName)

        return self._fileInfoWidget

    def __del__(self):
        self._getBackAllThread()

    def _getBackAllThread(self):
        for lThread in self.launchedThread:
            self.launchedThread[lThread].wait()

    def setLazyLoading(self, val):
        if self._lazyLoadingForImg != val:
            self._disconnectControl()
            self._lazyLoadingForImg = val
            self._connectControl()

    def _disconnectControl(self):
        if self._lazyLoadingForImg is True:
            self._qslider.sliderReleased.disconnect(self.updateActiveImage)
            self._qspinbox.editingFinished.disconnect(self.updateActiveImage)
        else:
            self._qslider.valueChanged.disconnect(self.updateActiveImage)
            self._qspinbox.valueChanged.disconnect(self.updateActiveImage)

    def _connectControl(self):
        if self._lazyLoadingForImg is True:
            self._qslider.sliderReleased.connect(self.updateActiveImage)
            self._qspinbox.editingFinished.connect(self.updateActiveImage)
        else:
            self._qslider.valueChanged.connect(self.updateActiveImage)
            self._qspinbox.valueChanged.connect(self.updateActiveImage)

    def clear(self):
        self._getBackAllThread()
        self._indexToFile = {}
        self._loadingStatus = {}
        for fileID, thread in self.launchedThread.items():
            if thread.isRunning():
                thread.quit()
            del thread
        self.launchedThread = {}
        super(_QImageFileStackPlot, self).clear()

    def setLoadingImage(self, sliceNb):
        """Set the status of the image to not loaded
        """
        self._loadingStatus[sliceNb] = self.loadingStatus['notLoaded']
        self.setImage(sliceNb, _QImageFileStackPlot.IMG_LOADING)

    def setImageFiles(self, imagesFiles):
        """
        Set the stack of images files

        :param _imagesFiles: the list of images path to be displayed
        """
        def dealWithVolFiles(_imagesFiles):
            volFiles = []
            if type(_imagesFiles) in (list, tuple):
                for _file in _imagesFiles:
                    if _file.endswith('.vol'):
                        volFiles.append(_file)
            elif type(_imagesFiles) is dict:
                for key, _file in _imagesFiles.items():
                    if _file.endswith('.vol'):
                        volFiles.append(_file)
            else:
                err = "imagesFiles type (%s) can't be manage" % type(
                    _imagesFiles)
                raise ValueError(err)

            if len(volFiles) > 0 and type(_imagesFiles) is dict:
                logger.debug('converting imageFiles from dict to list. Will '
                             'loose slice incides')
                _imagesFiles = OrderedDict(sorted(_imagesFiles.items(),
                                                 key=lambda t: t[0]))

                _imagesFiles = list(set(_imagesFiles.values()))

            for volFile in volFiles:
                del _imagesFiles[_imagesFiles.index(volFile)]

            for volFile in volFiles:
                volInfoFile = volFile.replace('.vol', '.vol.info')
                if not os.path.exists(volInfoFile):
                    mess = "Can't find description file %s associated with raw " \
                           "data file %s " % (volInfoFile, volFile)
                    logger.warning(mess)
                else:
                    shape = ftseriesutils._getShapeForVolFile(volInfoFile)
                    if shape is not None:
                        for zSlice in range(shape[0]):
                            _imagesFiles.append(volFile + '#z=' + str(zSlice))

            return _imagesFiles


        if imagesFiles is None or len(imagesFiles) == 0:
            return

        self._qslider.blockSignals(True)
        self._qspinbox.blockSignals(True)

        self.clear()

        _imagesFiles = imagesFiles
        # for now and for .vol file we are creating one file per z
        _imagesFiles = dealWithVolFiles(_imagesFiles)

        if self._sliderConnected:
            self._disconnectControl()

        if type(_imagesFiles) in (list, tuple):
            self.setRange(0, len(_imagesFiles) - 1)
            for iFile, filePath in enumerate(_imagesFiles):
                self._indexToFile[iFile] = filePath
                self.setLoadingImage(iFile)
        elif type(_imagesFiles) is dict:
            self.setRange(min(_imagesFiles.keys()), max(_imagesFiles.keys()))
            self._indexToFile = _imagesFiles.copy()
            for iFile in _imagesFiles.keys():
                self.setLoadingImage(iFile)
        else:
            err = "imagesFiles type (%s) can't be manage" % type(_imagesFiles)
            raise ValueError(err)

        self.updateActiveImage()

        self._qslider.blockSignals(False)
        self._qspinbox.blockSignals(False)

    def updateActiveImage(self, *args, **kw):
        """
        Launch a request to update the image for the given slice index
        """
        indexFile = self._qslider.value()

        if len(self._loadingStatus) == 0 or indexFile not in self._loadingStatus:
            return

        if self._loadingStatus[indexFile] == self.loadingStatus['notLoaded']:
            assert(indexFile in self._indexToFile)
            fileToLoad = self._indexToFile[indexFile]

            if fileToLoad in self.launchedThread:
                logger.info('A thread has already been launched for the file \
                    %s. Not launching an other one' % fileToLoad)
                return
            loaderThread = ImageLoaderThread(index=indexFile,
                                             filePath=fileToLoad)
            self.launchedThread[fileToLoad] = loaderThread

            callback = functools.partial(self._setImage, indexFile, fileToLoad,
                                         loaderThread.getData)
            loaderThread.finished.connect(callback)
            self._loadingStatus[indexFile] = self.loadingStatus['loading']
            loaderThread.start()

    def _setImage(self, sliceIndex, imageName, dataGetter, check=False):
        """
        Set the given image to the given slice

        :param int sliceIndex: the index of the slice. Fit with the slider
        :param imageName: the path of the file loaded
        :param fct pointer dataGetter: function to retrieve the data loaded
        :param check: if a filePath already exists for the sliceIndex and
            if the names of the file are different, won't do the set.
        """
        def setVolume(volumeName, volume):
            fileToIndex = self._getFileToIndexDict()
            for z in range(volume.shape[0]):
                _zImageName = volumeName + '#z=' + str(z)
                if _zImageName not in fileToIndex:
                    logger.warning('%s has been removed from stackplot' % _zImageName)
                    return
                index = fileToIndex[_zImageName]
                self._indexToFile[index] = _zImageName
                self.setImage(index, data[z])
                self._loadingStatus[index] = self.loadingStatus['loaded']

        data = dataGetter()
        # if a thread has been launch : remove if
        if imageName in self.launchedThread:
            del self.launchedThread[imageName]

        if check is True and sliceIndex in self._indexToFile and \
                        self._indexToFile[sliceIndex] != imageName:
            info = "Can't set image %s for slice %s because setted" \
                   "image path for this slice is different" % (imageName, sliceIndex)
            logger.debug(info)
            return

        if data is not None and '#z=' in imageName:
            # in the case of a vol file we are directly loading several image
            assert data.ndim is 3
            volumeName = imageName.split('#z=')[0]
            setVolume(volumeName, volume=data)
        else:
            self._indexToFile[sliceIndex] = imageName
            self.setImage(sliceIndex, data)
            self._loadingStatus[sliceIndex] = self.loadingStatus['loaded']

        # if the viewer displaying the index of the file : show the new image
        currentIndexDisplayed = self._qslider.value()
        if currentIndexDisplayed == sliceIndex:
            self.showImage(currentIndexDisplayed)

    def _updatefileName(self):
        imageIndex = self._qslider.value()
        # this can append since we are using thread to load image that the
        # imageIndex is no more referenced.
        if imageIndex not in self._indexToFile:
            return
        else:
            imageName = self._indexToFile[imageIndex]
            if self._joinFolderName is True:
                firstFolder = os.path.split(os.path.dirname(imageName))[-1]
                self._qlFileName.setText(os.path.join(firstFolder,
                                                      os.path.basename(imageName)))
            else:
                self._qlFileName.setText(os.path.basename(imageName))
            self._qlFileName.setToolTip(imageName)

    def _getFileToIndexDict(self):
        res = {}
        for key, value in self._indexToFile.items():
            assert value not in res
            res[value] = key
        return res

    def addFolderName(self, b):
        """
        
        :param bool val: If true then will join the folder name of the file in
                         addition of the file name.
        """
        self._joinFolderName = b


def main():

    import numpy
    images = {}
    for x in range(10):
        images[x] = numpy.random.rand(200, 200)

    app = qt.QApplication([])
    s = _QImageStackPlot(parent=None)
    s.setImages(images)

    s.show()
    app.exec_()


if __name__ == "__main__":
    main()
