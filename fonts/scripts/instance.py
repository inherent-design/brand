# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools>=4.61"]
# ///
#
# Generate static font instances from variable sources for Typst compatibility.
# Typst (as of 0.14.x) does not support variable fonts (issue #185).
#
# Usage:
#   uv run brand/fonts/scripts/instance.py
#
# Output:
#   brand/fonts/src/typst/ (static TTF instances, regular + bold per family)

import os
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

SCRIPT_DIR = Path(__file__).parent
SRC_DIR = SCRIPT_DIR.parent / "src"
OUT_DIR = SRC_DIR / "typst"

# Each entry: (source, output, axes, family_name, subfamily)
# family_name/subfamily override the name table so Typst resolves fonts correctly.
INSTANCES = [
    # Inter upright (axes: opsz 14-32, wght 100-900)
    ("inter-variable.ttf", "inter-regular.ttf", {"opsz": 14.0, "wght": 400.0}, "Inter", "Regular"),
    ("inter-variable.ttf", "inter-bold.ttf", {"opsz": 14.0, "wght": 700.0}, "Inter", "Bold"),
    ("inter-variable.ttf", "inter-black.ttf", {"opsz": 14.0, "wght": 900.0}, "Inter", "Black"),

    # Inter italic (axes: opsz 14-32, wght 100-900)
    ("inter-italic-variable.ttf", "inter-italic.ttf", {"opsz": 14.0, "wght": 400.0}, "Inter", "Italic"),
    ("inter-italic-variable.ttf", "inter-bold-italic.ttf", {"opsz": 14.0, "wght": 700.0}, "Inter", "Bold Italic"),

    # Commit Mono (axes: wght 200-700, ital 0-1)
    # Source has family "CommitMonoV143 ExtLt"; must override to "Commit Mono"
    ("commit-mono-variable.ttf", "commit-mono-regular.ttf", {"wght": 400.0, "ital": 0.0}, "Commit Mono", "Regular"),
    ("commit-mono-variable.ttf", "commit-mono-bold.ttf", {"wght": 700.0, "ital": 0.0}, "Commit Mono", "Bold"),

    # Cormorant Garamond upright (axes: wght 300-700)
    ("cormorant-garamond-variable.ttf", "cormorant-garamond-regular.ttf", {"wght": 400.0}, "Cormorant Garamond", "Regular"),
    ("cormorant-garamond-variable.ttf", "cormorant-garamond-bold.ttf", {"wght": 700.0}, "Cormorant Garamond", "Bold"),

    # Cormorant Garamond italic (axes: wght 300-700)
    ("cormorant-garamond-italic-variable.ttf", "cormorant-garamond-italic.ttf", {"wght": 400.0}, "Cormorant Garamond", "Italic"),
    ("cormorant-garamond-italic-variable.ttf", "cormorant-garamond-bold-italic.ttf", {"wght": 700.0}, "Cormorant Garamond", "Bold Italic"),

    # Noto Sans SC (axes: wght 100-900)
    ("noto-sans-sc-variable.ttf", "noto-sans-sc-regular.ttf", {"wght": 400.0}, "Noto Sans SC", "Regular"),
    ("noto-sans-sc-variable.ttf", "noto-sans-sc-bold.ttf", {"wght": 700.0}, "Noto Sans SC", "Bold"),

    # Noto Sans Devanagari (axes: wght 100-900, wdth 62.5-100)
    ("noto-sans-devanagari-variable.ttf", "noto-sans-devanagari-regular.ttf", {"wght": 400.0, "wdth": 100.0}, "Noto Sans Devanagari", "Regular"),
    ("noto-sans-devanagari-variable.ttf", "noto-sans-devanagari-bold.ttf", {"wght": 700.0, "wdth": 100.0}, "Noto Sans Devanagari", "Bold"),

    # Noto Sans Mono (axes: wght 100-900, wdth 62.5-100)
    ("noto-sans-mono-variable.ttf", "noto-sans-mono-regular.ttf", {"wght": 400.0, "wdth": 100.0}, "Noto Sans Mono", "Regular"),
    ("noto-sans-mono-variable.ttf", "noto-sans-mono-bold.ttf", {"wght": 700.0, "wdth": 100.0}, "Noto Sans Mono", "Bold"),
]


# OpenType name table IDs
NAME_FAMILY = 1        # Font Family name
NAME_SUBFAMILY = 2     # Font Subfamily name (Regular, Bold, Italic, Bold Italic)
NAME_FULL = 4          # Full font name
NAME_PS = 6            # PostScript name
NAME_PREF_FAMILY = 16  # Typographic Family name
NAME_PREF_SUB = 17     # Typographic Subfamily name


def fix_name_table(font, family, subfamily):
    """Set name table entries so Typst resolves the font correctly."""
    name_table = font["name"]

    ps_name = f"{family.replace(' ', '')}-{subfamily.replace(' ', '')}"
    full_name = f"{family} {subfamily}"

    for record in name_table.names:
        pid = record.platformID
        eid = record.platEncID
        lid = record.langID

        if record.nameID == NAME_FAMILY:
            name_table.setName(family, NAME_FAMILY, pid, eid, lid)
        elif record.nameID == NAME_SUBFAMILY:
            name_table.setName(subfamily, NAME_SUBFAMILY, pid, eid, lid)
        elif record.nameID == NAME_FULL:
            name_table.setName(full_name, NAME_FULL, pid, eid, lid)
        elif record.nameID == NAME_PS:
            name_table.setName(ps_name, NAME_PS, pid, eid, lid)
        elif record.nameID == NAME_PREF_FAMILY:
            name_table.setName(family, NAME_PREF_FAMILY, pid, eid, lid)
        elif record.nameID == NAME_PREF_SUB:
            name_table.setName(subfamily, NAME_PREF_SUB, pid, eid, lid)

    # Set OS/2 weight class
    if "OS/2" in font:
        weight_map = {"Regular": 400, "Bold": 700, "Italic": 400, "Bold Italic": 700, "Black": 900}
        if subfamily in weight_map:
            font["OS/2"].usWeightClass = weight_map[subfamily]

        # Set fsSelection flags
        # Bit 0 = ITALIC, Bit 5 = BOLD, Bit 6 = REGULAR
        flags = font["OS/2"].fsSelection
        flags &= ~(1 << 0 | 1 << 5 | 1 << 6)  # Clear italic, bold, regular bits
        if "Italic" in subfamily:
            flags |= 1 << 0
        if "Bold" in subfamily:
            flags |= 1 << 5
        if subfamily == "Regular":
            flags |= 1 << 6
        font["OS/2"].fsSelection = flags

    # Set macStyle in head table
    if "head" in font:
        style = 0
        if "Bold" in subfamily:
            style |= 1
        if "Italic" in subfamily:
            style |= 2
        font["head"].macStyle = style


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Copy existing static fonts (Charter) into typst/ as well
    static_fonts = [
        "charter-regular.otf",
        "charter-bold.otf",
        "charter-italic.otf",
        "charter-bold-italic.otf",
        "lxgw-wenkai-regular.ttf",
        "sarasa-mono-sc-regular.ttf",
        "tiro-devanagari-regular.ttf",
    ]

    print("Static font instances for Typst")
    print(f"Output: {OUT_DIR}\n")

    # Symlink existing static fonts
    for fname in static_fonts:
        src = SRC_DIR / fname
        dest = OUT_DIR / fname
        if not src.exists():
            print(f"  [skip] {fname} (source missing)")
            continue
        if dest.exists():
            print(f"  [exists] {fname}")
            continue
        os.symlink(os.path.relpath(src, OUT_DIR), dest)
        print(f"  [link] {fname}")

    print()

    # Generate instances from variable fonts
    font_cache = {}
    errors = 0

    for src_name, out_name, axes, family, subfamily in INSTANCES:
        dest = OUT_DIR / out_name
        if dest.exists():
            print(f"  [exists] {out_name}")
            continue

        src_path = SRC_DIR / src_name
        if not src_path.exists():
            print(f"  [skip] {out_name} (source {src_name} missing)")
            errors += 1
            continue

        # Cache source paths (font must be re-read each time since instancer mutates)
        if src_name not in font_cache:
            font_cache[src_name] = str(src_path)

        print(f"  [generate] {out_name} ({family} {subfamily})")
        try:
            font = TTFont(font_cache[src_name])
            static = instantiateVariableFont(font, axes)
            fix_name_table(static, family, subfamily)
            static.save(str(dest))
            size_kb = dest.stat().st_size / 1024
            print(f"             {size_kb:.0f} KB")
        except Exception as e:
            print(f"  [error] {out_name}: {e}", file=sys.stderr)
            errors += 1

    print()

    # Summary
    generated = [f for f in OUT_DIR.iterdir() if f.suffix in (".ttf", ".otf")]
    total_mb = sum(f.stat().st_size for f in generated) / (1024 * 1024)
    print(f"Total: {len(generated)} files, {total_mb:.1f} MB")

    if errors:
        print(f"Errors: {errors}")
        sys.exit(1)


if __name__ == "__main__":
    main()
