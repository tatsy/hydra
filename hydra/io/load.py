"""
Load .hdr format.
"""

import os
from .hdr_format import HDRFormat as HDR

def load(filename):
    _, ext = os.path.splitext(filename)
    if ext == '.hdr':
        return HDR.load(filename)
    else:
        raise Exception('Unsupported HDR format')
