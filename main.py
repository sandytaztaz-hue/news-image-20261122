#!/usr/bin/env python3
"""news-image-20261122 entrypoint (revision R4, full-day edition).

Takes the broadsheet image shipped beside this file (entry.png, drawn by
render-r4.py from the 36 verified stories in STORIES-R3.md) and places an
exact copy in the harness output directory. Before copying, it checks the
shipped file really is the R4 render: PNG magic bytes plus the SHA-256
recorded below. After copying, it reads the copy back and compares digests,
so a short or corrupted write fails loudly instead of scoring as the entry.
Standard library only; no network. Honors MAKEFUN_OUTPUT_DIR, else /output.
"""
import hashlib
import os
import sys

ENTRY_NAME = "entry.png"
ENTRY_SHA256 = "41dd5ea1366dfe68767b4270698c62a2f99b04352d59055cb92dab0044f30954"


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY_NAME)
    with open(src, "rb") as f:
        data = f.read()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        print("shipped entry.png is not a PNG file", file=sys.stderr)
        return 1
    if _sha256(data) != ENTRY_SHA256:
        print("shipped entry.png is not the R4 render (sha256 mismatch)",
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    # The harness runs this program twice and both runs must write the same
    # bytes, so there is no timestamp, no randomness and no network here.
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, ENTRY_NAME)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        copied = f.read()
    if _sha256(copied) != ENTRY_SHA256:
        print("copied entry.png failed its re-read check", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(copied)} bytes, sha256 {ENTRY_SHA256})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
