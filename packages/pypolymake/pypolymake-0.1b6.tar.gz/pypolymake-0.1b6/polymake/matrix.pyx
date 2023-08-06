r"""
Polymake matrices

This file contains wrappers for polymake matrices

- Matrix
- SparseMatrix
- IncidenceMatrix

The matrix constructor accepts the following format:

- Matrix(): initialize an empty matrix
- Matrix(values): initialize a matrix from a list of lists
- Matrix(nr, nc): initialize a zero matrix from given sizes
- Matrix(nr, nc, values): initialize a matrix with given dimensions and values
  (either as a plain list or as a list of lists)
"""
###############################################################################
#       Copyright (C) 2011-2012 Burcin Erocal <burcin@erocal.org>
#                     2016-2019 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

from cpython.object cimport Py_LT, Py_LE, Py_EQ, Py_NE, Py_GT, Py_GE

from libcpp cimport bool
from libcpp.string cimport string

from libc.stdlib cimport malloc, free
from .cygmp.types cimport mpz_t, mpq_t, mpz_srcptr, mpq_srcptr
from .cygmp.mpz cimport *
from .cygmp.mpq cimport *

from .defs cimport pm_Integer, pm_Rational, pm_Matrix_get, pm_repr_wrap, ostringstream

from .integer cimport Integer
from .rational cimport Rational
from .quadratic_extension cimport QuadraticExtension

#    def python(self):
#        r"""Converts to a list of list of fractions
#
#        >>> import polymake
#
#        >>> c = polymake.cube(3)
#        >>> m = c.DEGREE_ONE_GENERATORS.python()
#        >>> m
#        [[1, -1, -1, -1],
#         [1, -1, -1, 0],
#         [1, -1, -1, 1],
#        ...
#         [1, 1, 1, 0],
#         [1, 1, 1, 1]]
#        >>> type(m), type(m[0]), type(m[0][0])
#        (<type 'list'>, <type 'list'>, <type 'int'>)
#
#        >>> c = polymake.cube(3)
#        >>> m = c.VERTEX_NORMALS.python()
#        >>> m
#        [[Fraction(1, 2), Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)],
#         [Fraction(1, 2), Fraction(-1, 2), Fraction(1, 2), Fraction(1, 2)],
#         [Fraction(1, 2), Fraction(1, 2), Fraction(-1, 2), Fraction(1, 2)],
#        ...
#         [Fraction(1, 2), Fraction(1, 2), Fraction(-1, 2), Fraction(-1, 2)],
#         [Fraction(1, 2), Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2)]]
#
#        >>> c = polymake.cube(3)
#        >>> m = c.EDGE_ORIENTATION.python()
#        [[0, 4],
#         [2, 6],
#         [0, 2],
#         ...
#         [2, 3],
#         [6, 7]]
#        >>> type(m), type(m[0]), type(m[0][0])
#        (<type 'list'>, <type 'list'>, <type 'int'>)
#        """
#        cdef Py_ssize_t i, j, nrows, ncols
#        nrows = self.rows()
#        ncols = self.cols()
#        try:
#            return [[self[i,j].python() for j in range(ncols)] for i in range(nrows)]
#        except AttributeError:
#            return [[self[i,j] for j in range(ncols)] for i in range(nrows)]

cdef class PmMatrix(PmObject):
    def __init__(self, *args):
        cdef int nr, nc

        if len(args) == 0:
            # zero matrix
            return

        elif len(args) == 1:
            if isinstance(args[0], PmMatrix):
                # a matrix
                self._set_matrix(args[0])
            else:
                # a list of lists
                nr = len(args[0])
                if not nr:
                    nc = 0
                else:
                    nc = len(args[0][0])
                self.resize(nr, nc)
                if nr and nc:
                    self._set_list_of_lists(args[0])

        elif len(args) == 2:
            # nr, nc
            self.resize(args[0], args[1])

        elif len(args) == 3:
            # nr, nc, data
            if not isinstance(args[2], (tuple, list)):
                raise TypeError
            self.resize(args[0], args[1])
            if not args[0] or not args[1]:
                return
            if isinstance(args[2][0], (tuple, list)):
                self._set_list_of_lists(args[2])
            else:
                self._set_plain_list(args[2])
        else:
            raise ValueError("invalid matrix input")

    cpdef resize(self, int nr, int nc): raise NotImplementedError
    cpdef int rows(self): raise NotImplementedError
    cpdef int cols(self): raise NotImplementedError
    cpdef _set_list_of_lists(self, data): raise NotImplementedError
    cpdef _set_matrix(self, mat): raise NotImplementedError
    cpdef _set_plain_list(self, mat): raise NotImplementedError

cdef class MatrixInt(PmMatrix):
    cpdef int rows(self): return self.pm_obj.rows()
    cpdef int cols(self): return self.pm_obj.cols()
    cpdef resize(self, int nr, int nc): self.pm_obj.resize(nr, nc)

    cpdef _set_list_of_lists(self, data):
        cdef int i, j
        for i,row in enumerate(data):
            for j,elt in enumerate(row):
                pm_Matrix_set(self.pm_obj, i, j, <int> elt)

    cpdef _set_matrix(self, mat):
        if isinstance(mat, MatrixInt):
            self.pm_obj = (<MatrixInt> mat).pm_obj
        else:
            raise NotImplementedError

    cpdef _set_plain_list(self, mat):
        cdef int i,j,k
        k = 0
        for i in range(self.pm_obj.rows()):
            for j in range(self.pm_obj.cols()):
                pm_Matrix_set(self.pm_obj, i, j, <int> (mat[k]))
                k += 1

    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def __getitem__(self, elt):
        cdef Py_ssize_t nrows, ncols, i,j
        nrows = self.pm_obj.rows()
        ncols = self.pm_obj.cols()
        i,j = elt
        if not (0 <= i < nrows) or not (0 <= j < ncols):
            raise IndexError("matrix index out of range")

        return pm_Matrix_get(self.pm_obj, i, j)

    cpdef _richcmp_(self, other, int op):
        cdef pm_Matrix[int] * left = & (<MatrixInt> self).pm_obj
        cdef pm_Matrix[int] * right = & (<MatrixInt> other).pm_obj

        if op == Py_EQ:
            return left[0] == right[0]
        elif op == Py_NE:
            return left[0] != right[0]
        else:
            raise NotImplementedError

    def sage(self):
        r"""
        Converts to a Sage matrix
        """
        from .sage_conversion import MatrixInt_to_sage
        return MatrixInt_to_sage(self)

    cpdef _add_(self, other):
        cdef MatrixInt ans = MatrixInt.__new__(MatrixInt)
        ans.pm_obj = (<MatrixInt> self).pm_obj + (<MatrixInt> other).pm_obj
        return ans

    cpdef _sub_(self, other):
        cdef MatrixInt ans = MatrixInt.__new__(MatrixInt)
        ans.pm_obj = (<MatrixInt> self).pm_obj - (<MatrixInt> other).pm_obj
        return ans

cdef class MatrixFloat(PmMatrix):
    cpdef int rows(self): return self.pm_obj.rows()
    cpdef int cols(self): return self.pm_obj.cols()
    cpdef resize(self, int nr, int nc): self.pm_obj.resize(nr, nc)

    cpdef _set_list_of_lists(self, data):
        cdef int i, j
        for i,row in enumerate(data):
            for j,elt in enumerate(row):
                pm_Matrix_set(self.pm_obj, i, j, <float> elt)

    cpdef _set_matrix(self, mat):
        if isinstance(mat, MatrixFloat):
            self.pm_obj = (<MatrixFloat> mat).pm_obj
        else:
            raise NotImplementedError

    cpdef _set_plain_list(self, mat):
        cdef int i,j,k
        k = 0
        for i in range(self.pm_obj.rows()):
            for j in range(self.pm_obj.cols()):
                pm_Matrix_set(self.pm_obj, i, j, <float> (mat[k]))
                k += 1

    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def __getitem__(self, elt):
        cdef Py_ssize_t nrows, ncols, i,j
        nrows = self.pm_obj.rows()
        ncols = self.pm_obj.cols()
        i,j = elt
        if not (0 <= i < nrows) or not (0 <= j < ncols):
            raise IndexError("matrix index out of range")

        return pm_Matrix_get(self.pm_obj, i, j)

    cpdef _richcmp_(self, other, int op):
        cdef pm_Matrix[float] * left = & (<MatrixFloat> self).pm_obj
        cdef pm_Matrix[float] * right = & (<MatrixFloat> other).pm_obj

        if op == Py_EQ:
            return left[0] == right[0]
        elif op == Py_NE:
            return left[0] != right[0]
        else:
            raise NotImplementedError

    def sage(self):
        r"""
        Converts to a Sage matrix
        """
        from .sage_conversion import MatrixFloat_to_sage
        return MatrixFloat_to_sage(self)

cdef class MatrixInteger(PmMatrix):
    cpdef int rows(self): return self.pm_obj.rows()
    cpdef int cols(self): return self.pm_obj.cols()
    cpdef resize(self, int nr, int nc): self.pm_obj.resize(nr, nc)

    cpdef _set_list_of_lists(self, data):
        cdef int i, j
        cdef Integer z
        for i,row in enumerate(data):
            for j,elt in enumerate(row):
                # TODO: we should not create a new integer each time but rather
                # reset the value
                z = Integer(elt)
                pm_Matrix_set(self.pm_obj, i, j, z.pm_obj)

    cpdef _set_matrix(self, mat):
        if isinstance(mat, MatrixFloat):
            self.pm_obj = (<MatrixFloat> mat).pm_obj
        else:
            raise NotImplementedError

    cpdef _set_plain_list(self, mat):
        cdef int i,j,k
        cdef Integer z
        k = 0
        for i in range(self.pm_obj.rows()):
            for j in range(self.pm_obj.cols()):
                z = Integer(mat[k])
                pm_Matrix_set(self.pm_obj, i, j, z.pm_obj)
                k += 1

    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def __getitem__(self, elt):
        cdef Py_ssize_t nrows, ncols, i,j
        nrows = self.pm_obj.rows()
        ncols = self.pm_obj.cols()
        i,j = elt
        if not (0 <= i < nrows) or not (0 <= j < ncols):
            raise IndexError("matrix index out of range")

        cdef Integer ans = Integer.__new__(Integer)
        ans.pm_obj.set_mpz_srcptr(pm_Matrix_get(self.pm_obj, i, j).get_rep())
        return ans

    cpdef _richcmp_(self, other, int op):
        cdef pm_Matrix[pm_Integer] * left = & (<MatrixInteger> self).pm_obj
        cdef pm_Matrix[pm_Integer] * right = & (<MatrixInteger> other).pm_obj

        if op == Py_EQ:
            return left[0] == right[0]
        elif op == Py_NE:
            return left[0] != right[0]
        else:
            raise NotImplementedError

    def sage(self):
        r"""
        Converts to a Sage integer matrix
        """
        from .sage_conversion import MatrixInteger_to_sage
        return MatrixInteger_to_sage(self)

cdef class MatrixRational(PmMatrix):
    cpdef int rows(self): return self.pm_obj.rows()
    cpdef int cols(self): return self.pm_obj.cols()
    cpdef resize(self, int nr, int nc): self.pm_obj.resize(nr, nc)

    cpdef _set_list_of_lists(self, data):
        cdef int i, j
        cdef Rational q
        for i,row in enumerate(data):
            for j,elt in enumerate(row):
                # TODO: we should not create a new rational each time
                # but rather reset the value
                q = Rational(elt)
                pm_Matrix_set(self.pm_obj, i, j, q.pm_obj)

    cpdef _set_matrix(self, mat):
        if isinstance(mat, MatrixFloat):
            self.pm_obj = (<MatrixFloat> mat).pm_obj
        else:
            raise NotImplementedError

    cpdef _set_plain_list(self, mat):
        cdef int i,j,k
        cdef Rational q
        k = 0
        for i in range(self.pm_obj.rows()):
            for j in range(self.pm_obj.cols()):
                # TODO: we should not create a new rational each time
                # but rather reset the value
                q = Rational(mat[k])
                pm_Matrix_set(self.pm_obj, i, j, q.pm_obj)
                k += 1

    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def __getitem__(self, elt):
        cdef Py_ssize_t nrows, ncols, i, j
        nrows = self.pm_obj.rows()
        ncols = self.pm_obj.cols()
        i,j = elt
        if not (0 <= i < nrows) or not (0 <= j < ncols):
            raise IndexError("matrix index out of range")

        cdef Rational ans = Rational.__new__(Rational)
        cdef mpq_srcptr q = pm_Matrix_get(self.pm_obj, i, j).get_rep()
        ans.pm_obj.set_mpq_srcptr(q)
        return ans

    cpdef _richcmp_(self, other, int op):
        cdef pm_Matrix[pm_Rational] * left = & (<MatrixRational> self).pm_obj
        cdef pm_Matrix[pm_Rational] * right = & (<MatrixRational> other).pm_obj

        if op == Py_EQ:
            return left[0] == right[0]
        elif op == Py_NE:
            return left[0] != right[0]
        else:
            raise NotImplementedError

    def sage(self):
        r"""
        Converts into a Sage matrix
        """
        from .sage_conversion import MatrixRational_to_sage
        return MatrixRational_to_sage(self)

cdef class MatrixQuadraticExtension(PmMatrix):
    cpdef int rows(self): return self.pm_obj.rows()
    cpdef int cols(self): return self.pm_obj.cols()
    cpdef resize(self, int nr, int nc): self.pm_obj.resize(nr, nc)

    cpdef _set_list_of_lists(self, data):
        cdef int i, j
        cdef QuadraticExtension qe
        for i,row in enumerate(data):
            for j,elt in enumerate(row):
                # TODO: we should not create a new quadratic extension
                # integer each time but rather reset the value
                qe = QuadraticExtension(elt)
                pm_Matrix_set(self.pm_obj, i, j, qe.pm_obj)

    cpdef _set_matrix(self, mat):
        if isinstance(mat, MatrixFloat):
            self.pm_obj = (<MatrixFloat> mat).pm_obj
        else:
            raise NotImplementedError

    cpdef _set_plain_list(self, mat):
        cdef int i,j,k
        cdef QuadraticExtension qe
        k = 0
        for i in range(self.pm_obj.rows()):
            for j in range(self.pm_obj.cols()):
                # TODO: we should not create a new quadratic extension
                # integer each time but rather reset the value
                qe = QuadraticExtension(mat[k])
                pm_Matrix_set(self.pm_obj, i, j, qe.pm_obj)
                k += 1

    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

    def __getitem__(self, elt):
        cdef Py_ssize_t nrows, ncols, i, j
        nrows = self.pm_obj.rows()
        ncols = self.pm_obj.cols()
        i,j = elt
        if not (0 <= i < nrows) or not (0 <= j < ncols):
            raise IndexError("matrix index out of range")

        cdef QuadraticExtension ans = QuadraticExtension.__new__(QuadraticExtension)
        # TODO: this is a lot of useless copies
        cdef pm_Rational qa = pm_Matrix_get(self.pm_obj, i, j).a()
        cdef pm_Rational qb = pm_Matrix_get(self.pm_obj, i, j).b()
        cdef pm_Rational qr = pm_Matrix_get(self.pm_obj, i, j).r()
        ans.pm_obj = pm_QuadraticExtension(qa, qb, qr)
        return ans

    def sage(self, field=None):
        from .sage_conversion import MatrixQuadraticExtension_to_sage
        return MatrixQuadraticExtension_to_sage(self, field)
