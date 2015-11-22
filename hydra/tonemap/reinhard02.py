# -*- coding: utf-8 -*-

import math
from itertools import product

import numpy as np

def reinhard02(img, a=0.18):
    delta = 1.0e-8

    height, width, dims = img.shape

    lw_bar  = 0.0
    l_white = 0.0

    l = 0.2126 * img[:,:,0] + 0.7152 * img[:,:,1] + 0.0722 * img[:,:,2]
    lw_bar = np.sum(np.log(l + delta))
    l_white = np.max(l)

    lw_bar = math.exp(lw_bar / (width * height))
    l_white2 = l_white * l_white

    ret = img * (a / lw_bar)
    ret = np.multiply(ret, np.divide(1.0 + ret / l_white2, 1.0 + ret))

    ret = np.minimum(1.0, ret)
    return ret
