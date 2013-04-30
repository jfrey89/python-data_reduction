#!/usr/bin/env python

import numpy as np
import data_reduction.polynomial as poly
import data_reduction.dr_dxr as deriv
import data_reduction.norm as norm
import scipy.interpolate.fitpack as fitpack
import matplotlib.pyplot as plt

# main()
if __name__ == "__main__":
    import data_reduction.cutab as cut
    # dummy data
    run_count = 1
    r = 4
    tol = 1e-3
    eps = tol
    xi = np.linspace(-5, 5, 101)
    yi = 1 / (1 + np.power(xi, 2))
    #xi = np.linspace(-2, 2, 101)
    #yi = 10 * xi / (1 + 100 * np.power(xi, 2))
    data = np.c_[xi, yi]

    p = poly.Newton(points=data)
    d4p = deriv.dr_dxr(p, r=4)
    norm = norm.Norm(d4p)
    T, eps = cut.cutab(norm, xi, eps, r)

    tck = fitpack.splrep(xi, yi, t=T[1:-1])
    fit = fitpack.splev(xi, tck)
    error = np.abs(fit - yi)
    print "First Error %e\n" % error.max()

    while error.max() > tol:
        T, eps = cut.cutab(norm, xi, eps, r)
        print "\n\nRun %d" % run_count
        print "eps = %e in outer loop" % eps
        eps = eps / 2
        tck = fitpack.splrep(xi, yi, t=T[1:-1])
        fit = fitpack.splev(xi, tck)
        error = np.abs(fit - yi)
        print "Error %e\n" % error.max()
        run_count += 1

    plt.figure()
    plt.plot(xi, yi, 'r')
    f = lambda x: 1 / (1 + x ** 2)
    #f = lambda x: 10 * x / (1 + 100 * x ** 2)
    Ty = np.zeros(len(T))
    for i in range(0, len(T)):
            Ty[i] = f(T[i])

    plt.plot(T, Ty, 'ko')
    plt.plot(xi, fit, 'g')

    lines = plt.plot(xi, yi, xi, fit, T, Ty)
    l1, l2, l3 = lines
    plt.setp(l1, linestyle='_')
    plt.setp(l1, linewidth=2, color='b')
    plt.setp(l2, linestyle='_')
    plt.setp(l2, linewidth=1, color='r')
    plt.setp(l3, linestyle='o')
    plt.setp(l3, linewidth=2, color='r')

    pass
