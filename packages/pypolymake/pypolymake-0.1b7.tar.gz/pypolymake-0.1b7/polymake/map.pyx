###############################################################################
#       Copyright (C) 2011-2012 Burcin Erocal <burcin@erocal.org>
#                     2016-2019 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

from cython.operator cimport dereference, preincrement

from libcpp cimport bool
from libcpp.string cimport string

from .integer cimport Integer
from .rational cimport Rational

cdef class MapStringString(PmObject):
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def __getitem__(self, bytes key):
        return self.pm_obj[key]

    def __len__(self):
        return self.pm_obj.size()

    def __iter__(self):
        cdef pm_Map[string,string].iterator it = self.pm_obj.begin()
        while not it.at_end():
            yield dereference(it).first
            preincrement(it)

    def __contains__(self, bytes key):
        return self.pm_obj.exists(key)

    def items(self):
        "Iterator throug the pairs (key, value) of this map"
        cdef pm_Map[string,string].iterator it = self.pm_obj.begin()
        while not it.at_end():
            yield (dereference(it).first, dereference(it).second)
            preincrement(it)

    def keys(self):
        "Iterator throug the keys of this map"
        return iter(self)

    def values(self):
        "Iterator throug the values of this map"
        cdef pm_Map[string,string].iterator it = self.pm_obj.begin()
        while not it.at_end():
            yield dereference(it).second
            preincrement(it)

    def python(self):
        return dict(self.items())

cdef class MapIntInt(PmObject):
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def __getitem__(self, int key):
        return self.pm_obj[key]

    def __len__(self):
        return self.pm_obj.size()

    def __iter__(self):
        cdef pm_Map[int,int].iterator it = self.pm_obj.begin()
        while not it.at_end():
            yield dereference(it).first
            preincrement(it)

    def __contains__(self, int key):
        r"""
        TESTS:

        >>> import polymake
        >>> c = polymake.associahedron(3)
        >>> m = c.TWO_FACE_SIZES
        >>> 4 in m
        True
        >>> 5 in m
        True
        >>> 2 in m
        False
        >>> 'a' in m
        Traceback (most recent call last):
        ...
        TypeError: an integer is required
        """
        return self.pm_obj.exists(key)

    def items(self):
        "Iterator throug the pairs (key, value) of this map"
        cdef pm_Map[int,int].iterator it = self.pm_obj.begin()
        while not it.at_end():
            yield (dereference(it).first, dereference(it).second)
            preincrement(it)

    def keys(self):
        "Iterator throug the keys of this map"
        return iter(self)

    def values(self):
        "Iterator throug the values of this map"
        cdef pm_Map[int,int].iterator it = self.pm_obj.begin()
        while not it.at_end():
            yield dereference(it).second
            preincrement(it)

    def python(self):
        return dict(self.items())


cdef class MapRationalRational(PmObject):
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def __getitem__(self, Rational key):
        cdef Rational out = Rational.__new__(Rational)
        out.pm_obj = self.pm_obj[key.pm_obj]
        return out

    def __len__(self):
        return self.pm_obj.size()

    def __contains__(self, Rational key):
        r"""
        TESTS:

        >>> import polymake
        >>> c = polymake.associahedron(3)
        >>> m = c.RELATIVE_VOLUME
        >>> polymake.Rational(805,1) in m
        True
        >>> polymake.Rational(805,2) in m
        False
        """
        return self.pm_obj.exists(key.pm_obj)


cdef class MapIntegerInt(PmObject):
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def __getitem__(self, Integer key):
        return self.pm_obj[key.pm_obj]

    def __len__(self):
        return self.pm_obj.size()

    def __contains__(self, Integer key):
        return self.pm_obj.exists(key.pm_obj)

