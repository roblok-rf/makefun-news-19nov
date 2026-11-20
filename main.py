#!/usr/bin/env python3
"""make.fun bounty news-image-20261119 — entry program.

Deterministic, no network: copies the bundled front-page image
(entry.png, held in this repository) to /output/entry.png.
Running it twice writes the same bytes both times.

Usage: python3 main.py
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = "/output" if os.path.isdir("/output") else os.path.join(HERE, "output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    with open(dst, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print("wrote", dst, digest[:16])


if __name__ == "__main__":
    main()
