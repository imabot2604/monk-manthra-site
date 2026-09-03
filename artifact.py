#!/usr/bin/env python3
"""
Emit a single self-contained page for publishing as an Artifact.

Everything is inlined — the stylesheet, the mark, the photography as data URIs —
so the page holds together with no local server and no external requests beyond
Google Fonts.
"""

import base64
import os

import build as B

ROOT = B.ROOT
OUT = os.path.join(ROOT, "artifact.html")


def data_uri(slug):
    p = os.path.join(ROOT, "assets/img/products", f"{slug}@700.jpg")
    if not os.path.exists(p):
        return None
    with open(p, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def img(slug, alt, cls=""):
    u = data_uri(slug)
    if not u:
        return None
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{u}" alt="{alt}" loading="lazy" decoding="async">'


def pack(p):
    ph = img(p["slug"], f'{p["state"]} — {p["ing"].title()}, photographed overhead on linen')
    if ph:
        return ph
    if p["pack"] == "pouch":
        return B.pouch(p["state"], p["ing_lines"], f'{p["dose"]} protein · 900g')
    return B.jar(p["state"], p["ing_lines"], f'{p["dose"]} · {p["count"]}')


def card(p):
    photo = " card__figure--photo" if data_uri(p["slug"]) else ""
    return f'''      <a class="card" href="#{p["slug"]}" style="--band:{p["band"]}">
        <span class="card__band"></span>
        <span class="card__figure{photo}">{pack(p)}</span>
        <span class="card__body">
          <span class="card__name">{p["state"]}</span>
          <span class="label card__ing">{p["ing"]}</span>
          <span class="card__foot">
            <span class="data">{p["dose"]} · {p["count"]}</span>
            <span class="card__price">₹{p["price"]}</span>
          </span>
        </span>
      </a>'''


def main():
    css = open(os.path.join(ROOT, "assets/css/site.css")).read()
    js = open(os.path.join(ROOT, "assets/js/site.js")).read()

    cards = "\n".join(card(p) for p in B.PRODUCTS)
    calm = B.BY_SLUG["calm"]
    ev = B.BUNDLES[0]
    ev_items = "".join(f'''<li>
          <span class="n">{B.BY_SLUG[s]["state"]}</span>
          <span class="i">{B.BY_SLUG[s]["ing"]}</span>
          <span class="d">{B.BY_SLUG[s]["dose"]}</span>
        </li>''' for s in ev["items"])

    page = f'''<title>monk manthra</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,200;9..144,300;9..144,400&family=Karla:wght@300;400;500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
{css}
/* Artifact-only: one continuous page instead of eight */
.site-header {{ position: sticky; }}
.anchor {{ scroll-margin-top: 96px; }}
</style>

<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="lockup" href="#top" aria-label="monk manthra — top">
      <span class="lockup__disc on-purple">{B.mark(32, lock="3")}</span>
      <span class="lockup__type">
        <span class="wordmark">monk manthra</span>
        <span class="lockup__sub nav__hide-sm">Nutrition</span>
      </span>
    </a>
    <nav class="nav" aria-label="Primary">
      <a href="#start">Start</a>
      <a href="#idea">The idea</a>
      <a href="#bundle">Bundles</a>
      <a href="#range">The range</a>
    </nav>
  </div>
</header>

<main id="top">

<section class="hero on-purple">
  <div class="wrap">
    {B.mark(104, draw=True, lock="3")}
    <h1 class="display">Seven supplements. One habit.</h1>
    <p>Single-ingredient formulas at doses you can check. Made to be taken every day,
       not talked about every day.</p>
    <a class="btn" href="#range">See the range</a>
    <div class="hero__note"><p class="data">7 FORMULAS · 0 PROPRIETARY BLENDS</p></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <p class="label">Principles</p>
      <hr class="gold-rule">
      <h2 class="display">A manthra is one word, repeated, until it changes something.</h2>
      <p class="lede">That is also how a supplement works — a small dose, taken daily,
         until the effect compounds. Three rules follow from it, and we designed the
         whole range around them.</p>
    </div>
    <div class="principles">
      <div class="principle">
        <h3 class="heading">Repetition over intensity</h3>
        <p>A dose you will actually take every evening beats a stronger one you take
           twice a week. We formulate for the boring version, because that is the
           version that works.</p>
      </div>
      <div class="principle">
        <h3 class="heading">Show the dose</h3>
        <p>Milligrams, capsule count, lot, expiry — printed in full on the front of the
           pack and again on this page. Nothing sits behind the words proprietary blend.</p>
      </div>
      <div class="principle">
        <h3 class="heading">Earn the calm</h3>
        <p>White space is the product. We would rather leave a claim off the pack than
           crowd one onto it, and we would rather you read the panel than the poetry.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper anchor" id="range">
  <div class="wrap">
    <div class="section__head">
      <p class="label">The range</p>
      <hr class="gold-rule">
      <h2 class="display">Named for the state. Verified by the ingredient.</h2>
      <p class="lede">You shop by feeling and check by ingredient — never the other way
         round. Seven formulas, one word each. If a product needs two words, it needs a
         rethink.</p>
    </div>
    <div class="range">
{cards}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <p class="label">Show the dose</p>
      <hr class="gold-rule">
      <h2 class="display">The whole range, one line each.</h2>
    </div>
{B.dose_table()}
    <p class="data data--sm" style="margin-top:22px;color:#7A5CA8">
      EVERY FIGURE ON THIS PAGE IS THE FIGURE ON THE PACK
    </p>
  </div>
</section>

<section class="section section--paper anchor" id="calm">
  <div class="wrap">
    <div class="section__head">
      <p class="label">One product, in full</p>
      <hr class="gold-rule">
      <h2 class="display">Every formula gets a page like this.</h2>
    </div>
    <div class="product" style="--band:{calm["band"]}">
      <div class="product__figure product__figure--photo">{pack(calm)}</div>
      <div>
        <p class="label">{calm["ing"]}</p>
        <h3 class="product__name">{calm["state"]}</h3>
        <hr class="gold-rule">
        <p class="lede">{calm["line"]}</p>
        <div class="product__meta">
          <div><p class="label">Dose</p><p class="data">{calm["dose"]}</p></div>
          <div><p class="label">Count</p><p class="data">{calm["count"]}</p></div>
          <div><p class="label">Serving</p><p class="data">{calm["per"]}</p></div>
          <div><p class="label">When</p><p class="data">{calm["when"]}</p></div>
        </div>
        <p>{calm["blurb"]}</p>
        <div class="product__buy">
          <a class="btn" href="#start">Add to order</a>
          <span class="price">₹{calm["price"]}</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid-2">
    <div>
      <p class="label">Back of pack</p>
      <hr class="gold-rule">
      <h2 class="display">The panel, unedited.</h2>
      <p class="lede">The facts panel is a legal document, not a design surface. It is
         reproduced exactly as printed — black on white, full contrast, rules intact,
         nothing tinted purple.</p>
      <p class="data data--sm" style="color:#7A5CA8">LOT {calm["lot"]} · INK-JETTED ON THE BASE</p>
    </div>
    <div>{B.facts_panel(calm)}</div>
  </div>
</section>

<section class="section section--purple on-purple anchor" id="bundle">
  <div class="wrap">
    <div class="bundle">
      <div class="bundle__figure bundle__figure--photo">{
        img(ev["slug"], ev["name"] + " — gift carton with three amber jars on linen")
        or B.carton(ev["title"], [B.BY_SLUG[s]["state"] for s in ev["items"]])}</div>
      <div>
        <p class="label">Bundle</p>
        <hr class="gold-rule">
        <h2 class="display">{ev["name"]}</h2>
        <p class="lede">{ev["blurb"]}</p>
        <ul class="bundle__list">{ev_items}</ul>
        <p class="data" style="margin-top:22px">₹{ev["price"]} · SAVES ₹{ev["saving"]}</p>
        <p style="margin-top:20px" class="data data--sm">BUNDLES ARE NAMED FOR A TIME OF DAY, NEVER A BENEFIT</p>
      </div>
    </div>
  </div>
</section>

<section class="strip-gold on-gold">
  <div class="wrap">
    <p class="label">Practice</p>
    <h2 class="heading">A word, repeated, is how anything changes.</h2>
  </div>
</section>

<section class="section anchor" id="idea">
  <div class="wrap grid-2">
    <div>
      <p class="label">The mark</p>
      <hr class="gold-rule">
      <h2 class="display">One utterance, repeating.</h2>
      <p class="lede">A gold seed at the centre, rings travelling outward, and a gap at
         the top where the sound escapes.</p>
    </div>
    <div class="stack">
      <p>The seed radius is the unit. Each ring steps outward at roughly 1.6×, so the
         spacing loosens the way a real ripple does. Every arc runs the same 20° to 340°,
         which is why the opening sits centred and identical on all three.</p>
      <p>Gold appears exactly twice — the seed and the outer ring. The eye enters at the
         source and leaves at the edge.</p>
      <p>It drew once when this page loaded, over 1.4 seconds, outward. Then it stopped.
         It does not loop and it does not pulse, because a thing that repeats forever on
         a screen is not a practice, it is a nag.</p>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section__head">
      <p class="label">How we write</p>
      <hr class="gold-rule">
      <h2 class="display">The calmest voice in a loud category.</h2>
      <p class="lede">Plain verbs, no exclamation marks, no urgency. That is close to the
         whole of the differentiation.</p>
    </div>
    <div class="table-scroll">
      <table class="dose-table">
        <thead><tr><th scope="col">We write this</th><th scope="col">Not this</th></tr></thead>
        <tbody>
          <tr><td>Take one capsule with the evening meal.</td>
              <td style="color:#7A5CA8">Unlock your best sleep ever</td></tr>
          <tr><td>600mg of ashwagandha. Nothing else added.</td>
              <td style="color:#7A5CA8">Our proprietary blend of ancient botanicals</td></tr>
          <tr><td>Most people notice something by week three.</td>
              <td style="color:#7A5CA8">Feel the difference from day one, guaranteed</td></tr>
        </tbody>
      </table>
    </div>
    <p class="disclaimer">
      We never say a product treats, prevents, cures or diagnoses anything — that
      language turns a supplement into an unlicensed drug in most markets. We use
      structure-and-function phrasing only, and only where we hold evidence for the
      specific dose we sell. No before-and-after imagery, no weight-loss framing, no
      "clinically proven" flashes, on any channel.
    </p>
  </div>
</section>

<section class="section section--purple on-purple anchor" id="start">
  <div class="wrap wrap--narrow center">
    <p class="label">Start</p>
    <h2 class="display" style="margin-top:14px">Take it tonight.<br>Then take it again tomorrow.</h2>
    <p style="margin:26px auto 0">Most people notice something around week three. Set a
       reminder, keep the jar where you will see it, and give it a month before you
       decide.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <p class="label">Three steps, and then repetition</p>
      <hr class="gold-rule">
      <h2 class="display">There is not much to it, which is the point.</h2>
    </div>
    <div class="steps">
      <div class="step">
        <span class="n">01</span>
        <h3 class="heading">Pick the state, not the ingredient.</h3>
        <p>Choose by how you want to feel. The ingredient is printed underneath so you
           can check the choice, which is the right order to do it in.</p>
      </div>
      <div class="step">
        <span class="n">02</span>
        <h3 class="heading">Attach it to a meal you never skip.</h3>
        <p>Evening formulas go with dinner, morning ones with breakfast. A dose attached
           to an existing habit is a dose you will still be taking in March.</p>
      </div>
      <div class="step">
        <span class="n">03</span>
        <h3 class="heading">Give it a month before you judge it.</h3>
        <p>Then keep it or stop it. Because there is one ingredient in the jar, you will
           know exactly what you kept or stopped.</p>
      </div>
    </div>
  </div>
</section>

</main>

<footer class="site-footer on-purple">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__col footer__brand">
        {B.mark(44, lock="2")}
        <span class="wordmark" style="font-size:20px;display:block;margin-bottom:14px">monk manthra</span>
        <p>Daily supplements for people who want to feel steady, not supercharged.</p>
      </div>
      <div class="footer__col">
        <p class="label">The range</p>
        <ul>{"".join(f'<li><a href="#range">{p["state"]}</a></li>' for p in B.PRODUCTS)}</ul>
      </div>
      <div class="footer__col">
        <p class="label">Bundles</p>
        <ul>
          <li><a href="#bundle">The Evening Three</a></li>
          <li><a href="#bundle">The Morning Two</a></li>
          <li><a href="#start">Subscribe</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <p class="label">Company</p>
        <ul>
          <li><a href="#idea">The idea</a></li>
          <li><a href="#start">How to begin</a></li>
          <li><a href="mailto:hello@monkmanthra.com">hello@monkmanthra.com</a></li>
          <li><span class="data" style="color:rgba(244,241,236,.72)">+91 98 4712 0088</span></li>
        </ul>
      </div>
    </div>
    <p class="disclaimer">
      These statements have not been evaluated by a food-safety regulator. These
      products are not intended to diagnose, treat, cure or prevent any disease.
      Supplements are not a substitute for a varied diet. Speak to a doctor before
      starting anything new if you are pregnant, nursing, or taking medication.
      Prices, facts panels and lot codes on this page are placeholder content pending
      formulator and regulatory sign-off.
    </p>
    <div class="footer__base">
      <p class="data">© 2026 MONK MANTHRA NUTRITION</p>
      <p class="data">BRAND GUIDE V1.0 · MADE IN INDIA</p>
    </div>
  </div>
</footer>

<script>
{js}
</script>'''

    with open(OUT, "w") as f:
        f.write(page)
    print(f"artifact.html — {len(page)/1024/1024:.2f} MB")


if __name__ == "__main__":
    main()
