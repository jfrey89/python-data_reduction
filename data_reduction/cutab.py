#!/usr/bin/env python

import numpy as np
from data_reduction.bisection import bisection


def F(norm, a, b, k):
    return np.power(np.abs(b - a), k) * norm(a, b)


def cutab(norm, xi, eps, r, n0):
    C = 100
    E = C * eps
    k = r - 1

    b = xi[-1]
    T = np.array([xi[0]])
    j = 1

    while j <= n0:
        
        g = lambda x: np.abs(np.power(x - T[j-1], k)) * norm(T[j-1], x)
        
        if g(b) > E:
            h = lambda x: g(x) - E
            x_e = bisection(h, T[j-1], b)
            T = np.append(T, x_e)
            j += 1
        elif g(b) == E:
            T = np.append(T, b)
            return T
        elif g(b) < E:
            T = np.append(T, b)
            break
        else:
            print "You derp'd. Good job."
            return False

    pass
