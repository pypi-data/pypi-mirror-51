###############################################################################
#       Copyright (C) 2011-2012 Burcin Erocal <burcin@erocal.org>
#                     2016-2019 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

from libcpp.string cimport string

from .cygmp.mpz cimport *
from .cygmp.mpz cimport *
from .defs cimport *
from .perl_object cimport wrap_perl_object, get_properties
from .integer cimport Integer
from .rational cimport Rational
from .quadratic_extension cimport QuadraticExtension
from .matrix cimport MatrixRational, MatrixQuadraticExtension

def Polytope(typ='Rational', **args):
    r"""
    Construct a polytope

    INPUT:

    - ``VERTICES`` -- a matrix of vertices

    - ``POINTS`` -- a matrix of points

    - ``FACETS`` -- a matrix of facets

    Examples:

    >>> import polymake
    >>> polymake.Polytope(POINTS=[[1,0,0],[0,1,0],[0,0,1]])
    Polytope<Rational>
    >>> polymake.Polytope(VERTICES=[[1,-1,-1],[1,1,-1],[1,-1,1],[1,1,1]], LINEALITY_SPACE=[])
    Polytope<Rational>
    >>> polymake.Polytope(INEQUALITIES=[[5,-4,0,1],[-3,0,-4,1],[-2,1,0,0],[-4,4,4,-1],[0,0,1,0],[8,0,0,-1],[1,0,-1,0],[3,-1,0,0]])
    Polytope<Rational>
    >>> polymake.Polytope(INEQUALITIES=[[1,1,0,0],[1,0,1,0],[1,-1,0,0],[1,0,-1,0]], EQUATIONS=[[0,0,0,1],[0,0,0,2]])
    Polytope<Rational>
    """
    cdef string cprop

    cdef string ctyp = <string> (b"polytope::Polytope<" + typ.encode('ascii') + b">")
    cdef pm_PerlObject * pm_obj = new pm_PerlObject(ctyp)

    for prop, value in args.items():
        cprop = prop.encode('ascii')

        if cprop == b"CONE_AMBIENT_DIM":
            pm_assign_Int(pm_obj.take(cprop), value)

        elif cprop in [b"VERTICES", b"POINTS", b"FACETS", b"INEQUALITIES", b"INPUT_LINEALITY",
                b"LINEALITY_SPACE", b"INEQUALITIES", b"EQUATIONS"]:

            if typ == "Rational":
                pm_assign_Matrix(pm_obj.take(cprop),
                                 (<MatrixRational> MatrixRational(value)).pm_obj)
            elif typ == "QuadraticExtension":
                pm_assign_Matrix(pm_obj.take(cprop),
                                 (<MatrixQuadraticExtension> MatrixQuadraticExtension(value)).pm_obj)
            else:
                raise ValueError
        else:
            raise ValueError("{} is not a valid property of polytope::Polytope<Rational>".format(cprop))

    return wrap_perl_object(pm_obj[0])

def PolytopeRational(**opts):
    return Polytope(b"Rational", **opts)

def PolytopeQuadraticExtension(**opts):
    return Polytope(b"QuadraticExtension", **opts)

def PointConfiguration(**args):
    cdef pm_Matrix[pm_Rational] * pm_mat
    cdef pm_PerlObject * pm_obj = new pm_PerlObject(b"PointConfiguration<Rational>")
