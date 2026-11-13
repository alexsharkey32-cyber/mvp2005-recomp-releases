#!/usr/bin/env python3
"""Packs build/hd-4x-webp or build/hd-2x-webp into release parts, uploads each to the features-2 release as it is made,
and writes the part records to OUT/<id>.json.   pack_hd.py ID OUT REPO TAG"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import make_features as mf
fid, out, repo, tag = sys.argv[1:5]
src = os.path.join(out, 'build', fid + '-webp')
entries = [(p, 'textures/hd/' + os.path.relpath(p, src).replace(os.sep, '/'), n) for p, n in mf.walk(src)]
parts = mf.plan_parts(entries, 1900 * 1000000)
rec = {'install_size': sum(e[2] for e in entries), 'files': len(entries), 'parts': []}
print('%s: %d files, %.2f GB, %d parts' % (fid, len(entries), rec['install_size'] / 1e9, len(parts)), flush=True)
for i, pe in enumerate(parts):
    name = '%s.part%d.tar' % (fid, i + 1) if len(parts) > 1 else '%s.tar' % fid
    path = os.path.join(out, name)
    extra = [('textures/hd/.pack-%s' % fid.split('-')[1], b'%s\n' % fid.encode())] if i == 0 else None
    size, sha = mf.write_tar(path, pe, extra)
    mf.upload(repo, tag, path); os.remove(path)
    rec['parts'].append({'file': name, 'size': size, 'sha256': sha, 'files': len(pe)})
    print('  %s %.0f MB uploaded' % (name, size / 1e6), flush=True)
json.dump(rec, open(os.path.join(out, fid + '.json'), 'w'))
