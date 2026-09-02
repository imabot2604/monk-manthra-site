# Metafields this theme expects

Every product needs these, under the namespace `monkmanthra`.

**Correction to an earlier claim in this file:** definitions are *not*
required first. All 15 were written directly via `productCreate`'s
`metafields` input and read back correctly with the right types — verified
on the live store. Creating definitions in *Settings → Custom data →
Products* is still worth doing, because without them the values are
invisible in the admin product editor (they work fine in Liquid either
way), but it is a convenience, not a prerequisite.

| Key | Type | Example | Maps to (build.py) |
|---|---|---|---|
| `ingredient_label` | Single line text | "ASHWAGANDHA KSM-66" | `ing` — the small-caps line under the name on every card and product header |
| `tagline` | Single line text | "600mg of ashwagandha. That is the whole formula." | `line` |
| `blurb` | Multi-line text | The paragraph on the product page | `blurb` |
| `dose` | Single line text | "600mg" | `dose` |
| `count` | Single line text | "60 capsules" | `count` — its leading number is "servings per container" on the facts panel |
| `serving` | Single line text | "1 capsule" | `per` |
| `when_to_take` | Single line text | "Evening" | `when` |
| `supports_claim` | Multi-line text | The structure-and-function line | `supports` |
| `facts` | JSON | `[{"name":"Ashwagandha root extract","value":"600mg"},{"name":"(KSM-66, 5% withanolides)","value":"","indent":true}]` | `facts` |
| `other_ingredients` | Multi-line text | "hypromellose capsule, rice flour." | `other` |
| `allergens` | Single line text | "Contains no gluten, dairy, or soy." | *(was hardcoded identically on all 6 — now genuinely per-product, since that was never actually guaranteed to be true of a seventh product)* |
| `directions` | Multi-line text | "one capsule with the evening meal." | `directions` |
| `lot_code` | Single line text | "MM-2611" | `lot` |
| `best_before` | Single line text | "2028-04" | *(was hardcoded identically on all 6 — same fix as allergens)* |
| `tonal_band` | Color | `#7A5CA8` | `band` — Section Seven's 4mm tonal band |

**Deliberately dropped, not ported:**

- `shopify_variant_id` — existed only to bridge an external static site *into*
  Shopify. Inside Shopify, a product page already has its own variant; there
  is nothing to bridge.
- `pack` / `ing_lines` — existed to drive the drawn-SVG jar/pouch/carton
  placeholder (`jar()`/`pouch()`/`carton()` in build.py), which stood in for
  photography that wasn't ready yet on GitHub Pages. This theme assumes real
  product photography is uploaded before launch, via Shopify's own product
  images — reasonable for an actual store, and it avoids porting a
  from-scratch SVG generator into Liquid for a case that shouldn't arise here.

**Product title = the state** ("Calm"), not the ingredient — Section Seven is
explicit that products are named for the state and verified by the
ingredient, never the reverse. `ingredient_label` carries that verification
line; `product.title` carries the name.
