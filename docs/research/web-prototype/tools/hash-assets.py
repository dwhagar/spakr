#!/usr/bin/env python3
"""Content-hash static assets without Node: copy SRC to DEST naming each file name.<hash>.ext,
rewrite relative references (JS import specifiers, CSS url(), HTML href/src) and write manifest.json
(logical name -> hashed name) for the templates. Hashed files can be served 'immutable' for a year.
Limits: no import cycles (hash of a module depends on its imports); static references only."""
import hashlib, json, pathlib, re, shutil, sys

src, dest = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
files = sorted(p for p in src.rglob("*") if p.is_file())
imp = re.compile(r"""(from\s*|import\s*\(?\s*)(["'])(\.{1,2}/[^"']+\.js)\2""")
deps = {p: [(p.parent / m.group(3)).resolve() for m in imp.finditer(p.read_text())]
        for p in files if p.suffix == ".js"}
manifest, done = {}, {}

def build(p):
    p = p.resolve()
    if p in done:
        return done[p]
    data = p.read_bytes()
    if p.suffix == ".js":
        text = p.read_text()
        for m in imp.finditer(text):
            target = (p.parent / m.group(3)).resolve()
            text = text.replace(m.group(0), m.group(0).replace(m.group(3), "./" + build(target)))
        data = text.encode()
    name = f"{p.stem}.{hashlib.sha256(data).hexdigest()[:10]}{p.suffix}"
    out = dest / p.relative_to(src.resolve()).parent / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    done[p] = name
    manifest[str(p.relative_to(src.resolve()))] = str(out.relative_to(dest))
    return name

shutil.rmtree(dest, ignore_errors=True)
for p in files:
    build(p)
(dest / "manifest.json").write_text(json.dumps(manifest, indent=1, sort_keys=True))
print(f"{len(manifest)} files hashed")
