"""
Implementation of the paper,
Drago et al. 2003
"""

import numpy as np
import numpy.typing as npt

from hydra.core import lum, log_mean, remove_specials


def drago(img: npt.NDArray, Ld_max: float = 100.0, p: float = 0.95) -> npt.NDArray:
    L = lum(img)
    Lwa = log_mean(L)
    Lwa = Lwa / ((1.0 + p - 0.85) ** 5.0)
    LMax = np.max(L)

    L_wa = L / Lwa
    LMax_wa = LMax / Lwa

    c1 = np.log(p) / np.log(0.5)
    c2 = (Ld_max / 100.0) / np.log10(1.0 + LMax_wa)
    Ld = c2 * np.log(1.0 + L_wa) / np.log(2.0 + 8.0 * ((L_wa / LMax_wa) ** c1))

    ret = np.zeros(img.shape)
    for c in range(3):
        ret[:, :, c] = remove_specials(img[:, :, c] * Ld / L)

    ret = np.maximum(ret, 0.0)
    ret = np.minimum(ret, 1.0)
    return ret
