#!/usr/bin/env python
import math
import matplotlib.pyplot as plt


def is_square(x):
    if x == 1:
        return True
    low = 0
    high = x // 2
    root = high
    while root * root != x:
        root = (low + high) // 2
        if low + 1 >= high:
            return False
        if root * root > x:
            high = root
        else:
            low = root
    return True


def smallest_factors_distance(n):
    result = []
    for i in range(1, n + 1):
        if n % i == 0:
            result.append(i)
    if math.fmod(len(result), 2) != 0:
        raise ArithmeticError('Must have even number of factors')
    if len(result) < 4:
        raise ArithmeticError('Can not find smallest factor distance of prime numbers ' + result[1])
    return result[int((len(result) / 2) - 1)], result[int(len(result) / 2)]


def plot_images(images, cmap='gray'):
    assert isinstance(images, list), 'Images must be in a list'
    if len(images) < 4:
        f, ax = plt.subplots(1, len(images))
        for index, img in enumerate(images):
            ax[index].imshow(img, cmap=cmap)
            ax[index].axis('off')
        return f, ax
    else:
        if is_square(len(images)):
            x = y = int(math.sqrt(len(images)))
        else:
            x, y = smallest_factors_distance(len(images))
        f, ax = plt.subplots(x, y)
        for index, img in enumerate(images):
            i = int(index / max(x, y))
            j = int(math.fmod(index, max(x, y)))
            ax[i, j].imshow(img, cmap=cmap)
            ax[i, j].axis('off')
        return f, ax
