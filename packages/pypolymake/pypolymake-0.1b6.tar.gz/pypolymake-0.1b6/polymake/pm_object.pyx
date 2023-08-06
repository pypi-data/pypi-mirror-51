from .coercion cimport canonical_coercion

cdef inline int classify_element(left, right):
    if type(left) is type(right):
        return 0o37
    if not isinstance(right, PmObject):
        return 0o01
    if not isinstance(left, PmObject):
        return 0o02
    return 0o07

cdef inline bint ARE_SAME_PMOBJECTS(int cl):
    return cl & 0o20
cdef inline bint BOTH_ARE_PMOBJECTS(int cl):
    return cl & 0o04

cdef class PmObject(object):
    cpdef _add_(self, other): raise NotImplementedError
    cpdef _sub_(self, other): raise NotImplementedError
    cpdef _mul_(self, other): raise NotImplementedError
    cpdef _div_(self, other): raise NotImplementedError
    cpdef _floordiv_(self, other): raise NotImplementedError
    cpdef _richcmp_(self, other, int op): raise NotImplementedError

    def __add__(self, other):
        cdef int cl = classify_element(self, other)
        if not ARE_SAME_PMOBJECTS(cl):
            self, other = canonical_coercion(self, other)
        return (<PmObject> self)._add_(other)

    def __sub__(self, other):
        cdef int cl = classify_element(self, other)
        if not ARE_SAME_PMOBJECTS(cl):
            self, other = canonical_coercion(self, other)
        return (<PmObject> self)._sub_(other)

    def __mul__(self, other):
        cdef int cl = classify_element(self, other)
        if not ARE_SAME_PMOBJECTS(cl):
            self, other = canonical_coercion(self, other)
        return (<PmObject> self)._mul_(other)

    def __truediv__(self, other):
        cdef int cl = classify_element(self, other)
        if not ARE_SAME_PMOBJECTS(cl):
            self, other = canonical_coercion(self, other)
        if not other:
            raise ZeroDivisionError
        return (<PmObject> self)._div_(other)

    def __div__(self, other):
        cdef int cl = classify_element(self, other)
        if not ARE_SAME_PMOBJECTS(cl):
            self, other = canonical_coercion(self, other)
        if not other:
            raise ZeroDivisionError
        return (<PmObject> self)._div_(other)

    def __floordiv__(self, other):
        cdef int cl = classify_element(self, other)
        if not ARE_SAME_PMOBJECTS(cl):
            self, other = canonical_coercion(self, other)
        if not other:
            raise ZeroDivisionError
        return (<PmObject> self)._floordiv_(other)

    def __richcmp__(self, other, op):
        cdef int cl = classify_element(self, other)
        if not ARE_SAME_PMOBJECTS(cl):
            self, other = canonical_coercion(self, other)
        return (<PmObject> self)._richcmp_(other, op)
