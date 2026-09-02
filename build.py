#!/usr/bin/env python3
"""
monk manthra — static site generator.

Content lives here once; the pages are emitted from it so the six product
pages cannot drift apart. Run:  python3 build.py
"""

import os, math, json, textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# SHOPIFY — commerce backend only. The site's HTML, CSS and copy stay exactly
# as they are; Shopify holds price, stock and checkout. See README.md,
# "Selling on Shopify" for the three things you need to fill in below.
#
# Until "domain" stops saying YOUR-STORE, every buy button on the site is a
# plain link to start.html — unchanged from today. Nothing here can go live
# by accident.
# --------------------------------------------------------------------------
SHOP = {
    "domain": "YOUR-STORE.myshopify.com",          # Settings → Domains
    "token": "YOUR-STOREFRONT-ACCESS-TOKEN",        # public by design — see README
    # Storefront API is versioned quarterly (YYYY-01/04/07/10). Bump this
    # every few months: https://shopify.dev/docs/api/usage/versioning
    "apiVersion": "2025-10",
}
SHOP_CONFIGURED = "YOUR-STORE" not in SHOP["domain"] and "YOUR-" not in SHOP["token"]

# --------------------------------------------------------------------------
# THE MARK — gold seed, two purple rings, gold outer ring, gap at the top.
# Arcs run 20° to 340°. Ring radii step 1.6×. Round caps, no gradients.
# --------------------------------------------------------------------------
SEED_R = 5.2
RING_R = [14.0, 22.4, 35.84]          # 1.6× steps outward


def arc(r):
    """Arc from 20° to 340°, measured clockwise from the top."""
    a = math.radians(20.0)
    x1, y1 = 50 + r * math.sin(a), 50 - r * math.cos(a)
    x2, y2 = 50 - r * math.sin(a), 50 - r * math.cos(a)
    return f"M {x1:.3f} {y1:.3f} A {r} {r} 0 1 1 {x2:.3f} {y2:.3f}"


def mark(size=104, draw=False, cls="", lock=None):
    d = ' data-draw=""' if draw else ""
    lk = f' data-rings="{lock}" data-rings-lock=""' if lock else ""
    rings = "\n".join(
        f'    <path class="ring ring--{i+1}" d="{arc(r)}"/>' for i, r in enumerate(RING_R)
    )
    return (
        f'<svg class="mark {cls}" viewBox="0 0 100 100" width="{size}" height="{size}" '
        f'role="img" aria-label="monk manthra"{d}{lk} focusable="false">\n'
        f'{rings}\n'
        f'    <circle class="seed" cx="50" cy="50" r="{SEED_R}"/>\n'
        f'  </svg>'
    )


# --------------------------------------------------------------------------
# PACKAGING RENDERINGS — Section Eight. Placeholders until photography lands.
# Front of pack: mark, wordmark, state, ingredient. Dose and count in mono.
# --------------------------------------------------------------------------
def pack_mark(cx, cy, s, gold="#C2A053", purple="#7A5CA8"):
    """Small mark for a pack face, drawn at scale s around (cx, cy)."""
    def p(r):
        a = math.radians(20.0)
        x1, y1 = cx + r * s * math.sin(a), cy - r * s * math.cos(a)
        x2, y2 = cx - r * s * math.sin(a), cy - r * s * math.cos(a)
        return f"M {x1:.2f} {y1:.2f} A {r*s:.2f} {r*s:.2f} 0 1 1 {x2:.2f} {y2:.2f}"
    w = max(0.9, 2.4 * s)
    return (
        f'<path d="{p(14.0)}" fill="none" stroke="{purple}" stroke-width="{w:.2f}" stroke-linecap="round"/>'
        f'<path d="{p(22.4)}" fill="none" stroke="{purple}" stroke-width="{w:.2f}" stroke-linecap="round"/>'
        f'<path d="{p(35.84)}" fill="none" stroke="{gold}" stroke-width="{w:.2f}" stroke-linecap="round"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{5.2*s:.2f}" fill="{gold}"/>'
    )


def jar(state, ing_lines, dose):
    """Amber glass jar · deep purple cap · uncoated label, gold foil rule."""
    ing = "".join(
        f'<text class="pk-ing" x="150" y="{236 + i*13}" text-anchor="middle" '
        f'font-size="7.5" fill="#7A5CA8">{l}</text>'
        for i, l in enumerate(ing_lines)
    )
    return f'''<svg class="pack" viewBox="0 0 300 392" role="img" aria-label="{state} — amber glass jar with a deep purple cap">
  <rect class="pk-cap" x="92" y="10" width="116" height="40" rx="4"/>
  <rect x="92" y="44" width="116" height="8" fill="#2C1747"/>
  <rect class="pk-glass" x="60" y="50" width="180" height="332" rx="18"/>
  <rect class="pk-glass-2" x="60" y="50" width="16" height="332" rx="18"/>
  <rect x="214" y="66" width="9" height="300" rx="4.5" fill="#C08A45" opacity=".55"/>
  <rect class="pk-label" x="74" y="112" width="152" height="212" rx="2"/>
  {pack_mark(150, 146, 0.42)}
  <text class="pk-word" x="150" y="180" text-anchor="middle" font-size="12" fill="#3A1F5C">monk manthra</text>
  <line x1="126" y1="194" x2="174" y2="194" class="pk-foil"/>
  <text class="pk-state" x="150" y="222" text-anchor="middle" font-size="30" fill="#3A1F5C">{state}</text>
  {ing}
  <text class="pk-data" x="150" y="306" text-anchor="middle" font-size="8" fill="#3A1F5C">{dose}</text>
</svg>'''


def pouch(state, ing_lines, dose):
    """Stand pouch · matte deep purple · resealable, no window."""
    teeth = "".join(
        f'<rect x="{62 + i*11}" y="14" width="7" height="12" fill="#3A1F5C"/>' for i in range(16)
    )
    ing = "".join(
        f'<text class="pk-ing" x="150" y="{244 + i*13}" text-anchor="middle" '
        f'font-size="7.5" fill="#CBBFE0">{l}</text>'
        for i, l in enumerate(ing_lines)
    )
    return f'''<svg class="pack" viewBox="0 0 300 392" role="img" aria-label="{state} — matte deep purple stand pouch">
  {teeth}
  <rect class="pk-pouch" x="58" y="30" width="184" height="352" rx="12"/>
  <rect x="58" y="30" width="184" height="352" rx="12" fill="none" stroke="#4A2C70" stroke-width="1"/>
  <line x1="76" y1="60" x2="224" y2="60" stroke="#4A2C70" stroke-width="1"/>
  {pack_mark(150, 132, 0.42, gold="#E0C88C", purple="#CBBFE0")}
  <text class="pk-word" x="150" y="168" text-anchor="middle" font-size="12" fill="#F4F1EC">monk manthra</text>
  <line x1="126" y1="182" x2="174" y2="182" stroke="#E0C88C" stroke-width="1.4"/>
  <text class="pk-state" x="150" y="228" text-anchor="middle" font-size="32" fill="#F4F1EC">{state}</text>
  {ing}
  <text class="pk-data" x="150" y="322" text-anchor="middle" font-size="8" fill="#CBBFE0">{dose}</text>
</svg>'''


def carton(title_lines, contents):
    """Gift carton · gold spine reveals the bundle contents."""
    spine = " · ".join(contents).upper()
    lines = "".join(
        f'<text class="pk-state" x="132" y="{206 + i*40}" text-anchor="middle" '
        f'font-size="28" fill="#3A1F5C">{l}</text>'
        for i, l in enumerate(title_lines)
    )
    return f'''<svg class="pack" viewBox="0 0 300 392" role="img" aria-label="{' '.join(title_lines)} — gift carton with a gold spine">
  <rect x="34" y="30" width="232" height="332" fill="#EAE6DF"/>
  <rect x="46" y="42" width="172" height="308" fill="#F4F1EC"/>
  <rect x="218" y="42" width="36" height="308" fill="#C2A053"/>
  {pack_mark(132, 112, 0.40)}
  <text class="pk-word" x="132" y="152" text-anchor="middle" font-size="11" fill="#3A1F5C">monk manthra</text>
  <line x1="112" y1="166" x2="152" y2="166" class="pk-foil"/>
  {lines}
  <text class="pk-ing" x="132" y="300" text-anchor="middle" font-size="7.5" fill="#7A5CA8">{spine}</text>
  <text class="pk-ing" x="236" y="196" text-anchor="middle" font-size="8" fill="#3A1F5C"
        transform="rotate(90 236 196)" letter-spacing="3">{spine}</text>
</svg>'''


# --------------------------------------------------------------------------
# THE RANGE — Section Seven. Named for the state, verified by the ingredient.
# Products are separated by a 4mm tonal band drawn from the core palette,
# never by a new colour.
# --------------------------------------------------------------------------
PRODUCTS = [
    dict(
        slug="rest", state="Rest", ing="MAGNESIUM GLYCINATE", ing_lines=["MAGNESIUM", "GLYCINATE"],
        dose="400mg", count="60 capsules", per="1 capsule", when="Evening",
        price="1,290", band="#3A1F5C", pack="jar", lot="MM-2604",
        line="Magnesium bound to glycine, which is the form that tends to sit easily.",
        blurb=(
            "Magnesium bisglycinate at 400mg, and nothing else in the capsule but the "
            "capsule. It is the form chelated to glycine rather than oxide, which is the "
            "cheap one that mostly passes through. One capsule with the evening meal."
        ),
        supports="Contributes to normal muscle function and to the reduction of tiredness.",
        facts=[("Magnesium (as magnesium bisglycinate)", "400mg"),
               ("&nbsp;&nbsp;of which elemental magnesium", "56mg")],
        other="hypromellose capsule, rice flour.",
        directions="one capsule with the evening meal.",
    ),
    dict(
        slug="calm", state="Calm", ing="ASHWAGANDHA KSM-66", ing_lines=["ASHWAGANDHA", "KSM-66"],
        dose="600mg", count="60 capsules", per="1 capsule", when="Evening",
        price="1,450", band="#7A5CA8", pack="jar", lot="MM-2611",
        # Paste the variant's GraphQL ID from Shopify admin, exactly in this
        # form — the numeric ID alone will not work. Every other product
        # defaults to None (a plain link) until it gets the same treatment.
        shopify_variant_id=None,  # e.g. "gid://shopify/ProductVariant/45123456789012"
        line="600mg of ashwagandha. That is the whole formula.",
        blurb=(
            "One root extract, standardised to 5% withanolides, at the dose the research "
            "actually used. There is no blend behind it and no second ingredient doing "
            "quiet work. If it does not suit you, you know exactly what to stop taking."
        ),
        supports="Traditionally taken to support the body through periods of stress.",
        facts=[("Ashwagandha root extract", "600mg"),
               ("&nbsp;&nbsp;(KSM-66, 5% withanolides)", ""),
               ("Organic black pepper", "5mg")],
        other="hypromellose capsule, rice flour.",
        directions="one capsule with the evening meal.",
    ),
    dict(
        slug="ease", state="Ease", ing="TURMERIC + PIPERINE", ing_lines=["TURMERIC +", "PIPERINE"],
        dose="500mg", count="90 capsules", per="1 capsule", when="With food",
        price="1,150", band="#C2A053", pack="jar", lot="MM-2617",
        line="Turmeric with the black pepper that makes it worth swallowing.",
        blurb=(
            "Curcumin on its own is poorly absorbed, so it is paired with piperine, which "
            "is the whole reason the two appear together on every honest label. 500mg of "
            "extract, 5mg of pepper, taken with a meal that has some fat in it."
        ),
        supports="Contributes to the normal function of joints.",
        facts=[("Turmeric root extract", "500mg"),
               ("&nbsp;&nbsp;(95% curcuminoids)", ""),
               ("Black pepper extract (95% piperine)", "5mg")],
        other="hypromellose capsule, rice flour.",
        directions="one capsule with a meal containing fat.",
    ),
    dict(
        slug="clarity", state="Clarity", ing="OMEGA-3 · ALGAL", ing_lines=["OMEGA-3", "ALGAL"],
        dose="1000mg", count="60 capsules", per="1 capsule", when="With food",
        price="1,890", band="#CBBFE0", pack="jar", lot="MM-2622",
        line="Omega-3 taken from the algae, which is where the fish get it.",
        blurb=(
            "Algal oil rather than fish oil: same DHA and EPA, no ocean aftertaste, and "
            "nothing that came out of a trawler. 1000mg of oil per capsule, of which "
            "500mg is DHA. Vegan, and stable in an amber jar."
        ),
        supports="DHA contributes to the maintenance of normal brain function.",
        facts=[("Algal oil", "1000mg"),
               ("&nbsp;&nbsp;of which DHA", "500mg"),
               ("&nbsp;&nbsp;of which EPA", "100mg")],
        other="modified starch capsule, glycerol, rosemary extract.",
        directions="one capsule with any meal.",
    ),
    dict(
        slug="sun", state="Sun", ing="VITAMIN D3 + K2", ing_lines=["VITAMIN D3 + K2"],
        dose="2000 IU", count="90 capsules", per="1 capsule", when="Morning",
        price="890", band="#E0C88C", pack="jar", lot="MM-2629",
        line="D3 with the K2 that decides where the calcium goes.",
        blurb=(
            "2000 IU of vitamin D3 from lichen, with 100mcg of K2 as MK-7. The two are "
            "sold separately almost everywhere, which never made much sense to us. Take "
            "it in the morning, with something to eat."
        ),
        supports="Vitamin D contributes to the normal absorption of calcium.",
        facts=[("Vitamin D3 (as cholecalciferol, lichen)", "2000 IU"),
               ("&nbsp;&nbsp;equivalent to", "50mcg"),
               ("Vitamin K2 (as menaquinone-7)", "100mcg")],
        other="modified starch capsule, medium-chain triglycerides.",
        directions="one capsule in the morning, with food.",
    ),
    dict(
        slug="build", state="Build", ing="PLANT PROTEIN · VANILLA", ing_lines=["PLANT PROTEIN", "VANILLA"],
        dose="24g", count="900g pouch", per="1 scoop (32g)", when="Any time",
        price="2,290", band="#241B33", pack="pouch", lot="MM-2634",
        line="Pea and rice protein, vanilla, and nothing that needs explaining.",
        blurb=(
            "24g of protein per scoop from pea and brown rice, which between them cover "
            "the full amino profile. Sweetened lightly, flavoured with real vanilla, and "
            "sold in a matte pouch with no window because light is not good for it."
        ),
        supports="Protein contributes to the growth and maintenance of muscle mass.",
        facts=[("Protein", "24g"),
               ("Carbohydrate", "2.1g"),
               ("&nbsp;&nbsp;of which sugars", "0.8g"),
               ("Fat", "1.9g"),
               ("Salt", "0.21g")],
        other="pea protein isolate, brown rice protein, natural vanilla, sunflower lecithin, steviol glycosides.",
        directions="one scoop in 250ml of water or milk, any time of day.",
    ),
    dict(
        slug="golden-milk", state="Golden Milk", ing="TURMERIC · GINGER · CINNAMON",
        ing_lines=["TURMERIC · GINGER", "CINNAMON"],
        dose="5g", count="300g pouch", per="1 tsp (5g)", when="Evening",
        price="1,390", band="#C2A053", pack="pouch", lot="MM-2647",
        line="Turmeric, ginger and cinnamon. The warm milk is up to you.",
        blurb=(
            "The drink people have made at home for a very long time, measured out so "
            "you know what is in the cup. Turmeric for the colour and the curcumin, "
            "ginger and cinnamon because they belong there, and black pepper because "
            "turmeric is poorly absorbed without it. One teaspoon, stirred into "
            "whatever milk you use."
        ),
        supports="Contributes to the normal function of joints.",
        facts=[("Turmeric powder", "3g"),
               ("&nbsp;&nbsp;of which curcuminoids", "90mg"),
               ("Ginger powder", "1.2g"),
               ("Ceylon cinnamon", "700mg"),
               ("Black pepper extract", "10mg")],
        other="nothing else. No sweetener, no milk powder, no anti-caking agent.",
        directions="one teaspoon stirred into 200ml of warm milk, in the evening.",
    ),
]
BY_SLUG = {p["slug"]: p for p in PRODUCTS}

BUNDLES = [
    dict(
        slug="the-evening-three", title=["The Evening", "Three"], name="The Evening Three",
        items=["rest", "calm", "ease"], price="3,490", saving="400",
        line="Three capsules, one glass of water, the same time each night.",
        blurb=(
            "Rest, Calm and Ease are the three we are most often asked about together, so "
            "they ship together, in a carton with a gold spine that tells you what is "
            "inside without being opened. Take all three with the evening meal."
        ),
    ),
    dict(
        slug="the-morning-two", title=["The Morning", "Two"], name="The Morning Two",
        items=["sun", "clarity"], price="2,490", saving="290",
        line="Two capsules, before the day gets loud.",
        blurb=(
            "Sun and Clarity both want to be taken with food, and breakfast is the meal "
            "most people never skip. Two capsules, one carton, no decision to make at "
            "seven in the morning."
        ),
    ),
]


# --------------------------------------------------------------------------
# PAGE CHROME
# --------------------------------------------------------------------------
NAV = [("Start", "start.html"), ("The range", "range.html"),
       ("Bundles", "bundles.html"), ("The idea", "story.html")]


def head(title, desc, rel=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,200;9..144,300;9..144,400&family=Karla:wght@300;400;500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{rel}assets/css/site.css">
<link rel="icon" href="{rel}assets/img/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#3A1F5C">
</head>
<body>
<a class="visually-hidden" href="#main">Skip to content</a>'''


def header(active, rel="", section=None):
    def state(h):
        if h == active:
            return ' aria-current="page"'
        if h == section:
            return ' data-section=""'   # an ancestor section, not the page itself
        return ""
    links = "".join(f'<a href="{rel}{h}"{state(h)}>{t}</a>' for t, h in NAV)
    return f'''
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="lockup" href="{rel}index.html" aria-label="monk manthra — home">
      {mark(32, lock="3")}
      <span class="lockup__type">
        <span class="wordmark">monk manthra</span>
        <span class="lockup__sub nav__hide-sm">Nutrition</span>
      </span>
    </a>
    <nav class="nav" aria-label="Primary">{links}</nav>{"" if not SHOP_CONFIGURED else chr(10) + "    " + cart_chrome()}
  </div>
</header>
<main id="main">'''


def footer(rel=""):
    prods = "".join(
        f'<li><a href="{rel}products/{p["slug"]}.html">{p["state"]}</a></li>' for p in PRODUCTS
    )
    return f'''</main>
<footer class="site-footer on-purple">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__col footer__brand">
        {mark(44, lock="2")}
        <span class="wordmark" style="font-size:20px;display:block;margin-bottom:14px">monk manthra</span>
        <p>Daily supplements for people who want to feel steady, not supercharged.</p>
      </div>
      <div class="footer__col">
        <p class="label">The range</p>
        <ul>{prods}</ul>
      </div>
      <div class="footer__col">
        <p class="label">Bundles</p>
        <ul>
          <li><a href="{rel}bundles.html">The Evening Three</a></li>
          <li><a href="{rel}bundles.html">The Morning Two</a></li>
          <li><a href="{rel}start.html">Subscribe</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <p class="label">Company</p>
        <ul>
          <li><a href="{rel}story.html">The idea</a></li>
          <li><a href="{rel}start.html">How to begin</a></li>
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
    </p>
    <div class="footer__base">
      <p class="data">© 2026 MONK MANTHRA NUTRITION</p>
      <p class="data">BRAND GUIDE V1.0 · MADE IN INDIA</p>
    </div>
  </div>
</footer>
<script src="{rel}assets/js/site.js"></script>{("" if not SHOP_CONFIGURED else chr(10) + f'<script>window.SHOP={json.dumps(SHOP)};</script><script src="{rel}assets/js/shop.js"></script>')}
</body>
</html>'''


# --------------------------------------------------------------------------
# COMPONENTS
# --------------------------------------------------------------------------
def photo(slug, alt, rel="", lazy=True, sizes="(max-width: 900px) 92vw, 380px"):
    """Overhead, single object, soft light, linen ground — Section Eleven."""
    f = os.path.join(ROOT, "assets/img/products", slug + ".jpg")
    if not os.path.exists(f):
        return None
    lz = ' loading="lazy" decoding="async"' if lazy else ""
    return (f'<img src="{rel}assets/img/products/{slug}.jpg" '
            f'srcset="{rel}assets/img/products/{slug}@700.jpg 700w, '
            f'{rel}assets/img/products/{slug}.jpg 1024w" sizes="{sizes}" '
            f'width="1024" height="872" alt="{alt}"{lz}>')


def pack_for(p, rel="", lazy=True):
    """A photograph when one exists, otherwise the pack drawn to spec."""
    alt = f'{p["state"]} — {p["ing"].title()}, photographed overhead on linen'
    ph = photo(p["slug"], alt, rel, lazy)
    if ph:
        return ph
    dose = f'{p["dose"]} · {p["count"].replace(" pouch", "")}'
    if p["pack"] == "pouch":
        return pouch(p["state"], p["ing_lines"], f'{p["dose"]} protein · 900g')
    return jar(p["state"], p["ing_lines"], dose)


def has_photo(slug):
    return os.path.exists(os.path.join(ROOT, "assets/img/products", slug + ".jpg"))


def card(p, rel=""):
    ph = " card__figure--photo" if has_photo(p["slug"]) else ""
    return f'''      <a class="card" href="{rel}products/{p["slug"]}.html" style="--band:{p["band"]}">
        <span class="card__band"></span>
        <span class="card__figure{ph}">{pack_for(p, rel)}</span>
        <span class="card__body">
          <span class="card__name">{p["state"]}</span>
          <span class="label card__ing">{p["ing"]}</span>
          <span class="card__foot">
            <span class="data">{p["dose"]} · {p["count"]}</span>
            <span class="card__price">₹{p["price"]}</span>
          </span>
        </span>
      </a>'''


def buy_button(item, rel="", label="Add to order"):
    """A real cart when shopify_variant_id is set; today, a plain link to
    start.html — identical to every other page until Shopify is configured."""
    vid = item.get("shopify_variant_id")
    if vid:
        return f'<a class="btn" href="{rel}start.html" data-buy data-variant-id="{vid}" data-qty="1">{label}</a>'
    return f'<a class="btn" href="{rel}start.html">{label}</a>'


def cart_chrome():
    """The toggle, scrim and drawer. Present on every page via header(), but
    the toggle stays visually quiet — a small ring, not a fourth nav item —
    until something is actually in it."""
    return '''
    <button type="button" class="cart-toggle" data-cart-toggle aria-label="Order" aria-haspopup="dialog">
      <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
        <path d="M5 8h14l-1.2 10.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8L5 8Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>
        <path d="M8.5 8V6a3.5 3.5 0 0 1 7 0v2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
      </svg>
      <span class="cart-toggle__count" data-cart-count hidden>0</span>
    </button>
    <div class="cart-scrim" hidden data-cart-close></div>
    <aside class="cart-drawer" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Your order">
      <div class="cart-drawer__head">
        <p class="label">Your order</p>
        <button type="button" class="cart-drawer__close" data-cart-close aria-label="Close">×</button>
      </div>
      <ul class="cart-lines" data-cart-body></ul>
      <div class="cart-drawer__foot">
        <div class="cart-subtotal">
          <span class="label">Subtotal</span>
          <span class="data" data-cart-subtotal></span>
        </div>
        <a class="btn" data-cart-checkout aria-disabled="true">Checkout</a>
        <p class="data data--sm cart-drawer__note">Checkout and payment happen on Shopify's own secure page.</p>
      </div>
    </aside>'''


def dose_table():
    rows = "".join(f'''        <tr>
          <td class="state">{p["state"]}</td>
          <td>{p["ing"]}</td>
          <td class="num">{p["dose"]}</td>
          <td class="num">{p["count"]}</td>
          <td class="num">{p["when"]}</td>
        </tr>''' for p in PRODUCTS)
    return f'''    <div class="table-scroll">
      <table class="dose-table">
        <thead><tr>
          <th scope="col">State</th><th scope="col">Ingredient</th>
          <th scope="col">Dose</th><th scope="col">Count</th><th scope="col">When</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>'''


def facts_panel(p):
    rows = "".join(
        f'<tr><td>{n}</td><td>{v}</td></tr>' for n, v in p["facts"]
    )
    return f'''<div class="facts">
  <h3>Supplement Facts</h3>
  <hr class="facts__hr">
  <div class="row-head"><span>Serving size</span><span>{p["per"]}</span></div>
  <div class="row-head"><span>Servings per container</span><span>{p["count"].split()[0]}</span></div>
  <hr class="facts__hr facts__hr--heavy">
  <div class="row-head"><span></span><span>Amount / serving</span></div>
  <hr class="facts__hr">
  <table>{rows}</table>
  <hr class="facts__hr facts__hr--mid">
  <div class="facts__foot">
    <p>Other ingredients: {p["other"]}</p>
    <p>Contains no gluten, dairy, or soy.</p>
    <p>Directions: {p["directions"]}</p>
    <p>Not for use during pregnancy. Keep out of reach of children.</p>
    <p>Lot {p["lot"]} · best before end 2028-04</p>
  </div>
</div>'''


# --------------------------------------------------------------------------
# PAGES
# --------------------------------------------------------------------------
def page_index():
    cards = "\n".join(card(p) for p in PRODUCTS)
    ev = BUNDLES[0]
    ev_items = "".join(f'''<li>
        <span class="n">{BY_SLUG[s]["state"]}</span>
        <span class="i">{BY_SLUG[s]["ing"]}</span>
        <span class="d">{BY_SLUG[s]["dose"]}</span>
      </li>''' for s in ev["items"])

    return head("monk manthra", "Six single-ingredient daily supplements at doses you can check.") + header("index.html") + f'''
<section class="hero on-purple">
  <div class="wrap">
    {mark(104, draw=True, lock="3")}
    <h1 class="display">Seven supplements. One habit.</h1>
    <p>Single-ingredient formulas at doses you can check. Made to be taken every day,
       not talked about every day.</p>
    <a class="btn" href="range.html">See the range</a>
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
           pack and again on this site. Nothing sits behind the words proprietary blend.</p>
      </div>
      <div class="principle">
        <h3 class="heading">Earn the calm</h3>
        <p>White space is the product. We would rather leave a claim off the pack than
           crowd one onto it, and we would rather you read the panel than the poetry.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper">
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
{dose_table()}
    <p class="data data--sm" style="margin-top:22px;color:#7A5CA8">
      EVERY FIGURE ON THIS PAGE IS THE FIGURE ON THE PACK
    </p>
  </div>
</section>

<section class="section section--purple on-purple">
  <div class="wrap">
    <div class="bundle">
      <div class="bundle__figure{" bundle__figure--photo" if has_photo(ev["slug"]) else ""}">{
        photo(ev["slug"], ev["name"] + " — gift carton with three amber jars, photographed overhead on linen", sizes="(max-width: 860px) 92vw, 440px")
        or carton(ev["title"], [BY_SLUG[s]["state"] for s in ev["items"]])}</div>
      <div>
        <p class="label">Bundle</p>
        <hr class="gold-rule">
        <h2 class="display">{ev["name"]}</h2>
        <p class="lede">{ev["blurb"]}</p>
        <ul class="bundle__list">{ev_items}</ul>
        <p class="data" style="margin-top:22px">₹{ev["price"]} · SAVES ₹{ev["saving"]}</p>
        <p style="margin-top:26px"><a class="textlink" href="bundles.html">See both bundles</a></p>
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

<section class="section">
  <div class="wrap grid-2">
    <div>
      <p class="label">Day 21</p>
      <hr class="gold-rule">
      <h2 class="display">Nothing dramatic happened. That was the point.</h2>
    </div>
    <div class="stack">
      <p>Most people notice something around week three. Set a reminder, keep the jar
         where you will see it, and give it a month before you decide.</p>
      <p>We are not going to tell you that you will feel it on day one. What we will
         tell you is exactly what is in the capsule, how much of it there is, and when
         to take it. The rest is repetition.</p>
      <p style="margin-top:8px"><a class="textlink" href="start.html">How to begin</a></p>
    </div>
  </div>
</section>
''' + footer()


def page_range():
    cards = "\n".join(card(p) for p in PRODUCTS)
    return head("The range — monk manthra", "Six single-ingredient formulas at doses you can check.") + header("range.html") + f'''
<section class="section section--tight">
  <div class="wrap">
    <div class="section__head">
      <p class="label">The range</p>
      <hr class="gold-rule">
      <h1 class="display">Seven supplements. One habit.</h1>
      <p class="lede">Every product is named for the state it supports, with the actual
         ingredient underneath it. One word only. The range is never numbered and never
         lettered — numbers belong to doses.</p>
    </div>
    <div class="range">
{cards}
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section__head">
      <p class="label">Compare</p>
      <hr class="gold-rule">
      <h2 class="display">The whole range, one line each.</h2>
      <p class="lede">Doses are given in the units the ingredient is actually measured
         in, so there is nothing to convert and nothing to compare against a scale we
         invented.</p>
    </div>
{dose_table()}
  </div>
</section>

<section class="section">
  <div class="wrap grid-2">
    <div>
      <p class="label">How the shelf stays one family</p>
      <hr class="gold-rule">
      <h2 class="heading">Products are separated by a four-millimetre tonal band, not by
        a new colour.</h2>
    </div>
    <div class="stack">
      <p>Every band is drawn from the same six-colour palette the rest of the brand
         uses. Nothing joins the range with a colour of its own, which is why six jars
         on a shelf read as one thing rather than six.</p>
      <p>Capsules use the jar. Powders use the pouch. Gifting and subscription use the
         carton. There are no other formats.</p>
      <p><a class="textlink" href="bundles.html">See the bundles</a></p>
    </div>
  </div>
</section>
''' + footer()


def page_product(p):
    rel = "../"
    others = [q for q in PRODUCTS if q["slug"] != p["slug"]][:3]
    rel_cards = "\n".join(card(q, rel) for q in others)
    return head(f'{p["state"]} — monk manthra', f'{p["state"]} · {p["ing"]} · {p["dose"]} · {p["count"]}.', rel) \
        + header(None, rel, section="range.html") + f'''
<nav class="crumb" aria-label="Breadcrumb">
  <div class="wrap">
    <ol>
      <li><a href="{rel}index.html">monk manthra</a></li>
      <li><a href="{rel}range.html">The range</a></li>
      <li><span aria-current="page">{p["state"]}</span></li>
    </ol>
  </div>
</nav>
<section class="section section--tight">
  <div class="wrap">
    <div class="product" style="--band:{p["band"]}">
      <div class="product__figure{" product__figure--photo" if has_photo(p["slug"]) else ""}">{pack_for(p, rel, lazy=False)}</div>
      <div>
        <p class="label">{p["ing"]}</p>
        <h1 class="product__name">{p["state"]}</h1>
        <hr class="gold-rule">
        <p class="lede">{p["line"]}</p>

        <div class="product__meta">
          <div><p class="label">Dose</p><p class="data">{p["dose"]}</p></div>
          <div><p class="label">Count</p><p class="data">{p["count"]}</p></div>
          <div><p class="label">Serving</p><p class="data">{p["per"]}</p></div>
          <div><p class="label">When</p><p class="data">{p["when"]}</p></div>
        </div>

        <p>{p["blurb"]}</p>

        <div class="product__buy">
          {buy_button(p, rel)}
          <span class="price">₹{p["price"]}</span>
          <a class="textlink" href="{rel}start.html">Or subscribe monthly</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap grid-2">
    <div>
      <p class="label">Back of pack</p>
      <hr class="gold-rule">
      <h2 class="display">The panel, unedited.</h2>
      <p class="lede">The facts panel is a legal document, not a design surface. It is
         reproduced here exactly as it is printed — black on white, full contrast, rules
         intact, nothing tinted purple.</p>
      <p class="data data--sm" style="color:#7A5CA8">LOT {p["lot"]} · INK-JETTED ON THE BASE</p>
    </div>
    <div>{facts_panel(p)}</div>
  </div>
</section>

<section class="section section--purple on-purple">
  <div class="wrap">
    <div class="section__head">
      <p class="label">What to expect</p>
      <hr class="gold-rule">
      <h2 class="display">Take it tonight. Then take it again tomorrow.</h2>
    </div>
    <div class="steps">
      <div class="step">
        <span class="n">WEEK 1</span>
        <h3 class="heading">Nothing, probably.</h3>
        <p>The first week is about the habit, not the ingredient. Put the jar somewhere
           you cannot miss it and take it at the same point in the meal each night.</p>
      </div>
      <div class="step">
        <span class="n">WEEK 3</span>
        <h3 class="heading">Most people notice something.</h3>
        <p>Not a change you would post about. The kind you only see looking back at
           the fortnight behind you.</p>
      </div>
      <div class="step">
        <span class="n">WEEK 4</span>
        <h3 class="heading">Decide.</h3>
        <p>Give it a month before you judge it. If it is not doing anything for you,
           stop — and because there is one ingredient, you know what you stopped.</p>
      </div>
    </div>
    <p class="disclaimer">{p["supports"]} This is a structure-and-function statement,
      not a medical claim. {p["state"]} is not intended to diagnose, treat, cure or
      prevent any disease.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <p class="label">Also in the range</p>
      <hr class="gold-rule">
      <h2 class="heading">Seven formulas, one family.</h2>
      <p style="margin-top:18px"><a class="textlink" href="{rel}range.html">Back to the range</a></p>
    </div>
    <div class="range">
{rel_cards}
    </div>
  </div>
</section>
''' + footer(rel)


def page_bundles():
    blocks = []
    for i, b in enumerate(BUNDLES):
        items = "".join(f'''<li>
          <span class="n">{BY_SLUG[s]["state"]}</span>
          <span class="i">{BY_SLUG[s]["ing"]}</span>
          <span class="d">{BY_SLUG[s]["dose"]}</span>
        </li>''' for s in b["items"])
        blocks.append(f'''
<section class="section section--purple on-purple">
  <div class="wrap">
    <div class="bundle">
      <div class="bundle__figure{" bundle__figure--photo" if has_photo(b["slug"]) else ""}">{
        photo(b["slug"], b["name"] + " — gift carton with amber jars, photographed overhead on linen", sizes="(max-width: 860px) 92vw, 440px")
        or carton(b["title"], [BY_SLUG[s]["state"] for s in b["items"]])}</div>
      <div>
        <p class="label">Bundle</p>
        <hr class="gold-rule">
        <h2 class="display">{b["name"]}</h2>
        <p class="lede">{b["line"]}</p>
        <p>{b["blurb"]}</p>
        <ul class="bundle__list">{items}</ul>
        <div class="product__buy">
          {buy_button(b)}
          <span class="price" style="color:#F4F1EC">₹{b["price"]}</span>
          <span class="data">SAVES ₹{b["saving"]}</span>
        </div>
      </div>
    </div>
  </div>
</section>''')
    return head("Bundles — monk manthra", "The Evening Three and The Morning Two.") \
        + header("bundles.html") + f'''
<section class="section section--tight">
  <div class="wrap">
    <div class="section__head">
      <p class="label">Bundles</p>
      <hr class="gold-rule">
      <h1 class="display">Named for a time of day, not a benefit.</h1>
      <p class="lede">A bundle is a slot in your evening or your morning, not a promise
         about an outcome. Two of them, and there will not be a third unless a third
         time of day appears.</p>
    </div>
  </div>
</section>
''' + "\n".join(blocks) + f'''
<section class="section">
  <div class="wrap center">
    <hr class="gold-rule gold-rule--center">
    <div class="quote">
      <p class="display">Seven supplements. One habit.</p>
    </div>
    <p style="margin-top:26px"><a class="btn btn--quiet" href="range.html">See the range</a></p>
  </div>
</section>
''' + footer()


def page_story():
    return head("The idea — monk manthra", "We sell consistency, not transformation.") \
        + header("story.html") + f'''
<section class="section section--tight">
  <div class="wrap wrap--narrow">
    <p class="label">The idea</p>
    <hr class="gold-rule">
    <h1 class="display">A manthra is one word, repeated, until it changes something.</h1>
    <p class="lede" style="margin-top:26px">That is also how a supplement works — a small
       dose, taken daily, until the effect compounds. The brand is built entirely on that
       single parallel, and every decision below traces back to it.</p>
  </div>
</section>

<section class="section section--purple on-purple">
  <div class="wrap">
    <div class="principles">
      <div class="principle">
        <p class="label">Positioning</p>
        <hr class="gold-rule">
        <p>Daily supplements for people who want to feel steady, not supercharged. We
           sell consistency, not transformation. The rest of the category shouts about
           performance; we would rather speak quietly about repetition.</p>
      </div>
      <div class="principle">
        <p class="label">Who it is for</p>
        <hr class="gold-rule">
        <p>People who already have a practice of some kind — yoga, running, therapy,
           cooking. People who read the ingredient panel before the front of the pack,
           and who are suspicious of hype and of anything that looks like a pharmacy.</p>
      </div>
      <div class="principle">
        <p class="label">What we hold to</p>
        <hr class="gold-rule">
        <p>Repetition over intensity. Show the dose — numbers are visible, never hidden.
           Earn the calm, because white space is the product and a crowded label is a
           nervous one.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
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
      <p>It draws once when a page loads, over 1.4 seconds, outward. Then it stops. It
         does not loop and it does not pulse, because a thing that repeats forever on a
         screen is not a practice, it is a nag.</p>
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
        <thead><tr>
          <th scope="col">We write this</th><th scope="col">Not this</th>
        </tr></thead>
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

<section class="strip-gold on-gold">
  <div class="wrap">
    <p class="label">Practice</p>
    <h2 class="heading">A word, repeated, is how anything changes.</h2>
  </div>
</section>
''' + footer()


def page_start():
    return head("Start — monk manthra", "Take it tonight. Then take it again tomorrow.") \
        + header("start.html") + f'''
<section class="section section--purple on-purple">
  <div class="wrap wrap--narrow center">
    {mark(72, draw=True, lock="2")}
    <p class="label" style="margin-top:26px">Start</p>
    <h1 class="display" style="margin-top:14px">Take it tonight.<br>Then take it again tomorrow.</h1>
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

<section class="section section--paper">
  <div class="wrap grid-2">
    <div>
      <p class="label">Subscription</p>
      <hr class="gold-rule">
      <h2 class="display">A jar arrives before the last one runs out.</h2>
      <p class="lede">Sixty capsules is roughly two months at one a day, so that is the
         interval we ship on. Change it, pause it, or stop it from any email we send —
         there is no call to make and no offer waiting on the other end of it.</p>
    </div>
    <div class="stack">
      <div class="table-scroll">
        <table class="dose-table">
          <thead><tr><th scope="col">Interval</th><th scope="col">Suits</th><th scope="col">Price</th></tr></thead>
          <tbody>
            <tr><td class="state">Monthly</td><td>90-capsule jars, or two a day</td><td class="num">−10%</td></tr>
            <tr><td class="state">Two-monthly</td><td>60-capsule jars at one a day</td><td class="num">−10%</td></tr>
            <tr><td class="state">One-off</td><td>Trying it</td><td class="num">Full</td></tr>
          </tbody>
        </table>
      </div>
      <p class="data data--sm" style="color:#7A5CA8;margin-top:18px">
        FREE SHIPPING OVER ₹1,500 · DISPATCHED IN 48 HOURS
      </p>
      <p style="margin-top:22px"><a class="btn" href="range.html">See the range</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow center">
    <hr class="gold-rule gold-rule--center">
    <p class="label">Questions</p>
    <h2 class="display" style="margin-top:14px">Can I take more than one?</h2>
    <p style="margin:22px auto 0">Yes — the range is built to be combined, which is what
       the bundles are. What you should not do is double a single dose to speed
       something up. The dose on the pack is the dose we have evidence for, and taking
       two of them does not make three weeks into one.</p>
    <p style="margin-top:26px"><a class="textlink" href="mailto:hello@monkmanthra.com">Ask us anything else</a></p>
  </div>
</section>
''' + footer()


# --------------------------------------------------------------------------
def favicon():
    """≤32px — one ring plus the seed."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" fill="#3A1F5C"/>
  <path d="{arc(35.84)}" fill="none" stroke="#E0C88C" stroke-width="6" stroke-linecap="round"/>
  <circle cx="50" cy="50" r="11" fill="#E0C88C"/>
</svg>'''


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print("  ", path, f"{len(content)//1024}kb")


if __name__ == "__main__":
    print("building monk manthra —")
    write("index.html", page_index())
    write("range.html", page_range())
    write("bundles.html", page_bundles())
    write("story.html", page_story())
    write("start.html", page_start())
    for p in PRODUCTS:
        write(f"products/{p['slug']}.html", page_product(p))
    write("assets/img/favicon.svg", favicon())
    print("done.")
