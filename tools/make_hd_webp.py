#!/usr/bin/env python3
"""A texture pack (a folder of WxH_hash.png) re-encoded as WebP, same names with .webp: about a seventh of the size
for the same look (see below), so the HD packs download several times faster. The game reads .webp and .png alike.

  python3 tools/release/make_hd_webp.py SRC DST [--quality 90] [--jobs N] [--redo-clear]

  e.g.  python3 tools/release/make_hd_webp.py textures/replace build/hd-4x-webp
        python3 tools/release/make_hd_webp.py build/hd-2x build/hd-2x-webp

Pictures with few colours (up to 256) are stored losslessly, and so is see-through art (lettering, fonts, logos, HUD
art) that lossy WebP can't keep within MIN_PSNR: it halves the colour resolution, which smears the sharp, saturated
edges of logos and lettering (measured: 26-31 dB on team logos against 41-45 dB on everything else). Everything else (the upscaled photos: uniforms, faces, crowds, grass, walls) is stored lossy at
--quality (default 90; the alpha channel is always lossless), which on a sample of the 4x pack measured a PSNR of
about 44 dB against the PNG - below what can be seen at the game's resolutions.
Resumable: textures already in DST are skipped. Needs Pillow with WebP (pip3 install pillow).
"""
import io, os, shutil, sys, time
import numpy as np
from multiprocessing import Pool
from PIL import Image, features

QUALITY = 90
MIN_PSNR = 33.0      # see-through art (logos, lettering) that lossy WebP can't keep this close goes lossless


def convert(args):
    src, dst, q, only_clear = args
    try:
        im = Image.open(src); im.load()
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGBA' if ('A' in im.mode or 'transparency' in im.info) else 'RGB')
        if im.mode == 'RGBA' and im.getextrema()[3][0] == 255: im = im.convert('RGB')    # alpha that is all opaque
        few = im.getcolors(256) is not None
        clear = im.mode == 'RGBA' and sum(im.getchannel('A').histogram()[:16]) >= 0.10 * im.width * im.height
        if only_clear and not clear: return 0, 0, False
        tmp = dst + '.tmp'
        if not few:
            buf = io.BytesIO(); im.save(buf, 'WEBP', quality=q, method=4, alpha_quality=100, exact=True)
            if clear:                                      # see-through art: kept lossless where lossy smears it
                x = np.asarray(im, dtype=np.float32); y = np.asarray(Image.open(io.BytesIO(buf.getvalue())).convert('RGBA'), dtype=np.float32)
                m = x[..., 3] > 200
                e = float(((x[..., :3] - y[..., :3]) ** 2)[m].mean()) if m.any() else 0.0
                few = e > 255.0 ** 2 / 10 ** (MIN_PSNR / 10)
            if not few:
                with open(tmp, 'wb') as o: o.write(buf.getvalue())
        if few: im.save(tmp, 'WEBP', lossless=True, quality=50, method=2, exact=True)   # (method 2: 8x faster than 4, 5 % bigger)
        os.replace(tmp, dst)
        return os.path.getsize(src), os.path.getsize(dst), few
    except Exception as e:
        sys.stderr.write('%s: %s\n' % (src, e)); return 0, 0, False


def main():
    a = [x for x in sys.argv[1:]]
    def opt(name, default):
        if name in a: i = a.index(name); a.pop(i); return a.pop(i)
        return default
    redo = '--redo-clear' in a
    if redo: a.remove('--redo-clear')                     # made before see-through art was kept lossless: redo only those
    q = int(opt('--quality', QUALITY)); jobs = int(opt('--jobs', max(1, (os.cpu_count() or 2) - 1)))
    if len(a) < 2: print(__doc__); sys.exit(1)
    if not features.check('webp'): print('This Pillow has no WebP support: pip3 install --upgrade pillow'); sys.exit(1)
    src, dst = a[0], a[1]
    os.makedirs(dst, exist_ok=True)
    have = set(os.listdir(dst))
    todo = []
    for f in sorted(os.listdir(src)):
        if f.endswith('.tmp.png'): continue
        if not f.endswith('.png'):                        # the pack's marker (.pack-4x) and other files: as they are
            if os.path.isfile(os.path.join(src, f)) and f not in have: shutil.copy2(os.path.join(src, f), os.path.join(dst, f))
            continue
        out = f[:-4] + '.webp'
        if redo or out not in have: todo.append((os.path.join(src, f), os.path.join(dst, out), q, redo))
    print('%d to do (%d done before), %d processes, quality %d' % (len(todo), len(have), jobs, q), flush=True)
    t0 = time.time(); n = 0; sin = sout = 0; nfew = 0
    with Pool(jobs) as p:
        for i, o, few in p.imap_unordered(convert, todo, chunksize=32):
            n += 1; sin += i; sout += o; nfew += few
            if n % 2000 == 0:
                el = time.time() - t0
                print('%d of %d, %.2f GB -> %.2f GB so far, about %.0f min left' % (n, len(todo), sin / 1e9, sout / 1e9, el / n * (len(todo) - n) / 60), flush=True)
    print('done: %d in %.0f min, %.2f GB -> %.2f GB (%d lossless)' % (n, (time.time() - t0) / 60, sin / 1e9, sout / 1e9, nfew), flush=True)


if __name__ == '__main__':
    main()
