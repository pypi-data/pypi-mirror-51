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

import copy
import logging
import os
import shutil
import tempfile
import unittest
from tomwer.core.ftseries.FastSetupDefineGlobals import FastSetupAll
from tomwer.core.ftseries.ReconstructionStack import _ReconsFtSeriesThread
from tomwer.core.qtApplicationManager import QApplicationManager
from orangecontrib.tomwer.test.OrangeWorkflowTest import OrangeWorflowTest
from tomwer.test.utils import UtilsTest

app = QApplicationManager()
logging.disable(logging.INFO)


class TestScanListFTSerieWorkflow(OrangeWorflowTest):
    """Make sure the reconstruction of the second dataset is executed with the
    correct reconstruction parameters.
    Set up is as following :
        - ScanList contains two datasets. Those dataset can contains or not some .h5
        - FTSerie is activated with or without H5Exploration option
    """

    def setUp(self):
        super(TestScanListFTSerieWorkflow, self).setUp()
        self.inputDir = tempfile.mkdtemp()

        # define reconstruction parameters
        ft = FastSetupAll()
        self.default = copy.deepcopy(ft.structures)
        assert('FT' in ft.structures)
        assert('NUM_PART' in ft.structures['FT'])
        assert(ft.structures['FT']['NUM_PART'] not in (1, 2))
        ft.structures['FT']['NUM_PART'] = 1
        self.st1 = copy.deepcopy(ft.structures)
        ft.structures['FT']['NUM_PART'] = 2
        self.st2 = copy.deepcopy(ft.structures)

    def tearDow(self):
        if os.path.isdir(self.inputDir):
            shutil.rmtree(self.inputDir)
        super(TestScanListFTSerieWorkflow, self).tearDow()

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        nodeScanList = cls.addWidget(cls,
            'orangecontrib.tomwer.widgets.ScanListWidget.ScanListWidget')
        nodeFTSerie = cls.addWidget(cls,
            'orangecontrib.tomwer.widgets.FtseriesWidget.FtseriesWidget')
        cls.processOrangeEvents(cls)

        cls.link(cls, nodeScanList, "data", nodeFTSerie, "data")
        cls.processOrangeEvents(cls)

        cls.scanListWidget = cls.getWidgetForNode(cls, nodeScanList)
        cls.ftserieWidget = cls.getWidgetForNode(cls, nodeFTSerie)
        _ReconsFtSeriesThread.setCopyH5FileReconsIntoFolder(True)

        # Set we only want to simulate the reconstruction
        cls.ftserieWidget.reconsStack.setMockMode(True)

    @classmethod
    def tearDownClass(cls):
        del cls.scanListWidget
        del cls.ftserieWidget
        OrangeWorflowTest.tearDownClass()

    def initData(self, data01H5, data10H5):
        """Init the two datasets and set the given .h5 file if any given
        The order of scanning is always : first dataset01, second dataset10

        :param data01H5: the values of the structures to save as a h5 file.
            Apply on the daset01.
            If None given then no H5 file will be saved
        :param data10H5: the values of the structures to save as a h5 file.
            Apply on the daset10.
            If None given then no H5 file will be saved
        """

        dataDir01 = UtilsTest.getDataset('test01')
        dataDir10 = UtilsTest.getDataset('test10')
        # removing any previous dataset
        self.clearInputFolder()

        # set new dataset
        self.dest01 = os.path.join(self.inputDir, os.path.basename(dataDir01))
        shutil.copytree(src=dataDir01, dst=self.dest01)
        # make sure no h5 exists yet
        for f in os.listdir(dataDir01):
            assert(not f.lower().endswith('.h5'))
        self.dest10 = os.path.join(self.inputDir, os.path.basename(dataDir10))
        for f in os.listdir(dataDir10):
            assert(not f.lower().endswith('.h5'))
        shutil.copytree(src=dataDir10, dst=self.dest10)

        # if needed create some h5 file from structure
        data_and_dir = (data01H5, self.dest01), (data10H5, self.dest10)
        for data, dataDir in data_and_dir:
            if data is not None:
                ft = FastSetupAll()
                ft.structures = data
                path = os.path.join(dataDir, 'reconsH5File.h5')
                ft.writeAll(path, 3.8)

        # update scanList
        self.scanListWidget.clear()
        self.scanListWidget.add(self.dest01)
        self.scanListWidget.add(self.dest10)

    def clearInputFolder(self):
        for subFolder in os.listdir(self.inputDir):
            folder = os.path.join(self.inputDir, subFolder)
            assert(os.path.isdir(folder))
            # should never store something else than a folder
            shutil.rmtree(folder)

    def setH5Exploration(self, b):
        """Activate or not the exploration"""
        self.ftserieWidget.setH5Exploration(b)

    def runAndTestList(self, structures, results, caseMsg):
        """Check that the reconstruction are send in the same order as the list
        is sending them
        """
        # 1.0 processing
        self.initData(structures[0], structures[1])
        self.scanListWidget._sendList()

        # first folder
        self.processOrangeEvents()
        # # second folder
        # self.processOrangeEvents()

        # 2.0 testing
        # check the first dataset is correct
        output01 = os.path.join(self.dest01, _ReconsFtSeriesThread.copyH5ReconsName)
        self.assertTrue(os.path.isfile(output01))
        ft01 = FastSetupAll()
        ft01.readAll(output01, 3.8)

        # with self.subTest(msg=name):
        with self.subTest(msg="test reconstruction parameters used - folder1 : " + caseMsg,
                          value=int(ft01.structures['FT']['NUM_PART']),
                          expected=int(results[0]['FT']['NUM_PART'])):
            self.assertEqual(int(ft01.structures['FT']['NUM_PART']), int(results[0]['FT']['NUM_PART']))
        os.remove(output01)

        # check the second dataset is correct
        output10 = os.path.join(self.dest10, _ReconsFtSeriesThread.copyH5ReconsName)
        self.assertTrue(os.path.isfile(output10))
        ft10 = FastSetupAll()
        ft10.readAll(output10, 3.8)

        with self.subTest(msg="test reconstruction parameters used - folder2 : " + caseMsg,
                          value=ft10.structures['FT']['NUM_PART'],
                          expected=results[1]['FT']['NUM_PART']):
            self.assertTrue(ft10.structures['FT']['NUM_PART'] == results[1]['FT']['NUM_PART'])
        os.remove(output10)

    def getTestMsg(self, ftserieStatus, structures, results):
        """Return the message fitting with the structures we are setting to
        test01 and test10 and to the restul we want"""
        msg = 'FTSerieWidget status : ' + ftserieStatus
        msg += '\nConfiguration of folders : '
        msg += '\n    - Folder 1 contains '
        msg += 'no .h5' if structures[0] is self.default else "h5 with " + ('st1' if structures[0] is self.st1 else 'st2') + " structure"
        msg += '\n    - Folder 2 contains '
        msg += 'no .h5' if structures[1] is self.default else "h5 with " + ('st1' if structures[1] is self.st1 else 'st2') + " structure"
        msg += '\nResults in folder should be :'
        msg += '\n   - for first folder :'
        msg += 'default' if results[0] is self.default else ('st1' if results[0] is self.st1 else 'ft2')
        msg += '\n   - for second folder :'
        msg += 'default' if results[1] is self.default else ('st1' if results[1] is self.st1 else 'ft2')
        return msg


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestScanListFTSerieWorkflow,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite
