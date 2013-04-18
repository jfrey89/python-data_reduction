#!/usr/bin/env python

import numpy as np
from polynomial import Polynomial


class NewtonPolynomial(Polynomial):

    base = 'Newton'

    def __init__(self, **args):
        if 'coeff' in args:
            try:
                self.xi = np.array(args['xi'])
            except KeyError:
                raise ValueError('Coefficients need to be given together \
                                 with abscissae values xi')
        super(NewtonPolynomial, self).__init__(**args)

    def point_2_coeff(self):
        return np.array(list(self.divdiff()))

    def divdiff(self):
        xi = self.xi
        row = self.y
        yield row[0]

        for level in xrange(1, len(xi)):
            row = (row[1:] - row[:-1]) / (xi[level:] - xi[:-level])

            if np.allclose(row, 0):
                self.degree = level - 1
                break

            yield row[0]

    def divdiffcol(self, depth):
        xi = self.xi
        row = self.y

        if depth > len(xi):
            raise ValueError('depth out of bounds')

        for level in xrange(1, depth):
            row = (row[1:] - row[:-1]) / (xi[level:] - xi[:-level])

            if level == depth:
                break

            if np.allclose(row, 0):
                raise ValueError('derivative is identically zero')

        return row

    def __call__(self, x):
        # first compute the sequence 1, (x-x_1), (x-x_1)(x-x_2), ...
        nps = np.hstack([1., np.cumprod(x - self.xi[:self.degree])])
        return np.dot(self.coeff, nps)

    def newton_2_monomial(self):
        return Polynomial(points=self.points)

    def __add__(self, other):
        if not isinstance(other, NewtonPolynomial):
            raise ValueError('Operands must be Newton polynomials')
        pass

    def __changepoints__(self, other):
        pts = np.c_[self.xi, other(self.xi)]
        return NewtonPolynomial(points=pts).coeff
