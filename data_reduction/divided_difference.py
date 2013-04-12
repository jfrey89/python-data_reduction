#!/usr/bin/env python -O

import numpy as np


class NewtonPoly(object):

    def __init__(self, x_data, y_data):
        self.knots = np.column_stack((x_data, y_data))
        self.dim = len(x_data) - 1
        self.coeff = self._coefficients(x_data, y_data)

    def eval(self, x):
        """
        Evaluates Newton's divided difference polynomial p at x.
        The coefficients vector {a} can be computed by the function
        'coefficients'.
        """

        n = self.dim
        a = self.coeff
        p = a[n]

        for k in range(1, n + 1):
            p = a[n - k] + (x - self._x[n - k]) * p

        return p

    def _coefficients(self):
        """
        Computes the divided difference coefficients.
        """

        m = len(self.knots)     # number of data points
        x_data = self.knots[:, 0]
        a = self.knots[:, 1]

        for k in range(1, m):
            a[k:m] = (a[k:m] - a[k - 1]) / (x_data[k:m] - x_data[k - 1])

        return a
