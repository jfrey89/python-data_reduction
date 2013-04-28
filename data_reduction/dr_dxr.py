#1/usr/bin/env python

from scipy.interpolate import interp1d
from scipy.misc import factorial
import numpy as np


def dr_dxr(f, r=4):
    xi = f.x
    yi = np.zeros(len(xi))
    yi[r / 2:len(xi) - r / 2] = factorial(r) * f.divdiff(r)

    for i in np.arange(r / 2):
        m = r / 2 - i
        yi[m - 1] = extrapolate(xi[m - 1], np.c_[xi[m:m + 2], yi[m:m + 2]])
        yi[-m] = extrapolate(xi[-m], np.c_[xi[-(m + 2):-m], yi[-(m + 2):-m]])

    return interp1d(xi, yi)


def extrapolate(x, pts):
    xi, yi = pts[:, 0], pts[:, 1]
    return yi[0] + (x - xi[0]) * (yi[1] - yi[0]) / (xi[1] - xi[0])
