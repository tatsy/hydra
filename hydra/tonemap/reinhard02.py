import math
from itertools import product

import numpy as np
import hydra.core

def calc_white_point(L):
    Lmax = hydra.core.max_quart(L, 0.99)
    Lmin = hydra.core.max_quart(L, 0.01)

    log2Max = np.log2(Lmax + 1.0e-9)
    log2Min = np.log2(Lmin + 1.0e-9)

    return 1.5 * (2 ** (log2Max - log2Min - 5.0))

def reinhard02(img, alph=0.18):
    L = hydra.core.lum(img)
    Lwa = hydra.core.log_mean(L)

    Lscaled = (alph * L) / Lwa

    Lwhite = calc_white_point(L)
    Lwhite2 = Lwhite * Lwhite

    Ld = (Lscaled * (1.0 + Lscaled / Lwhite2) / (1.0 + Lscaled))

    ret = np.zeros(img.shape)
    for c in range(3):
        ret[:,:,c] = hydra.core.remove_specials(img[:,:,c] / L * Ld)

    ret = np.maximum(ret, 0.0)
    ret = np.minimum(ret, 1.0)

    return ret
