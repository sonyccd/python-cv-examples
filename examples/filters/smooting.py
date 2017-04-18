#!/usr/bin/env python

import math
import numpy as np


def gaussian_mask(size, sigma=1):
    mask = np.zeros((size, size))
    for x, row in enumerate(mask):
        for y, elm in enumerate(row):
            mask[x][y] = gaussian(x, y, sigma)
    print(mask)


def gaussian(x, y, sigma):
    return (1 / (math.sqrt(2 * math.pi * math.pow(sigma, 2)))) * math.pow(math.e, -(
        (math.pow(x, 2) + math.pow(y, 2)) / (2 * math.pow(sigma, 2))))
