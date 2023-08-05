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
__date__ = "09/01/2018"


from silx.gui import qt
from tomwer.core.utils.Singleton import singleton
from tomwer.core.ftseries.FastSetupDefineGlobals import FastSetupAll
import logging
import os

logger = logging.getLogger(__name__)


@singleton
class ReconsParam(qt.QObject):
    """This is the class defining the current parameter of reconstruction.
    They are unique and used in all tomwer class needing information about them
    
    .. warning:: this as been made into a singleton to make sure in the gui
                 that if 1..n ftserie widget(s) are editing a reconsparam and 
                 1..n darkRef widget(s) are also editing then they are all
                 editing the same object. This bring the constrain to have
                 only one active set of parameters.
                 Otherwise we would have to define an id for each set of
                 reconstruction but more importantly the management should be
                 done by the user in the widgets. That would be from my POV
                 way more complicated.
    """

    sigChanged = qt.Signal()
    """Signal emitted when at least one element of the dictionary change"""

    def __init__(self):
        qt.QObject.__init__(self)
        # Failed to do a direct inheritance to the dict object
        # (due to Qt inheritance ?)
        self._params = {}

        # try to load from mytomodefault.h5
        defaultH5File = os.path.expanduser('~') + '/.octave/mytomodefaults.h5'
        if os.path.isfile(defaultH5File) is True:
            self.load(defaultH5File)
        else:
            # otherwise load default parameters
            self._params = FastSetupAll().defaultValues

    def setValue(self, structID, paramID, value):
        """
        Set on spectific parameter to one existing structsID

        :param str structID: the struct parent of the param
        :param str paramID: the key of the structID dict 
        :param value: 
        """
        def _checkAngleOffset():
            """Deal with the link between ANGLE_OFFSET and ANGLE_OFFSET_VALUE
            """
            if structID == 'FT' and paramID == 'ANGLE_OFFSET':
                if value == 0:
                    self._params[structID]['ANGLE_OFFSET_VALUE'] = 0.0
            if structID == 'FT' and paramID == 'ANGLE_OFFSET_VALUE':
                self._params[structID]['ANGLE_OFFSET'] = int(not (value == 0.0))

        if structID not in self._params:
            raise ValueError('structID not register')
        self._params[structID][paramID] = value
        _checkAngleOffset()
        self.sigChanged.emit()

    def setStructs(self, structs):
        """Set the entire dictionary of parameters
        
        """
        def _checkAngleOffset():
            """Make sure there is coherence between ANGLE_OFFSET and
            ANGLE_OFFSET_VALUE parameters.
            ..note :: Policy is that ANGLE_OFFSET_VALUE is the reference
            """
            if 'FT' in structs:
                ftStructs = structs['FT']
                if 'ANGLE_OFFSET' in ftStructs and 'ANGLE_OFFSET_VALUE' in ftStructs:
                    self._params['FT']['ANGLE_OFFSET'] = not (ftStructs['ANGLE_OFFSET_VALUE'] == 0)

        assert(isinstance(structs, dict))
        self._params = structs
        FastSetupAll()._check_variables(self._params)
        _checkAngleOffset()
        self.sigChanged.emit()

    def getValue(self, structID, paramID):
        return self._params[structID][paramID]

    @property
    def params(self):
        return self._params

    def load(self, h5file):
        """Update GUI from the existing self.h5file

        :param str h5File: path to the file to load. If none then reload the
                           existing one.

        :note: the path given won't be stored as the path of the file we are
                editing. We will only load parameters values. Next saving action
                will apply on the previoulsy setted path

        """
        assert os.path.isfile(h5file)
        logger.info('Loading h5 structures from %s' %h5file)
        reader = FastSetupAll()
        reader.readAll(h5file, 3.8)
        self._params = reader.structures
        self.sigChanged.emit()
