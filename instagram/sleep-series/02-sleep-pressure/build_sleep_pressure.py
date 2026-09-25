"""
monk manthra carousel template — copy this file into a new carousel's
own folder (e.g. instagram/<topic>/build_<topic>.py) and edit the
SLIDES list at the bottom. It contains all five slide types used across
every carousel built for this brand, so a new one is composition, not
invention.

Rendering approach: each slide's full HTML+CSS is written to a temp
file and shot with headless Chrome at exactly 1080x1080. This is not
a screenshot-of-a-live-page hack — it's the actual rendering pipeline,
chosen because it reuses real CSS (the same custom properties as
assets/css/site.css) instead of hand-placing text with a library like
Pillow, and because Chrome handles the web fonts, flexbox centering,
and text wrapping correctly without extra math.

    /Applications/Google Chrome.app/Contents/MacOS/Google Chrome \\
        --headless --disable-gpu --virtual-time-budget=4000 \\
        --screenshot=<out.png> --window-size=1080,1080 file://<in.html>

--virtual-time-budget=4000 matters: Karla/Fraunces load from Google
Fonts over the network, and dropping this (or setting it too low) will
occasionally screenshot before the web font swaps in, silently falling
back to a system serif/sans. If you ever see slightly-off type in a
render, suspect this first before touching layout CSS.

THE FIVE SLIDE TYPES

  photo_slide   Full-bleed photo, dark bottom scrim, bold white headline
                (Karla 700-800) anchored near the bottom, optional sub
                paragraph or bullet list. Use for dramatic/emotional
                beats — hooks, single strong statements.

  split_slide   Clean half-white top panel (bold dark headline + small
                uppercase label) over a bottom photo panel. Use for
                slides that need to read as "editorial" rather than
                "poster" — a claim stated plainly next to its evidence.

  info_slide    Half-white background, no photo — a small line-icon
                (sun/eye/moon/clock-style SVGs included below; draw your
                own in the same thin-stroke currentColor style for a new
                concept) plus a mixed-weight headline (thin Fraunces
                serif spans next to bold Karla spans in the *same*
                heading — this is what gives the "science-explainer"
                look, not two separate text blocks) and a bulleted
                mechanism explanation with bold key terms. Use when
                there's no natural photo for the idea (a mechanism, a
                fact, an abstract concept).

  cover_slide   The fully-centered version of info_slide — label, icon,
                big centered headline, one sub line, wordmark. Reserve
                this for slide 1 specifically: Instagram's profile grid
                shows posts as small square thumbnails, and a
                top-anchored layout with a lot of empty space (which is
                what info_slide looks like used as a cover) reads as
                blank at that size. Centered + big does not.

  gradient_slide  Deep-purple-to-warm-gold radial gradient, mark +
                "monk manthra" wordmark, a short italic 2-3 line mantra.
                Use as the closing slide of almost every carousel — it's
                the brand's signature move, the thing worth screenshotting
                on its own.

A typical carousel is: cover_slide -> 2-4 of {photo_slide, split_slide,
info_slide} in whatever mix fits the content -> gradient_slide. There's
no fixed slide count; 4-7 has been the sweet spot so far. Don't pad a
carousel to hit a number — a strong 4-slide arc beats a padded 7-slide
one every time, and it's also just less work for the person reading it.

PHOTOS
If a slide needs a photo, see references/image-prompts.md in this
skill for how to write Flow/Nano-Banana prompts and the no-hands
question you need to resolve before writing them. Save generated
photos into this carousel's own photos/ folder and reference them with
an *absolute* file:// path in the HTML (the background-image / <img
src> values below already assume you're passing an absolute path in).

Usage once you've copied this file and edited SLIDES:
    python3 build_<topic>.py
Output:
    png/<slide-name>.png for every entry in SLIDES
"""
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "_build")
PNG = os.path.join(HERE, "png")
PHOTOS = os.path.join(HERE, "photos")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def bold(text):
    """**word** -> <strong>word</strong>. Bold spans render in gold
    inside dark-on-light bullets/headlines, and in light-gold inside
    white-on-photo text — see the `strong` rules in CSS below."""
    if text is None:
        return None
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


# The brand mark: three concentric rings + a seed dot. Reused verbatim
# everywhere — never redraw or restyle it, that consistency is the point.
MARK = """<svg class="mark" viewBox="0 0 100 100" role="img" aria-label="monk manthra" focusable="false">
  <path class="ring ring--1" d="M 54.788 36.844 A 14.0 14.0 0 1 1 45.212 36.844"/>
  <path class="ring ring--2" d="M 57.661 28.951 A 22.4 22.4 0 1 1 42.339 28.951"/>
  <path class="ring ring--3" d="M 62.258 16.321 A 35.84 35.84 0 1 1 37.742 16.321"/>
  <circle class="seed" cx="50" cy="50" r="5.2"/>
</svg>"""

# Reference line-icons for info_slide / cover_slide. Draw new ones the
# same way: viewBox sized to the art (not forced to a square), thin
# (2.5px) currentColor strokes, no fill except small dot accents.
ICON_SUN = """<svg viewBox="0 0 120 120" class="icon"><circle cx="60" cy="75" r="24" fill="none" stroke="currentColor" stroke-width="2.5"/>
<line x1="60" y1="30" x2="60" y2="14" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<line x1="27" y1="42" x2="16" y2="31" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<line x1="93" y1="42" x2="104" y2="31" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<line x1="14" y1="75" x2="2" y2="75" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<line x1="106" y1="75" x2="118" y2="75" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>"""

ICON_EYE = """<svg viewBox="0 0 140 90" class="icon"><path d="M5 45 C 30 5, 110 5, 135 45 C 110 85, 30 85, 5 45 Z" fill="none" stroke="currentColor" stroke-width="2.5"/>
<circle cx="70" cy="45" r="16" fill="none" stroke="currentColor" stroke-width="2.5"/>
<circle cx="70" cy="45" r="5" fill="currentColor"/></svg>"""

ICON_MOON = """<svg viewBox="0 0 120 120" class="icon"><path d="M75 20 A 42 42 0 1 0 75 100 A 34 34 0 1 1 75 20 Z" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/></svg>"""

ICON_CLOCK = """<svg viewBox="0 0 120 120" class="icon"><circle cx="60" cy="60" r="46" fill="none" stroke="currentColor" stroke-width="2.5"/>
<line x1="60" y1="60" x2="60" y2="30" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<line x1="60" y1="60" x2="82" y2="70" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="60" cy="60" r="3.5" fill="currentColor"/></svg>"""

CSS = """
:root {
  --deep-purple: #3A1F5C; --royal-purple: #7A5CA8; --pale-lilac: #CBBFE0;
  --gold: #C2A053; --light-gold: #E0C88C; --half-white: #F4F1EC; --ink: #241B33;
  --display: "Fraunces", serif; --body: "Karla", sans-serif;
}
* { box-sizing: border-box; }
html, body { margin: 0; width: 1080px; height: 1080px; }
body { font-family: var(--body); background: var(--half-white); }

/* ============ photo_slide ============ */
.photo-slide { width: 1080px; height: 1080px; position: relative; display: flex; align-items: flex-end; justify-content: center;
  background-size: cover; background-position: center; padding-bottom: 96px; }
.photo-slide::before { content: ""; position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(20,14,30,0) 34%, rgba(20,14,30,0.88) 72%, rgba(20,14,30,0.97) 100%); }
/* Flow/Nano-Banana generated photos carry a small sparkle watermark,
   almost always bottom-right. This patch blends it into the scrim. */
.photo-slide .corner-patch { content: ""; position: absolute; right: 0; bottom: 0; width: 260px; height: 220px;
  background: radial-gradient(circle at 100% 100%, rgba(20,14,30,1) 0%, rgba(20,14,30,1) 45%, rgba(20,14,30,0) 78%); }
.photo-slide .corner-mark { position: absolute; top: 40px; left: 40px; z-index: 1;
  filter: drop-shadow(0 0 3px rgba(0,0,0,0.85)) drop-shadow(0 0 8px rgba(0,0,0,0.6)); }
.photo-slide .corner-mark .mark { width: 46px; height: 46px; display: block; }
.photo-slide .corner-mark .mark .ring { fill: none; stroke-linecap: round; stroke-width: 2.6; }
.photo-slide .corner-mark .mark .ring--1 { stroke: var(--half-white); }
.photo-slide .corner-mark .mark .ring--2 { stroke: var(--pale-lilac); }
.photo-slide .corner-mark .mark .ring--3 { stroke: var(--light-gold); }
.photo-slide .corner-mark .mark .seed { fill: var(--light-gold); }
.photo-slide .copy { position: relative; z-index: 1; text-align: center; width: 880px; }
.photo-slide .kicker { font-family: var(--body); font-weight: 700; font-size: 20px; letter-spacing: 0.26em; text-transform: uppercase; color: var(--light-gold); margin: 0 0 20px; }
.photo-slide h1 { font-family: var(--body); font-weight: 700; font-size: 46px; line-height: 1.3; letter-spacing: -0.01em; color: var(--half-white); margin: 0; text-shadow: 0 2px 18px rgba(0,0,0,0.5); }
.photo-slide h1 strong { color: var(--light-gold); font-weight: 800; }
.photo-slide .sub { font-family: var(--body); font-weight: 400; font-size: 25px; line-height: 1.55; color: rgba(244,241,236,0.92); width: 680px; margin: 22px auto 0; text-shadow: 0 2px 14px rgba(0,0,0,0.5); }
.photo-slide .sub strong { color: var(--light-gold); font-weight: 700; }
.photo-slide .bullets { text-align: left; width: 680px; margin: 22px auto 0; }
.photo-slide .bullets .item { display: flex; gap: 12px; margin-bottom: 10px; color: rgba(244,241,236,0.92); font-size: 25px; text-shadow: 0 2px 14px rgba(0,0,0,0.5); }
.photo-slide .bullets .dot { color: var(--light-gold); flex: none; }
.photo-slide .bullets strong { color: var(--light-gold); font-weight: 700; }

/* ============ split_slide ============ */
.split-slide { width: 1080px; height: 1080px; display: flex; flex-direction: column; background: var(--half-white); }
.split-slide .panel-text { height: 428px; flex: none; padding: 72px 84px 0; display: flex; flex-direction: column; }
.split-slide .panel-photo { flex: 1; position: relative; overflow: hidden; }
.split-slide .panel-photo img { width: 100%; height: 100%; object-fit: cover; object-position: center; display: block; }
.split-slide .corner-patch { position: absolute; right: 0; bottom: 0; width: 220px; height: 190px;
  background: radial-gradient(circle at 100% 100%, rgba(20,14,30,1) 0%, rgba(20,14,30,0.9) 40%, rgba(20,14,30,0) 78%); }
.split-slide .corner-mark { position: absolute; top: 40px; right: 40px; }
.split-slide .corner-mark .mark { width: 40px; height: 40px; display: block; }
.split-slide .corner-mark .mark .ring { fill: none; stroke-linecap: round; stroke-width: 2.6; }
.split-slide .corner-mark .mark .ring--1 { stroke: var(--deep-purple); }
.split-slide .corner-mark .mark .ring--2 { stroke: var(--royal-purple); }
.split-slide .corner-mark .mark .ring--3 { stroke: var(--gold); }
.split-slide .corner-mark .mark .seed { fill: var(--gold); }
.split-slide .label { font-family: var(--body); font-weight: 700; font-size: 19px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--royal-purple); margin: 0 0 22px; }
.split-slide h1 { font-family: var(--body); font-weight: 800; font-size: 52px; line-height: 1.22; letter-spacing: -0.015em; color: var(--ink); margin: 0; max-width: 15ch; }

/* ============ info_slide ============ */
.info-slide { width: 1080px; height: 1080px; background: var(--half-white); padding: 88px 96px; display: flex; flex-direction: column; }
.info-slide .top { display: flex; align-items: flex-start; justify-content: space-between; }
.info-slide .label { font-family: var(--body); font-weight: 700; font-size: 19px; letter-spacing: 0.24em; text-transform: uppercase; color: var(--royal-purple); margin: 0; }
.info-slide .mark { width: 34px; height: 34px; }
.info-slide .mark .ring { fill: none; stroke-linecap: round; stroke-width: 2.6; }
.info-slide .mark .ring--1 { stroke: var(--deep-purple); }
.info-slide .mark .ring--2 { stroke: var(--royal-purple); }
.info-slide .mark .ring--3 { stroke: var(--gold); }
.info-slide .mark .seed { fill: var(--gold); }
.info-slide h1 { font-size: 58px; line-height: 1.18; margin: 36px 0 0; letter-spacing: -0.01em; max-width: 15ch; }
.info-slide h1 .serif { font-family: var(--display); font-weight: 300; color: var(--ink); }
.info-slide h1 .bold { font-family: var(--body); font-weight: 800; color: var(--deep-purple); }
.info-slide .icon-wrap { flex: 1; display: flex; align-items: center; justify-content: center; }
.info-slide .icon { width: 150px; height: 150px; color: var(--gold); }
.info-slide .bullets { display: flex; flex-direction: column; gap: 20px; margin: 0 0 20px; }
.info-slide .bullets .item { display: flex; gap: 16px; align-items: flex-start; }
.info-slide .bullets .dot { flex: none; width: 8px; height: 8px; border-radius: 50%; background: var(--gold); margin-top: 12px; }
.info-slide .bullets p { font-family: var(--body); font-weight: 400; font-size: 27px; line-height: 1.5; color: var(--ink); margin: 0; }
.info-slide .bullets strong { font-weight: 700; color: var(--deep-purple); }
.info-slide .foot { border-top: 1px solid rgba(122,92,168,0.25); padding-top: 20px; }
.info-slide .foot .wordmark { font-family: var(--display); font-weight: 200; text-transform: lowercase; letter-spacing: 0.15em; font-size: 20px; color: var(--deep-purple); }

/* ============ cover_slide ============ */
/* Fully centered — the point is legibility as a small square thumbnail
   on the Instagram profile grid, not just as a full-size feed post. */
.cover-slide { width: 1080px; height: 1080px; background: var(--half-white); display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center; padding: 80px; }
.cover-slide .label { font-family: var(--body); font-weight: 700; font-size: 20px; letter-spacing: 0.28em; text-transform: uppercase;
  color: var(--royal-purple); margin: 0 0 34px; }
.cover-slide .icon { width: 130px; height: 130px; color: var(--gold); margin: 0 0 34px; }
.cover-slide h1 { font-size: 68px; line-height: 1.16; letter-spacing: -0.015em; margin: 0; max-width: 13ch; }
.cover-slide h1 .serif { font-family: var(--display); font-weight: 300; color: var(--ink); }
.cover-slide h1 .bold { font-family: var(--body); font-weight: 800; color: var(--deep-purple); }
.cover-slide .sub { font-family: var(--body); font-weight: 400; font-size: 28px; line-height: 1.5; color: var(--ink);
  max-width: 20ch; margin: 30px 0 0; }
.cover-slide .wordmark { font-family: var(--display); font-weight: 200; text-transform: lowercase; letter-spacing: 0.15em;
  font-size: 20px; color: var(--royal-purple); margin: 48px 0 0; }

/* ============ gradient_slide ============ */
.gradient-slide { width: 1080px; height: 1080px; background: radial-gradient(circle at 50% 45%, #4A2A73 0%, #3A1F5C 45%, #7A5230 130%);
  display: flex; flex-direction: column; align-items: center; justify-content: center; }
.gradient-slide .mark { width: 64px; height: 64px; margin-bottom: 40px; }
.gradient-slide .mark .ring { fill: none; stroke-linecap: round; stroke-width: 2.2; }
.gradient-slide .mark .ring--1 { stroke: var(--half-white); }
.gradient-slide .mark .ring--2 { stroke: var(--pale-lilac); }
.gradient-slide .mark .ring--3 { stroke: var(--light-gold); }
.gradient-slide .mark .seed { fill: var(--light-gold); }
.gradient-slide .wordmark { font-family: var(--display); font-weight: 200; text-transform: lowercase; letter-spacing: 0.15em; font-size: 26px; color: var(--half-white); margin: 0 0 48px; }
/* Width is set in real pixels, not `ch` — `ch` sizing here previously
   caused every short line to wrap mid-phrase instead of breaking only
   at the <br> tags, because `ch` is measured against the fallback font
   before Fraunces loads. Keep this in px. */
.gradient-slide .copy { text-align: center; width: 760px; }
.gradient-slide p { font-family: var(--display); font-weight: 300; font-style: italic; font-size: 42px; line-height: 1.85; color: var(--half-white); margin: 0; white-space: pre-line; }
"""

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,200;9..144,300;9..144,400&family=Karla:wght@300;400;500;700;800&display=swap">
<style>{css}</style></head><body>"""


def render(html_path, png_path):
    subprocess.run([
        CHROME, "--headless", "--disable-gpu",
        "--virtual-time-budget=4000",
        f"--screenshot={png_path}",
        "--window-size=1080,1080",
        f"file://{html_path}",
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def photo_slide(photo_path, headline, kicker=None, sub=None, bullets=None):
    """Full-bleed photo, dark scrim, bold headline near the bottom."""
    kicker_html = f'<p class="kicker">{kicker}</p>' if kicker else ""
    sub_html = f'<p class="sub">{bold(sub)}</p>' if sub else ""
    bullets_html = ""
    if bullets:
        items = "".join(f'<div class="item"><span class="dot">—</span><span>{bold(b)}</span></div>' for b in bullets)
        bullets_html = f'<div class="bullets">{items}</div>'
    return HEAD.format(css=CSS) + f"""
<div class="photo-slide" style="background-image:url('file://{photo_path}')">
  <span class="corner-patch"></span>
  <div class="corner-mark">{MARK}</div>
  <div class="copy">{kicker_html}<h1>{bold(headline)}</h1>{sub_html}{bullets_html}</div>
</div></body></html>"""


def split_slide(label, headline, photo_path):
    """Clean top panel (bold dark text) over a bottom photo panel."""
    return HEAD.format(css=CSS) + f"""
<div class="split-slide">
  <div class="panel-text"><p class="label">{label}</p><h1>{bold(headline)}</h1></div>
  <div class="panel-photo"><img src="file://{photo_path}">
    <span class="corner-patch"></span>
    <div class="corner-mark">{MARK}</div>
  </div>
</div></body></html>"""


def info_slide(label, headline_html, icon_svg, bullets, foot_wordmark="monk manthra"):
    """No photo — line-icon + mixed-weight headline + bulleted mechanism.
    headline_html: hand-write the mixed-weight spans yourself, e.g.
      '<span class="serif">The</span> <span class="bold">Light-to-Clock</span> <span class="serif">Pathway</span>'
    bullets: list of strings, use **word** for a bolded key term."""
    bullets_html = "".join(
        f'<div class="item"><span class="dot"></span><p>{bold(b)}</p></div>' for b in bullets
    )
    return HEAD.format(css=CSS) + f"""
<div class="info-slide">
  <div class="top"><p class="label">{label}</p>{MARK}</div>
  <h1>{headline_html}</h1>
  <div class="icon-wrap">{icon_svg}</div>
  <div class="bullets">{bullets_html}</div>
  <div class="foot"><span class="wordmark">{foot_wordmark}</span></div>
</div></body></html>"""


def cover_slide(label, headline_html, icon_svg, sub):
    """Centered version of info_slide. Use for slide 1 — reads well as
    a small profile-grid thumbnail. headline_html: same mixed-weight
    span convention as info_slide. Keep the hook punchy/pain-point
    ("Tired at 2pm. Wired at 11pm.") rather than descriptive."""
    return HEAD.format(css=CSS) + f"""
<div class="cover-slide">
  <p class="label">{label}</p>
  {icon_svg}
  <h1>{headline_html}</h1>
  <p class="sub">{sub}</p>
  <span class="wordmark">monk manthra</span>
</div></body></html>"""


def gradient_slide(lines):
    """The closing signature card. lines: 2-3 short strings, each its
    own line (joined with <br>, not wrapped — see the CSS note on why
    this must stay in px)."""
    text = "<br>".join(lines)
    return HEAD.format(css=CSS) + f"""
<div class="gradient-slide">
  {MARK}
  <p class="wordmark">monk manthra</p>
  <div class="copy"><p>{text}</p></div>
</div></body></html>"""


# Extra line-icons for this carousel, same thin-stroke currentColor style.
ICON_HOURGLASS = """<svg viewBox="0 0 100 120" class="icon">
<line x1="22" y1="10" x2="78" y2="10" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<line x1="22" y1="110" x2="78" y2="110" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<path d="M30 10 C 30 40, 50 50, 50 60 C 50 70, 30 80, 30 110" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<path d="M70 10 C 70 40, 50 50, 50 60 C 50 70, 70 80, 70 110" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<path d="M38 96 L 62 96 L 50 82 Z" fill="currentColor"/>
<circle cx="50" cy="60" r="2.5" fill="currentColor"/></svg>"""

ICON_GAUGE = """<svg viewBox="0 0 140 110" class="icon">
<line x1="14" y1="96" x2="126" y2="96" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<rect x="24" y="72" width="16" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="2.5"/>
<rect x="52" y="52" width="16" height="44" rx="2" fill="none" stroke="currentColor" stroke-width="2.5"/>
<rect x="80" y="32" width="16" height="64" rx="2" fill="none" stroke="currentColor" stroke-width="2.5"/>
<rect x="108" y="12" width="16" height="84" rx="2" fill="none" stroke="currentColor" stroke-width="2.5"/>
<circle cx="116" cy="4" r="3.5" fill="currentColor"/></svg>"""

ICON_CUP = """<svg viewBox="0 0 130 120" class="icon">
<path d="M20 40 H 92 V 78 A 26 26 0 0 1 66 104 H 46 A 26 26 0 0 1 20 78 Z" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M92 50 H 104 A 14 14 0 0 1 104 78 H 92" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<path d="M42 28 C 38 20, 46 16, 42 8" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<path d="M58 28 C 54 20, 62 16, 58 8" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
<path d="M74 28 C 70 20, 78 16, 74 8" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>"""

SLIDES = [
    ("slide-1-cover", lambda: cover_slide(
        "Sleep Pressure",
        '<span class="bold">Exhausted.</span><br><span class="serif">But not sleepy.</span>',
        ICON_HOURGLASS,
        "There's a difference — and it's chemical.")),
    ("slide-2-mechanism", lambda: info_slide(
        "What Happens",
        '<span class="serif">The</span> <span class="bold">Sleep-Pressure</span> <span class="serif">Build-Up</span>',
        ICON_GAUGE,
        [
            "Every waking hour, your brain accumulates **adenosine** — a by-product of simply being awake.",
            "The more it builds, the heavier the **pull toward sleep**. That pull is sleep pressure.",
            "Sleep clears it. **Sixteen hours up, and the tank is full** — that's the design.",
        ],
        "Part 2 — what drains the pressure")),
    ("slide-3-undo", lambda: info_slide(
        "What Undoes It",
        '<span class="bold">Caffeine</span> <span class="serif">Doesn\'t Clear It.</span><br><span class="bold">It Hides It.</span>',
        ICON_CUP,
        [
            "Caffeine sits in the **adenosine receptors** so the signal can't land. The pressure is still there — you just can't feel it.",
            "Its half-life is roughly **five to six hours**. A 4pm coffee is still half-working at 10pm.",
            "A late afternoon nap **vents the pressure** you needed for bedtime.",
        ],
        "Part 3 — the reset")),
    ("slide-4-reset", lambda: info_slide(
        "The Reset",
        '<span class="serif">Let It Build.</span> <span class="bold">Then Let It Land.</span>',
        ICON_MOON,
        [
            "**Last caffeine by early afternoon** — so it has cleared by bedtime.",
            "If you nap, **keep it short and before 3pm**.",
            "Get up at the **same time every day** — pressure only builds on a fixed start line.",
        ],
        "monkmanthra.com")),
    ("slide-5-closer", lambda: gradient_slide([
        "Tired is a signal.",
        "Listen to it,",
        "don't mask it.",
    ])),
]

def main():
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(PNG, exist_ok=True)
    os.makedirs(PHOTOS, exist_ok=True)
    for name, fn in SLIDES:
        html_path = os.path.join(BUILD, f"{name}.html")
        png_path = os.path.join(PNG, f"{name}.png")
        with open(html_path, "w") as f:
            f.write(fn())
        render(html_path, png_path)
        print(f"{name}  done")


if __name__ == "__main__":
    main()
