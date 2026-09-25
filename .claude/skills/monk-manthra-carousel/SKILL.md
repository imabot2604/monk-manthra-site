---
name: monk-manthra-carousel
description: Build and publish Instagram carousel posts for the monk manthra supplements brand (monk-manthra-site) — ingredient explainers, product carousels, brand-intro posts, or topical/educational series (e.g. sleep science). Use this whenever the user asks to make, design, build, or post an Instagram carousel, a set of slides, or content for @monkmanthra, even if they don't name this skill directly — phrases like "make a carousel about X", "post about the ingredients", "do one for sleep/circadian rhythm", or "give me prompts so I can generate images for a post" for this project should all trigger it. Covers slide design (five reusable templates matching the brand's deep-purple/gold visual system), writing Flow/Nano-Banana image-generation prompts, rendering slides via headless Chrome, and publishing to Instagram through the existing composio-connected pipeline.
---

# monk manthra Instagram carousels

This packages the carousel workflow built over many iterations this
project — the visual system, the rendering pipeline, the publishing
script, and the content rules that kept coming up. The goal is that a
fresh session can produce something that looks like it belongs next to
every other post on the account, without re-deriving any of this from
scratch or re-making mistakes that were already fixed once (the ones
called out below as "earlier bug" were each real, not hypothetical).

## The shape of the workflow

1. **Figure out what this carousel is about** and which photography mode
   applies (see "Photography mode" below) — ask if genuinely unclear,
   don't guess on the mode specifically, since it's a brand decision.
2. **Design the slide sequence** using the five templates in
   `scripts/carousel_template.py` (read that file — it documents each
   template inline, including when to reach for which one). A typical
   arc: `cover_slide` → 2-4 content slides in whatever mix of
   `photo_slide` / `split_slide` / `info_slide` fits → `gradient_slide`.
   4-7 slides total; don't pad to hit a number.
3. **If a slide needs a photo that doesn't exist yet**, write prompts
   following `references/image-prompts.md` and hand them to the user —
   you don't generate images yourself. Wait for the photos before
   building that slide.
4. **Render every slide**: copy `scripts/carousel_template.py` into the
   carousel's own folder (e.g. `instagram/<topic>/build_<topic>.py`),
   fill in `SLIDES`, run it. Each slide becomes a real `file://` HTML
   page shot at 1080×1080 by headless Chrome — see the module docstring
   for exactly why (real CSS, real font/flexbox behavior, not
   hand-placed text).
5. **Convert PNG → JPEG** for every final slide — Instagram's publishing
   API requires JPEG, not PNG:
   ```bash
   sips -s format jpeg slide-1.png --out slide-1.jpg
   ```
6. **Write `caption.txt`**: a caption that mirrors the slide arc (hook →
   substance → close), ~8-10 relevant hashtags, always ending with the
   brand sign-off line:
   > monk manthra — daily supplements for people who want to feel steady, not supercharged.
7. **Show everything before publishing anything.** Send every rendered
   slide and the caption to the user. This isn't a formality — the
   content rules below (dosage, health claims, product naming) are
   exactly the kind of thing worth a human glance before it goes out
   publicly, and the visual design (text placement, photo crop, hook
   wording) is inherently a matter of taste that's cheaper to adjust
   before publishing than after.
8. **Publish only on an explicit go-ahead in the current conversation**
   — "post this", "go ahead", "publish it", something unambiguous said
   *now*. A standing preference from earlier in a much longer session
   doesn't carry forward to a new post; each publish is its own
   decision. When you do have the go-ahead:
   ```bash
   python3 scripts/publish_carousel.py <folder-of-jpgs> --caption-file caption.txt
   ```
   This shells out to the `composio` CLI (already connected to the
   @monkmanthra Instagram Business account in this environment) to
   create one container per image, bundle them into a carousel
   container, and publish. It prints every container id and the final
   live permalink — that permalink is your confirmation, hand it back to
   the user. Pass `--dry-run` to build containers without publishing.

   **If asked to "delete" a post or "save as draft"**: say plainly that
   neither is possible through the API — Instagram's Graph API has no
   delete-media endpoint and no way to reach the app's native Drafts.
   Only manual deletion in the Instagram app itself works. Don't imply
   otherwise or attempt a workaround.

## Photography mode

Two modes, and which one applies changes the prompts substantially —
see `references/image-prompts.md` for the full scaffolds:

- **Product/ingredient content** → object/macro photography only, no
  hands, no models, no packaging. This is the standing default,
  inherited from this project's own `IMAGE-PROMPTS.md` brand rule.
- **Editorial/topical content** (a science-explainer series, a general
  wellness topic) → candid lifestyle photography with real people is
  allowed, but only when the user has said so for that specific
  carousel. Ask if it's not already clear from context which mode a new
  topical idea falls into.

## Content rules (apply every time, not just when reminded)

These came out of real corrections during development, not
hypothetical caution — each one fixed something that had already gone
out slightly wrong.

- **No specific dosage or per-ingredient amount** unless the user has
  explicitly confirmed real, final numbers in the current conversation.
  This brand's actual supplement-facts panel is marked "TBC" as of this
  writing. Name ingredients without amounts by default.
- **Health claims are structure-and-function statements, never
  treatment claims.** "Contributes to the normal function of joints" and
  "supports the body's normal antioxidant processes" are the right
  register; "cures," "treats," "prevents," or naming a specific
  condition are not. Whenever a caption lists this kind of benefit,
  close with: *"These are structure-and-function statements, not
  medical claims. Not intended to diagnose, treat, cure or prevent any
  disease."* Also don't overclaim mechanism — e.g. turmeric is framed as
  part of an evening ritual, not as a sleep aid, because curcumin isn't
  actually a sedative and saying so would be the kind of claim this rule
  exists to prevent.
- **Only name "Golden Milk" (or any specific product) when the carousel
  is explicitly about that product.** Ingredient-only carousels and
  topical/educational series (the sleep series is the example so far)
  refer to "the blend" / "the scoop" generically, or don't reference a
  product at all. This was an explicit standing instruction, not a
  style preference — don't reintroduce the product name into that
  content by default.
- **Reuse the exact brand mark SVG and CSS custom properties** in
  `scripts/carousel_template.py` rather than inventing new colors, a new
  mark, or new fonts. The visual consistency across every post *is* the
  deliverable here — a carousel that looks close-but-different stands
  out for the wrong reason.

## Files in this skill

- `scripts/carousel_template.py` — the five slide-template functions +
  the headless-Chrome render pipeline. Copy this per new carousel.
- `scripts/publish_carousel.py` — the Instagram publisher. Used as-is,
  never copied/edited (it's generic across every carousel folder).
- `references/image-prompts.md` — how to write Flow prompts, including
  both photography-mode scaffolds and negative prompts in full.
