#!/usr/bin/env python3
"""
Drop new product frames into the site.

    python3 process-images.py ~/Downloads/new-frames

Crops the generator watermark strip off the bottom of each square frame, writes
a 1024w and a 700w progressive JPEG into assets/img/products/, and reports
whether the watermark actually cleared.

Files are matched to slugs by filename: any file whose name starts with a known
slug (rest, calm, ease, clarity, sun, build, the-evening-three, the-morning-two)
is written to that slug. Anything else is listed and skipped.
"""

import os
import sys
import glob

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets/img/products")

SLUGS = ["the-evening-three", "the-morning-two",
         "rest", "calm", "ease", "clarity", "sun", "build"]

CROP_FRACTION = 0.852   # keeps the top 85.2% — clears the bottom-right sparkle
WIDE, NARROW = 1024, 700


def slug_for(filename):
    stem = os.path.basename(filename).lower().replace("_", "-")
    for s in SLUGS:                       # longest first, so bundles win
        if stem.startswith(s):
            return s
    return None


def corner_max(img):
    """Brightest pixel in the bottom-right corner — the watermark's hiding place."""
    g = img.convert("L")
    w, h = g.size
    return max(g.crop((int(w * 0.82), int(h * 0.82), w, h)).getdata())


def process(path):
    slug = slug_for(path)
    if not slug:
        return None, f"no slug in filename: {os.path.basename(path)}"

    im = Image.open(path).convert("RGB")
    im = im.crop((0, 0, im.width, round(im.height * CROP_FRACTION)))

    os.makedirs(OUT, exist_ok=True)
    h = round(im.height * WIDE / im.width)
    im.resize((WIDE, h), Image.LANCZOS).save(
        f"{OUT}/{slug}.jpg", quality=88, optimize=True, progressive=True)
    im.resize((NARROW, round(im.height * NARROW / im.width)), Image.LANCZOS).save(
        f"{OUT}/{slug}@700.jpg", quality=86, optimize=True, progressive=True)

    peak = corner_max(Image.open(f"{OUT}/{slug}.jpg"))
    flag = "  ← check this corner by eye" if peak > 245 else ""
    return slug, f"{slug:18s} {WIDE}x{h}  corner peak {peak}{flag}"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    src = os.path.expanduser(sys.argv[1])
    files = sorted(
        f for ext in ("jpg", "jpeg", "png", "webp")
        for f in glob.glob(os.path.join(src, f"*.{ext}"))
    )
    if not files:
        print(f"no images found in {src}")
        return 1

    done, skipped = [], []
    for f in files:
        slug, msg = process(f)
        (done if slug else skipped).append(msg)

    for m in done:
        print("  " + m)
    for m in skipped:
        print("  skipped: " + m)
    print(f"\n{len(done)} written. Now run: python3 build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
