"""
Simple luminance normalization.
"""

import numpy.typing as npt

import hydra.core


def normalize(img: npt.NDArray) -> npt.NDArray:
    L = hydra.core.lum(img)
    maxval = hydra.core.max_quart(L, 0.999)
    return img / maxval
