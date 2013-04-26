#!/usr/bin/env python


import numpy as np
import scipy.misc as sc
from scipy.interpolate import interp1d
from polynomial import Newton


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


class BigF(object):
    def __init__(self, frnm, k=3):
        self.frnm = frnm
        self.k = k

    def __call__(self, frnm, a, b):
        return np.power(b - a, 3) * frnm(a, b)


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


def root_bisection(frnm, E, a, b, tol=1e-6, nmax=50):
    n = 1
    t0 = a
    F = BigF(frnm, k=3)

    while n <= nmax:
        c = (a + b) / 2
        Fc = F(t0, c)

        if Fc - E == 0 or (b - a) / 2 < tol:
            return c

        Fa = F(t0, a)
        n += 1

        if np.sign(Fc - E) == np.sign(Fa - E):
            a = c
        else:
            b = c

    raise ValueError("Method failed. Exceeded maximum number of iterations")


def cutab(eps, xi, frnm, k=3, C=1.0):
    first = True
    E = C * eps
    T = np.array(xi[0])
    b = xi[-1]
    j = 1
    F = BigF(frnm, k=3)

    while True:
        if j > len(xi) and not first:
            break

        if first:
            n = len(xi)

        if F(T[j], b) > E:
            t_next = root_bisection(frnm, E, T[j], b)
            T.append(t_next)
            j += 1
            continue
        elif F(T[j], b) == E:
            T.append(b)
            n = j
            return T, n
        elif F(T[j], b) < E:
            T.append(b)
            n = j
            break
        else:
            print "DEAD"
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
