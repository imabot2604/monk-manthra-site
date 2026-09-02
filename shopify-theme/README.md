# monk manthra — Shopify theme (Online Store 2.0)

Full storefront rebuild, replacing GitHub Pages as the live site once
finished. Not started blind — every file here has been checked the ways it
*can* be checked without a connected store (see "What's actually been
verified" below), same discipline as the rest of this repo.

## Status: live on the store as an unpublished theme

Theme id `189397303592`, name "monk manthra", role `unpublished` — the
store's live Horizon theme is untouched. All 8 products, 2 collections and
2 pages exist on `monkmanthra.myshopify.com`, created via the Admin API.
Products are **DRAFT** on purpose (placeholder facts panels, no FSSAI
clearance), which is why storefront product/collection URLs 404 until they
are activated behind a store password.

## What was chrome-only before

**Built and checked:**
- `layout/theme.liquid` — the shell (`content_for_header`/`content_for_layout`
  in the right places, both required by Shopify)
- `sections/header.liquid`, `sections/footer.liquid` — nav from a real
  Shopify menu, footer from real collections, full legal disclaimer intact
- `sections/cart-drawer.liquid` + `snippets/cart-toggle.liquid` — Shopify's
  own Ajax Cart API (no token needed, first-party), server-rendered so it's
  correct before any JS runs, section-rendering refresh on every add/change
- `snippets/mark.liquid`, `snippets/lockup.liquid` — the mark's geometry,
  precomputed and verified byte-identical against `build.py`'s `arc()`
- `sections/main-product.liquid` + `templates/product.json` — a complete
  product page: figure, meta, blurb, buy button, **facts panel**, "what to
  expect," related products
- `snippets/facts-panel.liquid`, `snippets/buy-button.liquid`,
  `snippets/product-card.liquid` — the reusable pieces the product page
  (and later, the range grid) are built from
- `assets/theme.css` — ported unchanged from the live site (it's plain CSS,
  no Python or Liquid in it)
- `assets/theme.js` — the mark/reduction/floating-header logic ported
  unchanged; the cart logic is new and Shopify-native
- `METAFIELDS.md` — the exact contract every product needs, cross-checked:
  every metafield the theme references is documented, and every documented
  one is actually used — no drift either direction

**Since built, to make the theme actually loadable:** `sections/hero.liquid`,
`range-grid.liquid`, `main-collection.liquid`, `main-cart.liquid`,
`main-page.liquid`; `templates/index.json`, `collection.json`, `cart.json`,
`page.json`, `404.liquid`, `search.liquid`; `locales/en.default.json` and
`config/settings_data.json` — Shopify refuses to load a theme without
locales, and 404s every page type lacking a template.

**Still not built:** dedicated bundles, "the idea" and "start" page designs.
Those exist as real Shopify pages with content, rendering through the
generic `main-page.liquid`, rather than the bespoke layouts `build.py`
gives them.

## What's actually been verified, and how

Static checks run before upload (all still worth re-running after edits):

- **The mark's geometry** — Liquid has no `sin`/`cos`, so the three ring
  paths in `mark.liquid` are hardcoded, not computed. Verified by running
  the exact same arithmetic in Python and diffing the output against
  `build.py`'s proven `arc()` function: identical, character for character.
- **Every `{% schema %}` block and every `templates/*.json` file** — parsed
  as JSON. A malformed schema doesn't error visibly in Shopify; it just
  silently kills the section. All parse clean.
- **Every Liquid tag** — `{% %}`/`{{ }}` delimiter counts balanced, and
  every `if/endif`, `for/endfor`, `unless/endunless`, `comment/endcomment`,
  `capture/endcapture`, `case/endcase` pair matched, across every file.
- **Every `{% render %}` and `{% section %}` call** — cross-referenced
  against the actual snippet/section files on disk. Nothing points at a
  file that doesn't exist.
- **The metafield contract** — every `product.metafields.monkmanthra.*`
  reference in the theme cross-checked against `METAFIELDS.md`; nothing
  used-but-undocumented, nothing documented-but-unused.

**Then verified against the real store.** All 29 files uploaded to theme
`189397303592`; the homepage renders our actual markup — `class="hero
on-purple"`, `class="wordmark"`, and the heading "Six supplements. One
habit." all present in the served HTML. One upload failed on first attempt
and was fixed: Shopify rejects a `settings_schema.json` whose `theme_info`
lacks `theme_support_url` (or `theme_support_email`, but not both).

Product and collection URLs still 404, because the products are DRAFT —
that is the intended state, not a bug. Full-page rendering with real
product data is unverified until they are activated behind a store
password.

## One real design decision, made along the way

Two bugs were caught and fixed *while building this*, not after:

1. **Mark colour.** `.on-purple .mark` in the live CSS is an ancestor
   selector — colour comes from whatever section wraps the mark, never
   from a class on the mark itself (matching `build.py`'s `mark()`, which
   has no colour parameter at all). The first draft of `mark.liquid` added
   an `on-purple` class directly onto the `<svg>`, which doesn't match that
   selector shape and would have silently rendered the wrong colours on
   every dark or gold background. Fixed before anything else was built on
   top of it.
2. **The cart drawer had to become a section, not a snippet.** Shopify's
   Ajax Cart API can only re-render actual sections after a mutation
   (`fetch('/cart/change.js', { sections: 'cart-drawer' })` returns
   `{ sections: { "cart-drawer": "<html>" } }`) — snippets aren't
   addressable that way. Caught before `theme.js` was written around the
   wrong assumption.

## Two metafields fixed a placeholder, not just ported it

`build.py`'s facts panel hardcoded the same allergen line
("Contains no gluten, dairy, or soy.") and the same expiry
("best before end 2028-04") identically across all six products — true by
coincidence in the current data, not guaranteed for a seventh. `allergens`
and `best_before` are real per-product metafields here instead of copied
static text, so a product that actually contains soy won't silently claim
otherwise.

## Done

1. ~~Store connected~~ — `monkmanthra.myshopify.com`, INR, professional plan
2. ~~Products created~~ — 6 products + 2 bundles, DRAFT, with all metafields
   and prices, photography pulled from the GitHub Pages URLs
3. ~~Collections~~ — `the-range` (6), `bundles` (2)
4. ~~Pages + menu~~ — `/pages/the-idea`, `/pages/start`; main menu rewired
   to The range / Bundles / The idea / Start
5. ~~Theme uploaded~~ — unpublished, live Horizon untouched

## Next

1. Turn on **Online Store → Preferences → Restrict store access** (no API
   exists for this; admin UI only — confirmed by schema introspection)
2. Activate the 8 products so every page renders with real data
3. Walk the preview and fix what static analysis could not catch
4. Fix the money format — the store renders `Rs. 1,450`, the design wants
   `₹1,450`. Settings → General → Currency formatting
5. Rename the store from "My Store"
6. Build bespoke bundles / the-idea / start layouts (they currently fall
   through the generic `main-page.liquid`)

## Known gaps

- **Bundle pages use the product template**, which renders a Supplement
  Facts panel. A carton of three jars has no single panel — each product
  inside has its own. Bundles were created without facts metafields so the
  panel renders empty rather than wrong, but they need their own template.
- **Header nav has no "section active" state.** Shopify menus expose
  `link.active` (current page) but no parent/ancestor relationship, so the
  `data-section` state the GitHub Pages nav uses on product pages has no
  equivalent yet.
