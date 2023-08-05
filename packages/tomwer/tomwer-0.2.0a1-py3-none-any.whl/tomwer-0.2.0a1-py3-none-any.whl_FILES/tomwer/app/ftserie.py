#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from silx.gui import qt
import argparse
from tomwer.utils import getMainSplashScreen
from tomwer.gui.FTSerie import _FtserieWidget

logging.basicConfig()
_logger = logging.getLogger(__file__)


def getinputinfo():
    return "tomwer ftserie [scanDir]"


def main(argv):
    import os
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

    splash = getMainSplashScreen()
    options.scan_path = options.scan_path.rstrip(os.path.sep)
    widget = _FtserieWidget(dir=options.scan_path)
    splash.finish(widget)
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
