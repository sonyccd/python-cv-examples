#!/usr/bin/env python


import math

import numpy as np
import scipy.signal
import matplotlib.pyplot as plt


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
    angle = np.arctan(convolv_y / convolv_x)
    return filterd, angle


def scharr(image):
    temp = np.copy(image)
    scharr_mask = np.array([[-3 - 3j, 0 - 10j, +3 - 3j],
                            [-10 + 0j, 0 + 0j, +10 + 0j],
                            [-3 + 3j, 0 + 10j, +3 + 3j]])  # Gx + j*Gy
    return scipy.signal.convolve2d(temp, scharr_mask, boundary='symm', mode='same')


def log(image, size=3, sigma=1):
    temp = np.copy(image)
    mask = log_mask(size, sigma)
    return scipy.signal.convolve2d(temp, mask, mode='same', boundary='wrap')


def log_mask(size=3, sigma=1):
    mask = np.zeros((size, size))
    shift = (size - 1) / 2
    for x, row in enumerate(mask):
        for y, elm in enumerate(row):
            mask[x][y] = log_eq(x-shift, y-shift, sigma)
    print(mask)
    plt.matshow(mask, cmap='Spectral', interpolation='spline16')
    plt.figure(2)
    return mask


def log_eq(x, y, sigma=1):
    a = (1 / (math.pi * math.pow(sigma, 4)))
    b = (((math.pow(x, 2) + math.pow(y, 2)) / (2 * math.pow(sigma, 2))) - 1)
    c = (math.pow(math.e, -((math.pow(x, 2) + math.pow(y, 2)) / (2 * math.pow(sigma, 2)))))
    print(x, y, sigma)
    return a * b * c


def pst(image, lpf=0.5, phase_strength=0.5, warp_strength=0.5, thresh_min=-0.5, thresh_max=0.5, morph_flag=False):
    import numpy
    from numpy.fft import fft2, ifft2, fftshift

    def cart2pol(x, y):
        return numpy.arctan2(y, x), numpy.hypot(x, y)

    image = image.astype(numpy.float64)

    L = 0.5

    x = numpy.linspace(-L, L, image.shape[1])
    y = numpy.linspace(-L, L, image.shape[0])

    X, Y = numpy.meshgrid(x, y)

    THETA, RHO = cart2pol(X, Y)

    X_step = x[1] - x[0]
    Y_step = y[1] - y[0]

    fx = numpy.linspace(-L / X_step, L / X_step, len(x))
    fy = numpy.linspace(-L / Y_step, L / Y_step, len(y))

    fx_step = fx[1] - fx[0]
    fy_step = fy[1] - fy[0]

    FX, FY = numpy.meshgrid(fx_step, fy_step)

    FTHETA, FRHO = cart2pol(FX, FY)

    # lowpass

    sigma = (lpf ** 2) / numpy.log(2)

    image_f = fft2(image)
    image_f = image_f * fftshift(numpy.exp(-(RHO / numpy.sqrt(sigma)) ** 2))
    image_filtered = numpy.real(ifft2(image_f))

    # PST kernel construction

    rws = RHO * warp_strength
    pst_kernel = rws * numpy.arctan(rws) - 0.5 * numpy.log(1 + (rws ** 2))
    pst_kernel /= pst_kernel.max()
    pst_kernel *= phase_strength

    # application of the kernel, and phase calculation

    image_processed = ifft2(fft2(image_filtered) * fftshift(numpy.exp(-1j * pst_kernel)))

    result = numpy.angle(image_processed)

    if morph_flag == False:
        return result
    else:
        binary = numpy.zeros_like(image, dtype=bool)

        binary[result > thresh_max] = 1
        binary[result < thresh_min] = 1
        binary[image < image.max() / 20] = 0

        # the matlab version does post-processing (cleaning) here!

        return binary
