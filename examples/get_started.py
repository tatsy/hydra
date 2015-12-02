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

def on_key_press(event):
    plt.close('all')

def main():
    # Load HDR
    img = hydra.io.load(filename)

    # Tone mapping
    TR93 = hydra.tonemap.tumblin(img)
    TR93 = hydra.tonemap.gamma(TR93, 1.0 / 2.2)
    RH02 = hydra.tonemap.reinhard(img)
    RH02 = hydra.tonemap.gamma(RH02, 1.0 / 2.2)
    DM03 = hydra.tonemap.drago(img)
    DM03 = hydra.tonemap.gamma(DM03, 1.0 / 2.2)
    FD02 = hydra.tonemap.fattal(img)
    FD02 = hydra.tonemap.gamma(FD02, 1.0 / 2.2)
    LF06 = hydra.tonemap.lischinski(img)
    LF06 = hydra.tonemap.gamma(LF06, 1.0 / 2.2)

    # Show original HDR
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.set_title('Tumblin 93')
    ax.imshow(TR93, interpolation='nearest')
    fig.canvas.mpl_connect('key_press_event', on_key_press)

    # Show Reinhard 02
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.set_title('Reinhard 02')
    ax.imshow(RH02, interpolation='nearest')
    fig.canvas.mpl_connect('key_press_event', on_key_press)

    # Show Drago 03
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.set_title('Drago 03')
    ax.imshow(DM03, interpolation='nearest')
    fig.canvas.mpl_connect('key_press_event', on_key_press)

    # Show Fattal 02
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.set_title('Fattal 02')
    ax.imshow(FD02, interpolation='nearest')
    fig.canvas.mpl_connect('key_press_event', on_key_press)

    # Show Lischinski 06
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.set_title('Lischinski 06')
    ax.imshow(LF06, interpolation='nearest')
    fig.canvas.mpl_connect('key_press_event', on_key_press)

    plt.show()

if __name__ == '__main__':
    main()
