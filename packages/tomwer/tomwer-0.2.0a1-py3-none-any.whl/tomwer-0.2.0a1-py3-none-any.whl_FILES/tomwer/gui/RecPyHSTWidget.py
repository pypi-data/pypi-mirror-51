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
"""GUI to call RecPyHST
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "22/01/2017"

from tomwer.core.utils import pyhstutils
from tomwer.core.ReconsParams import ReconsParam
from tomwer.gui.H5StructEditor import H5StructsEditor
import unittest
from silx.gui import qt
import logging

logger = logging.getLogger(__file__)


class RecPyHSTWidget(H5StructsEditor, qt.QWidget):
    """
    Widget to interface the `makeRecPyHST` function
    """
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        H5StructsEditor.__init__(self, structsManaged=('PYHSTEXE', ))
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._buildPyHSTEXE())
        self.layout().addWidget(self._buildMakeOARFile())
        self.load(ReconsParam().params)
        ReconsParam().sigChanged.connect(self._update)

    def _buildPyHSTEXE(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QVBoxLayout())

        exe_widget = qt.QWidget()
        widget.layout().addWidget(exe_widget)
        exe_widget.setLayout(qt.QHBoxLayout())

        # create the PyHST version combobox
        exe_widget.layout().addWidget(
            qt.QLabel("PyHST version : ", parent=exe_widget))
        self._qcbPyHSTVersion = qt.QComboBox(parent=self)
        self.linkComboboxWithH5Variable(self._qcbPyHSTVersion,
                                        structID='PYHSTEXE',
                                        h5ParamName='EXE')
        exe_widget.layout().addWidget(self._qcbPyHSTVersion)
        self._qcbPyHSTVersion.currentIndexChanged.connect(self._pyHSTVersionChanged)

        # try to get the PyHST dir
        d = pyhstutils._getPyHSTDir()
        if d is None:
            logger.warning("""Can't find the directory containing the PyHST
                directory. Please set the environment variable
                PYHST_DIR and run again""")
            d = 'not found'
        else:
            availablePyHSTVersion = pyhstutils._findPyHSTVersions(d)
            if len(availablePyHSTVersion) == 0:
                logger.warning('No valid PyHST version found.')
            else:
                [self._qcbPyHSTVersion.addItem(exe) for exe in availablePyHSTVersion]

        pyhst_dir_widget = qt.QWidget(parent=widget)
        widget.layout().addWidget(pyhst_dir_widget)
        pyhst_dir_widget.setLayout(qt.QHBoxLayout())
        pyhst_dir_widget.layout().addWidget(qt.QLabel('PyHST directory:'))
        pyhst_dir_widget.layout().addWidget(qt.QLabel(d))

        return widget

    def _pyHSTVersionChanged(self):
        if self._isLoading is False:
            value = self._qcbPyHSTVersion.currentText()
            ReconsParam().setValue(structID='PYHSTEXE',
                                               paramID='EXE',
                                               value=value)

    def _buildMakeOARFile(self):
        self._makeOARFileCB = qt.QCheckBox('make OAR file', parent=self)
        self.linkCheckboxWithH5Variable(self._makeOARFileCB, 'PYHSTEXE',
                                        'MAKE_OAR_FILE', invert=False)
        self._makeOARFileCB.toggled.connect(self._makeOARChanged)

        return self._makeOARFileCB

    def _makeOARChanged(self, b):
        if self._isLoading is False:
            ReconsParam().setValue(structID='PYHSTEXE',
                                               paramID='MAKE_OAR_FILE',
                                               value=int(b))

    def _update(self, params=None):
        _params = params
        if _params is None:
            _params = ReconsParam().params
        assert 'PYHSTEXE' in _params
        assert 'EXE' in _params['PYHSTEXE']
        self.load(_params)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (RecPyHSTWidget, ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")