"""
Utility functions and commonly-used constants in 'hydra'
"""

EPS = 1.0e-32
INF = 1.0e20

import numpy as np

def clamp(x, range=(0.0, 1.0)):
    if range[0] > range[1]:
        raise Exception('Lower bound is larger than upper bound!!')
    return max(range[0], min(x, range[1]))

def lum(img):
    l = 0.2126 * img[:,:,0] + \
        0.7152 * img[:,:,1] + \
        0.0722 * img[:,:,2]
    return l

def log_mean(img):
    delta = 1.0e-6
    img_delta = np.log(img + delta)
    return np.exp(np.average(img_delta))

def remove_specials(img):
    img[np.isinf(img)] = 0.0
    img[np.isnan(img)] = 0.0
    return img
