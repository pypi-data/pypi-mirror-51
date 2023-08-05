#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from silx.gui import qt
from tomwer.core.PyHSTCaller import PyHSTCaller
import argparse
from tomwer.gui.RecPyHSTWidget import RecPyHSTWidget

logging.basicConfig()
_logger = logging.getLogger(__file__)


class _RecPyHSTApp(RecPyHSTWidget):
    def __init__(self, parent, dir):
        RecPyHSTWidget.__init__(self, parent)
        self._dir = dir
        self._execButton = qt.QPushButton('execute', parent=self)
        self.layout().addWidget(self._execButton)
        self._execButton.pressed.connect(self._execute)

    def _execute(self):
        recCreator = PyHSTCaller()
        assert recCreator.isvalid()
        recCreator.makeRecFile(dirname=self._dir)


def getinputinfo():
    return "tomwer recpyhst [scanDir]"


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'scan_path',
        help='Data file to show (h5 file, edf files, spec files)')
    parser.add_argument(
        '--debug',
        dest="debug",
        action="store_true",
        default=False,
        help='Set logging system in debug mode')

    options = parser.parse_args(argv[1:])

    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication([])

    widget = _RecPyHSTApp(parent=None, dir=options.scan_path)
    widget.show()
    app.exec_()
    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv)