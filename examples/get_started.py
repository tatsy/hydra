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
    tmp = hydra.tonemap.reinhard02(img, a=0.18)

    # Show original HDR
    plt.subplot(1, 2, 1)
    plt.axis('off')
    plt.title('Original')
    plt.imshow(img, interpolation='nearest')

    # Show tonemapped LDR
    plt.subplot(1, 2, 2)
    plt.axis('off')
    plt.title('Reinhard 02')
    plt.imshow(tmp, interpolation='nearest')

    plt.show()

if __name__ == '__main__':
    main()
