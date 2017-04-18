#!/usr/bin/env python

import filters
import matplotlib.pyplot as plt
from skimage import data, io

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

    plt.imshow(filters.log(image), cmap='gray')
    plt.show()
