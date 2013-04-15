#!/usr/bin/env python -O

import numpy as np
import time


class NewtonPoly(object):

    def __init__(self, x_data, y_data):
        self.x = x_data
        self.y = y_data
        self.coeff = self.get_coeff()

    def eval_poly(self, x):
        """
        Evaluates Newton's divided difference polynomial p at x.
        The coefficients vector {a} can be computed by the function
        'coefficients'.
        """

        n = len(self.x) - 1     # degree of polynomial
        p = self.coeff[n]

        for k in xrange(1, n + 1):
            p = self.coeff[n - k] + (x - self.x[n - k]) * p

        return p

    def get_coeff(self):

        m = len(self.x) # number of data points
        a = self.y.copy()

        for k in xrange(1, m):
            a[k:m] = (a[k:m] - a[k - 1]) / (self.x[k:m] - self.x[k - 1])

        return a


if __name__ == "__main__":

    start_time = time.time()
    x = np.linspace(-20, 20, 1000)
    y = 1 / (1 + 25 * x * x)

    poly = NewtonPoly(x, y)

    print time.time() - start_time, "seconds"
