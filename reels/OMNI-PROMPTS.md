# Flow / Omni prompts — Reel 01

Four clips, 8s each, 9:16 vertical. Paste one at a time.

Every prompt names the palette explicitly. Left to itself a model will drift
warm-orange on anything involving turmeric and milk, and the brand has
exactly six colours.

Shared style suffix — append to all four if Flow lets you:

    Deep purple #3A1F5C background, gold #C2A053 and cream white #F4F1EC
    only. Single soft light source. Photographic, realistic, shot on a
    macro lens. Static camera. Calm and unhurried. No text, no captions,
    no logos, no graphics, no people.

---

## Clip 1 — the ripple  (0:00-0:07)

    Extreme macro shot from directly above, a single drop of warm golden
    liquid falling into still cream-white milk in a dark ceramic bowl. One
    slow concentric ripple travels outward from the point of impact and
    fades. Deep purple shadows, warm gold highlight. Soft window light from
    the left. Very shallow depth of field. Static camera, no camera
    movement. Slow motion. Photographic, realistic, no text.

Most important clip in the reel: the ripple is the mark's own geometry, a
seed at the centre with rings travelling outward. If only one clip is worth
regenerating until it is right, this is it.

Ask for **one** ripple. Models default to a busy splash with many rings, and
a splash says the opposite of what the voiceover is saying.

## Clip 2 — the powder  (0:07-0:14)

    Macro tabletop shot, a small brass spoon slowly lifting fine golden
    turmeric powder from a matte white ceramic dish, a thin stream of
    powder falling back into the dish. Warm side light from the left, deep
    purple background falling into shadow. Static camera. Slow and
    unhurried. Visible texture and grain of the powder. Photographic,
    realistic, no hands visible, no text.

"No hands visible" is deliberate — a hand introduces a person, and every
other shot is still life. If Flow insists on a hand, take it, but keep it
out of frame edges.

## Clip 3 — the three ingredients  (0:14-0:21)

    Macro shot, three small white ceramic dishes in a row on dark stone —
    one holding golden turmeric powder, one holding fresh ginger root, one
    holding two cinnamon quills. Very slow push in along the row. Deep
    purple background, single warm light from the upper left, deep shadows.
    Completely still, no hands, no movement other than the camera.
    Photographic, realistic, no text.

Fallback if the three dishes come out muddled: shoot them as three separate
3-second clips, one ingredient each, and cut on the voiceover's own commas
in "Turmeric, ginger, cinnamon." Cheaper than fighting the prompt, and the
cut lands better.

## Clip 4 — the pouch  (0:21-0:28)

    A plain matte white stand-up pouch, completely blank, with no text, no
    label, no printing and no design of any kind on it, standing upright on
    a dark stone surface. Warm side light from the left, deep shadow behind
    it. Camera perfectly static. Steam drifts slowly across the frame from
    the left. Nothing else moves. Photographic product photography,
    generous empty space around the pouch, no text anywhere in the image.

Blankness is stated four ways on purpose. One mention will not stop a model
decorating a pack, and an invented label is worse than no label — it reads
as a real brand that is not ours.

The real mark is composited on afterwards from `assets/img/instagram-pfp.png`
artwork, so it is exact rather than approximated.

---

## Picking takes

Reject a take for any of these, they are cheaper to regenerate than to fix:

- Any text, letterform or logo anywhere in frame
- A colour outside the six — orange, teal and green all creep in
- Camera drift where the prompt said static
- More than one ripple in clip 1
- A busy or cluttered frame; Section Eleven wants generous empty space

Save takes as `reels/footage/clip-1.mp4` … `clip-4.mp4`.
