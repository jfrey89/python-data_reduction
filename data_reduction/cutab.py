#!/usr/bin/env python

import numpy as np
import data_reduction.bisection as bs


def cutab(norm, xi, eps, r):
    C = 1e5
    eta = 0.5
    k = r - 1
    T = np.zeros(np.shape(xi))
    a, b = xi[0], xi[-1]

    # Statement (1)
    E = C * eps

    T[0] = a
    j = 1
    F = lambda x: np.abs(np.power(x - T[j - 1], k)) * norm(T[j - 1], x)

    while True:
        # if we're not on the first iteration
        if F(b) > E:
            g = lambda x: F(x) - E
            x_e = bs.bisect(g, T[j - 1], b)
            T[j] = x_e
            j += 1
        elif np.abs(
            norm(T[j - 1], b) - E / np.abs(np.power(b - T[j - 1], k))
        ) < 10e-8:
            T[j] = b
            n = j
            return np.trim_zeros(T, 'b'), eps
        elif F(b) < E:
            #print "shrink eps: %e -> %e" % (eps, eps * eta)
            T[j] = b
            n = j
            #print "eps = %e" % eps
            #print "too small...\nRetrying."
            eps = eps * eta
            break

    n0 = n
    print "# of knots:\t%d" % n0

    for iteration in range(0, 100):
        E = C * eps
        T = np.zeros(np.shape(T))
        T[0] = a
        j = 1
        while True:
            F = lambda x: np.abs(np.power(x - T[j - 1], k)) * norm(T[j - 1], x)

            if j <= n0:
                if F(b) > E:
                    g = lambda x: F(x) - E
                    x_e = bs.bisect(g, T[j - 1], b)
                    T[j] = x_e
                    j += 1
                elif np.abs(
                    norm(T[j - 1], b) - E / np.abs(np.power(b - T[j - 1], k))
                ) < 10e-8:
                    T[j] = b
                    return np.trim_zeros(T, 'b'), eps
                elif F(b) < E:
                    T[j] = b
                    #print "eps = %e" % eps
                    #print "too small...\nRetrying."
                    eps = eps * eta
                    break
            elif j > n0:
                eta = np.sqrt(eta)
                F = np.abs(np.power(b - T[n0 - 1], k)) * norm(T[n0 - 1], b)
                if F < E:
                    #print "eps = %e" % eps
                    #print "too small...\nRetrying."
                    eps = eps * eta
                    break
                else:
                    #print "eps = %e" % eps
                    #print "Too large.\nRetrying."
                    eps = eps / eta
                    break

    return np.trim_zeros(T, 'b'), eps
