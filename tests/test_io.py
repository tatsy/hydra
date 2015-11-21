"""
Testing HDR image input/output.
"""

try:
    import unittest2 as unittest
except:
    import unittest

import hydra.io

filename = 'data/memorial.hdr'

class TestIO(unittest.TestCase):
    def test_load(self):
        img = hydra.io.load(filename)
        self.assertEqual(img.shape[0], 768)
        self.assertEqual(img.shape[1], 512)

if __name__ == '__main__':
    unittest.main()
