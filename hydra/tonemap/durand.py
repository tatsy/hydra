"""
Implementation of the paper,

Durand and Dorsey SIGGGRAPH 2002,
"Fast Bilateral Fitering for the display of high-dynamic range images"
"""

import numpy as np
import hydra.io
import hydra.filters

def bilateral_separation(img, sigma_s=0.02, sigma_r=0.4):
    r, c = img.shape

    sigma_s = max(r, c) * sigma_s

    img_log = np.log10(img + 1.0e-6)
    img_fil = hydra.filter.bilateral(img_log, sigma_s, sigma_r)

    base = 10.0 ** (img_fil) - 1.0e-6

    base[base <= 0.0] = 0.0

    base = base.reshape((r, c))
    detail = hydra.core.remove_specials(img / base)

    return base, detail

def durand(img, target_contrast=5.0):
    L = hydra.core.lum(img)
    tmp = np.zeros(img.shape)
    for c in range(3):
        tmp[:,:,c] = hydra.core.remove_specials(img[:,:,c] / L)

    Lbase, Ldetail = bilateral_separation(L)

    log_base = np.log10(Lbase)

    max_log_base = np.max(log_base)
    log_detail = np.log10(Ldetail)
    compression_factor = np.log(target_contrast) / (max_log_base - np.min(log_base))
    log_absolute = compression_factor * max_log_base

    log_compressed = log_base * compression_factor + log_detail - log_absolute

    output = np.power(10.0, log_compressed)

    ret = np.zeros(img.shape)
    for c in range(3):
        ret[:,:,c] = tmp[:,:,c] * output

    ret = np.maximum(ret, 0.0)
    ret = np.minimum(ret, 1.0)

    return ret
