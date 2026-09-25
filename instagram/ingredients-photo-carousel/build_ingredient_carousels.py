"""
Ingredient carousels — photographic style, one 2-slide carousel per
ingredient, 14 total. Same visual system as ../golden-milk-photo-carousel/
(turmeric powder meeting milk, bold centered-bottom headline, corner
mark, watermark patch) — reuses the same 6 locked photos from that
folder, cycled round-robin. Six strong shots beat fourteen mediocre
ones — see FLOW-PROMPTS-V2.md if you want to regenerate those 6 with a
more editorial look; it overwrites the shared photos/ folder so every
carousel that reads off it improves at once.

"Golden Milk" (the product name) is never mentioned anywhere in this
carousel set, by request — copy refers to "the scoop" / "the blend"
generically instead. No per-ingredient dosage either (still unconfirmed
— see products/golden-milk.html).

Slide 1 (photo)    — pain point as the bold headline, ingredient name as
                      the gold reveal underneath. Corner mark, top-left.
Slide 2 (gradient) — mark + wordmark signature, "Why it's here", the
                      rationale paragraph. No photo needed.

Usage:
    python3 build_ingredient_carousels.py
Output:
    png/01-turmeric-extract/slide-1-hook.png
    png/01-turmeric-extract/slide-2-why.png
    ... etc, 14 folders
"""
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "_build")
PNG = os.path.join(HERE, "png")
PHOTOS = os.path.join(HERE, "..", "golden-milk-photo-carousel", "photos")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def bold(text):
    if text is None:
        return None
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


MARK = """<svg class="mark" viewBox="0 0 100 100" role="img" aria-label="monk manthra" focusable="false">
  <path class="ring ring--1" d="M 54.788 36.844 A 14.0 14.0 0 1 1 45.212 36.844"/>
  <path class="ring ring--2" d="M 57.661 28.951 A 22.4 22.4 0 1 1 42.339 28.951"/>
  <path class="ring ring--3" d="M 62.258 16.321 A 35.84 35.84 0 1 1 37.742 16.321"/>
  <circle class="seed" cx="50" cy="50" r="5.2"/>
</svg>"""

CSS = """
:root {
  --deep-purple: #3A1F5C; --royal-purple: #7A5CA8; --pale-lilac: #CBBFE0;
  --gold: #C2A053; --light-gold: #E0C88C; --half-white: #F4F1EC; --ink: #241B33;
  --display: "Fraunces", serif; --body: "Karla", sans-serif;
}
* { box-sizing: border-box; }
html, body { margin: 0; width: 1080px; height: 1080px; }
body { font-family: var(--body); }

/* ---- slide 1: split panel — clean solid ground on top, photo inset
   below. This is the reference's "collage" slide type: bold dark text
   directly on a plain light ground reads cleaner than white text over a
   photo, so the headline lives off the image entirely. ---- */
.split-slide {
  width: 1080px; height: 1080px; display: flex; flex-direction: column;
  background: var(--half-white);
}
.split-slide .panel-text {
  height: 428px; flex: none; padding: 72px 84px 0;
  display: flex; flex-direction: column; position: relative;
}
.split-slide .panel-photo {
  flex: 1; position: relative; overflow: hidden;
}
.split-slide .panel-photo img {
  width: 100%; height: 100%; object-fit: cover; object-position: center;
  display: block;
}
/* The Flow/Gemini watermark sits bottom-right of every generated photo */
.split-slide .corner-patch {
  position: absolute; right: 0; bottom: 0; width: 220px; height: 190px;
  background: radial-gradient(circle at 100% 100%, rgba(20,14,30,1) 0%, rgba(20,14,30,0.9) 40%, rgba(20,14,30,0) 78%);
}
.split-slide .corner-mark { position: absolute; top: 40px; right: 40px; }
.split-slide .corner-mark .mark { width: 40px; height: 40px; display: block; }
.split-slide .corner-mark .mark .ring { fill: none; stroke-linecap: round; stroke-width: 2.6; }
.split-slide .corner-mark .mark .ring--1 { stroke: var(--deep-purple); }
.split-slide .corner-mark .mark .ring--2 { stroke: var(--royal-purple); }
.split-slide .corner-mark .mark .ring--3 { stroke: var(--gold); }
.split-slide .corner-mark .mark .seed { fill: var(--gold); }
.split-slide .label {
  font-family: var(--body); font-weight: 700; font-size: 19px; letter-spacing: 0.22em;
  text-transform: uppercase; color: var(--royal-purple); margin: 0 0 22px;
}
.split-slide h1 {
  font-family: var(--body); font-weight: 800; font-size: 54px;
  line-height: 1.2; letter-spacing: -0.015em; color: var(--ink); margin: 0;
  max-width: 15ch;
}
.split-slide h1 strong { color: var(--royal-purple); }

/* ---- slide 2: gradient + why ---- */
.why-slide {
  width: 1080px; height: 1080px; position: relative;
  background: radial-gradient(circle at 50% 40%, #4A2A73 0%, #3A1F5C 45%, #2A1B45 100%);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 0 120px;
}
.why-slide .mark { width: 52px; height: 52px; margin-bottom: 28px; }
.why-slide .mark .ring { fill: none; stroke-linecap: round; stroke-width: 2.2; }
.why-slide .mark .ring--1 { stroke: var(--half-white); }
.why-slide .mark .ring--2 { stroke: var(--pale-lilac); }
.why-slide .mark .ring--3 { stroke: var(--light-gold); }
.why-slide .mark .seed { fill: var(--light-gold); }
.why-slide .label {
  font-family: var(--body); font-weight: 700; font-size: 20px; letter-spacing: 0.26em;
  text-transform: uppercase; color: var(--light-gold); margin: 0 0 30px;
}
.why-slide h2 {
  font-family: var(--display); font-weight: 300; font-size: 46px; line-height: 1.2;
  color: var(--half-white); margin: 0 0 28px; text-align: center; max-width: 15ch;
}
.why-slide p {
  font-family: var(--body); font-weight: 300; font-size: 27px; line-height: 1.65;
  color: rgba(244,241,236,0.88); text-align: center; max-width: 30ch; margin: 0;
}
"""

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,200;9..144,300;9..144,400&family=Karla:wght@300;400;500;700;800&display=swap">
<style>{css}</style></head><body>"""

# name, pain-point hook, why-body — no "Golden Milk", no dosage.
INGREDIENTS = [
    ("Turmeric",
     "Restless nights, and nothing in the evening routine built for it.",
     "Turmeric isn't a sleep aid by itself — that's not what curcumin does. But it's part of why the ritual is worth keeping: known to contribute to the normal function of joints, support the body's normal antioxidant processes, and support normal digestive comfort. We use an extract standardised for curcuminoids, paired with black pepper — turmeric barely absorbs without it. Structure-and-function statements, not medical claims."),
    ("Monk Fruit Extract",
     "Wanting something sweet without paying for it at 2am.",
     "A fruit extract sweetener stands in for sugar, so an evening scoop doesn't end in a spike right before bed. No added sugar. No artificial sweetener either."),
    ("Natural Vanilla",
     "A supplement that tastes like one.",
     "Vanilla rounds off the spice and the sweetener so the cup tastes finished — closer to dessert than to medicine."),
    ("Pumpkin Powder",
     "The fibre nobody plans for and everybody needs.",
     "Pumpkin powder adds body and a mild natural sweetness, and brings its own fibre along with it. Whole food, not an extract."),
    ("Black Pepper Extract",
     "Taking turmeric every day and absorbing almost none of it.",
     "Turmeric is poorly absorbed on its own. Piperine from black pepper is the standard way to help the body take up the curcumin — which is why it's here at all."),
    ("Cinnamon Extract",
     "The spice everyone assumes is already in there.",
     "Cinnamon is what makes this taste like a ritual, not a spice rub. An extract keeps the flavour without a large raw-powder dose."),
    ("Nutmeg Extract",
     "A blend that tastes almost right, but not quite.",
     "A touch of nutmeg rounds out the turmeric-cinnamon base — the extra note that makes it taste finished."),
    ("Taurine",
     "Running on empty by 9pm and still wired.",
     "One of the most-studied amino acids for everyday calm, included as a standard part of the blend — not as a trend ingredient."),
    ("MCT Powder",
     "Wanting it creamy without reaching for dairy.",
     "MCT powder gives the drink a creamy body even without dairy, and helps carry curcumin, which is fat-soluble and needs something to travel with."),
    ("Glycine",
     "Tired all day, then lying there wide awake.",
     "Glycine is the amino acid most associated with winding down before sleep — taken in the evening, on purpose, for exactly this reason."),
    ("Magnesium Glycinate",
     "Wired all day. Wide awake at night.",
     "A well-absorbed, gentle-on-the-stomach form of magnesium, bound to glycine so one ingredient does two jobs in the same scoop."),
    ("Lutein",
     "Eyes worn out before the day is.",
     "Lutein is a carotenoid the eye already stores for itself — usually found in greens, and just as often skipped."),
    ("Zeaxanthin",
     "Screens all day, and nothing done about it.",
     "Zeaxanthin works alongside lutein in the same eye tissue. The two are almost always dosed together for a reason — this scoop doesn't split them up."),
    ("Fiber",
     "The gram of fibre most days quietly skip.",
     "A little fibre in a drink you're already taking daily. No claim needed — no reason not to."),
]


def render(html_path, png_path):
    subprocess.run([
        CHROME, "--headless", "--disable-gpu",
        "--virtual-time-budget=4000",
        f"--screenshot={png_path}",
        "--window-size=1080,1080",
        f"file://{html_path}",
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def slide1_hook(name, pain, photo_path):
    return HEAD.format(css=CSS) + f"""
<div class="split-slide">
  <div class="panel-text">
    <p class="label">{name}</p>
    <h1>{bold(pain)}</h1>
  </div>
  <div class="panel-photo">
    <img src="file://{photo_path}">
    <span class="corner-patch"></span>
    <div class="corner-mark">{MARK}</div>
  </div>
</div></body></html>"""


def slide2_why(name, why_body):
    return HEAD.format(css=CSS) + f"""
<div class="why-slide">
  {MARK}
  <p class="label">{name}</p>
  <h2>Why it's here</h2>
  <p>{bold(why_body)}</p>
</div></body></html>"""


def main():
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(PNG, exist_ok=True)
    for idx, (name, pain, why_body) in enumerate(INGREDIENTS, start=1):
        slug = name.lower().replace(" ", "-").replace("'", "")
        folder = f"{idx:02d}-{slug}"
        html_dir = os.path.join(BUILD, folder)
        png_dir = os.path.join(PNG, folder)
        os.makedirs(html_dir, exist_ok=True)
        os.makedirs(png_dir, exist_ok=True)

        photo_num = ((idx - 1) % 6) + 1
        photo_path = os.path.abspath(os.path.join(PHOTOS, f"slide-{photo_num}.jpg"))

        slides = [
            ("slide-1-hook.html", "slide-1-hook.png", slide1_hook(name, pain, photo_path)),
            ("slide-2-why.html", "slide-2-why.png", slide2_why(name, why_body)),
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
