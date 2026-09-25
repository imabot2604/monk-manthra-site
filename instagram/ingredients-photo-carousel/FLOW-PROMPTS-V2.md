# Ingredient carousels — elevated aesthetic prompts (v2)

Just 6 photos, reused across all 14 ingredient carousels (round-robin) —
not one per ingredient. Same locked subject as before (turmeric powder
meeting milk, no packets, no hands/models), but the prompt language is
pushed harder toward an editorial, magazine-food-photography look
instead of a plain product shot — richer light, shallower focus, a
proper colour grade.

These replace the original 6 in `../golden-milk-photo-carousel/photos/`
(slide-1.jpg through slide-6.jpg) — both this carousel and the Golden
Milk carousel already posted read off that same folder, so regenerating
these 6 upgrades every carousel at once.

## Prompt scaffold (elevated)

> Editorial macro food photography, shot as if on a medium-format camera
> with a 100mm macro lens, extremely shallow depth of field with soft,
> creamy bokeh. Warm, directional key light from the upper left with a
> subtle golden rim light separating the subject from the background,
> giving it real dimension. Rich, moody colour grade — deep warm shadows
> that still hold detail, luminous golden highlights, nothing blown out.
> Subject: turmeric powder (saturated golden-yellow) and dairy milk (warm
> ivory-white), nothing else in frame. Matte, tactile surfaces — no
> gloss, no plastic. Background falls into a soft near-black or deep
> aubergine-purple vignette. No packaging of any kind, no labels, no
> text, no logos, no hands, no models, no props, no plants. Photographic
> realism, not illustration or a 3D render. Square, 1:1, ultra-high
> detail — the kind of image that could run in a Kinfolk or Cereal
> magazine food story, not a stock-photo product shot.

**Negative prompt:** hands, fingers, model, face, packaging, pouch, jar,
label, text, watermark, signature, logo, gloss, plastic, flat lighting,
harsh shadow, oversaturated, stock-photo lighting, gradient background
(digital-looking), lens flare, busy background, wood grain, marble
countertop, cartoon, CGI look, multiple light sources

## The 6 scenes

1. **Splash** (`slide-1.jpg`) — turmeric powder mid-fall into milk,
   frozen at the exact moment of impact, a crown-shaped splash thrown
   upward.
2. **First swirl** (`slide-2.jpg`) — overhead, powder just landed on the
   milk surface, blooming outward, most of the surface still
   ivory-white.
3. **The pour** (`slide-3.jpg`) — golden milk poured in a thin stream
   into a matte ceramic cup, a wisp of steam rising, warm rim light on
   the stream.
4. **Full marble** (`slide-4.jpg`) — extreme close-up, top-down, powder
   and milk mid-mix, dense marbled pattern filling the frame.
5. **Lifted** (`slide-5.jpg`) — a ceramic spoon lifts a thick ribbon of
   golden milk out of the cup, caught mid-air, rim-lit against the dark
   ground.
6. **Fully mixed** (`slide-6.jpg`) — extreme macro of the finished golden
   milk's smooth texture, tiny bubbles catching the golden highlight, no
   edges visible.

## Once generated

Overwrite the 6 files in `../golden-milk-photo-carousel/photos/`, then
rebuild everything that reads off them:

```bash
cd ../golden-milk-photo-carousel && python3 build_photo_carousel.py
cd ../ingredients-photo-carousel && python3 build_ingredient_carousels.py
```

(The Golden Milk carousel post already published won't update itself —
only a fresh publish would use the new images.)
