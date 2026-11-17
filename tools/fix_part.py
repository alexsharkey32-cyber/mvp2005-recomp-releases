#!/usr/bin/env python3
"""Remakes a feature's tar with corrected announcer names (fix/<id>/DATABASE.BIG, PBP_PNAMEHDR.BIG), uploads it to
TAG and points TAG's manifest at it (version + 1).   fix_part.py ID PREFIX W REPO TAG
PREFIX: the pack's commentary folder in the tar, e.g. mods/pack-1910/commentary"""
import hashlib, io, json, os, subprocess, sys, tarfile
fid, pre, W, repo, tag = sys.argv[1:6]
src = os.path.join(W, fid + '.tar'); out = os.path.join(W, 'new', fid + '.tar'); os.makedirs(os.path.dirname(out), exist_ok=True)
fix = {pre + '/DATA/DATABASE/DATABASE.BIG': 'fix/%s/DATABASE.BIG' % fid,
       pre + '/DATA/AUDIO/SPCH_PBP/PNAMEHDR.BIG': 'fix/%s/PBP_PNAMEHDR.BIG' % fid}
drop = {pre + '/DATA/AUDIO/SPCH_PA/PNAMEHDR.BIG'}
n = size = 0
with tarfile.open(src) as ti, tarfile.open(out, 'w', format=tarfile.USTAR_FORMAT) as to:
    for m in ti:
        if m.name in drop or m.name in fix: continue
        to.addfile(m, ti.extractfile(m) if m.isfile() else None)
        if m.isfile(): n += 1; size += m.size
    for name, p in fix.items():
        b = open(p, 'rb').read(); t = tarfile.TarInfo(name); t.size = len(b); t.mode = 0o644
        to.addfile(t, io.BytesIO(b)); n += 1; size += len(b)
h = hashlib.sha256()
with open(out, 'rb') as f:
    for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
tsize = os.path.getsize(out)
subprocess.check_call(['gh', 'release', 'upload', tag, out, '--repo', repo, '--clobber'])
os.remove(out); os.remove(src)
mp = os.path.join(W, 'manifest.json')
subprocess.check_call(['gh', 'release', 'download', tag, '--repo', repo, '--pattern', 'manifest.json', '--dir', W, '--clobber'])
m = json.load(open(mp))
for f in m['features']:
    if f['id'] == fid:
        f['version'] = str(int(f.get('version', '1')) + 1); f['install_size'] = size; f['files'] = n
        f['parts'] = [{'file': fid + '.tar', 'size': tsize, 'sha256': h.hexdigest(), 'files': n}]
        print(fid, '->', f['version'], n, 'files', h.hexdigest())
json.dump(m, open(mp, 'w'), indent=1)
subprocess.check_call(['gh', 'release', 'upload', tag, mp, '--repo', repo, '--clobber'])
