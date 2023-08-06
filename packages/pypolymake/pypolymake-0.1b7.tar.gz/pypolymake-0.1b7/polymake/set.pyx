###############################################################################
#       Copyright (C) 2016-2019 Vincent Delecroix <vincent.delecroix@labri.fr> 
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

from .defs cimport ostringstream, pm_repr_wrap

from libcpp cimport bool
from libcpp.string cimport string

cdef class SetSetInt(PmObject):
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap(out, self.pm_obj)
        #pm_repr_wrap[pm_Set[pm_Set[int]]](out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

cdef class SetMatrixRational(PmObject):
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap[pm_Set[pm_Matrix[pm_Rational]]](out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

cdef class SetArrayInt(PmObject):
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap[pm_Set[pm_Array[int]]](out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')

cdef class SetInt(PmObject):
    def __len__(self):
        return self.pm_obj.size()
    def __repr__(self):
        cdef ostringstream out
        pm_repr_wrap[pm_Set[int]](out, self.pm_obj)
        return (<bytes>out.str()).decode('ascii')
    def __iter__(self):
        # TODO: Entire
        raise NotImplementedError
        #cdef pm_SetInt_iterator it = entire_SetInt(self.pm_obj)
        #while not it.at_end():
        #    yield it.get()
        #    it.next()

