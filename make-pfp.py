"""
Instagram profile picture: the mark on a deep-purple disc.

Not a fresh design — it reproduces the header lockup exactly, which is the
treatment already signed off. Geometry comes from build.py's numbers, not
from eyeballing: ring radii 14.0 / 22.4 / 35.84 and a 5.2 seed on a 100-unit
canvas, each arc running 20deg to 340deg clockwise from the top so the gap
is centred and identical on all three.

Two things Instagram forces:

1. It crops every avatar to a circle, so the square PNG is really a circle
   brief. The purple ground is painted as a full-bleed square anyway — a
   square whose corners get cut is safe, a circle drawn slightly wrong is
   a visible seam against the app's background.
2. Small display. The mark's own reduction rule (Section Two) would drop to
   one ring at this size, but the brand owner already overrode that for the
   header at 32px. Three rings here keeps the two marks identical, which is
   the whole point.

Ink-to-canvas ratio is taken from the header disc rather than invented:
a 32px mark (=22.94px of actual ink) inside a 46px disc is 0.499.
"""
from PIL import Image, ImageDraw

SS = 4                     # supersample; PIL has no antialiased arc
OUT = 1080                 # Instagram stores 320px, but upload big and let it downsample
N = OUT * SS

DEEP_PURPLE = (0x3A, 0x1F, 0x5C)
HALF_WHITE  = (0xF4, 0xF1, 0xEC)
PALE_LILAC  = (0xCB, 0xBF, 0xE0)
LIGHT_GOLD  = (0xE0, 0xC8, 0x8C)

SEED_R = 5.2

# Two builds. The full mark is the correct artwork and wrong for the job;
# rendered at 32-44px its three 2.4-unit strokes fall below one device pixel
# and read as a smudge. The reduction is Section Two's own answer to that:
# one ring, and it is not a compromise, it is the rule.
#
# The reduction also gets a heavier stroke and more of the canvas. Both are
# required, not stylistic: thin ink is what fails first, and clear space is
# only worth protecting while there is something legible inside it.
VARIANTS = {
    "instagram-pfp-full": dict(
        rings=[(14.0, HALF_WHITE), (22.4, PALE_LILAC), (35.84, LIGHT_GOLD)],
        stroke=2.4, ink=0.499, seed=SEED_R),
    "instagram-pfp": dict(
        rings=[(35.84, LIGHT_GOLD)],
        stroke=5.0, ink=0.62, seed=8.0),
}

for name, v in VARIANTS.items():
    outer = max(r for r, _ in v["rings"])
    scale = (v["ink"] * N) / (outer * 2)
    cx = cy = N / 2

    img = Image.new("RGB", (N, N), DEEP_PURPLE)
    d = ImageDraw.Draw(img)

    # PIL angles: 0deg is 3 o'clock, increasing clockwise. The guide measures
    # clockwise from 12 o'clock, so subtract 90. 20->340 becomes -70->250, a
    # 320deg sweep leaving the 40deg gap centred exactly on top.
    for r, colour in v["rings"]:
        rr = r * scale
        w = max(1, round(v["stroke"] * scale))
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], -70, 250, fill=colour, width=w)

    sr = v["seed"] * scale
    d.ellipse([cx - sr, cy - sr, cx + sr, cy + sr], fill=LIGHT_GOLD)

    img.resize((OUT, OUT), Image.LANCZOS).save(
        f"assets/img/{name}.png", optimize=True)
    px = v["stroke"] * scale / SS
    print(f"assets/img/{name}.png  {OUT}x{OUT}  stroke {px:.0f}px @1080 "
          f"= {px * 44 / OUT:.2f}px @44")
