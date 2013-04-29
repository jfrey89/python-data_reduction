#!/usr/bin/env python

import numpy as np
from data_reduction.bisection import bisection


def cutab(norm, xi, eps, r, n0):
    k = r - 1
    b = xi[-1]
    C = 100

    E = C * eps
    n0 = len(xi)




def cutab_inner(F, E, n0, a, b, eps):
    T = np.array([a])
    j = 1

    while j <= n0:
        # Define our interval weighting function
        F = lambda x: np.abs(np.power(x - T[j - 1], k)) * norm(T[j - 1], x)

        if F(b) > E:
            # define function to find roots of
            # note that it is monotone increasing
            g = lambda x: F(x) - E
            x_e = bisection(g, T[j - 1], b)
            T = np.append(T, x_e)
            j += 1
        elif F(b) == E:
            T = np.append(T, b)
            n = j
            return T, n
        elif F(b) < E:
            T = np.append(T, b)
            n = j
            eps = 0.5 * eps
        else:
            print "It broke."
            return False
