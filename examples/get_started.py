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
    # logs = hydra.tonemap.logarithmic(img)
    logs = hydra.tonemap.tumblin93(img)
    logs = hydra.tonemap.gamma(logs, 1.0 / 2.2)
    RH02 = hydra.tonemap.reinhard02(img, alph=0.18)
    RH02 = hydra.tonemap.gamma(RH02, 1.0 / 2.2)
    DM03 = hydra.tonemap.drago03(img, Ld_max=100, p=0.85)
    DM03 = hydra.tonemap.gamma(DM03, 1.0 / 2.2)
    FD02 = hydra.tonemap.fattal02(img)
    FD02 = hydra.tonemap.gamma(FD02, 1.0 / 2.2)
    LF06 = hydra.tonemap.lischinski06(img)
    LF06 = hydra.tonemap.gamma(LF06, 1.0 / 2.2)

    # Show original HDR
    plt.subplot(1, 5, 1)
    plt.axis('off')
    plt.title('Original')
    plt.imshow(logs, interpolation='nearest')

    # Show Reinhard 02
    plt.subplot(1, 5, 2)
    plt.axis('off')
    plt.title('Reinhard 02')
    plt.imshow(RH02, interpolation='nearest')

    # Show Drago 03
    plt.subplot(1, 5, 3)
    plt.axis('off')
    plt.title('Drago 03')
    plt.imshow(DM03, interpolation='nearest')

    # Show Fattal 02
    plt.subplot(1, 5, 4)
    plt.axis('off')
    plt.title('Fattal 02')
    plt.imshow(FD02, interpolation='nearest')

    # Show Lischinski 06
    plt.subplot(1, 5, 5)
    plt.axis('off')
    plt.title('Lischinski 06')
    plt.imshow(LF06, interpolation='nearest')

    plt.show()

if __name__ == '__main__':
    main()
