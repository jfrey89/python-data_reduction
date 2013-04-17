#!/usr/bin/env python

import numpy as np

nsample = 6
xi = np.linspace(0, 5, nsample)
pts = np.c_[xi, xi ** 2]
row = pts[:, 1]

print '*' * 10
print 'Starting row!'
print '*' * 10
print row
print '\n\n'

n = 1
for level in xrange(1, len(xi)):
    print '*' * 10
    print 'Row %d' % n
    print '*' * 10
    row = (row[1:] - row[:-1]) / (xi[level:] - xi[:-level])
    print row
    print '\n\n'
    n += 1

    if np.allclose(row, 0):
        print "Row of zeros!"
        print "Ending!"
        break
