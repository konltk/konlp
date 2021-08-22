# *****************************************************************************
# Copyright 2004-2008 Steve Menard
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# *****************************************************************************

import collections

import _jpype

from . import _jclass
from . import _jwrapper


_CLASSES = {}
_CUSTOMIZERS = []


def _initialize():
    _jpype.setJavaArrayClass(_JavaArrayClass)
    _jpype.setGetJavaArrayClassMethod(_getClassFor)

    registerArrayCustomizer(CharArrayCustomizer())
    registerArrayCustomizer(ByteArrayCustomizer())


def registerArrayCustomizer(c):
    _CUSTOMIZERS.append(c)


class _JavaArrayClass(object):
    def __init__(self, jo):
        self.__javaobject__ = jo

    def __str__(self):
        return str(tuple(self))

    def __len__(self):
        return _jpype.getArrayLength(self.__javaobject__)

    def __iter__(self):
        return _JavaArrayIter(self)

    def __getitem__(self, ndx):
        if type(ndx) is not slice:
            # Simple index
            return _jpype.getArrayItem(self.__javaobject__, ndx)

        # Slice
        start = ndx.start if ndx.start is not None else 0
        stop = ndx.stop if ndx.stop is not None else 0

        if stop >= start and ndx.step in (None, 1):
            # Normal slice
            return _jpype.getArraySlice(self.__javaobject__, start, stop)
        else:
            # Complex slice
            start, stop, step = ndx.indices(self.__len__())
            return [_jpype.getArrayItem(self.__javaobject__, index)
                    for index in range(start, stop, step)]

    def __setitem__(self, ndx, val):
        if type(ndx) is not slice:
            # Simple index
            _jpype.setArrayItem(self.__javaobject__, ndx, val)
            return

        # Slice
        start = ndx.start if ndx.start is not None else 0
        stop = ndx.stop if ndx.stop is not None else 0

        if stop >= start and ndx.step in (None, 1):
            # Normal slice
            _jpype.setArraySlice(self.__javaobject__, start, stop, val)
        else:
            # Complex slice
            start, stop, step = ndx.indices(self.__len__())
            indices = range(start, stop, step)
            for value in val:
                _jpype.setArrayItem(self.__javaobject__, next(indices), value)


def _jarrayInit(self, *args):
    if len(args) == 2 and args[0] == _jclass._SPECIAL_CONSTRUCTOR_KEY:
        _JavaArrayClass.__init__(self, args[1])
    elif len(args) != 1:
        raise TypeError(
            "Array classes only take 2 parameters, {0} given"
            .format(len(args) + 1))
    else:
        values = None
        if isinstance(args[0], collections.Sequence):
            sz = len(args[0])
            values = args[0]
        else:
            sz = args[0]

        _JavaArrayClass.__init__(
            self, _jpype.newArray(self.__class__.__javaclass__, sz))

        if values is not None:
            _jpype.setArrayValues(self.__javaobject__, values)


class _JavaArrayIter(object):
    def __init__(self, a):
        self._array = a
        self._ndx = -1

    def __iter__(self):
        return self

    def __next__(self):
        self._ndx += 1
        if self._ndx >= len(self._array):
            raise StopIteration
        return self._array[self._ndx]

    next = __next__


class _JavaArray(type):
    pass


def _defineArrayClass(name, jt):
    members = {
        "__init__": _jarrayInit,
        "__javaclass__": jt,
    }

    bases = [_JavaArrayClass]

    for i in _CUSTOMIZERS:
        if i.canCustomize(name, jt):
            i.customize(name, jt, bases, members)

    return _JavaArray(name, tuple(bases), members)


def _getClassFor(name):
    if name not in _CLASSES:
        jc = _jpype.findArrayClass(name)
        _CLASSES[name] = _defineArrayClass(name, jc)

    return _CLASSES[name]


def JArray(t, ndims=1):
    if issubclass(t, _jwrapper._JWrapper):
        t = t.typeName

    elif isinstance(t, _JavaArray):
        t = t.typeName

    elif issubclass(t, _jclass._JAVAOBJECT):
        t = t.__name__

    elif not isinstance(t, str):
        raise TypeError("Argument must be a java class, java array class, "
                        "java wrapper or string representing a java class")

    arrayTypeName = t + ('[]' * ndims)

    return _getClassFor(arrayTypeName)


def _charArrayStr(self):
    return ''.join(self)


def _charArrayUnicode(self):
    return ''.join(self)


class CharArrayCustomizer(object):
    def canCustomize(self, name, jc):
        if name == 'char[]':
            return True
        return False

    def customize(self, name, jc, bases, members):
        members['__str__'] = _charArrayStr
        members['__unicode__'] = _charArrayUnicode


def _byteArrayStr(self):
    s = _jclass.JClass('java.lang.String')(self)
    return s.toString()


class ByteArrayCustomizer(object):
    def canCustomize(self, name, jc):
        if name == 'byte[]':
            return True
        return False

    def customize(self, name, jc, bases, members):
        members['__str__'] = _byteArrayStr
