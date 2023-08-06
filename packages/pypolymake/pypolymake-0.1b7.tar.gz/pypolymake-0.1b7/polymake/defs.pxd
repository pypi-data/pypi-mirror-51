# distutils: language = c++
# distutils: libraries = polymake
###############################################################################
#       Copyright (C) 2011-2012 Burcin Erocal <burcin@erocal.org>
#                     2016-2019 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 3 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

# This file contain header declarations from polymake (in include/core/polymake).
# The explicit list of supported "small objects" from polymake is declared
# in this file
#
#     AccurateFloat.h
#     AnyString.h
#     Array.h
#     Bitset.h
#     CascadedContainer.h
#     ContainerChain.h
#     ContainerUnion.h
#     EmbeddedList.h
#     EquivalenceRelation.h
#     FaceMap.h
#     FacetList.h
#     Fibonacci.h
#     GenericGraph.h
#     GenericIncidenceMatrix.h
#     GenericIO.h
#     GenericMatrix.h
#     GenericSet.h
#     GenericStruct.h
#     GenericVector.h
#     Graph.h
#     Heap.h
#     IncidenceMatrix.h
#     IndexedSubgraph.h
#     IndexedSubset.h
#     Integer.h
#     ListMatrix.h
#     Map.h
#     Matrix.h
#     MultiDimCounter.h
#     Plucker.h
#     Polynomial.h
#     PowerSet.h
#     PuiseuxFraction.h
#     QuadraticExtension.h
#     RandomGenerators.h
#     RandomSpherePoints.h
#     RandomSubset.h
#     RationalFunction.h
#     Rational.h
#     Ring.h
#     SelectedSubset.h
#     Series.h
#     Set.h
#     Smith_normal_form.h
#     SparseMatrix.h
#     SparseVector.h
#     TransformedContainer.h
#     TropicalNumber.h
#     Vector.h
#
#     client.h
#     color.h
#     integer_linalg.h
#     linalg.h
#     meta_function.h
#     meta_list.h
#     node_edge_incidences.h
#     numerical_functions.h
#     pair.h
#     permutations.h
#     socketstream.h
#     totally_unimodular.h
#     type_utils.h
#
# lib/callable/include/Main.h

from libcpp cimport bool
from libcpp.string cimport string
from libcpp.pair cimport pair
from libcpp.vector cimport vector

from .cygmp.types cimport mpz_t, mpq_t, mpz_srcptr, mpq_srcptr

cdef extern from "<sstream>" namespace "std":
    cdef cppclass ostringstream:
        string str()

cdef extern from "wrap.h":
    void pm_repr [T] (ostringstream, T)
    void pm_repr_wrap [T] (ostringstream, T)

###############################################################################
# Polymake mathematical types                                                 #
###############################################################################

cdef extern from "polymake/Integer.h" namespace "polymake":
    ctypedef pm_const_Integer "const Integer"
    cdef cppclass pm_Integer "Integer":
        mpz_srcptr get_rep() const
        Py_ssize_t strsize(int)
        int compare(int)

# in beta, explicit casts defined
#       long to_long()   # FIXME: this is const
#       double to_double()

# in beta, set gets renamed into copy_from
        pm_Integer set_mpz_t "copy_from" (mpz_t)
        pm_Integer& set_mpz_srcptr "copy_from" (mpz_srcptr)

# in beta, non_zero replaced by is_zero
#        bool non_zero()
        bool is_zero()

        bool operator== (pm_Integer)
        bool operator== (long)
        bool operator> (pm_Integer)
        bool operator> (long)
        bool operator< (pm_Integer)
        bool operator< (long)

        int compare(pm_Integer)
        int compare(long)

        pm_Integer operator+ (pm_Integer) except +
        pm_Integer operator+ (long) except +
        pm_Integer operator- () except +
        pm_Integer operator- (pm_Integer) except +
        pm_Integer operator- (long) except +
        pm_Integer operator* (pm_Integer) except +
        pm_Integer operator* (long) except +
        pm_Integer operator/ (pm_Integer) except +
        pm_Integer operator/ (long) except +
        pm_Integer operator% (pm_Integer) except +
        pm_Integer operator% (long) except +
        pm_Integer negate()

    bool pm_is_zero "is_zero" (const pm_Integer&)
    bool pm_is_one "is_one" (const pm_Integer&)
    pm_Integer pm_pow "pow" (const pm_Integer&, long) except +
    pm_Integer pm_pow "pow" (long a, long) except +
    pm_Integer pm_abs "abs" (const pm_Integer&) except +
    pm_Integer pm_gcd "gcd" (const pm_Integer&, const pm_Integer&) except +
    pm_Integer pm_gcd "gcd" (const pm_Integer&, long) except +
    pm_Integer pm_gcd "gcd" (long, const pm_Integer&) except +
    pm_Integer pm_lcm "lcm" (const pm_Integer&, const pm_Integer&) except +
    pm_Integer pm_lcm "lcm" (const pm_Integer&, long) except +
    pm_Integer pm_lcm "lcm" (long, const pm_Integer&) except +

    # cast
    long operator()(pm_Integer) except +

cdef extern from "polymake/Rational.h" namespace 'polymake':
    ctypedef pm_const_Rational "const Rational"
    cdef cppclass pm_Rational "Rational":
        pm_Rational()

        mpq_srcptr get_rep()
# in beta, set replaced by copy_from
        pm_Rational set_mpq_t "copy_from" (mpq_t)
        pm_Rational& set_mpq_srcptr "copy_from" (mpq_srcptr)
        pm_Rational& set_long "set" (long, long)

        pm_Rational abs()

# in beta, non_zero replaced by is_zero
#        bool non_zero()
        bool is_zero()

        bool operator== (pm_Rational)
        bool operator== (pm_Integer)
        bool operator== (long)
        bool operator< (pm_Rational)
        bool operator< (pm_Integer)
        bool operator< (long)
        bool operator> (pm_Rational)
        bool operator> (pm_Integer)
        bool operator> (long)

        int compare(pm_Rational)
        int compare(pm_Integer)
        int compare(long)

        pm_Rational operator+ (pm_Rational) except +
        pm_Rational operator+ (pm_Integer) except +
        pm_Rational operator+ (long) except +
        pm_Rational operator- () except +
        pm_Rational operator- (pm_Rational) except +
        pm_Rational operator- (pm_Integer) except +
        pm_Rational operator- (long) except +
        pm_Rational operator* (pm_Rational) except +
        pm_Rational operator* (pm_Integer) except +
        pm_Rational operator* (long) except +
        pm_Rational operator/ (pm_Rational) except +
        pm_Rational operator/ (pm_Integer) except +
        pm_Rational operator/ (long) except +

    bool pm_is_zero "is_zero" (const pm_Rational&)
    bool pm_is_one "is_one" (const pm_Rational&)
    pm_Rational pm_abs "abs" (const pm_Rational&) except +
    pm_Rational pm_pow "pow" (const pm_Rational&, long) except +
    pm_Rational pm_pow "pow" (long, long) except +

cdef extern from "polymake/Vector.h" namespace 'polymake':
    cdef cppclass pm_Vector "Vector" [E]:
        pm_Vector()
        pm_Vector(int)
        pm_Vector(int, const E&)
        pm_Vector(pm_Vector[E]&)
        pm_Vector(vector[E]&)

        bool operator==(pm_Vector[E]&)
        bool operator!=(pm_Vector[E]&)

        pm_Vector[E]& operator=(pm_Vector[E]&)
        pm_Vector[E]& operator=(vector[E]&)

        void swap(pm_Vector[E]&)

        E operator[](int)
        int size()
        void clear()
        void resize(int)

        pm_Vector[E]& operator+(const pm_Vector[E]&)
        pm_Vector[E]& operator-(const pm_Vector[E]&)
        pm_Vector[E]& negate()


cdef extern from "polymake/Array.h" namespace "polymake":
    cdef cppclass pm_Array "Array" [E]:
        # NOTE: for iterators in Cython code, you need to use the following from cython.operator
        #   dereference(foo) for *foo
        #   preincrement(foo) for ++foo
        #   postincrement(foo) for foo++
        cppclass iterator:
            E operator*()
            iterator operator++()
            bint operator==(iterator&)
            bint operator!=(iterator&)

        cppclass const_iterator:
            E operator*()
            iterator operator++()
            bint operator==(const_iterator&)
            bint operator!=(const_iterator&)

        int size()
        void clear()
        void resize(int)
        void assign(int, const E&)
        bool empty()
        E operator[] (int)
        bool operator== (const pm_Array[E]&)
        bool operator!= (const pm_Array[E]&)
        const_iterator begin()
        const_iterator end()


cdef extern from "polymake/Set.h" namespace "polymake":
    cdef cppclass pm_Set "Set" [E]:
        cppclass iterator:
            E operator*()
            iterator operator++()
            bint operator==(iterator&)
            bint operator!=(iterator&)
        void clear()
        void resize(int)
        int size()
        bool empty()
        iterator begin() const
        iterator end() const


cdef extern from "polymake/Map.h" namespace "polymake":
    cdef cppclass pm_Map "Map" [T0, T1]:
        cppclass iterator:
            pair[T0,T1] operator*()
            iterator operator++()
            bint operator==(iterator&)
            bint operator!=(iterator&)
            bool at_end()

        iterator begin()

        T1 operator[] (T0)
        int size()
        bool exists(T0&)


cdef extern from "polymake/IncidenceMatrix.h" namespace "polymake":
    cdef cppclass pm_IncidenceMatrixNonSymmetric "IncidenceMatrix<NonSymmetric>":
        pm_IncidenceMatrixNonSymmetric()
        pm_IncidenceMatrixNonSymmetric(int nr, int nc)
        int rows()
        int cols()


cdef extern from "polymake/SparseMatrix.h" namespace "polymake":
    cdef cppclass pm_SparseMatrix "SparseMatrix" [T]:
        pm_SparseMatrixInt ()
        pm_SparseMatrixInt (int nr, int nc)
        int assign (int r, int c, T val)
        int rows()
        int cols()

    # WRAP_CALL(t,i,j) -> t(i,j)
    int pm_SparseMatrix_get "WRAP_CALL" (pm_SparseMatrix[int], int, int)
    pm_Rational pm_SparseMatrix_get "WRAP_CALL" (pm_SparseMatrix[pm_Rational], int, int)


cdef extern from "polymake/Matrix.h" namespace "polymake":
    cdef cppclass pm_Matrix "Matrix" [T]:
        pm_Matrix()
        pm_Matrix(int nr, int nc)
        pm_Matrix(pm_Matrix[T]&)
        pm_Matrix(vector[T]&)

        void resize(int r, int c) except+
        int assign(int r, int c, T val)
        int rows()
        int cols()

        pm_Matrix[T]& operator= (const pm_Matrix[T]&)

        bool operator==(pm_Matrix[T]&)
        bool operator!=(pm_Matrix[T]&)

        pm_Matrix[T]& operator+ (const pm_Matrix[T]&) except+
        pm_Matrix[T]& operator- (const pm_Matrix[T]&) except+


cdef extern from "polymake/Polynomial.h" namespace "polymake":
    # TODO: use Cython support for C++ templates
    cdef cppclass UniPolynomial[Coeff, Pow]:
        int n_vars()
        int n_terms()
        bool trivial()
        bool unit()
        int deg()
        int lower_deg()

        # makes compiler crash...
        # Vector[Coeff] coefficients_as_vector()

        bool operator== (const UniPolynomial[Coeff,Pow]&)
        bool operator!= (const UniPolynomial[Coeff,Pow]&)

    cdef cppclass pm_UniPolynomialRationalInt "UniPolynomial<Rational, int>":
        int n_vars()
        int n_terms()
        bool trivial()
        bool unit()
        int deg()
        int lower_deg()

        pm_Vector[pm_Rational] coefficients_as_vector()
#        bool operator== (const UniPolynomial& other)
#        bool operator!= (const UniPolynomial& other)


cdef extern from "polymake/QuadraticExtension.h" namespace "polymake":
    cdef cppclass pm_QuadraticExtension "QuadraticExtension<Rational>":
        pm_QuadraticExtension()
        pm_QuadraticExtension(pm_Rational&) except+
        pm_QuadraticExtension(pm_Rational&, pm_Rational&, pm_Rational&) except+
        pm_QuadraticExtension(pm_QuadraticExtension&) except+
        pm_QuadraticExtension& operator+(const pm_QuadraticExtension&) except+
        pm_QuadraticExtension& operator-(const pm_QuadraticExtension&) except+
        pm_QuadraticExtension& operator*(const pm_QuadraticExtension&) except+
        pm_QuadraticExtension& operator/(const pm_QuadraticExtension&) except+
        pm_QuadraticExtension& operator-() except+
        bool operator==(const pm_QuadraticExtension&)
        bool operator<(const pm_QuadraticExtension&)
        bool operator<=(const pm_QuadraticExtension&)
        bool operator>=(const pm_QuadraticExtension&)
        bool operator>(const pm_QuadraticExtension&)

        pm_QuadraticExtension& operator= (const pm_QuadraticExtension&) except+

        pm_Rational& a()
        pm_Rational& b()
        pm_Rational& r()

    bool pm_is_zero "is_zero" (pm_QuadraticExtension&)
    bool pm_is_one "is_zero" (pm_QuadraticExtension&)


cdef extern from "polymake/RationalFunction.h" namespace "polymake":
    cdef cppclass pm_RationalFunctionRationalInt "RationalFunction<Rational, int>":
        pm_UniPolynomialRationalInt numerator()
        pm_UniPolynomialRationalInt denominator()


cdef extern from "polymake/Set.h" namespace "polymake":
    cdef cppclass pm_SetInt "Set<Int>":
        pass


cdef extern from "wrap.h":
    void pm_assign_Int "WRAP_OUT" (pm_PerlPropertyValue, int)
    void pm_assign_Matrix "WRAP_OUT" (pm_PerlPropertyValue, pm_Matrix[pm_Integer])
    void pm_assign_Matrix "WRAP_OUT" (pm_PerlPropertyValue, pm_Matrix[pm_Rational])
    void pm_assign_Matrix "WRAP_OUT" (pm_PerlPropertyValue, pm_Matrix[pm_QuadraticExtension])

    # set a single entry of a matrix
    void pm_Matrix_set[T](pm_Matrix[T]&, int, int, const T&)
    const T& pm_Matrix_get[T](const pm_Matrix[T]&, int, int)

    # the except clause below is fake
    # it is used to catch errors in PerlObject.give(), however adding
    # the except statement to the declaration of give() makes cython
    # split lines like
    #        pm_get(self.pm_obj.give(prop), pm_res)
    # and store the result of give() first. This causes problems since
    # pm_PerlPropertyValue doesn't have a default constructor.

    # WRAP_IN(x,y) x>>y
#    void pm_get_float "WRAP_IN" (pm_PerlPropertyValue, float) except +ValueError


cdef extern from "polymake/PowerSet.h" namespace "polymake":
    cdef cppclass pm_PowerSet "PowerSet" [E]:
        int size()

cdef extern from "polymake/SparseVector.h" namespace "polymake":
    pass

###############################################################################
# Polymake utilities                                                          #
###############################################################################

cdef extern from "polymake/Main.h" namespace "polymake":
    cdef cppclass Main:
        Main()
        Main(string)
        void set_application(string) except +
        void set_preference(string) except +
        void pm_include "include" (string) except +

cdef extern from "polymake/client.h":
    cdef cppclass pm_PerlPropertyValue "perl::PropertyValue":
        pass

    cdef cppclass pm_PerlObject "perl::Object":
        pm_PerlObject()
        pm_PerlObject(string) except +
        pm_PerlObject(pm_PerlObject&) except+
        bool valid()
        void VoidCallPolymakeMethod(char*) except +
        void save(char*)
        pm_PerlObject copy()


# HOW DO WE ACCESS ELEMENTS OF ARRAYS, ETC?
#        long get_long_from_int "operator[]" (int i)
#        pm_PerlObject get_PerlObject_from_int "operator[]" (int i)

        pm_PerlPropertyValue take(string&)
        pm_PerlPropertyValue give(string&) # do not add except here, see pm_get for why
        pm_PerlObjectType type()
        int exists(const string& name)
        string name()
        string description()
        bool isa(pm_PerlObjectType)
        pm_PerlObject parent()

    cdef cppclass pm_PerlObjectType "perl::ObjectType":
#        pm_PerlObjectType(AnyString&)
        string name()
#        bool isa "isa" (AnyString&)

# in beta, CallPolymakeFunction is deprecated in favor of
#   call_method and call_function
#    pm_PerlObject CallPolymakeFunction (char*) except +ValueError
#    pm_PerlObject CallPolymakeHelp "CallPolymakeFunction" \
#            (char *, char *) except +ValueError
#    pm_PerlObject CallPolymakeFunction1 "CallPolymakeFunction" \
#            (char*, int) except +ValueError
#    pm_PerlObject CallPolymakeFunction2 "CallPolymakeFunction" \
#            (char*, int, int) except +ValueError
#    pm_PerlObject CallPolymakeFunction3 "CallPolymakeFunction" \
#            (char*, int, int, int) except +ValueError

    pm_PerlObject call_function "polymake::call_function" (string) except+
    pm_PerlObject call_function "polymake::call_function" (string, int) except+
    pm_PerlObject call_function "polymake::call_function" (string, int, int) except+
    pm_PerlObject call_function "polymake::call_function" (string, int, int, int) except+
    pm_Map[string,string] call_function "polymake::call_function" (string, pm_PerlObject) except+

    pm_PerlObject* new_PerlObject_from_PerlObject "new perl::Object" (pm_PerlObject)


