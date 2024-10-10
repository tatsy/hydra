"""
Example 3. Generate HDR from LDR images.
"""

import os
import re

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import hydra.io
import hydra.gen
import hydra.tonemap

ROOT_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir)
STACK_DIR = os.path.join(ROOT_DIR, "data", "stack")
LIST_PATH = "memorial.hdr_image_list.txt"


def main():
    hdr = None
    with open(os.path.join(STACK_DIR, LIST_PATH), "r") as f:
        lines = [l.strip() for l in f if not l.startswith("#")]

        nimg = int(lines[0])
        imgs = []
        expotimes = [0.0] * nimg
        for i in range(nimg):
            items = re.split(" +", lines[i + 1])
            img = np.array(Image.open(os.path.join(STACK_DIR, items[0])), dtype="uint8")
            imgs.append(img)
            expotimes[i] = float(items[1])

        hdr = hydra.gen.devebec(imgs, expotimes)

    tm = hydra.tonemap.durand(hdr)
    tm = hydra.tonemap.gamma(tm, 1.0 / 2.2)

    fig, ax = plt.subplots()
    ax.imshow(tm)
    ax.set_title("Generated HDR")
    ax.axis("off")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
