import numpy as np
from polynomial import NewtonPolynomial
from scipy.interpolate import interp1d


class ApproxDeriv(object):

    def __init__(self, **args):

        if 'points' in args:
            self.points = np.array(args['points'])
            self.xi = self.x
        else:
            self.points = np.array([[0, 0]])
            self.xi = np.array([1.])

    @property
    def x(self):
        return self.points[:, 0]

    @property
    def y(self):
        return self.points[:, 1]

    def __call__(self, x):
        f = interp1d(self.x, self.y)
        return f(x)


def compute_deriv(pN, k=4):
    if not isinstance(pN, NewtonPolynomial):
        raise ValueError('Input must be Newton polynomial')

    #divdiff = pN.divdiffcol(k+1)


if __name__ == "__main__":
    pass
