#!/usr/bin/env python

import numpy as np


class Polynomial(object):
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
        return np.linalg.solve(np.vander(self.x), self.y)

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
            np.plot(x, y)

        if plotinterp:
            np.plot(self.x, self.y, 'ro')

    def __call__(self, x):
        return np.polyval(self.coeff, x)

    def companion(self):
        degree = self.degree
        companion = np.eye(degree, k=-1)
        companion[0, :] -= self.coeff[1:] / self.coeff[0]
        return companion

    def zeros(self):
        companion = self.companion()
        return np.linalg.eigvals(companion)
