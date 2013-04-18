import numpy as np
import scipy.misc as sc
from NewtonPolynomial import NewtonPolynomial
from scipy.interpolate import interp1d


def approxderiv(newtpoly, k=4):
    """
    Computes a linear interpolant approximation of the Newton Polynomial
    {newtpoly}. Assumes you want the {k} = 4th derivative but others should
    be supported.

    Returns an {interp1d} class from {scipy.interpolate}.
    """
    if not isinstance(newtpoly, NewtonPolynomial):
        raise ValueError('Input must be Newton polynomial')

    if k % 2 == 1:
        raise ValueError('k must be even for now')

    x = newtpoly.x
    y = np.zeros(len(x))
    y[k / 2:len(x) - k / 2] = sc.factorial(k) * newtpoly.divdiffcol(k + 1)
    # this should probably be a for loop
    y[1] = linextrap(x[1], np.c_[x[2:4], y[2:4]])
    y[0] = linextrap(x[0], np.c_[x[1:3], y[1:3]])
    y[-2] = linextrap(x[-2], np.c_[x[-4:-2], y[-4:-2]])
    y[-1] = linextrap(x[-1], np.c_[x[-3:-1], y[-3:-1]])
    return interp1d(x, y)


def linextrap(x, pts):
    xi, yi = pts[:, 0], pts[:, 1]
    return yi[0] + (x - xi[0]) * (yi[1] - yi[0]) / (xi[1] - xi[0])

if __name__ == "__main__":
    xi = np.linspace(-5, 5, 101)
    pts = np.c_[xi, np.sin(xi)]
    pN = NewtonPolynomial(points=pts)
    d4pN = approxderiv(pN)
    pass
