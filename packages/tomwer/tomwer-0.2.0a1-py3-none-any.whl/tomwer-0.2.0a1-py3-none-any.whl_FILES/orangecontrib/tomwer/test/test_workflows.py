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
__date__ = "24/01/2017"

import logging
import os
import shutil
import tempfile
import unittest
import time
from tomwer.core import utils
from tomwer.core.qtApplicationManager import QApplicationManager
from tomwer.core.settings import mock_lsbram
from orangecontrib.tomwer.test.OrangeWorkflowTest import OrangeWorflowTest
from tomwer.test.utils import UtilsTest
from tomwer.core.RSyncManager import RSyncManager

logging.disable(logging.INFO)

app = QApplicationManager()


class TestLocalReconstructions(OrangeWorflowTest):
    """test with three widgets : ScanList, FTSerieWidget and ImageStackViewerWidget.
        Make sure that when path with data set:
            - scanList is sending signals
            - FTSerieWidget is reconstructing and emitting a signal
            - viewer is displaying a set of data (receiving the information)
    """
    def setUp(self):
        OrangeWorflowTest.setUp(self)
        self.inputdir = tempfile.mkdtemp()

        # copy files directly
        utils.mockAcquisition(self.inputdir)

    def tearDow(self):
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)
        OrangeWorflowTest.tearDown(self)

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        nodeScanList = cls.addWidget(cls,
                                     'orangecontrib.tomwer.widgets.ScanListWidget.ScanListWidget')
        nodeFTSerie = cls.addWidget(cls,
                                    'orangecontrib.tomwer.widgets.FtseriesWidget.FtseriesWidget')
        nodeViewer = cls.addWidget(cls,
                                   'orangecontrib.tomwer.widgets.ImageStackViewerWidget.ImageStackViewerWidget')
        cls.processOrangeEvents(cls)

        cls.link(cls, nodeScanList, "data", nodeFTSerie, "data")
        cls.link(cls, nodeFTSerie, "data", nodeViewer, "data")
        cls.processOrangeEvents(cls)

        cls.scanListWidget = cls.getWidgetForNode(cls, nodeScanList)
        cls.ftserieWidget = cls.getWidgetForNode(cls, nodeFTSerie)
        cls.viewerWidget = cls.getWidgetForNode(cls, nodeViewer)

        # Set we only want to simulate the reconstruction
        cls.ftserieWidget.reconsStack.setMockMode(True)
        cls.ftserieWidget.setForceSync(True)

    @classmethod
    def tearDownClass(cls):
        cls.scanListWidget = None
        cls.ftserieWidget = None
        cls.viewerWidget = None
        OrangeWorflowTest.tearDownClass()

    def test(self):
        """Make sure the workflow is valid and end on the data transfert"""

        # add the path to the directory
        self.scanListWidget.add(self.inputdir)

        self.assertTrue(self.ftserieWidget.ftserieReconstruction is None)

        self.assertTrue(
            self.viewerWidget.viewer.getCurrentScanFolder() == '')
        self.assertTrue(
            self.viewerWidget.viewer.ftseriereconstruction is None)

        # start the workflow by sending the list of path
        self.scanListWidget._sendList()

        # let Orange process
        self.processOrangeEvents()

        # make sure the ftserieWidget have correctly been updated
        self.assertTrue(self.ftserieWidget.ftserieReconstruction is not None)

        while(app.hasPendingEvents()):
            app.processEvents()
            self.processOrangeEventsStack()

        self.assertTrue(
            self.viewerWidget.viewer.getCurrentScanFolder() == self.inputdir)


class TestGlobalReconstructions(OrangeWorflowTest):
    """test the workflow composed of the following widgets :
        - TomoDirWidget
        - FTSerieWidget
        - DarkRef widget
        - ScanValidatorWidget
        - FolderTransfertWidget

        Specially test action at the scan validator level :
            - validation : should bring to a folder transfert (and later to a new validation)
            - cancel : should bring to a clean of the scan validator
            - updateReconsParam : should bring to a new reconstruction
            - low memory case : when the computer is running into low memory then :
                - reconstruction from ftserie should be skipped
                - the user validation from scan validator should be skipped to
    """
    datasetID = 'test10'

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        # copy files directly
        self.inputFolder = tempfile.mkdtemp()
        self.folder1 = os.path.join(self.inputFolder, self.datasetID) + os.sep
        self.output = tempfile.mkdtemp()

        test10Path = UtilsTest().getDataset(self.datasetID)
        shutil.copytree(src=test10Path, dst=self.folder1)

        assert(os.path.isdir(self.folder1))
        # remove refHST file which are incorect
        for _file in ('refHST0000.edf', 'refHST0010.edf'):
            os.remove(os.path.join(self.folder1, _file))
        # register the output folder for transfert
        self.transfertWidget._forceDestinationDir(self.output)

        # get output dir
        self.outputdir1 = self.transfertWidget.getDestinationDir(self.folder1)
        os.mkdir(os.path.join(self.outputdir1, self.datasetID))

        # make sur output folder doesn't exists
        self.assertFalse(self.dataHasBeenCopied())

        self.tomodirWidget.setFolderObserved(self.inputFolder)
        self.transfertWidget._copying = False
        self.lastReconstructionDone = None

        utils.mockLowMemory(False)
        mock_lsbram(False)

        RSyncManager().setForceSync(True)
        self.darkWidget.widget.clearRef()

    def reconstructionDone(self, scanID):
        self.lastReconstructionDone = scanID

    def tearDown(self):
        app.processEvents()
        self.clear()
        # then clean output directory
        self.cleanOutputDir()
        if os.path.isdir(self.output) is True:
            shutil.rmtree(self.output)

        if os.path.isdir(self.inputFolder) is True:
            shutil.rmtree(self.inputFolder)

        if os.path.isdir(self.folder1) is True:
            shutil.rmtree(self.folder1)

        OrangeWorflowTest.tearDown(self)

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        nodeTomodir = cls.addWidget(cls,
                                    'orangecontrib.tomwer.widgets.TomoDirWidget.TomoDirWidget')
        nodeDarkRef = cls.addWidget(cls,
                                    'orangecontrib.tomwer.widgets.DarkRefAndCopyWidget.DarkRefAndCopyOW')
        nodeFTSerie = cls.addWidget(cls,
                                    'orangecontrib.tomwer.widgets.FtseriesWidget.FtseriesWidget')
        nodeValidator = cls.addWidget(cls,
                                      'orangecontrib.tomwer.widgets.ScanValidatorWidget.ScanValidatorWidget')
        nodeFolderTransfert = cls.addWidget(cls,
                                            'orangecontrib.tomwer.widgets.FolderTransfertWidget.FolderTransfertWidget')

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls,
                 nodeTomodir, "data",
                 nodeDarkRef, "data")
        cls.link(cls,
                 nodeDarkRef, "data",
                 nodeFTSerie, "data")
        cls.link(cls,
                 nodeFTSerie, "data",
                 nodeValidator, "data")
        cls.link(cls,
                 nodeValidator, "data",
                 nodeFolderTransfert, "data")

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.tomodirWidget = cls.getWidgetForNode(cls, nodeTomodir)
        cls.ftserieWidget = cls.getWidgetForNode(cls, nodeFTSerie)
        cls.darkWidget = cls.getWidgetForNode(cls, nodeDarkRef)
        cls.validatorWidget = cls.getWidgetForNode(cls, nodeValidator)
        cls.transfertWidget = cls.getWidgetForNode(cls, nodeFolderTransfert)

        # skip any warning for the scan validator
        cls.validatorWidget._warnValManualShow = True
        # set mock mode for FTSerieWidget
        cls.ftserieWidget.reconsStack.setMockMode(True)
        cls.ftserieWidget.setForceSync(True)
        # to avoid one folder transfert to use a thread
        cls.transfertWidget.setIsBlocking(True)
        cls.transfertWidget.turn_off_print = True
        # force Dark ref to be sync
        cls.darkWidget.setForceSync(True)
        # set tomodir ready for observation
        cls.tomodirWidget.displayAdvancement = False

    @classmethod
    def tearDownClass(cls):
        del cls.tomodirWidget
        del cls.ftserieWidget
        del cls.darkWidget
        del cls.validatorWidget
        del cls.transfertWidget
        OrangeWorflowTest.tearDownClass()

    def dataHasBeenCopied(self):
        """

        :return: True if the data has been copied
        """
        sub = os.listdir(self.output)
        return len(sub) > 0 and len(os.listdir(os.path.join(self.output, sub[0]))) > 0

    def testValidation(self):
        """test that workflow is correct if the validate button of the scan
        validator is valid (transfert data)
        """
        # run tomodir widget
        self.executeTomoDir()

        # wait for the dark ref to be reconstructed
        for wt in (1, 1, 1):
            while(app.hasPendingEvents()):
                app.processEvents()
                self.processOrangeEventsStack()
            time.sleep(wt)

        # check refHST have been created
        self.assertTrue(os.path.isfile(os.path.join(self.folder1, 'refHST0000.edf')))
        self.assertTrue(os.path.isfile(os.path.join(self.folder1, 'refHST0020.edf')))

        # make sure FTSerie has the correct path to process
        self.assertTrue(self.ftserieWidget.ftserieReconstruction is not None)

        # check no data have been copied yet
        self.assertFalse(self.dataHasBeenCopied())

        self.validatorWidget._validateCurrentScan()

        # let signal tomodir to ftseries be processed
        while(app.hasPendingEvents()):
            app.processEvents()
            self.processOrangeEventsStack()
        self.assertTrue(self.dataHasBeenCopied())

    def testCancel(self):
        """test that the workflow is correct if the cancel button is activated
        (no data transfert)
        """
        # run tomodir widget
        self.executeTomoDir()

        # wait for the dark ref to be reconstructed
        for wt in (1, 1, 1):
            while(app.hasPendingEvents()):
                app.processEvents()
                self.processOrangeEventsStack()
            time.sleep(wt)

        self.assertFalse(self.dataHasBeenCopied())
        self.validatorWidget._cancelCurrentScan()

        self.processOrangeEvents()

        # check no data have been copied yet
        self.assertFalse(self.dataHasBeenCopied())

    def testChangeReconstructionParameter(self):
        """test that the behavior of the workflow is valid if the
        'change reconstruction param' is activated(no data copied then if
            validated, data will be)
        """
        # make sure we have wait for the validation
        tabDisplaying = self.validatorWidget.widget
        self.assertTrue(tabDisplaying.ftseriereconstruction is None)
        self.assertTrue(len(self.validatorWidget._scansToValidate) is 0)
        # run tomodir widget
        self.executeTomoDir()

        # wait for the dark ref to be reconstructed
        for wt in (1, 1, 1):
            while(app.hasPendingEvents()):
                app.processEvents()
                self.processOrangeEventsStack()
            time.sleep(wt)

        # check no data have been copied yet
        self.assertFalse(self.dataHasBeenCopied())
        nScan = len(self.validatorWidget._scansToValidate)
        # note: some scan can remain fron the cancel unit test
        self.assertTrue(nScan > 0)

        self.validatorWidget._validateCurrentScan()

        # make sure the file have been copied
        while(app.hasPendingEvents()):
            app.processEvents()
            self.processOrangeEventsStack()

        self.assertTrue(len(self.validatorWidget._scansToValidate) is nScan - 1)
        self.assertTrue(self.dataHasBeenCopied())

    def testLowMemory(self):
        """
        Make sure the 'box' locks are unlock when running into low memory

            - Tomodir widget is receiving an acquisition
            - FTSerieWidget should skip reconstruction
            - ScanValidator should be skipped to
            - FolderTransfertWidget should copy data
        """
        assert (os.path.isdir(self.folder1))
        # check no data have been copied yet
        self.assertFalse(self.dataHasBeenCopied())
        utils.mockLowMemory(True)
        mock_lsbram(True)

        # run tomodir widget
        self.executeTomoDir()

        # let signal tomodir to ftseries be processed and from ftseries to
        # folder transfert (and folder transfert to process
        for wt in (1, 1, 1):
            while(app.hasPendingEvents()):
                app.processEvents()
                self.processOrangeEventsStack()
            time.sleep(wt)

        # check data have been copy
        self.assertTrue(self.dataHasBeenCopied())
        # then clean output directory
        self.cleanOutputDir()

    def cleanOutputDir(self):
        """remove any file/folder in the destination directory"""
        for lf in os.listdir(self.output):
            f = os.path.join(self.output, lf)
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)
        self.assertFalse(self.dataHasBeenCopied())

    def executeTomoDir(self):
        """Simulate tomodir execution by sending a signal that an acquisition
        is ready to in self.tomodir
        """
        self.tomodirWidget._widget.mockObservation(self.folder1)

        self.processOrangeEvents()

        self.processOrangeEvents()

    def clear(self):
        """Clear current scheme"""
        # then clean output directory
        self.cleanOutputDir()
        # check no data have been copied yet
        self.assertFalse(self.dataHasBeenCopied())
        self.processOrangeEvents()


class TestCopyNFolder(OrangeWorflowTest):
    """test the following workflow and behavior.
    Workflow is :
        - ScanListWidget
        - FTSerieWidget
        - FolderTransfertWidget

    A list of folder into ScanList them go through FTserieWidget and to
    FolderTransfert. Make sure all the data have been copied
    """

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        scanListNode = cls.addWidget(cls,
                                     'orangecontrib.tomwer.widgets.ScanListWidget.ScanListWidget')
        FTSerieNode = cls.addWidget(cls,
                                    'orangecontrib.tomwer.widgets.FtseriesWidget.FtseriesWidget')
        folderTransfertNode = cls.addWidget(cls,
                                            'orangecontrib.tomwer.widgets.FolderTransfertWidget.FolderTransfertWidget')

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls,
                 scanListNode, "data",
                 FTSerieNode, "data")
        cls.link(cls,
                 FTSerieNode, "data",
                 folderTransfertNode, "data")

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.scanListWidget = cls.getWidgetForNode(cls, scanListNode)
        cls.ftserieWidget = cls.getWidgetForNode(cls, FTSerieNode)
        cls.transfertWidget = cls.getWidgetForNode(cls, folderTransfertNode)

        cls.processOrangeEvents(cls)

        # set mock mode for FTSerieWidget
        cls.ftserieWidget.reconsStack.setMockMode(True)
        cls.transfertWidget.turn_off_print = True
        # to avoid one folder transfert to use a thread
        cls.transfertWidget.setIsBlocking(True)
        cls.ftserieWidget.setForceSync(True)

    @classmethod
    def tearDownClass(cls):
        cls.scanListWidget = None
        cls.ftserieWidget = None
        cls.transfertWidget = None
        OrangeWorflowTest.tearDownClass()

    def setUp(self):
        OrangeWorflowTest.setUp(self)

        # Create n folder
        self.folders = []
        for i in range(1):
            inputFolder = tempfile.mkdtemp()
            self.folders.append(inputFolder)
            # copy files directly
            utils.mockAcquisition(inputFolder)

        self.outputdir = tempfile.mkdtemp()

    def tearDown(self):
        # remove input folders if any
        for f in self.folders:
            if os.path.isdir(f):
                shutil.rmtree(f)

        # remove output folders if any
        if os.path.isdir(self.outputdir):
            shutil.rmtree(self.outputdir)

        OrangeWorflowTest.tearDown(self)

    def testCopy(self):
        # add outputdir to transfertFolderWidget
        self.assertTrue(os.path.isdir(self.outputdir))
        self.transfertWidget._forceDestinationDir(self.outputdir)

        # add all fodle rinto the scanList
        for f in self.folders:
            assert(os.path.isdir(f))
            self.scanListWidget.add(f)
            app.processEvents()
            self.processOrangeEventsStack()

        # make sure nothing has been copied
        self.assertTrue(self.outpudirIsEmpty())

        # then start workflow run by asking the scanListWidget to notice action
        # to the next widget
        self.scanListWidget.start()

        while(app.hasPendingEvents()):
            app.processEvents()
            self.processOrangeEventsStack()

        self.assertTrue(self.dataHasBeenCopied())

    def outpudirIsEmpty(self):
        return len(os.listdir(self.outputdir)) == 0

    def dataHasBeenCopied(self):
        return len(os.listdir(self.outputdir)) == 1


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestGlobalReconstructions, TestCopyNFolder,
               TestLocalReconstructions):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
