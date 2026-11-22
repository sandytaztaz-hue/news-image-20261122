#!/usr/bin/env python3
"""news-image-20261122 entrypoint: copy the shipped broadsheet image to
the output directory byte-for-byte, verifying its SHA-256 first.

Stdlib only. Honors MAKEFUN_OUTPUT_DIR (default /output). The image is
the entry itself: a 1024x1024 PNG front page for Sunday 22 November 2026,
drawn in code from 36 verified stories across 7 regions, with 13 original
flat-colour drawings, a dotted world map with numbered pins, and a DATE
CHECK box for the big stories that did not happen that day.
"""
import hashlib
import os
import sys

ENTRY_SHA256 = "85d217366c943cca44bc796223ae8ff99fbeb6d9bb3b84b5059b19db8067df76"
ENTRY_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(src, "rb") as f:
        data = f.read()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    if digest != ENTRY_SHA256:
        print(f"entry.png sha256 mismatch: got {digest}, want {ENTRY_SHA256}",
              file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, ENTRY_NAME)
    with open(dst, "wb") as f:
        f.write(data)
    os.chmod(dst, 0o644)
    print(f"wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
