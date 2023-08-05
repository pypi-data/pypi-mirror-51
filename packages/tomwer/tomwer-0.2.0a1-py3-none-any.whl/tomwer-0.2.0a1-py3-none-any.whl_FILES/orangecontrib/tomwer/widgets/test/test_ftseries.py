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


from tomwer.core.qtApplicationManager import QApplicationManager
from orangecontrib.tomwer.widgets.FtseriesWidget import FtseriesWidget
from tomwer.core.ftseries.FastSetupDefineGlobals import FastSetupAll
from tomwer.core.utils import ftseriesutils
from tomwer.core.ReconsParams import ReconsParam
from silx.gui import qt
import unittest
import os
import tempfile
import shutil
import logging

logging.disable(logging.INFO)

# Makes sure a QApplication exists
_qapp = QApplicationManager()


class TestFTSerieWidget(unittest.TestCase):
    """Simple unit test to test the start/stop observation button action"""

    def setUp(self):
        super(TestFTSerieWidget, self).setUp()
        self.ftseriewidget = FtseriesWidget()

        self.tempdir = tempfile.mkdtemp()
        self.h5_fname = os.path.join(self.tempdir, "octave.h5")
        ftseriesutils.generateDefaultH5File(self.h5_fname)
        self.savePath = tempfile.mkstemp(suffix=".h5")[1]
        ReconsParam().setStructs(FastSetupAll().defaultValues)
        self.ftseriewidget.setAttribute(qt.Qt.WA_DeleteOnClose)

    def tearDown(self):
        os.unlink(self.savePath)
        if os.path.isdir(self.tempdir):
            shutil.rmtree(self.tempdir)
        self.ftseriewidget.close()
        del self.ftseriewidget
        super(TestFTSerieWidget, self).tearDown()

    def testAngleOffset(self):
        self.ftseriewidget.updatePath(self.tempdir)
        self.assertTrue(
            self.ftseriewidget.getFileEditor().isParamH5Managed('FT', 'ANGLE_OFFSET')
        )
        _qapp.processEvents()
        ft = self.ftseriewidget.getFileEditor().getStructs()
        self.assertTrue(ft['FT']['FIXEDSLICE'] == 'middle')
        self.assertTrue(float(ft['FT']['ANGLE_OFFSET_VALUE']) == 0.0)

        self.ftseriewidget.show()

        self.ftseriewidget.save(self.savePath)
        _qapp.processEvents()

        readed = FastSetupAll()
        readed.readAll(self.h5_fname, 3.8)
        self.assertTrue(readed.structures['FT']['ANGLE_OFFSET'] == 0)

        ReconsParam().setValue('FT', 'ANGLE_OFFSET_VALUE', 1.0)
        self.assertTrue(ReconsParam().getValue('FT', 'ANGLE_OFFSET') == 1)
        self.ftseriewidget.save(self.savePath)
        _qapp.processEvents()
        readed = FastSetupAll()
        readed.readAll(self.savePath, 3.8)
        self.assertTrue(readed.structures['FT']['ANGLE_OFFSET_VALUE'] == 1)
        self.assertTrue(readed.structures['FT']['ANGLE_OFFSET'] == 1)


class TestControlsFTSeriesWidget(unittest.TestCase):
    """Simple test of the control button for the FTserieWidget
    """
    def setUp(self):
        super(TestControlsFTSeriesWidget, self).setUp()
        # create octave h5 with default
        self.scanID = tempfile.mkdtemp()
        # one with some modifications
        self.modifySettings = os.path.join(self.scanID, 'modifySettings.h5')
        ft = FastSetupAll()
        assert(ft.structures['FTAXIS']['OVERSAMPLING'] != 12)
        ft.structures['FTAXIS']['OVERSAMPLING'] = 12
        ft.writeAll(self.modifySettings, 3.8)
        # simulate an acquisition (files at least)
        self.widget = FtseriesWidget()
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)

    def tearDown(self):
        self.widget.close()
        del self.widget
        if os.path.isdir(self.scanID):
            shutil.rmtree(self.scanID)
        super(TestControlsFTSeriesWidget, self).tearDown()

    def testShow(self):
        """make sure the h5file is created in the dataset directory"""
        self.widget.updatePath(self.scanID)
        _qapp.processEvents()
        self.assertTrue(self.scanID == self.widget.ftserieReconstruction.scanID)

    def testSave(self):
        """Make sure that the save action is correct"""
        self.widget.updatePath(self.scanID)
        _qapp.processEvents()
        self.assertTrue(self.scanID == self.widget.ftserieReconstruction.scanID)
        self.widget.show()
        _qapp.processEvents()

        tmpH5File = tempfile.mkstemp(suffix=".h5")[1]
        self.widget.save(tmpH5File, displayInfo=False)

        ftOri = FastSetupAll()
        originalStructures = ftOri.defaultValues

        ftSaved = FastSetupAll()
        ftSaved.readAll(filn=self.modifySettings, targetted_octave_version=3.8)
        self.assertTrue(ftSaved.structures["FTAXIS"]["OVERSAMPLING"] == 12)
        ftSaved.structures["FTAXIS"]["OVERSAMPLING"] = originalStructures["FTAXIS"]["OVERSAMPLING"]
        self.assertTrue(originalStructures == ftSaved.structures)

    def testLoad(self):
        """Make sure the load action is correct"""
        self.widget.updatePath(self.scanID)
        _qapp.processEvents()
        self.assertTrue(self.scanID == self.widget.ftserieReconstruction.scanID)
        self.widget.show()
        self.widget.load(self.modifySettings)

        tmpH5File = tempfile.mkstemp(suffix=".h5")[1]
        self.widget.save(tmpH5File)
        self.assertTrue(
            self.fileContainEqual(self.modifySettings, tmpH5File))
        os.unlink(tmpH5File)

    def fileContainEqual(self, f1, f2):
        ft1 = FastSetupAll()
        ft1.readAll(filn=f1, targetted_octave_version=3.8)

        ft2 = FastSetupAll()
        ft2.readAll(filn=f2, targetted_octave_version=3.8)

        return ft1.structures == ft2.structures


class TestExploreDatasetForH5(unittest.TestCase):
    """Make sure that in the case the octave_FT_params.h5 exists in a directory
    this will be the one picked by the editor if the 'explore dataset' option
    is activated
    """
    def setUp(self):
        super(TestExploreDatasetForH5, self).setUp()
        self.scanIDWithH5 = tempfile.mkdtemp()
        self.scanIDWithoutH5 = tempfile.mkdtemp()
        self.ft = FastSetupAll()
        assert(self.ft.structures['FTAXIS']['OVERSAMPLING'] != 12)
        self.ft.structures['FTAXIS']['OVERSAMPLING'] = 12

        self.modifySettings = os.path.join(self.scanIDWithH5, 'octave_FT_params.h5')
        self.ft.writeAll(self.modifySettings, 3.8)

        self.widget = FtseriesWidget()
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)

        ReconsParam().setStructs(self.ft.defaultValues)

    def tearDown(self):
        if os.path.isfile(self.modifySettings):
            os.remove(self.modifySettings)
        if os.path.isdir(self.scanIDWithH5):
            shutil.rmtree(self.scanIDWithH5)
        if os.path.isdir(self.scanIDWithoutH5):
            shutil.rmtree(self.scanIDWithoutH5)
        self.widget.close()
        super(TestExploreDatasetForH5, self).tearDown()

    def testExploreInFolderWithH5(self):
        """Make sure the widget if try to explore the scan dir will load
        the reconstruction parameters from it
        """
        self.widget.setH5Exploration(True)
        self.widget.updatePath(self.scanIDWithH5)
        self.assertTrue(self.scanIDWithH5 == self.widget.ftserieReconstruction.scanID)
        self.assertTrue(
            ReconsParam().getValue('FTAXIS', 'OVERSAMPLING') == 12)

    def testExploreInFolderWithoutH5(self):
        """Make sure the widget if try to explore the scan dir will load
        the reconstruction parameters from it
        """
        self.widget.setH5Exploration(False)
        self.widget.updatePath(self.scanIDWithoutH5)
        self.assertTrue(self.scanIDWithoutH5 == self.widget.ftserieReconstruction.scanID)
        self.assertTrue(
            ReconsParam().getValue('FTAXIS', 'OVERSAMPLING') != 12)

    def testNoExploreInFolderWithoutH5(self):
        self.widget.setH5Exploration(False)
        self.widget.updatePath(self.scanIDWithH5)
        self.assertTrue(self.scanIDWithH5 == self.widget.ftserieReconstruction.scanID)
        self.assertTrue(
            ReconsParam().getValue('FTAXIS', 'OVERSAMPLING') != 12)

    def testNoExploreInFolderWithH5(self):
        self.widget.setH5Exploration(False)
        self.widget.updatePath(self.scanIDWithoutH5)
        self.assertTrue(self.scanIDWithoutH5 == self.widget.ftserieReconstruction.scanID)
        self.assertTrue(
            ReconsParam().getValue('FTAXIS', 'OVERSAMPLING') != 12)


class TestLoadSaveH5File(unittest.TestCase):
    """Simple test that make sure we are able to manage correctly input h5 file
    with the following behavior :
        - if some H5 parameter are missing fron the default set of parameter
        then we are loading the default parameter
        - if the h5 file as some extra H5 parameter or structure then the
        editor should also store them.
    """
    def setUp(self):
        super(TestLoadSaveH5File, self).setUp()
        self.scanID = tempfile.mkdtemp()
        self.ft = FastSetupAll()
        self.file = os.path.join(self.scanID, 'octave_FT_params.h5')

    def tearFown(self):
        del self.ft
        del self.file
        if os.path.isdir(self.scanID):
            shutil.rmtree(self.scanID)
        super(TestLoadSaveH5File, self).tearDown()

    def loadAndSave(self):
        # save actual FastSetup status
        self.ft.writeAll(self.file, 3.8)

        # create FTSerie, load and save dataparamValue = self.getDefaultValue(param)
        widgetWithout = FtseriesWidget()
        widgetWithout.setAttribute(qt.Qt.WA_DeleteOnClose)

        widgetWithout.setH5Exploration(True)
        widgetWithout.updatePath(self.scanID)
        widgetWithout.save(self.file)
        widgetWithout.close()
        # then get back what FTSerie has saved
        loader = FastSetupAll()
        loader.readAll(self.file, targetted_octave_version=3.8)
        return loader.structures

    def testDefaultFileWithMissingParameters(self):
        """Make sure the FastSetupDefaultGlobals.readAll function is
        correctly setting values to missing parameters"""
        # remove a full structure
        self.assertTrue('VOLSELECT' in self.ft.defaultValues['FT'])
        del self.ft.structures['FTAXIS']
        # remove one parameter of the FT structure
        del self.ft.structures['FT']['VOLSELECT']
        # change value of one element of the FT structure
        assert(self.ft.structures['FT']['RINGSCORRECTION'] == 0)
        self.ft.structures['FT']['RINGSCORRECTION'] = 1

        savedData = self.loadAndSave()
        self.assertTrue('FTAXIS' in savedData)
        self.assertTrue(savedData['FTAXIS'] == self.ft.defaultValues['FTAXIS'])
        self.assertTrue('VOLSELECT' in savedData['FT'])
        self.assertTrue('VOLSELECT' in self.ft.defaultValues['FT'])
        self.assertTrue(
            savedData['FT']['VOLSELECT'] == self.ft.defaultValues['FT']['VOLSELECT'])
        self.assertTrue(savedData['FT']['RINGSCORRECTION'] == 1)

    def testDefaultFileWithExtraParameters(self):
        self.ft.structures['TEST'] = {'PARAM1': 1, 'PARAM2': 'dsadsa'}
        self.ft.structures['FT']['PARAMTATA'] = 56.3

        savedData = self.loadAndSave()
        self.assertTrue('PARAMTATA' in savedData['FT'])
        self.assertTrue(savedData['FT']['PARAMTATA'] == 56.3)


class TestSync(unittest.TestCase):
    """Make sure all the tab from the editor are correctly sync with
    :class:`ReconsParam` instance"""
    def setUp(self):
        self.widget = FtseriesWidget()
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        fsdg = FastSetupAll()
        ReconsParam().setStructs(fsdg.defaultValues)

    def tearDown(self):
        self.widget.close()

    def testFTRead(self):
        """Make sure modifications from the ReconsParam are take into account
        """
        ftWidget = self.widget.getFileEditor()._mainWidget
        assert(ReconsParam().params['FT']['DO_TEST_SLICE'] == 1)
        ReconsParam().setValue(structID='FT',
                                           paramID='DO_TEST_SLICE',
                                           value=0)
        self.assertFalse(ftWidget._qcbDoTestSlice.isChecked())

        assert(ReconsParam().params['FT']['FIXEDSLICE'] == 'middle')
        ReconsParam().setValue(structID='FT',
                                           paramID='FIXEDSLICE',
                                           value='on radio')
        self.assertTrue(ftWidget._qcbSelectSlice.currentText() == 'on radio')

        assert(ReconsParam().params['FT']['CORRECT_SPIKES_THRESHOLD'] == 0.04)
        ReconsParam().setValue(structID='FT',
                                           paramID='CORRECT_SPIKES_THRESHOLD',
                                           value=1.23)
        self.assertTrue(float(ftWidget._qleThresholdSpikesRm.text()) == 1.23)

        assert(ReconsParam().params['FT']['RINGSCORRECTION'] == 0)
        ReconsParam().setValue(structID='FT',
                                           paramID='RINGSCORRECTION',
                                           value=1)
        self.assertTrue(ftWidget._qcbRingsCorrection.isChecked())

        assert(ReconsParam().params['FT']['VOLSELECTION_REMEMBER'] == 0)
        ReconsParam().setValue(structID='FT',
                                           paramID='VOLSELECTION_REMEMBER',
                                           value=1)
        self.assertTrue(ftWidget._qcbVolSelRemenber.isChecked())

        assert(ReconsParam().params['FT']['VOLSELECT'] == 'total')
        ReconsParam().setValue(structID='FT',
                                           paramID='VOLSELECT',
                                           value='graphics')
        self.assertTrue(ftWidget._qcbVolumeSelection.currentText() == 'graphics')

    def testFTWrite(self):
        """Make sure user modification from the gui are updating the
        :class:`ReconsParam` instance"""
        ftWidget = self.widget.getFileEditor()._mainWidget

        assert(ReconsParam().params['FT']['DO_TEST_SLICE'] == 1)
        ftWidget._qcbDoTestSlice.setChecked(False)
        self.assertTrue(ReconsParam().getValue(structID='FT',
                                                           paramID='DO_TEST_SLICE') == 0)
        assert(ReconsParam().params['FT']['FIXEDSLICE'] == 'middle')

        iOnRadio = ftWidget._qcbSelectSlice.findText('on radio')
        assert iOnRadio >= 0
        ftWidget._qcbSelectSlice.setCurrentIndex(iOnRadio)
        self.assertTrue(ReconsParam().params['FT']['FIXEDSLICE'] == 'on radio')
        self.assertTrue(ftWidget._qleSliceN.isVisible() is False)

        ftWidget._qleSliceN.setText('4')
        iRowN = ftWidget._qcbSelectSlice.findText('row n')
        assert iRowN >= 0
        ftWidget._qcbSelectSlice.setCurrentIndex(iRowN)
        self.assertTrue(ReconsParam().params['FT']['FIXEDSLICE'] == '4')

        assert(ReconsParam().params['FT']['VOLOUTFILE'] == 0)
        ReconsParam().setValue(structID='FT',
                                           paramID='VOLOUTFILE',
                                           value=0)
        ftWidget._setSingleVolOrStack(1)
        self.assertTrue(ReconsParam().getValue(structID='FT',
                                                           paramID='VOLOUTFILE') == 1)

        assert(ReconsParam().params['FT']['CORRECT_SPIKES_THRESHOLD'] == 0.04)
        ftWidget._setSpikeThreshold(1.12)
        ftWidget._qleThresholdSpikesRm.editingFinished.emit()
        self.assertTrue(ReconsParam().getValue(structID='FT', paramID='CORRECT_SPIKES_THRESHOLD') == 1.12)
        ftWidget._grpThreshold.setChecked(False)
        self.assertTrue(ReconsParam().getValue(structID='FT', paramID='CORRECT_SPIKES_THRESHOLD') == 'Inf')

        assert(ReconsParam().params['FT']['RINGSCORRECTION'] == 0)
        ftWidget._qcbRingsCorrection.setChecked(True)
        self.assertTrue(ReconsParam().getValue(structID='FT', paramID='RINGSCORRECTION') == 1)

        assert(ReconsParam().params['FT']['VOLSELECTION_REMEMBER'] == 0)
        ftWidget._qcbVolSelRemenber.setChecked(True)
        self.assertTrue(ReconsParam().params['FT']['VOLSELECTION_REMEMBER'] == 1)

        assert(ReconsParam().params['FT']['VOLSELECT'] == 'total')
        iSel = ftWidget._qcbVolumeSelection.findText('manual')
        assert iSel >= 0
        ftWidget._qcbVolumeSelection.setCurrentIndex(iSel)
        assert(ReconsParam().params['FT']['VOLSELECT'] == 'manual')

    def testFTAxisRead(self):
        ftAxisWidget = self.widget.getFileEditor()._axisWidget

        assert(ReconsParam().params['FTAXIS']['COR_POSITION'] == 0)
        self.assertTrue(ftAxisWidget._qrbCOR_0_180.isChecked())
        ReconsParam().setValue(structID='FTAXIS',
                                           paramID='COR_POSITION',
                                           value=1)
        self.assertTrue(ftAxisWidget._qrbCOR_90_270.isChecked())

        assert(ReconsParam().params['FTAXIS']['TO_THE_CENTER'] == 1)
        ReconsParam().setValue(structID='FTAXIS',
                                           paramID='TO_THE_CENTER',
                                           value=0)
        self.assertFalse(ftAxisWidget._qcbCenterReconsRegion.isChecked())

        assert(ReconsParam().params['FTAXIS']['FILESDURINGSCAN'] == 0)
        ReconsParam().setValue(structID='FTAXIS',
                                           paramID='FILESDURINGSCAN',
                                           value=1)
        self.assertTrue(ftAxisWidget._qcbuseImgsDuringScan.isChecked())

        assert(ReconsParam().params['FTAXIS']['OVERSAMPLING'] == 4)
        ReconsParam().setValue(structID='FTAXIS',
                                           paramID='OVERSAMPLING',
                                           value=12)
        self.assertTrue(ftAxisWidget._qsbOversampling.value() == 12)

        assert(ReconsParam().params['FTAXIS']['POSITION'] == 'accurate')
        ReconsParam().setValue(structID='FTAXIS',
                                           paramID='POSITION',
                                           value='near')
        self.assertTrue(ftAxisWidget._qcbPosition.currentText() == 'near')

        assert(ReconsParam().params['FTAXIS']['POSITION_VALUE'] == 0.0)
        ReconsParam().setValue(structID='FTAXIS',
                                           paramID='POSITION_VALUE',
                                           value=2.3)
        self.assertTrue(ftAxisWidget._qlePositionValue.text() == '2.3')

        assert(ReconsParam().params['FTAXIS']['PLOTFIGURE'] == 1)
        ReconsParam().setValue(structID='FTAXIS',
                                           paramID='PLOTFIGURE',
                                           value=0)
        self.assertFalse(ftAxisWidget._qcbPlotFigure.isChecked())

        assert(ReconsParam().params['FTAXIS']['HA'] == 1)
        ReconsParam().setValue(structID='FTAXIS',
                                           paramID='HA',
                                           value=0)
        self.assertFalse(ftAxisWidget._qcbHA.isChecked())

        assert(ReconsParam().params['FT']['HALF_ACQ'] == 0)
        ReconsParam().setValue(structID='FT',
                                           paramID='HALF_ACQ',
                                           value=1)
        self.assertTrue(ftAxisWidget._qcbHalfAcq.isChecked())

        assert(ReconsParam().params['FT']['FORCE_HALF_ACQ'] == 0)
        ReconsParam().setValue(structID='FT',
                                           paramID='FORCE_HALF_ACQ',
                                           value=1)
        self.assertTrue(ftAxisWidget._qcbForceHA.isChecked())

    def testFTAxisWrite(self):
        ftAxisWidget = self.widget.getFileEditor()._axisWidget

        assert(ReconsParam().params['FTAXIS']['COR_POSITION'] == 0)
        ftAxisWidget._qrbCOR_90_270.setChecked(True)
        self.assertTrue(ReconsParam().params['FTAXIS']['COR_POSITION'] == 1)

        assert(ReconsParam().params['FTAXIS']['TO_THE_CENTER'] == 1)
        ftAxisWidget._qcbCenterReconsRegion.setChecked(False)
        self.assertTrue(ReconsParam().params['FTAXIS']['TO_THE_CENTER'] == 0)

        assert(ReconsParam().params['FTAXIS']['FILESDURINGSCAN'] == 0)
        ftAxisWidget._qcbuseImgsDuringScan.setChecked(True)
        self.assertTrue(ReconsParam().params['FTAXIS']['FILESDURINGSCAN'] == 1)

        assert(ReconsParam().params['FTAXIS']['POSITION'] == 'accurate')
        iPos = ftAxisWidget._qcbPosition.findText('near')
        assert iPos >= 0
        ftAxisWidget._qcbPosition.setCurrentIndex(iPos)
        self.assertTrue(ReconsParam().params['FTAXIS']['POSITION'] == 'near')

        assert(ReconsParam().params['FTAXIS']['POSITION_VALUE'] == 0.0)
        ftAxisWidget._qlePositionValue.setText('2.3')
        ftAxisWidget._qlePositionValue.editingFinished.emit()
        self.assertTrue(ReconsParam().params['FTAXIS']['POSITION_VALUE'] == 2.3)

        assert(ReconsParam().params['FTAXIS']['PLOTFIGURE'] == 1)
        ftAxisWidget._qcbPlotFigure.setChecked(False)
        self.assertTrue(ReconsParam().params['FTAXIS']['PLOTFIGURE'] == 0)

        assert(ReconsParam().params['FTAXIS']['HA'] == 1)
        ftAxisWidget._qcbHA.setChecked(False)
        self.assertTrue(ReconsParam().params['FTAXIS']['HA'] == 0)

        assert(ReconsParam().params['FT']['HALF_ACQ'] == 0)
        ftAxisWidget._qcbHalfAcq.setChecked(True)
        self.assertTrue(ReconsParam().params['FT']['HALF_ACQ'] == 1)

        assert(ReconsParam().params['FT']['FORCE_HALF_ACQ'] == 0)
        ftAxisWidget._qcbForceHA.setChecked(True)
        self.assertTrue(ReconsParam().params['FT']['FORCE_HALF_ACQ'] == 1)

    def testDisplayRead(self):
        ftAxisWidget = self.widget.getFileEditor()._displayWidget

        assert(ReconsParam().params['FT']['SHOWPROJ'] == 0)
        ReconsParam().setValue(structID='FT',
                                           paramID='SHOWPROJ',
                                           value=1)
        self.assertTrue(ftAxisWidget._qcbShowProj.isChecked())

        assert(ReconsParam().params['FT']['SHOWSLICE'] == 1)
        ReconsParam().setValue(structID='FT',
                                           paramID='SHOWSLICE',
                                           value=0)
        self.assertFalse(ftAxisWidget._qcbShowSlice.isChecked())

        assert(ReconsParam().params['FT']['ANGLE_OFFSET'] == 0)
        assert(ReconsParam().params['FT']['ANGLE_OFFSET_VALUE'] == 0.0)
        ReconsParam().setValue(structID='FT',
                                           paramID='ANGLE_OFFSET_VALUE',
                                           value=2.3)
        self.assertTrue(ftAxisWidget._qleAngleOffset.text() == '2.3')

    def testDisplayWrite(self):
        displayWidget = self.widget.getFileEditor()._displayWidget

        assert(ReconsParam().params['FT']['SHOWPROJ'] == 0)
        displayWidget._qcbShowProj.setChecked(True)
        self.assertTrue(ReconsParam().params['FT']['SHOWPROJ'] == 1)

        assert(ReconsParam().params['FT']['SHOWSLICE'] == 1)
        displayWidget._qcbShowSlice.setChecked(False)
        self.assertTrue(ReconsParam().params['FT']['SHOWSLICE'] == 0)

        assert(ReconsParam().params['FT']['ANGLE_OFFSET'] == 0)
        assert(ReconsParam().params['FT']['ANGLE_OFFSET_VALUE'] == 0.0)
        displayWidget._qleAngleOffset.setText('2.3')
        displayWidget._qleAngleOffset.editingFinished.emit()
        assert(ReconsParam().params['FT']['ANGLE_OFFSET'] == 1.0)
        assert(ReconsParam().params['FT']['ANGLE_OFFSET_VALUE'] == 2.3)
        displayWidget._qleAngleOffset.setText('0.0')
        displayWidget._qleAngleOffset.editingFinished.emit()
        assert(ReconsParam().params['FT']['ANGLE_OFFSET'] == 0)
        assert(ReconsParam().params['FT']['ANGLE_OFFSET_VALUE'] == 0.0)

    def testPaganinRead(self):
        pagWidget = self.widget.getFileEditor()._PaganinWidget

        assert(ReconsParam().params['PAGANIN']['MODE'] == 0)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='MODE',
                                           value=3)
        self.assertTrue(pagWidget._qcbpaganin.currentText() == 'multi')

        assert(ReconsParam().params['PAGANIN']['DB'] == 500.)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='DB',
                                           value=2.3)
        self.assertTrue(pagWidget._qleSigmaBeta.text() == '2.3')

        assert(ReconsParam().params['PAGANIN']['DB2'] == 100.)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='DB2',
                                           value=3.6)
        self.assertTrue(pagWidget._qleSigmaBeta2.text() == '3.6')

        assert(ReconsParam().params['PAGANIN']['UNSHARP_COEFF'] == 3.0)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='UNSHARP_COEFF',
                                           value=2.6)
        self.assertTrue(pagWidget._unsharp_sigma_coeff.text() == '2.6')

        assert(ReconsParam().params['PAGANIN']['UNSHARP_SIGMA'] == 0.8)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='UNSHARP_SIGMA',
                                           value=1.0)
        self.assertTrue(pagWidget._unsharp_sigma_mask_value.text() == '1.0')

        assert(ReconsParam().params['PAGANIN']['THRESHOLD'] == 500.0)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='THRESHOLD',
                                           value=1.0)
        self.assertTrue(pagWidget._qleThreshold.text() == '1.0')

        assert(ReconsParam().params['PAGANIN']['DILATE'] == 2)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='DILATE',
                                           value=1)
        self.assertTrue(pagWidget._qleDilatation.text() == '1')

        assert(ReconsParam().params['PAGANIN']['MEDIANR'] == 4)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='MEDIANR',
                                           value=1)
        self.assertTrue(pagWidget._qleMedianFilterSize.text() == '1')

        assert(ReconsParam().params['PAGANIN']['MKEEP_BONE'] == 0)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='MKEEP_BONE',
                                           value=1)
        self.assertTrue(pagWidget._qcbKeepBone.isChecked())

        assert(ReconsParam().params['PAGANIN']['MKEEP_SOFT'] == 0)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='MKEEP_SOFT',
                                           value=1)
        self.assertTrue(pagWidget._qcbKeepSoft.isChecked())

        assert(ReconsParam().params['PAGANIN']['MKEEP_ABS'] == 0)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='MKEEP_ABS',
                                           value=1)
        self.assertTrue(pagWidget._qcbKeepAbs.isChecked())

        assert(ReconsParam().params['PAGANIN']['MKEEP_CORR'] == 0)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='MKEEP_CORR',
                                           value=1)
        self.assertTrue(pagWidget._qcbKeepCorr.isChecked())

        assert(ReconsParam().params['PAGANIN']['MKEEP_MASK'] == 0)
        ReconsParam().setValue(structID='PAGANIN',
                                           paramID='MKEEP_MASK',
                                           value=1)
        self.assertTrue(pagWidget._qcbKeepMask.isChecked())

    def testPaganinWrite(self):
        pagWidget = self.widget.getFileEditor()._PaganinWidget

        iMulti = pagWidget._qcbpaganin.findText('multi')
        assert iMulti >= 0
        pagWidget._qcbpaganin.setCurrentIndex(iMulti)
        self.assertTrue(ReconsParam().params['PAGANIN']['MODE'] == 3)

        assert(ReconsParam().params['PAGANIN']['DB'] == 500.)
        pagWidget._qleSigmaBeta.setText('2.3')
        pagWidget._qleSigmaBeta.editingFinished.emit()
        assert(ReconsParam().params['PAGANIN']['DB'] == 2.3)

        assert(ReconsParam().params['PAGANIN']['DB2'] == 100.)
        pagWidget._qleSigmaBeta2.setText('3.6')
        pagWidget._qleSigmaBeta2.editingFinished.emit()
        assert(ReconsParam().params['PAGANIN']['DB2'] == 3.6)

        assert(ReconsParam().params['PAGANIN']['UNSHARP_COEFF'] == 3.0)
        pagWidget._unsharp_sigma_coeff.setText('1.2')
        pagWidget._unsharp_sigma_coeff.editingFinished.emit()
        assert(ReconsParam().params['PAGANIN']['UNSHARP_COEFF'] == 1.2)

        assert(ReconsParam().params['PAGANIN']['UNSHARP_SIGMA'] == 0.8)
        pagWidget._unsharp_sigma_mask_value.setText('1.0')
        pagWidget._unsharp_sigma_mask_value.editingFinished.emit()
        assert(ReconsParam().params['PAGANIN']['UNSHARP_SIGMA'] == 1.0)

        assert(ReconsParam().params['PAGANIN']['THRESHOLD'] == 500.0)
        pagWidget._qleThreshold.setText('1.0')
        pagWidget._qleThreshold.editingFinished.emit()
        assert(ReconsParam().params['PAGANIN']['THRESHOLD'] == 1.0)

        assert(ReconsParam().params['PAGANIN']['DILATE'] == 2)
        pagWidget._qleDilatation.setText('1')
        pagWidget._qleDilatation.editingFinished.emit()
        assert(ReconsParam().params['PAGANIN']['DILATE'] == 1)

        assert(ReconsParam().params['PAGANIN']['MEDIANR'] == 4)
        pagWidget._qleMedianFilterSize.setText('1')
        pagWidget._qleMedianFilterSize.editingFinished.emit()
        assert(ReconsParam().params['PAGANIN']['MEDIANR'] == 1)

        assert(ReconsParam().params['PAGANIN']['MKEEP_BONE'] == 0)
        pagWidget._qcbKeepBone.setChecked(True)
        assert(ReconsParam().params['PAGANIN']['MKEEP_BONE'] == 1)

        assert(ReconsParam().params['PAGANIN']['MKEEP_SOFT'] == 0)
        pagWidget._qcbKeepSoft.setChecked(True)
        assert(ReconsParam().params['PAGANIN']['MKEEP_SOFT'] == 1)

        assert(ReconsParam().params['PAGANIN']['MKEEP_ABS'] == 0)
        pagWidget._qcbKeepAbs.setChecked(True)
        assert(ReconsParam().params['PAGANIN']['MKEEP_ABS'] == 1)

        assert(ReconsParam().params['PAGANIN']['MKEEP_CORR'] == 0)
        pagWidget._qcbKeepCorr.setChecked(True)
        assert(ReconsParam().params['PAGANIN']['MKEEP_CORR'] == 1)

        assert(ReconsParam().params['PAGANIN']['MKEEP_MASK'] == 0)
        pagWidget._qcbKeepMask.setChecked(True)
        assert(ReconsParam().params['PAGANIN']['MKEEP_MASK'] == 1)

    def testPyHSTRead(self):
        pyHSTWidget = self.widget.getFileEditor()._PyHSTWidget

        assert(ReconsParam().params['PYHSTEXE']['VERBOSE'] == 0)
        ReconsParam().setValue(structID='PYHSTEXE',
                                           paramID='VERBOSE',
                                           value=1)
        self.assertTrue(pyHSTWidget._qcbverbose.isChecked())

        assert(ReconsParam().params['PYHSTEXE']['EXE'] == 'pyhst2')
        ReconsParam().setValue(structID='PYHSTEXE',
                                           paramID='EXE',
                                           value='pyhst3')
        self.assertTrue(pyHSTWidget._qcbPyHSTVersion.currentText() == 'pyhst3')

        assert(ReconsParam().params['PYHSTEXE']['OFFV'] == 'pyhst2')
        ReconsParam().setValue(structID='PYHSTEXE',
                                           paramID='OFFV',
                                           value='pyhst3')
        self.assertTrue(pyHSTWidget._qlOfficalVersion.text() == 'pyhst3')

        assert(ReconsParam().params['PYHSTEXE']['VERBOSE_FILE'] == 'pyhst_out.txt')
        ReconsParam().setValue(structID='PYHSTEXE',
                                           paramID='VERBOSE_FILE',
                                           value='outToto.dsad')
        self.assertTrue(pyHSTWidget._qleVerboseFile.text() == 'outToto.dsad')

    def testPyHSTWrite(self):
        pyHSTWidget = self.widget.getFileEditor()._PyHSTWidget

        assert(ReconsParam().params['PYHSTEXE']['VERBOSE'] == 0)
        pyHSTWidget._qcbverbose.setChecked(True)
        assert(ReconsParam().params['PYHSTEXE']['VERBOSE'] == 1)

        assert(ReconsParam().params['PYHSTEXE']['EXE'] == 'pyhst2')
        pyHSTWidget._qcbPyHSTVersion.addItem('pyhst3Toto')
        pyHSTWidget._qcbPyHSTVersion.setCurrentIndex(pyHSTWidget._qcbPyHSTVersion.count() - 1)
        assert(ReconsParam().params['PYHSTEXE']['EXE'] == 'pyhst3Toto')

        assert(ReconsParam().params['PYHSTEXE']['VERBOSE_FILE'] == 'pyhst_out.txt')
        pyHSTWidget._qleVerboseFile.setText('outFile.dsad')
        pyHSTWidget._qleVerboseFile.editingFinished.emit()
        assert(ReconsParam().params['PYHSTEXE']['VERBOSE_FILE'] == 'outFile.dsad')

    def testBeamGeoRead(self):
        beamGeoWidget = self.widget.getFileEditor()._beamGeoWidget

        assert(ReconsParam().params['BEAMGEO']['TYPE'] == 'p')
        ReconsParam().setValue(structID='BEAMGEO',
                                           paramID='TYPE',
                                           value='f')
        self.assertTrue(beamGeoWidget._qcbType.currentText() == 'fan beam')

        assert(ReconsParam().params['BEAMGEO']['SX'] == 0.)
        ReconsParam().setValue(structID='BEAMGEO',
                                           paramID='SX',
                                           value=10.2)
        assert(ReconsParam().params['BEAMGEO']['SX'] == 10.2)
        self.assertTrue(beamGeoWidget._qleSX.text() == '10.2')

        assert(ReconsParam().params['BEAMGEO']['SY'] == 0.)
        ReconsParam().setValue(structID='BEAMGEO',
                                           paramID='SY',
                                           value=20.2)
        self.assertTrue(beamGeoWidget._qleSY.text() == '20.2')

        assert(ReconsParam().params['BEAMGEO']['DIST'] == 55.)
        ReconsParam().setValue(structID='BEAMGEO',
                                           paramID='DIST',
                                           value=1.0)
        self.assertTrue(beamGeoWidget._qleDIST.text() == '1.0')

    def testBeamGeoWrite(self):
        beamGeoWidget = self.widget.getFileEditor()._beamGeoWidget

        assert(ReconsParam().params['BEAMGEO']['TYPE'] == 'p')
        iType = beamGeoWidget._qcbType.findText('fan beam')
        assert iType >= 0
        beamGeoWidget._qcbType.setCurrentIndex(iType)
        assert(ReconsParam().params['BEAMGEO']['TYPE'] == 'f')

        assert(ReconsParam().params['BEAMGEO']['SX'] == 0.)
        beamGeoWidget._qleSX.setText('10.2')
        beamGeoWidget._qleSX.editingFinished.emit()
        assert(ReconsParam().params['BEAMGEO']['SX'] == 10.2)

        assert(ReconsParam().params['BEAMGEO']['SY'] == 0.)
        beamGeoWidget._qleSY.setText('11.2')
        beamGeoWidget._qleSY.editingFinished.emit()
        assert(ReconsParam().params['BEAMGEO']['SY'] == 11.2)

        assert(ReconsParam().params['BEAMGEO']['DIST'] == 55.)
        beamGeoWidget._qleDIST.setText('0.2')
        beamGeoWidget._qleDIST.editingFinished.emit()
        assert(ReconsParam().params['BEAMGEO']['DIST'] == 0.2)

    def testExpertRead(self):
        expertWidget = self.widget.getFileEditor()._expertWidget

        assert(ReconsParam().params['FT']['NUM_PART'] == 4)
        ReconsParam().setValue(structID='FT',
                                           paramID='NUM_PART',
                                           value=2)
        self.assertTrue(expertWidget._qsbNumPart.value() == 2)

        assert(ReconsParam().params['FT']['VERSION'] == 'fastomo3 3.2')
        ReconsParam().setValue(structID='FT',
                                           paramID='VERSION',
                                           value='toto')
        self.assertTrue(expertWidget._qleVersion.text() == 'toto')

        assert(ReconsParam().params['FT']['DATABASE'] == 0)
        ReconsParam().setValue(structID='FT',
                                           paramID='DATABASE',
                                           value=1)
        self.assertTrue(expertWidget._qcbDataBase.isChecked())

        assert(ReconsParam().params['FT']['NO_CHECK'] == 0)
        ReconsParam().setValue(structID='FT',
                                           paramID='NO_CHECK',
                                           value=1)
        self.assertTrue(expertWidget._qcbNocheck.isChecked())

        assert(ReconsParam().params['FT']['ZEROOFFMASK'] == 1)
        ReconsParam().setValue(structID='FT',
                                           paramID='ZEROOFFMASK',
                                           value=0)
        self.assertFalse(expertWidget._qcbZeroRegionMask.isChecked())

        assert(ReconsParam().params['FT']['FIXHD'] == 0)
        ReconsParam().setValue(structID='FT',
                                           paramID='FIXHD',
                                           value=1)
        self.assertTrue(expertWidget._qcbFixHD.isChecked())

    def testExpertWrite(self):
        expertWidget = self.widget.getFileEditor()._expertWidget

        assert(ReconsParam().params['FT']['NUM_PART'] == 4)
        expertWidget._qsbNumPart.setValue(2)
        assert(ReconsParam().params['FT']['NUM_PART'] == 2)

        assert(ReconsParam().params['FT']['DATABASE'] == 0)
        expertWidget._qcbDataBase.setChecked(True)
        assert(ReconsParam().params['FT']['DATABASE'] == 1)

        assert(ReconsParam().params['FT']['NO_CHECK'] == 0)
        expertWidget._qcbNocheck.setChecked(True)
        assert(ReconsParam().params['FT']['NO_CHECK'] == 1)

        assert(ReconsParam().params['FT']['ZEROOFFMASK'] == 1)
        expertWidget._qcbZeroRegionMask.setChecked(False)
        assert(ReconsParam().params['FT']['ZEROOFFMASK'] == 0)

        assert(ReconsParam().params['FT']['FIXHD'] == 0)
        expertWidget._qcbFixHD.setChecked(True)
        assert(ReconsParam().params['FT']['FIXHD'] == 1)

    def testOtherRead(self):
        ReconsParam().setValue(structID='FT',
                                           paramID='MYPARAM',
                                           value='tata')
        otherWidget = self.widget.getFileEditor()._otherWidget

        widgetTata = otherWidget.paramToWidget['FT']['MYPARAM']
        assert(widgetTata.text() == 'tata')
        ReconsParam().setValue(structID='FT',
                                           paramID='MYPARAM',
                                           value='toto')
        otherWidget = self.widget.getFileEditor()._otherWidget
        widgetTata = otherWidget.paramToWidget['FT']['MYPARAM']
        self.assertTrue(widgetTata.text() == 'toto')

    def testOtherWrite(self):

        ReconsParam().setValue(structID='FT',
                                           paramID='MYPARAM',
                                           value='tata')
        otherWidget = self.widget.getFileEditor()._otherWidget
        widgetTata = otherWidget.paramToWidget['FT']['MYPARAM']
        widgetTata.setText('toto')
        ReconsParam().params['FT']['MYPARAM'] = 'toto'


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestControlsFTSeriesWidget, TestFTSerieWidget,
               TestExploreDatasetForH5, TestLoadSaveH5File, TestSync):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
