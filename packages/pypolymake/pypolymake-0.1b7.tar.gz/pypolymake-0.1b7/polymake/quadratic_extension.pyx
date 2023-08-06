###############################################################################
#       Copyright (C) 2016-2019 Vincent Delecroix <vincent.delecroix@labri.fr> 
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

from cpython.object cimport Py_LT, Py_LE, Py_EQ, Py_NE, Py_GT, Py_GE

from libcpp cimport bool
from libcpp.string cimport string

from .defs cimport pm_QuadraticExtension, pm_repr_wrap
from .integer cimport Integer
from .rational cimport Rational

import numbers

# this is a bug in Cython!
def _NOT_TO_BE_USED_():
    raise ValueError
def _NOT_TO_BE_USED_():
    raise TypeError

cpdef Rational to_rat(a):
    if type(a) is Rational:
        return a
    elif a is None:
        return Rational(0)
    else:
        return Rational(a)

cdef class QuadraticExtension(PmObject):
    r"""
    Element of a quadratic extension of the rational numbers

    This class implements numbers of the form a + b sqrt(r).
    """
    def __init__(self, a=None, b=None, r=None):
        if a is None and b is None:
            return

        if b is None and r is None:
            if type(a) is QuadraticExtension:
                self.pm_obj = (<QuadraticExtension> a).pm_obj
                return
            elif isinstance(a, (list, tuple)):
                if len(a) == 3:
                    a, b, r = a
                else:
                    raise ValueError

        cdef Rational ra = to_rat(a)
        if b is None or r is None:
            self.pm_obj = pm_QuadraticExtension(ra.pm_obj)
            return

        cdef Rational rb = to_rat(b)
        cdef Rational rr = to_rat(r)

        self.pm_obj = pm_QuadraticExtension(ra.pm_obj, rb.pm_obj, rr.pm_obj)

    def __nonzero__(self):
        return not pm_is_zero(self.pm_obj)

    def a(self):
        cdef Rational a = Rational.__new__(Rational)
        a.pm_obj.set_mpq_srcptr(self.pm_obj.a().get_rep())
        return a

    def b(self):
        cdef Rational b = Rational.__new__(Rational)
        b.pm_obj.set_mpq_srcptr(self.pm_obj.b().get_rep())
        return b

    def r(self):
        cdef Rational r = Rational.__new__(Rational)
        r.pm_obj.set_mpq_srcptr(self.pm_obj.r().get_rep())
        return r

    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    cpdef _add_(self, other):
        cdef QuadraticExtension ans = QuadraticExtension.__new__(QuadraticExtension)
        ans.pm_obj = (<QuadraticExtension> self).pm_obj + \
                     (<QuadraticExtension> other).pm_obj
        return ans

    cpdef _sub_(self, other):
        cdef QuadraticExtension ans = QuadraticExtension.__new__(QuadraticExtension)
        ans.pm_obj = (<QuadraticExtension> self).pm_obj - \
                     (<QuadraticExtension> other).pm_obj
        return ans

    cpdef _mul_(self, other):
        cdef QuadraticExtension ans = QuadraticExtension.__new__(QuadraticExtension)
        ans.pm_obj = (<QuadraticExtension> self).pm_obj * \
                     (<QuadraticExtension> other).pm_obj
        return ans

    cpdef _div_(self, other):
        cdef QuadraticExtension ans = QuadraticExtension.__new__(QuadraticExtension)
        ans.pm_obj = (<QuadraticExtension> self).pm_obj / \
                     (<QuadraticExtension> other).pm_obj
        return ans

    cpdef _richcmp_(self, other, int op):
        cdef QuadraticExtension a = <QuadraticExtension> self
        cdef QuadraticExtension b = <QuadraticExtension> other

        if a.pm_obj == b.pm_obj:
            return op in [Py_EQ, Py_LE, Py_GE]
        elif op == Py_NE:
            return True
        elif op == Py_EQ:
            return False

        if a.pm_obj < b.pm_obj:
            return op in [Py_LE, Py_LT]
        else:
            return op in [Py_GE, Py_GT]

    def __neg__(self):
        cdef QuadraticExtension ans = QuadraticExtension.__new__(QuadraticExtension)
        ans.pm_obj = - self.pm_obj
        return ans

    def sage(self, field=None):
        r"""
        Convert this quadratic extension element to SageMath
        """
        from .sage_conversion import QuadraticExtension_to_sage
        return QuadraticExtension_to_sage(self, field)

import numbers
numbers.Real.register(QuadraticExtension)
