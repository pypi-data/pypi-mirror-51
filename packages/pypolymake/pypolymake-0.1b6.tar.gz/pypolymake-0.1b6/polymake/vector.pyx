###############################################################################
#       Copyright (C) 2011-2012 Burcin Erocal <burcin@erocal.org>
#                     2016-2019 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

from cpython.object cimport Py_LT, Py_LE, Py_EQ, Py_NE, Py_GT, Py_GE

from .integer cimport Integer
from .rational cimport Rational

import numbers

cdef class VectorInteger(PmObject):
    r"""
    A vector of integers

    >>> import polymake
    >>> v = polymake.VectorInteger([-3,1,2**80,13])
    >>> v
    -3 1 1208925819614629174706176 13
    >>> v[0]
    -3
    >>> v[-1]
    13
    """
    def __init__(self, data=None):
        if data is None:
            return
        elif isinstance(data, numbers.Integral):
            self.pm_obj.resize(<int> data)
        elif isinstance(data, VectorInteger):
            self._init_from_pm_Vector(<VectorInteger> data)
        else:
            self._init_from_iterable(data)

    def __copy__(self):
        cdef VectorInteger other = VectorInteger.__new__(VectorInteger)
        other.pm_obj = self.pm_obj
        return other

    def _init_from_pm_Vector(self, VectorInteger v):
        self.pm_obj = v.pm_obj

    def _init_from_iterable(self, data):
        cdef vector[pm_Integer] vv
        cdef Integer z
        for i,j in enumerate(data):
            z = Integer(j)
            vv.push_back(z.pm_obj)
        self.pm_obj = vv

    def __len__(self):
        return self.pm_obj.size()

    size = __len__

    def __getitem__(self, _i):
        cdef Py_ssize_t size = self.pm_obj.size()
        cdef Py_ssize_t i = <Py_ssize_t?> _i

        if i < 0:
            i += size

        if not (0 <= i < size):
            raise IndexError("integer vector out of range")

        cdef Integer ans = Integer.__new__(Integer)
        ans.pm_obj.set_mpz_srcptr(self.pm_obj[i].get_rep())
        return ans

    cpdef _richcmp_(self, other, int op):
        if op == Py_EQ:
            return (<VectorInteger> self).pm_obj == (<VectorInteger> other).pm_obj
        elif op == Py_NE:
            return (<VectorInteger> self).pm_obj != (<VectorInteger> other).pm_obj
        else:
            raise TypeError

    cpdef _add_(self, other):
        r"""
        >>> import polymake
        >>> polymake.VectorInteger([1,3]) + polymake.VectorInteger([-3,-3])
        -2 0
        """
        cdef VectorInteger left = <VectorInteger> self
        cdef VectorInteger right = <VectorInteger> other
        cdef VectorInteger ans = VectorInteger.__new__(VectorInteger)
        ans.pm_obj = left.pm_obj + right.pm_obj
        return ans

    cpdef _sub_(self, other):
        r"""
        >>> import polymake
        >>> polymake.VectorInteger([1,3]) - polymake.VectorInteger([-3,-3])
        4 6
        """
        cdef VectorInteger left = <VectorInteger> self
        cdef VectorInteger right = <VectorInteger> other
        cdef VectorInteger ans = VectorInteger.__new__(VectorInteger)
        ans.pm_obj = left.pm_obj - right.pm_obj
        return ans

    def __neg__(self):
        cdef VectorInteger other = self.__copy__()
        other.pm_obj.negate()
        return other

    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def python(self):
        return [x.python() for x in self]

    def sage(self):
        r"""
        Convert to a Sage integer vector
        """
        from .sage_conversion import VectorInteger_to_sage
        return VectorInteger_to_sage(self)

cdef class VectorRational(PmObject):
    r"""
    Vector of rationals

    >>> import polymake
    >>> v = polymake.VectorRational([1, (2,3), (-3,5)])
    >>> v
    1 2/3 -3/5
    >>> v[-1]
    -3/5
    """
    def __init__(self, data=None):
        if data is None:
            return
        elif isinstance(data, numbers.Integral):
            self.pm_obj.resize(<int> data)
        elif isinstance(data, VectorRational):
            self._init_from_pm_Vector(<VectorRational> data)
        else:
            self._init_from_iterable(data)

    def __copy__(self):
        cdef VectorRational other = VectorRational.__new__(VectorRational)
        other.pm_obj = self.pm_obj
        return other

    def _init_from_pm_Vector(self, VectorRational v):
        self.pm_obj = v.pm_obj

    def _init_from_iterable(self, data):
        cdef vector[pm_Rational] vv
        cdef Rational z
        for i,j in enumerate(data):
            z = Rational(j)
            vv.push_back(z.pm_obj)
        self.pm_obj = vv

    def __len__(self):
        return self.pm_obj.size()

    size = __len__

    def __getitem__(self, _i):
        cdef Py_ssize_t size = self.pm_obj.size()
        cdef Py_ssize_t i = <Py_ssize_t?> _i

        if i < 0:
            i += size

        if not (0 <= i < size):
            raise IndexError("integer vector out of range")

        cdef Rational ans = Rational.__new__(Rational)
        ans.pm_obj.set_mpq_srcptr(self.pm_obj[i].get_rep())
        return ans

    cpdef _richcmp_(self, other, int op):
        if op == Py_EQ:
            return (<VectorRational> self).pm_obj == (<VectorRational> other).pm_obj
        elif op == Py_NE:
            return (<VectorRational> self).pm_obj != (<VectorRational> other).pm_obj
        else:
            raise TypeError

    cpdef _add_(self, other):
        r"""
        >>> import polymake
        >>> polymake.VectorRational([1,(2,3)]) + polymake.VectorRational([-3,-3])
        -2 0
        >>> polymake.VectorRational([(2,3),(1,2)]) + polymake.VectorInteger([1,1])
        5/3 3/2
        >>> polymake.VectorInteger([1,1]) + polymake.VectorRational([(2,3),(1,2)])
        5/3 3/2
        """
        cdef VectorRational left = <VectorRational> self
        cdef VectorRational right = <VectorRational> other
        cdef VectorRational ans = VectorRational.__new__(VectorRational)
        ans.pm_obj = left.pm_obj + right.pm_obj
        return ans

    cpdef _sub_(self, other):
        r"""
        >>> import polymake
        >>> polymake.VectorRational([1,3]) - polymake.VectorRational([-3,-3])
        4 6
        """
        cdef VectorRational left = <VectorRational> self
        cdef VectorRational right = <VectorRational> other
        cdef VectorRational ans = VectorRational.__new__(VectorRational)
        ans.pm_obj = left.pm_obj - right.pm_obj
        return ans

    def __neg__(self):
        cdef VectorRational other = self.__copy__()
        other.pm_obj.negate()
        return other

    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def python(self):
        return [x.python() for x in self]

    def sage(self):
        from .sage_conversion import VectorRational_to_sage
        return VectorRational_to_sage(self)
