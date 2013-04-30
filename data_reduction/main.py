#!/usr/bin/env python

import numpy as np
import data_reduction.polynomial as poly
import data_reduction.dr_dxr as deriv
import data_reduction.norm as norm
import matplotlib.pyplot as plt

# main()
if __name__ == "__main__":
    import data_reduction.cutab as cut
    # dummy data
    tau = 10e-4
    eps = tau
    xi = np.linspace(-5, 5, 101)
    yi = 1 / (1 + np.power(xi, 2))
    #yi = np.sin(xi)
    knots = np.c_[xi, yi]
    r = 4
    p = poly.Newton(points=knots)
    d4p = deriv.dr_dxr(p, r=4)
    norm = norm.Norm(d4p)
    T = cut.cutab(norm, xi, eps, r)
    f = lambda x: 1 / (1 + np.power(x, 2))
    Ty = np.zeros(len(T))
    for i in range(0, len(T)):
        Ty[i] = f(T[i])
    plt.figure()
    plt.plot(p.x, p.y)
    plt.plot(T, Ty, 'ro')
    pass
