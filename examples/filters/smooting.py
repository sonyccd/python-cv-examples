#!/usr/bin/env python

import math
import numpy as np
import scipy.signal


def gaussian(image, size=3, sigma=1):
    temp = np.copy(image)
    mask = gaussian_mask(size, sigma)
    return scipy.signal.convolve2d(temp, mask, boundary='wrap')


def gaussian_mask(size, sigma=1):
    mask = np.zeros((size, size))
    for x, row in enumerate(mask):
        for y, elm in enumerate(row):
            mask[x][y] = gaussian_eq(x, y, sigma)
    return mask


def gaussian_eq(x, y, sigma):
    return (1 / (2 * math.pi * math.pow(sigma, 2))) * math.pow(math.e, -(
        (math.pow(x, 2) + math.pow(y, 2)) / (2 * math.pow(sigma, 2))))
