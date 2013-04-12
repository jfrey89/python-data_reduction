#!/usr/bin/env python -O


def evaluate(a, x_data, x):
    """
    p = evaluate(a, x_data, x)
    Evaluates Newton's divided difference polynomial p at x. The coefficients
    vector {a} can be computed by the function 'coefficients'.
    """

    n = len(x_data) - 1     # degree of polynomial
    p = a[n]

    for k in range(1, n + 1):
        p = a[n - k] + (x - x_data[n - k]) * p

    return p


def coefficients(x_data, y_data):
    """a = coefficients(x_data, y_data)
    Computes the divided difference coefficients.
    """

    m = len(x_data)     # number of data points
    a = y_data.copy()

    for k in range(1, m):
        a[k:m] = (a[k:m] - a[k - 1]) / (x_data[k:m] - x_data[k - 1])

    return a
