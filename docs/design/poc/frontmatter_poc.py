"""Front matter proof of concept for docs/design/content-model-and-exchange.html.

Shows the YAML 1.1 traps in PyYAML's default safe loader, a hardened loader that
removes them, the cost of parsing 5,000 pages, and a zip-bundle round trip with
the safety checks the importer needs. Run: python3 frontmatter_poc.py
"""
import io, re, time, zipfile, hashlib, sys
import yaml

class StrictLoader(yaml.CSafeLoader):
    """YAML 1.2 core-like: only true/false are booleans, no timestamps, no anchors."""

StrictLoader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag not in ("tag:yaml.org,2002:timestamp",)]
    for k, v in yaml.CSafeLoader.yaml_implicit_resolvers.items()
}
BOOL = re.compile(r"^(?:true|false)$")
StrictLoader.yaml_implicit_resolvers = {
    k: [(t, BOOL if t == "tag:yaml.org,2002:bool" else rx) for t, rx in v]
    for k, v in StrictLoader.yaml_implicit_resolvers.items()
}
# 'true'/'false' only start with t/f; y, n, o (yes/no/on/off) no longer resolve.
INT = re.compile(r"^[-+]?(?:0|[1-9][0-9]*)$")
StrictLoader.yaml_implicit_resolvers = {
    k: [(t, INT if t == "tag:yaml.org,2002:int" else rx) for t, rx in v]
    for k, v in StrictLoader.yaml_implicit_resolvers.items()
}

def load_strict(text):
    for ev in yaml.parse(text, Loader=StrictLoader):
        if isinstance(ev, (yaml.AliasEvent,)) or getattr(ev, "anchor", None):
            raise ValueError("anchors and aliases are not allowed")
        if isinstance(ev, (yaml.ScalarEvent, yaml.CollectionStartEvent)) and ev.tag:
            raise ValueError("explicit tags are not allowed")
    return yaml.load(text, Loader=StrictLoader)

SAMPLE = """\
spakr: 1
type: race
title: Gnomes
fields:
  size: no
  lifespan: 0750
  languages: [NO, on, 1e3]
  founded: 2001-02-03
"""
print("default safe_load:", yaml.safe_load(SAMPLE)["fields"])
print("strict loader    :", load_strict(SAMPLE)["fields"])
for bad in ("a: &x [1]\nb: *x\n", "a: !!python/object:os.system x\n"):
    try:
        load_strict(bad); print("NOT rejected:", bad)
    except Exception as e:
        print("rejected:", type(e).__name__, str(e).splitlines()[0])

doc = """\
spakr: 1
type: character
title: Captain Mara Vell
summary: Harbour master of Drift.
settings: [scifi]
tags: [navy, veteran]
visibility: public
image: {media: "image/9f2c41d0", alt: "Portrait", caption: "Mara in 2189"}
fields:
  race: race/human
  home_place: place/drift-station
  occupation: Harbour master
relations:
  - {kind: member_of, to: nation-state/free-ports, note: "since 2185"}
"""
N = 5000
t = time.perf_counter()
for _ in range(N): yaml.safe_load(doc)
a = time.perf_counter() - t
t = time.perf_counter()
for _ in range(N): yaml.load(doc, Loader=StrictLoader)
b = time.perf_counter() - t
t = time.perf_counter()
for _ in range(N): load_strict(doc)
c = time.perf_counter() - t
print(f"parse {N} front matters: safe_load {a*1000:.0f} ms, strict loader {b*1000:.0f} ms, strict plus event check {c*1000:.0f} ms")

# bundle round trip: export bytes == import bytes, manifest hashes verify
pages = {f"pages/character/p{i}.md": (f"---\n{doc}---\n\nBody {i}\n").encode() for i in range(N)}
t = time.perf_counter()
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
    manifest = {n: hashlib.sha256(d).hexdigest() for n, d in pages.items()}
    for n, d in pages.items(): z.writestr(n, d)
    z.writestr("manifest.txt", "\n".join(f"{h}  {n}" for n, h in manifest.items()))
w = time.perf_counter() - t
t = time.perf_counter()
ok = 0
with zipfile.ZipFile(buf) as z:
    total = sum(i.file_size for i in z.infolist())
    assert total < 500 * 2**20 and len(z.infolist()) < 100_000
    for i in z.infolist():
        assert not i.filename.startswith("/") and ".." not in i.filename.split("/")
        if i.filename.startswith("pages/"):
            d = z.read(i)
            ok += hashlib.sha256(d).hexdigest() == manifest[i.filename] and d == pages[i.filename]
r = time.perf_counter() - t
print(f"zip of {N} pages: {buf.tell()/1024:.0f} KB, write {w*1000:.0f} ms, read+verify {r*1000:.0f} ms, byte-identical {ok}/{N}")
