#!/usr/bin/env python

from __future__ import division
import numpy as np


def bisection(f, a, b, tol=10e-8, nmax=100):
    """
    INPUT: Function f, endpoint values a, b, tolerance tol,
    maximum iterations nmax.
    CONDITIONS: a < b, either f(a) < 0 and f(b) > 0 or f(a) > 0 and f(b) < 0
    OUTPUT: value which differs from a root of f(x) = 0 by less than tol
    """

    n = 1

    while n <= nmax:
        c = (a + b) / 2
        func_val = f(c)

        if func_val == 0 or (b - a) / 2 < tol:
            return c

        n += 1

        if func_val > 0:
            b = c
        if func_val < 0:
            a = c

    return c
