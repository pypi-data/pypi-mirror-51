# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
# ###########################################################################*/
"""
Basic class each orange widget processing an action should inheritate from
her corresponding class in core.
And all of those classes from core should implement this interface to deal
with the interpreter parser.
Allowing to convert an orane workflow to a TOWER workflow ( same action but no
GUI )
"""


__author__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "02/06/2017"


from tomwer.core.log.colorlogger import ColoredLogger


class BaseProcess(object):
    """Class from which all tomwer process should inherit
    
    :param logger: the logger used by the class
    """

    def __init__(self, logger):
        logger = ColoredLogger(logger)
        self._scheme_title = None  # title of the associated sheme

    def setProperties(self, properties):
        raise NotImplementedError('BaseProcess is an abstract class')
