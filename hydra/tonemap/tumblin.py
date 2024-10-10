import math

import numpy as np
import numpy.typing as npt

import hydra.core


def calc_gamma(x: npt.NDArray) -> npt.NDArray:
    y = np.zeros(x.shape)
    y[x <= 100.0] = 1.855 + 0.4 * np.log10(x[x <= 100.0] + 2.3 * 1.0e-5)
    y[x > 100.0] = 2.655
    return y


def tumblin(
    img: npt.NDArray, Lda: float = 20.0, Ldmax: float = 100.0, Cmax: float = 100.0
) -> npt.NDArray:
    L = hydra.core.lum(img)
    tmp = np.log(L + 2.3 * 1.0e-5)
    Lwa = math.exp(np.average(tmp))

    gamma_w = calc_gamma(np.array([Lwa]))[0]
    gamma_d = calc_gamma(np.array([Lda]))[0]

    gamma_wd = gamma_w / (1.855 + 0.4 * math.log(Lda))
    mLwa = math.sqrt(Cmax) ** (gamma_wd - 1.0)
    Ld = Lda * mLwa * (np.power(L / Lwa, gamma_w / gamma_d))

    ret = np.zeros(img.shape)
    for c in range(3):
        ret[:, :, c] = hydra.core.remove_specials(img[:, :, c] / L * Ld)

    ret = np.clip(ret / Ldmax, 0.0, 1.0)
    return ret
