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

__authors__ = ["C. Nemoz", "H. Payno"]
__license__ = "MIT"
__date__ = "18/02/2018"

import logging
from silx.gui import qt, icons as silxicons
import os
from tomwer.core.tomodir.TomoDir import TomoDir, logger as TDLogger
from tomwer.core.WaiterThread import WaiterThread
from tomwer.gui.datawatcher import actions
from tomwer.gui.datawatcher import history
from tomwer.gui.datawatcher import configuration, observations

logger = logging.getLogger(__name__)


class DataWatcherWidget(TomoDir, qt.QMainWindow):
    """
    Widget used to see if a finished acquisition is discovered on sub node of
    a selected folder
    """
    _textStopObservation = "Stop observation"
    _textStartObservation = "Start observation"

    obsStatusToWidgetStatus = {
        'not processing': 'Not processed',
        'none found': 'Running',
        'starting': 'Running',
        'started': 'Running',
        'waiting for acquisition ending': 'Running',
        'acquisition ended': 'Executed',
        'acquisition canceled': 'Failed',
        'failure': 'Failed'
    }

    _animatedStates = (
        'none found',
        'parsing',
        'waiting for acquisition ending',
        'starting',
        'started'
    )

    DEFAULT_DIRECTORY = '/lbsram/data/visitor'

    sigTMStatusChanged = qt.Signal(str)
    sigScanReady = qt.Signal(str)

    def __init__(self, parent=None, displayAdvancement=True):
        """Simple class which will check advancement state of the acquisition
        for a specific folder

        :param parent: the parent widget
        """
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self._maxAdv = 100  # maximal progress bar advancement
        self.displayAdvancement = displayAdvancement
        self._configWindow = None
        """Widget containing the configuration of the watcher"""
        self._historyWindow = None
        """Widget containing the latest valid scan found by the watcher"""
        self._observationWidget = None
        """Widget containing the current observed directory by the watcher"""
        TomoDir.__init__(self)
        self.setFolderObserved(self.folderObserved)

    def _initClass(self):
        TomoDir._initClass(self)

        toolbar = qt.QToolBar('')
        self._observationsAction = actions._ObservationAction(
            parent=self, obsWidget = self.getObservationWidget()
        )
        self._configurationAction = actions._ConfigurationAction(
            parent=self, configWidget=self.getConfigWindow())
        self._historyAction = actions._HistoryAction(
            parent=self, historyWidget=self.getHistoryWindow())
        toolbar.addAction(self._observationsAction)
        toolbar.addAction(self._configurationAction)
        toolbar.addAction(self._historyAction)
        self.addToolBar(qt.Qt.RightToolBarArea, toolbar)
        toolbar.setMovable(False)

        self._buildGUI()

        # set initial path to observe
        self.setFolderObserved(self._getInitPath())
        self._initStatusView()

    def getConfigWindow(self):
        if self._configWindow is None:
            self._configWindow = configuration._DWConfigurationWidget(parent=self)
            self._configWindow.startByOldestStateChanged.connect(self.setStartByOldest)
            self._configWindow.startByOldestStateChanged.connect(self._restartObservation)
        return self._configWindow

    def getObservationWidget(self):
        if self._observationWidget is None:
            self._observationWidget = observations._ScanObservation(parent=self)
            if self.observationThread:
                self._observationWidget.setOnGoingObservations(self.observationThread.observations)
        return self._observationWidget

    def _buildGUI(self):
        """Build the GUI of the widget"""
        self.mainWidget = qt.QWidget(parent=self)
        self.mainWidget.setLayout(qt.QVBoxLayout())
        layout = self.mainWidget.layout()

        self.statusBar = qt.QStatusBar(parent=self.mainWidget)
        self._qlInfo = qt.QLabel(parent=self.mainWidget)

        layout.addWidget(self._getFolderSelection())
        layout.addWidget(self._qlInfo)
        layout.addWidget(self._buildStartStopButton())
        layout.addWidget(self.statusBar)

        self.setCentralWidget(self.mainWidget)

    def _buildStartStopButton(self):
        """
        Build the start/stop button in a QHLayout with one spacer on the left
        and one on the rigth
        """
        widget = qt.QWidget(self.mainWidget)
        layout = qt.QHBoxLayout()
        widget.setLayout(layout)

        # left spacer
        spacerL = qt.QWidget(widget)
        spacerL.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        layout.addWidget(spacerL)

        # button
        self._qpbstartstop = qt.QPushButton(self._textStartObservation)
        self._qpbstartstop.setAutoDefault(True)
        self._qpbstartstop.pressed.connect(self._switchObservation)
        layout.addWidget(self._qpbstartstop)

        # right spacer
        spacerR = qt.QWidget(widget)
        spacerR.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        layout.addWidget(spacerR)

        return widget

    def _buildLoopTimeBreak(self):
        """
        Build the spin box to define the break we want to make between two
        observations
        """
        widget = qt.QWidget(self.mainWidget)
        layout = qt.QHBoxLayout()
        widget.setLayout(layout)

        layout.addWidget(qt.QLabel('Waiting time between observations (in s)'))
        self._qsbLoopTimeBreak = qt.QSpinBox(parent=widget)
        self._qsbLoopTimeBreak.setMinimum(1)
        self._qsbLoopTimeBreak.setMaximum(1000000)
        self._qsbLoopTimeBreak.setValue(self.maxWaitBtwObsLoop)
        self._qsbLoopTimeBreak.valueChanged.connect(self.setWaitTimeBtwLoop)
        layout.addWidget(self._qsbLoopTimeBreak)

        return widget

    def _getInitPath(self):
        initPath = ''
        if 'DATADIR' in os.environ:
            initPath = os.environ['DATADIR']
            self._qlInfo.setText(
                "note : environment variable DATADIR found, "
                "$DATADIR setted has the root of the observe folder")
            myFont = self._qlInfo.font()
            myFont.setItalic(True)
            self._qlInfo.setFont(myFont)
        else:
            self._qlInfo.setText(
                "note : no DATADIR environment variable setted. "
                "Can't set a default root directory for observation")
            myFont = self._qlInfo.font()
            myFont.setItalic(True)
            self._qlInfo.setFont(myFont)
        return initPath

    def getHistoryWindow(self):
        if self._historyWindow is None:
            self._historyWindow = history._ScanHistory(parent=self)
        return self._historyWindow

    def stopObservation(self, sucess=False):
        """
        Stop the thread of observation

        :param bool sucess: if True this mean that we are stopping the
        observation because we found an acquisition finished. In this case we
        don't want to update the status and the log message

        :return bool: True if the observation have been stopped. Otherwise this
            mean that not observation was executing
        """
        if TomoDir.stopObservation(self) is True:
            if sucess is False:
                if self._observationWidget is not None:
                    self._observationWidget.clear()
                message = "observation stopped"
                logger.inform(message)
                self.statusBar.showMessage(message)
                self._setCurrentStatus('not processing')
            return True
        else:
            return False

    def startObservation(self):
        """
        Start the thread of observation

         :return bool: True if the observation was started. Otherwise this
            mean that an observation was already running
        """
        if TomoDir.startObservation(self):
            mess = "start observation on %s" % self.folderObserved
            logger.inform(mess)
            self.statusBar.showMessage(mess)
            self._setCurrentStatus('started')
            return True
        else:
            return False

    def _setIsObserving(self, b):
        TomoDir._setIsObserving(self, b)
        if TomoDir.isObserving(self) is True:
            self._qpbstartstop.setText(self._textStopObservation)
        else:
            self._qpbstartstop.setText(self._textStartObservation)

    def _getFolderSelection(self):
        """
        Return the widget used for the folder selection
        """
        widget = qt.QWidget(self)
        layout = qt.QHBoxLayout()

        self._qtbSelectFolder = qt.QPushButton('Select folder', parent=widget)
        self._qtbSelectFolder.setAutoDefault(True)
        self._qtbSelectFolder.clicked.connect(self._setFolderPath)

        self._qteFolderSelected = qt.QLineEdit("", parent=widget)
        self._qteFolderSelected.textChanged.connect(self._updateFolderObserved)
        self._qteFolderSelected.editingFinished.connect(
            self._restartObservation)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._qteFolderSelected)
        layout.addWidget(self._qtbSelectFolder)

        self.animated_icon = silxicons.getWaitIcon()
        self.__stateLabel = qt.QLabel(parent=widget)
        self.animated_icon.register(self.__stateLabel)
        self._setStateIcon(silxicons.getQIcon('remove'))

        self.__stateLabel.setFixedWidth(30)
        layout.addWidget(self.__stateLabel)

        widget.setLayout(layout)
        return widget

    def _setFolderPath(self):
        """
        Ask the user the path to the folder to observe
        """
        defaultDirectory = self.getFolderObserved()
        if defaultDirectory is None or not os.path.isdir(defaultDirectory):
            if os.path.isdir(self.DEFAULT_DIRECTORY):
                defaultDirectory = self.DEFAULT_DIRECTORY
            if defaultDirectory is None:
                defaultDirectory = os.getcwd()

        dialog = qt.QFileDialog(self, directory=defaultDirectory)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)

        if not dialog.exec_():
            dialog.close()
            return

        self.setFolderObserved(dialog.selectedFiles()[0])

        if self.isObserving:
            self._restartObservation()

    def _updateFolderObserved(self, txt):
        self.folderObserved = self._qteFolderSelected.text()

    def setFolderObserved(self, path):
        if path is not None and os.path.isdir(path):
            TomoDir.setFolderObserved(self, path)
            self._qteFolderSelected.setText(self.folderObserved)

    def setStartByOldest(self, b):
        """
        Set if we want to start parsing files from the oldest or the newest

        :param b: 
        :return: 
        """
        TomoDir.setStartByOldest(self, b)
        self.getConfigWindow()._qcboldest.setChecked(self.startByOldest)

    def _initObservation(self):
        """
        Init the thread running the tomodir functions
        """
        if TomoDir._initObservation(self) is True:
            if self._observationWidget is not None:
                self._observationWidget.setOnGoingObservations(
                    self.observationThread.observations)
            return True
        else:
            return False

    def informationReceived(self, info):
        self.statusBar.showMessage(info)

    def _scanStatusChanged(self, scan, status):
        mess = 'scan %s is observed. Status: %s' % (os.path.basename(scan), status)
        self.statusBar.showMessage(mess)

    def _connectObserverThread(self):
        if self.observationThread is not None and self.obsThIsConnected is False:
            self.observationThread.observations.sigObsStatusReceived.connect(
                self._scanStatusChanged
            )
        TomoDir._connectObserverThread(self)

    def _disconnectObserverThread(self):
        if self.observationThread is not None and self.obsThIsConnected is True:
            self.observationThread.observations.sigObsStatusReceived.disconnect(
                self._scanStatusChanged
            )
        TomoDir._disconnectObserverThread(self)

        if self.observationThread is not None and self.obsThIsConnected is True:
            self.observationThread.sigScanReady.disconnect(self._signalScanReady)
            self.obsThIsConnected = False

    def _initStatusView(self):
        """
        The status view need a thread to update the animated icon when scanning
        """
        self.__threadAnimation = WaiterThread(0.3)
        self.__threadAnimation.finished.connect(self._updateAnimatedIcon)

    def _updateStatusView(self):
        """Update the processing state"""
        if self.currentStatus in self._animatedStates:
            if not self.__threadAnimation.isRunning():
                self.__threadAnimation.start()
            elif self.__threadAnimation is not None:
                self.__threadAnimation.quit()
        elif self.currentStatus == 'acquisition ended':
            self._setStateIcon(silxicons.getQIcon('selected'))
        elif self.currentStatus == 'failure':
            self._setStateIcon(silxicons.getQIcon('remove'))
        elif self.currentStatus == 'not processing':
            self._setStateIcon(None)

    def _setStateIcon(self, icon):
        """set the icon pass in parameter to the state label

        :param icon:the icon to set"""
        # needed for heritage from TomoDir
        if icon is None:
            self.__stateLabel.setPixmap(
                qt.QIcon().pixmap(30, state=qt.QIcon.On))
        else:
            self.__stateLabel.setPixmap(icon.pixmap(30, state=qt.QIcon.On))

    def _updateAnimatedIcon(self):
        """Simple function which manage the waiting icon"""
        if self.currentStatus in self._animatedStates:
            icon = self.animated_icon.currentIcon()
            if icon is None:
                icon = qt.QIcon()
            self._setStateIcon(icon)
            # get ready for the next animation
            self.__threadAnimation.start()

    def _signalScanReady(self, scanID):
        TomoDir._signalScanReady(self, scanID)
        self.lastFoundScans.add(scanID)
        self._updateLastReceived()

    def _updateLastReceived(self):
        """
        For now we are updating each time the list.
        It would be better to update it instead.
        """
        self.getHistoryWindow().update(scans=self.lastFoundScans)


if __name__ == '__main__':
    qapp = qt.QApplication([])
    widget = DataWatcherWidget(parent=None)
    widget.show()
    qapp.exec_()
