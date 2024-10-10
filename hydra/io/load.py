"""
Load HDR image files.
"""

from pathlib import Path

import numpy.typing as npt

from .hdr_format import HDRFormat as HDR
from .pfm_format import PFMFormat as PFM


def load(filename: str) -> npt.NDArray:
    ext = Path(filename).suffix
    if ext.lower() == ".hdr":
        return HDR.load(filename)
    elif ext.lower() == ".pfm":
        return PFM.load(filename)
    else:
        raise Exception("Unsupported HDR format")
