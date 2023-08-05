#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import os
from silx.gui import qt
import argparse
from tomwer.utils import getMainSplashScreen
from tomwer.gui.SlicesStack import SlicesStack

logging.basicConfig()
_logger = logging.getLogger(__file__)


def getinputinfo():
    return "tomwer ftserie [scanDir]"


def addFolderAndSubFolder(stack, path):
    stack.addLeafScan(path)
    for f in os.listdir(path):
        _path = os.path.join(path, f)
        if os.path.isdir(_path) is True:
            addFolderAndSubFolder(stack, _path)


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'scan_path',
        help='Root dir to browse and to extract all slices files under it.')
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
    widget = SlicesStack()
    options.scan_path = options.scan_path.rstrip(os.path.sep)
    addFolderAndSubFolder(stack=widget, path=options.scan_path)

    splash.finish(widget)
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
