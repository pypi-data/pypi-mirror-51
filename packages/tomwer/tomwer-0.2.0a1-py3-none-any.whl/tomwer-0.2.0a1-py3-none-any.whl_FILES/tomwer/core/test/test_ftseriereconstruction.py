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

import unittest
import logging
import tempfile
import numpy
import fabio.edfimage
from tomwer.core.ftseries.FtserieReconstruction import FtserieReconstruction
import shutil
import os

logging.disable(logging.INFO)


class FTSerieReconstructionTest(unittest.TestCase):
    """unit test for the FTSerieReconstruction functions"""
    def setUp(self):
        def saveData(data, _file, folder):
            file_desc = fabio.edfimage.EdfImage(data=data)
            file_desc.write(os.path.join(folder, _file))

        unittest.TestCase.setUp(self)
        self.folderTwoFlats = tempfile.mkdtemp()
        self.folderOneFlat = tempfile.mkdtemp()

        self.darkData = numpy.arange(100).reshape(10, 10)
        self.flatField_0 = numpy.arange(start=10, stop=110).reshape(10, 10)
        self.flatField_600 = numpy.arange(start=-10, stop=90).reshape(10, 10)
        self.flatField = numpy.arange(start=0, stop=100).reshape(10, 10)

        # save configuration one
        saveData(self.darkData, 'darkHST.edf', self.folderTwoFlats)
        saveData(self.flatField_0, 'refHST_0000.edf', self.folderTwoFlats)
        saveData(self.flatField_600, 'refHST_0600.edf', self.folderTwoFlats)

        # save configuration two
        saveData(self.darkData, 'darkHST.edf', self.folderOneFlat)
        saveData(self.flatField, 'refHST.edf', self.folderOneFlat)

        self.acquiOneFlat = FtserieReconstruction(self.folderOneFlat)
        self.acquiTwoFlats = FtserieReconstruction(self.folderTwoFlats)

    def tearDown(self):
        for f in (self.folderOneFlat, self.folderTwoFlats):
            shutil.rmtree(f)
        unittest.TestCase.tearDown(self)

    def testGetDark(self):
        self.assertTrue(numpy.array_equal(
            self.acquiOneFlat.getDark(), self.darkData))
        self.assertTrue(numpy.array_equal(
            self.acquiTwoFlats.getDark(), self.darkData))

    def testGetFlat(self):
        # check one flat file with two ref
        self.assertTrue(
            numpy.array_equal(self.acquiOneFlat.getFlat(), self.flatField))

        # check two flat files
        self.assertTrue(numpy.array_equal(
            self.acquiTwoFlats.getFlat(), numpy.arange(100).reshape(10, 10)))
        self.assertTrue(numpy.array_equal(
            self.acquiTwoFlats.getFlat(projectionI=300), numpy.arange(100).reshape(10, 10)))
        self.assertTrue(numpy.array_equal(
            self.acquiTwoFlats.getFlat(projectionI=600), self.flatField_600))
        self.assertTrue(numpy.array_equal(
            self.acquiTwoFlats.getFlat(projectionI=0), self.flatField_0))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (FTSerieReconstructionTest, ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
