# cython: preliminary_late_includes_cy28=False
r"""
Conversion of small Polymake objects to Sage

The implementation is done at C++ level and should be fast enough
in practice.
"""
###############################################################################
#       Copyright (C) 2017-2019  Vincent Delecroix <vincent.delecroix@labri.fr> 
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

from __future__ import absolute_import

from libcpp.vector cimport vector

from .defs cimport pm_Matrix_get, pm_Integer, pm_Rational
from .integer cimport Integer
from .rational cimport Rational
from .vector cimport VectorInteger, VectorRational
from .matrix cimport MatrixInt, MatrixFloat, MatrixInteger, MatrixRational
from .quadratic_extension cimport QuadraticExtension
from .perl_object cimport PerlObject
from .big_object import PolytopeRational, PolytopeQuadraticExtension

from .cygmp.types cimport mpz_t, mpq_t
from .cygmp.mpz cimport mpz_set, mpz_neg
from .cygmp.mpq cimport mpq_init, mpq_clear, mpq_set, mpq_numref, mpq_denref, mpq_canonicalize

from sage.all import (ZZ, QQ, AA, RIF, RDF, QuadraticField, NumberField,
        polygen, PolynomialRing, FreeModule, MatrixSpace, parent, matrix)
from sage.rings.number_field.number_field import NumberField_quadratic

from sage.libs.flint.fmpq cimport fmpq_set_mpq
from sage.libs.flint.fmpq_mat cimport fmpq_mat_entry

from sage.ext.stdsage cimport PY_NEW
from sage.structure.parent cimport Parent
from sage.rings.number_field.number_field_element_quadratic cimport NumberFieldElement_quadratic
from sage.rings.integer cimport Integer as sage_Integer
from sage.rings.rational cimport Rational as sage_Rational

from sage.modules.vector_integer_dense cimport Vector_integer_dense as sage_Vector_integer_dense
from sage.modules.vector_rational_dense cimport Vector_rational_dense as sage_Vector_rational_dense
from sage.matrix.matrix_rational_dense cimport Matrix_rational_dense as sage_Matrix_rational_dense
from sage.matrix.matrix_integer_dense cimport Matrix_integer_dense as sage_Matrix_integer_dense

def Integer_to_sage(Integer n):
    cdef sage_Integer ans = PY_NEW(sage_Integer)
    ans.set_from_mpz(<mpz_t>n.pm_obj.get_rep())
    return ans

def Rational_to_sage(Rational q):
    cdef sage_Rational ans = sage_Rational.__new__(sage_Rational)
    ans.set_from_mpq(<mpq_t>q.pm_obj.get_rep())
    return ans

class SageQuadraticFieldToPolymake(object):
    def __init__(self, K):
        if not isinstance(K, NumberField_quadratic):
            raise ValueError("K must be a quadratic field")

        self._K = K

    def __call__(self, elt):
        K = self._K
        if parent(elt) is not K:
            elt = K(elt)

        cdef mpq_t q
        cdef Rational a, b
        a = Rational.__new__(Rational)
        mpq_init(q)
        mpz_set(mpq_numref(q), (<NumberFieldElement_quadratic> elt).a)
        mpz_set(mpq_denref(q), (<NumberFieldElement_quadratic> elt).denom)
        mpq_canonicalize(q)
        a.pm_obj.set_mpq_srcptr(q)

        b = Rational.__new__(Rational)
        mpz_set(mpq_numref(q), (<NumberFieldElement_quadratic> elt).b)
        mpz_set(mpq_denref(q), (<NumberFieldElement_quadratic> elt).denom)
        if not K._standard_embedding:
            mpz_neg(mpq_numref(q), mpq_numref(q))
        mpq_canonicalize(q)
        b.pm_obj.set_mpq_srcptr(q)
        mpq_clear(q)

        return QuadraticExtension(a, b, int(K._D))

def QuadraticExtension_to_sage(QuadraticExtension z, field=None):
    cdef pm_Rational pm_r = z.pm_obj.r()
    cdef sage_Integer denom
    cdef sage_Rational a, b, r
    cdef NumberFieldElement_quadratic ans

    if pm_r == 0:
        a = sage_Rational.__new__(sage_Rational)
        mpq_set(a.value, z.pm_obj.a().get_rep())
        if field is not None:
            return field(a)
        else:
            return a
    else:
        a = sage_Rational.__new__(sage_Rational)
        b = sage_Rational.__new__(sage_Rational)
        r = sage_Rational.__new__(sage_Rational)
        mpq_set(a.value, z.pm_obj.a().get_rep())
        mpq_set(b.value, z.pm_obj.b().get_rep())
        mpq_set(r.value, pm_r.get_rep())

        if field is None and r.is_square():
            field = QQ

        if field is QQ:
            if not b:
                return a
            else:
                num_root, num_rem = r.numerator().sqrtrem()
                den_root, den_rem = r.denominator().sqrtrem()
                if num_rem or den_rem:
                    raise ValueError("not rational")
                return a + b * num_root / den_root

        if field is None:
            x = polygen(QQ, 'x')
            D = (r.numerator() * r.denominator()).squarefree_part()
            K = QuadraticField(D, 'sqrt{}'.format(D), embedding=AA(D).sqrt())
        elif not isinstance(field, NumberField_quadratic):
            raise ValueError("field must be a quadratic number field")
        else:
            K = field

        D = K._D   # should we access this hidden attribute?
        if not D.is_squarefree():
            raise RuntimeError

        q = r / D
        num_scale, num_rem = q.numerator().sqrtrem()
        den_scale, den_rem = q.denominator().sqrtrem()
        if num_rem or den_rem:
            raise ValueError("invalid Sage number field for polymake QuadraticExtension")

        b *= num_scale
        b /= den_scale

        denom = a.denominator().lcm(b.denominator())
        a *= denom
        b *= denom
        # WARNING: calling K(0) or K(1) will *always* create the same element
        # again and again (the cached zero and one respectively)
        ans = K.zero().__copy__()
        mpz_set(ans.a, mpq_numref(a.value))
        mpz_set(ans.b, mpq_numref(b.value))
        mpz_set(ans.denom, denom.value)

        if not ans.standard_embedding:
            mpz_neg(ans.b, ans.b)

        return ans

def QuadraticExtension_from_sage(NumberFieldElement_quadratic x):
    return SageQuadraticFieldToPolymake(x.parent())(x)

#def SetInt_to_sage(SetInt a):
#    pass

def VectorInteger_to_sage(VectorInteger v):
    V = FreeModule(ZZ, len(v))
    cdef sage_Vector_integer_dense ans = V.zero().__copy__()
    cdef int i
    for i in range(len(v)):
        mpz_set(ans._entries[i], v.pm_obj[i].get_rep())
    return ans

def VectorInteger_from_sage(sage_Vector_integer_dense v):
    cdef vector[pm_Integer] data
    cdef int i
    cdef pm_Integer z
    for i in range(v._degree):
        z.set_mpz_srcptr(v._entries[i])
        data.push_back(z)

    cdef VectorInteger ans = VectorInteger.__new__(VectorInteger)
    ans.pm_obj = data
    return ans

def VectorRational_to_sage(VectorRational v):
    V = FreeModule(QQ, len(v))
    cdef sage_Vector_rational_dense ans = V.zero().__copy__()
    cdef int i
    for i in range(len(v)):
        mpq_set(ans._entries[i], v.pm_obj[i].get_rep())
    return ans

def VectorRational_from_sage(sage_Vector_rational_dense v):
    cdef vector[pm_Rational] data
    cdef int i
    cdef pm_Rational q
    for i in range(v._degree):
        q.set_mpq_srcptr(v._entries[i])
        data.push_back(q)

    cdef VectorRational ans = VectorRational.__new__(VectorRational)
    ans.pm_obj = data
    return ans

def VectorQuadraticExtension_to_sage(v):
    raise NotImplementedError

def VectorQuadraticExtension_from_sage(v):
    raise NotImplementedError

def MatrixInt_to_sage(MatrixInt m):
    cdef Py_ssize_t i, j
    cdef Py_ssize_t nrows = m.pm_obj.rows()
    cdef Py_ssize_t ncols = m.pm_obj.cols()
    M = MatrixSpace(ZZ, nrows, ncols)
    cdef sage_Matrix_integer_dense ans = M.zero().__copy__()
    for i in range(nrows):
        for j in range(ncols):
            ans.set_unsafe_si(i, j, pm_Matrix_get(m.pm_obj, i, j))
    return ans

def MatrixInt_from_sage(sage_Matrix_integer_dense m):
    raise NotImplementedError

def MatrixFloat_to_sage(MatrixFloat m):
    cdef Py_ssize_t i, j
    cdef Py_ssize_t nrows = m.pm_obj.rows()
    cdef Py_ssize_t ncols = m.pm_obj.cols()
    M = MatrixSpace(RDF, nrows, ncols)
    ans = M()
    for i in range(nrows):
        for j in range(ncols):
            ans[i,j] = pm_Matrix_get(m.pm_obj, i, j)
    return ans

def MatrixFloat_from_sage(m):
    raise NotImplementedError

def MatrixInteger_to_sage(MatrixInteger m):
    cdef Py_ssize_t i, j
    cdef Py_ssize_t nrows = m.pm_obj.rows()
    cdef Py_ssize_t ncols = m.pm_obj.cols()
    M = MatrixSpace(ZZ, nrows, ncols)
    cdef sage_Matrix_integer_dense ans = M.zero().__copy__()
    for i in range(nrows):
        for j in range(ncols):
            ans.set_unsafe_mpz(i, j, <mpz_t> pm_Matrix_get(m.pm_obj, i, j).get_rep())
    return ans

def MatrixInteger_from_sage(sage_Matrix_integer_dense m):
    raise NotImplementedError

def MatrixRational_to_sage(MatrixRational m):
    cdef Py_ssize_t i, j
    cdef Py_ssize_t nrows = m.pm_obj.rows()
    cdef Py_ssize_t ncols = m.pm_obj.cols()
    M = MatrixSpace(QQ, nrows, ncols)
    cdef sage_Matrix_rational_dense ans = M.zero().__copy__()
    for i in range(nrows):
        for j in range(ncols):
            fmpq_set_mpq(fmpq_mat_entry(ans._matrix, i, j), <mpq_t> pm_Matrix_get(m.pm_obj, i, j).get_rep())
    return ans

def MatrixRational_from_sage(sage_Matrix_rational_dense m):
    raise NotImplementedError

def MatrixQuadraticExtension_to_sage(m, field=None):
    entries = [m[i,j] for i in range(m.rows()) for j in range(m.cols())]

    if field is None:
        if not entries:
            field = QQ
        else:
            D = set((x.r().numerator() * x.r().denominator()).sage().squarefree_part() for x in entries)
            D.discard(0)
            D.discard(1)
            if len(D) > 1:
                raise ValueError("D = {} consists of more than one root".format(D))
            if len(D) == 0:
                field = QQ
            else:
                D = D.pop()
                field = QuadraticField(D, 'sqrt{}'.format(D), embedding=AA(D).sqrt())

    entries = [x.sage(field) for x in entries]
    return matrix(field, m.rows(), m.cols(), entries)

def MatrixQuadraticExtension_from_sage(m):
    raise NotImplementedError

def PolytopeRational_to_sage(PerlObject pm, **opts):
    from sage.geometry.polyhedron.constructor import Polyhedron
    return Polyhedron(ieqs=pm.FACETS.sage(), eqns=pm.AFFINE_HULL.sage(), **opts)

def PolytopeQuadraticExtension_to_sage(PerlObject pm, base_ring=None, **opts):
    from sage.geometry.polyhedron.constructor import Polyhedron
    return Polyhedron(ieqs=pm.FACETS.sage(), eqns=pm.AFFINE_HULL.sage(), **opts)

def Polytope_from_sage(p):
    if p.base_ring() is ZZ or p.base_ring() is QQ:
        return PolytopeRational(
                  CONE_AMBIENT_DIM = 1 + p.parent().ambient_dim(),
                  POINTS = [[1] + v for v in p.vertices_list()] + \
                          [[0] + r for r in p.rays_list()],
                  INPUT_LINEALITY = [[0] + l for l in p.lines_list()])
    elif isinstance(p.base_ring(), NumberField_quadratic):
        f = SageQuadraticFieldToPolymake(p.base_ring())
        return PolytopeQuadraticExtension(
                CONE_AMBIENT_DIM = 1 + p.parent().ambient_dim(),
                POINTS = [[1] + list(map(f, v)) for v in p.vertices_list()] + \
                         [[0] + list(map(f, r)) for r in p.rays_list()],
                INPUT_LINEALITY = [[0] + list(map(f, l)) for l in p.lines_list()])
    else:
        raise NotImplementedError
