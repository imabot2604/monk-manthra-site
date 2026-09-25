# Turmeric carousel — 6 image prompts

Turmeric only — no milk, no splash concept. The root and the powder, on
their own. No packets, no hands, no models, same as every other carousel
in this project. Editorial-macro language so the result matches the
reference post's dramatic quality (instagram.com/p/DdJ5o76kz9z/) rather
than a flat product shot.

Paste each scaffold + scene into Google Flow as one prompt.

## Scaffold (same for all 6)

> Editorial macro food photography, shot as if on a medium-format camera
> with a 100mm macro lens, extremely shallow depth of field with soft,
> creamy bokeh. Warm, directional key light from the upper left with a
> subtle golden rim light separating the subject from the background,
> giving it real dimension. Rich, moody colour grade — deep warm shadows
> that still hold detail, luminous golden-orange highlights, nothing
> blown out. Subject: turmeric root and/or turmeric powder only, nothing
> else in frame. Matte, tactile surfaces — no gloss, no plastic.
> Background falls into a soft near-black or deep aubergine-purple
> vignette. No packaging of any kind, no labels, no text, no logos, no
> hands, no models, no props, no other spices, no plants. Photographic
> realism, not illustration or a 3D render. Square, 1:1, ultra-high
> detail — the kind of image that could run in a Kinfolk or Cereal
> magazine food story, not a stock-photo product shot.

**Negative prompt (same for all 6):** hands, fingers, model, face,
packaging, pouch, jar, label, text, watermark, signature, logo, gloss,
plastic, flat lighting, harsh shadow, oversaturated, stock-photo
lighting, gradient background (digital-looking), lens flare, busy
background, wood grain, marble countertop, cartoon, CGI look, multiple
light sources, milk, liquid, splash, other spices

## The 6 scenes

### 1 · The root, cut open (cover slide)
> [scaffold] A single fresh turmeric root, sliced clean through the
> middle, resting cut-side up — the vivid deep-orange interior exposed
> and in sharp focus, the rough tan skin visible at the edges, everything
> else falling into soft shadow.

### 2 · The powder mound
> [scaffold] Directly overhead, a small conical mound of fine turmeric
> powder sitting on a plain near-black matte surface, its peak catching
> the key light, the texture of the powder visible in extreme detail at
> the edges of the mound.

### 3 · Root slices, fanned
> [scaffold] Several thin cross-section slices of turmeric root fanned
> out slightly overlapping on a dark matte surface, each slice showing
> its own ring pattern, side-lit so the translucent edges glow slightly.

### 4 · The powder veil
> [scaffold] A fine, cloud-like veil of turmeric powder caught mid-fall
> against a near-black background, individual particles visible and
   > sharp where the light catches them, the cloud dispersing outward.

### 5 · Root and powder together
> [scaffold] One small whole turmeric root resting on a bed of loose
> turmeric powder, raw and processed forms side by side, extreme macro,
> shallow focus on the root with the powder softly blurred beneath it.

### 6 · Powder texture, extreme macro
> [scaffold] Extreme close-up filling the entire frame with turmeric
> powder's texture alone — fine grains and soft micro-shadows between
> them, like a golden sand dune, one raking light source from the side
> to bring out every grain.

## Once generated

Save as `slide-1.jpg` through `slide-6.jpg` in
`../../golden-milk-photo-carousel/photos/` (the shared photo pool every
carousel in this project reads from), then rebuild:

```bash
cd ../.. && python3 golden-milk-photo-carousel/build_photo_carousel.py
cd ingredients-photo-carousel && python3 build_ingredient_carousels.py
```

Note: overwriting that shared folder changes the Golden Milk carousel's
photos too, since it reads from the same 6 files. If you want turmeric's
own photos kept separate from that carousel, save them into
`ingredients-photo-carousel/photos/` instead and say so — the build
script would need a one-line change to point at that folder for this
ingredient.
