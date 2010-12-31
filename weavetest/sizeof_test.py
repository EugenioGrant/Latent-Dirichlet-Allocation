
import scipy as sp

def sizeof_C_explore():

    tmp = [2, 3 , 3]
    # quick check of what is happenign in C on my arch
    code = """

       printf("The size of int is: %d", sizeof(int));
       printf("The size of long is: %d", sizeof(long));
       printf("The size of float is: %d", sizeof(float));
       printf("The size of double is: %d", sizeof(double));

    """

    err = sp.weave.inline( code,
                           ['tmp' ],
                           compiler='gcc')
    return err


def sizeof_numpy_vec(vec):
    """
    hand over a 1D numpy arrays to C
    and see what it looks like.
    """

    assert len(vec.shape) == 1

    code = """

        // CXX listlike API
        /* it appears not to be available for numpy arrays :
            printf("array has size: %d \\n", vec.length()  );
            printf("last entry contains: %d \\n", vec[vec.length()-1]  );
            printf("\\n");
        */

        // CXX numpy API
        /* Somewhere in the header file for this code there is this code:
            npy_intp* Nvec = vec_array->dimensions;
            npy_intp* Svec = vec_array->strides;
            int Dvec = vec_array->nd;
           so weave has made available to us the following attributes:
            Svec[0] = how much to jump between vec[0] and vec[1]
            Svec[1] = how much to jump between vec[i][0] and vec[i][1] (if 2d or more array)
                        (note this is the C style layout, Fortran might be different)
            Nvec[0] = len(vec)
            Dvec[0] = len(vec.shape) = vec.nd
        */
        printf("array has size: %d \\n", Nvec[0]  );
        printf("array has dimension: %d \\n", Dvec  );
        printf("last entry contains: %d \\n", vec[Nvec[0]-1]  );
        printf("\\n");

        // try to brake things ... index out of bound:
        printf("last entry contains: %d \\n", vec[Nvec[0]]  );
        printf("\\n");

        // Numpy/Python C API


    """

    err = sp.weave.inline( code,
                           ['vec' ],
                           compiler='gcc')
    return err


def sizeof_numpy_mat(mat):
    """
    hand over a 2D numpy arrays to C
    and see what it looks like.

    >>> import numpy as np

    >>> a=np.array([[1,2,3],[5,55,5555]])
    >>> sizeof_numpy_mat(a)
    array has 2 rows
    array has 3 columns
    1, 2, 3,
    3, 5, 55,
    1, 2, 3, 5, 55, 5555,

    >>> a=np.array([[1,2,3],[5,55,5555]], order='F')
    >>> sizeof_numpy_mat(a)
    array has 2 rows
    array has 3 columns
    1, 5, 2,
    2, 55, 3,
    1, 5, 2, 55, 3, 5555,

    """
    assert len(mat.shape) == 2

    code = """

        // CXX numpy API
        /*
            Svec[0] = how much to jump between vec[0] and vec[1]
            Svec[1] = how much to jump between vec[i][0] and vec[i][1] (if 2d or more array)
                        (note this is the C style layout, Fortran might be different)
            Nvec[0] = len(vec)
            Dvec[0] = len(vec.shape) = vec.nd
        */

        int i, j, ij;
        int nc, nr;

        nr=Nmat[0];
        nc=Nmat[1];

        printf("array has %d rows \\n", Nmat[0]  );
        printf("array has %d columns \\n", Nmat[1]  );

        for(i=0; i<nr; i++){

            for(j=0; j<nc; j++){
                printf("%d, ", mat[i*nr+j]  );
            }
            printf("\\n");
        }

        // traverse array sequentially as it were a vector
        for(ij=0; ij<nr*nc; ij++){
            printf("%d, ", mat[ij]  );
        }
        printf("\\n");


        // weave macros with normal brackets
        /*  In the C code generated by weave there
            are macros of the form:

                py_mat = get_variable("mat",raw_locals,raw_globals);
                PyArrayObject* mat_array = convert_to_numpy(py_mat,"mat");
                conversion_numpy_check_type(mat_array,PyArray_INT,"mat");
                #define MAT1(i) (*((int*)(mat_array->data + (i)*Smat[0])))
                #define MAT2(i,j) (*((int*)(mat_array->data + (i)*Smat[0] + (j)*Smat[1])))
                #define MAT3(i,j,k) (*((int*)(mat_array->data + (i)*Smat[0] + (j)*Smat[1] + (k)*Smat[2])))
                #define MAT4(i,j,k,l) (*((int*)(mat_array->data + (i)*Smat[0] + (j)*Smat[1] + (k)*Smat[2] + (l)*Smat[3])))
                npy_intp* Nmat = mat_array->dimensions;
                npy_intp* Smat = mat_array->strides;
                int Dmat = mat_array->nd;
                int* mat = (int*) mat_array->data;

             so presumably I should be able to access the matrix elements as
             MAT2(i,j)
            */


        // Numpy/Python C API

    """

    err = sp.weave.inline( code,
                           ['mat' ],
                           compiler='gcc')
    return err



