#####################################################
# main_pure_python.py, which should not be compiled #
#####################################################
"""
This file imports the fibonacci module and call its "pfib" function.
This works when commons.py and fibonacci.py are both compiled to *.so
while this file remain uncompiled, or when running in pure Python mode
(no *.so files exist in the directory).
"""

# Normal imports
import numpy as np
import time

# Import fibonacci as usual, even though this module may be compiled
import fibonacci

# Initialize arrays for storing data
N = 32
n = np.empty(N, dtype='intc')    # Contiguous array of C ints
f = np.empty(N, dtype='intc')
t = np.empty(N, dtype='double')  # Contiguous array of C doubles

# For each n, compute fib(n) and store the result in f.
# Also store the computation time in t.
for i in range(N):
    # Do timed call to fibonacci.pfib
    t_before = time.time()
    F = fibonacci.pfib(i)  # Note: fibonacci.fib(i) will not work!
    t_after = time.time()
    # Save the results in the arrays
    n[i] = i
    f[i] = F
    t[i] = t_after - t_before

# Print out a table with (n, fib(n), computation time)
print(' n |  fib(n) | computation time (s)')
print('-----------------------')
for N, F, T in zip(n, f, t):  
    print('%2d | %7d | %.6f' % (N, F, T))

