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
    tol = 10e-4
    eps = tol

    #xi = np.linspace(-5, 5, 101)
    #f = lambda x: 1 / (1 + np.power(x, 2))

    #xi = np.linspace(-2, 2, 101)
    #f = lambda x: 10 * x / (1 + 100 * np.power(x, 2))

    #xi = np.linspace(0, 2, 101)
    #f = lambda x: np.sqrt(x)

    xi = np.linspace(0, 5, 101)
    f = lambda x: np.power(x, 4)

    yi = np.zeros(np.shape(xi))
    yi[:] = f(xi[:])

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
        fT = np.zeros(np.shape(T))
        fT[:] = f(T[:])
        error = np.abs(fit - yi)
        print "Error %e\n" % error.max()
        files = []
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.cla()
        ax.plot(xi, yi, 'b', xi, fit, 'r--', T, fT, 'ko')
        fname = '_tmp%03d.png' % run_count
        print 'Saving frame', fname
        fig.savefig(fname)
        files.append(fname)
        run_count += 1
        plt.close('all')

    print '*' * 10, "MAKING MOVIE animation.png", '*' * 101
    print 'this may take a while'
    os.system("ffmpeg -qscale 5 -r 0.5 -b 9600 -i _tmp%03d.png movie.mp4")
    os.system('rm _tmp*')

    pass
