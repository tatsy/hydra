"""
Example 3. Generate HDR from LDR images.
"""

import os
import re
import scipy as sp
import scipy.misc

import matplotlib.pyplot as plt

import hydra.io
import hydra.gen
import hydra.tonemap

dirname = '../data/stack'
filename = 'memorial.hdr_image_list.txt'

def main():
    hdr = None
    with open(os.path.join(dirname, filename), 'r') as f:
        lines = [ l.strip() for l in f if not l.startswith('#') ]

        nimg = int(lines[0])
        imgs = [ None ] * nimg
        expotimes = [ 0.0 ] * nimg
        for i in range(nimg):
            items = re.split(' +', lines[i + 1])
            imgs[i] = sp.misc.imread(os.path.join(dirname, items[0]))
            expotimes[i] = float(items[1])

        hdr = hydra.gen.devebec(imgs, expotimes)

    tm = hydra.tonemap.durand(hdr)
    tm = hydra.tonemap.gamma(tm, 1.0 / 2.2)

    fig, ax = plt.subplots()
    ax.imshow(tm)
    ax.set_title('Generated HDR')
    ax.axis('off')
    plt.show()

if __name__ == '__main__':
    main()
