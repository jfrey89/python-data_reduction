#!/usr/bin/env python

from __future__ import division
import numpy as np


def bisect(f, a, b, tol=10e-8):
    """
    Implementation of the bisection algorithm.
    f real valued function
    a, b interval boundarird (float) with
        the property f(a) * f(b) <= 0
    tol tolerance (float)
    """
    if f(a) * f(b) > 0:
        raise ValueError("Incorrect initial interval [a, b]")

    for i in xrange(100):
        c = (a + b) / 2

        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c

        if np.abs(a - b) < tol:
            return (a + b) / 2

    raise Exception('No root found within the given tolerance {}'.format(tol))
