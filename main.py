#!/usr/bin/env python3
"""news-image-20261122 R5 entry point.

Copies the shipped entry.png to the output directory byte-for-byte and
verifies its SHA-256 against the hash of the rendered R5 broadsheet.
Standard library only.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = (
    "c86d753de9b37ef34b447a6390591fbfef8b19080827176b236b8e680e4e3d63"
)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("shipped entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    if digest != EXPECTED_SHA256:
        print("SHA-256 mismatch: got %s, expected %s"
              % (digest, EXPECTED_SHA256), file=sys.stderr)
        return 1
    print("entry.png copied to %s (%d bytes, sha256 %s)" % (dst, size, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
