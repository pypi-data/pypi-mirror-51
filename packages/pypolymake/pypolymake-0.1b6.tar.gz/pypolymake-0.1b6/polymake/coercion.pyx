from cpython.object cimport PyObject, PyTypeObject
from libc.string cimport strncmp

import numbers

from .pm_object cimport PmObject

# TODO: we should try to not import inside!

cpdef as_pm_object(x):
    # fast type checking
    if isinstance(x, (int, long)):
        from .integer import Integer
        return Integer(x)

    # slower type checking
    if isinstance(x, numbers.Integral):
        from .integer import Integer
        return Integer(x)

    if isinstance(x, numbers.Rational):
        from .rational import Rational
        return Rational(x)

    if is_sage_type(type(x)):
        from .sage_conversion import (QuadraticExtension_from_sage,
                Polytope_from_sage,
                VectorInteger_from_sage, MatrixInteger_from_sage,
                VectorRational_from_sage, MatrixRational_from_sage,
                VectorQuadraticExtension_from_sage, MatrixQuadraticExtension_from_sage)
        from sage.all import ZZ, QQ
        from sage.structure.element import Matrix
        from sage.geometry.polyhedron.base import Polyhedron_base
        from sage.modules.free_module_element import FreeModuleElement
        from sage.rings.number_field.number_field import NumberField_quadratic
        from sage.rings.number_field.number_field_element_quadratic import NumberFieldElement_quadratic

        if isinstance(x, NumberFieldElement_quadratic):
            return QuadraticExtension_from_sage(x)
        elif isinstance(x, FreeModuleElement):
            if x.base_ring() is ZZ:
                if x.is_dense():
                    return VectorInteger_from_sage(x)
                else:
                    from .vector import VectorInteger
                    return VectorInteger(x)
            elif x.base_ring() is QQ:
                if x.is_dense():
                    return VectorRational_from_sage(x)
                else:
                    from .rational import VectorRational
                    return VectorRational(x)
            elif isinstance(x.base_ring(), NumberField_quadratic):
                return VectorQuadraticExtension_from_sage(x)
            else:
                raise NotImplementedError("no equivalent polymake vector")
        elif isinstance(x, Matrix):
            if x.base_ring() is ZZ:
                return MatrixInteger_from_sage(x)
            elif x.base_ring() is QQ:
                return MatrixRational_from_sage(x)
            elif isinstance(x.base_ring(), NumberField_quadratic):
                return MatrixQuadraticExtension_from_sage(x)
            else:
                raise NotImplementedError("no equivalent polymake matrix")
        elif isinstance(x, Polyhedron_base):
            return Polytope_from_sage(x)
        else:
            raise NotImplementedError("no equivalent polymake object")

    raise NotImplementedError("no equivalent polymake object")

# TODO: this is very slow!
cpdef bint is_sage_type(t):
    return isinstance(t, type) and t.__module__.startswith('sage.')

cpdef canonical_coercion(x, y):
    if type(x) is type(y):
        return (x,y)

    if not isinstance(x, PmObject):
        x = as_pm_object(x)
    if not isinstance(y, PmObject):
        y = as_pm_object(y)

    if type(x) is type(y):
        return (x, y)

    from .integer import Integer
    from .rational import Rational
    from .quadratic_extension import QuadraticExtension
    from .vector import VectorInteger, VectorRational

    if type(x) is Integer and type(y) is Rational:
        return (Rational(x), y)
    if type(x) is Rational and type(y) is Integer:
        return (x, Rational(y))
    if type(x) in [Integer, Rational] and type(y) is QuadraticExtension:
        return (QuadraticExtension(x), y)
    if type(x) is QuadraticExtension and type(y) in [Integer, Rational]:
        return (x, QuadraticExtension(y))
    if type(x) is VectorInteger and type(y) is VectorRational:
        return (VectorRational(x), y)
    if type(x) is VectorRational and type(y) is VectorInteger:
        return (x, VectorRational(y))

    raise ValueError("no coercion found for x={} (of type {}) and y={} (of type {})".format(x, type(x), y, type(y)))
