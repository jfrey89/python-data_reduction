#!/usr/bin/env python

import numpy as np
import data_reduction.polynomial as poly
import data_reduction.dr_dxr as deriv
import data_reduction.norm as norm
import scipy.interpolate.fitpack as fitpack
import matplotlib.pyplot as plt
import data_reduction.cutab as cut
import os

# main()
if __name__ == "__main__":
    # dummy data
    run_count = 1
    r = 4
    tol = 1e-3
    eps = tol

    #xi = np.linspace(-5, 5, 101)
    #f = lambda x: 1 / (1 + np.power(x, 2))
    #xi_hd = np.linspace(-5, 5, 1001)

    xi = np.linspace(-2, 2, 101)
    f = lambda x: 10 * x / (1 + 100 * np.power(x, 2))
    xi_hd = np.linspace(-2, 2, 1001)

    #xi = np.linspace(-5, 5, 101)
    #f = lambda x: np.abs(x)
    #xi_hd = np.linspace(-5, 5, 1001)

    #xi = np.linspace(0, 2, 101)
    #f = lambda x: np.sqrt(x)
    #xi_hd = np.linspace(0, 2, 1001)

    #xi = np.linspace(0, 5, 101)
    #f = lambda x: np.power(x, 4)
    #xi_hd = np.linspace(0, 5, 1001)

    yi = np.zeros(np.shape(xi))
    yi_hd = np.zeros(np.shape(xi_hd))
    yi[:] = f(xi[:])
    yi_hd = f(xi_hd[:])

    #xi = np.linspace(-2, 2, 101)
    #yi = 10 * xi / (1 + 100 * np.power(xi, 2))
    data = np.c_[xi, yi]

    p = poly.NewtonPolynomial(points=data)
    d4p = deriv.dr_dxr(p, r=4)
    norm = norm.Norm(d4p)
    T, eps = cut.cutab(norm, xi, eps, r)

    tck = fitpack.splrep(xi, yi, t=T[1:-1])
    fit = fitpack.splev(xi, tck)
    error = np.abs(fit - yi)
    print '*' * 10 + " FIRST ERROR RATIO " + '*' * 10 + '\n\n'
    print "error / tol = %f" % (error.max() / tol)

    while error.max() > tol:
        T, eps = cut.cutab(norm, xi, eps, r)
        print "\n\nRun %d" % run_count
        print "eps = %e in outer loop" % eps
        eps = eps / 2
        tck = fitpack.splrep(xi, yi, t=T[1:-1])
        fit = fitpack.splev(xi, tck)
        fit_hd = fitpack.splev(xi_hd, tck)
        fT = np.zeros(np.shape(T))
        fT[:] = f(T[:])
        error = np.abs(fit - yi)
        print "Error %e\n" % error.max()
        files = []
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.cla()
        ax.plot(xi_hd, yi_hd, 'b', linewidth=2.0)
        ax.plot(xi_hd, fit_hd, 'r--', linewidth=2.0)
        midpoint = (yi.max() + yi.min()) / 2.0
        ax.plot(T, midpoint * np.ones(len(T)), 'ko')
        ax.grid(color='grey')
        ax.set_title('# of knots: %d; error = %.1e; eps = %.1e' %
                    (len(T), error.max(), eps))
        fname = '_tmp%03d.png' % run_count
        print 'Saving frame', fname
        fig.set_size_inches(19.2, 10.8)
        fig.savefig(fname)
        files.append(fname)
        run_count += 1
        plt.close('all')

    print '*' * 10, "MAKING MOVIE out.mp4", '*' * 101
    print 'this may take a while'
    os.system("avconv -r 1/2 -i _tmp%03d.png -c:v libx264 -r 30 -b 65536k \
            out.mp4")
    os.system('rm _tmp*')

    pass
