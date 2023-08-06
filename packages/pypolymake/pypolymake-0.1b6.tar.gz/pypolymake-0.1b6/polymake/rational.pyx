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
from .cygmp.mpq cimport mpq_init, mpq_clear, mpq_numref, mpq_denref, mpq_canonicalize
from .cygmp.utils cimport mpz_set_pylong, mpz_get_bytes, mpq_get_bytes

from libcpp.string cimport string

from .defs cimport pm_Integer, ostringstream, pm_repr
from .integer cimport Integer

def get_num_den(elt):
    if isinstance(elt, (tuple, list)):
        if len(elt) == 2:
            num, den = elt
        else:
            raise ValueError("no conversion to rational")
        if not isinstance(num, numbers.Integral) or not isinstance(den, numbers.Integral):
            raise ValueError("no conversion to rational")

    elif isinstance(elt, numbers.Rational):
        num = elt.numerator
        den = elt.denominator

        # Sage rational are not complient with Numbers abc
        if callable(num) and callable(den):
            num = num()
            den = den()
    else:
        raise TypeError("no conversion to rational")

    return (num, den)

cdef class Rational(PmObject):
    r"""Polymake rational

    >>> import polymake
    >>> polymake.Rational(3)
    3
    >>> polymake.Rational(2, 7)
    2/7
    >>> polymake.Rational((2,7))
    2/7

    >>> polymake.Rational(polymake.Integer(-3))
    -3
    >>> polymake.Rational(polymake.Integer(-3), polymake.Integer(19))
    -3/19
    >>> polymake.Rational(polymake.Integer(-3), 19)
    -3/19
    >>> polymake.Rational(-3, polymake.Integer(19))
    -3/19

    >>> polymake.Rational(polymake.Rational(2, 5))
    2/5

    >>> polymake.Rational(polymake.Rational(2, 5), polymake.Rational(3,7))
    Traceback (most recent call last):
    ...
    ValueError: invalid argument for polymake Rational
    >>> polymake.Rational((polymake.Rational(1,2), polymake.Rational(2,3)))
    Traceback (most recent call last):
    ...
    ValueError: no conversion to rational
    """
    def __init__(self, num, den=None):
        if den is None:
            num, den = get_num_den(num)
        elif not isinstance(num, numbers.Integral) or not isinstance(den, numbers.Integral):
            raise ValueError("invalid argument for polymake Rational")

        if not den:
            raise ValueError("denominator must not be zero")

        cdef mpq_t z
        mpq_init(z)
        if isinstance(num, Integer):
            mpz_set(mpq_numref(z), (<Integer> num).pm_obj.get_rep())
        elif isinstance(num, long):
            mpz_set_pylong(mpq_numref(z), num)
        elif isinstance(num, int):  # Python 2 only
            mpz_set_si(mpq_numref(z), num)
        else:
            num = num.__index__()
            if isinstance(num, long):
                mpz_set_pylong(mpq_numref(z), num)
            elif isinstance(num, int):  # Python 2 only
                mpz_set_si(mpq_numref(z), num)

        if isinstance(den, Integer):
            mpz_set(mpq_denref(z), (<Integer> den).pm_obj.get_rep())
        elif isinstance(den, long):
            mpz_set_pylong(mpq_denref(z), den)
        elif isinstance(den, int):  # Python 2 only
            mpz_set_si(mpq_denref(z), den)
        else:
            den = den.__index__()
            if isinstance(den, long):
                mpz_set_pylong(mpq_denref(z), den)
            elif isinstance(den, int):  # Python 2 only
                mpz_set_si(mpq_denref(z), den)

        mpq_canonicalize(z)
        self.pm_obj.set_mpq_srcptr(<mpq_srcptr>z)
        mpq_clear(z)

    def __mpq__(self):
        # TODO: go directly through mpq initialization
        import gmpy2
        return gmpy2.mpq(int(self.numerator()), int(self.denominator()))

    def sage(self):
        r"""
        Converts this rational to Sage
        """
        from .sage_conversion import Rational_to_sage
        return Rational_to_sage(self)

    _rational_ = sage

    def python(self):
        r"""Converts to a python fraction

        >>> import polymake
        >>> c = polymake.Rational(12, 5)
        """
        from fractions import Fraction
        return Fraction(self.numerator().python(), self.denominator().python())

    def __nonzero__(self):
        return not pm_is_zero(self.pm_obj)

    cpdef _richcmp_(self, other, int op):
        cdef int c = (<Rational>self).pm_obj.compare((<Rational>other).pm_obj)
        if c < 0:
            return op in (Py_LE, Py_LT, Py_NE)
        elif c == 0:
            return op in (Py_LE, Py_EQ, Py_GE)
        else:
            return op in (Py_GE, Py_GT, Py_NE)

    def __repr__(self):
        cdef ostringstream out
        pm_repr(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def numerator(self):
        cdef Integer ans = Integer.__new__(Integer)
        cdef mpq_srcptr z = self.pm_obj.get_rep()
        ans.pm_obj.set_mpz_srcptr(mpq_numref(z))
        return ans

    def denominator(self):
        cdef Integer ans = Integer.__new__(Integer)
        cdef mpq_srcptr z = self.pm_obj.get_rep()
        ans.pm_obj.set_mpz_srcptr(mpq_denref(z))
        return ans

    cpdef _add_(self, other):
        r"""
        >>> from polymake import Integer, Rational
        >>> Rational(1,2) + Rational(1,2)
        1
        >>> Rational(1) + Integer(2)
        3
        >>> Integer(2) + Rational(1)
        3
        >>> Rational(2,3) + 318
        956/3
        >>> -2 + Rational(3,4)
        -5/4
        """
        cdef Rational ans = Rational.__new__(Rational)
        ans.pm_obj = (<Rational>self).pm_obj + (<Rational>other).pm_obj
        return ans

    cpdef _sub_(self, other):
        cdef Rational ans = Rational.__new__(Rational)
        ans.pm_obj = (<Rational>self).pm_obj - (<Rational>other).pm_obj
        return ans

    cpdef _mul_(self, other):
        cdef Rational ans = Rational.__new__(Rational)
        ans.pm_obj = (<Rational>self).pm_obj * (<Rational>other).pm_obj
        return ans

    cpdef _div_(self, other):
        r"""
        >>> from polymake import Rational
        >>> Rational(2,3) / Rational(5,7)
        14/15
        """
        cdef Rational ans = Rational.__new__(Rational)
        ans.pm_obj = (<Rational>self).pm_obj / (<Rational>other).pm_obj
        return ans

    def __pow__(self, n, mod):
        r"""
        >>> from polymake import Integer, Rational
        >>> Rational(2,3) ** 5
        32/243
        >>> Rational(2,3) ** Integer(5)
        32/243
        >>> Rational(2,3) ** (-5)
        243/32
        >>> Rational(2,3) ** (2**100)
        Traceback (most recent call last):
        ...
        OverflowError: Python int too large to convert to C long
        """
        if type(self) is not Rational:
            return NotImplemented
        cdef Rational ans = Rational.__new__(Rational)
        if isinstance(n, (int, long)):
            ans.pm_obj = pm_pow((<Rational> self).pm_obj, PyLong_AsLong(n))
        elif isinstance(n, Integer):
            ans.pm_obj = pm_pow((<Rational> self).pm_obj, <long> (<Integer> n).pm_obj)
        else:
            n = Integer(n)
            ans.pm_obj = pm_pow((<Rational> self).pm_obj, <long> (<Integer> n).pm_obj)
        return ans

import numbers
numbers.Rational.register(Rational)
