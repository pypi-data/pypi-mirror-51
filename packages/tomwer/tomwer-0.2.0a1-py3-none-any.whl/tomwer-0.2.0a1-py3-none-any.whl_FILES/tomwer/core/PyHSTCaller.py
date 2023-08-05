# /*##########################################################################
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

__author__ = ["PJ.Gouttenoire", "H. Payno"]
__license__ = "MIT"
__date__ = "22/01/2018"

from tomwer.core.utils.pyhstutils import _getPyHSTDir, _findPyHSTVersions
from tomwer.core.ReconsParams import ReconsParam
import logging
import os

logger = logging.getLogger(__name__)


class PyHSTCaller(object):
    """Simple class containing information to be able to call PyHST
    """
    REC_EXT = '.rec'
    """Extension of the record file"""
    PAR_EXT = '.par'
    """Extension of the reconstruction parameters file"""

    def __init__(self, execDir=None, exeName=None):
        """

        :param execDir: directory containing the pyhst executable(s)
        :param exeName: name of the selected pyhst executable
        """
        self.execDir = execDir
        self.exeName = exeName
        if self.execDir is None:
            self.execDir = _getPyHSTDir()
        if self.execDir is not None:
            executableAvailable = _findPyHSTVersions(self.execDir)
            if len(executableAvailable) > 0:
                self.exeName = executableAvailable[0]

    def isvalid(self):
        """Return True if the exe file exists"""
        return os.path.isfile(os.path.join(self.execDir, self.exeName))
       
    def makeParFile(self, dirname, options=None):
        """
        Function creating the .par file

        creates parameter file for processing with PyHST
        The par file requires 9 fixed arguments:

        * argument 1: direc : path of the scan directory
        * argument 2: prefix : scan prefix
        * argument 3: nvue : number of angles used in the reconstruction
        * argument 4: num_image_1 : number of pixels in the projections along the first axis (horizontal)
        * argument 5: num_image_2 : number of pixels in the projections along the second axis (vertical)
        * argument 6: image_pixel_size : pixel size in microns
        * argument 7: corr : do flatfield correction + log or not: 'YES' or 'NO'
        * argument 8: refon : interval between the flatfield files: e.g. 100
        * argument 9: offset : position of rotation axis with respect to middle in pixels

        :param dirname: the directory to store the .par file
        :param options: dictionary with options you want to set.

                    Regular options are:

                        * 'parfilename': parameter file ( default: direc/prefix.par )
                        * 'start_voxel_1': first pixel in x (starting from 1)
                          (default 1)
                        * 'start_voxel_2': first pixel in y (starting from 1)
                          (default 1)
                        * 'start_voxel_3': first pixel in z (starting from 1)
                          (default 1)
                        * 'end_voxel_1': last pixel in x (starting from 1)
                          (default num_image_1)
                        * 'end_voxel_2': last pixel in y (starting from 1)
                          (default num_image_1)
                        * 'end_voxel_3': last pixel in z (starting from 1)
                          (default num_image_2)
                        * 'angle_offset': offset angle in degrees
                          (default 0)
                        * 'output_file': name of the volume file
                          (default: direc/prefix.vol)
                        * 'ff_prefix': prefix of the flatfield images
                          (default: direc/refHST)
                        * 'background_file': name of the dark file
                          (default: = direc/dark.edf)
                        * 'horaxis': rotation axis horizontal (=constant y) (1)
                          or not (=constant x) (0) ( default 0 )
                        * 'correct_spikes_threshold' : threshold value for ccd
                          filter when value is given, ccd filter will be
                          applied with this parameter (default : parameter is
                          set to 0.04, but DO_CCD_FILTER = 'NO')
                        * 'ccd_filter': filter for correction of spikes
                          (default: 'CCD_Filter')
                        * 'ccd_filter_para': parameters for ccd filter when
                          given overrides choice with correct_spikes_threshold
                        * 'do_axis_correction' : correct for sample motion
                          (default: 'NO')
                        * 'axis_correction_file': name of file with sample
                          movement (default: 'correct.txt' )
                        * 'first column': x motion [ , second column: y motion]
                        * 'do_sino_filter': correction of rings by filtering
                          the sinogram ( default: 'NO' )
                        * 'sino_filter': filter for correction of rings
                          (default: 'SINO_Filter')
                        * 'correct_rings_nb': number of elements (|f|>0) that
                          will not be filtered from sinograms (default 8)
                        * 'padding': padding at edges with edge values 'E' or
                          zero '0' ( default: 'E' )
                        * 'axis_to_the_center' : move axis to the center 'Y' or
                          not 'N' (default: 'Y') !!!
                        * 'angle_between_projections': angle between successive
                          projections ( default 180/nvue )
                        * 'doubleffcorrection': name of the file (e.g.
                          filtered_mean.edf) for double flatfield subtracted
                          after normal flatfield and logarithm.
                        * 'do_projection_median': calculate median of
                          projections (after flat/log) (default: 'NO')
                        * 'projection_median_filename' : name of output
                          edf-file with median (default: median.edf)
                        * 'do_projection_mean': calculate mean of projections
                          (after flat/log) (default: 'NO')
                        * 'projection_mean_filename': name of output edf-file
                          with mean (default: mean.edf) PyHST uses for both
                          median and mean PROJECTION_MEDIAN_FILENAME

                    Advanced options (= do not change, except if you know what
                    you are doing):

                        * 'zeroclipvalue': minimum value of radiographs after
                          flatfield / before logarithm values below are clipped
                          (default 1e-9)
                        * 'oneclipvalue': maximum value of radiographs after
                          flatfield / before logarithm values above are clipped
                          (default: not applied)
                        * 'multiframe': more than one projection in input file
                          (default: 0)
                        * 'num_first_image': index of first image used in
                          reconstruction (default 0)
                        * 'num_last_image': index of last image
                          (default nvue-1)
                        * 'number_length_varies': width index varies or not
                          (default: 'NO')
                        * 'length_of_numerical_part': width of image index
                          (default 4)
                        * 'file_postfix': extension of the image files
                          (default: '.edf')
                        * 'file_interval': downsample in angle (default 1)
                        * 'subtract_background': subtract dark file 'YES' or
                          not 'NO' ( default: corr )
                        * 'correct_flatfield': divide by flatfield image 'YES'
                          or not 'NO' (default: corr)
                        * 'take_logarithm': use -log 'Y' or 'N'
                          (default: 'YES')
                        * 'output_sinograms': output sinogram files or not
                          (default: 'NO')
                        * 'output_reconstruction': do the reconstruction or not
                          (default: 'YES')
                        * 'oversampling_factor': oversampling of projections
                          before backprojection (0 = linear interpolation,
                          1 = nearest pixel) ( default 4 )
                        * 'sinogram_megabytes': maximum memory in MB used for
                          reading the sinograms ( default 400 )
                        * 'cache_kilobytes': obsolete ( default 256 )
                        * 'display_graphics': NOT IMPLEMENTED IN PYHST
                          (default: 'NO')
        """
        
        def loadDefaultPar():
            defaultParams = {}
            params = ReconsParam().params
            logger.info('Loading ERSF parameters')

            FT = params['FT']
            PG = PAG = params['PAGANIN']
            BG = params['BEAMGEO']
            paganin=PAG['MODE']

            basename1 = os.path.basename(prefix)

            defaultParams['half_acquisition'] = FT['HALF_ACQ']

            if PAG['UNSHARP_SIGMA'] !=0 :
                defaultParams['do_unsharp'] = 1
            else :
                defaultParams['do_unsharp'] = 0

            defaultParams['correct_spikes_threshold_default'] = 0.04
            defaultParams['status'] = 1
            defaultParams['parfilename'] = direc + '/' + basename1+ '.par'

            defaultParams['num_first_image'] = 0
            defaultParams['num_last_image'] = params['FT']['NUM_LAST_IMAGE'] -1
            defaultParams['angle_offset'] = 0

            defaultParams['number_length_varies'] = 'NO'
            defaultParams['file_postfix'] = '.edf'
            defaultParams['image_pixel_size_1'] = defaultParams['image_pixel_size_2'] = image_pixel_size
            defaultParams['file_interval'] =1
            defaultParams['subtract_background'] = defaultParams['correct_flatfield'] = corr #= take_logarithm
            defaultParams['take_logarithm'] = 'YES'
            defaultParams['correct'] = ( corr == 'YES' )
            defaultParams['background_file'] = direc + '/dark.edf'
            defaultParams['ff_prefix'] = direc + '/refHST'
            defaultParams['flatfield_file'] = defaultParams['ff_prefix'] + '0000.edf'
            defaultParams['ff_num_first_image'] = 0
            defaultParams['ff_num_last_image'] = nvue
            defaultParams['ff_file_interval'] = refon

            if defaultParams['ff_file_interval'] == 0 :
                defaultParams['flatfield_changing'] = 'NO'
            else :
                defaultParams['flatfield_changing'] = 'YES'

            defaultParams['doubleffcorrection'] = []
            defaultParams['zeroclipvalue'] = .001
            defaultParams['oneclipvalue'] = []
            defaultParams['multiframe'] = 0
            defaultParams['angle_between_projections'] = 180/nvue
            defaultParams['horaxis'] = 0
            defaultParams['output_sinograms'] = 'NO'
            defaultParams['output_reconstruction'] = 'YES'
            defaultParams['start_voxel_1'] = defaultParams['start_voxel_2'] = defaultParams['start_voxel_3'] = 1
            defaultParams['end_voxel_1'] = defaultParams['end_voxel_2'] = num_image_1
            defaultParams['end_voxel_3'] = num_image_2
            defaultParams['oversampling_factor'] = 4

            # limit the memory taken by each reconstruction process to ~ sinogram_megabytes
            defaultParams['sinogram_megabytes'] = 1000
            # provisional trick to avoid that hst on almond reconstructs 4 small slices simultaneously and 'forgets' to use all processors
            defaultParams['cache_kilobytes'] = 256
            # correction spikes
            defaultParams['ccd_filter'] = 'CCD_Filter'

            # correction rings
            if (FT['RINGSCORRECTION']):
                defaultParams['do_sino_filter'] = 'YES'
            else:
                defaultParams['do_sino_filter'] = 'NO'

            defaultParams['correct_rings_nb'] = 2  # number of elements (|f|>0) that will not be filtered from sinograms
            defaultParams['sino_filter'] = 'SINO_Filter'

            # correction motion of axis (filename should contain drift expressed in pixels)
            defaultParams['do_axis_correction'] = 'NO'
            if FT['DO_AXIS_CORRECTION'] == 1:
                defaultParams['do_axis_correction'] = 'YES'
            else :
                defaultParams['axis_correction_file'] = FT['AXIS_CORRECTION_FILE']

            # padding at edges 'E' edge values or '0'
            defaultParams['padding'] = 'E'
            # move axis to the center 'Y' or not 'N'
            defaultParams['axis_to_the_center'] = 'Y'
            defaultParams['do_projection_median'] = 'NO'
            defaultParams['projection_median_filename'] = 'median.edf'
            defaultParams['do_projection_mean'] = 'NO'
            defaultParams['projection_mean_filename'] = 'mean.edf'
            defaultParams['display_graphics'] = 'NO'

            if ((BG['TYPE'] == 'c') or (BG['TYPE'] == 'f')):
                defaultParams['source_x'] = BG['SX']
                defaultParams['source_y'] = BG['SY']
                defaultParams['source_distance'] = BG['DIST']
            else:
                defaultParams['source_x'] = 0
                defaultParams['source_y'] = 0
                defaultParams['source_distance'] = 0

            valJP2 = FT['JP2'] if 'JP2' in FT else 0
            defaultParams['ft_jp2'] = valJP2

            if paganin == 0:
                defaultParams['output_file'] = direc + '/' + basename1 + '.vol'
            elif paganin == 1 or paganin == 2:
                defaultParams['pag_length'] = FT['PAG_LENGTH']
                defaultParams['output_file'] = direc + '/' + basename1 + 'pag.vol'
            elif paganin == 3:
                defaultParams['output_file'] = direc + '/' + basename1 + 'multipag.vol'
                defaultParams['pag_length'] = FT['PAG_LENGTH']
                defaultParams['pag_length2'] = FT['PAG_LENGTH2']
                defaultParams['ft_pag_db2'] = PG['DB2']
                defaultParams['ft_pag_threshold'] = PG['THRESHOLD']
                defaultParams['ft_pag_dilate'] = PG['DILATE']
                defaultParams['ft_pag_medianr'] = PG['MEDIANR']
                defaultParams['multipag_keep_bone'] = PG['MKEEP_BONE']
                defaultParams['multipag_keep_soft'] = PG['MKEEP_SOFT']
                defaultParams['multipag_keep_abs'] = PG['MKEEP_ABS']
                defaultParams['multipag_keep_corr'] = PG['MKEEP_CORR']
                defaultParams['multipag_keep_mask'] = PG['MKEEP_MASK']
                #probleme a regler
                defaultParams['multipag_extra_files'] = (defaultParams['multipag_keep_bone'] == 1
                                                         or defaultParams['multipag_keep_soft'] == 1
                                                         or defaultParams['multipag_keep_mask'] == 1
                                                         or defaultParams['multipag_keep_abs'] == 1
                                                         or defaultParams['multipag_keep_corr'] ==1)
                defaultParams['output_file_bone'] = direc + '/' + prefix + 'multipag_bone.vol'
                defaultParams['output_file_soft'] = direc + '/' + prefix + 'multipag_soft.vol'
                defaultParams['output_file_abs'] =  direc + '/' + prefix + 'multipag_abs.vol'
                defaultParams['output_file_corr'] = direc + '/' + prefix + 'multipag_corr.vol'
                defaultParams['output_file_mask'] = direc + '/' + prefix + 'multipag_mask.vol'

            return defaultParams

        def remove_lbs_head(dirin,params):

            PYHSTEXE = params['FT']

            dirout = dirin

            if 'RM_HEAD_DIR' not in PYHSTEXE:
                return dirout

            lbsram_l = len(PYHSTEXE['RM_HEAD_DIR'])

            if lbsram_l >= 1 and 'RM_HEAD_DIR_EXCEPT' in PYHSTEXE:
                # Get back UTILS.RM_HEAD_DIR_EXCEPT
                assert 'PYHSTEXE' in params
                # Where should it be stored ?
                assert 'RM_HEAD_DIR_EXCEPT' in PYHSTEXE
                utilsRmDirExpect = params['PYHSTEXE']['RM_HEAD_DIR_EXCEPT']

                if dirin.find(PYHSTEXE['RM_HEAD_DIR']) == 1 and dirin.find(utilsRmDirExpect) == 0:
                    dirout = dirin.lstrip(lbsram_l)

            return dirout

        params = ReconsParam().params

        assert 'FT' in params
        assert 'FILE_PREFIX' in params['FT']
        assert 'NUM_LAST_IMAGE' in params['FT']
        assert 'NUM_IMAGE_1' in params['FT']
        assert 'NUM_IMAGE_2' in params['FT']
        assert 'IMAGE_PIXEL_SIZE_1' in params['FT']
        assert 'CORRECT_FLATFIELD' in params['FT']
        assert 'FF_FILE_INTERVAL' in params['FT']
        assert 'OFFSET' in params['FT']

        # those values can't be set by options
        prefix = params['FT']['FILE_PREFIX']
        nvue = params['FT']['NUM_LAST_IMAGE']
        num_image_1 = params['FT']['NUM_IMAGE_1']
        num_image_2 = params['FT']['NUM_IMAGE_2']
        image_pixel_size = params['FT']['IMAGE_PIXEL_SIZE_1']
        corr = params['FT']['CORRECT_FLATFIELD']
        refon = params['FT']['FF_FILE_INTERVAL']
        offset = params['FT']['OFFSET']
        direc = dirname

        fileParameter = loadDefaultPar()
        # Dealing with options
        if options:
            for opt in options:
                fileParameter[opt] = options[opt]

        not_available = 'N.A.'

        FT = params['FT']
        PAG = params['PAGANIN']
        BG = params['BEAMGEO']
        paganin = PAG['MODE']

        length_of_numerical_part = FT['NUM_PART']

        ###################################################
        ##### check and calculate dependent variables #####
        ###################################################
        if fileParameter['horaxis']:
            fileParameter['rotation_vertical']= 'NO'
            fileParameter['rotation_axis_position']= num_image_2/2+offset
            fileParameter['end_voxel_12_limit ']= num_image_2
            fileParameter['end_voxel_3_limit'] = num_image_1
        else:
            fileParameter['rotation_vertical']= 'YES'
            fileParameter['rotation_axis_position']= num_image_1/2+offset
            fileParameter['end_voxel_12_limit'] = num_image_1
            fileParameter['end_voxel_3_limit'] = num_image_2

        # start_voxel should be > 0 ; end_voxel should be <= image dimension
        if (fileParameter['start_voxel_1'] < 1):
            logger.warning('START_VOXEL_1 can not be zero or negative, forcing to 1')
            fileParameter['start_voxel_1'] = 1
        if (fileParameter['start_voxel_2'] < 1):
            logger.warning('START_VOXEL_2 can not be zero or negative, forcing to 1')
            fileParameter['start_voxel_2'] = 1
        if (fileParameter['start_voxel_3'] < 1):
            logger.warning('START_VOXEL_3 can not be zero or negative, forcing to 1')
            fileParameter['start_voxel_3'] = 1

        if fileParameter['half_acquisition'] == 0:
            if (fileParameter['end_voxel_1'] > fileParameter['end_voxel_12_limit']):
                logger.warning('END_VOXEL_1 can not be larger than image dimension, forcing to maximum')
                fileParameter['end_voxel_1'] = fileParameter['end_voxel_12_limit']

            if (fileParameter['end_voxel_2'] > fileParameter['end_voxel_12_limit']):
                logger.warning('END_VOXEL_2 can not be larger than image dimension, forcing to maximum')
                fileParameter['end_voxel_2'] = fileParameter['end_voxel_12_limit']

            fileParameter['avoidhalftomo'] = 'Y'
        else :
            fileParameter['avoidhalftomo'] = 'N'

        if 'FORCE_HALF_ACQ' in params['FT']:
            if FT['FORCE_HALF_ACQ'] == 1 and fileParameter['half_acquisition'] !=0:
                avoidhalftomo = '-1'

        if (fileParameter['end_voxel_3'] > fileParameter['end_voxel_3_limit']):
            logger.warning('END_VOXEL_3 can not be larger than image dimension, forcing to maximum\n')
            fileParameter['end_voxel_3'] = fileParameter['end_voxel_3_limit']

        if (fileParameter['output_file'][0]!='/') :
            fileParameter['output_file'] = direc + fileParameter['output_file']

        # Remove directory head if necessary
        fileParameter['output_file']= remove_lbs_head(fileParameter['output_file'],params)

        if paganin==3 and fileParameter['multipag_extra_files'] == 1:
            if (fileParameter['extra_output_file'][0] != '/'):
                fileParameter['extra_output_file'] = direc + fileParameter['extra_output_file']

            # Remove directory head if necessary
            fileParameter['extra_output_file'] = remove_lbs_head(fileParameter['extra_output_file'], params)

            if fileParameter['multipag_keep_bone'] == 1:
                fileParameter['output_file_bone'] = fileParameter['extra_output_file'] + '_bone.vol'

            if fileParameter['multipag_keep_soft'] == 1:
                fileParameter['output_file_soft'] = fileParameter['extra_output_file'] + '_soft.vol'

            if fileParameter['multipag_keep_mask'] == 1:
                fileParameter['output_file_mask'] = fileParameter['extra_output_file'] + '_mask.vol'

            if fileParameter['multipag_keep_abs'] == 1:
                fileParameter['output_file_abs'] = fileParameter['extra_output_file'] + '_abs.vol'

            if fileParameter['multipag_keep_corr'] == 1:
                fileParameter['output_file_corr'] = fileParameter['extra_output_file'] + '_corr.vol'

        if (fileParameter['parfilename'][0] != '/'):
            fileParameter['parfilename'] = direc + fileParameter['parfilename']

        if (fileParameter['background_file'][0]!='/'):
            fileParameter['background_file'] = direc + fileParameter['background_file']

        if (fileParameter['ff_prefix'][0]!='/'):
            fileParameter['ff_prefix'] = direc + fileParameter['ff_prefix']

        #############################
        #####    angle offset   #####
        #############################
        if not ('ANGLE_OFFSET' in FT):
            fileParameter['angle_offset'] = 0.

        #############################
        ##### correction spikes #####
        #############################
        if not ('CORRECT_SPIKES_THRESHOLD' in FT):
            fileParameter['correct_spikes_threshold'] = 0.
        if not ('CCD_FILTER_PARA' in FT):
            fileParameter['ccd_filter_para'] = []
        if not ('DO_CCD_FILTER' in FT):
            fileParameter['do_ccd_filter'] = []

        if not 'ccd_filter_para' in fileParameter:
            if not 'correct_spikes_threshold' in fileParameter:
                fileParameter['do_ccd_filter_preference'] = 'NO'
                fileParameter['ccd_filter_para'] = '{"threshold": ' + fileParameter['correct_spikes_threshold_default'] + ' }'
            elif fileParameter['correct_spikes_threshold'].isinf():
                fileParameter['do_ccd_filter'] = 'NO'
                fileParameter['ccd_filter_para'] = '{"threshold": ' + fileParameter['correct_spikes_threshold_default'] + ' }'
            else:
                fileParameter['do_ccd_filter_preference'] = 'YES'
                fileParameter['ccd_filter_para'] = '{"threshold": ' + fileParameter['correct_spikes_threshold'] + ' }'
        else :
            fileParameter['do_ccd_filter_preference'] = 'YES'

        if len(fileParameter['do_ccd_filter']) == 0:
            fileParameter['do_ccd_filter'] = fileParameter['do_ccd_filter_preference']

        ##########################
        ##### create parfile #####
        ##########################
        fidparfile = open(fileParameter['parfilename'], 'wb')

        if fileParameter['multiframe'] == 0:
            fileParameter['file_prefix'] = direc + '/' + prefix
        else:
            fileParameter['file_prefix'] = direc + '/' + prefix + '.edf'

        # Remove directory head if necessary
        if ('RM_HEAD_DIR_EXCEPT' in params['PYHSTEXE'] and
                    fileParameter['parfilename'].find(params['PYHSTEXE']['RM_HEAD_DIR_EXCEPT']) == 0):
            fileParameter['file_prefix'] = remove_lbs_head(fileParameter['file_prefix'], params)
            fileParameter['background_file'] = remove_lbs_head(fileParameter['background_file'], params)
            fileParameter['ff_prefix'] = remove_lbs_head(fileParameter['ff_prefix'], params)

        fidparfile.write(bytes('# pyHST_SLAVE PARAMETER FILE\n\n', 'UTF-8'))

        fidparfile.write(
            bytes('# Parameters defining the projection file series\n',
                  'UTF-8'))
        fidparfile.write(bytes('MULTIFRAME = %d\n\n' % fileParameter['multiframe'],
                         'UTF-8'))

        fidparfile.write(
            bytes('FILE_PREFIX = %s\n' % fileParameter['file_prefix'], 'UTF-8'))
        fidparfile.write(
            bytes('NUM_FIRST_IMAGE = %d # No. of first projection file\n' % fileParameter['num_first_image'],
                  'UTF-8'))
        fidparfile.write(
            bytes('NUM_LAST_IMAGE = %d # No. of last projection file\n' % fileParameter['num_last_image'],
                  'UTF-8'))
        fidparfile.write(
            bytes('NUMBER_LENGTH_VARIES = %s\n' % fileParameter['number_length_varies'],
                  'UTF-8'))
        fidparfile.write(
            bytes('LENGTH_OF_NUMERICAL_PART = %d # No. of characters\n' % length_of_numerical_part,
                  'UTF-8'))
        fidparfile.write(
            bytes('FILE_POSTFIX = %s\n' % fileParameter['file_postfix'],
                  'UTF-8'))
        fidparfile.write(
            bytes('FILE_INTERVAL = %d # Interval between input files\n' % fileParameter['file_interval'],
                  'UTF-8'))
        fidparfile.write(
            bytes('\n# Parameters defining the projection file format\n',
                  'UTF-8'))
        fidparfile.write(
            bytes('NUM_IMAGE_1 = %d # Number of pixels horizontally\n' % num_image_1,
                  'UTF-8'))
        fidparfile.write(
            bytes('NUM_IMAGE_2 = %d # Number of pixels vertically\n' % num_image_2,
                  'UTF-8'))
        fidparfile.write(
            bytes('IMAGE_PIXEL_SIZE_1 = %f # Pixel size horizontally (microns)\n' % fileParameter['image_pixel_size_1'],
                  'UTF-8'))
        fidparfile.write(
            bytes('IMAGE_PIXEL_SIZE_2 = %f # Pixel size vertically\n' % fileParameter['image_pixel_size_2'],
                  'UTF-8'))
        fidparfile.write(
            bytes('\n# Parameters defining background treatment\n', 'UTF-8'))
    
        if fileParameter['correct']:
            fidparfile.write(
                bytes('SUBTRACT_BACKGROUND = %s # Subtract background from data\n' % fileParameter['subtract_background'],
                      'UTF-8'))
            fidparfile.write(
                bytes('BACKGROUND_FILE = %s\n' % fileParameter['background_file'],
                      'UTF-8'))
        else:
            fidparfile.write(
                bytes('SUBTRACT_BACKGROUND = %s # No background subtraction\n' % fileParameter['subtract_background'],
                      'UTF-8'))
            fidparfile.write(
                bytes('BACKGROUND_FILE = %s\n' % not_available, 'UTF-8'))

        fidparfile.write(
            bytes('\n# Parameters defining flat-field treatment\n', 'UTF-8'))
        if fileParameter['correct']:
            fidparfile.write(
                bytes('CORRECT_FLATFIELD = %s # Divide by flat-field image\n' % fileParameter['correct_flatfield'],
                      'UTF-8'))
            fidparfile.write(
                bytes('FLATFIELD_CHANGING = %s # Series of flat-field files\n' % fileParameter['flatfield_changing'],
                      'UTF-8'))
            fidparfile.write(
                bytes('FLATFIELD_FILE = %s\n' % fileParameter['flatfield_file'],
                      'UTF-8'))
            fidparfile.write(
                bytes('FF_PREFIX = %s\n' % fileParameter['ff_prefix'], 'UTF-8'))
            fidparfile.write(
                bytes('FF_NUM_FIRST_IMAGE = %d # No. of first flat-field file\n' % fileParameter['ff_num_first_image'],
                      'UTF-8'))
            fidparfile.write(
                bytes('FF_NUM_LAST_IMAGE = %d # No. of last flat-field file\n' % fileParameter['ff_num_last_image'],
                      'UTF-8'))
            fidparfile.write(
                bytes('FF_NUMBER_LENGTH_VARIES = %s\n' % fileParameter['number_length_varies'],
                      'UTF-8'))
            fidparfile.write(
                bytes('FF_LENGTH_OF_NUMERICAL_PART = %d # No. of characters\n' % length_of_numerical_part,
                      'UTF-8'))
            fidparfile.write(
                bytes('FF_POSTFIX = %s\n' % fileParameter['file_postfix'],
                      'UTF-8'))
            fidparfile.write(
                bytes('FF_FILE_INTERVAL = %d # Interval between flat-field files\n' % fileParameter['ff_file_interval'],
                      'UTF-8'))
        else :
            fidparfile.write(
                bytes('CORRECT_FLATFIELD = %s # No flat-field correction\n' % fileParameter['correct_flatfield'],
                      'UTF-8'))
            fidparfile.write(
                bytes('FLATFIELD_CHANGING = %s\n' % not_available,
                      'UTF-8'))
            fidparfile.write(
                bytes('FLATFIELD_FILE = %s\n' % not_available, 'UTF-8'))
            fidparfile.write(
                bytes('FF_PREFIX = %s\n' % not_available, 'UTF-8'))
            fidparfile.write(
                bytes('FF_NUM_FIRST_IMAGE = %s\n' % not_available, 'UTF-8'))
            fidparfile.write(
                bytes('FF_NUM_LAST_IMAGE = %s\n' % not_available, 'UTF-8'))
            fidparfile.write(
                bytes('FF_NUMBER_LENGTH_VARIES = %s\n' % not_available, 'UTF-8'))
            fidparfile.write(
                bytes('FF_LENGTH_OF_NUMERICAL_PART = %s\n' % not_available,
                      'UTF-8'))
            fidparfile.write(
                bytes('FF_POSTFIX = %s\n' % not_available, 'UTF-8'))
            fidparfile.write(
                bytes('FF_FILE_INTERVAL = %s\n' % not_available, 'UTF-8'))

        fidparfile.write(
            bytes('\nTAKE_LOGARITHM = %s # Take log of projection values\n' % fileParameter['take_logarithm'],
                  'UTF-8'))
        if not (fileParameter['doubleffcorrection']==[]):
            fidparfile.write(
                bytes('DOUBLEFFCORRECTION = "filtered_mean.edf" # double flatfield\n',
                      'UTF-8'))

        fidparfile.write(
            bytes('\n# Parameters defining experiment\n', 'UTF-8'))
        fidparfile.write(
            bytes('ANGLE_BETWEEN_PROJECTIONS = %f # Increment angle in degrees\n' % fileParameter['angle_between_projections'],
                  'UTF-8'))
        fidparfile.write(
            bytes('ROTATION_VERTICAL = %s\n' % fileParameter['rotation_vertical'],
                  'UTF-8'))
        fidparfile.write(
            bytes('ROTATION_AXIS_POSITION = %f # Position in pixels\n' % fileParameter['rotation_axis_position'],
                  'UTF-8'))
        fidparfile.write(
            bytes('\n# Parameters defining reconstruction\n', 'UTF-8'))
        fidparfile.write(
            bytes('OUTPUT_SINOGRAMS = %s # Output sinograms to files or not\n' % fileParameter['output_sinograms'],
                  'UTF-8'))
        fidparfile.write(
            bytes('OUTPUT_RECONSTRUCTION = %s # Reconstruct and save or not\n' % fileParameter['output_reconstruction'],
                  'UTF-8'))
        fidparfile.write(
            bytes('START_VOXEL_1 =   %4d # X-start of reconstruction volume\n' % fileParameter['start_voxel_1'],
                  'UTF-8'))
        fidparfile.write(
            bytes('START_VOXEL_2 =   %4d # Y-start of reconstruction volume\n' % fileParameter['start_voxel_2'],
                  'UTF-8'))
        fidparfile.write(
            bytes('START_VOXEL_3 =   %4d # Z-start of reconstruction volume\n' % fileParameter['start_voxel_3'],
                  'UTF-8'))
        fidparfile.write(
            bytes('END_VOXEL_1 =   %4d # X- of reconstruction volume\n' % fileParameter['end_voxel_1'],
                  'UTF-8'))
        fidparfile.write(
            bytes('END_VOXEL_2 =   %4d # Y- of reconstruction volume\n' % fileParameter['end_voxel_2'],
                  'UTF-8'))
        fidparfile.write(
            bytes('END_VOXEL_3 =   %4d # Z- of reconstruction volume\n' % fileParameter['end_voxel_3'],
                  'UTF-8'))
        fidparfile.write(
            bytes('OVERSAMPLING_FACTOR = %d # 0 = Linear, 1 = Nearest pixel\n' % fileParameter['oversampling_factor'],
                  'UTF-8'))
        fidparfile.write(
            bytes('ANGLE_OFFSET = %f # Reconstruction rotation offset angle in degrees\n' % fileParameter['angle_offset'],
                  'UTF-8'))
        fidparfile.write(
            bytes('CACHE_KILOBYTES = %d # Size of processor cache (L2) per processor (KBytes)\n' % fileParameter['cache_kilobytes'],
                  'UTF-8'))
        fidparfile.write(
            bytes('SINOGRAM_MEGABYTES = %d # Maximum size of sinogram storage (megabytes)\n' % fileParameter['sinogram_megabytes'],
                  'UTF-8'))

        # adding extra features for PyHST
        fidparfile.write(
            bytes('\n# Parameters extra features PyHST\n', 'UTF-8'))
        fidparfile.write(
            bytes('DO_CCD_FILTER = %s # CCD filter (spikes)\n' % fileParameter['do_ccd_filter'],
                  'UTF-8'))
        fidparfile.write(
            bytes('CCD_FILTER = "%s"\n' % fileParameter['ccd_filter'],
                  'UTF-8'))
        fidparfile.write(
            bytes('CCD_FILTER_PARA = %s\n' % fileParameter['ccd_filter_para'],
                  'UTF-8'))
        fidparfile.write(
            bytes('DO_SINO_FILTER = %s # Sinogram filter (rings)\n' % fileParameter['do_sino_filter'],
                  'UTF-8'))
        fidparfile.write(
            bytes('SINO_FILTER = "%s"\n' % 'SINO_Filter', 'UTF-8'))
        fidparfile.write(
            bytes('ar = Numeric.ones(%d,''f'')\n' % num_image_1, 'UTF-8'))
        # fidparfile.write('ar = Numeric.ones(%d,''f'')\n' % 2048); pco @@@
        fidparfile.write(bytes('ar[0]=0.0\n', 'UTF-8'))
    
        if (fileParameter['correct_rings_nb'] > 0):
            fidparfile.write(
                bytes('ar[2:%d]=0.0\n' % 2*(fileParameter['correct_rings_nb']+1),
                      'UTF-8'))

        fidparfile.write(
            bytes('SINO_FILTER_PARA = {"FILTER": ar }\n', 'UTF-8'))
        fidparfile.write(
            bytes('DO_AXIS_CORRECTION = %s # Axis correction\n' % fileParameter['do_axis_correction'],
                  'UTF-8'))
        fidparfile.write(
            bytes('AXIS_CORRECTION_FILE = %s\n' % fileParameter['axis_correction_file'],
                  'UTF-8'))
        fidparfile.write(
            bytes('OPTIONS= { ''padding'':''%s'' , ''axis_to_the_center'':''%s'' , ''avoidhalftomo'':''%s''} # Padding and position axis\n' % (fileParameter['padding'],fileParameter['axis_to_the_center'],fileParameter['avoidhalftomo']),
                  'UTF-8'))
        #fidparfile.write('NSLICESATONCE=200  # limiting the number of slices at once to not crash the memory \n')

        if paganin > 0:
            fidparfile.write(
                bytes('\n# Parameters for Paganin reconstruction\n', 'UTF-8'))
            fidparfile.write(
                bytes('# delta over beta ratio for Paganin phase retrieval = %1.2f \n' % PAG['DB'],
                      'UTF-8'))
            fidparfile.write(bytes('DO_PAGANIN = 1 \n', 'UTF-8'))
            fidparfile.write(
                bytes('PAGANIN_Lmicron = %f \n' % fileParameter['pag_length'],
                      'UTF-8'))

            if fileParameter['start_voxel_3'] == fileParameter['end_voxel_3']:
                #disp('file for reconstruction of a single slice, I reduce the part of the picture taken into account for the phase retrieval for faster processing')
                fidparfile.write(bytes('PAGANIN_MARGE = 50 \n', 'UTF-8'))
            else:
                #disp('preparation for a full reconstruction of the volume, the whole picture will be used for the phase retrieval process to ensure final quality and accuracy')
                fidparfile.write(bytes('PAGANIN_MARGE = 200 \n', 'UTF-8'))

            fidparfile.write(bytes('DO_OUTPUT_PAGANIN = 0 \n', 'UTF-8'))
            fidparfile.write(
                bytes('OUTPUT_PAGANIN_FILE = paga_cufft \n', 'UTF-8'))
            fidparfile.write(bytes('PAGANIN_TRY_CUFFT = 1 \n', 'UTF-8'))
            fidparfile.write(bytes('PAGANIN_TRY_FFTW = 1 \n', 'UTF-8'))

            if fileParameter['do_unsharp'] == 1:
                fidparfile.write(
                    bytes('\n# Parameters for unsharp masking on the radiographs\n',
                          'UTF-8'))
                fidparfile.write(bytes('UNSHARP_LOG = 1 \n', 'UTF-8'))
                fidparfile.write(
                    bytes('PUS = %f \n' % PAG['UNSHARP_SIGMA'], 'UTF-8'))
                fidparfile.write(
                    bytes('PUC = %f \n' % PAG['UNSHARP_COEFF'], 'UTF-8'))

        if paganin == 3:
            fidparfile.write(bytes('\n# Multi_paganin\n', 'UTF-8'))
            fidparfile.write(
                bytes('# 2nd delta over beta ratio for multi Paganin phase retrieval = %1.2f \n' % PAG['DB2'],
                      'UTF-8'))
            fidparfile.write(bytes('MULTI_PAGANIN_PARS={}\n', 'UTF-8'))
            fidparfile.write(
                bytes('MULTI_PAGANIN_PARS["BONE_Lmicron"]= %f \n' % fileParameter['pag_length2'],
                      'UTF-8'))
            fidparfile.write(
                bytes('MULTI_PAGANIN_PARS["THRESHOLD"]= %1.3f\n' % fileParameter['ft_pag_threshold'],
                      'UTF-8'))
            fidparfile.write(
                bytes('MULTI_PAGANIN_PARS["DILATE"]= %1.0f\n' % fileParameter['ft_pag_dilate'],
                      'UTF-8'))
            fidparfile.write(
                bytes('MULTI_PAGANIN_PARS["MEDIANR"]= %1.0f\n' % fileParameter['ft_pag_medianr'],
                      'UTF-8'))

            if fileParameter['multipag_keep_bone'] == 1:
                fidparfile.write(
                    bytes('MULTI_PAGANIN_PARS["PAGBONE_FILE"] = "%s"\n' % fileParameter['output_file_bone'],
                          'UTF-8'))
            if fileParameter['multipag_keep_mask'] == 1:
                fidparfile.write(
                    bytes('MULTI_PAGANIN_PARS["MASKBONE_FILE"] = "%s"\n' % fileParameter['output_file_mask'],
                          'UTF-8'))
            if fileParameter['multipag_keep_abs'] == 1:
                fidparfile.write(
                    bytes('MULTI_PAGANIN_PARS["ABSBONE_FILE"] = "%s"\n' % fileParameter['output_file_abs'],
                          'UTF-8'))
            if fileParameter['multipag_keep_corr'] == 1:
                fidparfile.write(
                    bytes('MULTI_PAGANIN_PARS["CORRBONE_FILE"] = "%s"\n' % fileParameter['output_file_corr'],
                          'UTF-8'))
            if fileParameter['multipag_keep_soft'] == 1:
                fidparfile.write(
                    bytes('MULTI_PAGANIN_PARS["CORRECTEDVOL_FILE"] = "%s"\n' % fileParameter['output_file_soft'],
                          'UTF-8'))

        if fileParameter['half_acquisition'] == 1:
            fidparfile.write(bytes('PENTEZONE=300\n', 'UTF-8'))

        if FT['ZEROOFFMASK'] == 0:
            fidparfile.write(bytes('ZEROOFFMASK=0\n', 'UTF-8'))

        ########################## addings for version 2 of Pyhst ################################

        fidparfile.write(
            bytes('TRYEDFCONSTANTHEADER=%d \n' % (1-FT['FIXHD']), 'UTF-8'))

        ##########################################################################################

        if not 'zeroclipvalue' in fileParameter:
            fidparfile.write(
                bytes('ZEROCLIPVALUE = %g # Minimum value of radiographs after flat / before log\n' % fileParameter['zeroclipvalue'],
                      'UTF-8'))

        if not 'oneclipvalue' in fileParameter:
            fidparfile.write(
                bytes('ONECLIPVALUE = %g # Maximum value of radiographs after flat / before log\n' % fileParameter['oneclipvalue'],
                      'UTF-8'))

        if fileParameter['do_projection_median'] == 'YES':
            fidparfile.write(
                bytes('DO_PROJECTION_MEDIAN = %s # Calculate median of all projections\n' % fileParameter['do_projection_median'],
                      'UTF-8'))
            fidparfile.write(
                bytes('PROJECTION_MEDIAN_FILENAME = "%s" # Name output file median calculation\n' % fileParameter['projection_median_filename'],
                      'UTF-8'))

        if fileParameter['do_projection_mean'] == 'YES':
            fidparfile.write(
                bytes('DO_PROJECTION_MEAN = %s # Calculate median of all projections\n' % fileParameter['do_projection_mean'],
                      'UTF-8'))
            fidparfile.write(
                bytes('PROJECTION_MEDIAN_FILENAME = "%s" # Name output file mean calculation\n' % fileParameter['projection_mean_filename'],
                      'UTF-8'))

        fidparfile.write(
            bytes('\n# Parameters defining output file / format\n', 'UTF-8'))
        fidparfile.write(
            bytes('OUTPUT_FILE = %s\n' % fileParameter['output_file'],
                  'UTF-8'))

        fidparfile.write(
            bytes('\n# Reconstruction program options\n', 'UTF-8'))
        fidparfile.write(
            bytes('DISPLAY_GRAPHICS = %s # No images\n' % fileParameter['display_graphics'],
                  'UTF-8'))

        if fileParameter['ft_jp2'] == 1:
            fidparfile.write(bytes('\n#JP2000\n', 'UTF-8'))
            fidparfile.write(bytes('JP2EDF_DIR = "/tmp/jp2/" \n', 'UTF-8'))
            fidparfile.write(bytes('JP2EDF_REMOVE = 1 \n', 'UTF-8'))

        ##########CONICAL AND FAN BEAM RECONSTRUCTION############################################

        if BG['TYPE'] == 'c':
            fidparfile.write(
                bytes('\n# Conical and Fan beam reconstruction\n', 'UTF-8'))
            fidparfile.write(bytes('CONICITY = 1\n', 'UTF-8'))
            fidparfile.write(bytes('CONICITY_FAN = 0\n', 'UTF-8'))
            fidparfile.write(
                bytes('SOURCE_X = %f\n' % fileParameter['source_x'],
                      'UTF-8'))
            fidparfile.write(
                bytes('SOURCE_Y = %f\n' % fileParameter['source_y'],
                      'UTF-8'))
            fidparfile.write(
                bytes('SOURCE_DISTANCE = %f\n' % fileParameter['source_distance'],
                      'UTF-8'))

        if BG['TYPE'] == 'f':
            fidparfile.write(
                bytes('\n# Conical and Fan beam reconstruction\n', 'UTF-8'))
            fidparfile.write(bytes('CONICITY = 0\n', 'UTF-8'))
            fidparfile.write(bytes('CONICITY_FAN = 1\n', 'UTF-8'))
            fidparfile.write(
                bytes('SOURCE_X = %f\n' % fileParameter['source_x'], 'UTF-8'))
            fidparfile.write(
                bytes('SOURCE_Y = %f\n' % fileParameter['source_y'], 'UTF-8'))
            fidparfile.write(
                bytes('SOURCE_DISTANCE = %f\n' % fileParameter['source_distance'],
                      'UTF-8'))

        fidparfile.close()

    def makeRecFile(self, dirname):
        """
        Function creating the .rec file

        :param dirname: the directory to store the .rec file
        """

        def loadFileInfoFrmPar(filePath):
            info = 'Reading %s to get reconstruction parameters'
            logger.info(info)
            ofile = open(filePath, 'rb')
            lines = ofile.readlines()
            outputFile = None
            filePrefix = None
            for line in lines:
                l = str(line)
                if 'OUTPUT_FILE' in l:
                    splitLine = l.split()
                    outputFile = splitLine[2]
                    logger.info('Found OUTPUT_FILE: %s' % outputFile)

                if 'FILE_PREFIX' in l:
                    splitLine = l.split()
                    filePrefix = splitLine[2]
                    logger.info('Found FILE_PREFIX: %s' % filePrefix)
            ofile.close()
            return outputFile, filePrefix

        params = ReconsParam().params
        test = params['FT']

        aux = dirname.split('/')
        filepar = os.path.join(dirname, aux[-1] + PyHSTCaller.PAR_EXT)
        vol_output = test['VOLOUTFILE']

        if os.path.isfile(vol_output):
            err = "Vol out file (%s) not existing" % vol_output
            raise ValueError(err)

        ### Get useful parameter
        if os.path.isfile(filepar):
            recFile, prefix = loadFileInfoFrmPar(filepar)
        else:
            err = 'No %s file found. Can\'t deduce reconstruction parameters.'
            raise ValueError(err)

        if recFile is None or prefix is None:
            raise IOError('Failed to load parameters `OUTPUT_FILE` and/or '
                          '`FILE_PREFIX` in the reconstruction parameters file')

        ### Get the prefix for .rec name file
        ### prefix : only name of file without extension
        ### prefix_full : name and directory of file without extension
        basename1 = os.path.basename(prefix)
        logger.info("prefix is %s" % basename1)
        prefix_full = filepar[0:-4]
        logger.info("prefix is %s" % prefix_full)
        if prefix_full[-3:] == "pag":
            prefix = prefix_full[0:-3]
        else:
            prefix = prefix_full

        # Get parameter for writing the script
        assert 'PYHSTEXE' in params
        assert 'MAKE_OAR_FILE' in params['PYHSTEXE']
        utilsMakeOAR = params['PYHSTEXE']['MAKE_OAR_FILE']

        logger.info(('Processing the file %s %s' % (prefix_full, prefix)))

        # Writing the script file
        shellfilename = prefix_full + '.rec'
        fidshell = open(shellfilename, 'wb')
        fidshell.write(bytes('#!/bin/bash\n', 'UTF-8'))
        fidshell.write(
            bytes('GET_OS="/csadmin/common/scripts/get_os.share"\n', 'UTF-8'))
        fidshell.write(bytes('os=`$GET_OS`\n', 'UTF-8'))
        fidshell.write(
            bytes('export PYHST=' + self.execDir + self.exeName + '\n',
                  'UTF-8'))
        fidshell.write(bytes('case "${os}" in\n', 'UTF-8'))
        fidshell.write(bytes('    centos*)\n', 'UTF-8'))
        if vol_output == 0:
            fidshell.write(bytes('    mkdir ' + recFile + ' \n', 'UTF-8'))
            fidshell.write(bytes('    chmod 775 ' + recFile + ' \n', 'UTF-8'))

        fidshell.write(bytes(
            '        ' + str(utilsMakeOAR) + ' ' + prefix_full + ' 1\n',
            'UTF-8'))

        fidshell.write(bytes(
            '        oarsub -q gpu  -S ./' + prefix_full + '.oar\n', 'UTF-8'))

        fidshell.write(bytes('        ;;\n', 'UTF-8'))
        fidshell.write(bytes('    debian*)\n', 'UTF-8'))
        if vol_output == 0:
            fidshell.write(bytes('    mkdir ' + recFile + ' \n', 'UTF-8'))

        fidshell.write(bytes(
            '        ' + str(utilsMakeOAR) + ' ' + prefix_full + ' 1\n', 'UTF-8'))
        fidshell.write(bytes(
            '        oarsub -q gpu -S ./' + prefix_full + '.oar\n', 'UTF-8'))

        fidshell.write(bytes('        ;;\n', 'UTF-8'))
        fidshell.write(bytes('    *)\n', 'UTF-8'))
        fidshell.write(bytes('esac\n', 'UTF-8'))
        fidshell.close()
        os.chmod(shellfilename, 0o777)
        return
