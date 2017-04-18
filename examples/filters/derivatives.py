#!/usr/bin/env python

import math

import numpy as np
import scipy.signal


def sobel(image):
    temp = np.copy(image)
    sobel_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, 1]])
    sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    convolv_x = scipy.signal.convolve2d(temp, sobel_x)
    convolv_y = scipy.signal.convolve2d(temp, sobel_y)
    filterd = np.sqrt(convolv_x ** 2 + convolv_y ** 2)
    return filterd
