#!/usr/bin/env python

import numpy as np
import data_reduction.bisection as root


def cutab(norm, xi, eps, r):
    C = 5000
    eta = 0.5
    k = r - 1
    T = np.zeros(np.shape(xi))
    a, b = xi[0], xi[-1]
    print '*' * 20
    print "Initialized"
    print '*' * 20
    print "\n\n"

    # Statement (1)
    E = C * eps

    print "First run."
    T[0] = a
    j = 1
    F = lambda x: np.abs(np.power(x - T[j - 1], k)) * norm(T[j - 1], x)

    while True:
        if F(b) > E:
            print "Adding a new point."
            g = lambda x: F(x) - E
            x_e = root.bisection(g, T[j - 1], b)
            T[j] = x_e
            j += 1
        elif np.abs(
            norm(T[j - 1], b) - E / np.abs(np.power(b - T[j - 1], k))
        ) < 10e-8:
            print "Equality reached.\nTerminating!"
            T[j] = b
            n = j
            return np.trim_zeros(T, 'b')
        elif F(b) < E:
            print "Adjusting epsilon."
            T[j] = b
            n = j
            eps = eps * eta
            break
        else:
            print "It broke."

    n0 = n

    for iteration in range(0, 10):
        E = C * eps
        T = np.zeros(np.shape(T))
        T[0] = a
        j = 1
        while True:
            F = lambda x: np.abs(np.power(x - T[j - 1], k)) * norm(T[j - 1], x)

            if j <= n0:
                if F(b) > E:
                    g = lambda x: F(x) - E
                    x_e = root.bisection(g, T[j - 1], b)
                    T[j] = x_e
                    j += 1
                elif np.abs(
                    norm(T[j - 1], b) - E / np.abs(np.power(b - T[j - 1], k))
                ) < 10e-8:
                    T[j] = b
                    return np.trim_zeros(T, 'b')
                elif F(b) < E:
                    T[j] = b
                    eps = eps * eta
                    break
            elif j > n0:
                eta = np.sqrt(eta)
                F = np.abs(np.power(b - T[n0 - 1], k)) * norm(T[n0 - 1], b)
                if F < E:
                    print "too large"
                    eps = eps * eta
                    break
                else:
                    print "too small"
                    eps = eps / eta
                    break
    return np.trim_zeros(T, 'b')
