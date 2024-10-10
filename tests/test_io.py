"""
Testing HDR image input/output.
"""

import numpy as np
import pytest

import hydra.io

filename = "data/memorial.hdr"


def test_hdr_load():
    img = hydra.io.load(filename)
    assert img.shape[0] == 768
    assert img.shape[1] == 512


def test_hdr_save_and_load():
    w = 256
    h = 256
    img = np.random.random((h, w, 3))
    hydra.io.save("image.hdr", img)
    tmp = hydra.io.load("image.hdr")
    assert img.shape[0] == tmp.shape[0]
    assert img.shape[1] == tmp.shape[1]

    for y in range(h):
        for x in range(w):
            for c in range(3):
                assert np.abs(img[y, x, c] - tmp[y, x, c]) < 1.0e-2


def test_pfm_save_and_load():
    w = 256
    h = 256
    img = np.random.random((h, w, 3))
    hydra.io.save("image.pfm", img)
    tmp = hydra.io.load("image.pfm")
    assert img.shape[0] == tmp.shape[0]
    assert img.shape[1] == tmp.shape[1]
    for y in range(h):
        for x in range(w):
            for c in range(3):
                assert np.abs(img[y, x, c] - tmp[y, x, c]) < 1.0e-2
