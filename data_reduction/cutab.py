#!/usr/bin/env python

import numpy as np
from data_reduction.bisection import bisection


def F(norm, a, b, k):
    return np.power(np.abs(b - a), k) * norm(a, b)


def cutab(norm, xi, eps, r, n0):
    C = 100
    k = r - 1
    b = xi[-1]
    T = np.array([xi[0]])
    j = 1
    eta = 0.5

    while j <= n0:
        F = lambda x: np.abs(np.power(x - T[j-1], k)) * norm(T[j-1], x)
        E = C * eps
        
        if F(b) > E:
            g = lambda x: g(x) - E
            x_e = bisection(g, T[j-1], b)
            T = np.append(T, x_e)
            j += 1
        elif F(b) == E:
            T = np.append(T, b)
            return T
        elif F(b) < E:
            T = np.append(T, b)
            if j <= n0:
                eps = eta * eps
        else:
            print "You derp'd. Good job."
            return False
        
    if j > n0:
        print "This is the worst written algorithm ever."
        print "Seriously, fuck this."
        pass
        
            
    