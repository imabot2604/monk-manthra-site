"""
Golden Milk ingredient carousels — one carousel per ingredient, two slides
each, built straight from the site's own tokens (assets/css/site.css) so
they read as the same brand, not a spin-off style.

Slide 1 (deep purple) — the pain point pinned as the headline, the
                         ingredient name as the reveal underneath.
Slide 2 (half white)  — why it's actually in the scoop, in the site's own
                         plain-spoken copy voice.

No per-ingredient amounts — the real dosage isn't confirmed yet, so these
carousels are ingredients-only. Add a dose slide back in once the facts
panel on products/golden-milk.html has real numbers.

Ginger Extract has been removed from the formula — 14 ingredients now, not
15. See products/golden-milk.html for the same change on the site.

Renders each slide to a real 1080x1080 PNG with headless Chrome, so what
you get is pixel-identical to what the browser draws — same fonts, same
colour, same rules as the rest of the site.

Usage:
    python3 build_carousels.py
Output:
    png/01-turmeric-extract/slide-1-cover.png (etc.)
"""
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "_build")
PNG = os.path.join(HERE, "png")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BASE_CSS = """
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

/* ---- cover slide: pain point is the headline, ingredient is the reveal ---- */
.slide--cover { background: var(--deep-purple); color: var(--half-white); justify-content: space-between; }
.slide--cover .label { color: var(--light-gold); }
.slide--cover .cover__mid { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.slide--cover h1.pain { font-family: var(--display); font-weight: 200; font-size: 84px; line-height: 1.08; letter-spacing: -0.02em; margin: 0; max-width: 15ch; }
.slide--cover .reveal { display: flex; align-items: center; gap: 18px; margin-top: 44px; }
.slide--cover .reveal .rule { width: 34px; height: 2px; background: var(--gold); flex: none; }
.slide--cover .reveal .ing-name { font-family: var(--body); font-weight: 500; font-size: 28px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--light-gold); }
.slide--cover .foot { display: flex; align-items: center; justify-content: space-between; }
.slide--cover .foot .wordmark { font-family: var(--display); font-weight: 200; text-transform: lowercase; letter-spacing: 0.15em; font-size: 28px; color: var(--half-white); }
.slide--cover .dots { display: flex; gap: 10px; }
.slide--cover .dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(244,241,236,0.28); }
.slide--cover .dot.is-on { background: var(--light-gold); }

/* ---- why slide ---- */
.slide--why { background: var(--half-white); color: var(--deep-purple); }
.slide--why .label { color: var(--royal-purple); }
.slide--why .why__mid { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.slide--why h2 { font-family: var(--display); font-weight: 300; font-size: 56px; line-height: 1.14; letter-spacing: -0.015em; margin: 0 0 36px; max-width: 15ch; }
.slide--why p { font-family: var(--body); font-weight: 300; font-size: 34px; line-height: 1.6; margin: 0; max-width: 26ch; color: var(--ink); }
.slide--why .foot { display: flex; align-items: center; justify-content: space-between; }
.slide--why .foot .data { font-family: var(--mono); font-size: 20px; color: var(--royal-purple); }
.slide--why .dots { display: flex; gap: 10px; }
.slide--why .dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(122,92,168,.28); }
.slide--why .dot.is-on { background: var(--gold); }
"""

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,200;9..144,300;9..144,400&family=Karla:wght@300;400;500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{css}</style></head><body>"""

TAGLINE = "GOLDEN MILK &middot; TURMERIC &middot; CINNAMON"

# name, pain-point hook, why-heading, why-body — no amounts, dosage TBC.
# Ginger Extract removed from the formula (was slot 2 in the original 15).
INGREDIENTS = [
    ("Turmeric Extract",
     "The joints that complain before the weather even changes.",
     "Why it's here",
     "Turmeric is why golden milk is golden. We use an extract standardised for curcuminoids instead of raw powder, and pair it with black pepper — turmeric is poorly absorbed alone."),
    ("Monk Fruit Extract",
     "Wanting something sweet without paying for it at 2am.",
     "Why it's here",
     "A fruit extract sweetener stands in for sugar, so a drink meant for the evening doesn't end in a spike right before bed. No added sugar, no artificial sweetener either."),
    ("Natural Vanilla",
     "A supplement that tastes like one.",
     "Why it's here",
     "Vanilla rounds off the spice and the sweetener so the cup tastes finished — closer to dessert than to medicine."),
    ("Pumpkin Powder",
     "The fibre nobody plans for and everybody needs.",
     "Why it's here",
     "Pumpkin powder adds body and a mild natural sweetness to the blend, and brings its own fibre and nutrients along with it. Whole food, not an extract."),
    ("Black Pepper Extract",
     "Taking turmeric every day and absorbing almost none of it.",
     "Why it's here",
     "Turmeric is poorly absorbed on its own. Piperine from black pepper is the standard way to help the body actually take up the curcumin — which is why it's in here at all."),
    ("Cinnamon Extract",
     "The spice everyone assumes is already in there.",
     "Why it's here",
     "Cinnamon is one of the ingredients golden milk is named for. An extract keeps the flavour without needing a large raw-powder dose."),
    ("Nutmeg Extract",
     "A blend that tastes almost right, but not quite.",
     "Why it's here",
     "A touch of nutmeg rounds out the turmeric-cinnamon base — the extra spice that makes it taste like the drink people already know."),
    ("Taurine",
     "Running on empty by 9pm and still wired.",
     "Why it's here",
     "Taurine is one of the most-studied amino acids for everyday calm — included as a standard part of the blend, not as a trend ingredient."),
    ("MCT Powder",
     "Wanting it creamy without reaching for dairy.",
     "Why it's here",
     "MCT powder gives the drink a creamy body even without dairy, and helps carry curcumin, which is fat-soluble and needs something to travel with."),
    ("Glycine",
     "Tired all day, then lying there wide awake.",
     "Why it's here",
     "Glycine is the amino acid most associated with winding down before sleep — taken in the evening, on purpose, for exactly this reason."),
    ("Magnesium Glycinate",
     "Wired all day. Wide awake at night.",
     "Why it's here",
     "A well-absorbed, gentle-on-the-stomach form of magnesium, bound to glycine so one ingredient does two jobs in the same scoop."),
    ("Lutein",
     "Eyes worn out before the day is.",
     "Why it's here",
     "Lutein is a carotenoid the eye already stores for itself — usually found in greens, and just as often skipped."),
    ("Zeaxanthin",
     "Screens all day, and nothing done about it.",
     "Why it's here",
     "Zeaxanthin works alongside lutein in the same eye tissue. The two are almost always dosed together for a reason, and this scoop doesn't split them up."),
    ("Fiber",
     "The gram of fibre most days quietly skip.",
     "Why it's here",
     "A little fibre in a drink you're already taking daily. No claim needed — no reason not to."),
]

TOTAL = len(INGREDIENTS)


def slide_cover(i, name, pain):
    return HEAD.format(css=BASE_CSS) + f"""
<div class="slide slide--cover on-purple">
  <p class="label">Golden Milk &middot; Ingredient {i:02d} / {TOTAL}</p>
  <div class="cover__mid">
    <h1 class="pain">{pain}</h1>
    <div class="reveal"><span class="rule"></span><span class="ing-name">{name}</span></div>
  </div>
  <div class="foot">
    <span class="wordmark">monk manthra</span>
    <div class="dots"><span class="dot is-on"></span><span class="dot"></span></div>
  </div>
</div></body></html>"""


def slide_why(i, name, heading, body):
    return HEAD.format(css=BASE_CSS) + f"""
<div class="slide slide--why">
  <p class="label">{name}</p>
  <div class="why__mid">
    <h2>{heading}</h2>
    <p>{body}</p>
  </div>
  <div class="foot">
    <span class="data">{TAGLINE}</span>
    <div class="dots"><span class="dot"></span><span class="dot is-on"></span></div>
  </div>
</div></body></html>"""


def render(html_path, png_path):
    subprocess.run([
        CHROME, "--headless", "--disable-gpu",
        "--virtual-time-budget=4000",
        f"--screenshot={png_path}",
        "--window-size=1080,1080",
        f"file://{html_path}",
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    # Full rebuild: ingredient count and numbering changed (ginger removed),
    # so stale folders (old 02-ginger-extract, old numbering past it) must go.
    if os.path.exists(BUILD):
        shutil.rmtree(BUILD)
    if os.path.exists(PNG):
        shutil.rmtree(PNG)
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(PNG, exist_ok=True)

    for idx, (name, pain, heading, body) in enumerate(INGREDIENTS, start=1):
        slug = name.lower().replace(" ", "-").replace("'", "")
        folder = f"{idx:02d}-{slug}"
        html_dir = os.path.join(BUILD, folder)
        png_dir = os.path.join(PNG, folder)
        os.makedirs(html_dir, exist_ok=True)
        os.makedirs(png_dir, exist_ok=True)

        slides = [
            ("slide-1-cover.html", "slide-1-cover.png", slide_cover(idx, name, pain)),
            ("slide-2-why.html", "slide-2-why.png", slide_why(idx, name, heading, body)),
        ]
        for html_name, png_name, html in slides:
            html_path = os.path.join(html_dir, html_name)
            png_path = os.path.join(png_dir, png_name)
            with open(html_path, "w") as f:
                f.write(html)
            render(html_path, png_path)
        print(f"{folder}  done")


if __name__ == "__main__":
    main()
