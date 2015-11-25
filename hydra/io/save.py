"""
Save HDR image files.
"""

import os
from .hdr_format import HDRFormat as HDR
from .pfm_format import PFMFormat as PFM

def save(filename, img):
    _, ext = os.path.splitext(filename)
    if ext == '.hdr':
        HDR.save(filename, img)
    elif ext == '.pfm':
        PFM.save(filename, img)
    else:
        raise Exception('Unsupported HDR format')
