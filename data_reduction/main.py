#!/usr/bin/env python

import numpy as np
from data_reduction.polynomial import Newton
from data_reduction.dr_dxr import dr_dxr
from data_reduction.norm import Norm
from data_reduction.bisection import bisection
from data_reduction.cutab import cutab

# main()
if __name__ == "__main__":
    # dummy data
    tau = 10e-4
    eps = tau
    xi = np.linspace(-5, 5, 101)
    yi = 1 / (1 + np.power(xi, 2))
    knots = np.c_[xi, yi]
    r = 4
    p = Newton(points=knots)
    d4p = dr_dxr(p, r=4)
    norm = Norm(d4p)
    #g = lambda x: np.abs(np.power(x - xi[0], 3)) * norm(xi[0], x)
    #h = lambda x: g(x) - 0.1
    #x_e = bisection(h, xi[0], xi[-1])

    # First run of middle loop
    n0 = len(xi)
    cutab(norm, xi, eps, r, n0)

    pass
