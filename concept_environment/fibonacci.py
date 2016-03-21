from commons import *

@cython.header(n='int',
               returns='int',
               )
def fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


@cython.pheader(n='int',
               returns='int',
               )
def pfib(n):
    if n == 0 or n == 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)

