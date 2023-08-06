"""
Various functions to deal with conversion mpz <-> Python int/long
"""
from .types cimport *

cdef bytes mpz_get_bytes(mpz_srcptr)
cdef bytes mpq_get_bytes(mpq_srcptr)
cdef mpz_get_pylong(mpz_srcptr z)
cdef mpz_get_pyintlong(mpz_srcptr z)
cdef int mpz_set_pylong(mpz_ptr z, L) except -1
cdef Py_hash_t mpz_pythonhash(mpz_srcptr z)
cdef double mpz_get_d_nearest(mpz_srcptr x) except? -648555075988944.5
