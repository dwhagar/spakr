#!/usr/bin/env python3
"""RES.33 benchmark: git vs Mercurial vs Fossil vs Subversion as a page store.
Usage: vcs_bench.py WORKDIR   (needs git, hg, fossil, svn, svnmucc on PATH)
"""
import os, random, shutil, subprocess as sp, sys, time, threading, statistics as st

W = os.path.abspath(sys.argv[1]); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
N, SIZE = 2000, 2500
random.seed(7)
words = [''.join(random.choices('abcdefghij klmnop', k=random.randint(3, 9))) for _ in range(500)]
def body(i, rev=0):
    r = random.Random(i)
    t = ' '.join(r.choice(words) for _ in range(SIZE // 6))
    for k in range(rev):  # each revision changes a few words
        rr = random.Random(i * 1000 + k); ws = t.split(' ')
        for _ in range(5): ws[rr.randrange(len(ws))] = rr.choice(words)
        t = ' '.join(ws)
    return t + '\n'
def path(i): return f'page/{i % 50:02d}/p{i}.md'
def run(cmd, cwd=None, env=None, ok=False):
    e = dict(os.environ, FOSSIL_USER='a', **(env or {}))
    r = sp.run(cmd, cwd=cwd, env=e, capture_output=True, text=True)
    if r.returncode and not ok: raise RuntimeError(f'{cmd}: {r.stderr[:300]}')
    return r.stdout
def timed(f, n=15):
    ts = []
    for k in range(n):
        t = time.perf_counter(); f(k); ts.append((time.perf_counter() - t) * 1000)
    return round(st.median(ts), 1)
def du(p): return int(run(['du', '-sk', p]).split()[0])
def conc(f, writers=8, each=10):
    errs = [0]
    def w(j):
        for k in range(each):
            try: f(j, k)
            except Exception: errs[0] += 1
    t = time.perf_counter()
    th = [threading.Thread(target=w, args=(j,)) for j in range(writers)]
    [x.start() for x in th]; [x.join() for x in th]
    return round(writers * each / (time.perf_counter() - t), 1), errs[0]
def seed(root):
    for i in range(N):
        p = os.path.join(root, path(i)); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w').write(body(i))
def edit(root, i, rev):
    open(os.path.join(root, path(i)), 'w').write(body(i, rev))
out = {}

# ---- git (working tree + flock-less here; concurrent test with and without serialisation)
g = f'{W}/git'; os.makedirs(g); seed(g)
ge = {'GIT_AUTHOR_NAME': 'a', 'GIT_AUTHOR_EMAIL': 'a@x', 'GIT_COMMITTER_NAME': 'a', 'GIT_COMMITTER_EMAIL': 'a@x'}
run(['git', 'init', '-q', '-b', 'main'], g); run(['git', 'add', '-A'], g); run(['git', 'commit', '-qm', 'seed'], g, ge)
def git_save(i, rev, lock=None):
    edit(g, i, rev); p = path(i)
    if lock: lock.acquire()
    try: run(['git', 'add', '--', p], g); run(['git', 'commit', '-qm', f'e{rev}', '--', p], g, ge)
    finally:
        if lock: lock.release()
r = {}
r['save'] = timed(lambda k: git_save(k, 1))
lk = threading.Lock()
r['conc'] = conc(lambda j, k: git_save(100 + j * 10 + k, 2, lk))
r['conc_nolock'] = conc(lambda j, k: git_save(300 + j * 10 + k, 2))
for rev in range(3, 12):
    for i in range(300, 340): edit(g, i, rev)
    run(['git', 'add', '-A'], g); run(['git', 'commit', '-qm', f'r{rev}'], g, ge)
r['history'] = timed(lambda k: run(['git', 'log', '--format=%H %an %ad', '--', path(310)], g))
r['diff'] = timed(lambda k: run(['git', 'diff', 'HEAD~3', 'HEAD', '--', path(310)], g))
r['blame'] = timed(lambda k: run(['git', 'blame', '--', path(310)], g))
r['old'] = timed(lambda k: run(['git', 'show', f'HEAD~4:{path(310)}'], g))
run(['git', 'gc', '-q'], g); r['size_kb'] = du(g + '/.git'); out['git'] = r

# ---- mercurial
h = f'{W}/hg'; os.makedirs(h); seed(h)
he = {'HGUSER': 'a <a@x>', 'HGPLAIN': '1'}
run(['hg', 'init'], h); run(['hg', 'add', '-q'], h, he); run(['hg', 'commit', '-qm', 'seed'], h, he)
def hg_save(i, rev):
    edit(h, i, rev); run(['hg', 'commit', '-qm', f'e{rev}', path(i)], h, he)
r = {}
r['save'] = timed(lambda k: hg_save(k, 1))
r['conc'] = conc(lambda j, k: hg_save(100 + j * 10 + k, 2))
r['conc_nolock'] = '(hg locks internally)'
for rev in range(3, 12):
    for i in range(300, 340): edit(h, i, rev)
    run(['hg', 'commit', '-qm', f'r{rev}'], h, he)
r['history'] = timed(lambda k: run(['hg', 'log', '--template', '{node} {author} {date}\n', path(310)], h, he))
r['diff'] = timed(lambda k: run(['hg', 'diff', '-r', '.~3', '-r', '.', path(310)], h, he))
r['blame'] = timed(lambda k: run(['hg', 'annotate', path(310)], h, he))
r['old'] = timed(lambda k: run(['hg', 'cat', '-r', '.~4', path(310)], h, he))
r['size_kb'] = du(h + '/.hg'); out['hg'] = r

# ---- fossil
f = f'{W}/fossil'; os.makedirs(f); fz = f'{f}/r.fossil'; fw = f'{f}/w'; os.makedirs(fw)
run(['fossil', 'new', '--admin-user', 'a', fz])
run(['fossil', 'open', fz, '--workdir', fw], fw, ok=True); seed(fw)
run(['fossil', 'addremove'], fw); run(['fossil', 'commit', '-m', 'seed', '--no-warnings', '--hash'], fw)
def fo_save(i, rev):
    edit(fw, i, rev); run(['fossil', 'commit', '-m', f'e{rev}', '--no-warnings', '--hash', path(i)], fw)
r = {}
r['save'] = timed(lambda k: fo_save(k, 1))
r['conc'] = conc(lambda j, k: fo_save(100 + j * 10 + k, 2))
r['conc_nolock'] = '(SQLite locks; shared work tree)'
for rev in range(3, 12):
    for i in range(300, 340): edit(fw, i, rev)
    run(['fossil', 'commit', '-m', f'r{rev}', '--no-warnings', '--hash'], fw)
r['history'] = timed(lambda k: run(['fossil', 'finfo', path(310)], fw))
r['diff'] = timed(lambda k: run(['fossil', 'diff', '--from', 'current-3', '--to', 'current', path(310)], fw, ok=True))
r['blame'] = timed(lambda k: run(['fossil', 'blame', path(310)], fw))
r['old'] = timed(lambda k: run(['fossil', 'cat', '-r', 'tip', path(310)], fw))
run(['fossil', 'rebuild', '--compress', fz]); r['size_kb'] = du(fz); out['fossil'] = r

# ---- subversion (server-side commits with svnmucc, no working copy needed)
s = f'{W}/svn'; run(['svnadmin', 'create', s]); url = 'file://' + s
imp = f'{W}/svnimp'; os.makedirs(imp); seed(imp)
run(['svn', 'import', '-q', '-m', 'seed', imp, url])
def sv_save(i, rev):
    tmp = f'{W}/svn_{threading.get_ident()}.md'; open(tmp, 'w').write(body(i, rev))
    run(['svnmucc', '-m', f'e{rev}', '-U', url, 'put', tmp, path(i)])
r = {}
r['save'] = timed(lambda k: sv_save(k, 1))
r['conc'] = conc(lambda j, k: sv_save(100 + j * 10 + k, 2))
r['conc_nolock'] = '(FSFS handles it; retries on conflict)'
wc = f'{W}/svnwc'; run(['svn', 'co', '-q', url, wc])
for rev in range(3, 12):
    for i in range(300, 340): edit(wc, i, rev)
    run(['svn', 'commit', '-q', '-m', f'r{rev}', wc])
run(['svn', 'update', '-q', wc])
r['history'] = timed(lambda k: run(['svn', 'log', f'{url}/{path(310)}']))
r['diff'] = timed(lambda k: run(['svn', 'diff', '-r', 'HEAD:HEAD', f'{url}/{path(310)}'], ok=True))
r['blame'] = timed(lambda k: run(['svn', 'blame', f'{url}/{path(310)}']))
r['old'] = timed(lambda k: run(['svn', 'cat', '-r', '5', f'{url}/{path(310)}']))
r['size_kb'] = du(s); out['svn'] = r

import json; print(json.dumps(out, indent=1))
