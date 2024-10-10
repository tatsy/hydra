"""
Example 2. Load and save
"""

import os
import time

import hydra as hdr

ROOT_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir)
IMAGE_PATH = os.path.join(ROOT_DIR, "data", "memorial.hdr")


def main():
    # Load HDR
    start = time.time()
    img = hdr.io.load(IMAGE_PATH)
    print("Load time: {:.6f} sec".format(time.time() - start))

    # Save HDR
    start = time.time()
    hdr.io.save("image.hdr", img)
    print("Save time: {:.6f} sec".format(time.time() - start))


if __name__ == "__main__":
    main()
