#!/usr/bin/env python3
"""Copy the shipped entry.png to the output directory, verifying SHA-256.

Standard library only. Reads the output directory from the
MAKEFUN_OUTPUT_DIR environment variable and falls back to /output when
that variable is absent. Exits non-zero if the copied file's SHA-256
does not match the hash baked in below.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "1737c9ff53710db99ec5888d4102e62be598b267ffbef3a6a82889e34eed6992"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    if digest != EXPECTED_SHA256:
        print("SHA-256 mismatch: got %s, expected %s" % (digest, EXPECTED_SHA256),
              file=sys.stderr)
        return 1
    print("wrote %s sha256 %s" % (dst, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
