import math
import numpy as np
from itertools import product

import hydra.core

def drago03(img, Ld_max = 100.0, p = 0.95):
    L = hydra.core.lum(img)
    Lw_max = np.max(L)
    denom1 = math.log10(1.0 + Lw_max)

    a = L / Lw_max
    b = math.log(p) / math.log(0.5)
    denom2 = np.log(2.0 + 8.0 * np.power(a, b))

    numer1 = Ld_max / 100.0
    numer2 = np.log(1.0 + L)
    ret = np.zeros(img.shape)
    Ld = (numer1 * numer2) / (denom1 * denom2)
    for c in range(3):
        ret[:,:,c] = img[:,:,c] * Ld / L

    ret = np.maximum(ret, 0.0)
    ret = np.minimum(ret, 1.0)
    return ret
