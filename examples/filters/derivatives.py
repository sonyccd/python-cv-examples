#!/usr/bin/env python


import math

import numpy as np
import scipy.signal


def sobel(image):
    temp = np.copy(image)
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    sobel_y = np.array([[1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1]])
    convolv_x = scipy.signal.convolve2d(temp, sobel_x)
    convolv_y = scipy.signal.convolve2d(temp, sobel_y)
    filterd = np.hypot(convolv_x, convolv_y)
    filterd *= 255 / np.max(filterd)
    return filterd


def scharr(image):
    temp = np.copy(image)
    scharr_mask = np.array([[-3 - 3j, 0 - 10j, +3 - 3j],
                            [-10 + 0j, 0 + 0j, +10 + 0j],
                            [-3 + 3j, 0 + 10j, +3 + 3j]])  # Gx + j*Gy
    return scipy.signal.convolve2d(temp, scharr_mask, boundary='symm', mode='same')


def log(image, size=3, sigma=1):
    temp = np.copy(image)
    mask = log_mask(size, sigma)
    print(mask)
    return scipy.signal.convolve2d(temp, mask, mode='same', boundary='wrap')


def log_mask(size=3, sigma=1):
    mask = np.zeros((size, size))
    for x, row in enumerate(mask):
        for y, elm in enumerate(row):
            mask[x][y] = log_eq(x, y, sigma)
    return mask


def log_eq(x, y, sigma=1):
    return -(1 / math.pi * math.pow(sigma, 4)) * (
        1 - (math.pow(x, 2) + math.pow(y, 2)) / 2 * math.pow(sigma, 2)) * math.pow(math.e, -(
        (math.pow(x, 2) + math.pow(y, 2)) / (2 * math.pow(sigma, 2))))
