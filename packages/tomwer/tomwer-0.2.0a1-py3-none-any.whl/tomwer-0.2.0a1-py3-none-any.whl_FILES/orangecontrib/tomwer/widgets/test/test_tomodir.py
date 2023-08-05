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
__date__ = "17/01/2017"

from tomwer.core.qtApplicationManager import QApplicationManager
from tomwer.core import tomodir
from orangecontrib.tomwer.test.TestAcquisition import Simulation
from orangecontrib.tomwer.widgets.TomoDirWidget import TomoDirWidget
from silx.gui import qt
import unittest
import time
import os
import tempfile
import shutil
import logging

logging.disable(logging.INFO)

# Makes sure a QApplication exists
_qapp = QApplicationManager()


class TomoDirWaiter(object):
    """Define a simple objecy able to wait for some state of the TomodirTo arrive"""
    def __init__(self):
        self.reset()
        self.lastStatus = []

    def reset(self):
        self.lastStatus = []

    def stateHasChanged(self, val):
        """Register all status """
        if val not in self.lastStatus:
            self.lastStatus.append(val)

    def waitForState(self, state, maxWaiting):
        """simple function wich wait until the tomodirWidget reach the given
        state.
        If the widget doesn't reach this state after maxWaiting second. Then fail.

        :param str state: the state we are waiting for
        :param int maxWaiting: the maximal number of second to wait until failling.
        """
        while state not in self.lastStatus:
            time.sleep(1.0)
            _qapp.processEvents()
            maxWaiting -= 1
            if maxWaiting <= 0:
                return False
        return state in self.lastStatus


class TestTomodirAcquisition(unittest.TestCase, TomoDirWaiter):
    """Functions testing the classical behavior of tomodir
    - signal acquisition is over only when all files are copied
    """

    def tearDown(self):
        while(_qapp.hasPendingEvents()):
            _qapp.processEvents()
        self.tomodirWidget.setObservation(False)
        self.tomodirWidget.close()
        del self.tomodirWidget
        self.tomodirWidget = None
        self.s.wait()
        del self.s
        super(TestTomodirAcquisition, self).tearDown()
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)

    def setUp(self):
        self.manipulationId = 'test10'

        super(TestTomodirAcquisition, self).setUp()
        self.inputdir = tempfile.mkdtemp()
        TomoDirWaiter.reset(self)
        self.tomodirWidget = TomoDirWidget(displayAdvancement=False)
        self.tomodirWidget.srcPattern = ''
        self.tomodirWidget.sigTMStatusChanged.connect(self.stateHasChanged)
        self.tomodirWidget.setAttribute(qt.Qt.WA_DeleteOnClose)

        self.s = Simulation(self.inputdir,
                            self.manipulationId,
                            finalState=Simulation.advancement['acquisitionRunning'])

    def testStartAcquisition(self):
        """Make sure the data watch detect the acquisition of started"""
        observeDir = os.path.join(self.inputdir, self.manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s.createFinalXML(True)
        self.tomodirWidget.setFolderObserved(observeDir)

        self.assertTrue(self.tomodirWidget.currentStatus == 'not processing')
        self.s.start()
        self.s.advanceTo('acquisitionDone')
        self.s.start()
        self.s.wait()
        self.tomodirWidget.startObservation()
        self.tomodirWidget._widget.observationThread.wait()
        self.tomodirWidget._widget.observationThread.observations.dict[observeDir].wait()
        finishedAcqui = self.tomodirWidget._widget.observationThread.observations.ignoredFolders
        _qapp.processEvents()
        self.assertTrue(observeDir in finishedAcqui)


class TestTomodirInteraction(unittest.TestCase):
    """Simple unit test to test the start/stop observation button action"""

    def setUp(self):
        super(TestTomodirInteraction, self).setUp()
        self.inputdir = tempfile.mkdtemp()
        self.tomodirWidget = TomoDirWidget(displayAdvancement=False)
        self.tomodirWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.tomodirWidget.srcPattern = ''

    def tearDown(self):
        while(_qapp.hasPendingEvents()):
            _qapp.processEvents()
        self.tomodirWidget.close()
        del self.tomodirWidget
        super(TestTomodirInteraction, self).tearDown()
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)

        def tearDown(self):
            while (_qapp.hasPendingEvents()):
                _qapp.processEvents()

    def testStartAndStopAcquisition(self):
        """test multiple start and stop action on the start observation to
        make sure no crash are appearing
        """
        try:
            self.tomodirWidget.setFolderObserved(self.inputdir)
            self.tomodirWidget.show()
            self.tomodirWidget.setObservation(True)
            for iTest in range(5):
                def tearDown(self):
                    while (_qapp.hasPendingEvents()):
                        _qapp.processEvents()
                self.tomodirWidget._widget._qpbstartstop.pressed.emit()
            self.assertTrue(True)
        except:
            self.assertTrue(False)


class WaitForXMLOption(unittest.TestCase, TomoDirWaiter):
    """test the behavior of tomodir when the option 'wait for xml copy'
    Basically in this case TomoDirObserver will wait until an .xml arrived
    """

    @classmethod
    def setUpClass(cls):
        cls.tomodirWidget = TomoDirWidget(displayAdvancement=False)
        cls.tomodirWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        cls.tomodirWidget.obsMethod = tomodir.DET_END_XML
        cls.tomodirWidget.srcPattern = ''
        cls.manipulationId = 'test10'
        super(WaitForXMLOption, cls).setUpClass()

    def setUp(self):
        self.inputdir = tempfile.mkdtemp()
        self.reset()
        self.tomodirWidget.setObservation(False)
        self.tomodirWidget.resetStatus()
        super(WaitForXMLOption, self).setUp()

    def tearDown(self):
        while(_qapp.hasPendingEvents()):
            _qapp.processEvents()
        super(WaitForXMLOption, self).tearDown()
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)

    @classmethod
    def tearDownClass(cls):
        cls.tomodirWidget.close()
        del cls.tomodirWidget
        if hasattr(cls, 's'):
            cls.s.quit()
            del cls.s
        super(WaitForXMLOption, cls).tearDownClass()

    def testAcquistionNotEnding(self):
        """Check behavior if an acquisition never end
        """
        observeDir = os.path.join(self.inputdir, self.manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s = Simulation(self.inputdir,
                            self.manipulationId,
                            finalState=Simulation.advancement['acquisitionRunning'])
        self.tomodirWidget.setFolderObserved(observeDir)
        self.tomodirWidget.show()
        self.tomodirWidget.sigTMStatusChanged.connect(self.stateHasChanged)

        self.assertTrue(self.tomodirWidget.currentStatus == 'not processing')
        self.s.start()
        self.s.wait()
        self.tomodirWidget.setObservation(True)
        self.tomodirWidget._widget.observationThread.wait()
        self.tomodirWidget._widget.observationThread.observations.dict[observeDir].wait()
        finishedAcqui = self.tomodirWidget._widget.observationThread.observations.ignoredFolders
        _qapp.processEvents()
        self.assertFalse(observeDir in finishedAcqui)

    def testAcquistionEnded(self):
        """Check behavior if an acquisition is ending
        """
        manipulationId = 'test10'
        observeDir = os.path.join(self.inputdir, self.manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s = Simulation(self.inputdir,
                            manipulationId,
                            finalState=Simulation.advancement['acquisitionDone'])
        self.s.createFinalXML(True)
        self.tomodirWidget.setFolderObserved(observeDir)
        self.tomodirWidget.show()
        self.tomodirWidget.sigTMStatusChanged.connect(self.stateHasChanged)

        self.assertTrue(self.tomodirWidget.currentStatus == 'not processing')
        self.s.start()
        self.s.wait()
        self.tomodirWidget.setObservation(True)
        self.tomodirWidget._widget.observationThread.wait()
        self.tomodirWidget._widget.observationThread.observations.dict[observeDir].wait()
        finishedAcqui = self.tomodirWidget._widget.observationThread.observations.ignoredFolders
        _qapp.processEvents()
        self.assertTrue(observeDir in finishedAcqui)


class TestRSync(unittest.TestCase, TomoDirWaiter):
    """test that the synchronization using RSyncManager is working"""

    def setUp(self):
        super(TestRSync, self).setUp()
        self.inputdir = tempfile.mkdtemp()
        self.outputdir = tempfile.mkdtemp()
        TomoDirWaiter.reset(self)
        self.tomodirWidget = TomoDirWidget(displayAdvancement=False)
        self.tomodirWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.tomodirWidget._widget.setSrcAndDestPattern(self.inputdir, self.outputdir)

    def tearDown(self):
        while(_qapp.hasPendingEvents()):
            _qapp.processEvents()
        self.tomodirWidget.close()
        del self.tomodirWidget
        if hasattr(self, 's'):
            self.s.quit()
            del self.s
        super(TestRSync, self).tearDown()
        for d in (self.inputdir, self.outputdir):
            if os.path.isdir(d):
                shutil.rmtree(d, ignore_errors=True)

    def testStartAcquisition(self):
        """Test that rsync is launched when an acquisition is discovered
        """
        manipulationId = 'test10'
        observeDir = os.path.join(self.inputdir, manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s = Simulation(self.inputdir,
                            manipulationId,
                            finalState=Simulation.advancement['acquisitionRunning'])

        self.s.setSrcDestPatterns(self.inputdir, self.outputdir)
        self.s.createFinalXML(True)
        self.tomodirWidget.setFolderObserved(self.inputdir)
        self.tomodirWidget.show()
        self.tomodirWidget.sigTMStatusChanged.connect(self.stateHasChanged)
        self.assertTrue(self.tomodirWidget.currentStatus == 'not processing')
        self.tomodirWidget.setObservation(True)
        maxWaiting = 10
        self.s.start()
        # check state scanning
        time.sleep(0.5)

        self.tomodirWidget.stopObservation()

        # in this case the .info should be in the output dir also
        test10_output = os.path.join(self.outputdir, 'test10')
        test10_input = os.path.join(self.inputdir, 'test10')
        self.assertTrue(os.path.isfile(os.path.join(test10_output, 'test10.info')))

        # make sure file transfert have been started (using rsync)
        # all file in outputdir should be in input dir
        time.sleep(2)
        # check that some .edf file have already been copied
        self.assertTrue(len(test10_output) > 5)

        # xml shouldn't be there because we are righting it at the end
        self.assertFalse(os.path.isfile(os.path.join(test10_output, 'test10.xml')))
        self.assertFalse(os.path.isfile(os.path.join(test10_input, 'test10.xml')))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestTomodirAcquisition, TestTomodirInteraction,
        WaitForXMLOption, TestRSync):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
