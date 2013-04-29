#!/usr/bin/env python

import numpy as np
import data_reduction.bisection as root


def cutab(norm, xi, eps, r):
    C, eta = 100, 0.5
    k = r - 1
    a, b = xi[0], xi[-1]
    E, T = C * eps, np.array([a])
    j = 1

    while True:
        if j <= n0:
            F = lambda x: np.abs(np.power(x - T[j - 1], k)) * norm(T[j - 1], x)
            if F(b) > E:
                g = lambda x: F(x) - E
                x_e = root.bisection(g, T[j - 1], b)
                T = np.append(T, x_e)
                j += 1
            elif np.abs(norm(T[j - 1], b) -
                        E / np.abs(np.power(b - T[j - 1], k))) < 10e-8:
                T = np.append(T, b)
                return T
            elif F(b) < E:
                T = np.append(T, b)
                eps = eta * eps
                E = C * eps
                eps = eps * eta
                T = np.array([a])
                j = 1

        elif j > n0:
            eta = np.sqrt(eta)
            if np.abs(np.power(b - T[n0 - 1], 3)) * norm(T[n0 - 1], b) < E:
                eps = eps * eta
            else:
                eps = eps / eta

            T = np.array([a])
            j = 1

    return T
