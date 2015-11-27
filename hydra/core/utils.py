"""
Utility functions and commonly-used constants in 'hydra'
"""

EPS = 1.0e-32
INF = 1.0e20

import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS

def clamp(x, range=(0.0, 1.0)):
    if range[0] > range[1]:
        raise Exception('Lower bound is larger than upper bound!!')
    return max(range[0], min(x, range[1]))

def lum(img):
    l = 0.2126 * img[:,:,0] + \
        0.7152 * img[:,:,1] + \
        0.0722 * img[:,:,2]
    return l

def getexptime(filename):
    im = Image.open(filename)
    try:
        exif = im._getexif()
    except AttributeError:
        return 1.0

    exif_table = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value

    expo_str = 'ExposureTime'
    expo_time = 1.0
    if expo_str in exif_table:
        expo_tubple = exif_table[expo_str]
        expo_time = expo_tuple[0] / expo_tuble[1]

    return expo_time

def log_mean(img):
    delta = 1.0e-6
    img_delta = np.log(img + delta)
    return np.exp(np.average(img_delta))

def max_quart(mat, percentile):
    M = mat.copy()
    if mat.ndim == 2:
        n, m = M.shape
        M = M.reshape(n * m)

    M = np.sort(M)
    return M[min(round(M.size * percentile), M.size - 1)]

def remove_specials(img):
    img[np.isinf(img)] = 0.0
    img[np.isnan(img)] = 0.0
    return img
