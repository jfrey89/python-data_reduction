#!/usr/bin/env python

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as sl


class Monomial(object):
    base = 'monomial'

    def __init__(self, **args):
        if 'points' in args:
            self.points = np.array(args['points'])
            self.xi = self.x
            self.coeff = self.point_2_coeff()
            self.degree = len(self.coeff) - 1
        elif 'coeff' in args:
            self.coeff = np.array(args['coeff'])
            self.degree = len(self.coeff) - 1
            self.points = self.coeff_2_point()
        else:
            self.points = np.array([[0, 0]])
            self.xi = np.array([1.])
            self.coeff = self.point_2_coeff()
            self.degree = 0

    def point_2_coeff(self):
        return sl.solve(np.vander(self.x), self.y)

    def coeff_2_point(self):
        return np.array([[x, self(x)] for x
                         in np.linspace(0, 1, len(self.coeff))])

    @property
    def x(self):
        return self.points[:, 0]

    @property
    def y(self):
        return self.points[:, 1]

    margin = .05
    plotres = 500

    def plot(self, ab=None, plotinterp=True):
        if ab is None:  # guess a and b
            x = self.x
            a, b = x.min(), x.max()
            h = b - a
            a -= self.margin * h
            b += self.margin * h
        else:
            a, b = ab

        n = self.plotres
        x = np.linspace(a, b, n)
        y = np.vectorize(self.__call__)(x)
        plt.plot(x, y)

        if plotinterp:
            plt.plot(self.x, self.y, 'ro')

    def __call__(self, x):
        return np.polyval(self.coeff, x)

    def __repr__(self):
        txt = 'Polynomial of degree {degree} \n with coefficients {coeff} \n \
                in {base} basis.'
        return txt.format(coeff=self.coeff, degree=self.degree,
                          base=self.base)

    def companion(self):
        degree = self.degree
        companion = np.eye(degree, k=-1)
        companion[0, :] -= self.coeff[1:] / self.coeff[0]
        return companion

    def zeros(self):
        companion = self.companion()
        return np.linalg.eigvals(companion)

    def __add__(self, other):
        if not isinstance(other, Monomial):
            raise ValueError('Operands must be polynomials')

        if len(self.coeff) < len(other.coeff):
            newcoeff = other.coeff.copy()
            newcoeff[len(other.coeff) - len(self.coeff):] += self.coeff
        else:
            newcoeff = self.coeff.copy()
            newcoeff[len(self.coeff) - len(other.coeff):] += other.coeff

        return Monomial(coeff=newcoeff)


class Newton(Monomial):
    base = 'Newton'

    def __init__(self, **args):
        if 'coeff' in args:
            try:
                self.xi = np.array(args['xi'])
            except KeyError:
                raise ValueError('Coefficients need to be given together \
                                 with abscissae values xi')
        super(Newton, self).__init__(**args)

    def point_2_coeff(self):
        return np.array(list(self.newtcoeff()))

    def newtcoeff(self):
        xi = self.xi
        row = self.y
        yield row[0]

        for level in xrange(1, len(xi)):
            row = (row[1:] - row[:-1]) / (xi[level:] - xi[:-level])

            if np.allclose(row, 0):
                self.degree = level - 1
                break

            yield row[0]

    def divdiff(self, n_column):
        xi = self.xi
        row = self.y

        if n_column > len(xi):
            raise ValueError('depth out of bounds')

        for level in xrange(1, len(xi)):
            row = (row[1:] - row[:-1]) / (xi[level:] - xi[:-level])

            if level == n_column:
                return row

        return 0

    def __call__(self, x):
        # first compute the sequence 1, (x-x_1), (x-x_1)(x-x_2), ...
        nps = np.hstack([1., np.cumprod(x - self.xi[:self.degree])])
        return np.dot(self.coeff, nps)

    def companion(self):
        degree = self.degree
        companion = np.eye(degree, k=-1)
        diagonal = np.identity(degree, dtype=bool)
        companion[diagonal] = self.x[:degree]
        companion[:, -1] -= self.coeff[:degree] / self.coeff[degree]
        return companion
