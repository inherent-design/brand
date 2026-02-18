#!/usr/bin/env python3
"""Generate a minimal PNG with accent cell and optional centered grid."""

import argparse
import math
import struct
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


def parse_cell_pos(s: str) -> tuple[int, int]:
    parts = s.lower().split("x")
    if len(parts) != 2:
        raise ValueError(f"expected CxR, got '{s}'")
    return int(parts[0]), int(parts[1])


def grid_layout(w: int, h: int, cell: int) -> tuple[int, int, int, int]:
    full_cols = w // cell
    h_margin = (w - full_cols * cell) // 2
    full_rows = h // cell
    v_margin = (h - full_rows * cell) // 2
    return full_cols, h_margin, full_rows, v_margin


def pack_2bit(pixels: list[int], row_bytes: int) -> bytes:
    row = bytearray(row_bytes)
    for i, idx in enumerate(pixels):
        byte_pos = i // 4
        shift = 6 - (i % 4) * 2
        row[byte_pos] |= (idx & 0x03) << shift
    return bytes(row)


def make_png_no_grid(
    w: int, h: int, main: tuple[int, int, int], accent: tuple[int, int, int],
    cell: int, ax: int, ay: int,
) -> bytes:
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 1, 3, 0, 0, 0)
    plte = bytes([*accent, *main])

    row_bytes = math.ceil(w / 8)

    accent_row = bytearray(row_bytes)
    for i in range(row_bytes):
        byte_val = 0
        for bit in range(8):
            x = i * 8 + bit
            if x >= w:
                break
            if not (ax <= x < ax + cell):
                byte_val |= 1 << (7 - bit)
        accent_row[i] = byte_val

    main_row = b"\xFF" * row_bytes

    parts = []
    for y in range(h):
        parts.append(b"\x00")
        parts.append(bytes(accent_row) if ay <= y < ay + cell else main_row)

    compressed = zlib.compress(b"".join(parts), 9)
    return (
        sig
        + chunk(b"IHDR", ihdr)
        + chunk(b"PLTE", plte)
        + chunk(b"IDAT", compressed)
        + chunk(b"IEND", b"")
    )


def make_png_grid(
    w: int, h: int, main: tuple[int, int, int], accent: tuple[int, int, int],
    cell: int, ax: int, ay: int, grid_rgb: tuple[int, int, int],
) -> bytes:
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 2, 3, 0, 0, 0)
    plte = bytes([*accent, *main, *grid_rgb])

    full_cols, h_margin, full_rows, v_margin = grid_layout(w, h, cell)
    row_bytes = math.ceil(w * 2 / 8)

    h_lines: set[int] = set()
    for r in range(full_rows + 1):
        y = v_margin + r * cell
        if 0 < y < h:
            h_lines.add(y - 1)
        if 0 <= y < h:
            h_lines.add(y)

    v_lines: set[int] = set()
    for c in range(full_cols + 1):
        x = h_margin + c * cell
        if 0 < x < w:
            v_lines.add(x - 1)
        if 0 <= x < w:
            v_lines.add(x)

    def build_row(in_accent_y: bool, on_hline: bool) -> bytes:
        pixels = [0] * w
        for x in range(w):
            if in_accent_y and ax <= x < ax + cell:
                pixels[x] = 0
            elif on_hline or x in v_lines:
                pixels[x] = 2
            else:
                pixels[x] = 1
        return pack_2bit(pixels, row_bytes)

    row_a = build_row(True, False)
    row_b = build_row(True, True)
    row_c = build_row(False, False)
    row_d = build_row(False, True)

    parts = []
    for y in range(h):
        parts.append(b"\x00")
        ia = ay <= y < ay + cell
        oh = y in h_lines
        if ia and not oh:
            parts.append(row_a)
        elif ia and oh:
            parts.append(row_b)
        elif oh:
            parts.append(row_d)
        else:
            parts.append(row_c)

    compressed = zlib.compress(b"".join(parts), 9)
    return (
        sig
        + chunk(b"IHDR", ihdr)
        + chunk(b"PLTE", plte)
        + chunk(b"IDAT", compressed)
        + chunk(b"IEND", b"")
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Generate a PNG with accent cell and optional grid.")
    p.add_argument("main", help="main/background hex color (e.g. ffffff)")
    p.add_argument("accent", help="accent cell hex color (e.g. 2563eb)")
    p.add_argument("dims", help="dimensions as WxH (e.g. 1200x630)")
    p.add_argument("output", help="output file path")
    p.add_argument("--accent-cell", default="0x0", help="accent cell as CxR (default: 0x0)")
    p.add_argument("--grid-color", default="aaaaaa", help="grid line color (default: aaaaaa)")
    p.add_argument("--render-grid", action="store_true", help="enable grid lines")
    p.add_argument("--cell", type=int, default=90, help="grid cell size in pixels (default: 90)")
    args = p.parse_args()

    main_rgb = parse_color(args.main)
    accent_rgb = parse_color(args.accent)
    w, h = parse_dims(args.dims)
    col, row = parse_cell_pos(args.accent_cell)

    full_cols, h_margin, full_rows, v_margin = grid_layout(w, h, args.cell)
    if col < 0 or col >= full_cols or row < 0 or row >= full_rows:
        p.error(f"accent cell {col}x{row} out of range for {full_cols}x{full_rows} grid")

    ax = h_margin + col * args.cell
    ay = v_margin + row * args.cell

    if args.render_grid:
        grid_rgb = parse_color(args.grid_color)
        data = make_png_grid(w, h, main_rgb, accent_rgb, args.cell, ax, ay, grid_rgb)
        gr, gg, gb = grid_rgb
        grid_info = f"grid=#{gr:02x}{gg:02x}{gb:02x} cell={args.cell}px"
    else:
        data = make_png_no_grid(w, h, main_rgb, accent_rgb, args.cell, ax, ay)
        grid_info = "no grid"

    with open(args.output, "wb") as f:
        f.write(data)

    mr, mg, mb = main_rgb
    ar, ag, ab = accent_rgb
    print(
        f"{args.output}: {w}x{h} main=#{mr:02x}{mg:02x}{mb:02x} "
        f"accent=#{ar:02x}{ag:02x}{ab:02x} accent-cell={col}x{row} "
        f"{grid_info} ({len(data)} bytes)"
    )


if __name__ == "__main__":
    main()
