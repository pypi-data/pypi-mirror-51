# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017 European Synchrotron Radiation Facility
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
__date__ = "09/06/2017"

import os
import shutil
import tempfile
import time
import unittest
from tomwer.core import tomodir
from tomwer.core.qtApplicationManager import QApplicationManager
from tomwer.core.tomodir.TomoDirObserver import _TomoDirObserver, _TomoDirFixObserver
from tomwer.core.tomodir._TomoDirProcess import _TomoDirProcess
from tomwer.core.RSyncManager import RSyncManager
from silx.gui import qt
from tomwer.test.utils import UtilsTest

_qapp = QApplicationManager()


class TestTomoDirObserver(unittest.TestCase):
    """
    Simple test to make sure the timeout of tomodir is working properly
    """

    FOLDER_WITH_DATA = 4

    FOLDER_WITHOUT_DATA = 3

    def setUp(self):
        self.observeFolder = tempfile.mkdtemp()

        self.dataSetID = 'test10'
        dataDir = UtilsTest.getDataset(self.dataSetID)
        for iFolder in range(self.FOLDER_WITH_DATA):
            shutil.copytree(dataDir,
                            os.path.join(self.observeFolder, 'f' + str(iFolder), self.dataSetID))

        for iFolder in range(self.FOLDER_WITHOUT_DATA):
            os.makedirs(os.path.join(self.observeFolder, 'empty' + str(iFolder)))

        # observer
        self.observer = _TomoDirObserver(headDir=self.observeFolder,
                                         startByOldest=False,
                                         obsMethod=tomodir.DET_END_XML,
                                         srcPattern=None,
                                         destPattern=None)

    def tearDown(self):
        if os.path.isdir(self.observeFolder):
            shutil.rmtree(self.observeFolder)

    def testRun(self):
        self.observer.run()
        self.assertTrue(len(self.observer.observations) is self.FOLDER_WITH_DATA)
        self.observer.waitForObservationFinished(2)
        for dir, thread in self.observer.observations.dict.items():
            self.assertTrue(thread.status == 'acquisition ended')

    def testRunAcquisitionNotFinished(self):
        for iFolder in range(self.FOLDER_WITH_DATA):
            folder = os.path.join(self.observeFolder, 'f' + str(iFolder), self.dataSetID)
            xmlFile = os.path.join(folder, self.dataSetID + '.xml')
            os.remove(xmlFile)

        self.observer.run()
        self.assertTrue(
            len(self.observer.observations) is self.FOLDER_WITH_DATA)
        self.observer.waitForObservationFinished(2)
        for dir, thread in self.observer.observations.dict.items():
            self.assertTrue(thread.status == 'waiting for acquisition ending')

        f1 = list(self.observer.observations.dict.keys())[0]
        obs = self.observer.observations.dict[f1]
        self.observer.cancelObservation(f1)

        self.assertTrue(
            len(self.observer.observations) is self.FOLDER_WITH_DATA - 1)


class TestTomoDirFixObserver(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.observeFolder = tempfile.mkdtemp()
        self.dataSetID = 'test10'
        dataDir = UtilsTest.getDataset(self.dataSetID)
        shutil.copytree(dataDir,
                        os.path.join(self.observeFolder, self.dataSetID))

        self.thread = _TomoDirFixObserver(
            scanID=os.path.join(self.observeFolder, self.dataSetID),
            obsMethod=tomodir.DET_END_XML,
            srcPattern=None,
            destPattern=None,
            patternObs=None)

    def tearDown(self):
        shutil.rmtree(self.observeFolder)
        unittest.TestCase.tearDown(self)

    def testRunOk(self):
        self.thread.start()
        self.thread.wait(2)
        self.assertTrue(self.thread.status == 'acquisition ended')

    def testFolderNotExisting(self):
        self.thread.setDirToObserve('toto/pluto')
        self.thread.start()
        self.thread.wait(2)
        self.assertTrue(self.thread.status == 'failure')

    def testRunWaitingXML(self):
        fileXML = os.path.join(self.thread.tomodirProcess.RootDir,
                               self.dataSetID + '.xml')
        assert os.path.isfile(fileXML)
        os.remove(fileXML)
        self.thread.start()
        self.thread.wait(2)
        self.assertTrue(self.thread.status == 'waiting for acquisition ending')


class _ObservationCounter(qt.QObject):
    """Basically simulate the next box which has to receive some signal to
    process"""
    def __init__(self):
        qt.QObject.__init__(self)
        self.scansCounted = 0
        self.scansID = []

    def add(self, scanID):
        self.scansCounted = self.scansCounted + 1
        if scanID not in self.scansID:
            self.scansID.append(scanID)

    def getReceivedScan(self):
        return self.scansCounted

    def getDifferentScanReceived(self):
        return len(self.scansID)

    def clear(self):
        self.scansID = []
        self.scansCounted = 0


class TestTomoDir(unittest.TestCase):
    """
    Make sur the TomoDir process is valid
    """

    WAIT_BTW_LOOP = 0.1

    def setUp(self):
        # create a folder with an unfinished acquisition
        self.observeFolder = tempfile.mkdtemp()

        self.dataSetIDs = 'test10', 'test01'
        for scanID in self.dataSetIDs:
            dataDir = UtilsTest.getDataset(scanID)
            shutil.copytree(dataDir,
                            os.path.join(self.observeFolder, scanID))

        self.observationCounter = _ObservationCounter()

        # tomodir
        self.tomodir = tomodir.TomoDir.TomoDirP()
        self.tomodir.setFolderObserved(self.observeFolder)
        self.tomodir.obsMethod = tomodir.DET_END_XML
        self.tomodir.setSrcAndDestPattern(srcPattern=None, destPattern=None)
        self.tomodir.setWaitTimeBtwLoop(self.WAIT_BTW_LOOP)
        self.tomodir.sigScanReady.connect(self.observationCounter.add)

    def tearDown(self):
        self.tomodir.stopObservation()
        self.observationCounter.clear()

        del self.tomodir
        if os.path.isdir(self.observeFolder):
            shutil.rmtree(self.observeFolder)

    def testInfinity(self):
        """
        Test that if we ar ein the infinity mode and two acquisitions are
        existing we will found only those two observations once and that the
        tomodir object is still observing
        """
        self.tomodir.startObservation()
        _qapp.processEvents()
        time.sleep(self.WAIT_BTW_LOOP * 2.0)  # make sure no multiple signal are emitted
        _qapp.processEvents()
        time.sleep(0.4)
        _qapp.processEvents()
        self.tomodir.waitForObservationFinished()
        self.assertTrue(self.tomodir.observationThread is not None)
        self.assertTrue(len(self.tomodir.lastFoundScans) == 2)
        self.assertTrue(self.observationCounter.getReceivedScan() == 2)
        self.assertTrue(self.observationCounter.getDifferentScanReceived() == 2)
        self.tomodir.stopObservation()

    def testPatternFileObsMethod(self):
        """
        Test the DET_END_USER_ENTRY observation method.
        Will look for a file pattern given by the user in the scanID directory
        """
        def tryPattern(pattern, filePrefix, fileSuffix):
            self.tomodir.stopObservation()
            self.observationCounter.clear()

            self.tomodir.setObsMethod((tomodir.DET_END_USER_ENTRY,
                                      {'pattern': pattern}))

            tempfile.mkdtemp(prefix=filePrefix,
                             suffix=fileSuffix,
                             dir=os.path.join(self.observeFolder, 'test10'))

            self.assertTrue(
                self.observationCounter.getDifferentScanReceived() is 0)

            self.tomodir.startObservation()
            self.tomodir.waitForObservationFinished()
            _qapp.processEvents()
            time.sleep(0.4)
            _qapp.processEvents()

            return self.observationCounter.getDifferentScanReceived() is 1

        self.assertTrue(tryPattern(pattern='*tatayoyo*.cfg',
                                   filePrefix='tatayoyo',
                                   fileSuffix='.cfg'))

        self.assertFalse(tryPattern(pattern='*tatayoyo*.cfg',
                                    filePrefix='tatayoyo',
                                    fileSuffix=''))

        self.assertFalse(tryPattern(pattern='tatayoyo.cfg',
                                    filePrefix='tatayoyo',
                                    fileSuffix='.cfg'))


class TestTomodirAborted(unittest.TestCase):
    """Test behavior of the TomoDir when some acquisition are aborted"""
    def setUp(self):
        # create a folder with an unfinished acquisition
        self.observeFolder = tempfile.mkdtemp()

        # tomodir
        self.tomodir = tomodir.TomoDir.TomoDirP()
        self.tomodir.setFolderObserved(self.observeFolder)
        self.tomodir.obsMethod = tomodir.DET_END_XML
        self.tomodir.setSrcAndDestPattern(srcPattern=None, destPattern=None)

        self.dataDir01 = UtilsTest.getDataset('test01')
        self.dataDir10 = UtilsTest.getDataset('test10')

        RSyncManager().setForceSync(False)

    def tearDown(self):
        self.tomodir.stopObservation()
        if os.path.exists(self.observeFolder):
            shutil.rmtree(self.observeFolder)

    def testAbortedFindNext(self):
        """Make sure if an acquisition is aborted then we will skip it
        and that the NEXT acquisition will be found"""
        self.tomodir.setWaitTimeBtwLoop(0.1)
        self.assertTrue(len(self.tomodir.getIgnoredFolders()) is 0)

        dirTest01 = os.path.join(self.observeFolder, 'test01')
        shutil.copytree(self.dataDir01, dirTest01)
        # add the `abort file`
        open(os.path.join(dirTest01, 'test01' + _TomoDirProcess.ABORT_FILE),
             'a')
        self.tomodir.startObservation()
        self.tomodir.observationThread.wait()
        _qapp.processEvents()
        self.assertTrue(len(self.tomodir.getIgnoredFolders()) is 0)
        self.assertTrue(self.tomodir.isObserving is True)
        dirTest10 = os.path.join(self.observeFolder, 'test10')
        shutil.copytree(self.dataDir10, dirTest10)
        _qapp.processEvents()
        time.sleep(0.2)
        _qapp.processEvents()
        self.assertTrue(len(self.tomodir.lastFoundScans) is 1)
        self.assertTrue(dirTest10 in self.tomodir.lastFoundScans)

    def testAbortedFindPrevious(self):
        """Make sure if an acquisition is aborted then we will skip it
        and that the PREVIOUS acquisition will be found"""
        self.tomodir.setWaitTimeBtwLoop(0.1)
        self.assertTrue(len(self.tomodir.getIgnoredFolders()) is 0)

        dirTest10 = os.path.join(self.observeFolder, 'test10')
        shutil.copytree(self.dataDir10, dirTest10)
        dirTest01 = os.path.join(self.observeFolder, 'test01')
        shutil.copytree(self.dataDir01, dirTest01)
        # add the `abort file`
        open(os.path.join(dirTest01, 'test01' + _TomoDirProcess.ABORT_FILE),
             'a')
        self.tomodir.startObservation()
        self.tomodir.observationThread.wait()
        _qapp.processEvents()
        self.assertTrue(self.tomodir.isObserving is True)
        time.sleep(0.2)
        _qapp.processEvents()
        time.sleep(0.2)
        _qapp.processEvents()
        self.assertTrue(len(self.tomodir.lastFoundScans) is 1)
        self.assertTrue(dirTest10 in self.tomodir.lastFoundScans)

    def testAbortedWhenWaitingFor(self):
        """
        Make sure will skip the scan if aborted even if observation started
        """
        self.tomodir.setWaitTimeBtwLoop(0.1)
        self.assertTrue(len(self.tomodir.getIgnoredFolders()) is 0)

        dirTest01 = os.path.join(self.observeFolder, 'test01')
        shutil.copytree(self.dataDir01, dirTest01)
        self.tomodir.startObservation()
        # add the `abort file`
        open(os.path.join(dirTest01, 'test01' + _TomoDirProcess.ABORT_FILE),
             'a')
        self.tomodir.observationThread.wait()
        _qapp.processEvents()
        self.assertTrue(len(self.tomodir.getIgnoredFolders()) is 0)
        self.assertTrue(self.tomodir.isObserving is True)
        dirTest10 = os.path.join(self.observeFolder, 'test10')
        shutil.copytree(self.dataDir10, dirTest10)
        _qapp.processEvents()
        time.sleep(0.2)
        _qapp.processEvents()
        self.assertTrue(len(self.tomodir.lastFoundScans) is 1)
        self.assertTrue(dirTest10 in self.tomodir.lastFoundScans)

    def testAbortedRemovingFolder(self):
        """Make sure the aborted folder is removed after found by tomodir"""
        RSyncManager().setForceSync(True)
        self.tomodir.setWaitTimeBtwLoop(0.1)
        dirTest01 = os.path.join(self.observeFolder, 'test01')
        shutil.copytree(self.dataDir01, dirTest01)
        # add the `abort file`
        open(os.path.join(dirTest01, 'test01' + _TomoDirProcess.ABORT_FILE),
             'a')
        self.tomodir.startObservation()
        self.tomodir.observationThread.wait()
        assert dirTest01 in self.tomodir.observationThread.observations.dict
        obs = self.tomodir.observationThread.observations.dict[dirTest01]
        obs.wait()
        self.assertFalse(os.path.exists(dirTest01))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestTomoDirObserver, TestTomoDir, TestTomoDirFixObserver):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")