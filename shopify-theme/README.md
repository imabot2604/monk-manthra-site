# monk manthra — Shopify theme (Online Store 2.0)

Full storefront rebuild, replacing GitHub Pages as the live site once
finished. Not started blind — every file here has been checked the ways it
*can* be checked without a connected store (see "What's actually been
verified" below), same discipline as the rest of this repo.

## Status: chrome complete, one full page proven

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

**Not built yet:** the home page, the range/collection listing, bundles,
the idea, and start — index.html, range.html, bundles.html, story.html,
start.html's Liquid equivalents. The product page was built first because
it is the most constrained page on the site — the facts panel is a legal
document, Section Nine is explicit about that — so it's the page most worth
proving the pattern on before repeating it five more times.

## What's actually been verified, and how

There is no connected store yet, so nothing here has *rendered*. What could
be checked without one, was:

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

None of that is the same as a real render. Liquid's actual runtime
behaviour, Shopify's exact object shapes, and whether the design holds up
visually can only be confirmed once this is pushed to a real store and
opened in a theme preview.

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

## Next steps, in order

1. Create the Shopify store, run `composio link shopify`
2. Create the metafield **definitions** in `METAFIELDS.md` (admin UI —
   Composio's Shopify tools can set metafield values once definitions
   exist, but definition creation itself wasn't in the tool set found)
3. Push these files as a theme (via the Composio theme-asset tools, or the
   Shopify CLI / GitHub integration once the store exists)
4. Create the six products + two bundles, fill in their metafields
5. Open the theme preview — this is the first point any of this actually
   renders — and fix whatever a real render reveals that static analysis
   couldn't catch
6. Build the remaining five page types, now that the pattern is proven
