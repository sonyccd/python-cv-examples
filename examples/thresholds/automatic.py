#!/usr/bin/env python

import numpy as np
import math


# returns indexes
def peak_detect(histogram, lookahead=5, min_range=0, max_range=256):
    minum_index = []
    maxum_index = []
    if max_range == 256:
        max_range = len(histogram)
    for i in range(min_range, max_range):
        if lookahead < i < len(histogram) - lookahead:
            if histogram[i + 1:i + lookahead].max() < histogram[i] and histogram[i - lookahead:i - 1].max() < histogram[
                i]:
                if len(maxum_index) > 1:
                    if maxum_index[len(maxum_index) - 1] != i - 1:
                        maxum_index.append(i)
                else:
                    maxum_index.append(i)
            if histogram[i + 1:i + lookahead].min() > histogram[i] and histogram[i - lookahead:i - 1].min() > histogram[
                i]:
                if len(minum_index) > 1:
                    if minum_index[len(minum_index) - 1] != i - 1:
                        minum_index.append(i)
                else:
                    minum_index.append(i)
    return minum_index, maxum_index


def peakiness(img, dist=20):
    hist = np.histogram(img.ravel(), 256)[0]
    maxum_indexs = peak_detect(hist)[1]
    maxum = np.take(hist, maxum_indexs)
    print(maxum)
    min_max_index = np.argpartition(maxum, -4)[-2:]
    print(maxum_indexs, maxum[min_max_index])


def iterative(img):
    img_cp = np.copy(img)
    t = np.mean(img_cp)
    r1 = img_cp[img_cp > t]
    r2 = img_cp[img_cp < t]
    r1_mean_old = np.mean(r1)
    r2_mean_old = np.mean(r2)
    count = 0
    while True:
        count = count + 1
        t = 0.5 * (r1_mean_old + r2_mean_old)
        r1 = img[img > t]
        r2 = img[img < t]
        r1_mean_new = np.mean(r1)
        r2_mean_new = np.mean(r2)
        if math.ceil(r1_mean_old) == math.ceil(r1_mean_new) and math.ceil(r2_mean_old) == math.ceil(r2_mean_new):
            break
        elif count > 100:
            break
    return threshold(img_cp, math.ceil(t)), math.ceil(t)


def adaptive(img):
    img_cp = np.copy(img)
    i, j = img_cp.shape
    hi = math.ceil(i / 2)
    hj = math.ceil(j / 2)
    top_left = img_cp[0:hi, 0:hj]
    top_right = img_cp[0:hi, hj:j]
    bottom_left = img_cp[hi:i, 0:hj]
    bottom_right = img_cp[hi:i, hj:j]
    top_left, t = iterative(top_left)
    top_right, t = iterative(top_right)
    bottom_left, t = iterative(bottom_left)
    bottom_right, t = iterative(bottom_right)
    return img_cp


def dual(img):
    img_cp = np.copy(img)
    hist = np.histogram(img_cp.ravel(), 256)[0]
    min_index, max_index = peak_detect(hist)
    ret, t = iterative(img_cp)
    img_r1 = np.copy(img_cp)
    img_r2 = np.copy(img_cp)
    mask_r1 = img_r1 >= t
    mask_r2 = img_r1 < t
    img_r1[mask_r1] = 0
    img_r2[mask_r2] = 0
    r1_t = iterative(img_r1)[1]
    r2_t = iterative(img_r2)[1]

    mask_r1 = img_cp < r1_t
    mask_r2 = r1_t <= img_cp <= r2_t
    mask_r3 = img_cp > r2_t
    img_cp[mask_r1] = 0
    img_cp[mask_r2] = 1
    img_cp[mask_r3] = 2



    return img_cp


# find threshold of image using numpy array masking
def threshold(img, t):
    maska = img < t
    maskb = img >= t
    img[maska] = 1
    img[maskb] = 0
    return img