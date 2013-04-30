#!/usr/bin/env python

import numpy as np


class Norm(object):
    def __init__(self, f):
        self.points = np.c_[f.x, f.y]
        self.frnm = self.integrate_4_frnm()
        self.f = f

    @property
    def x(self):
        return self.points[:, 0]

    @property
    def y(self):
        return self.points[:, 1]

    def __call__(self, a, b):
        xi, f = self.x, self.f
        (j, k) = np.searchsorted(xi, [a, b])

        # check if they're both in the xi array
        if a == xi[j] and b == xi[k]:
            #print '(j, k) = (%d, %d)\n' % (j, k)
            return self.frnm[k - 1] - self.frnm[j]
        # check if we're sandwiched between the end point and another point
        elif b == xi[-1] and a > xi[j - 1]:
            return np.trapz(np.abs(f([a, xi[-1]])), [a, xi[-1]])
        elif a == xi[0] and b < xi[1]:
            return np.trapz(np.abs(f([xi[0], b])), [xi[0], b])
        else:
            j = j + 1
            k = k - 1
            return np.trapz(np.abs(f([a, xi[j]])), [a, xi[j]]) + \
                self.frnm[k] - self.frnm[j] + \
                np.trapz(np.abs(f([xi[k], b])), [xi[k], b])

    def integrate_4_frnm(self):
        x, y = self.x, self.y
        frnm = np.zeros(len(x) - 1)

        for i in np.arange(1, len(x)):
            frnm[i - 1] = np.trapz(np.abs(y[:i + 1]), x[:i + 1])

        return frnm
