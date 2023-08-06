"""
Various functions to deal with conversion mpz <-> Python int/long

AUTHORS:

- Gonzalo Tornaria (2006): initial version

- David Harvey (2007-08-18): added ``mpz_get_pyintlong`` function
  (:trac:`440`)

- Jeroen Demeyer (2015-02-24): moved from c_lib, rewritten using
  ``mpz_export`` and ``mpz_import`` (:trac:`17853`)

- Vincent Delecroix (2016)
"""

#*****************************************************************************
#       Copyright (C) 2015 Jeroen Demeyer <jdemeyer@cage.ugent.be>
#                     2016 Vincent Delecroix <vincent.delecroix@labri.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from __future__ import absolute_import, print_function

from cysignals.signals cimport sig_on, sig_off

from libc.stdlib cimport malloc, free
from libc.math cimport ldexp
from libc.stdint cimport uint64_t

from cpython.object cimport Py_SIZE
from cpython.int cimport PyInt_FromLong
from cpython.long cimport PyLong_FromLong

# NOTE: needs recent enough Cython
from cpython.longintrepr cimport _PyLong_New, py_long, digit, PyLong_SHIFT

from .mpz cimport *
from .mpq cimport *

cdef extern from *:
    Py_ssize_t* Py_SIZE_PTR "&Py_SIZE"(object)
    int hash_bits """
        #ifdef _PyHASH_BITS
        _PyHASH_BITS         /* Python 3 */
        #else
        (8 * sizeof(void*))  /* Python 2 */
        #endif
        """
    int limb_bits "(8 * sizeof(mp_limb_t))"

# Unused bits in every PyLong digit
cdef size_t PyLong_nails = 8*sizeof(digit) - PyLong_SHIFT

cdef mpz_get_pylong_large(mpz_srcptr z):
    """
    Convert a non-zero ``mpz`` to a Python ``long``.
    """
    cdef size_t nbits = mpz_sizeinbase(z, 2)
    cdef size_t pylong_size = (nbits + PyLong_SHIFT - 1) // PyLong_SHIFT
    L = _PyLong_New(pylong_size)
    mpz_export(L.ob_digit, NULL,
            -1, sizeof(digit), 0, PyLong_nails, z)
    if mpz_sgn(z) < 0:
        # Set correct size (use a pointer to hack around Cython's
        # non-support for lvalues).
        sizeptr = Py_SIZE_PTR(L)
        sizeptr[0] = -pylong_size
    return L


cdef mpz_get_pylong(mpz_srcptr z):
    """
    Convert an ``mpz`` to a Python ``long``.
    """
    if mpz_fits_slong_p(z):
        return PyLong_FromLong(mpz_get_si(z))
    return mpz_get_pylong_large(z)


cdef mpz_get_pyintlong(mpz_srcptr z):
    """
    Convert an ``mpz`` to a Python ``int`` if possible, or a ``long``
    if the value is too large.
    """
    if mpz_fits_slong_p(z):
        return PyInt_FromLong(mpz_get_si(z))
    return mpz_get_pylong_large(z)


cdef int mpz_set_pylong(mpz_ptr z, L) except -1:
    """
    Convert a Python ``long`` `L` to an ``mpz``.
    """
    cdef Py_ssize_t pylong_size = Py_SIZE(L)
    if pylong_size < 0:
        pylong_size = -pylong_size
    mpz_import(z, pylong_size, -1, sizeof(digit), 0, PyLong_nails,
            (<py_long>L).ob_digit)
    if Py_SIZE(L) < 0:
        mpz_neg(z, z)


cdef Py_hash_t mpz_pythonhash(mpz_srcptr z):
    """
    Hash an ``mpz``, where the hash value is the same as the hash value
    of the corresponding Python ``int`` or ``long``, except that we do
    not replace -1 by -2 (the Cython wrapper for ``__hash__`` does that).
    """
    if mpz_sgn(z) == 0:
        return 0

    # The hash value equals z % m where m = 2 ^ hash_bits - 1.
    #
    # Safely compute 2 ^ hash_bits - 1 without overflow
    cdef mp_limb_t modulus = (((<mp_limb_t>(1) << (hash_bits - 1)) - 1) * 2) + 1

    cdef mp_limb_t h = 0
    cdef mp_limb_t x, y
    cdef size_t i, n
    cdef unsigned int r
    n = mpz_size(z)
    for i in range(n):
        x = mpz_getlimbn(z, i)

        # Computing modulo 2 ^ hash_bits - 1 means that the bit at
        # position j is really moved to position (j % hash_bits).
        # We need to shift every bit of x left by (limb_bits * i)
        # and then put it in the right position to account for
        # the modulo operation. Store the result in y.
        if limb_bits == hash_bits:
            y = x
        else:
            r = (limb_bits * i) % hash_bits
            y = (x << r) & modulus
            y += (x >> (hash_bits - r)) & modulus
            # Only do this shift if we don't shift more than the size of the
            # type
            if r > 2 * hash_bits - limb_bits:
                y += (x >> (2 * hash_bits - r))
            # At this point, y <= 2 * modulus, so y did not overflow, but we
            # need y <= modulus. We use > instead of >= on the line below
            # because it generates more efficient code.
            if y > modulus:
                y -= modulus

        # Safely compute h = (h + y) % modulus knowing that h < modulus
        # and y <= modulus
        if h < modulus - y:
            h = h + y
        else:
            h = h - (modulus - y)

    # Special case for Python 2
    if limb_bits == hash_bits and h == 0:
        h = -1

    if mpz_sgn(z) < 0:
        return -h
    return h


assert hash_bits <= limb_bits <= 2 * hash_bits

cdef bytes mpz_get_bytes(mpz_srcptr z):
    # NOTE: copied from sage.rings.integer.Integer.str
    cdef char *s
    cdef size_t n
    n = mpz_sizeinbase(z, 10) + 2
    s = <char*>malloc(n)
    mpz_get_str(s, 10, z)
    k = <bytes>s
    free(s)
    return k

cdef bytes mpq_get_bytes(mpq_srcptr z):
    # NOTE: copied from sage.rings.rational.Rational.str
    cdef size_t n
    cdef char*s
    n = mpz_sizeinbase(mpq_numref(z), 10) + \
        mpz_sizeinbase(mpq_denref(z), 10) + 3    
    s = <char *> malloc(n * sizeof(char))
    mpq_get_str(s, 10, z)
    k = <bytes>s
    free(s)
    return k

# The except value is just some random double, it doesn't matter what it is.
cdef double mpz_get_d_nearest(mpz_srcptr x) except? -648555075988944.5:
    cdef mp_bitcnt_t sx = mpz_sizeinbase(x, 2)

    # Easy case: x is exactly representable as double.
    if sx <= 53:
        return mpz_get_d(x)

    cdef int resultsign = mpz_sgn(x)

    # Check for overflow
    if sx > 1024:
        if resultsign < 0:
            return -1.0/0.0
        else:
            return 1.0/0.0

    # General case

    # We should shift x right by this amount in order
    # to have 54 bits remaining.
    cdef mp_bitcnt_t shift = sx - 54

    # Compute q = trunc(x / 2^shift) and let remainder_is_zero be True
    # if and only if no truncation occurred.
    cdef int remainder_is_zero
    remainder_is_zero = mpz_divisible_2exp_p(x, shift)

    sig_on()

    cdef mpz_t q
    mpz_init(q)
    mpz_tdiv_q_2exp(q, x, shift)

    # Convert abs(q) to a 64-bit integer.
    cdef mp_limb_t* q_limbs = (<mpz_ptr>q)._mp_d
    cdef uint64_t q64
    if sizeof(mp_limb_t) >= 8:
        q64 = q_limbs[0]
    else:
        assert sizeof(mp_limb_t) == 4
        q64 = q_limbs[1]
        q64 = (q64 << 32) + q_limbs[0]

    mpz_clear(q)
    sig_off()

    # Round q from 54 to 53 bits of precision.
    if ((q64 & 1) == 0):
        # Round towards zero
        pass
    else:
        if not remainder_is_zero:
            # Remainder is non-zero: round away from zero
            q64 += 1
        else:
            # Halfway case: round to even
            q64 += (q64 & 2) - 1

    # The conversion of q64 to double is *exact*.
    # This is because q64 is even and satisfies 2^53 <= q64 <= 2^54.
    cdef double d = <double>q64
    if resultsign < 0:
        d = -d
    return ldexp(d, shift)
