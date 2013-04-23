import numpy as np
import scipy.misc as sc
from scipy.interpolate import interp1d
from NewtonPolynomial import NewtonPolynomial


class Norm(object):
    def __init__(self, df):
        self.points = np.c_[df.x, df.y]
        self.vals = self._integrate()
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
        (i, k) = np.searchsorted(x, [t0, t1]) + np.array([1, -1])
        return np.trapz(df([t0, x[i]]), [t0, x[i]]) + \
            self.vals[k] - self.vals[i] + \
            np.trapz(df([x[k], t1]), [x[k], t1])

    def _integrate(self):
        x, f = self.x, self.f
        frnm = np.zeros(len(x) - 1)

        for i in np.arange(1, len(x)):
            frnm[i - 1] = np.trapz(f[:i + 1], x[: i + 1])

        return frnm


def diff(newtpoly, r=4):
    if not isinstance(newtpoly, NewtonPolynomial):
        raise ValueError('Input must be Newton polynomial')

    if r % 2 == 1:
        raise ValueError('k must be even for now')

    x = newtpoly.x
    y = np.zeros(len(x))
    y[r / 2:len(x) - r / 2] = sc.factorial(r) * newtpoly.divdiffcol(r + 1)

    for i in range(r / 2):
        m = r / 2 - i
        y[m - 1] = linear_ext(x[m - 1], np.c_[x[m:m + 2], y[m:m + 2]])
        y[-m] = linear_ext(x[-m], np.c_[x[-(m + 2):-m], y[-(m + 2):-m]])

    return y


def linear_ext(x, pts):
    xi, yi = pts[:, 0], pts[:, 1]
    return yi[0] + (x - xi[0]) * (yi[1] - yi[0]) / (xi[1] - xi[0])


if __name__ == "__main__":
    xi = np.linspace(-5, 5, 101)
    pts = np.c_[xi, np.sin(xi)]
    pN = NewtonPolynomial(points=pts)
    pN4_norm = Norm(interp1d(xi, diff(pN, r=4)))
    pass
