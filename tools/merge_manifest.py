#!/usr/bin/env python3
"""manifest.json for features-2: the old features release's manifest, its features downloading from there as before,
with the HD packs replaced by the WebP ones (OUT/hd-4x.json, OUT/hd-2x.json).   merge_manifest.py OLD OUT OLD_BASE"""
import json, os, sys
old, out, base = sys.argv[1:4]
m = json.load(open(old))
for f in m['features']:
    if f['id'] in ('hd-4x', 'hd-2x'):
        f.update(json.load(open(os.path.join(out, f['id'] + '.json'))))
    else:
        for p in f.get('parts', []): p.setdefault('url', base + p['file'])
    for pv in f.get('previews', []):
        if pv.get('file'): pv.setdefault('url', base + 'preview-' + pv['file'])
        if pv.get('after'): pv.setdefault('after_url', base + 'preview-' + pv['after'])
json.dump(m, open(os.path.join(out, 'manifest.json'), 'w'), indent=1)
for f in m['features']: print(f['id'], len(f.get('parts', [])), round(sum(p['size'] for p in f.get('parts', [])) / 1e9, 2), 'GB')
