import numpy as np
from scipy import interpolate
from polynomial import NewtonPolynomial


def compute_deriv(pN, k=4):
    if not isinstance(pN, NewtonPolynomial):
        raise ValueError('Input must be Newton polynomial')

    divdiff = pN.divdiffcol(k)



if __name__ == "__main__":
    pass
