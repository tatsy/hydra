"""
Load .hdr format.
"""

import re
import math
import numpy as np
from itertools import product

HDR_NONE = 0
HDR_RLE_RGBE_32 = 1

def hdr_load(filename):
    img = None
    with open(filename, 'rb') as fp:
        bufsize = 4096
        filetype = HDR_NONE
        isvalid = False
        exposure = 1.0

        while True:
            buf = fp.readline(bufsize).decode()
            if buf[0] == '#':
                if buf == '#?RADIANCE\n':
                    isvalid = True
            else:
                p = re.compile('FORMAT=(.*)')
                m = p.match(buf)
                if m is not None:
                    if m.group(1) == '32-bit_rle_rgbe':
                        filetype = HDR_RLE_RGBE_32

                p = re.compile('EXPOSURE=(.*)')
                m = p.match(buf)
                if m is not None:
                    exposure = float(m.group(1))

            if buf[0] == '\n':
                break

        if not isvalid:
            raise Exception('Invalid HDR file format')

        width = 0
        height = 0
        buf = fp.readline(bufsize).decode()
        p = re.compile('([\-\+]Y) ([0-9]+) ([\-\+]X) ([0-9]+)')
        m = p.match(buf)
        if m is not None and m.group(1) == '-Y' and m.group(3) == '+X':
            width = int(m.group(4))
            height = int(m.group(2))
        else:
            raise Exception('Invalid HDR format')

        tmp_data = [0] * width * height * 4
        nowy = 0
        while True:
            now = -1
            now2 = -1
            try:
                now = ord(fp.read(1))
                now2 = ord(fp.read(1))
            except Exception as e:
                break

            if now != 0x02 or now2 != 0x02:
                break

            A = ord(fp.read(1))
            B = ord(fp.read(1))
            width = (A << 8) | B

            nowx = 0
            nowvalue = 0
            while True:
                if nowx >= width:
                    nowvalue += 1
                    nowx = 0
                    if nowvalue == 4:
                        break

                info = ord(fp.read(1))
                if info <= 128:
                    for i in range(info):
                        data = ord(fp.read(1))
                        tmp_data[(nowy * width + nowx) * 4 + nowvalue] = data
                        nowx += 1
                else:
                    num = info - 128
                    data = ord(fp.read(1))
                    for i in range(num):
                        tmp_data[(nowy * width + nowx) * 4 + nowvalue] = data
                        nowx += 1

            nowy += 1

        tmp = np.array(tmp_data).reshape((height, width, 4))
        expo = np.power(2.0, tmp[:,:,3] - 128.0) / 256.0
        img = np.multiply(tmp[:,:,0:3], expo[:,:,np.newaxis])

    if img is None:
        raise Exception('Invalid HDR format')

    return img
