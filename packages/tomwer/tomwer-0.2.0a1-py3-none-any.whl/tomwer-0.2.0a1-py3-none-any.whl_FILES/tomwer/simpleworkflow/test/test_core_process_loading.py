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
__date__ = "29/05/2017"

import os
import tempfile
import unittest
from tomwer.core.FolderTransfert import FolderTransfertP
from tomwer.core.ScanList import ScanListP
from tomwer.core.ScanValidator import ScanValidatorP
from tomwer.core.ftseries.Ftseries import FtseriesP
from tomwer.core.tomodir.TomoDir import TomoDirP
from tomwer.test.utils import UtilsTest
from tomwer.core.ReconsParams import ReconsParam
from ..parser import scheme_load
from ..scheme import _GUIFreeScheme


class TestParser(unittest.TestCase):
    """Test that the parser for the non-gui workflow is able to process on a
    simple scanlist _ folder transfert workflow"""
    @classmethod
    def setUpClass(cls):
        # get the .ows file from the web if needed
        dataSetID = 'owsfiles'
        datafolder = UtilsTest.getDataset(dataSetID)
        assert(os.path.isdir(datafolder))
        cls.datafile = os.path.join(datafolder, 'scanlist_foldertransfert.ows')
        assert(os.path.isfile(cls.datafile))

    def testParsing(self):
        """Make sure we can parse a simple .ows file"""
        scheme = _GUIFreeScheme()
        with open(self.datafile, "rb") as f:
            scheme_load(scheme, f)


class SimpleWorkflow(unittest.TestCase):
    """Test a set of basic workflow and make sure they are correctly executing
    """
    @classmethod
    def setUpClass(cls):
        # get the .ows file from the web if needed
        dataSetID = 'owsfiles'
        cls.datafolder = UtilsTest.getDataset(dataSetID)
        assert(os.path.isdir(cls.datafolder))

    def test_scan_list_transfert(self):
        """Make sure the testscan_list_transfert workflow is correctly executed
        """

        self.datafile = os.path.join(self.datafolder, 'scanlist_foldertransfert.ows')
        assert(os.path.isfile(self.datafile))

        self.folderPath = tempfile.mkdtemp()
        tempfile.mkstemp(suffix=".edf", dir=self.folderPath)
        tempfile.mkstemp(suffix=".edf", dir=self.folderPath)
        self.output = tempfile.mkdtemp()
        scheme = _GUIFreeScheme()
        with open(self.datafile, "rb") as f:
            scheme_load(scheme, f)

        # check scheme
        self.assertTrue(len(scheme.node_by_id) is 2)
        self.assertTrue(len(scheme.links) is 1)
        self.assertTrue(scheme.links[0].source_node_id == '0')
        self.assertTrue(scheme.links[0].sink_node_id == '1')
        self.assertTrue(scheme.links[0].source_channel == "data")
        self.assertTrue(scheme.links[0].sink_channel == "data")

        # check node value
        self.assertTrue(type(scheme.node_by_id['0']) == ScanListP)
        self.assertTrue(type(scheme.node_by_id['1']) == FolderTransfertP)
        self.assertTrue(len(scheme.node_by_id['0']._scanIDs) == 1)
        self.assertTrue(scheme.node_by_id['0']._scanIDs[0] == '/users/payno/tmp/d1')

        self.assertTrue(os.path.isdir(self.folderPath))
        self.assertTrue(len(os.listdir(self.output)) == 0)
        self.assertTrue(len(os.listdir(self.folderPath)) == 2)
        # change folder values
        scheme.node_by_id['0']._scanIDs[0] = self.folderPath
        scheme.node_by_id['1']._forceDestinationDir(self.output)

        # since folder transfert is using tread we should deal with sync
        scheme.node_by_id['1'].setIsBlocking(True)

        # execute it
        scheme.run()

        # test file have been copied
        self.assertFalse(os.path.isdir(self.folderPath))
        self.assertTrue(len(os.listdir(self.output)) == 1)
        odir = os.path.join(self.output, os.path.basename(self.folderPath))
        self.assertTrue(len(os.listdir(odir)) == 2)


class LoadProcess(unittest.TestCase):
    """Test that all basic process are correctly loading
    """
    @classmethod
    def setUpClass(cls):
        # get the .ows file from the web if needed
        dataSetID = 'owsfiles'
        cls.datafolder = UtilsTest.getDataset(dataSetID)
        assert(os.path.isdir(cls.datafolder))

    def test_scanlist(self):
        """test that scanlist process is loading
        """
        self.datafile = os.path.join(self.datafolder, 'scanlist_foldertransfert.ows')
        assert(os.path.isfile(self.datafile))

        self.folderPath = tempfile.mkdtemp()
        tempfile.mkstemp(suffix=".edf", dir=self.folderPath)
        tempfile.mkstemp(suffix=".edf", dir=self.folderPath)
        self.output = tempfile.mkdtemp()
        scheme = _GUIFreeScheme()
        with open(self.datafile, "rb") as f:
            scheme_load(scheme, f)

        # check scheme
        self.assertTrue(len(scheme.node_by_id) is 2)
        self.assertTrue(len(scheme.links) is 1)
        self.assertTrue(scheme.links[0].source_node_id == '0')
        self.assertTrue(scheme.links[0].sink_node_id == '1')
        self.assertTrue(scheme.links[0].source_channel == "data")
        self.assertTrue(scheme.links[0].sink_channel == "data")

        # check node value
        self.assertTrue(type(scheme.node_by_id['0']) == ScanListP)
        self.assertTrue(type(scheme.node_by_id['1']) == FolderTransfertP)
        self.assertTrue(len(scheme.node_by_id['0']._scanIDs) == 1)
        self.assertTrue(scheme.node_by_id['0']._scanIDs[0] == '/users/payno/tmp/d1')

        self.assertTrue(os.path.isdir(self.folderPath))
        self.assertTrue(len(os.listdir(self.output)) == 0)
        self.assertTrue(len(os.listdir(self.folderPath)) == 2)
        # change folder values
        scheme.node_by_id['0']._scanIDs[0] = self.folderPath
        scheme.node_by_id['1']._forceDestinationDir(self.output)

        # since folder transfert is using tread we should deal with sync
        scheme.node_by_id['1'].setIsBlocking(True)

        # execute it
        scheme.run()

        # test file have been copied
        self.assertFalse(os.path.isdir(self.folderPath))
        self.assertTrue(len(os.listdir(self.output)) == 1)
        odir = os.path.join(self.output, os.path.basename(self.folderPath))
        self.assertTrue(len(os.listdir(odir)) == 2)

    def test_datatransfert(self):
        """test that scanlist process is loading
        """

        self.datafile = os.path.join(self.datafolder, 'datatransfert.ows')
        assert(os.path.isfile(self.datafile))

        self.output = tempfile.mkdtemp()
        scheme = _GUIFreeScheme()
        with open(self.datafile, "rb") as f:
            scheme_load(scheme, f)

        # check scheme
        self.assertTrue(len(scheme.node_by_id) is 1)
        self.assertTrue(len(scheme.links) is 0)

        # check node value
        self.assertTrue(type(scheme.node_by_id['0']) == FolderTransfertP)

    def test_ftseries(self):
        """Make sure the ftseries process is correctling loading"""
        self.datafile = os.path.join(self.datafolder,
                                     'ftserie.ows')

        scheme = _GUIFreeScheme()
        with open(self.datafile, "rb") as f:
            scheme_load(scheme, f)

        self.assertTrue(len(scheme.node_by_id) == 1)
        self.assertTrue(type(scheme.node_by_id['0']) == FtseriesP)
        self.assertTrue(ReconsParam().params['BEAMGEO']['SX'] == 40.0)
        self.assertTrue(ReconsParam().params['FTAXIS']['OVERSAMPLING'] == 10)

    def test_tomodir(self):
        """Make sure the tomodir process is correctly loading"""
        self.datafile = os.path.join(self.datafolder,
                                     'tomodir.ows')

        scheme = _GUIFreeScheme()
        with open(self.datafile, "rb") as f:
            scheme_load(scheme, f)

        self.assertTrue(len(scheme.node_by_id) == 1)
        self.assertTrue(type(scheme.node_by_id['0']) == TomoDirP)

    def test_scan_validator(self):
        """Make sure the scan validator process is correctly loading"""
        self.datafile = os.path.join(self.datafolder,
                                     'scan_validator.ows')

        scheme = _GUIFreeScheme()
        with open(self.datafile, "rb") as f:
            scheme_load(scheme, f)

        self.assertTrue(len(scheme.node_by_id) == 1)
        self.assertTrue(type(scheme.node_by_id['0']) == ScanValidatorP)

    def test_image_stack_viewer(self):
        """Make sure the image stack viewer is ignored"""
        self.datafile = os.path.join(self.datafolder,
                                     'image_stack_viewer.ows')

        scheme = _GUIFreeScheme()
        with open(self.datafile, "rb") as f:
            scheme_load(scheme, f)

        # the scheme should be empty because the image_stack_viewer is ignored
        self.assertTrue(len(scheme.node_by_id) == 0)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestParser, SimpleWorkflow, LoadProcess):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
