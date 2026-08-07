"""
Converts assets/hardik.png into an animated monochrome ASCII-art SVG.
No external services, no JS - pure SVG + SMIL animation so GitHub renders it.
"""
import numpy as np
from PIL import Image, ImageOps

SRC = "assets/hardik.png"
OUT = "assets/ascii-portrait.svg"

COLS = 90
FONT_W = 6.2
FONT_H = 11
GREEN = "#39d353"
BG = "#0d1117"

# density ramp: sparse (dark) -> dense (light) characters, reversed since
# we invert luminance to read light-on-dark like a terminal
RAMP = " .:-=+*#%@"


def load_grid():
    img = Image.open(SRC).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    w, h = img.size
    cell_w = w / COLS
    # characters are taller than wide, compensate aspect ratio
    rows = int((h / cell_w) * (FONT_W / FONT_H) * COLS / COLS * (h / w) * 0) or 0
    rows = int(COLS * (h / w) * (FONT_W / FONT_H))
    img = img.resize((COLS, rows))
    arr = np.asarray(img).astype(float) / 255.0
    return arr


def to_chars(arr):
    idx = (arr * (len(RAMP) - 1)).astype(int)
    return [[RAMP[v] for v in row] for row in idx]


def build_svg(chars):
    rows = len(chars)
    cols = len(chars[0])
    width = cols * FONT_W
    height = rows * FONT_H

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">'
    )
    parts.append(f'<rect width="100%" height="100%" fill="{BG}"/>')
    parts.append(
        f'<style>text{{font-family:"Courier New",monospace;font-size:{FONT_H}px;'
        f'fill:{GREEN};white-space:pre;}}</style>'
    )

    for r, row in enumerate(chars):
        line = "".join(row).replace("&", "&amp;").replace("<", "&lt;")
        y = (r + 1) * FONT_H
        delay = r * 0.035
        parts.append(
            f'<text x="0" y="{y:.1f}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f"{line}</text>"
        )

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    arr = load_grid()
    chars = to_chars(arr)
    svg = build_svg(chars)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(chars[0])}x{len(chars)} chars)")
