# Define the encoding, for Python 2 compatibility:
# This Python file uses the following encoding: utf-8
from __future__ import print_function, unicode_literals

# As usual, import everything from the commons module
from commons import *

# Other imports
import time, collections

# Deside which features to show, based on user input
features = ('function call overhead',
            'C library math functions',
            'Expressions of constant value',
            'Integer powers',
            'Memoryviews and pointers',
            )
show_features = collections.OrderedDict([(feature, False) for feature in features])
for i, feature in enumerate(show_features):
    if feature in sys.argv or str(i) in sys.argv:
        show_features[feature] = True
if not any(show_features.values()):
    print('Call this module with one of the following arguments:')
    for i, feature in enumerate(show_features):
        print("{}: '{}'".format(i, feature))

# Define a context manager that can measure time
class Timer:
    def __init__(self, name=''):
        self.name = name
    def __enter__(self):
        self.start = time.clock()
        return self
    def __exit__(self, *args):
        if not any(args):
            self.end = time.clock()
            print(self.name, 'took', (self.end - self.start)*1000, 'ms')

# Global declarations and definitions
cython.declare(N='Py_ssize_t',  # Number of times to call each function
               i='Py_ssize_t',  # Loop index
               )
N = 10000



##########################
# function call overhead #
##########################
def function_call_overhead0(x, y=0):
    return x

@cython.pheader(x='int', y='int')
def function_call_overhead1(x, y=0):
    return x

@cython.header(x='int', y='int')
def function_call_overhead2(x, y=0):
    return x

if show_features['function call overhead']:
    with Timer('function call overhead: fun0') as timer:
        for i in range(N):
            function_call_overhead0(i)
 
    with Timer('function call overhead: fun1') as timer:
        for i in range(N):
            function_call_overhead1(i)

    with Timer('function call overhead: fun2') as timer:
        for i in range(N):
            function_call_overhead2(i)



############################
# C library math functions #
############################
@cython.header(x='double', returns='double')
def C_library_math_functions0(x):
    return np.tan(x)

np_tan = np.tan
@cython.header(x='double', returns='double')
def C_library_math_functions1(x):
    return np_tan(x)

@cython.header(x='double', returns='double')
def C_library_math_functions2(x):
    return tan(x)

if show_features['C library math functions']:
    with Timer('C library math functions: fun0') as timer:
        for i in range(N):
            C_library_math_functions0(i)

    with Timer('C library math functions: fun1') as timer:
        for i in range(N):
            C_library_math_functions1(i)

    with Timer('C library math functions: fun2') as timer:
        for i in range(N):
            C_library_math_functions2(i)



#################################
# Expressions of constant value #
#################################
# NOTE: The ℝ-sybtax is disallowed in pure Python mode by Python 2
var = 42

@cython.header(x='double', returns='double')
def expressions_of_constant_value0(x):
    return x*(sin(1) + sqrt(np.pi/var))

#@cython.header(x='double', returns='double')
#def expressions_of_constant_value1(x):
#    return x*ℝ[sin(1) + sqrt(np.pi/var)]

if show_features['Expressions of constant value']:
    if sys.version_info.major < 3:
        print('This feature is only avialable for Python 3')
    else:
        print("To enable this feature, uncomment the 'expressions_of_constant_value1' function")
    try:
        expressions_of_constant_value1(0)
    except:
        sys.exit()
    with Timer('Expressions of constant value: fun0') as timer:
        for i in range(N):
            expressions_of_constant_value0(i)

    with Timer('Expressions of constant value: fun1') as timer:
        for i in range(N):
            expressions_of_constant_value1(i)



##################
# Integer powers #
##################
cython.declare(ten='int')
ten = 10
@cython.header(x='double', returns='double')
def integer_powers0(x):
    return x**ten

@cython.header(x='double', y='double', returns='double')
def integer_powers1(x):
    x = x*x      # x**2
    y = x*x      # x**4
    y *= y       # x**8
    return y*x   # x**10

@cython.header(x='double', returns='double')
def integer_powers2(x):
    return x**10

if show_features['Integer powers']:
    with Timer('Integer powers: fun0') as timer:
        for i in range(N):
            integer_powers0(i)

    with Timer('Integer powers: fun1') as timer:
        for i in range(N):
            integer_powers1(i)

    with Timer('Integer powers: fun2') as timer:
        for i in range(N):
            integer_powers2(i)



############################
# Memoryviews and pointers #
###########################
M_array = np.empty([10, 10, 10], dtype=C2np['int'])

@cython.header(i='Py_ssize_t', j='Py_ssize_t', k='Py_ssize_t')
def memoryviews_and_pointers0():
    for i in range(M_array.shape[0]):
        for j in range(M_array.shape[1]):
            for k in range(M_array.shape[2]):
                M_array[i, j, k] = i + j + k

cython.declare(M_view='int[:, :, ::1]')
M_view = M_array
@cython.header(i='Py_ssize_t', j='Py_ssize_t', k='Py_ssize_t')
def memoryviews_and_pointers1():
    for i in range(M_view.shape[0]):
        for j in range(M_view.shape[1]):
            for k in range(M_view.shape[2]):
                M_view[i, j, k] = i + j + k

cython.declare(M_ptr='int*')
M_ptr = address(M_view[:, :, :])
@cython.header(i='Py_ssize_t', j='Py_ssize_t', k='Py_ssize_t', index='Py_ssize_t')
def memoryviews_and_pointers2():
    index = 0
    for i in range(M_view.shape[0]):
        for j in range(M_view.shape[1]):
            for k in range(M_view.shape[2]):
                M_ptr[index] = i + j + k
                index += 1

if show_features['Memoryviews and pointers']:
    with Timer('Memoryviews and pointers: fun0') as timer:
        for i in range(N//100):
            memoryviews_and_pointers0()

    with Timer('Memoryviews and pointers: fun1') as timer:
        for i in range(N//100):
            memoryviews_and_pointers1()

    with Timer('Memoryviews and pointers: fun2') as timer:
        for i in range(N//100):
            memoryviews_and_pointers2()

    # Memoryviews can also be constructed from pointers:
    cython.declare(M_view2='int[:, ::1]')
    M_view2 = cast(M_ptr, 'int[:M_array.shape[1]//2, :M_array.shape[2]]')
    print('Block of NumPy array:')
    print(M_array[0, :5, :])
    print('Block of memoryview:')
    print(np.asarray(M_view[0, :5, :]))
    print('New memoryview containing only the block:')
    print(np.asarray(M_view2))



# Exit gracefully
sys.exit()

