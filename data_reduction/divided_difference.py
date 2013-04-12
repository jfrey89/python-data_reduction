#!/usr/bin/env python -O


class NewtonPolynomial(object):

    def __init__(self, x_data, y_data):
        self.x = x_data
        self.y = y_data

    def evaluate(self, x):
        """
        Evaluates Newton's divided difference polynomial p at x.
        The coefficients vector {a} can be computed by the function
        'coefficients'.
        """

        n = len(self.x) - 1     # degree of Polynomial
        a = self.coefficients(self.x, self.y)
        p = a[n]

        for k in range(1, n + 1):
            p = a[n - k] + (x - self.x[n - k]) * p

        return p

    def coefficients(self):
        """
        Computes the divided difference coefficients.
        """

        m = len(self.x)     # number of data points
        a = self.y.copy()

        for k in range(1, m):
            a[k:m] = (a[k:m] - a[k - 1]) / (self.x[k:m] - self.x[k - 1])

        return a
