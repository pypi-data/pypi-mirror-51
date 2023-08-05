# coding: utf-8
###########################################################################
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
#############################################################################

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "30/05/2017"

import os
import fabio
import numpy
import logging
import glob
from tomwer.core.darkref.DarkRefs import DarkRefs
from collections import OrderedDict


_logger = logging.getLogger(__file__)


class FtserieReconstruction():
    """"Class that group needed information per validate or not a scan"""

    def __init__(self, scanID, radioList=None, reconstructedScan=None):
        """

        :param scanID: path to the acquisition folder
        :param radioList: list of the radio files
        :param reconstructedScan: list of the reconstruction files
        """
        self.scanID = os.path.abspath(scanID)
        self.radioList = radioList
        self.reconstructedScan = reconstructedScan

    def getDark(self):
        """
        For now only deal with one existing dark file.

        :return: image of the dark if existing. Else None
        """
        # first try to retrieve data from dark.edf file or darkHST.edf files
        data = self._extractFromOneFile('dark.edf', what='dark')
        if data is None:
            data = self._extractFromOneFile('darkHST.edf', what='dark')
        if data is not None:
            return data

        data = self._extractFromPrefix(DarkRefs.DARKHST_PREFIX, what='dark')
        if data is None:
            data = self._extractFromPrefix('darkend', what='dark')
        if data is not None:
            return data

        _logger.warning('Cannot retrieve dark file from %s' % self.scanID)
        return None

    def getFlat(self, projectionI=None):
        """
        If projectionI is not requested then return the mean value. Otherwise
        return the interpolated value for the requested projection.

        :param int or None projectionI:
        :return: Flat field value or None if can't deduce it
        """
        data = self._extractFromOneFile('refHST.edf', what='flat')
        if data is not None:
            return data

        data = self._extractFromPrefix(DarkRefs.REFHST_PREFIX, what='flat',
                                       proI=projectionI)
        if data is not None:
            return data

        _logger.warning('Cannot retrieve flat file from %s' % self.scanID)
        return None

    def _extractFromOneFile(self, f, what):
        path = os.path.join(self.scanID, f)
        if os.path.exists(path):
            _logger.info('Getting %s from %s' % (what, f))
            try:
                data = fabio.open(path).data
            except:
                return None
            else:
                if data.ndim is 2:
                    return data
                elif data.ndim is 3:
                    _logger.warning('%s file contains several images. Taking '
                                    'the mean value' % what)
                    return numpy.mean(data.ndim)
        else:
            return None

    def _extractFromPrefix(self, pattern, what, proI=None):
        files = glob.glob(os.path.join(self.scanID, pattern + '*.edf'))
        if len(files) is 0:
            return None
        else:
            d = {}
            for f in files:
                index = self.guessIndexFromEDFFileName(f)
                if index is None:
                    _logger.error('cannot retrieve projection index for %s'
                                  '' % f)
                    return None
                else:
                    d[index] = fabio.open(f).data

            if len(files) is 1:
                return d[list(d.keys())[0]]

            oProj = OrderedDict(sorted(d.items()))
            # for now we only deal with interpolation between the higher
            # and the lower acquired file ()
            lowPI = list(oProj.keys())[0]
            uppPI = list(oProj.keys())[-1]


            lowPD = oProj[lowPI]
            uppPD = oProj[uppPI]

            if len(oProj) > 2:
                _logger.warning('Only bordering projections (%s and %s) will '
                                'be used for extracting %s' % (lowPI, proI, what))

            uppPI = uppPI
            index = proI
            if index is None:
                index = (uppPI - lowPI) / 2

            if (index >= lowPI) is False:
                index = lowPI
                _logger.warning('ProjectionI not in the files indexes'
                                'range (projectionI >= lowerProjIndex)')

            if (index <= uppPI) is False:
                index = uppPI
                _logger.warning('ProjectionI not in the files indexes'
                                'range upperProjIndex >= projectionI')

            # simple interpolation
            _nRef = (uppPI - lowPI)
            lowPI = lowPI

            w0 = (lowPI + (uppPI - index)) / _nRef
            w1 = index / _nRef

            return (w0 * lowPD + w1 * uppPD)

    @staticmethod
    def guessIndexFromEDFFileName(_file):
        name = _file.rstrip('.edf')
        ic = []
        while name[-1].isdigit():
            ic.append(name[-1])
            name = name[:-1]

        if len(ic) is 0:
            return None
        else:
            orignalOrder = ic[::-1]
            return int(''.join(orignalOrder))
