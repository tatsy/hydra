"""
Testing hydra.core module.
"""

try:
    import unittest2 as unittest
except:
    import unittest

import hydra.core
from .test_helper import *
from random import *

class TestCore(unittest.TestCase):
    def test_clamp(self):
        for t in range(REPEAT):
            r = random()
            a = hydra.core.clamp(r)
            self.assertLessEqual(0.0, r)
            self.assertLessEqual(r, 1.0)
            if 0.0 <= r and r <= 1.0:
                self.assertEqual(r, a)

    def test_clamp_range(self):
        for t in range(REPEAT):
            r = random()
            l = random()
            h = random()
            if l > h:
                l, h = h, l

            a = hydra.core.clamp(r, range=(l, h))
            self.assertLessEqual(l, a)
            self.assertLessEqual(a, h)
            if l <= r and r <= h:
                self.assertEqual(r, a)

    def test_clamp_raises(self):
        for t in range(REPEAT):
            r = random()
            l = random()
            h = random()
            if l <= h:
                l, h = h, l

            with self.assertRaises(Exception):
                hydra.core.clamp(r, range=(l, h))

    def test_pixel(self):
        p = hydra.core.Pixel(0.0, 0.0, 0.0)
        self.assertEqual(p.r, 0)
        self.assertEqual(p.g, 0)
        self.assertEqual(p.b, 0)
        self.assertEqual(p.e, 0)

        p = hydra.core.Pixel(1.0, 1.0, 1.0)
        self.assertEqual(p.r, 128)
        self.assertEqual(p.g, 128)
        self.assertEqual(p.b, 128)
        self.assertEqual(p.e, 129)

    def test_pixel_get(self):
        p = hydra.core.Pixel(0.0, 0.0, 0.0)
        self.assertEqual(p.get(0), 0)
        self.assertEqual(p.get(1), 0)
        self.assertEqual(p.get(2), 0)
        self.assertEqual(p.get(3), 0)
        with self.assertRaises(Exception):
            p[4]

        self.assertEqual(p[0], 0)
        self.assertEqual(p[1], 0)
        self.assertEqual(p[2], 0)
        self.assertEqual(p[3], 0)
        with self.assertRaises(Exception):
            p[4]

if __name__ == '__main__':
    unittest.main()
