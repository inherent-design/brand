#!/usr/bin/env python3
"""Generate a minimal solid-color PNG (indexed, 1-bit, single-entry palette)."""

import argparse
import math
import struct
import sys
import zlib


def chunk(ctype: bytes, data: bytes) -> bytes:
    c = ctype + data
    return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)


def parse_color(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    if len(s) != 6:
        raise ValueError(f"expected 6-digit hex color, got '{s}'")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def parse_dims(s: str) -> tuple[int, int]:
    parts = s.lower().split("x")
    if len(parts) != 2:
        raise ValueError(f"expected WxH, got '{s}'")
    return int(parts[0]), int(parts[1])


def make_png(w: int, h: int, r: int, g: int, b: int) -> bytes:
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 1, 3, 0, 0, 0)
    plte = bytes([r, g, b])
    row_bytes = math.ceil(w / 8)
    row = b"\x00" + b"\x00" * row_bytes
    compressed = zlib.compress(row * h, 9)
    return (
        sig
        + chunk(b"IHDR", ihdr)
        + chunk(b"PLTE", plte)
        + chunk(b"IDAT", compressed)
        + chunk(b"IEND", b"")
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Generate a solid-color PNG.")
    p.add_argument("color", help="hex color (e.g. f97316 or #ffffff)")
    p.add_argument("dims", help="dimensions as WxH (e.g. 1200x630)")
    p.add_argument("output", help="output file path")
    args = p.parse_args()

    r, g, b = parse_color(args.color)
    w, h = parse_dims(args.dims)

    data = make_png(w, h, r, g, b)
    with open(args.output, "wb") as f:
        f.write(data)
    print(f"{args.output}: {w}x{h} #{r:02x}{g:02x}{b:02x} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
