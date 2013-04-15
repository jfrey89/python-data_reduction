#!/usr/bin/env python -O

import numpy as np


class NewtonPoly(object):

    def __init__(self, x_data, y_data):
        self.knots = np.column_stack((x_data, y_data))
        self.dim = len(x_data)
        self.coeff = self._coefficients()

    def eval(self, x):
        """
        Evaluates Newton's divided difference polynomial p at x.
        The coefficients vector {a} can be computed by the function
        'coefficients'.
        """

        n = self.dim
        x_data = self.knots[:, 0]
        a = self.coeff
        val = a[0]
        factor = 1.0

        for i in range(1, n):
            factor *= (x - x_data[i - 1])
            val += (a[i] * factor)

        return val

        #n = self.deg + 1
        #x_data = self.knots[:, 0]
        #a = self.coeff
        #p = a[n]

        #for k in range(1, n + 1):
            #p = a[n - k] + (x - x_data[n - k]) * p

        #return p

    def _coefficients(self):
        """
        Computes the divided difference coefficients.
        """

        n = self.dim    # number of data points
        a = self.knots[:, 1]
        x = self.knots[:, 0]

        for i in range(1, n):
            for j in range(n - 1, i - 1, -1):
                a[j] = (a[j] - a[j - 1]) / (x[j] - x[j - 1])

        return a

        #for k in range(1, m):
            #a[k:m] = (a[k:m] - a[k - 1]) / (x_data[k:m] - x_data[k - 1])

        #return a


if __name__ == "__main__":

    x = np.array([1, 4, 7])
    y = np.array([1.5709, 1.5727, 1.5751])
    p = NewtonPoly(x, y)

    print "computed coeff=", p.coeff

    t = 3.5
    print "value at x=", t, p.eval(t)
