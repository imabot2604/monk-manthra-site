# monk manthra — introduction carousel

Post this one first, before any ingredient carousel. It introduces the
brand; the ingredient carousels only make sense once someone knows what
monk manthra is and why the panel matters.

6 slides in `png/`, in order:
1. Cover — mark + wordmark + the bio line
2. The category's noise vs. the actual position
3. Who it's for
4. How it's dosed (brand-wide philosophy, not a Golden Milk claim)
5. The range, honestly — Golden Milk live, the rest coming
6. CTA — start with Golden Milk

All copy is pulled from what's already live on the site (story.html's
Who/How sections, the footer/bio line, the Shopify homepage subheading)
rather than invented — this carousel's job is tone and positioning, so it
leans on lines that were already signed off rather than new claims.

## Caption

Every bottle in this category promises everything, all at once, forever.
We make one thing at a time, and we say what's actually in it.

monk manthra — daily supplements for people who want to feel steady, not
supercharged. Golden Milk is live now. The rest of the range follows, one
formula at a time, as each one is ready.

## Notes

- Slide 4's "the dose stays visible, never hidden" is a brand-wide
  principle from story.html, not a claim about Golden Milk specifically
  — Golden Milk's own dose is still TBC (see
  [products/golden-milk.html](../../products/golden-milk.html) and the
  ingredient carousels' captions). Don't quote slide 4 in a way that
  implies Golden Milk's panel already has numbers.
- Rebuild with `python3 build_intro.py` if the range list changes (a
  product ships, a name changes, etc.) — edit the `RANGE` list at the top
  of the script.
