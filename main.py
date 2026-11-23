#!/usr/bin/env python3
"""news-image-20261122 (R7): ship the rendered broadsheet image.

Copies the entry.png bundled in this repo to the output directory
byte-for-byte, then verifies its SHA-256 against the hash baked in
below. Exits non-zero if the copy does not match.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "7c1bc1d84933e0189665dbc282dff92876878ed1d446cbabeae42533305a47fd"


def main():
    """Copy entry.png to the output dir and verify its SHA-256."""
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    if digest != EXPECTED_SHA256:
        print("hash mismatch: got %s, expected %s" % (digest, EXPECTED_SHA256),
              file=sys.stderr)
        return 1
    print("wrote %s sha256=%s" % (dst, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
