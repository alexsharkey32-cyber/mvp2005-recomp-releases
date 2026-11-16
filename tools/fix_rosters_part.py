#!/usr/bin/env python3
"""Remakes rosters-2026.tar with the corrected announcer names (fix/commentary-2026), uploads it to features-2 and
points features-2's manifest at it.   fix_rosters_part.py W REPO TAG"""
import hashlib, io, json, os, subprocess, sys, tarfile
W, repo, tag = sys.argv[1:4]
src = os.path.join(W, 'rosters-2026.tar'); out = os.path.join(W, 'new', 'rosters-2026.tar'); os.makedirs(os.path.dirname(out), exist_ok=True)
fix = {'mods/commentary-2026/DATA/DATABASE/DATABASE.BIG': 'fix/commentary-2026/DATABASE.BIG',
       'mods/commentary-2026/DATA/AUDIO/SPCH_PBP/PNAMEHDR.BIG': 'fix/commentary-2026/PBP_PNAMEHDR.BIG'}
drop = {'mods/commentary-2026/DATA/AUDIO/SPCH_PA/PNAMEHDR.BIG'}            # the stadium announcer's index is the disc's again
n = size = 0
with tarfile.open(src) as ti, tarfile.open(out, 'w', format=tarfile.USTAR_FORMAT) as to:
    for m in ti:
        if m.name in drop or m.name in fix: continue
        to.addfile(m, ti.extractfile(m) if m.isfile() else None)
        if m.isfile(): n += 1; size += m.size
    for name, p in fix.items():
        b = open(p, 'rb').read(); ti_ = tarfile.TarInfo(name); ti_.size = len(b); ti_.mode = 0o644
        to.addfile(ti_, io.BytesIO(b)); n += 1; size += len(b)
sha = hashlib.sha256(open(out, 'rb').read()).hexdigest()
subprocess.check_call(['gh', 'release', 'upload', tag, out, '--repo', repo, '--clobber'])
mp = os.path.join(W, 'manifest.json')
subprocess.check_call(['gh', 'release', 'download', tag, '--repo', repo, '--pattern', 'manifest.json', '--dir', W, '--clobber'])
m = json.load(open(mp))
for f in m['features']:
    if f['id'] == 'rosters-2026':
        f['version'] = str(int(f.get('version', '1')) + 1); f['install_size'] = size; f['files'] = n
        f['parts'] = [{'file': 'rosters-2026.tar', 'size': os.path.getsize(out), 'sha256': sha, 'files': n}]
        print('rosters-2026 ->', f['version'], n, 'files', os.path.getsize(out), sha)
json.dump(m, open(mp, 'w'), indent=1)
subprocess.check_call(['gh', 'release', 'upload', tag, mp, '--repo', repo, '--clobber'])
