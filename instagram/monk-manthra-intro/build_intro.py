"""
monk manthra — brand introduction carousel. Posted before the ingredient
carousels, so it has to do the job those can't: say who the brand is, not
just what's in the scoop.

Six slides, built from copy already live on the site (story.html, the
footer, the Shopify homepage subheading) rather than invented — this is
the one carousel where tone matters more than any single fact, so it
leans on lines that were already signed off.

  1. Cover      — the mark, drawn full, plus the line from the bio/footer.
  2. Contrast   — the category's noise vs. the brand's actual position.
  3. Who it's for — story.html's "Who" section, near-verbatim.
  4. How it's dosed — story.html's "How" section: visible dose, honest week one.
  5. What's live — the real state of the range right now (Golden Milk only).
  6. CTA        — mark again, close on the one thing you can actually buy.

Same rendering approach as the ingredient carousels: real HTML/CSS with
the site's own tokens and fonts, shot to 1080x1080 PNG with headless
Chrome — pixel-identical to the browser, not a redraw.

Usage:
    python3 build_intro.py
Output:
    png/slide-1-cover.png ... png/slide-6-cta.png
"""
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "_build")
PNG = os.path.join(HERE, "png")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

MARK = """<svg class="mark" viewBox="0 0 100 100" role="img" aria-label="monk manthra" focusable="false">
  <path class="ring ring--1" d="M 54.788 36.844 A 14.0 14.0 0 1 1 45.212 36.844"/>
  <path class="ring ring--2" d="M 57.661 28.951 A 22.4 22.4 0 1 1 42.339 28.951"/>
  <path class="ring ring--3" d="M 62.258 16.321 A 35.84 35.84 0 1 1 37.742 16.321"/>
  <circle class="seed" cx="50" cy="50" r="5.2"/>
</svg>"""

CSS = """
:root {
  --deep-purple: #3A1F5C; --royal-purple: #7A5CA8; --pale-lilac: #CBBFE0;
  --gold: #C2A053; --light-gold: #E0C88C; --half-white: #F4F1EC;
  --ink: #241B33; --paper: #FFFFFF;
  --display: "Fraunces", serif; --body: "Karla", sans-serif; --mono: "IBM Plex Mono", monospace;
}
* { box-sizing: border-box; }
html, body { margin: 0; width: 1080px; height: 1080px; }
body { font-family: var(--body); font-weight: 300; -webkit-font-smoothing: antialiased; }
.slide { width: 1080px; height: 1080px; padding: 88px; display: flex; flex-direction: column; }
.label { font-family: var(--body); font-weight: 500; font-size: 20px; letter-spacing: 0.2em; text-transform: uppercase; margin: 0; }
.gold-rule { width: 56px; height: 3px; background: var(--gold); border: 0; margin: 30px 0; }
.mark { display: block; }
.mark .ring { fill: none; stroke-linecap: round; stroke-width: 2.2; }

/* purple ground */
.on-purple { background: var(--deep-purple); color: var(--half-white); }
.on-purple .label { color: var(--light-gold); }
.on-purple .mark .ring--1 { stroke: var(--half-white); }
.on-purple .mark .ring--2 { stroke: var(--pale-lilac); }
.on-purple .mark .ring--3 { stroke: var(--light-gold); }
.on-purple .mark .seed { fill: var(--light-gold); }
.on-purple .wordmark { color: var(--half-white); }

/* paper ground */
.on-paper { background: var(--half-white); color: var(--deep-purple); }
.on-paper .label { color: var(--royal-purple); }
.on-paper .mark .ring--1 { stroke: var(--deep-purple); }
.on-paper .mark .ring--2 { stroke: var(--royal-purple); }
.on-paper .mark .ring--3 { stroke: var(--gold); }
.on-paper .mark .seed { fill: var(--gold); }

.wordmark { font-family: var(--display); font-weight: 200; text-transform: lowercase; letter-spacing: 0.15em; }

/* ---- slide 1 · cover ---- */
/* Editorial, not centred-and-stacked: the ring motif blown up huge and
   bled off the top-right corner gives the frame depth the small centred
   mark couldn't, and the copy sits left, asymmetric, like a poster. */
.s-cover { position: relative; overflow: hidden; justify-content: space-between; }
.s-cover .bleed-ring {
  position: absolute; top: -420px; right: -420px; width: 900px; height: 900px;
  border-radius: 50%; border: 1.5px solid rgba(224,200,140,0.16);
  pointer-events: none;
}
.s-cover .bleed-ring--2 {
  position: absolute; top: -270px; right: -270px; width: 580px; height: 580px;
  border-radius: 50%; border: 1.5px solid rgba(203,191,224,0.14);
  pointer-events: none;
}
.s-cover .mid { flex: 1; display: flex; flex-direction: column; justify-content: center; position: relative; z-index: 1; }
.s-cover .mark { width: 92px; height: 92px; margin-bottom: 48px; }
.s-cover .mark .ring { stroke-width: 2; }
.s-cover .eyebrow { font-family: var(--body); font-weight: 500; font-size: 20px; letter-spacing: 0.24em; text-transform: uppercase; color: var(--light-gold); margin: 0 0 22px; }
.s-cover .wordmark { font-size: 108px; line-height: 0.98; margin: 0; }
.s-cover .mantra { font-family: var(--display); font-weight: 300; font-style: italic; font-size: 30px; line-height: 1.5; color: var(--pale-lilac); max-width: 15ch; margin: 40px 0 0; }
.s-cover .tagline { font-family: var(--body); font-weight: 300; font-size: 24px; line-height: 1.6; color: rgba(244,241,236,0.72); max-width: 26ch; margin: 26px 0 0; }

/* ---- slide 2 · contrast (pain vs. position) ---- */
.s-contrast .mid { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.s-contrast .noise { font-family: var(--display); font-weight: 300; font-style: italic; font-size: 42px; line-height: 1.32; color: var(--pale-lilac); max-width: 17ch; margin: 0 0 40px; text-decoration: line-through; text-decoration-color: rgba(224,200,140,0.55); text-decoration-thickness: 2px; }
.s-contrast .position { font-family: var(--display); font-weight: 200; font-size: 66px; line-height: 1.14; letter-spacing: -0.015em; margin: 0; max-width: 15ch; }

/* ---- slide 3 & 4 · statement on paper ---- */
.s-statement .mid { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.s-statement h2 { font-family: var(--display); font-weight: 300; font-size: 54px; line-height: 1.16; letter-spacing: -0.015em; margin: 0 0 34px; max-width: 14ch; }
.s-statement p { font-family: var(--body); font-weight: 300; font-size: 32px; line-height: 1.62; margin: 0; max-width: 25ch; color: var(--ink); }

/* ---- slide 5 · one formula at a time (no product names) ---- */
.s-range .mid { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.s-range h2 { font-family: var(--display); font-weight: 300; font-size: 52px; line-height: 1.18; letter-spacing: -0.015em; margin: 0 0 34px; max-width: 16ch; }
.s-range p { font-family: var(--body); font-weight: 300; font-size: 32px; line-height: 1.62; color: var(--ink); max-width: 25ch; margin: 0; }

/* ---- slide 6 · cta ---- */
.s-cta { align-items: center; text-align: center; justify-content: center; }
.s-cta .mid { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.s-cta .mark { width: 96px; height: 96px; margin-bottom: 36px; }
.s-cta h2 { font-family: var(--display); font-weight: 200; font-size: 62px; line-height: 1.16; margin: 0; max-width: 15ch; }
"""

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,200;0,9..144,300;1,9..144,300;9..144,400&family=Karla:wght@300;400;500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{css}</style></head><body>"""

def slide1_cover():
    body = f"""
<div class="slide s-cover on-purple">
  <span class="bleed-ring"></span>
  <span class="bleed-ring--2"></span>
  <div class="mid">
    {MARK}
    <p class="eyebrow">Nutrition</p>
    <h1 class="wordmark">monk<br>manthra</h1>
    <hr class="gold-rule">
    <p class="mantra">A manthra is one word, repeated, until it changes something.</p>
    <p class="tagline">Daily supplements for people who want to feel steady, not supercharged.</p>
  </div>
</div>"""
    return HEAD.format(css=CSS) + body + "</body></html>"


def slide2_contrast():
    body = f"""
<div class="slide s-contrast on-purple">
  <p class="label">The category</p>
  <div class="mid">
    <p class="noise">Energy. Focus. Sleep. Calm. All at once. Forever.</p>
    <h1 class="position">We sell consistency, not transformation.</h1>
  </div>
</div>"""
    return HEAD.format(css=CSS) + body + "</body></html>"


def slide3_who():
    body = f"""
<div class="slide s-statement on-paper">
  <p class="label">Who this is for</p>
  <div class="mid">
    <h2>People who read the panel before the pack.</h2>
    <p>Suspicious of hype, and of anything that looks like a pharmacy. Already have a practice of some kind — yoga, running, therapy, cooking. This is the supplement version of that.</p>
  </div>
</div>"""
    return HEAD.format(css=CSS) + body + "</body></html>"


def slide4_how():
    body = f"""
<div class="slide s-statement on-purple">
  <p class="label">How it's dosed</p>
  <div class="mid">
    <h2 style="color:var(--half-white)">Repetition over intensity.</h2>
    <p style="color:rgba(244,241,236,0.82)">The dose stays visible, never hidden. And the honest number, including the unglamorous one — the first week usually feels like nothing at all.</p>
  </div>
</div>"""
    return HEAD.format(css=CSS) + body + "</body></html>"


def slide5_range():
    body = f"""
<div class="slide s-range on-paper">
  <p class="label">The range, honestly</p>
  <div class="mid">
    <h2>One formula at a time.</h2>
    <p>We don't launch everything at once. One is live, and each new one waits until it's actually ready — not before.</p>
  </div>
</div>"""
    return HEAD.format(css=CSS) + body + "</body></html>"


def slide6_cta():
    body = f"""
<div class="slide s-cta on-purple">
  <div class="mid">
    {MARK}
    <h2>Start with the one that's ready.</h2>
  </div>
</div>"""
    return HEAD.format(css=CSS) + body + "</body></html>"


SLIDES = [
    ("slide-1-cover", slide1_cover),
    ("slide-2-contrast", slide2_contrast),
    ("slide-3-who", slide3_who),
    ("slide-4-how", slide4_how),
    ("slide-5-range", slide5_range),
    ("slide-6-cta", slide6_cta),
]


def render(html_path, png_path):
    subprocess.run([
        CHROME, "--headless", "--disable-gpu",
        "--virtual-time-budget=4000",
        f"--screenshot={png_path}",
        "--window-size=1080,1080",
        f"file://{html_path}",
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    if os.path.exists(BUILD):
        shutil.rmtree(BUILD)
    if os.path.exists(PNG):
        shutil.rmtree(PNG)
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(PNG, exist_ok=True)

    for name, fn in SLIDES:
        html_path = os.path.join(BUILD, f"{name}.html")
        png_path = os.path.join(PNG, f"{name}.png")
        with open(html_path, "w") as f:
            f.write(fn())
        render(html_path, png_path)
        print(f"{name}  done")


if __name__ == "__main__":
    main()
