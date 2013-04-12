from nose.tools import *
from data_reduction.divided_difference import *
import numpy as np


def test_coefficients():
    x_data = np.linspace(0., 1., 10)
    y_data = np.sin(x_data)


