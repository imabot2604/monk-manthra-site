#!/usr/bin/env python3
"""
Split a two-up generated frame into the two product images it contains.

    python3 split-pair.py <file.jpg> left-slug right-slug
    python3 split-pair.py ~/Downloads/pair.jpg golden-milk the-morning-two

Generators asked for two packs in one frame return a single square with the
two subjects side by side. This cuts it down the middle, then squares each
half around its subject rather than leaving a 1:2 portrait — the range
grid's card figure is 4/3 with object-fit:cover, and a portrait source gets
centre-cropped to a narrow horizontal band that decapitates a tall pouch.

Also drops the bottom strip, where these generators put their watermark,
and reports the brightest corner pixel afterwards so you can tell whether
it actually cleared.
"""

import os
import sys

from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/img/products")
WIDE, NARROW = 1024, 700
WATERMARK_STRIP = 0.12   # fraction of height removed from the bottom


def corner_peak(img):
    g = img.convert("L")
    w, h = g.size
    return max(g.crop((int(w * 0.80), int(h * 0.80), w, h)).getdata())


# Deliberately NOT squaring these halves.
#
# A half of a two-up frame is ~512x900 — squaring it crops away 43% of the
# height and clips the top and bottom off a tall pouch, which breaks
# Section Eleven's "generous empty space around it" outright. Padding out
# to landscape instead would mean fabricating more background than there is
# real photograph, which is worse.
#
# So each half is kept whole and portrait. On the product page that is
# ideal (.product__figure--photo lets height run free). In the 4/3 card the
# browser centre-crops to roughly the middle third — which on these packs
# lands on the mark, the wordmark and the product name, the most
# identifying band of the whole face.


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 1

    src, left_slug, right_slug = sys.argv[1], sys.argv[2], sys.argv[3]
    im = Image.open(os.path.expanduser(src)).convert("RGB")
    w, h = im.size
    print(f"source {w}x{h}")

    # Drop the watermark strip before splitting — it only ever sits bottom-right,
    # but trimming both halves keeps them the same shape.
    im = im.crop((0, 0, w, int(h * (1 - WATERMARK_STRIP))))
    mid = im.width // 2

    os.makedirs(OUT, exist_ok=True)
    for slug, box in [(left_slug, (0, 0, mid, im.height)),
                      (right_slug, (mid, 0, im.width, im.height))]:
        half = im.crop(box)
        ar = half.height / half.width
        # Upscaled to honour the 700w/1024w srcset descriptors build.py emits.
        # These two are genuinely half the linear resolution of the other
        # frames because they arrived two-to-an-image; shoot them singly if
        # the softness shows.
        big = half.resize((WIDE, round(WIDE * ar)), Image.LANCZOS)
        big.save(f"{OUT}/{slug}.jpg", quality=88, optimize=True, progressive=True)
        half.resize((NARROW, round(NARROW * ar)), Image.LANCZOS).save(
            f"{OUT}/{slug}@700.jpg", quality=86, optimize=True, progressive=True)
        peak = corner_peak(big)
        flag = "  <- check by eye" if peak > 245 else ""
        print(f"  {slug:20s} native {half.size[0]}x{half.size[1]} -> {big.size[0]}x{big.size[1]}  corner {peak}{flag}")

    print("\nNow run: python3 build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
