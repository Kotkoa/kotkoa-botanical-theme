# Bug: Hero (slideshow) text unreadable on mobile

## Symptom
On `shop.kotkoa.com` mobile viewport, the hero heading/subheading ("Botanical
beauty for everyday life") renders directly on top of the hero image, and
part of the text falls over a light/bright area of the photo, making it
illegible. On desktop the same slide is fine because the text box sits over
a shaded/darker part of the image.

## Root cause
`sections/slideshow.liquid` renders the hero via the shared Dawn `banner`
markup (`assets/section-image-banner.css`):

- The image is rendered with `object-fit: cover` (`assets/base.css:1174-1175`)
  and no explicit `object-position`, so the visible crop differs between the
  desktop and mobile aspect ratios ([slideshow.liquid](sections/slideshow.liquid#L140-L151)).
- Text box position comes from `block.settings.box_align`
  (`banner__content--middle-center` etc.), which is a fixed flex
  alignment — it has no awareness of where the image is actually dark
  vs. light at the current viewport ([slideshow.liquid](sections/slideshow.liquid#L161-L162)).
- When `show_text_below` (`banner--mobile-bottom`) is off, mobile stacks the
  text **over** the image instead of below it, and the per-slide
  `image_overlay_opacity` (`block.settings.image_overlay_opacity`, default
  `0`) is the only thing that could darken the whole image uniformly — it's
  disabled here, so nothing compensates for the shifted crop.

Net effect: contrast that works for the desktop crop breaks on the mobile
crop because nothing ties text placement/legibility to the actual image
content at that breakpoint.

## Fix options (pick one, or combine)
1. **Content fix (fastest, no code change):** in the theme editor, for this
   slide set `show_text_below` = on (`banner--mobile-bottom`) so mobile text
   stacks below the image instead of over it. Zero risk, but changes visual
   layout intent.
2. **Content fix:** raise `image_overlay_opacity` for the slide (e.g. 20-30%)
   so the whole image darkens uniformly, guaranteeing contrast against light
   text regardless of crop. Also zero code risk.
3. **Code fix:** add a mobile-specific text-shadow / scrim behind
   `.banner__box` text (independent of `image_overlay_opacity`) so heading
   legibility doesn't depend on the underlying photo at all. Small, scoped
   CSS change.
4. **Code fix:** set an explicit `object-position` per slide (new schema
   setting) so merchants can pin the crop's focal point and keep desktop's
   dark area visible on mobile too. Larger change (schema + settings UI).

Recommended: **Option 3** (scrim/text-shadow) as the durable code fix, since
it fixes the class of bug for all future images/slides without relying on
merchants remembering to set overlay opacity per slide. Optionally pair with
Option 1/2 as an immediate content-only patch on the live slide while the
code fix ships.

## Plan (discrete, independently verifiable steps)

1. **Reproduce & confirm root cause** — capture a mobile-viewport screenshot
   locally (theme dev server + browser devtools mobile emulation) of the
   current hero, confirm heading text overlaps the light area of the image.
   *(judgment step — do myself, not delegated)*

2. **Implement CSS scrim fix** — in `assets/section-image-banner.css`, add a
   mobile-only rule that gives `.banner__box` (or heading/subtext) a
   subtle text-shadow / semi-transparent backdrop when
   `.banner:not(.banner--mobile-bottom)` on mobile, so text stays legible
   regardless of image brightness underneath. Scoped, additive CSS only —
   no markup/schema changes. *(mechanical, delegable)*

3. **Theme-check / lint pass** — run the project's Liquid/theme checks to
   confirm no syntax errors introduced. *(mechanical, delegable)*

4. **Local visual verification** — run theme dev server, view hero at mobile
   width (375px/390px), confirm text is legible against the actual product
   image. *(judgment step — do myself, not delegated, per user's
   instruction to test locally in-browser before pushing)*

5. **Optional content-only mitigation on live slide** — bump this slide's
   `image_overlay_opacity` slightly via theme editor while code fix is
   reviewed. *(user/editor action, not code)*

6. **Commit** — only after step 4 passes visually. No push without explicit
   go-ahead.

## Delegation notes
Only step 2 (mechanical CSS edit) and step 3 (lint/theme-check run) are
candidates for a Haiku subagent — they're bounded, low-judgment, and
verifiable by output (diff + lint exit code). Steps 1 and 4 require visually
judging contrast against the real image and must be done directly (with
`shopify theme dev` + browser), not delegated blind. Step 5 is a merchant
action outside code.
