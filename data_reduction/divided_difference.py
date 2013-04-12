#!/usr/bin/env python -O


class NewtonPolynomial(object):

    def __init__(self, x_data, y_data):
        self.dimension = len(x_data) - 1
        self.coefficients = self._coefficients(x_data, y_data)

    def evaluate(self, x):
        """
        Evaluates Newton's divided difference polynomial p at x.
        The coefficients vector {a} can be computed by the function
        'coefficients'.
        """

        n = self.dimension
        a = self.coefficients
        p = a[n]

        for k in range(1, n + 1):
            p = a[n - k] + (x - self.x[n - k]) * p

        return p

    def _coefficients(self, x_data, y_data):
        """
        Computes the divided difference coefficients.
        """

        m = len(x_data)     # number of data points
        a = y_data.copy()

        for k in range(1, m):
            a[k:m] = (a[k:m] - a[k - 1]) / (x_data[k:m] - x_data[k - 1])

        return a
