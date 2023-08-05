# coding: utf-8
#/*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "22/01/2017"


import unittest
from tomwer.gui.darkref.DarkRefCopyWidget import DarkRefAndCopyWidget
from tomwer.core.darkref.DarkRefs import DarkRefs
from tomwer.gui.FTSerie import _FtserieWidget
from tomwer.core.ReconsParams import ReconsParam
from silx.gui import qt


class TestReconsParamFtSerieDarkRef(unittest.TestCase):
    """Test that the FtSerie and Dark Ref instances are synchronized
    both with the ReconsParam instance"""
    def setUp(self):
        self._ftserie = _FtserieWidget(dir=None, parent=None)
        self._darkRefCopy = DarkRefAndCopyWidget(parent=None)

    def tearDown(self):
        self._ftserie.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._darkRefCopy.setAttribute(qt.Qt.WA_DeleteOnClose)

    def testSync(self):
        """Make sure that connection between dkrf and ftserie are made.
        Some individual test (ftserie and ReconsParams) are also existing"""
        self._ftserie.show()
        self._darkRefCopy.show()
        ftserieEditor = self._ftserie.getFileEditor()
        ftserieDKRf = ftserieEditor._dkRefWidget
        dkrfSkip = self._darkRefCopy.mainWidget.tabGeneral._skipOptionCB

        # test skipping option
        skipping = ftserieDKRf._qcbSkipRef.isChecked()
        self.assertTrue(dkrfSkip.isChecked() is skipping)
        self.assertTrue(ReconsParam().params['DKRF']['REFSOVE'] is not skipping)
        self.assertTrue(ReconsParam().params['DKRF']['DARKSOVE'] is not skipping)
        ftserieDKRf._qcbSkipRef.setChecked(not skipping)
        self.assertTrue(dkrfSkip.isChecked() is not skipping)
        self.assertTrue(ReconsParam().params['DKRF']['REFSOVE'] is int(skipping))
        self.assertTrue(ReconsParam().params['DKRF']['DARKSOVE'] is int(skipping))

        # test dark pattern
        ftserieRef = ftserieEditor._dkRefWidget._qleDKPattern
        dkrfRef = self._darkRefCopy.mainWidget.tabExpert._darkLE
        self.assertTrue(dkrfRef.text() == ftserieRef.text())
        self.assertTrue(dkrfRef.text() == ReconsParam().params['DKRF']['DKFILE'])
        txt = dkrfRef.text()
        dkrfRef.setText(txt + 'toto')
        dkrfRef.editingFinished.emit()
        self.assertTrue(dkrfRef.text() == ftserieRef.text())
        self.assertTrue(dkrfRef.text() == ReconsParam().params['DKRF']['DKFILE'])
        ftserieRef.setText(txt + 'tata')
        ftserieRef.editingFinished.emit()
        self.assertTrue(dkrfRef.text() == ftserieRef.text())
        self.assertTrue(dkrfRef.text() == ReconsParam().params['DKRF']['DKFILE'])

        # test what ref
        ftserieWhatDark = ftserieEditor._dkRefWidget._qcbDKMode
        dkrfWhatDark = self._darkRefCopy.mainWidget.tabGeneral._darkWCB
        self.assertTrue(ftserieWhatDark.getMode() == dkrfWhatDark.getMode())
        for mode in DarkRefs.CALC_MODS:
            ftserieWhatDark.setMode(mode)
            self.assertTrue(dkrfWhatDark.getMode() == mode)
            ReconsParam().params['DKRF']['DARKCAL'] == mode
        for mode in DarkRefs.CALC_MODS:
            dkrfWhatDark.setMode(mode)
            self.assertTrue(ftserieWhatDark.getMode() == mode)
            ReconsParam().params['DKRF']['DARKCAL'] == mode


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestReconsParamFtSerieDarkRef, ):
        test_suite.addTest(
            unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")


