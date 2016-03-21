# Define the encoding, for Python 2 compatibility:
# This Python file uses the following encoding: utf-8

# This file is part of the CO𝘕CEPT environment, the programming environment
# which makes writing clean and efficient Cython code easy.
# The CO𝘕CEPT environment can be viewed as a standalone application,
# but is really a small part of the larger CO𝘕CEPT code,
# the cosmological 𝘕-body code in Python. The CO𝘕CEPT environment
# and CO𝘕CEPT therefore share the same copyright. For this copyright,
# confront the header of e.g.
# https://raw.githubusercontent.com/jmd-dk/concept/master/installer
# Copyright © 2015-2016 Jeppe Mosgaard Dakin.
#
# The auther of the CO𝘕CEPT environment can be contacted at
# dakin(at)phys.au.dk
# The latest version of the CO𝘕CEPT environment is available at
# https://github.com/jmd-dk/concept_environment/


# This module contains imports, Cython declarations and values
# of parameters common to all other modules. Each module should have
# 'from commons import *' as its first statement.



############################################
# Imports common to pure Python and Cython #
############################################
# Import functionality from the future, for Python 2 compatibility
from __future__ import absolute_import, division, print_function, unicode_literals

# Miscellaneous modules
import contextlib, ctypes, cython, inspect, numpy as np, re, sys, unicodedata



###########
# C types #
###########
# Import the signed integer type ptrdiff_t
pxd = """
from libc.stddef cimport ptrdiff_t
"""
# C type names to NumPy dtype names
cython.declare(C2np='dict')
C2np = {# Booleans
        'bint': np.bool,
        # Integers
        'char'         : np.byte,
        'short'        : np.short,
        'int'          : np.intc,
        'long int'     : np.long,
        'long long int': np.longlong,
        'ptrdiff_t'    : np.intp,
        'Py_ssize_t'   : np.intp,
        # Unsgined integers
        'unsigned char'         : np.ubyte,
        'unsigned short'        : np.ushort,
        'unsigned int'          : np.uintc,
        'unsigned long int'     : np.uint,
        'unsigned long long int': np.ulonglong,
        'size_t'                : np.uintp,
        # Floating-point numbers
        'float'     : np.single,
        'double'    : np.double,
        'long float': np.longfloat,
        }
# In NumPy, binary operations between some unsigned int types (unsigned
# long int, unsigned long long int, size_t) and signed int types results
# in a double, rather than a signed int.
# Get around this bug by never using these particular unsigned ints.
if not cython.compiled:
    C2np['unsigned long int'] = C2np['long int']
    C2np['unsigned long long int'] = C2np['long long int']
    C2np['size_t'] = C2np['ptrdiff_t']



#####################
# Pure Python stuff #
#####################
# Definitions used by pure Python to understand Cython syntax
if not cython.compiled:
    # No-op decorators for Cython compiler directives
    def dummy_decorator(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # Called as @dummy_decorator. Return function
            return args[0]
        else:
            # Called as @dummy_decorator(*args, **kwargs).
            # Return decorator
            return dummy_decorator
    # Already builtin: cfunc, inline, locals, returns
    for directive in ('boundscheck',
                      'cdivision',
                      'initializedcheck',
                      'wraparound',
                      'header',
                      'pheader',
                      ):
        setattr(cython, directive, dummy_decorator)
    # Address (pointers into arrays)
    def address(a):
        dtype = re.search('ctypeslib\.(.*?)_Array', np.ctypeslib.as_ctypes(a).__repr__()).group(1)
        return a.ctypes.data_as(ctypes.POINTER(eval('ctypes.' + dtype)))
    setattr(cython, 'address', address)
    # C allocation syntax for memory management
    def sizeof(dtype):
        # C dtype names to Numpy dtype names
        if dtype in C2np:
            dtype = C2np[dtype]
        elif dtype in ('func_b_ddd',
                       'func_d_dd',
                       'func_d_ddd',
                       'func_ddd_ddd',
                       ):
            dtype='object'
        elif dtype[-1] == '*':
            # Allocate pointer array of pointers (eg. int**).
            # Emulate these as lists of arrays.
            return [empty(1, dtype=sizeof(dtype[:-1]).dtype)]
        elif master:
            abort(dtype + ' not implemented as a Numpy dtype in commons.py')
        return np.array([1], dtype=dtype)
    def malloc(a):
        if isinstance(a, list):
            # Pointer to pointer represented as list of arrays
            return a
        return empty(a[0], dtype=a.dtype)
    def realloc(p, a):
        # Reallocation of pointer assumed
        p.resize(a[0], refcheck=False)
        return p
    def free(a):
        pass
    # Casting
    def cast(a, dtype):
        match = re.search('(.*)\[', dtype)
        if match:
            # Pointer to array cast assumed
            # (array to array in pure Python).
            return a
        else:
            # Scalar
            return C2np[dtype](a)
    # Mathematical functions
    from numpy import (sin, cos, tan,
                       arcsin,  arccos, arctan,
                       sinh, cosh, tanh,
                       arcsinh, arccosh, arctanh,
                       exp, log, log2, log10,
                       sqrt,
                       round,
                       )
    from math import erf, erfc
    # Dummy ℝ dict for constant expressions
    class DummyDict(dict):
        def __getitem__(self, key):
            return key
    if sys.version_info.major > 2:
        exec('ℝ = DummyDict()')
    # The cimport function, which in the case of pure Python should
    # simply execute the statements parsed to it as a string.
    def cimport(import_statement):
        exec(import_statement, inspect.getmodule(inspect.stack()[1][0]).__dict__)



###################################
# Cython imports and declarations #
###################################
pxd = """
# Get full access to all of Cython
cimport cython
# Functions for manual memory management
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
# Function type definitions of the form func_returntype_argumenttypes
ctypedef bint    (*func_b_ddd)  (double, double, double)
ctypedef double  (*func_d_dd)   (double, double)
ctypedef double  (*func_d_ddd)  (double, double, double)
ctypedef double* (*func_ddd_ddd)(double, double, double)
# Mathematical functions
from libc.math cimport (sin, cos, tan,
                        asin as arcsin, 
                        acos as arccos, 
                        atan as arctan,
                        sinh, cosh, tanh,
                        asinh as arcsinh, 
                        acosh as arccosh, 
                        atanh as arctanh,
                        exp, log, log2, log10,
                        sqrt, erf, erfc,
                        round,
                        )
"""



########################
# The unicode function #
########################
# The pyxpp script convert all Unicode source code characters into
# ASCII. The function below grants the code access to
# Unicode string literals, by undoing the convertion.
if not cython.compiled:
    # Dummy unicode function for pure Python
    def unicode(c):
        return c
else:
    """
    @cython.header(c='str', returns='str')
    def unicode(c):
        if len(c) > 10 and c.startswith('__UNICODE__'):
            c = c[11:]
        c = c.replace('__space__', ' ')
        c = c.replace('__dash__', '-')
        return unicodedata.lookup(c)
    """

