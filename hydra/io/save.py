"""
Save HDR image files.
"""

from pathlib import Path

import numpy.typing as npt

from .hdr_format import HDRFormat as HDR
from .pfm_format import PFMFormat as PFM


def save(filename: str, img: npt.NDArray) -> None:
    ext = Path(filename).suffix
    if ext.lower() == ".hdr":
        HDR.save(filename, img)
    elif ext.lower() == ".pfm":
        PFM.save(filename, img)
    else:
        raise Exception("Unsupported HDR format")
