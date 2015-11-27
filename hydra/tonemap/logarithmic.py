"""
Simple logarithmic tone mapping.
"""

import math
import numpy as np
import hydra.core

def logarithmic(img):
    L = hydra.core.lum(img)
    Lmax = np.max(L)

    Ld = np.log10(1.0 + L) / math.log10(1.0 + Lmax)

    ret = np.zeros(img.shape)
    for c in range(3):
        ret[:,:,c] = hydra.core.remove_specials(img[:,:,c] / L * Ld)

    ret = np.maximum(ret, 0.0)
    ret = np.minimum(ret, 1.0)
    return ret
