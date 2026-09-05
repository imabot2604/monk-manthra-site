---
workflow: general-video
flow: companion
---

# Reel 01 — "One word, repeated"

First post on @monkmanthra (0 posts, 0 followers). Introduces the idea and
the name. Sells nothing: no FSSAI licence yet, and nothing on the store we
want traffic on.

- 1080x1920, 9:16, ~29s, 24fps (footage is 24fps; matching avoids a cadence judder)
- Narrated. VO already rendered, one wav per line, in `../vo/af_heart-*.wav`
- Hybrid: supplied generated footage intercut with built motion graphics

## Script and VO

Full script: `../reel-01-SCRIPT.md`. VO is final and must not be
re-rendered — the brand name is fed to the engine as "mantra" so it is not
read with an English *th*. Every visible spelling stays "manthra".

## Division of labour

Motion graphics carry every word, number and exact colour. Footage carries
texture and light. Cuts land on the VO's pauses, never mid-phrase.

## Footage: two clips, not four

Supplied: `Spoon_lifting_turmeric_powder` and `Ceramic_dishes_with_spices`,
both 1920x1080, 8s, 24fps. The ripple (clip 1) and pouch (clip 4) were not
generated, so motion graphics cover both — which is fine, and for the ripple
arguably better: the mark *is* a seed with rings travelling outward, so it
can be drawn rather than filmed.

Two defects in the supplied footage, both handled by the same decision:

1. A ✦ watermark sits bottom-right in both clips, inside the rightmost 20%
   of width and bottom 25% of height.
2. The footage's background purple is #271C29 / #3E2B42 — warmer and darker
   than brand #3A1F5C.

**Full-bleed 9:16 centre crop**, not a letterboxed window. The crop keeps the
middle 607px of 1920, so the watermark falls outside it entirely — removed by
framing, with no blur patch or logo cover. And because no brand purple ever
sits adjacent to footage purple, the colour difference never shows as a seam.

The cost is losing 68% of the width, which is spent deliberately:

- **Dishes clip**: the crop window pans slowly left-to-right across the three
  bowls, timed to the VO's own commas in "Turmeric, ginger, cinnamon." The
  narrow window becomes the reason the shot works rather than a compromise.
- **Spoon clip**: window sits slightly right of centre to hold both the bowl
  and the spoon. A hand appears at the top-right of the source; the crop
  removes most of it.

## Brand constraints

Colours, and nothing else enters frame:

    deep purple  #3A1F5C     royal purple #7A5CA8    pale lilac  #CBBFE0
    gold         #C2A053     light gold   #E0C88C    half white  #F4F1EC

Type: Fraunces (display), Karla (body), IBM Plex Mono (data/labels).

**Motion is constrained by the brand guide, not by taste.** "Never loops,
never pulses." Response motion is allowed; decorative motion is not. The
mark's one-shot 1.4s outward draw is the only non-response motion permitted,
and it happens once, at the start.

No swipe-up prompt, no arrow, no button on the end card. There is nothing to
tap yet.

## Captions

Deliberate break from the house one-word-centre style used on the other
channels: that is a retention device for fast formats and would read as
exactly the "nag" the brand guide names. Lower third, one full phrase at a
time, fade in and out, no per-word reveal. Present because most of Instagram
watches muted.

## Audio

VO is the spine. Music is a single sustained low drone, no percussion — a
beat implies a pace, and the script is about not hurrying. Duck ~12dB under
VO.
