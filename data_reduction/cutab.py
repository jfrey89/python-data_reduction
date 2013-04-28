#!/usr/bin/env python

import numpy as np


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

        g = lambda x: norm(T[j-1], x) - E

        pass

    pass
