#!/usr/bin/env python


import numpy as np
import scipy.misc as sc
from scipy.interpolate import interp1d
from data_reduction.polynomial import Newton


def differentiate(f, r=4):
    if not isinstance(f, Newton):
        raise ValueError('Input must be a Newton polynomial')

    if r % 2 == 1:
        raise ValueError('r must be even')

    x = f.x
    y = np.zeros(len(x))
    y[r / 2:len(x) - r / 2] = sc.factorial(r) * f.divdiffcol(r + 1)

    for i in range(r / 2):
        m = r / 2 - i
        y[m - 1] = linear_extrapolate(x[m - 1], np.c_[x[m:m + 2], y[m:m + 2]])
        y[-m] = linear_extrapolate(x[-m], np.c_[x[-(m + 2):-m],
                                                y[-(m + 2):-m]])

    return interp1d(x, y)


def linear_extrapolate(x, pts):
    xi, yi = pts[:, 0], pts[:, 1]
    return yi[0] + (x - xi[0]) * (yi[1] - yi[0]) / (xi[1] - xi[0])


class Norm(object):
    def __init__(self, f):
        self.points = np.c_[f.x, f.y]
        self.frnm = self._integrate()
        self.f = f

    @property
    def x(self):
        return self.points[:, 0]

    @property
    def y(self):
        return self.points[:, 1]

    def __call__(self, t0, t1):
        x, f = self.x, self.f

        (i, k) = np.searchsorted(x, [t0, t1]) + np.array([1, -1])

        if t0 == x[i]:
            if t1 == x[k]:
                return self.frnm[k] - self.frnm[i]
        else:
            return np.trapz(np.abs(f([t0, x[i]])), [t0, x[i]]) + \
                self.frnm[k] - self.frnm[i] + \
                np.trapz(np.abs(f([x[k], t1])), [x[k], t1])

    def _integrate(self):
        x, y = self.x, self.y
        frnm = np.zeros(len(x) - 1)

        for i in np.arange(1, len(x)):
            frnm[i - 1] = np.trapz(np.abs(y[:i + 1]), x[:i + 1])

        return frnm

def bisection(frnm, E, a, b, tol=1e-6, nmax=1000):
    n = 1
    t0 = a

    while n <= nmax:
        c = (a + b) / 2
        
        if F(frnm, t0, c) - E == 0 or (b - a) / 2 < tol:
            return c
            
        n += 1
        
        if np.sign(F(frnm, t0, c) - E) == np.sign(F(frnm, t0, a) - E):
            a = c
        else:
            b = c
        
    raise ValueError("Method failed. Exceeded maximum number of iterations")


def F(frnm, a, b, k=3):
    return np.power(np.abs(b - a), 3) * frnm(a, b)

def cutab(eps, xi, frnm, k=3, C=1.0):
    E = C * eps
    t0 = xi[0]
    b = xi[-1]
    j = 1
    n = len(xi)

    while True:
        if j > len(xi):
            break

        if F(frnm, t0, b, k=3) > E:
            t0 = bisection(frnm, E, t0, b)
            j += 1
            pass
        elif F(frnm, t0, b, k=3) == E:
            t0 = b
            n = j
            break
        elif F(frnm, t0, b, k=3) < E:
            t0 = b
            n = j
            pass
    
    pass


# main()
if __name__ == "__main__":
    # dummy data
    xi = np.linspace(-5, 5, 1010)
    yi = -1 / (1 + 25 * np.power(xi, 2))
    knots = np.c_[xi, yi]

    p = Newton(points=knots)
    d4p_dx4 = differentiate(p, r=4)
    d4p_norm = Norm(d4p_dx4)
    pass
