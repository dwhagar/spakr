#!/usr/bin/env python3
"""RES.26: git vs MySQL as the source of truth for page content.

Needs a running MySQL 8 (socket via MYSQL_SOCK, database "bench") and git.
Usage: python3 store_bench.py [pages] [edits_per_page_for_growth]
"""
import os, sys, time, random, subprocess, threading, statistics, difflib, tempfile, shutil, fcntl
import pymysql

PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
GROW_PAGES = 500
GROW_EDITS = int(sys.argv[2]) if len(sys.argv) > 2 else 20
SOCK = os.environ.get("MYSQL_SOCK", "/tmp/my.sock")
random.seed(7)
WORDS = [("w%d" % i) for i in range(4000)]

def body(n=450):
    return " ".join(random.choice(WORDS) for _ in range(n)) + "\n"

def edit(text):
    lines = text.split(" ")
    for _ in range(5):
        lines[random.randrange(len(lines))] = random.choice(WORDS)
    return " ".join(lines)

def ms(f, n):
    t = time.perf_counter()
    for i in range(n):
        f(i)
    return (time.perf_counter() - t) / n * 1000

def conn():
    return pymysql.connect(unix_socket=SOCK, user="root", database="bench", autocommit=False, charset="utf8mb4")

GIT_ENV = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1",
               GIT_AUTHOR_NAME="u", GIT_AUTHOR_EMAIL="u@x", GIT_COMMITTER_NAME="u", GIT_COMMITTER_EMAIL="u@x")
def git(repo, *a, inp=None):
    return subprocess.run(["git", "-C", repo, "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", *a],
                          env=GIT_ENV, input=inp, capture_output=True, text=True, check=True).stdout

def path(i):
    return "item/%02d/page-%d.md" % (i % 50, i)

def du(p):
    return int(subprocess.run(["du", "-sk", p], capture_output=True, text=True).stdout.split()[0])

out = {}
tmp = tempfile.mkdtemp(prefix="gs", dir="/tmp")
repo = os.path.join(tmp, "repo")
os.makedirs(repo); git(repo, "init", "-q")
texts = [body() for _ in range(PAGES)]
for i, t in enumerate(texts):
    p = os.path.join(repo, path(i)); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(t)
git(repo, "add", "-A"); git(repo, "commit", "-qm", "seed")

# ---------- MySQL schema
db = conn(); c = db.cursor()
c.execute("DROP TABLE IF EXISTS rev"); c.execute("DROP TABLE IF EXISTS pg")
c.execute("""CREATE TABLE pg (id INT PRIMARY KEY, version INT NOT NULL, body MEDIUMTEXT NOT NULL) ENGINE=InnoDB ROW_FORMAT=DYNAMIC""")
c.execute("""CREATE TABLE rev (id BIGINT AUTO_INCREMENT PRIMARY KEY, page_id INT NOT NULL, version INT NOT NULL,
  author INT NOT NULL, created_at DATETIME(6) NOT NULL, body MEDIUMTEXT NOT NULL, UNIQUE(page_id, version)) ENGINE=InnoDB ROW_FORMAT=DYNAMIC""")
for i in range(0, PAGES, 500):
    c.executemany("INSERT INTO pg VALUES (%s,1,%s)", [(j, texts[j]) for j in range(i, min(i + 500, PAGES))])
    c.executemany("INSERT INTO rev (page_id,version,author,created_at,body) VALUES (%s,1,1,NOW(6),%s)",
                  [(j, texts[j]) for j in range(i, min(i + 500, PAGES))])
db.commit()

# ---------- single-writer latency
cur = list(texts)
def git_write(i):
    k = random.randrange(PAGES); cur[k] = edit(cur[k])
    open(os.path.join(repo, path(k)), "w").write(cur[k])
    git(repo, "add", "--", path(k)); git(repo, "commit", "-q", "--author", "u <u@x>", "-m", "edit", "--", path(k))
out["write_git_ms"] = ms(git_write, 40)

def my_write(i):
    k = random.randrange(PAGES); cur[k] = edit(cur[k])
    c.execute("SELECT version FROM pg WHERE id=%s FOR UPDATE", (k,)); v = c.fetchone()[0]
    c.execute("UPDATE pg SET version=%s, body=%s WHERE id=%s", (v + 1, cur[k], k))
    c.execute("INSERT INTO rev (page_id,version,author,created_at,body) VALUES (%s,%s,1,NOW(6),%s)", (k, v + 1, cur[k]))
    db.commit()
out["write_mysql_ms"] = ms(my_write, 300)

# ---------- concurrent writers, 8 threads, 3 s
def run_threads(fn, n=8, secs=3):
    stop = time.time() + secs; counts = [0] * n; errs = [0] * n
    def w(t):
        cx = conn() if fn.__name__.startswith("my") else None
        while time.time() < stop:
            try:
                fn(t, cx); counts[t] += 1
            except Exception as e:
                errs[t] += 1
    th = [threading.Thread(target=w, args=(t,)) for t in range(n)]
    [x.start() for x in th]; [x.join() for x in th]
    return sum(counts) / secs, sum(errs)

def git_conc(t, cx):
    k = random.randrange(PAGES)
    lockf = open(os.path.join(tmp, "lock"), "w")  # one descriptor per operation: flock is per open file description
    fcntl.flock(lockf, fcntl.LOCK_EX)
    try:
        open(os.path.join(repo, path(k)), "a").write("x ")
        git(repo, "add", "--", path(k)); git(repo, "commit", "-q", "--author", "u <u@x>", "-m", "e", "--", path(k))
    finally:
        lockf.close()
out["conc_git_locked_per_s"], out["conc_git_locked_err"] = run_threads(git_conc)
def git_conc_nolock(t, cx):
    k = random.randrange(PAGES)
    open(os.path.join(repo, path(k)), "a").write("y ")
    git(repo, "add", "--", path(k)); git(repo, "commit", "-q", "--author", "u <u@x>", "-m", "e", "--", path(k))
out["conc_git_unlocked_per_s"], out["conc_git_unlocked_err"] = run_threads(git_conc_nolock, secs=2)
git(repo, "reset", "-q", "--hard") if False else None
subprocess.run(["rm", "-f", os.path.join(repo, ".git", "index.lock")])
def my_conc(t, cx):
    k = random.randrange(PAGES); cu = cx.cursor()
    cu.execute("SELECT version, body FROM pg WHERE id=%s FOR UPDATE", (k,)); v, b = cu.fetchone()
    cu.execute("UPDATE pg SET version=%s, body=%s WHERE id=%s", (v + 1, b + "x ", k))
    cu.execute("INSERT INTO rev (page_id,version,author,created_at,body) VALUES (%s,%s,1,NOW(6),%s)", (k, v + 1, b + "x "))
    cx.commit()
out["conc_mysql_per_s"], out["conc_mysql_err"] = run_threads(my_conc)
# same-page contention: all threads edit page 0
def my_same(t, cx):
    cu = cx.cursor()
    cu.execute("SELECT version, body FROM pg WHERE id=0 FOR UPDATE"); v, b = cu.fetchone()
    cu.execute("UPDATE pg SET version=%s WHERE id=0", (v + 1,))
    cu.execute("INSERT INTO rev (page_id,version,author,created_at,body) VALUES (0,%s,1,NOW(6),%s)", (v + 1, b))
    cx.commit()
out["conc_mysql_samepage_per_s"], out["conc_mysql_samepage_err"] = run_threads(my_same)

# ---------- reads
c.execute("COMMIT")
def my_read(i):
    c.execute("SELECT body FROM pg WHERE id=%s", (random.randrange(PAGES),)); c.fetchone()
out["read_mysql_pk_ms"] = ms(my_read, 2000)
def wt_read(i):
    open(os.path.join(repo, path(random.randrange(PAGES)))).read()
out["read_git_worktree_ms"] = ms(wt_read, 2000)
out["read_git_show_ms"] = ms(lambda i: git(repo, "show", "HEAD:" + path(random.randrange(PAGES))), 100)

# ---------- history features on one page with 30 edits in both stores
hp = 4242 % PAGES
for n in range(30):
    cur[hp] = edit(cur[hp])
    open(os.path.join(repo, path(hp)), "w").write(cur[hp])
    git(repo, "add", "--", path(hp)); git(repo, "commit", "-q", "--author", "u <u@x>", "-m", "e%d" % n, "--", path(hp))
    c.execute("SELECT version FROM pg WHERE id=%s", (hp,)); v = c.fetchone()[0]
    c.execute("UPDATE pg SET version=%s, body=%s WHERE id=%s", (v + 1, cur[hp], hp))
    c.execute("INSERT INTO rev (page_id,version,author,created_at,body) VALUES (%s,%s,1,NOW(6),%s)", (hp, v + 1, cur[hp]))
    db.commit()
out["hist_git_log_ms"] = ms(lambda i: git(repo, "log", "--format=%H %an %s", "--", path(hp)), 30)
def my_hist(i):
    c.execute("SELECT version, author, created_at FROM rev WHERE page_id=%s ORDER BY version DESC", (hp,)); c.fetchall()
out["hist_mysql_ms"] = ms(my_hist, 300)
shas = git(repo, "log", "--format=%H", "--", path(hp)).split()
out["diff_git_ms"] = ms(lambda i: git(repo, "diff", shas[5], shas[0], "--", path(hp)), 50)
def my_diff(i):
    c.execute("SELECT body FROM rev WHERE page_id=%s ORDER BY version DESC LIMIT 1 OFFSET 5", (hp,)); a = c.fetchone()[0]
    c.execute("SELECT body FROM rev WHERE page_id=%s ORDER BY version DESC LIMIT 1", (hp,)); b = c.fetchone()[0]
    list(difflib.unified_diff(a.split(" "), b.split(" "), lineterm=""))
out["diff_mysql_difflib_ms"] = ms(my_diff, 50)
out["blame_git_ms"] = ms(lambda i: git(repo, "blame", "--line-porcelain", "--", path(hp)), 20)
def my_blame(i):
    c.execute("SELECT body FROM rev WHERE page_id=%s ORDER BY version", (hp,)); rows = [r[0].split(" ") for r in c.fetchall()]
    owner = {}; prev = []
    for ver, ws in enumerate(rows):
        sm = difflib.SequenceMatcher(None, prev, ws, autojunk=False)
        new = [None] * len(ws)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            for j in range(j1, j2):
                new[j] = owner.get(i1 + (j - j1)) if tag == "equal" else ver
        owner = dict(enumerate(new)); prev = ws
out["blame_mysql_difflib_ms"] = ms(my_blame, 3)

# ---------- repository / table size and growth, GROW_PAGES pages x GROW_EDITS edits
gtmp = os.path.join(tmp, "grow"); os.makedirs(gtmp); grepo = os.path.join(gtmp, "r"); os.makedirs(grepo); git(grepo, "init", "-q")
c.execute("DROP TABLE IF EXISTS grev"); c.execute("CREATE TABLE grev (id BIGINT AUTO_INCREMENT PRIMARY KEY, page_id INT, version INT, body MEDIUMTEXT) ENGINE=InnoDB")
g = [texts[i] for i in range(GROW_PAGES)]
for i in range(GROW_PAGES):
    os.makedirs(os.path.dirname(os.path.join(grepo, path(i))), exist_ok=True); open(os.path.join(grepo, path(i)), "w").write(g[i])
git(grepo, "add", "-A"); git(grepo, "commit", "-qm", "s")
c.executemany("INSERT INTO grev (page_id,version,body) VALUES (%s,1,%s)", [(i, g[i]) for i in range(GROW_PAGES)]); db.commit()
for e in range(GROW_EDITS):
    for i in range(GROW_PAGES):
        g[i] = edit(g[i]); open(os.path.join(grepo, path(i)), "w").write(g[i])
    git(grepo, "add", "-A"); git(grepo, "commit", "-qm", "e%d" % e)
    c.executemany("INSERT INTO grev (page_id,version,body) VALUES (%s,%s,%s)", [(i, e + 2, g[i]) for i in range(GROW_PAGES)]); db.commit()
raw = sum(len(x) for x in g) / 1024
out["grow_raw_current_kb"] = raw
out["grow_git_loose_kb"] = du(os.path.join(grepo, ".git"))
git(grepo, "gc", "-q"); out["grow_git_gc_kb"] = du(os.path.join(grepo, ".git"))
c.execute("ANALYZE TABLE grev"); c.execute("SELECT data_length/1024 FROM information_schema.tables WHERE table_schema='bench' AND table_name='grev'")
out["grow_mysql_fullcopy_kb"] = float(c.fetchone()[0])
# MySQL with zlib compressed copies (what COMPRESS() would give)
c.execute("SELECT SUM(LENGTH(COMPRESS(body)))/1024 FROM grev"); out["grow_mysql_compress_kb"] = float(c.fetchone()[0])

# ---------- git at scale: add+commit with 20k files, history of one file
big = os.path.join(tmp, "big"); os.makedirs(big); git(big, "init", "-q")
for i in range(20000):
    p = os.path.join(big, path(i)); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(texts[i % PAGES])
git(big, "add", "-A"); git(big, "commit", "-qm", "seed")
def big_write(i):
    k = random.randrange(20000); open(os.path.join(big, path(k)), "a").write("z ")
    git(big, "add", "--", path(k)); git(big, "commit", "-q", "--author", "u <u@x>", "-m", "e", "--", path(k))
out["write_git_20k_files_ms"] = ms(big_write, 30)

# ---------- crash/consistency: kill between git commit and MySQL commit is a logic matter; measure fsck + rebuild
out["fsck_git_5k_s"] = ms(lambda i: git(repo, "fsck", "--no-dangling"), 1) / 1000
t = time.perf_counter()
for i in range(PAGES):
    open(os.path.join(repo, path(i))).read()
out["rebuild_read_5k_files_s"] = time.perf_counter() - t
t = time.perf_counter(); c.execute("SELECT id, body FROM pg"); rows = c.fetchall(); out["rebuild_read_5k_mysql_s"] = time.perf_counter() - t
t = time.perf_counter(); git(repo, "bundle", "create", os.path.join(tmp, "b.bundle"), "--all"); out["backup_git_bundle_s"] = time.perf_counter() - t
t = time.perf_counter(); subprocess.run("mysqldump -uroot -S%s bench pg rev > %s/d.sql" % (SOCK, tmp), shell=True); out["backup_mysqldump_s"] = time.perf_counter() - t
out["bundle_kb"] = os.path.getsize(os.path.join(tmp, "b.bundle")) / 1024
out["dump_kb"] = os.path.getsize(os.path.join(tmp, "d.sql")) / 1024

for k, v in out.items():
    print("%-32s %s" % (k, ("%.2f" % v) if isinstance(v, float) else v))
shutil.rmtree(tmp, ignore_errors=True)
