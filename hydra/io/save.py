# -*- coding: utf-8 -*-

import struct

from .hdr_pixel import HDRPixel

def strwrite(fp, str):
    fp.write(bytearray(str, 'ascii'))

def hdr_save(filename, hdr):
    with open(filename, 'wb') as fp:
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
                line[j] = HDRPixel(r, g, b)

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
