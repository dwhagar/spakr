#!/usr/bin/env python3
"""Build static/icons.svg (an SVG sprite) from a short list of Lucide icons (ISC licence).

usage: make-icons.py LUCIDE_ICONS_DIR OUT.svg name [name ...]
Only the icons the UI uses are copied, so the sprite stays a few KB.
"""
import re, sys, pathlib

src, out, names = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3:]
symbols = []
for name in names:
    svg = (src / f"{name}.svg").read_text()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    inner = re.sub(r"\s+", " ", inner).strip()
    symbols.append(f'<symbol id="i-{name}" viewBox="0 0 24 24">{inner}</symbol>')
out.write_text('<svg xmlns="http://www.w3.org/2000/svg">\n' + "\n".join(symbols) + "\n</svg>\n")
print(f"{len(symbols)} icons, {out.stat().st_size} bytes")
