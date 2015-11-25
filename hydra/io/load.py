"""
Load HDR image files.
"""

import os
from .hdr_format import HDRFormat as HDR
from .pfm_format import PFMFormat as PFM

def load(filename):
    _, ext = os.path.splitext(filename)
    if ext == '.hdr':
        return HDR.load(filename)
    elif ext == '.pfm':
        return PFM.load(filename)
    else:
        raise Exception('Unsupported HDR format')
