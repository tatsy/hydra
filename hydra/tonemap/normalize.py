"""
Simple luminance normalization.
"""

import hydra.core

def normalize(img):
    L = hydra.core.lum(img)
    maxval = hydra.core.max_quart(L, 0.999)
    return img / maxval
