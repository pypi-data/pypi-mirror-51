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
import unittest
from silx.gui import qt
from orangecontrib.tomwer.widgets.DarkRefAndCopyWidget import DarkRefWidget
from orangecontrib.tomwer.widgets.FtseriesWidget import FtseriesWidget
from tomwer.core.ftseries.FastSetupDefineGlobals import FastSetupAll
from tomwer.core.darkref.DarkRefs import DarkRefs
from tomwer.core.ReconsParams import ReconsParam
from tomwer.core.qtApplicationManager import QApplicationManager
from tomwer.test.utils import UtilsTest
import tempfile
import shutil
import os

_qapp = QApplicationManager()

logging.disable(logging.INFO)


class TestDarkRefWidget(unittest.TestCase):
    """class testing the DarkRefWidget"""

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.widget = DarkRefWidget(parent=None)
        ReconsParam().setStructs(FastSetupAll().defaultValues)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()

    def testSyncRead(self):
        """Make sure any modification on the ReconsParam() is 
        applied on the GUI"""
        rp = ReconsParam()
        self.assertTrue('DKRF' in rp.params)
        self.assertTrue(rp.getValue(structID='DKRF', paramID='REFSRMV') is 1)
        self.assertTrue(self.widget.mainWidget.tabGeneral._rmOptionCB.isChecked())
        rp.setValue(structID='DKRF', paramID='REFSRMV', value=0)
        self.assertFalse(self.widget.mainWidget.tabGeneral._rmOptionCB.isChecked())

        pattern = self.widget.mainWidget.tabExpert._refLE.text()
        newText = 'popo.*'
        assert(pattern != newText)
        rp.setValue(structID='DKRF', paramID='RFFILE', value=newText)
        self.assertTrue(
            self.widget.mainWidget.tabExpert._refLE.text() == newText)

    def testSyncWrite(self):
        """Test that if we edit through the :class:`DarkRefWidget` then the
        modification are fall back into the ReconsParam()"""
        rp = ReconsParam()

        # test patterns
        pattern = self.widget.mainWidget.tabExpert._refLE.text()
        newText = 'popo.*'
        assert(pattern != newText)
        self.widget.mainWidget.tabExpert._refLE.setText(newText)
        self.assertTrue(rp.getValue('DKRF', 'RFFILE') == newText)
        self.widget.mainWidget.tabExpert._darkLE.setText(newText)
        self.assertTrue(rp.getValue('DKRF', 'DKFILE') == newText)

        # test calc mode
        self.widget.mainWidget.tabGeneral._darkWCB.setMode(DarkRefs.CALC_NONE)
        self.widget.mainWidget.tabGeneral._refWCB.setMode(DarkRefs.CALC_MEDIAN)
        self.assertTrue(rp.getValue('DKRF', 'DARKCAL') == DarkRefs.CALC_NONE)
        self.assertTrue(rp.getValue('DKRF', 'REFSCAL') == DarkRefs.CALC_MEDIAN)

        # test options
        cuRm = self.widget.mainWidget.tabGeneral._rmOptionCB.isChecked()
        self.widget.mainWidget.tabGeneral._rmOptionCB.setChecked(not cuRm)
        self.assertTrue(rp.getValue('DKRF', 'REFSRMV') == (not cuRm))
        self.assertTrue(rp.getValue('DKRF', 'DARKRMV') == (not cuRm))

        cuSkip = self.widget.mainWidget.tabGeneral._skipOptionCB.isChecked()
        self.widget.mainWidget.tabGeneral._skipOptionCB.setChecked(not cuSkip)
        # warning : here value of skip and overwrite are of course inverse
        self.assertTrue(rp.getValue('DKRF', 'DARKOVE') == cuSkip)
        self.assertTrue(rp.getValue('DKRF', 'REFSOVE') == cuSkip)

    def testBehaviorWithFtserie(self):
        """Make sure modification on ftserie 'Dark and flat field' tab are
        correctly take into account"""
        ftserie = FtseriesWidget()

        cuRm = ftserie.getFileEditor()._dkRefWidget._qcbRmRef.isChecked()
        cuSkip = ftserie.getFileEditor()._dkRefWidget._qcbSkipRef.isChecked()
        calcDK = ftserie.getFileEditor()._dkRefWidget._qcbDKMode.getMode()
        calcRef = ftserie.getFileEditor()._dkRefWidget._qcbRefMode.getMode()
        patternRef = ftserie.getFileEditor()._dkRefWidget._qleRefsPattern.text()
        patternDK = ftserie.getFileEditor()._dkRefWidget._qleDKPattern.text()

        # make sure initial status are the same between ftserie and darkref
        self.assertTrue(self.widget.mainWidget.tabGeneral._rmOptionCB.isChecked() == cuRm)
        self.assertTrue(self.widget.mainWidget.tabGeneral._skipOptionCB.isChecked() == cuSkip)
        self.assertTrue(self.widget.mainWidget.tabGeneral._darkWCB.getMode() == calcDK)
        self.assertTrue(self.widget.mainWidget.tabGeneral._refWCB.getMode() == calcRef)
        self.assertTrue(self.widget.mainWidget.tabExpert._refLE.text() == patternRef)
        self.assertTrue(self.widget.mainWidget.tabExpert._darkLE.text() == patternDK)

        # change parameters
        ftserie.getFileEditor()._dkRefWidget._qcbRmRef.setChecked(not cuRm)
        ftserie.getFileEditor()._dkRefWidget._qcbSkipRef.setChecked(not cuSkip)
        ftserie.getFileEditor()._dkRefWidget._qcbDKMode.setMode(DarkRefs.CALC_NONE)
        ftserie.getFileEditor()._dkRefWidget._qcbRefMode.setMode(DarkRefs.CALC_AVERAGE)
        text_ref_pattern = 'toto.*'
        text_dk_pattern = '[maestro]?.'
        ftserie.getFileEditor()._dkRefWidget._qleDKPattern.setText(text_dk_pattern)
        ftserie.getFileEditor()._dkRefWidget._qleRefsPattern.setText(text_ref_pattern)

        # check modification are well take into account
        self.assertTrue(self.widget.mainWidget.tabGeneral._rmOptionCB.isChecked() == (not cuRm))
        self.assertTrue(ReconsParam().getValue('DKRF', 'DARKRMV') == (not cuRm))
        self.assertTrue(self.widget.mainWidget.tabGeneral._skipOptionCB.isChecked() == (not cuSkip))
        self.assertTrue(ReconsParam().getValue('DKRF', 'DARKOVE') == cuRm)
        self.assertTrue(self.widget.mainWidget.tabGeneral._darkWCB.getMode() == DarkRefs.CALC_NONE)
        self.assertTrue(ReconsParam().getValue('DKRF', 'DARKCAL') == DarkRefs.CALC_NONE)
        self.assertTrue(self.widget.mainWidget.tabGeneral._refWCB.getMode() == DarkRefs.CALC_AVERAGE)
        self.assertTrue(ReconsParam().getValue('DKRF', 'REFSCAL') == DarkRefs.CALC_AVERAGE)
        self.assertTrue(self.widget.mainWidget.tabExpert._refLE.text() == text_ref_pattern)
        self.assertTrue(self.widget.mainWidget.tabExpert._darkLE.text() == text_dk_pattern)
        self.assertTrue(ReconsParam().getValue('DKRF', 'DKFILE') == text_dk_pattern)
        self.assertTrue(ReconsParam().getValue('DKRF', 'RFFILE') == text_ref_pattern)


@unittest.skipIf(UtilsTest.getInternalTestDir('testslicesNemoz6x') is None, "No extra datatset")
class TestID16TestCase(unittest.TestCase):
    """
    class testing the process of the dark ref widget in the case of ID16
    """
    def setUp(self):
        unittest.TestCase.setUp(self)
        print(UtilsTest.getInternalTestDir('testslicesNemoz6x'))
        datasetDir = UtilsTest.getInternalTestDir('testslicesNemoz6x')
        self._tmpDir = tempfile.mkdtemp()
        self.datasets = []
        for subFolder in ('testslicesNemoz61_1_', 'testslicesNemoz62_1_',
                          'testslicesNemoz63_1_', 'testslicesNemoz64_1_',
                          'testslicesNemoz65_1_'):
            shutil.copytree(os.path.join(datasetDir, subFolder),
                            os.path.join(self._tmpDir, subFolder))
            self.datasets.append(os.path.join(self._tmpDir, subFolder))

        self.widget = DarkRefWidget(self)
        self.widget.setForceSync(True)

    def tearDown(self):
        shutil.rmtree(self._tmpDir)
        unittest.TestCase.tearDown(self)

    def test(self):
        """make sure the behavior of dark ref is correct for id16b pipeline:
        datasets is composed of :
        
        - testslicesNemoz61_1_: contains original dark and ref. DarkRef should
           process thos to generate median ref and dark
        - testslicesNemoz62_1_, testslicesNemoz63_1_, testslicesNemoz64_1_:
           contains no ref or dark orignals or median.
           should copy the one normalized from testslicesNemoz61_1_
        testslicesNemoz65_1_: contains dark median. Should copy ref from 
            testslicesNemoz61_1_
        """
        # check behavior for testslicesNemoz61_1_.
        files = os.listdir(self.datasets[0])
        assert 'darkend0000.edf' in files
        assert 'ref0000_0000.edf' in files
        assert 'ref0000_0050.edf' in files
        assert 'ref0001_0000.edf' in files
        assert 'ref0001_0050.edf' in files
        assert 'refHST0000.edf' not in files
        assert 'refHST0050.edf' not in files
        assert 'dark.edf' not in files

        self.widget.process(self.datasets[0])

        files = os.listdir(self.datasets[0])
        self.assertTrue('darkend0000.edf' not in files)
        self.assertTrue('ref0000_0000.edf' not in files)
        self.assertTrue('ref0000_0050.edf' not in files)
        self.assertTrue('ref0001_0000.edf' not in files)
        self.assertTrue('ref0001_0050.edf' not in files)
        self.assertTrue('refHST0000.edf' in files)
        self.assertTrue('refHST0050.edf' in files)
        self.assertTrue('dark.edf' in files)
        self.assertTrue(self.widget.hasRefStored())

        # check behavior for testslicesNemoz62_1_, testslicesNemoz63_1_,
        # testslicesNemoz64_1_.
        for dataset in self.datasets[1:4]:
            files = os.listdir(dataset)
            assert 'darkend0000.edf' not in files
            assert 'ref0000_0000.edf' not in files
            assert 'ref0000_0050.edf' not in files
            assert 'ref0001_0000.edf' not in files
            assert 'ref0001_0050.edf' not in files
            assert 'refHST0000.edf' not in files
            assert 'refHST0050.edf' not in files
            assert 'dark.edf' not in files
            self.widget.process(dataset)

            files = os.listdir(dataset)
            self.assertTrue('darkend0000.edf' not in files)
            self.assertTrue('ref0000_0000.edf' not in files)
            self.assertTrue('ref0000_0050.edf' not in files)
            self.assertTrue('ref0001_0000.edf' not in files)
            self.assertTrue('ref0001_0050.edf' not in files)
            self.assertTrue('refHST0000.edf' in files)
            self.assertTrue('refHST0050.edf' in files)
            self.assertTrue('dark.edf' in files)

        # check behavior for testslicesNemoz65_1_
        dataset = self.datasets[-1]
        files = os.listdir(dataset)
        assert 'darkend0000.edf' not in files
        assert 'ref0000_0000.edf' not in files
        assert 'ref0000_0050.edf' in files
        assert 'ref0001_0000.edf' not in files
        assert 'ref0001_0050.edf' in files
        assert 'refHST0000.edf' not in files
        assert 'refHST0050.edf' not in files
        assert 'dark0000.edf' not in files
        self.widget.process(dataset)
        # TODO : compare the refHST to make the correct one is keeped

        files = os.listdir(dataset)
        self.assertTrue('darkend0000.edf' not in files)
        self.assertTrue('ref0000_0000.edf' not in files)
        self.assertTrue('ref0000_0050.edf' not in files)
        self.assertTrue('ref0001_0000.edf' not in files)
        self.assertTrue('ref0001_0050.edf' not in files)
        self.assertTrue('refHST0000.edf' in files)
        self.assertTrue('refHST0050.edf' in files)
        self.assertTrue('dark.edf' in files)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestDarkRefWidget, TestID16TestCase):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
