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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "14/06/2017"

from Orange.canvas.registry.description import (InputSignal, OutputSignal)


def convertInputsForOrange(inputs):
    assert(type(inputs) in (list, tuple) )
    res = []
    for input in inputs:
        assert (type(input) is dict)
        assert('name' in input)
        assert ('type' in input)
        assert ('handler' in input)
        res.append( InputSignal(name=input['name'],
                                type=input['type'],
                                handler=input['handler']))
    return res


def convertOutputsForOrange(outputs):
    assert(type(outputs) in (list, tuple))
    res = []
    for output in outputs:
        assert(type(output) is dict)
        assert ('name' in output)
        assert ('type' in output)
        res.append( OutputSignal(name=output['name'],
                                 type=output['type'],
                                 doc=(output['doc'] if 'doc' in output else '')
                                 ))

    return res
