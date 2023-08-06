###############################################################################
#       Copyright (C) 2017-2019  Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

from libcpp.pair cimport pair

from cython.operator cimport dereference, preincrement, postincrement

from .defs cimport ostringstream, pm_repr_wrap
from .set cimport SetInt

cdef class ArrayBool(PmObject):
    def __len__(self): return self.pm_obj.size()
    def __getitem__(self, Py_ssize_t i):
        if i < 0 or i >= self.pm_obj.size(): raise IndexError
        return self.pm_obj[i]
    def __iter__(self):
        cdef pm_Array[bool].const_iterator it = self.pm_obj.begin()
        while it != self.pm_obj.end():
            yield dereference(it)
            postincrement(it)
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')
    def python(self):
        r"""
        Converts into a list of booleans
        """
        return [self.pm_obj[i] for i in range(len(self))]

cdef class ArrayInt(PmObject):
    def __len__(self): return self.pm_obj.size()
    def __getitem__(self, Py_ssize_t i):
        r"""
        >>> import polymake
        >>> p = polymake.cube(3)
        >>> type(c)
        <type 'polymake.array.ArrayInt'>
        >>> c[0]
        7
        >>> c[-1]
        Traceback (most recent call last):
        ...
        IndexError
        >>> c[len(c)]
        Traceback (most recent call last):
        ...
        IndexError
        """
        if i < 0 or i >= self.pm_obj.size(): raise IndexError
        return self.pm_obj[i]
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')
    def python(self):
        r"""
        Converts into a Python list of integers

        >>> import polymake
        >>> p = polymake.cube(3)
        >>> type(c)
        <type 'polymake.array.ArrayInt'>
        >>> c.python()
        [7, 6, 5, 4, 3, 2, 1, 0]
        """
        return [self[i] for i in range(len(self))]

cdef class ArrayString(PmObject):
    def __len__(self): return self.pm_obj.size()
    def __getitem__(self, Py_ssize_t i):
        if i < 0 or i >= self.pm_obj.size(): raise IndexError
        return (<bytes>self.pm_obj[i]).decode('ascii')
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')
    def python(self):
        return [self[i] for i in range(len(self))]

cdef class ArraySetInt(PmObject):
    r"""
    Array of sets of integers

    EXAMPLES:

    >>> import polymake
    >>> c = polymake.cube(3,2,0)
    """
    def __len__(self): return self.pm_obj.size()
    def __getitem__(self, Py_ssize_t i):
        if i < 0 or i >= self.pm_obj.size(): raise IndexError
        cdef SetInt s = SetInt.__new__(SetInt)
        s.pm_obj = self.pm_obj[i]
        return s
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

cdef class ArrayArrayInt(PmObject):
    def __len__(self): return self.pm_obj.size()
    def __getitem__(self, Py_ssize_t i):
        if i < 0 or i >= self.pm_obj.size(): raise IndexError
        cdef ArrayInt a = ArrayInt.__new__(ArrayInt)
        a.pm_obj = self.pm_obj[i]
        return a
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

cdef class ArrayArrayString(PmObject):
    def __len__(self): return self.pm_obj.size()
    def __getitem__(self, Py_ssize_t i):
        if i < 0 or i >= self.pm_obj.size(): raise IndexError
        cdef ArrayString a = ArrayString.__new__(ArrayString)
        a.pm_obj = self.pm_obj[i]
        return a
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')
    def python(self):
        r"""Converts into a list of list of strings
        """
        return [self[i].python() for i in range(len(self))]

cdef class ArrayPairStringString(PmObject):
    def __len__(self): return self.pm_obj.size()
    def __getitem__(self, Py_ssize_t i):
        if i < 0 or i >= self.pm_obj.size(): raise IndexError
        cdef pair[string,string] x = self.pm_obj[i]
        return (x.first, x.second)
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')
    def python(self):
        cdef Py_ssize_t i
        return [self[i] for i in range(self.pm_obj.size())]

cdef class ArrayPairStringArrayString(PmObject):
    def __len__(self): return self.pm_obj.size()
    def __getitem__(self, Py_ssize_t i):
        if i < 0 or i >= self.pm_obj.size(): raise IndexError
        cdef pair[string, pm_Array[string]] x = self.pm_obj[i]
        cdef ArrayString y = ArrayString.__new__(ArrayString)
        y.pm_obj = x.second
        return (x.first, y)
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')
    def python(self):
        cdef Py_ssize_t i
        l = [self[i] for i in range(self.pm_obj.size())]
        return [(x, y.python()) for x,y in l]

cdef class ArrayArrayPairStringString(PmObject):
    def __len__(self): return self.pm_obj.size()
    def __getitem__(self, Py_ssize_t i):
        if i < 0 or i >= self.pm_obj.size(): raise IndexError
        cdef ArrayPairStringString a = ArrayPairStringString.__new__(ArrayPairStringString)
        a.pm_obj = self.pm_obj[i]
        return a
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')
    def python(self):
        cdef Py_ssize_t i
        return [self[i].python() for i in range(self.pm_obj.size())]
