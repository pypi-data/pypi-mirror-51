#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from silx.gui import qt
import argparse
from tomwer.utils import getMainSplashScreen
from tomwer.core.utils.ftseriesutils import getSampleEvolScan
from tomwer.core.utils.normalization import flatFieldCorrection
from tomwer.core.ftseries.FtserieReconstruction import FtserieReconstruction
from tomwer.gui.samplemoved import SampleMovedWidget
import os

logging.basicConfig()
_logger = logging.getLogger(__file__)


def getinputinfo():
    return "tomwer samplemoved [scanDir]"


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

    splash = getMainSplashScreen()
    widget = SampleMovedWidget()
    options.scan_path = options.scan_path.rstrip(os.path.sep)
    rawSlices = getSampleEvolScan(options.scan_path)
    dark = FtserieReconstruction(options.scan_path).getDark()
    flat = FtserieReconstruction(options.scan_path).getFlat()
    if flat is not None and dark is not None:
        normedSlices = flatFieldCorrection(imgs=rawSlices, dark=dark,
                                           flat=flat)
    else:
        _logger.warning('Cannot find dark and/or flat field for %s.'
                        'Won\'t normalized scans' % options.scan_path)
        normedSlices = rawSlices
    widget.setImages(normedSlices)
    splash.finish(widget)
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
