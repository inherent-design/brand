#!/usr/bin/env python3
"""Generate a minimal two-color PNG with an accent square flush top-left."""

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


def make_png(
    w: int,
    h: int,
    main: tuple[int, int, int],
    accent: tuple[int, int, int],
    square: int,
) -> bytes:
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 1, 3, 0, 0, 0)
    plte = bytes([*accent, *main])

    row_bytes = math.ceil(w / 8)

    if square <= 0 or square > w or square > h:
        raise ValueError(f"square size {square} out of range for {w}x{h}")

    full_accent_bytes = square // 8
    leftover_bits = square % 8

    accent_row = bytearray(row_bytes)
    for i in range(row_bytes):
        if i < full_accent_bytes:
            accent_row[i] = 0x00
        elif i == full_accent_bytes and leftover_bits > 0:
            accent_row[i] = (0xFF >> leftover_bits)
        else:
            accent_row[i] = 0xFF

    main_row = b"\xFF" * row_bytes

    rows = []
    for y in range(h):
        rows.append(b"\x00")
        if y < square:
            rows.append(bytes(accent_row))
        else:
            rows.append(main_row)

    compressed = zlib.compress(b"".join(rows), 9)

    return (
        sig
        + chunk(b"IHDR", ihdr)
        + chunk(b"PLTE", plte)
        + chunk(b"IDAT", compressed)
        + chunk(b"IEND", b"")
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Generate a two-color PNG with accent square.")
    p.add_argument("main", help="main/background hex color (e.g. ffffff)")
    p.add_argument("accent", help="accent square hex color (e.g. 2563eb)")
    p.add_argument("dims", help="image dimensions as WxH (e.g. 1200x630)")
    p.add_argument("square", type=int, help="accent square size in pixels (e.g. 90)")
    p.add_argument("output", help="output file path")
    args = p.parse_args()

    main_rgb = parse_color(args.main)
    accent_rgb = parse_color(args.accent)
    w, h = parse_dims(args.dims)

    data = make_png(w, h, main_rgb, accent_rgb, args.square)
    with open(args.output, "wb") as f:
        f.write(data)

    mr, mg, mb = main_rgb
    ar, ag, ab = accent_rgb
    print(f"{args.output}: {w}x{h} main=#{mr:02x}{mg:02x}{mb:02x} accent=#{ar:02x}{ag:02x}{ab:02x} square={args.square}px ({len(data)} bytes)")


if __name__ == "__main__":
    main()
