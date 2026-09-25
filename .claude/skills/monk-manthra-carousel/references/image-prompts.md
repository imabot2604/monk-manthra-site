# Writing Flow / Nano Banana image prompts

Used whenever a carousel slide (photo_slide or split_slide) needs a
photo that doesn't exist yet. The user generates these themselves in
Google Flow and sends the files back — you never generate images
yourself, only the prompts.

## First, resolve which photography mode applies

Ask yourself (or the user, if genuinely unclear) which of these the
carousel is:

- **Product or ingredient content** (a specific ingredient, the
  formula, the ritual of taking it) → **no hands, no models, no
  packaging.** This project's own `IMAGE-PROMPTS.md` sets that rule for
  product photography, and it's been the default for every ingredient
  carousel built so far (turmeric root/powder macro shots, the
  turmeric-and-milk motif). Object/macro only.
- **Editorial or topical content** (a sleep-science explainer, a
  general wellness topic not tied to one ingredient) → candid lifestyle
  photography **with real people is allowed**, but only once the user
  has said so for that carousel — it was an explicit call-out
  ("you can use models too... just to make a clean carousel"), not a
  standing default. If a new topical carousel comes up and it's not
  clear which mode applies, ask rather than assume — the two modes
  produce very different-feeling carousels and it's a brand decision,
  not a technical one.

## Prompt structure

Always three parts, written out in full so the user can paste directly
into Flow — don't make them assemble it:

1. **A shared scaffold paragraph**, held constant across every shot in
   the set: camera/lens language, lighting direction, color grade, and
   an explicit "no text, no logo, no watermark" (Flow sometimes tries to
   add on-image text or a fake logo unless told not to).
2. **A negative prompt line**, also shared across the set.
3. **One scene description per shot**, appended to the scaffold.

### Object/macro scaffold (product & ingredient content)

> Macro photograph, shallow depth of field, dramatic single-source
> lighting from the upper left, deep shadow falling away into
> near-black. [Subject line — describe only the actual subject, nothing
> else in frame]. Matte surfaces, no gloss, no plastic, no packaging of
> any kind, no labels, no text, no logos, no hands, no models, no props,
> no plants. Photographic realism, not illustration or a 3D render.
> Square, 1:1, ultra-high detail, editorial food-photography quality.

For a more premium/editorial push (this is the version that's actually
been used, after an early round felt too flat): add "shot as if on a
medium-format camera with a 100mm macro lens... warm rim light
separating the subject from the background... rich, moody colour
grade... the kind of image that could run in a Kinfolk or Cereal
magazine food story, not a stock-photo product shot."

Negative prompt: `hands, fingers, model, face, packaging, pouch, jar,
label, text, watermark, signature, logo, gloss, plastic, flat lighting,
harsh shadow, oversaturated, stock-photo lighting, gradient background
(digital-looking), lens flare, busy background, wood grain, marble
countertop, cartoon, CGI look, multiple light sources`

### Lifestyle scaffold (editorial/topical content, models explicitly OK)

> Natural, candid lifestyle photography, shot on a full-frame camera
> with a 35mm or 50mm lens, soft available light (window or early
> morning sun), warm and calm colour grade — muted, not saturated,
> nothing that reads as a gym-ad or stock-photo energy. Real, relaxed
> human presence, not posed at the camera. Square, 1:1, shallow depth of
> field. Photographic realism, not illustration or 3D render.

Negative prompt: `stock-photo smile, posed-at-camera, harsh flash,
oversaturated, gym-ad energy, text, watermark, logo, cartoon, CGI look`

## After the user sends photos back

1. Look at each one before using it — Flow output varies in quality and
   sometimes drifts from the brief (wrong crop, an extra prop, a subtly
   posed feel). Confirm each photo actually matches its intended scene
   before wiring it into a slide; don't assume file order matches your
   prompt order without checking.
2. Save into that carousel's own `photos/` folder (e.g.
   `instagram/<topic>/photos/slide-2.jpg`) — keep each carousel's photos
   in its own folder rather than a shared pool, so a later edit to one
   carousel never silently changes another's images.
3. Every Flow-generated photo carries a small sparkle watermark, almost
   always bottom-right. `photo_slide` and `split_slide` in
   `scripts/carousel_template.py` already include a `.corner-patch`
   element that blends it into the scrim/corner — you don't need to
   crop or edit the photo file itself.
