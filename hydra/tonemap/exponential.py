"""
Exponential tone mapping operator.
"""

import numpy as np
import hydra.core

def exponential(img):
    L = hydra.core.lum(img)
    Lwa = hydra.core.log_mean(L)

    Ld = 1.0 - np.exp(- L / Lwa)

    ret = np.zeros(img.shape)
    for c in range(3):
        ret[:,:,c] = hydra.core.remove_specials(img[:,:,c] / L * Ld)

    ret = np.maximum(ret, 0.0)
    ret = np.minimum(ret, 1.0)
    return ret
