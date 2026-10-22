"""RES.26/28/30 measurements: hashing, compression, par2 and erasure coding, hash chain.
Run: python3 integrity_bench.py  (needs par2, pbzip2, zstd; zfec and reedsolo optional)"""
import hashlib, os, random, shutil, subprocess, tempfile, time, tarfile, json

def t(f, *a):
    s = time.perf_counter(); r = f(*a); return time.perf_counter() - s, r

def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)

work = tempfile.mkdtemp(prefix="intbench")
rnd = random.Random(1)

# --- hashing 100 MB
blob = os.urandom(100 * 1024 * 1024)
print("HASH 100 MB")
for name in ("sha256", "sha512", "blake2b", "sha3_256", "md5"):
    d, _ = t(lambda: hashlib.new(name, blob).hexdigest())
    print(f"  {name:9s} {d*1000:7.1f} ms  {100/d:6.0f} MB/s")
import zlib
d, _ = t(zlib.crc32, blob); print(f"  crc32     {d*1000:7.1f} ms  {100/d:6.0f} MB/s")

# --- row hash chain, 100k rows
print("CHAIN")
def chain(n):
    prev = b"\0" * 32
    for i in range(n):
        row = json.dumps({"id": i, "actor": 7, "action": "page.edit", "target": i * 3}, sort_keys=True).encode()
        prev = hashlib.sha256(prev + row).digest()
    return prev
d, _ = t(chain, 100000); print(f"  100000 rows chained in {d*1000:.0f} ms ({d/100000*1e6:.1f} us per row)")

# --- compression corpus: text pages + git pack + incompressible media
words = open("/usr/share/dict/words").read().split() if os.path.exists("/usr/share/dict/words") else [f"w{i}" for i in range(5000)]
corp = os.path.join(work, "corpus"); os.makedirs(corp + "/content"); os.makedirs(corp + "/media")
for i in range(5000):
    open(f"{corp}/content/p{i}.md", "w").write(" ".join(rnd.choice(words) for _ in range(450)))
for i in range(5):
    open(f"{corp}/media/v{i}.mp4", "wb").write(os.urandom(20 * 1024 * 1024))
sql = os.path.join(work, "dump.sql")
with open(sql, "w") as f:
    for i in range(200000):
        f.write(f"INSERT INTO audit_log VALUES ({i},7,'page.edit','page',{i*3},'{{}}','203.0.113.5','2026-10-22 01:00:00');\n")
print("COMPRESS (text = 5000 pages 13 MB; sql = 200k audit rows; media = 100 MB random, like h264)")
def tarit(path, flt):
    sh(f"tar -C {corp} -cf - {path} | {flt} > {work}/out.bin")
    return os.path.getsize(f"{work}/out.bin")
for label, path in (("text", "content"), ("media", "media")):
    raw = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(f"{corp}/{path}") for f in fs)
    for flt in ("gzip -6", "bzip2 -9", "pbzip2 -9 -p4", "zstd -3 -T4", "zstd -19 -T4"):
        d, sz = t(tarit, path, flt)
        print(f"  {label:5s} {flt:15s} {d:6.2f} s  {sz/raw*100:5.1f}% of {raw/1e6:.0f} MB")
raw = os.path.getsize(sql)
for flt in ("gzip -6", "bzip2 -9", "pbzip2 -9 -p4", "zstd -3 -T4"):
    d, _ = t(lambda: sh(f"{flt} < {sql} > {work}/out.bin"))
    print(f"  sql   {flt:15s} {d:6.2f} s  {os.path.getsize(work+'/out.bin')/raw*100:5.1f}% of {raw/1e6:.0f} MB")

# --- par2 on a 100 MB archive
print("PAR2 on a 100 MB archive")
arc = os.path.join(work, "arc.tar.bz2"); open(arc, "wb").write(blob)
for pct in (5, 10, 20):
    for f in os.listdir(work):
        if f.startswith("arc") and f != "arc.tar.bz2": os.remove(os.path.join(work, f))
    d, r = t(sh, f"cd {work} && par2 create -q -r{pct} -n1 arc.tar.bz2.par2 arc.tar.bz2")
    psz = sum(os.path.getsize(os.path.join(work, f)) for f in os.listdir(work) if f.endswith(".par2"))
    dv, rv = t(sh, f"cd {work} && par2 verify -q arc.tar.bz2.par2")
    print(f"  r{pct:2d}%: create {d:5.2f} s, parity {psz/1e6:5.1f} MB, verify {dv:4.2f} s (rc {rv.returncode})")
    # damage: flip 2 KB in 3 places
    with open(arc, "r+b") as f:
        orig = []
        for off in (1_000_000, 50_000_000, 99_000_000):
            f.seek(off); orig.append((off, f.read(2048))); f.seek(off); f.write(os.urandom(2048))
    dr, rr = t(sh, f"cd {work} && par2 repair -q arc.tar.bz2.par2")
    ok = hashlib.sha256(open(arc, "rb").read()).digest() == hashlib.sha256(blob).digest()
    print(f"        repair of 3 damaged spots: {dr:5.2f} s rc {rr.returncode} identical={ok}")
    # damage beyond budget: overwrite 30% of file
    with open(arc, "r+b") as f:
        f.seek(0); f.write(os.urandom(30 * 1024 * 1024))
    dr, rr = t(sh, f"cd {work} && par2 repair -q arc.tar.bz2.par2")
    ok = hashlib.sha256(open(arc, "rb").read()).digest() == hashlib.sha256(blob).digest()
    print(f"        30 MB wiped: repair rc {rr.returncode} identical={ok}")
    open(arc, "wb").write(blob)

# par2 on many small files
print("PAR2 on 5000 small page files vs one bundle")
for f in os.listdir(work):
    if f.endswith(".par2"): os.remove(os.path.join(work, f))
d, r = t(sh, f"cd {corp}/content && par2 create -q -r10 -n1 {work}/small.par2 *.md")
print(f"  5000 files, 13 MB: {d:.1f} s, rc {r.returncode}")
sh(f"tar -C {corp} -cf {work}/c.tar content")
d, r = t(sh, f"cd {work} && par2 create -q -r10 -n1 c.par2 c.tar")
print(f"  single tar of the same: {d:.2f} s")

# erasure coding libraries
print("ERASURE CODING")
try:
    import zfec
    k, m = 10, 11
    data = blob[: (len(blob) // k) * k]; sz = len(data) // k
    blocks = [data[i * sz:(i + 1) * sz] for i in range(k)]
    enc = zfec.Encoder(k, m)
    d, res = t(enc.encode, blocks)
    print(f"  zfec k=10 m=11 (10% parity) on 100 MB: {d:.2f} s")
except Exception as e: print("  zfec:", e)
try:
    import reedsolo
    rs = reedsolo.RSCodec(25)
    chunk = blob[: 1024 * 1024]
    d, _ = t(rs.encode, chunk)
    print(f"  reedsolo 25 parity bytes per 230 on 1 MB: {d:.2f} s  => {100*d:.0f} s for 100 MB")
except Exception as e: print("  reedsolo:", e)
shutil.rmtree(work)
