#!/usr/bin/env python

import numpy as np
from scipy import linalg
from data_reduction.Polynomial import Polynomial


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

    def __call__(self, x):
        # first compute the sequence 1, (x-x_1), (x-x_1)(x-x_2), ...
        nps = np.hstack([1., np.cumprod(x - self.xi[:self.degree])])
        return np.dot(self.coeff, nps)

    def newton_2_monomial(self):
        L, U = linalg.lu(np.transpose(np.fliplr(np.vander(self.x))))
