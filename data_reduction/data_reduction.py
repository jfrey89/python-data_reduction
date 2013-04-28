#!/usr/bin/env python

import numpy as np
from data_reduction.polynomial import Monomial, Newton
from data_reduction.dr_dxr import dr_dxr
from data_reduction.norm import Norm

# main()
if __name__ == "__main__":
    # dummy data
    xi = np.linspace(-5, 5, 101)
    yi = 1 / (1 + np.power(xi, 2))
    knots = np.c_[xi, yi]
    r = 4

    p = Newton(points=knots)
    q = Monomial(points=knots)
    d4p = dr_dxr(p, r=4)
    norm = Norm(d4p)
    pass
