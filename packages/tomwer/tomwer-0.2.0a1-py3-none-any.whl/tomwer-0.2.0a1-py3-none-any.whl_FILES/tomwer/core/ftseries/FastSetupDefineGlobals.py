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

"""This module provides global definitions to prepare fasttomo input as HDF5 file.
of reconstruction parameters structure and should be a mirror of the octave one:
/sware/pub/octave-tomwer/suse82/m/tomotools/DEV/defineGLOBALS.m
"""

__authors__ = ["C. Nemoz", "H.Payno"]
__license__ = "MIT"
__date__ = "25/05/2016"

import os
import logging
import copy
logger = logging.getLogger(__name__)

try:
    from silx.io.octaveh5 import Octaveh5
except ImportError as e:
    logger.error("Module " + __name__ + " requires silx.io.octaveh5")
    raise e


class H5MissingParameters(Exception):
    """Exception launch when some h5 parameters are missing from a structure"""
    def __init__(self, missingStruc, missingVar):
        super(H5MissingParameters, self).__init__()
        self.missingStructures = missingStruc
        self.missingVariables = missingVar

    def __str__(self):
        mess = "File is missing some structures and/or variables."
        mess += "Values of those has been setted to default values. "
        mess += "Please make sure they are correct. Missing structures are "
        mess += " missing variables \n: %s" % self.missingVariables
        mess += " missing structures \n: %s" % self.missingStructures
        return mess


class FastSetupAll(object):
    OFFV = 'pyhst2'
    h5_prefix = 'ftinput_'  # prefix of h5 files to consider it is an octave input

    def __init__(self):
        self.tmph5 = 'octave_input.h5'

        self.resetDefaultStructures()

    def resetDefaultStructures(self):
        self.structures = {}
        self.structures['FT'] = FastSetupAll.getDefaultStructFT()
        self.structures['PYHSTEXE'] = FastSetupAll.getDefaultStructPYHSTEXE()
        self.structures['FTAXIS'] = FastSetupAll.getDefaultStructFTAXIS()
        self.structures['PAGANIN'] = FastSetupAll.getDefaultStructPAGANIN()
        self.structures['BEAMGEO'] = FastSetupAll.getDefaultStructBEAMGEO()
        self.structures['DKRF'] = FastSetupAll.getDefaultStructDKRF()
        self.defaultValues = copy.deepcopy(self.structures)

    def getDefaultValues(self, structID):
        if structID not in self.defaultValues:
            raise ValueError('%s has no default values' % structID)
        else:
            return self.defaultValues[structID]

    def readAll(self, filn, targetted_octave_version):
        if not os.path.isfile(filn):
            raise IOError("given path is not a file %s" % filn)

        reader = Octaveh5(targetted_octave_version).open(filn)
        self.resetDefaultStructures()
        # get minimal groups (existing groups and default groups)
        for st in set(list(reader.file) + list(self.defaultValues.keys())):
            try:
                self.structures[st] = reader.get(st)
            except(KeyError):
                if st in self.structures:
                    logger.warning('%s structure isn\'t existing yet, setting values to default' % st)
                    self.structures[st] = self.defaultValues[st].copy()
                else:
                    raise ValueError('Unable to load structure %s' % st)

        self._check_variables(self.structures)

    def _check_variables(self, structures):
        """Check that all the variables needed in each structure are existing.
        Otherwise set them to default if possible
        """
        success = True
        missingStructures = []
        """Strore all the structures missing in the file"""
        missingVariables = {}
        """Strore all the variables missing in the structure of the file"""
        for structRef in self.defaultValues:
            if structRef not in structures:
                success = False
                missingStructures.append(structRef)
            else:
                for var in self.defaultValues[structRef]:
                    if var not in structures[structRef]:
                        # Do not create problem if a key is missing - set simply the local default
                        logger.info('Parameter %s is missing in the %s '
                                    'structure. Setting to default' % (var, structRef))
                        if structRef not in missingVariables:
                            missingVariables[structRef] = []
                        missingVariables[structRef].append(var)
                        structures[structRef][var] = self.defaultValues[structRef][var]

        if not success:
            raise H5MissingParameters(missingStructures, missingVariables)

    def writeAll(self, filn, targetted_octave_version):
        if os.path.isfile(filn) is True:
            os.remove(filn)

        writer = Octaveh5(targetted_octave_version)
        writer.open(filn, 'a')

        for s in self.structures:
            writer.write(s, self.structures[s])
        writer.close()

    @staticmethod
    def getDefaultStructFT():
        """ Dictionary definitions for the main fasttomo octave structure FT"""
        return {
            'SHOWPROJ': 0,                         # show graphical proj during reconstruction
            'SHOWSLICE': 1,                        # show graphical slice during reconstruction
            'FIXEDSLICE': 'middle',                # which slice to reconstruct
            'VOLOUTFILE': 0,                       # single .vol instead of edf stack
            'HALF_ACQ': 0,                         # Use half acquisition reconstruction
            'FORCE_HALF_ACQ': 0,                   # Force half acquisition even if angle is not 360 (from PyHST 2016c)
            'ANGLE_OFFSET_VALUE': 0.,              # finale image rotation angle in degrees
            'ANGLE_OFFSET': 0,
            'NUM_PART': 4,                         # length of the numerical part in the data filenames
            'VERSION': 'fastomo3 3.2',
            'CORRECT_SPIKES_THRESHOLD': 0.04,     # threshold above which we have spike
            'DATABASE': 0,                         # Bolean put scan in tomoDB
            'DO_TEST_SLICE': 1,                    # Bolean to reconstruct one slice
            'NO_CHECK': 0,                         # Bolean to force or not reconst of slices in ftseries
            'ZEROOFFMASK': 1,                      # Sets to zero the region outside the reconstruction mask
            'VOLSELECT': 'total',                  # how to select volume: total, manual or graphic
            'VOLSELECTION_REMEMBER': 0,            # option remember when manual
            'RINGSCORRECTION': 0,                  # Bolean to invoke rings correction
            'FIXHD': 0,                            # Not disable to try fixed header size determination
            'RM_HEAD_DIR': '/lbsram',
            'AXIS_CORRECTION_FILE' : 'correct.txt',
            'DO_AXIS_CORRECTION' : 0
        }    

    @staticmethod
    def getDefaultStructPYHSTEXE():
        """ special structure containing PYHST executable """
        return {
            'OFFV': FastSetupAll.OFFV,          # textread([self.DIR self.OFFN], '%s'){1} # ne dois jamais changer On ne la presente pas
            'EXE': FastSetupAll.OFFV,
            'VERBOSE_FILE': 'pyhst_out.txt',
            'VERBOSE': 0,
            'MAKE_OAR_FILE': 0,
        }
        
    @staticmethod
    def getDefaultStructFTAXIS():
        """ special structure containing rotation axis infos """
        return{
            'POSITION': 'accurate',
            'POSITION_VALUE': 0.0,   # value of rotation axis if fixed
            'TO_THE_CENTER': 1,    # Center reconstructed region on rotation axis
            'FILESDURINGSCAN': 0,  # use images during scan for axis calc
            'COR_POSITION': 0,     # use 0-180 or 90-270 images to calculate COR.
            'COR_ERROR': 0,        # systematic error on COR calculation
            'PLOTFIGURE': 1,       # display image in case of highlow
            'HA': 1,               # invoque multi proj algo for COR calculation
            'OVERSAMPLING': 4
        }

    @staticmethod
    def getDefaultStructPAGANIN():
        """ special structure containing rotation axis infos """
        return{
            'MODE': 0,              # mode 0 or 1, 2, 3  Si 0 : tab non visible
            'DB': 500.,              # value of delta/beta
            'DB2': 100.,             # value of delta/beta multi pag
            'UNSHARP_SIGMA': 0.8,   # size of the mask of unsharp masking
            'UNSHARP_COEFF': 3.,    # coeff for unsharp masking
            'THRESHOLD': 500,
            'DILATE': 2,
            'MEDIANR': 4,
            'MKEEP_BONE': 0,
            'MKEEP_SOFT': 0,
            'MKEEP_ABS': 0,
            'MKEEP_CORR': 0,
            'MKEEP_MASK': 0
        }
            
    @staticmethod
    def getDefaultStructBEAMGEO():
        """ special structure containing beam type infos """
        return{
            'TYPE': 'p',            # type p parallel, f fan, c conical
            'SX': 0.,              # Source position on vertical axis(X)
            'SY': 0.,              # Source position on vertical axis(X)
            'DIST': 55.             # Source distance in meters
        }
        
    @staticmethod
    def getDefaultStructDKRF():
        """ special structure containing Dark and Refs methods """
        return{
            'DOWHEN' : 'before',   # Execute calculation Never, before, after
            'DARKCAL': 'Average',  # Dark calculation method (None, Average, Median)
            'DARKOVE': 0,          # Overwrite Dark results if already exists
            'DARKRMV': 1,          # Remove original Darks when done
            'DKFILE': 'darkend[0-9]{3,4}',  # File pattern to detect Dark field
            'REFSCAL': 'Median',   # Dark calculation method (None, Average, Median)
            'REFSOVE': 0,          # Overwrite Dark results if already exists
            'REFSRMV': 0,          # Remove original Darks when done
            'RFFILE': 'ref*.*[0-9]{3,4}_[0-9]{3,4}'  # File pattern to detect references
        }

    @staticmethod
    def getAllDefaultStructures():
        res = {}
        res['FT'] = FastSetupAll.getDefaultStructFT()
        res['PYHSTEXE'] = FastSetupAll.getDefaultStructPYHSTEXE()
        res['FTAXIS'] = FastSetupAll.getDefaultStructFTAXIS()
        res['PAGANIN'] = FastSetupAll.getDefaultStructPAGANIN()
        res['BEAMGEO'] = FastSetupAll.getDefaultStructBEAMGEO()
        res['DKRF'] = FastSetupAll.getDefaultStructDKRF()
        return res
