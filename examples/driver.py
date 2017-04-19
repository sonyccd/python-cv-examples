#!/usr/bin/env python

import filters
import matplotlib.pyplot as plt
from skimage import data, io
import numpy as np

IMAGE_FILE = '../img/cir.gif'

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

    sobel_image = filters.sobel(image)
    plt.imshow(sobel_image, cmap='gray')
    plt.show()
