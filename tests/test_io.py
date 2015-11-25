"""
Testing HDR image input/output.
"""

try:
    import unittest2 as unittest
except:
    import unittest

import numpy as np
from itertools import product
from nose.tools import nottest

import hydra.io


filename = 'data/memorial.hdr'

class TestIO(unittest.TestCase):
    def test_load(self):
        img = hydra.io.load(filename)
        self.assertEqual(img.shape[0], 768)
        self.assertEqual(img.shape[1], 512)

class TestHDR(unittest.TestCase):
    @nottest
    def test_save_and_load(self):
        w = 256
        h = 256
        img = np.random.random((h, w, 3))
        hydra.io.save('image.hdr', img)
        tmp = hydra.io.load('image.hdr')
        self.assertEqual(img.shape[0], tmp.shape[0])
        self.assertEqual(img.shape[1], tmp.shape[1])
        for y, x in product(range(h), range(w)):
            for c in range(3):
                self.assertAlmostEqual(img[y,x,c], tmp[y,x,c])

class TestPFM(unittest.TestCase):
    def test_save_and_load(self):
        w = 256
        h = 256
        img = np.random.random((h, w, 3))
        hydra.io.save('image.pfm', img)
        tmp = hydra.io.load('image.pfm')
        self.assertEqual(img.shape[0], tmp.shape[0])
        self.assertEqual(img.shape[1], tmp.shape[1])
        for y, x in product(range(h), range(w)):
            for c in range(3):
                self.assertAlmostEqual(img[y,x,c], tmp[y,x,c])

if __name__ == '__main__':
    unittest.main()
