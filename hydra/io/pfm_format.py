"""
IO for .pfm format
"""

import struct
import numpy as np

class PFMFormat(object):
    @staticmethod
    def load(filename):
        img = None
        with open(filename, 'rb') as f:
            f.readline()
            w, h = f.readline().decode('ascii').strip().split(' ')
            w = int(w)
            h = int(h)
            f.readline()

            siz = h * w * 3
            img = np.array(struct.unpack('f' * siz, f.read(4 * siz)))
            img = img.reshape((h, w, 3))

        if img is None:
            raise Exception('Failed to load file "{0}"'.format(filename))

        return img

    @staticmethod
    def save(filename, img):
        h, w, dim = img.shape
        with open(filename, 'wb') as f:
            f.write(bytearray('PFM\n', 'ascii'))
            f.write(bytearray('{0:d} {1:d}\n\n'.format(w, h), 'ascii'))

            siz = h * w * 3
            tmp = img.reshape(siz)
            f.write(struct.pack('f' * siz, *tmp))
