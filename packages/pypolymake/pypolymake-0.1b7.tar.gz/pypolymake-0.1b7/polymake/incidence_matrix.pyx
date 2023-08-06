###############################################################################
#       Copyright (C) 2011-2012 Burcin Erocal <burcin@erocal.org>
#                     2016-2019 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

from libcpp.string cimport string

from .defs cimport ostringstream, pm_repr_wrap

cdef extern from "polymake/IncidenceMatrix.h" namespace "polymake":
    bint pm_IncidenceMatrixNonSymmetric_get "WRAP_CALL" (pm_IncidenceMatrixNonSymmetric, int i, int j)

cdef class IncidenceMatrixNonSymmetric(PmObject):
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

        return pm_IncidenceMatrixNonSymmetric_get(self.pm_obj, i, j)

    def rows(self):
        return self.pm_obj.rows()

    def cols(self):
        return self.pm_obj.cols()
