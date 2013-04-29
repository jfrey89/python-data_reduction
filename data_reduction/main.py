#!/usr/bin/env python

import numpy as np
import data_reduction as dr

# main()
if __name__ == "__main__":
    # dummy data
    tau = 10e-8
    eps = tau
    xi = np.linspace(-5, 5, 101)
    yi = 1 / (1 + np.power(xi, 2))
    knots = np.c_[xi, yi]
    r = 4
    p = dr.Newton(points=knots)
    d4p = dr.dr_dxr(p, r=4)
    norm = dr.Norm(d4p)
    #g = lambda x: np.abs(np.power(x - xi[0], 3)) * norm(xi[0], x)
    #h = lambda x: g(x) - 0.1
    #x_e = bisection(h, xi[0], xi[-1])

    # First run of middle loop

    pass
