#!/usr/bin/env python

import filters
import matplotlib.pyplot as plt
from skimage import data, io
import numpy as np

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

    plt.imshow(filters.gaussian(image, 7, 0.84089642), cmap='gray')
    xx, yy = np.mgrid[0:image.shape[0], 0:image.shape[1]]

    # create the figure
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(xx, yy, image, rstride=1, cstride=1, cmap=plt.cm.gray,
                    linewidth=0)
    plt.show()
