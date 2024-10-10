"""
Testing hydra.core module.
"""

import pytest

import hydra.core


def test_pixel():
    p = hydra.core.Pixel(0.0, 0.0, 0.0)
    assert p.r == 0
    assert p.g == 0
    assert p.b == 0
    assert p.e == 0

    p = hydra.core.Pixel(1.0, 1.0, 1.0)
    assert p.r == 128
    assert p.g == 128
    assert p.b == 128
    assert p.e == 129


def test_pixel_get():
    p = hydra.core.Pixel(0.0, 0.0, 0.0)
    assert p.get(0) == 0
    assert p.get(1) == 0
    assert p.get(2) == 0
    assert p.get(3) == 0

    with pytest.raises(IndexError):
        p.get(4)


def test_pixel_getitem():
    p = hydra.core.Pixel(0.0, 0.0, 0.0)
    assert p[0] == 0
    assert p[1] == 0
    assert p[2] == 0
    assert p[3] == 0

    with pytest.raises(IndexError):
        p[4]
