#!/usr/bin/env python


from __future__ import division
import numpy as np

class Norm(object):
    def __init__(self, f):
        self.points = np.c_[f.x, f.y]
        self.frm, = self.integrate()
        self.f = f
        
    @property
    def x(self):
        return self.points[:, 0]
        
    @property
    def y(self):
        return self.points[:, 1]
        
    def __call__(self, a, b)
    x, f = self.x, self.f
    
    (i, k) = np.searchsorted(x, [a, b]) + np.array([1, -1])
    
    if a == x[i] and b == x[k]:
        return self.frnm[k] - self.frnm[i]
    else:
        return np.trapz(np.abs(f([a, x[i]])), [a, x[i]]) + \
            self.frnm[k] - self.frnm[i] + \
            np.trapz(np.abs(f([x[k], b])), [x[k], b])
            
    def integrate(self):
        x, y = self.x, self.y
        frnm = np.zeros(len(x) - 1)
        
        for i in np.arange(1, len(x)):
            frnm[i - 1] = np.trapz(np.abs(y[:i + 1]), x[:i + 1])

        return frnm