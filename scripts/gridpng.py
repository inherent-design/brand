#!/usr/bin/env python3
"""Generate brand PNGs with a single accent cell on a centered grid.

Grid and centering system
-------------------------
The canvas (WxH) is divided into a grid of equal square cells. The cell
count per axis is floor(dimension / cell_size). When the dimension is not
an exact multiple, the leftover pixels are split evenly as margins on
both sides, centering the grid on the canvas.

    full_cols = W // cell
    h_margin  = (W - full_cols * cell) // 2

Example: 1200x630 at cell=90 gives 13 columns (h_margin=15) and 7 rows
(v_margin=0). A 512x512 icon at cell=85 gives 6x6 (margin=1).

One cell is designated the accent cell by column/row index (0-based).
Its pixel origin is (h_margin + col * cell, v_margin + row * cell).

Brand usage: both inherent.design (blue #2563eb on white) and cfgate
(orange #f97316 on black) place their accent at cell 3x2 on a 6x6 grid.

Palette minimization
--------------------
Without grid lines, only two colors exist (accent + background), so the
image uses a 1-bit indexed palette (bit depth 1, color type 3). Each
scanline packs 8 pixels per byte. A 2048x2048 image stores 256 bytes
per row instead of 6144 for RGB.

With grid lines, three colors exist (accent + background + grid), so the
image uses a 2-bit indexed palette (bit depth 2, color type 3). Each
scanline packs 4 pixels per byte. The PLTE chunk is 9 bytes total.

Indexed color keeps the palette to the theoretical minimum: no unused
entries, no alpha channel, no wasted bit depth.

Compression
-----------
Row deduplication is the primary compression lever. A grid image has at
most 4 distinct row patterns (accent/non-accent crossed with grid-line/
non-grid-line). Non-grid images have exactly 2 (accent row, background
row). Identical rows compress to near-zero cost under zlib deflate
(level 9), since the PNG filter byte (0x00 = None) preserves byte-level
repetition that LZ77 collapses. A 2048x2048 icon compresses to ~2.4 KB.
"""

import argparse
import math
import struct
import zlib


def chunk(ctype: bytes, data: bytes) -> bytes:
    """Build a PNG chunk: length + type + data + CRC32."""
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
    """Compute centered grid geometry.

    Returns (full_cols, h_margin, full_rows, v_margin). The grid occupies
    full_cols * cell pixels horizontally, centered with h_margin on each
    side. Same vertically.
    """
    full_cols = w // cell
    h_margin = (w - full_cols * cell) // 2
    full_rows = h // cell
    v_margin = (h - full_rows * cell) // 2
    return full_cols, h_margin, full_rows, v_margin


def pack_2bit(pixels: list[int], row_bytes: int) -> bytes:
    """Pack a list of 2-bit palette indices into bytes (MSB first)."""
    row = bytearray(row_bytes)
    for i, idx in enumerate(pixels):
        byte_pos = i // 4
        shift = 6 - (i % 4) * 2
        row[byte_pos] |= (idx & 0x03) << shift
    return bytes(row)


# -- No-grid path: 1-bit indexed (2-color PLTE) ------------------------------

def make_png_no_grid(
    w: int, h: int, main: tuple[int, int, int], accent: tuple[int, int, int],
    cell: int, ax: int, ay: int,
) -> bytes:
    """Generate a 1-bit indexed PNG with two colors: accent (index 0) and
    background (index 1). Bit depth 1 packs 8 pixels per byte, giving
    maximum compression for images with only two distinct colors.
    """
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 1, 3, 0, 0, 0)  # 1-bit indexed
    plte = bytes([*accent, *main])  # 2 entries, 6 bytes

    row_bytes = math.ceil(w / 8)

    # Precompute the accent row: index 0 where accent cell is, index 1 elsewhere.
    # Index 1 = bit set, index 0 = bit clear (palette order).
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

    # Background row: all index 1 (all bits set).
    main_row = b"\xFF" * row_bytes

    # Build scanlines. Filter byte 0x00 (None) preserves raw bytes for
    # optimal zlib repetition detection across identical rows.
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


# -- Grid path: 2-bit indexed (3-color PLTE) ---------------------------------

def make_png_grid(
    w: int, h: int, main: tuple[int, int, int], accent: tuple[int, int, int],
    cell: int, ax: int, ay: int, grid_rgb: tuple[int, int, int],
) -> bytes:
    """Generate a 2-bit indexed PNG with three colors: accent (index 0),
    background (index 1), grid (index 2). Grid lines are 2px wide,
    straddling each cell boundary (1px on each side).
    """
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 2, 3, 0, 0, 0)  # 2-bit indexed
    plte = bytes([*accent, *main, *grid_rgb])  # 3 entries, 9 bytes

    full_cols, h_margin, full_rows, v_margin = grid_layout(w, h, cell)
    row_bytes = math.ceil(w * 2 / 8)

    # Grid lines at cell boundaries, 2px wide (y-1 and y for horizontal,
    # x-1 and x for vertical). Boundaries at margin + n * cell for
    # n in 0..full_rows (inclusive, so edges get lines too).
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

    # Only 4 distinct row patterns exist (accent-y/grid-y cross product).
    # Precompute all 4 and select per-scanline for zlib to collapse.
    def build_row(in_accent_y: bool, on_hline: bool) -> bytes:
        pixels = [0] * w
        for x in range(w):
            if in_accent_y and ax <= x < ax + cell:
                pixels[x] = 0  # accent always wins over grid
            elif on_hline or x in v_lines:
                pixels[x] = 2  # grid line
            else:
                pixels[x] = 1  # background
        return pack_2bit(pixels, row_bytes)

    row_a = build_row(True, False)   # accent row, no grid line
    row_b = build_row(True, True)    # accent row, on grid line
    row_c = build_row(False, False)  # background, no grid line
    row_d = build_row(False, True)   # background, on grid line

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
    p = argparse.ArgumentParser(
        description="Generate a PNG with accent cell and optional grid.",
        epilog=(
            "Examples:\n"
            "  # inherent.design icon (blue on white, 6x6 grid, cell 3x2)\n"
            "  %(prog)s ffffff 2563eb 512x512 icon.png --cell 85 --accent-cell 3x2\n"
            "\n"
            "  # cfgate og-card (orange on black, 90px grid, with grid lines)\n"
            "  %(prog)s 000000 f97316 1200x630 og.png --accent-cell 7x3 --render-grid\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
