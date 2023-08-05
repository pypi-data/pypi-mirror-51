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
__date__ = "14/02/2017"


from tomwer.gui.reconsParamsEditor import ReconsParamsEditor
from tomwer.core.qtApplicationManager import QApplicationManager
from tomwer.core.ftseries.FastSetupDefineGlobals import FastSetupAll
from silx.gui.test.utils import TestCaseQt
from silx.gui import qt
import logging
import unittest
import tempfile

# Makes sure a QApplication exists
_qapp = QApplicationManager()

logging.disable(logging.INFO)


class TestSimplifyH5EditorDisplay(TestCaseQt):
    """Make sure we are displayig the correct things
    """
    def setUp(self):
        super(TestSimplifyH5EditorDisplay, self).setUp()
        self.h5Editor = ReconsParamsEditor(None)
        self.h5Editor.setAttribute(qt.Qt.WA_DeleteOnClose)

        self.input = FastSetupAll()
        self.input.structures = self.input.defaultValues
        assert('PAGANIN' in self.input.structures)
        assert('PYHSTEXE' in self.input.structures)
        assert('BEAMGEO' in self.input.structures)

    def tearDown(self):
        self.h5Editor.close()
        del self.h5Editor
        self.qapp.processEvents()
        super(TestCaseQt, self).tearDown()

    def testPAGANIN(self):
        """ As test are 'raw' and based on the values of the FastSetupDefineGlobals
        We are checking the values of FastSetupDefineGlobals by assert
        to make the difference with the 'True' unittest
        """
        widget = self.h5Editor._PaganinWidget
        widget.load(self.input.structures)

        # check Mode conbobox
        assert('MODE' in self.input.structures['PAGANIN'])
        assert(self.input.structures['PAGANIN']['MODE'] == 0)
        self.assertTrue(widget._qcbpaganin.currentIndex() == 0)
        self.assertTrue(widget._qcbpaganin.currentText() == "off")

        # test alpha/beta
        assert('DB2' in self.input.structures['PAGANIN'])
        assert(self.input.structures['PAGANIN']['DB2'] == 100.)
        self.assertTrue(widget._qleSigmaBeta2.text() == str(100.))

        # unsharp coefficient
        assert('UNSHARP_COEFF' in self.input.structures['PAGANIN'])
        assert(self.input.structures['PAGANIN']['UNSHARP_COEFF'] == 3.)
        self.assertTrue(widget._unsharp_sigma_coeff.text() == str(3.))

        # dilate coefficient
        assert('DILATE' in self.input.structures['PAGANIN'])
        assert(self.input.structures['PAGANIN']['DILATE'] == 2)
        self.assertTrue(widget._qleDilatation.text() == str(2))

        # high absorption
        assert('MKEEP_BONE' in self.input.structures['PAGANIN'])
        assert(self.input.structures['PAGANIN']['MKEEP_BONE'] == 0)
        self.assertFalse(widget._qcbKeepBone.isChecked())

    def testPYHST(self):
        """test that the display of the PyHST widget is correct"""
        widget = self.h5Editor._PyHSTWidget
        widget.load(self.input.structures)

        # checkversion
        assert('EXE' in self.input.structures['PYHSTEXE'])
        assert(self.input.structures['PYHSTEXE']['EXE'] == self.input.OFFV)
        self.assertTrue(widget._qcbPyHSTVersion.currentText() == self.input.OFFV)

        # checkofficialversion
        assert('OFFV' in self.input.structures['PYHSTEXE'])
        assert(self.input.structures['PYHSTEXE']['OFFV'] == self.input.OFFV)
        self.assertTrue(widget._qlOfficalVersion.text() == self.input.OFFV)

        # #check verbose
        assert('VERBOSE' in self.input.structures['PYHSTEXE'])
        assert(self.input.structures['PYHSTEXE']['VERBOSE'] == 0)
        self.assertFalse(widget._qcbverbose.isChecked())

        # # check output file
        assert('VERBOSE_FILE' in self.input.structures['PYHSTEXE'])
        assert(self.input.structures['PYHSTEXE']['VERBOSE_FILE'] == 'pyhst_out.txt')
        self.assertTrue(widget._qleVerboseFile.text() == 'pyhst_out.txt')

    def testBeamGEO(self):
        """test that the display of the BeamGeo widget is correct"""
        widget = self.h5Editor._beamGeoWidget
        widget.load(self.input.structures)

        # test reconstruction geometry
        assert('TYPE' in self.input.structures['BEAMGEO'])
        assert(self.input.structures['BEAMGEO']['TYPE'] == 'p')
        self.assertTrue(widget._qcbType.currentText() == 'parallel')

        # test source X
        assert('SX' in self.input.structures['BEAMGEO'])
        assert(self.input.structures['BEAMGEO']['SX'] == 0.)
        self.assertTrue(widget._qleSX.text() == str(0.))

        # test source Y
        assert('SY' in self.input.structures['BEAMGEO'])
        assert(self.input.structures['BEAMGEO']['SY'] == 0.)
        self.assertTrue(widget._qleSY.text() == str(0.))

        # test source Distance
        assert('DIST' in self.input.structures['BEAMGEO'])
        assert(self.input.structures['BEAMGEO']['DIST'] == 55.)
        self.assertTrue(widget._qleDIST.text() == str(55.))

    def testFT(self):
        # parameters from the main widget
        widget = self.h5Editor._mainWidget
        widget.load(self.input.structures)

        assert('FIXEDSLICE' in self.input.structures['FT'])
        assert(self.input.structures['FT']['FIXEDSLICE'] == 'middle')
        self.assertTrue(widget._qcbSelectSlice.currentText() == 'middle')

        assert('VOLOUTFILE' in self.input.structures['FT'])
        assert(self.input.structures['FT']['VOLOUTFILE'] == 0)
        self.assertTrue(widget._qcbEDFStack.isChecked())
        self.assertFalse(widget._qcbSingleVolFile.isChecked())

        assert('CORRECT_SPIKES_THRESHOLD' in self.input.structures['FT'])
        assert(self.input.structures['FT']['CORRECT_SPIKES_THRESHOLD'] == 0.04)
        self.assertTrue(widget._qleThresholdSpikesRm.text() == str(0.04))

        assert('DO_TEST_SLICE' in self.input.structures['FT'])
        assert(self.input.structures['FT']['DO_TEST_SLICE'] == 1)
        self.assertTrue(widget._qcbDoTestSlice.isChecked())

        assert('VOLSELECT' in self.input.structures['FT'])
        assert(self.input.structures['FT']['VOLSELECT'] == 'total')
        self.assertTrue(widget._qcbVolumeSelection.currentText() == 'total')

        assert('VOLSELECTION_REMEMBER' in self.input.structures['FT'])
        assert(self.input.structures['FT']['VOLSELECTION_REMEMBER'] == 0)
        self.assertFalse(widget._qcbVolSelRemenber.isChecked())

        assert('RINGSCORRECTION' in self.input.structures['FT'])
        assert(self.input.structures['FT']['RINGSCORRECTION'] == 0)
        self.assertFalse(widget._qcbRingsCorrection.isChecked())

        # parameters from display widget
        widget = self.h5Editor._displayWidget
        widget.load(self.input.structures)

        assert('SHOWPROJ' in self.input.structures['FT'])
        assert(self.input.structures['FT']['SHOWPROJ'] == 0)
        self.assertFalse(widget._qcbShowProj.isChecked())

        assert('SHOWSLICE' in self.input.structures['FT'])
        assert(self.input.structures['FT']['SHOWSLICE'] == 1)
        self.assertTrue(widget._qcbShowSlice.isChecked())

        assert('ANGLE_OFFSET_VALUE' in self.input.structures['FT'])
        assert(self.input.structures['FT']['ANGLE_OFFSET_VALUE'] == 0.)
        self.assertTrue(widget._qleAngleOffset.text() == str(0.))

        # parameters fron expert widget
        widget = self.h5Editor._expertWidget
        widget.load(self.input.structures)

        assert('NUM_PART' in self.input.structures['FT'])
        assert(self.input.structures['FT']['NUM_PART'] == 4)
        self.assertTrue(widget._getNumericalPart() == 4)

        assert('VERSION' in self.input.structures['FT'])
        assert(self.input.structures['FT']['VERSION'] == 'fastomo3 3.2')
        self.assertTrue(widget._qleVersion.text() == 'fastomo3 3.2')

        assert('DATABASE' in self.input.structures['FT'])
        assert(self.input.structures['FT']['DATABASE'] == 0)
        self.assertFalse(widget._qcbDataBase.isChecked())

        assert('NO_CHECK' in self.input.structures['FT'])
        assert(self.input.structures['FT']['NO_CHECK'] == 0)
        self.assertFalse(widget._qcbNocheck.isChecked())

        assert('ZEROOFFMASK' in self.input.structures['FT'])
        assert(self.input.structures['FT']['ZEROOFFMASK'] == 1)
        self.assertTrue(widget._qcbZeroRegionMask.isChecked())

        assert('FIXHD' in self.input.structures['FT'])
        assert(self.input.structures['FT']['FIXHD'] == 0)
        self.assertFalse(widget._qcbFixHD.isChecked())

    def testFTAxis(self):
        widget = self.h5Editor._axisWidget
        widget.load(self.input.structures)

        assert('POSITION' in self.input.structures['FTAXIS'])
        assert(self.input.structures['FTAXIS']['POSITION'] == 'accurate')
        self.assertTrue(widget._qcbPosition.currentText() == 'accurate')

        assert('POSITION_VALUE' in self.input.structures['FTAXIS'])
        assert(self.input.structures['FTAXIS']['POSITION_VALUE'] == 0.0)
        self.assertTrue(widget._qlePositionValue.text() == str(0.0))

        assert('FILESDURINGSCAN' in self.input.structures['FTAXIS'])
        assert(self.input.structures['FTAXIS']['FILESDURINGSCAN'] == 0)
        self.assertFalse(widget._qcbuseImgsDuringScan.isChecked())

        assert('COR_POSITION' in self.input.structures['FTAXIS'])
        assert(self.input.structures['FTAXIS']['COR_POSITION'] == 0)
        self.assertTrue(widget._getCORPosition() == 0)

        assert('COR_ERROR' in self.input.structures['FTAXIS'])
        assert(self.input.structures['FTAXIS']['COR_ERROR'] == 0)
        self.assertFalse(widget._grpCORError.isChecked())
        self.assertFalse(widget._qleCORError.isEnabled())

        assert('PLOTFIGURE' in self.input.structures['FTAXIS'])
        assert(self.input.structures['FTAXIS']['PLOTFIGURE'] == 1)
        self.assertTrue(widget._qcbPlotFigure.isChecked())

        assert('HA' in self.input.structures['FTAXIS'])
        assert(self.input.structures['FTAXIS']['HA'] == 1)
        self.assertTrue(widget._qcbHA.isChecked())

        assert('HALF_ACQ' in self.input.structures['FT'])
        assert(self.input.structures['FT']['HALF_ACQ'] == 0)
        self.assertFalse(widget._qcbHalfAcq.isChecked())

        assert('FORCE_HALF_ACQ' in self.input.structures['FT'])
        assert(self.input.structures['FT']['FORCE_HALF_ACQ'] == 0)
        self.assertFalse(widget._qcbForceHA.isChecked())

        assert('OVERSAMPLING' in self.input.structures['FTAXIS'])
        assert(self.input.structures['FTAXIS']['OVERSAMPLING'] == 4)
        self.assertTrue(widget._getOversampling() == 4)

    def testDKRF(self):
        widget = self.h5Editor._dkRefWidget
        widget.load(self.input.structures)

        assert('DARKCAL' in self.input.structures['DKRF'])
        assert(self.input.structures['DKRF']['DARKCAL'] == 'Average')
        self.assertTrue(widget._qcbDKMode.getMode() == 'Average')

        assert('REFSCAL' in self.input.structures['DKRF'])
        assert(self.input.structures['DKRF']['REFSCAL'] == 'Median')
        self.assertTrue(widget._qcbRefMode.getMode() == 'Median')

        assert('DKFILE' in self.input.structures['DKRF'])
        assert(self.input.structures['DKRF']['DKFILE'] == 'darkend[0-9]{3,4}')
        self.assertTrue(widget._qleDKPattern.text() == 'darkend[0-9]{3,4}')

        assert('RFFILE' in self.input.structures['DKRF'])
        assert(self.input.structures['DKRF']['RFFILE'] == 'ref*.*[0-9]{3,4}_[0-9]{3,4}')
        self.assertTrue(widget._qleRefsPattern.text() == 'ref*.*[0-9]{3,4}_[0-9]{3,4}')

        assert('REFSRMV' in self.input.structures['DKRF'])
        assert(self.input.structures['DKRF']['REFSRMV'] == 0)
        self.assertFalse(widget._qcbRmRef.isChecked())

        assert('REFSOVE' in self.input.structures['DKRF'])
        assert (self.input.structures['DKRF']['REFSOVE'] == 0)
        self.assertTrue(widget._qcbSkipRef.isChecked())


class TestSimplifyH5EditorSave(TestCaseQt):
    """test that h5editor is returning the correct H5 structures"""

    def setUp(self):
        super(TestSimplifyH5EditorSave, self).setUp()
        self.h5Editor = ReconsParamsEditor(None)
        self.h5Editor.setAttribute(qt.Qt.WA_DeleteOnClose)

        self.input = FastSetupAll()
        self.h5Editor.loadStructures(self.input.structures)

    def tearDown(self):
        self.qapp.processEvents()
        self.h5Editor.close()
        del self.h5Editor
        self.qapp.processEvents()
        super(TestSimplifyH5EditorSave, self).tearDown()

    def testSaving(self):
        # changing some values in BEAMGEO
        assert(self.input.structures['BEAMGEO']['TYPE'] == 'p')
        self.input.structures['BEAMGEO']['TYPE'] = 'c'
        # changing some values in PAGANIN
        assert(self.input.structures['PAGANIN']['MKEEP_BONE'] == 0)
        self.input.structures['PAGANIN']['MKEEP_BONE'] = 1
        # changing some values in PYHSTEXE
        assert(self.input.structures['PYHSTEXE']['VERBOSE_FILE'] == 'pyhst_out.txt')
        self.input.structures['PYHSTEXE']['VERBOSE_FILE'] = 'pyhst_out2.txt'
        assert(self.input.structures['PYHSTEXE']['OFFV'] == self.input.OFFV)
        self.input.structures['PYHSTEXE']['OFFV'] = 'randomString'
        # changing some FT value
        self.input.structures['FT']['FIXEDSLICE'] = 12
        self.input.structures['FT']['CORRECT_SPIKES_THRESHOLD'] = 'Inf'
        self.input.structures['FT']['RINGSCORRECTION'] = 1
        self.input.structures['FTAXIS']['FIXEDSLICE'] = '12'
        self.input.structures['FTAXIS']['ANGLE_OFFSET'] = 1
        self.input.structures['FTAXIS']['SHOWSLICE'] = 0
        self.input.structures['FTAXIS']['PLOTFIGURE'] = 0

        # changing FTAxis values
        self.input.structures['FTAXIS']['POSITION'] = 'fixed'
        self.input.structures['FTAXIS']['POSITION_VALUE'] = 12

        # changing the DKRF values
        self.input.structures['DKRF']['REFSCAL'] = 'Average'
        self.input.structures['DKRF']['DARKCAL'] = 'None'
        self.input.structures['DKRF']['RFFILE'] = 'toto.*'
        self.input.structures['DKRF']['REFSRMV'] = 0

        # loading from new values
        self.h5Editor.loadStructures(self.input.structures)

        # changing again some values
        self.h5Editor._PaganinWidget._qcbpaganin.setCurrentIndex(1)
        self.h5Editor._PyHSTWidget._qcbverbose.setCheckState(qt.Qt.Unchecked)
        self.h5Editor._beamGeoWidget._qleSY.setText('12.0')
        # add some checking on the FT
        self.assertFalse(self.h5Editor._mainWidget._grpThreshold.isChecked())
        self.h5Editor._axisWidget._setOversampling(5)

        _qapp = qt.QApplication.instance()
        _qapp.processEvents()

        # saving the values
        savedStructures = self.h5Editor.getStructs()
        self.assertTrue('BEAMGEO' in savedStructures)
        self.assertTrue('PYHSTEXE' in savedStructures)
        self.assertTrue('PAGANIN' in savedStructures)
        self.assertTrue('FT' in savedStructures)
        self.assertTrue(savedStructures['BEAMGEO']['TYPE'] == 'c')
        self.assertTrue(savedStructures['BEAMGEO']['SY'] == 12.0)

        self.assertTrue(savedStructures['PAGANIN']['MKEEP_BONE'] == 1)
        self.assertTrue(savedStructures['PAGANIN']['MODE'] == 1)

        self.assertTrue(savedStructures['PYHSTEXE']['VERBOSE_FILE'] == 'pyhst_out2.txt')
        self.assertTrue(savedStructures['PYHSTEXE']['OFFV'] == 'randomString')
        self.assertTrue(savedStructures['PYHSTEXE']['VERBOSE'] == 0)

        self.assertTrue(savedStructures['FT']['FIXEDSLICE'] == '12')
        self.assertTrue(savedStructures['FT']['CORRECT_SPIKES_THRESHOLD'] == 'Inf')
        self.assertTrue(savedStructures['FT']['RINGSCORRECTION'] == 1)
        self.assertTrue(self.input.structures['FTAXIS']['FIXEDSLICE'] == '12')
        self.assertTrue(self.input.structures['FTAXIS']['ANGLE_OFFSET'] == 1)
        self.assertTrue(self.input.structures['FTAXIS']['SHOWSLICE'] == 0)

        self.assertTrue(savedStructures['FTAXIS']['POSITION'] == 'fixed')
        self.assertTrue(savedStructures['FTAXIS']['POSITION_VALUE'] == 12)
        self.assertTrue(savedStructures['FTAXIS']['PLOTFIGURE'] == 0)

        self.assertTrue(savedStructures['DKRF']['REFSCAL'] == 'Average')
        self.assertTrue(savedStructures['DKRF']['DARKCAL'] == 'None')
        self.assertTrue(savedStructures['DKRF']['RFFILE'] == 'toto.*')
        self.assertTrue(savedStructures['DKRF']['REFSRMV'] == 0)


class TestOtherWidget(TestCaseQt):

    def setUp(self):
        super(TestOtherWidget, self).setUp()
        self.params = FastSetupAll()

        # Add a h5 group with two parameters
        self.params.structures['TEST'] = {}
        self.params.structures['TEST']['PARAM1'] = 10
        self.params.structures['TEST']['PARAM2'] = 'toto'

        # Add a h5 paraneter under the 'FTAXIS' group
        self.params.structures['FTAXIS']['PARAMTEST'] = 20
        # save the file
        self.inputFile = tempfile.mkstemp(suffix=".h5")[1]
        self.params.writeAll(self.inputFile, 3.8)

        self.h5Editor = ReconsParamsEditor(None)
        self.h5Editor.setAttribute(qt.Qt.WA_DeleteOnClose)

        self.params = FastSetupAll()
        self.params.readAll(self.inputFile, 3.8)
        # load the file
        self.h5Editor.loadStructures(self.params.structures)

    def tearDown(self):
        self.qapp.processEvents()
        self.h5Editor.close()
        del self.h5Editor
        super(TestOtherWidget, self).tearDown()

    def testRead(self):
        "make sure all the H5 parameters and group are loaded correctly"
        self.assertTrue(self.h5Editor.isParamH5Managed('TEST', 'PARAM1'))
        self.assertTrue(self.h5Editor.isParamH5Managed('TEST', 'PARAM2'))
        self.assertTrue(self.h5Editor.isParamH5Managed('FTAXIS', 'PARAMTEST'))

        self.assertTrue(
            self.h5Editor._otherWidget.getParamValue('TEST', 'PARAM1') == 10)
        self.assertTrue(
            self.h5Editor._otherWidget.getParamValue('TEST', 'PARAM2') == 'toto')
        self.assertTrue(
            self.h5Editor._otherWidget.getParamValue('FTAXIS', 'PARAMTEST') == 20)

        savedStructures = self.h5Editor.getStructs()

        self.assertTrue(savedStructures == self.params.structures)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSimplifyH5EditorDisplay, TestSimplifyH5EditorSave,
               TestOtherWidget, ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
