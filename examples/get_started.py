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
    RH02 = hydra.tonemap.gamma(RH02, 1.0 / 2.2)
    DM03 = hydra.tonemap.drago03(img, Ld_max=100, p=0.85)
    DM03 = hydra.tonemap.gamma(DM03, 1.0 / 2.2)
    FD02 = hydra.tonemap.fattal02(img)
    FD02 = hydra.tonemap.gamma(FD02, 1.0 / 2.2)

    # Show original HDR
    plt.subplot(1, 4, 1)
    plt.axis('off')
    plt.title('Original')
    plt.imshow(img, interpolation='nearest')

    # Show Reinhard 02
    plt.subplot(1, 4, 2)
    plt.axis('off')
    plt.title('Reinhard 02')
    plt.imshow(RH02, interpolation='nearest')

    # Show Drago 03
    plt.subplot(1, 4, 3)
    plt.axis('off')
    plt.title('Drago 03')
    plt.imshow(DM03, interpolation='nearest')

    # Show Fattal 02
    plt.subplot(1, 4, 4)
    plt.axis('off')
    plt.title('Fattal 02')
    plt.imshow(FD02, interpolation='nearest')

    plt.show()

if __name__ == '__main__':
    main()
