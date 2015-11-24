"""
Example 1. Get started
"""

import sys
import hydra.io
import hydra.tonemap

try:
    import numpy as np
    import matplotlib.pyplot as plt
except:
    print('NumPy and MatplotLib is necessary to run examples!')
    sys.exit(1)

filename = '../data/memorial.hdr'

def main():
    # Load HDR
    img = hydra.io.load(filename)

    # Tone mapping
    RH02 = hydra.tonemap.reinhard02(img, a=0.18)
    DM03 = hydra.tonemap.drago03(img, Ld_max=1000, p=0.85)

    # Show original HDR
    plt.subplot(1, 3, 1)
    plt.axis('off')
    plt.title('Original')
    plt.imshow(img, interpolation='nearest')

    # Show Reinhard 02
    plt.subplot(1, 3, 2)
    plt.axis('off')
    plt.title('Reinhard 02')
    plt.imshow(RH02, interpolation='nearest')

    # Show Drago 03
    plt.subplot(1, 3, 3)
    plt.axis('off')
    plt.title('Drago 03')
    plt.imshow(DM03, interpolation='nearest')

    plt.show()

if __name__ == '__main__':
    main()
