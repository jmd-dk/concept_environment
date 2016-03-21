##################################
# main.py, which may be compiled #
##################################
"""
This file imports the fibonacci module and call its "fib" function.
This only works when running in compiled mode (commons.py, fibonacci.py
and main.py are all compiled to *.so) or when running in pure Python mode
(no *.so files exist in the directory).
"""

# Always include this as the first statement of modules which should be compiled
from commons import *

# Normal imports
import numpy as np
import time

# Enclose import statements inside cimport function
# calls when importing from compiled modules.
cimport('import fibonacci')

# Declare global variables
cython.declare(N='int',         # C int
               F='int',
               T='double',      # C double
               n='int[::1]',    # Contiguous array of C ints. For e.g. 2D arrays, use 'int[:, ::1]'
               f='int[::1]',
               t='double[::1]',
               t_before='double',
               t_after='double',
               i='Py_ssize_t',  # Analogous to ptrdiff_t. Use this (or indeed ptrdiff_t) for array indexing. 
               )

# Initialize arrays for storing data
N = 32
n = np.empty(N, dtype=C2np['int'])  # Note the symmetric syntax (no 'intc')
f = np.empty(N, dtype=C2np['int'])
t = np.empty(N, dtype=C2np['double'])

# For each n, compute fib(n) and store the result in f.
# Also store the computation time in t.
for i in range(N):
    # Do timed call to fibonacci.pfib
    t_before = time.time()
    F = fibonacci.pfib(i)
    t_after = time.time()
    T = t_after - t_before
    # Save the results in the arrays
    n[i] = i
    f[i] = F
    t[i] = T

# Print out a table with (n, fib(n), computation time)
print(' n |  fib(n) | computation time (s)')
print('-----------------------')
for N, F, T in zip(n, f, t):  
    print('%2d | %7d | %.6f' % (N, F, T))

# End of program. If not excited explicitly,
# an error will be thrown when running in compiled mode.
sys.exit()

