# monk manthra — website

A static site built to *Brand & Visual Guidelines v1.0 (2026)*. No build
dependencies beyond Python 3 and Pillow, no framework, no JavaScript beyond a
40-line file whose only job is drawing the mark once.

```bash
python3 build.py                 # emit the pages
python3 -m http.server 4321      # serve them
```

**Also in this repo:** `shopify-theme/` — a from-scratch Shopify Online
Store 2.0 theme meant to replace this site once finished. See
`shopify-theme/README.md` for status; it currently has the full chrome
(header, footer, cart) and one complete page (product) proven out, with the
remaining page types still to build.

## Layout

```
build.py                 all page content and markup, in one file
process-images.py        drop-in tool for new product photography
assets/css/site.css      the whole design system
assets/js/site.js        the mark: draws once, 1.4s, outward, then never again
assets/img/products/     photography, at 1024w and 700w
index.html  range.html  bundles.html  story.html  start.html
products/rest.html … build.html
```

`build.py` holds every product, price, facts panel and paragraph of copy as
data, then renders the pages from it — so the six product pages cannot drift
apart, and adding a seventh product is a dict entry.

## How the guide is enforced

Each rule below lives in exactly one place, commented where it sits.

| Guide | Where it is enforced |
|---|---|
| 60/30/10 — half white, purple, gold | Half white is `body`. Purple appears only as full-bleed `.section--purple` bands. Gold is a 34px rule, a button, and one slim strip per page. |
| Body text is only Deep Purple or Ink | `body { color: var(--deep-purple) }`. `#7A5CA8` is scoped to `.label`, rules and sub-labels — it never carries running text. |
| Gold never fills more than a tenth of a surface | One `.strip-gold` per page, ~7% of page height. |
| Never bold a headline | `h1–h4 { font-weight: 300 }`, and `.display` is 200. There is no bold heading rule to reach for. |
| Fraunces lowercase, tracking .13–.16em | `.wordmark { letter-spacing: 0.15em; text-transform: lowercase }` |
| Every checkable number in Plex Mono | `.data`, `.facts`, `.card__price`, `.dose-table td.num`, and the pack renderings — all `--mono`, all `tabular-nums`. |
| Mark: gold seed, gap at top, arcs 20°–340°, 1.6× steps | `arc()` in `build.py` computes the geometry from `SEED_R` and `RING_R`; nothing is hand-drawn. |
| Gold appears exactly twice — seed and outer ring | `.mark .seed` and `.mark .ring--3`. Rings 1 and 2 are purple. |
| Reduction: ≥96px three rings · 48–95 two · ≤32 one + seed | `applyReduction()` measures each mark and sets `data-rings`. |
| Clear space = one seed diameter | `--seed: 10px`, `.lockup { padding: var(--seed) }`, `--clear` for packaging-scale margins. |
| Nothing enters the rings | No mark anywhere has a child element. |
| The mark draws once, 1.4s, outward. Never loops | `site.js` runs it once with `animation-fill-mode: both`, then drops `data-draw`. Reduced-motion skips straight to the drawn state. |
| Front of pack: mark, wordmark, state, ingredient only | `jar()` / `pouch()` / `carton()` draw those four, plus dose and count in mono at the base. |
| Products separated by a 4mm tonal band from the core palette | `.card__band`, coloured by `--band` from each product's `band` key. No product introduces a new colour. |
| One-word product names, never numbered or lettered | Enforced by the data: `state` is one word, and no product carries an index. |
| Bundles named for a time of day | *The Evening Three*, *The Morning Two*. |
| Facts panel is a legal document | `.facts` is `#000` on `#FFF`, Plex Mono, heavy rules intact, 6pt floor, never tinted. |
| Structure-and-function claims only | Each product's `supports` line, printed under the required disclaimer. |
| Plain verbs, no exclamation marks, no urgency | There is not one exclamation mark in `build.py`. |

## Single theme, deliberately

The guide makes Half White `#F4F1EC` the default ground and fixes the 60/30/10
ratio. A dark-mode inversion would break that ratio, so the site commits to one
visual world and paints every colour explicitly rather than inheriting a host
background.

## What is placeholder and needs a real decision

- **Prices.** `₹890`–`₹2,290` and the bundle savings are invented. Nothing in the
  guide sets them.
- **Facts panels.** Plausible and correctly formatted, but the actual amounts,
  excipients and allergen lines must come from your formulator.
- **The disclaimer.** A generic structure-and-function block. Section Twelve is
  explicit that this is design guidance, not legal advice — a regulatory
  consultant in each selling market has to sign off every pack and every product
  page before print. The site has an India-facing footer; FSSAI nutraceutical
  declarations are not yet in it.
- **Lot codes and expiry** (`MM-2604`, `best before end 2028-04`) are illustrative.
- **`hello@monkmanthra.com` and the phone number** are taken from the guide's own
  stationery mock.
- **Add to order / Subscribe** are links to `start.html`, not a cart — unless
  Shopify is configured, see below.

## Selling on Shopify

The site stays headless: `build.py` keeps every product's copy, design and
facts panel; Shopify holds price, stock, and checkout. Nothing on the page
changes — the cart is a drawer that opens over the existing design, using the
same tokens (half white ground, deep purple ink, one gold action).

**It is completely inert until you fill in three things.** Right now
`SHOP["domain"]` in `build.py` still says `YOUR-STORE`, so `build.py` never
emits the cart toggle, never loads `shop.js`, and every "Add to order" button
is the same plain link to `start.html` it always was. Confirmed by grepping a
built page for `cart-toggle` — zero matches until this is configured.

**1. A store.** Start a Shopify trial and note the `*.myshopify.com` domain —
that goes in `SHOP["domain"]`.

**2. A Storefront API token.** In Shopify admin: *Settings → Apps and sales
channels → Develop apps → Create an app.* Under *Configuration*, enable the
**Storefront API** and grant it cart read/write scopes. Install the app, then
copy the **Storefront API access token** — not the Admin API token. The
Storefront token is meant to sit in client-side code; Shopify scopes it to
cart and product read access only, nothing an attacker could do damage with.
The Admin token is a real secret and must never go in this file. That goes in
`SHOP["token"]`.

**3. A variant ID per product.** In Shopify admin, open a product, open the
variant, and its GraphQL ID is `gid://shopify/ProductVariant/` followed by the
numeric ID in the page's URL. Paste the full `gid://…` string — not the bare
number — into that product's `shopify_variant_id` key in `build.py` (see the
`calm` entry in `PRODUCTS` for the exact spot). Every product without one
keeps linking straight to `start.html`, so you can light products up one at a
time.

Then:

```bash
python3 build.py && git add -A && git commit -m "Connect Shopify" && git push
```

**How it works once live:** `assets/js/shop.js` talks to Shopify's Storefront
API (GraphQL) directly from the browser — no backend needed, so this still
runs on GitHub Pages. It creates a cart on the first add, persists the cart ID
in `localStorage` so it survives a reload, and the drawer's Checkout button
sends the customer to Shopify's own hosted checkout — that's also where card
details belong; this site never touches them. Verified against a mocked
Storefront API before shipping: add → drawer opens, badge updates, line item
renders, checkout link resolves to Shopify's real `checkoutUrl`.

**What Shopify does not solve on its own:** subscriptions need a separate app
(Recharge, Loop, Appstle); COD needs enabling in Shopify's payment settings;
and none of this replaces the FSSAI licence and real facts-panel data the site
still needs before any of it goes live — see the placeholder list above.

## Photography

See `IMAGE-PROMPTS.md` for the shot list, the constant preamble, and the two
issues in the current set worth regenerating.
