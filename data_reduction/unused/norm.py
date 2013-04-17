#!/usr/bin/env python -O

import numpy as np


def make_table(x, y):
    """
    Constructs the divided difference table.
    """

    n = len(x)
    f = np.zeros((n, n + 1))
    f[:, 0] = x.copy()
    f[:, 1] = y.copy()

    for k in xrange(1, n):
        for i in xrange(0, n - k):
            f[i, k + 1] = (f[i + 1, k] - f[i, k]) / (x[i + k] - x[i])

    return f


def clean_table(table, order=4):
    """
    Cleans up the divided difference table. This is done by extracting the
    desired coefficient array and reindexing it so that it's ready for
    linear extrapolation.
    """

    f = table[:, order + 1]
    n = len(f)
    tmp = np.zeros(n)

    if order % 2 == 0:
        pad = order / 2
        tmp[pad:(n - pad)] = f[:n - order]
        clean_f = tmp.copy()
    else:
        print "I can't deal with odd yet"

    return clean_f


def linear_extrap(x, f):
    """
    Extrapolates a clean divided difference array to the boundary nodes.
    Extrapolation is linear.
    """

    # Assign the linear extrapolation
    f[1] = f[2] + (x[1] - x[3]) * (f[3] - f[2]) / (x[3] - x[2])
    f[0] = f[1] + (x[0] - x[2]) * (f[2] - f[1]) / (x[2] - x[1])
    f[-2] = f[-3] + (x[-2] - x[-4]) * (f[-4] - f[-2]) / (x[-4] - x[-3])
    f[-1] = f[-2] + (x[-1] - x[-3]) * (f[-3] - f[-1]) / (x[-3] - x[-2])

    return f


if __name__ == "__main__":

    x = np.linspace(-4, 4, 10)
    y = np.sin(x)

    f = make_table(x, y)
    f = clean_table(f, 4)
    f = linear_extrap(x, f)
    f = 4 * 3 * 2 * f
