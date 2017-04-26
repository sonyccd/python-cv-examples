#!/usr/bin/env python

import matplotlib.pyplot as plt
from skimage import data, io
import numpy as np

from examples import thresholds

IMAGE_FILE = '../img/hw1.jpg'

if __name__ == '__main__':
    image = None
    if IMAGE_FILE == '':
        image = data.camera()
    else:
        try:
            image = io.imread(IMAGE_FILE)
        except IOError as e:
            print(e)
            print('Could not find or read ' + IMAGE_FILE)
            exit()
        except Exception as e:
            print(e)
            print('Unknown error reading file!')
            exit()
    thresh = thresholds.peakiness(image)
    plt.imshow(thresh, cmap='gray')
    plt.show()
