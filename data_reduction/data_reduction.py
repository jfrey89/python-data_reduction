import numpy as np
import scipy.misc as sc
from scipy.interpolate import interp1d
from NewtonPolynomial import NewtonPolynomial


class Integral(object):
    def __init__(self, df):
        self.points = np.c_[df.x, df.y]
        self.frnm = self.integrate()
        self.df = df

    @property
    def x(self):
        return self.points[:, 0]

    @property
    def f(self):
        return self.points[:, 1]

    def __call__(self, t0, t1):
        x = self.x
        df = self.df
        (i, k) = np.searchsorted(x, [t0, t1]) + np.c_[1, -1]
        ivl0 = np.c_[t0, x[i]]
        ivl1 = np.c_[x[k], t1]
        return np.trapz(df(ivl0), ivl0) + self.fnrm[k] - self.fnrm[i] + \
            np.trapz(df(ivl1), ivl1)

    def integrate(self):
        x, f = self.x, self.f
        frnm = np.zeros(len(x) - 1)

        for i in np.arange(1, len(x)):
            frnm[i - 1] = np.trapz(f[:i + 1], x[: i + 1])

        return frnm


def differentiate(newtpoly, k=4):
    """
    Computes a linear interpolant approximation of the Newton Polynomial
    {newtpoly} derivative. Assumes you want the {k} = 4th derivative but
    others should be supported.

    Returns an {interp1d} class from {scipy.interpolate}.
    """
    if not isinstance(newtpoly, NewtonPolynomial):
        raise ValueError('Input must be Newton polynomial')

    if k % 2 == 1:
        raise ValueError('k must be even for now')

    x = newtpoly.x
    y = np.zeros(len(x))
    y[k / 2:len(x) - k / 2] = sc.factorial(k) * newtpoly.divdiffcol(k + 1)

    for i in range(k / 2):
        m = k / 2 - i
        y[m - 1] = linextrap(x[m - 1], np.c_[x[m:m + 2], y[m:m + 2]])
        y[-m] = linextrap(x[-m], np.c_[x[-(m + 2):-m], y[-(m + 2):-m]])

    return interp1d(x, y)


def linextrap(x, pts):
    xi, yi = pts[:, 0], pts[:, 1]
    return yi[0] + (x - xi[0]) * (yi[1] - yi[0]) / (xi[1] - xi[0])


if __name__ == "__main__":
    xi = np.linspace(-5, 5, 101)
    pts = np.c_[xi, np.sin(xi)]
    pN = NewtonPolynomial(points=pts)
    d4pN = differentiate(pN)
    # frnm = integrate(np.c_[d4pN.x, d4pN.y])
    pass
