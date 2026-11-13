#!/bin/bash
# convert.sh ID W: the old release's PNG pack ID, part by part, into W/build/ID-webp
set -eu
id=$1; W=$2; M=$W/old-manifest.json; BASE=https://github.com/${GITHUB_REPOSITORY}/releases/download/features
for part in $(python3 -c "import json;m=json.load(open('$M'));print(' '.join(p['file'] for f in m['features'] if f['id']=='$id' for p in f['parts']))"); do
  t0=$(date +%s)
  curl -sSL --retry 5 -o "$W/$part" "$BASE/$part"
  mkdir -p "$W/stage" && tar -xf "$W/$part" -C "$W/stage" && rm -f "$W/$part"
  python3 tools/make_hd_webp.py "$W/stage/textures/hd" "$W/build/$id-webp" --jobs 4 | tail -1
  rm -rf "$W/stage"
  echo "== $part in $(( $(date +%s) - t0 )) s, pack so far $(du -sh "$W/build/$id-webp" | cut -f1), disk free $(df -h "$W" | tail -1 | awk '{print $4}')"
done
