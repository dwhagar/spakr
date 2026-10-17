#!/usr/bin/env python3
"""Check text/background contrast of the design tokens in static/app.css, light and dark (WCAG 1.4.3 / 1.4.11).
Also checks that the media-query dark block and the [data-theme=dark] block hold identical values."""
import re, sys, pathlib

css = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "static/app.css").read_text()

def block(selector):
    m = re.search(re.escape(selector) + r"\s*\{(.*?)\}", css, re.S)
    return dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", m.group(1)))

light = block(":root")
dark_auto = block(":root:not([data-theme=\"light\"])")
dark = block(":root[data-theme=\"dark\"]")
assert dark_auto == dark, "dark palettes differ between media query and data-theme blocks"

def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

PAIRS = [("ink", "bg", 4.5), ("ink", "surface", 4.5), ("muted", "bg", 4.5), ("muted", "surface", 4.5),
         ("muted", "code-bg", 4.5), ("accent", "bg", 4.5), ("accent", "surface", 4.5), ("accent-ink", "accent", 4.5),
         ("ink", "accent-soft", 4.5), ("ink", "warn-bg", 4.5), ("nav-ink", "nav-bg", 4.5), ("ink", "code-bg", 4.5),
         ("focus", "bg", 3.0), ("focus", "surface", 3.0), ("line", "bg", 1.0), ("warn-line", "warn-bg", 3.0)]
bad = 0
for name, pal in (("light", light), ("dark", {**light, **dark})):
    for fg, bg, need in PAIRS:
        r = ratio(pal[fg], pal[bg])
        flag = "ok " if r >= need else "FAIL"
        bad += r < need
        print(f"{name:5} {fg:10} on {bg:10} {r:5.2f} (need {need}) {flag}")
sys.exit(1 if bad else 0)
