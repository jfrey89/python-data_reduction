#!/usr/bin/env python

import numpy as np
import data_reduction as dr


def cutab(norm, xi, eps, r):
    C, eta = 1, 0.5
    k = r - 1
    a, b = xi[0], xi[-1]
    E, T = C * eps, np.array([a])

    n0 = len(xi)
    j = 1

    while True:

        if j <= n0:
            F = lambda x: np.abs(np.power(x - T[j - 1], k)) * norm(T[j - 1], x)
            if F(b) > E:
                g = lambda x: F(x) - E
                x_e = dr.bisection(g, T[j - 1], b)
                T = np.append(T, x_e)
                j += 1
            elif F(b) == E:
                T = np.append(T, b)
                n = j
                return T
            elif F(b) < E:
                T = np.append(T, b)
                eps = eta * eps
                E = C * eps
                n = j
                j = 1
            else:
                return False
        elif j > n0:
            eta = np.sqrt(eta)
            if np.abs(np.power(b - T[n0 - 1], 3)) * norm(T[n0 - 1], b) < E:
                eps = eps * eta
            else:
                eps = eps / eta

            j = 1
