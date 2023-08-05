#/*##########################################################################
# Copyright (C) 2016-2017 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
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

__author__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "02/06/2017"

from silx.gui import qt
import numpy
import logging
import os
import fabio
from tomwer.core.utils import ftseriesutils

logger = logging.getLogger(__name__)


class ImageLoaderThread(qt.QThread):
    """Thread used to load an image"""
    def __init__(self, index, filePath):
        """

        :param index: index of the image on the stackplot
        :param filePath: filePath is the file to load on stackplot reference.
                         It can be an .edf file or a .vol file. If this is a
                         vol file then the name is given with the slice z index
                         to be loaded.
        """
        super(qt.QThread, self).__init__()
        self.data = None
        self.refFileName = filePath
        self.fileToLoad = filePath
        if '#z=' in self.fileToLoad:
            self.fileToLoad = self.refFileName.split('#z=')[0]
        self.index = index

    def getData(self):
        if hasattr(self, 'data'):
            return self.data
        else:
            return None

    def run(self):
        if os.path.exists(self.fileToLoad) and os.path.isfile(self.fileToLoad):
            if (self.fileToLoad.lower().endswith('.vol.info') or
                    self.fileToLoad.lower().endswith('.vol')):
                self.data = self._loadVol()
            else:
                try:
                    with fabio.open(self.fileToLoad) as fh:
                        self.data = fh.data
                except:
                    logger.warning(
                        'file %s not longer exists or is empty' % self.fileToLoad)
                    self.data = None
        else:
            logger.warning('file %s not longer exists or is empty' % self.fileToLoad)
            self.data = None

    def _loadVol(self):
        if self.fileToLoad.lower().endswith('.vol.info'):
            infoFile = self.fileToLoad
            rawFile = self.fileToLoad.replace('.vol.info', '.vol')
        else:
            assert self.fileToLoad.lower().endswith('.vol')
            rawFile = self.fileToLoad
            infoFile = self.fileToLoad.replace('.vol', '.vol.info')

        if not os.path.exists(rawFile):
            data = None
            mess = "Can't find raw data file %s associated with %s" % (rawFile, infoFile)
            logger.warning(mess)
        elif not os.path.exists(infoFile):
            mess = "Can't find info file %s associated with %s" % (infoFile, rawFile)
            logger.warning(mess)
            data = None
        else:
            shape = ftseriesutils._getShapeForVolFile(infoFile)
            if None in shape:
                logger.warning(
                    'Fail to retrieve data shape for %s.' % infoFile)
                data = None
            else:
                try:
                    numpy.zeros(shape)
                except MemoryError:
                    data = None
                    logger.warning('Raw file %s is to large for being '
                                   'readed %s' % rawFile)
                else:
                    data = numpy.fromfile(rawFile, dtype=numpy.float32,
                                          count=-1, sep='')
                    try:
                        data = data.reshape(shape)
                    except ValueError:
                        logger.warning('unable to fix shape for raw file %s. '
                                       'Look for information in %s'
                                       '' % (rawFile, infoFile))
                        try:
                            sqr = int(numpy.sqrt(len(data)))
                            print('sqr is %s' % sqr)
                            shape = (1, sqr, sqr)
                            data = data.reshape(shape)
                        except ValueError:
                            logger.info('deduction of shape size for %s failed'
                                        % rawFile)
                            data = None
                        else:
                            logger.warning('try deducing shape size for %s '
                                           'might be an incorrect '
                                           'interpretation' % rawFile)

        return data
