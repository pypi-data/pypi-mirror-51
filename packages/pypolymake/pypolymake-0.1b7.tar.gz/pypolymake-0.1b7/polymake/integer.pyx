###############################################################################
#       Copyright (C) 2016-2019 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

from cpython.object cimport Py_LT, Py_LE, Py_EQ, Py_NE, Py_GT, Py_GE
from cpython.long cimport PyLong_AsLong

from .cygmp.types cimport mpz_t, mpq_t, mpz_srcptr, mpq_srcptr
from .cygmp.mpz cimport mpz_init, mpz_clear, mpz_set_si, mpz_set
from .cygmp.mpq cimport mpq_init, mpq_clear, mpq_canonicalize, mpq_numref, mpq_denref
from .cygmp.utils cimport mpz_set_pylong, mpz_get_pyintlong, mpz_get_bytes, mpq_get_bytes, mpz_get_d_nearest, mpz_get_pylong

from libcpp.string cimport string

from .defs cimport pm_Rational, ostringstream, pm_repr
from .rational cimport Rational

cdef class Integer(PmObject):
    r"""
    Polymake integer
    """
    def __init__(self, data):
        r"""
        >>> from polymake import Integer
        >>> Integer(2)
        2
        >>> Integer(Integer(2))
        2
        """
        cdef mpz_t z

        if isinstance(data, Integer):
            self.pm_obj.set_mpz_srcptr((<Integer>data).pm_obj.get_rep())
            return

        elif not isinstance(data, (int, long)):
            data = data.__index__()

        mpz_init(z)

        if isinstance(data, long):
            mpz_set_pylong(z, data)
        elif isinstance(data, int): # only Python 2
            mpz_set_si(z, data)

        self.pm_obj.set_mpz_srcptr(<mpz_srcptr>z)
        mpz_clear(z)

    def __mpz__(self):
        # TODO: go directly through mpz initialization
        import gmpy2
        return gmpy2.mpz(int(self))

    def __index__(self):
        return mpz_get_pyintlong(self.pm_obj.get_rep())

    def __int__(self):
        return mpz_get_pyintlong(self.pm_obj.get_rep())

    def __long__(self):
        return mpz_get_pylong(self.pm_obj.get_rep())

    def __float__(self):
        return mpz_get_d_nearest(self.pm_obj.get_rep())

    python = __index__

    def _integer_(self, R=None):
        r"""
        Conversion to Sage integer
        """
        return R(self.sage())

    def numerator(self):
        return self

    def denominator(self):
        return Integer(1)

    def __nonzero__(self):
        return not pm_is_zero(self.pm_obj)

    def __repr__(self):
        cdef ostringstream out
        pm_repr(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def __float__(self):
        return <double> self.pm_obj

    # TODO: in python 3 the management of python integers is completely wrong
    cpdef _richcmp_(self, other, int op):
        cdef int c = (<Integer>self).pm_obj.compare((<Integer>other).pm_obj)
        if c < 0:
            return op in (Py_LE, Py_LT, Py_NE)
        elif c == 0:
            return op in (Py_LE, Py_EQ, Py_GE)
        else:
            return op in (Py_GE, Py_GT, Py_NE)

    cpdef _add_(self, other):
        cdef Integer ans = Integer.__new__(Integer)
        ans.pm_obj = (<Integer>self).pm_obj + (<Integer>other).pm_obj
        return ans

    cpdef _sub_(self, other):
        cdef Integer ans = Integer.__new__(Integer)
        ans.pm_obj = (<Integer>self).pm_obj - (<Integer>other).pm_obj
        return ans

    cpdef _mul_(self, other):
        cdef Integer ans = Integer.__new__(Integer)
        ans.pm_obj = (<Integer>self).pm_obj * (<Integer>other).pm_obj
        return ans

    cpdef _floordiv_(self, other):
        cdef Integer ans = Integer.__new__(Integer)
        ans.pm_obj = (<Integer>self).pm_obj / (<Integer>other).pm_obj
        return ans

    cpdef _div_(self, other):
        cdef mpq_t q
        if not other:
            raise ZeroDivisionError
        mpq_init(q)
        mpz_set(mpq_numref(q), (<Integer> self).pm_obj.get_rep())
        mpz_set(mpq_denref(q), (<Integer> other).pm_obj.get_rep())
        mpq_canonicalize(q)
        cdef Rational ans = Rational.__new__(Rational)
        ans.pm_obj.set_mpq_srcptr(q)
        mpq_clear(q)
        return ans

    def __neg__(self):
        cdef Integer ans = Integer.__new__(Integer)
        ans.pm_obj = -self.pm_obj
        return ans

    def __pow__(self, n, mod):
        if type(self) is not Integer:
            return NotImplemented
        cdef Integer ans = Integer.__new__(Integer)
        if isinstance(n, (int, long)):
            ans.pm_obj = pm_pow((<Integer> self).pm_obj, PyLong_AsLong(n))
        elif isinstance(n, Integer):
            ans.pm_obj = pm_pow((<Integer> self).pm_obj, <long> (<Integer> n).pm_obj)
        else:
            n = Integer(n)
            ans.pm_obj = pm_pow((<Integer> self).pm_obj, <long> (<Integer> n).pm_obj)
        return ans

    def sage(self):
        r"""
        Converts to a Sage integer
        """
        from .sage_conversion import Integer_to_sage
        return Integer_to_sage(self)

import numbers
numbers.Integral.register(Integer)
