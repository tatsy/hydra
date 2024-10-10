"""
Example 1. Get started
"""

import sys

import numpy as np
import matplotlib.pyplot as plt

import hydra.io
import hydra.tonemap

filename = "../data/memorial.hdr"


def on_key_press(event):
    plt.close("all")


def main():
    # Load HDR
    img = hydra.io.load(filename)

    # Tumblin and Rushmeier 1993
    tm = hydra.tonemap.tumblin(img)
    tm = hydra.tonemap.gamma(tm, 1.0 / 2.2)
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.set_title("Tumblin 93")
    ax.imshow(tm, interpolation="nearest")
    fig.canvas.mpl_connect("key_press_event", on_key_press)
    fig.tight_layout()
    plt.show()

    # Show Reinhard 2002
    tm = hydra.tonemap.reinhard(img)
    tm = hydra.tonemap.gamma(tm, 1.0 / 2.2)
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.set_title("Reinhard 02")
    ax.imshow(tm, interpolation="nearest")
    fig.canvas.mpl_connect("key_press_event", on_key_press)
    fig.tight_layout()
    plt.show()

    # Durand and Dorsey 2002
    tm = hydra.tonemap.durand(img)
    tm = hydra.tonemap.gamma(tm, 1.0 / 2.2)
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.set_title("Dorsey 02")
    ax.imshow(tm, interpolation="nearest")
    fig.canvas.mpl_connect("key_press_event", on_key_press)
    fig.tight_layout()
    plt.show()

    # Show Drago 03
    tm = hydra.tonemap.drago(img)
    tm = hydra.tonemap.gamma(tm, 1.0 / 2.2)
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.set_title("Drago 03")
    ax.imshow(tm, interpolation="nearest")
    fig.canvas.mpl_connect("key_press_event", on_key_press)
    fig.tight_layout()
    plt.show()

    # Show Fattal 02
    tm = hydra.tonemap.fattal(img)
    tm = hydra.tonemap.gamma(tm, 1.0 / 2.2)
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.set_title("Fattal 02")
    ax.imshow(tm, interpolation="nearest")
    fig.canvas.mpl_connect("key_press_event", on_key_press)
    fig.tight_layout()
    plt.show()

    # Show Lischinski 06
    tm = hydra.tonemap.lischinski(img)
    tm = hydra.tonemap.gamma(tm, 1.0 / 2.2)
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.set_title("Lischinski 06")
    ax.imshow(tm, interpolation="nearest")
    fig.canvas.mpl_connect("key_press_event", on_key_press)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
