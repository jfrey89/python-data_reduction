#!/usr/bin/env python

import numpy as np


def lu_nopiv(A, ptol=2.e-16):
    m, n = np.shape(A)

    for i in np.arange(0, n):
        pivot = A[i, i]

        if abs(pivot) < ptol:
            raise ValueError('Zero pivot encountered')
            break

        for k in np.arange(i + 1, n):
            A[k, i] = A[k, i] / pivot
            A[k, (i + 1):n] = A[k, (i + 1):n] - A[k, i] * A[i, (i + 1):n]

    L = np.eye(n) + np.tril(A, -1)
    U = np.triu(A)
    return L, U
