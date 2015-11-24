"""
IO for .hdr format
"""

import re
import math
import numpy as np
from itertools import product

HDR_NONE = 0x00
HDR_RLE_RGBE_32 = 0x01

class HDRFormat(object):
    @staticmethod
    def load(filename):
        """
        Load .hdr format
        """
        img = None
        with open(filename, 'rb') as f:
            bufsize = 4096
            filetype = HDR_NONE
            valid = False
            exposure = 1.0

            # Read header section
            while True:
                buf = f.readline(bufsize).decode()
                if buf[0] == '#' and buf == '#?RADIANCE\n':
                    valid = True
                else:
                    p = re.compile('FORMAT=(.*)')
                    m = p.match(buf)
                    if m is not None and m.group(1) == '32-bit_rle_rgbe':
                        filetype = HDR_RLE_RGBE_32
                        continue

                    p = re.compile('EXPOSURE=(.*)')
                    m = p.match(buf)
                    if m is not None:
                        exposure = float(m.group(1))
                        continue

                if buf[0] == '\n':
                    # Header section ends
                    break

            if not valid:
                raise Exception('HDR header is invalid!!')

            # Read body section
            width = 0
            height = 0
            buf = f.readline(bufsize).decode()
            p = re.compile('([\-\+]Y) ([0-9]+) ([\-\+]X) ([0-9]+)')
            m = p.match(buf)
            if m is not None and m.group(1) == '-Y' and m.group(3) == '+X':
                width = int(m.group(4))
                height = int(m.group(2))
            else:
                raise Exception('HDR image size is invalid!!')

            tmpdata = np.zeros((width * height * 4))
            nowy = 0
            while True:
                now = -1
                now2 = -1
                try:
                    now = ord(f.read(1))
                    now2 = ord(f.read(1))
                except:
                    break

                if now != 0x02 or now2 != 0x02:
                    break

                A = ord(f.read(1))
                B = ord(f.read(1))
                width = (A << 8) | B

                nowx = 0
                nowv = 0
                while True:
                    if nowx >= width:
                        nowv += 1
                        nowx = 0
                        if nowv == 4:
                            break

                    info = ord(f.read(1))
                    if info <= 128:
                        data = f.read(info)
                        for i in range(info):
                            tmpdata[(nowy * width + nowx) * 4 + nowv] = data[i]
                            nowx += 1
                    else:
                        num = info - 128
                        data = ord(f.read(1))
                        for i in range(num):
                            tmpdata[(nowy * width + nowx) * 4 + nowv] = data
                            nowx += 1

                nowy += 1

            tmpdata = tmpdata.reshape((height, width, 4))
            expo = np.power(2.0, tmpdata[:,:,3] - 128.0) / 256.0
            img = np.multiply(tmpdata[:,:,0:3], expo[:,:,np.newaxis])

        if img is None:
            raise Exception('Failed to load file "{0}"'.format(filename))

        return img

    def strwrite(fp, str):
        fp.write(bytearray(str, 'ascii'))

    def save(filename):
        """
        Save .hdr format
        """
        with open(filename, 'wb') as f:
            # Write header
            ret = 0x0a
            strwrite(fp, '#?RADIANCE%c' % ret)
            strwrite(fp, '# Made with100%% pure HDR Shop%c' % ret)
            strwrite(fp, 'FORMAT=32-bit_rle_rgbe%c' % ret)
            strwrite(fp, 'EXPOSURE=1.0000000000000%c%c' % (ret, ret))

            # Write size
            [height, width, dim] = hdr.shape
            if dim != 3:
                raise Exception('HDR image must have 3 channels')

            strwrite(fp, '-Y %d +X %d%c' % (height, width, ret))

            for i in range(height):
                line = [None] * width
                for j in range(width):
                    r = hdr[i, j, 0]
                    g = hdr[i, j, 1]
                    b = hdr[i, j, 2]
                    line[j] = hydra.core.Pixel(r, g, b)

                fp.write(struct.pack('BBBB', 0x02, 0x02, (width >> 8) & 0xff, width & 0xff))

                buf = []
                for ch in range(4):
                    cursor = 0
                    while cursor < width:
                        cursor_move = min(127, width - cursor)
                        buf.append(cursor_move)
                        for j in range(cursor, cursor + cursor_move):
                            buf.append(line[j].get(ch))
                        cursor += cursor_move

                fp.write(struct.pack('B' * len(buf), *buf))
