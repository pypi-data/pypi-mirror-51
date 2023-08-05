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
from tomwer.core.ReconsParams import ReconsParam
from silx.gui import qt
from silx.gui.test.utils import TestCaseQt
from tomwer.gui.FTSerie import _FtserieWidget
from tomwer.gui.RecPyHSTWidget import RecPyHSTWidget
from tomwer.core.utils.pyhstutils import _findPyHSTVersions, _getPyHSTDir
from tomwer.core.qtApplicationManager import QApplicationManager
from tomwer.core.ftseries.FastSetupDefineGlobals import FastSetupAll


pyhstVersion = _findPyHSTVersions(_getPyHSTDir())
_qapp = QApplicationManager()


@unittest.skipIf(len(pyhstVersion) is 0, "PyHST2 missing")
class TestRecPyHSTWidget(TestCaseQt):
    """Make sure the gui is correctly editing the ReconsParam and the
    RecPyHST class
    """
    def setUp(self):
        self.widget = RecPyHSTWidget()
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)

        self.ftserieWidget = _FtserieWidget(dir=None)
        self.ftserieWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        ft = FastSetupAll()
        ReconsParam().setStructs(ft.defaultValues)

    def tearDown(self):
        self.widget.close()
        self.ftserieWidget.close()

    def testUpdating(self):
        """Check behavior of the gui when editing the ReconsParam()
        Make sure also that sync with the ftserie is made
        """
        pyhstWidget = self.ftserieWidget.getFileEditor()._PyHSTWidget

        # Test make oar
        isMakeOAR = ReconsParam().getValue(structID='PYHSTEXE',
                                           paramID='MAKE_OAR_FILE')
        self.assertTrue(self.widget._makeOARFileCB.isChecked() == isMakeOAR)
        self.assertTrue(pyhstWidget._makeOARFileCB.isChecked() == isMakeOAR)
        ReconsParam().setValue(structID='PYHSTEXE',
                               paramID='MAKE_OAR_FILE',
                               value=not isMakeOAR)
        self.assertTrue(self.widget._makeOARFileCB.isChecked() != isMakeOAR)
        self.assertTrue(pyhstWidget._makeOARFileCB.isChecked() != isMakeOAR)

        # test pyhst version
        exe = ReconsParam().getValue(structID='PYHSTEXE',
                                     paramID='EXE')
        self.assertTrue(self.widget._qcbPyHSTVersion.currentText() == FastSetupAll.OFFV)
        self.assertTrue(pyhstWidget._qcbPyHSTVersion.currentText() == FastSetupAll.OFFV)
        ReconsParam().setValue(structID='PYHSTEXE',
                               paramID='EXE',
                               value='toto')
        self.assertTrue(pyhstWidget._qcbPyHSTVersion.currentText() == 'toto')
        self.assertTrue(self.widget._qcbPyHSTVersion.currentText() == 'toto')

    def testEdition(self):
        """Check behavior of ReconsParam when editing i through the gui"""
        pyhstWidget = self.ftserieWidget.getFileEditor()._PyHSTWidget

        # Test make oar
        oVal = self.widget._makeOARFileCB.isChecked()
        self.assertTrue(oVal == pyhstWidget._makeOARFileCB.isChecked())
        self.widget._makeOARFileCB.setChecked(not oVal)
        self.assertTrue(
            ReconsParam().getValue(structID='PYHSTEXE',
                                   paramID='MAKE_OAR_FILE') != oVal)
        self.assertFalse(oVal == pyhstWidget._makeOARFileCB.isChecked())
        pyhstWidget._makeOARFileCB.setChecked(oVal)
        self.assertTrue(self.widget._makeOARFileCB.isChecked() == oVal)
        self.assertTrue(
            ReconsParam().getValue(structID='PYHSTEXE',
                                   paramID='MAKE_OAR_FILE') == oVal)

        # test pyhst version
        oExe = ReconsParam().getValue(structID='PYHSTEXE',
                                      paramID='EXE')
        self.assertTrue(
            self.widget._qcbPyHSTVersion.currentText() == oExe)
        self.assertTrue(
            pyhstWidget._qcbPyHSTVersion.currentText() == oExe)
        self.widget._qcbPyHSTVersion.addItem('toto')
        iToto = self.widget._qcbPyHSTVersion.findText('toto')
        assert iToto > 0
        self.widget._qcbPyHSTVersion.setCurrentIndex(iToto)
        self.assertTrue(self.widget._qcbPyHSTVersion.currentText() == 'toto')
        self.assertTrue(pyhstWidget._qcbPyHSTVersion.currentText() == 'toto')
        self.assertTrue(
            ReconsParam().getValue(structID='PYHSTEXE',
                                   paramID='EXE') == 'toto')
        iOExe = self.widget._qcbPyHSTVersion.findText(oExe)
        assert iOExe > 0
        pyhstWidget._qcbPyHSTVersion.setCurrentIndex(iOExe)
        self.assertTrue(self.widget._qcbPyHSTVersion.currentText() == oExe)
        self.assertTrue(pyhstWidget._qcbPyHSTVersion.currentText() == oExe)
        self.assertTrue(
            ReconsParam().getValue(structID='PYHSTEXE',
                                   paramID='EXE') == oExe)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestRecPyHSTWidget, ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
