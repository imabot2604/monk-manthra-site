"""
monk manthra — photo carousel (v2, centered).

Slides 1-6 are photographs generated in Google Flow from FLOW-PROMPTS.md
(turmeric powder meeting milk, no packets, no hands/models per the
existing brand rule), with centered headline text composited on top here
once the photos exist at photos/slide-N.jpg.

Slide 7 needs no photo — pure gradient card, built now.

Usage:
    python3 build_photo_carousel.py          # builds whatever inputs exist
Output:
    png/slide-7-closer.png always
    png/slide-N-*.png once photos/slide-N.jpg is dropped in
"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "_build")
PNG = os.path.join(HERE, "png")
PHOTOS = os.path.join(HERE, "photos")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
:root {
  --deep-purple: #3A1F5C; --royal-purple: #7A5CA8; --pale-lilac: #CBBFE0;
  --gold: #C2A053; --light-gold: #E0C88C; --half-white: #F4F1EC;
  --display: "Fraunces", serif; --body: "Karla", sans-serif;
}
* { box-sizing: border-box; }
html, body { margin: 0; width: 1080px; height: 1080px; }
body { font-family: var(--body); }

/* ---- photo slide: full-bleed image + centered headline ---- */
.photo-slide {
  width: 1080px; height: 1080px; position: relative;
  display: flex; align-items: center; justify-content: center;
  background-size: cover; background-position: center;
}
.photo-slide::before {
  content: ""; position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(36,27,51,0.15) 0%, rgba(36,27,51,0.55) 100%);
}
.photo-slide .copy {
  position: relative; z-index: 1; text-align: center; padding: 0 100px;
}
.photo-slide h1 {
  font-family: var(--display); font-weight: 300; font-size: 54px;
  line-height: 1.28; color: var(--half-white); margin: 0;
  text-shadow: 0 2px 24px rgba(0,0,0,0.35);
}
.photo-slide .heading-kicker {
  font-family: var(--body); font-weight: 500; font-size: 20px;
  letter-spacing: 0.2em; text-transform: uppercase; color: var(--light-gold);
  margin: 0 0 22px;
}
.photo-slide .sub {
  font-family: var(--body); font-weight: 300; font-size: 26px; line-height: 1.6;
  color: rgba(244,241,236,0.88); max-width: 32ch; margin: 24px auto 0;
  text-shadow: 0 2px 16px rgba(0,0,0,0.4);
}

/* ---- slide 7: pure gradient, centered mantra ---- */
.gradient-slide {
  width: 1080px; height: 1080px;
  background: radial-gradient(circle at 50% 45%, #4A2A73 0%, #3A1F5C 45%, #7A5230 130%);
  display: flex; align-items: center; justify-content: center;
}
.gradient-slide .copy { text-align: center; width: 760px; }
.gradient-slide p {
  font-family: var(--display); font-weight: 300; font-style: italic;
  font-size: 44px; line-height: 1.85; color: var(--half-white); margin: 0;
  white-space: pre-line;
}
"""

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,200;0,9..144,300;1,9..144,300;9..144,400&family=Karla:wght@300;400;500&display=swap">
<style>{css}</style></head><body>"""

PHOTO_SLIDES = [
    (1, "slide-1-splash", None, "Turmeric deserves the credit. It just can't do the job alone.", None),
    (2, "slide-2-swirl", "Why turmeric alone usually falls short", None,
     "Curcumin is poorly absorbed by the body on its own. Most of a raw dose passes straight through. Heat and fat change how much actually gets used."),
    (3, "slide-3-pour", None, "Which is why golden milk was never just turmeric.", None),
    (4, "slide-4-marble", None, "But a ritual only works if you trust what's in the cup.",
     "The rest of the formula isn't there for colour. It's there to help the body actually use what you just drank."),
    (5, "slide-5-lifted", None, "So the formula isn't a secret. It's a list.", None),
    (6, "slide-6-mixed", None, "Every ingredient earns its place, or it doesn't make the scoop.", None),
]


def render(html_path, png_path):
    subprocess.run([
        CHROME, "--headless", "--disable-gpu",
        "--virtual-time-budget=4000",
        f"--screenshot={png_path}",
        "--window-size=1080,1080",
        f"file://{html_path}",
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build_photo_slide(idx, slug, kicker, headline, sub):
    photo_path = os.path.join(PHOTOS, f"slide-{idx}.jpg")
    if not os.path.exists(photo_path):
        print(f"skip slide {idx} ({slug}) — photos/slide-{idx}.jpg not found yet")
        return
    kicker_html = f'<p class="heading-kicker">{kicker}</p>' if kicker else ""
    sub_html = f'<p class="sub">{sub}</p>' if sub else ""
    body = f"""
<div class="photo-slide" style="background-image:url('file://{photo_path}')">
  <div class="copy">
    {kicker_html}
    <h1>{headline}</h1>
    {sub_html}
  </div>
</div>"""
    html = HEAD.format(css=CSS) + body + "</body></html>"
    html_path = os.path.join(BUILD, f"slide-{idx}-{slug}.html")
    png_path = os.path.join(PNG, f"slide-{idx}-{slug}.png")
    with open(html_path, "w") as f:
        f.write(html)
    render(html_path, png_path)
    print(f"slide-{idx}-{slug}  done")


def build_gradient_slide():
    body = """
<div class="gradient-slide">
  <div class="copy">
    <p>Nothing added for the label.<br>Nothing hidden from the panel.<br>That's the whole idea.</p>
  </div>
</div>"""
    html = HEAD.format(css=CSS) + body + "</body></html>"
    html_path = os.path.join(BUILD, "slide-7-closer.html")
    png_path = os.path.join(PNG, "slide-7-closer.png")
    with open(html_path, "w") as f:
        f.write(html)
    render(html_path, png_path)
    print("slide-7-closer  done")


def main():
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(PNG, exist_ok=True)
    os.makedirs(PHOTOS, exist_ok=True)
    for idx, slug, kicker, headline, sub in PHOTO_SLIDES:
        build_photo_slide(idx, slug, kicker, headline, sub)
    build_gradient_slide()


if __name__ == "__main__":
    main()
