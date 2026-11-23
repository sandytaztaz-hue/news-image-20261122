#!/usr/bin/env python3
"""Entry program for news-image-20261122 (R6).

Copies the shipped broadsheet image (entry.png) to the output directory
byte-for-byte and verifies the copy's SHA-256 against the hash baked into
this program. Standard library only. The copy is verified after it lands,
so a truncated or corrupted write is caught before the program reports
success.

The output directory comes from the MAKEFUN_OUTPUT_DIR environment variable
and falls back to /output when that variable is absent. Any hash mismatch
exits non-zero.
"""

import hashlib
import os
import shutil
import sys

# SHA-256 of the shipped entry.png (render-r6.py output).
EXPECTED_SHA256 = "ac61f9de2b62a6431f9a5e8976beda6119037f4b4f72925b9e80a9e43e1cff87"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    digest = hashlib.sha256()
    with open(dst, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    if digest.hexdigest() != EXPECTED_SHA256:
        print("error: entry.png hash mismatch", file=sys.stderr)
        return 1
    print("wrote %s (sha256 %s)" % (dst, digest.hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
