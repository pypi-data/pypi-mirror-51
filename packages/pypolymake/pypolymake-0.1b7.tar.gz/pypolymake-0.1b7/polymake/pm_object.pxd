cdef class PmObject(object):
    cpdef _add_(self, other)
    cpdef _sub_(self, other)
    cpdef _mul_(self, other)
    cpdef _div_(self, other)
    cpdef _floordiv_(self, other)
    cpdef _richcmp_(self, other, int op)

