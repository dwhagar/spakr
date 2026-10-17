# Web layer prototype (research thread C, 2026-10-17)

Static pages and tools backing `docs/research/web-layer.html`, `web-devices.html` and `web-components.html`.
Open `index.html` or `editor.html` directly, or serve with the strict CSP the real site will use:

    python3 tools/serve-csp.py docs/research 8801 &     # serves with Content-Security-Policy; open /web-prototype/index.html
    python3 tools/contrast.py static/app.css            # palette contrast and light/dark consistency check
    python3 tools/hash-assets.py static /tmp/dist       # content-hashed copies plus manifest.json (no Node)
    python3 tools/make-icons.py LUCIDE_ICONS_DIR static/icons.svg search menu moon   # icon sprite
    NODE_PATH=... node tools/matrix.js                   # 9 viewports x light/dark x 2 pages: overflow, axe-core, CSP (needs playwright and axe-core from npm; in CI use Python playwright and a vendored axe.min.js)

`static/img/map.svg` and the pages are original to this project. Icons are copied from Lucide (ISC licence, https://lucide.dev).
Nothing here is production code; the real client lives in `src/` (UI.1).
