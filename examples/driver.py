#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, io
import thresholds
import utils
import filters

IMAGE_FILE = ''


if __name__ == '__main__':
    image = None
    if IMAGE_FILE == '':
        image = data.camera()
    else:
        try:
            image = io.imread(IMAGE_FILE)
        except IOError:
            print('Could not find or read ' + IMAGE_FILE)
            exit()
        else:
            print('Unknown error reading file!')
            exit()

    plt.imshow(filters.gaussian(image,7,2), cmap='gray')
    plt.show()
