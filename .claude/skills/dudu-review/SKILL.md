---
name: dudu-review
description: Used by Dudu (AI promo video director) at every gate. Checks script claims against project/product.md, structure and pacing, and reviews images and clips with keep/fix/regenerate decisions into project/qa-notes.md.
---

# Dudu: review

Append to `project/qa-notes.md`. Every item is PASS, FIX or KEEP/REGENERATE, with the exact shot and the concrete fix.

## A. Claims (script and on-screen text)
- No number (time, %, price, count) without a source in `product.md`. Show time with a clock in the scene instead.
- No "fixes everything". No capability shown as working that `product.md` lists as planned, unless the owner decided otherwise; record that decision.
- No competitor or real-brand names.

## B. Structure
- Hook in the first 3 s, problem/solution split as in the brief, one CTA, at least 2 silent shots.
- Every shot has one camera move. No text, UI or logo in any prompt.

## C. Images
Face and distinctive details match the sheets; no doppelgangers; hands; physical truth (ports, cables, devices); no logos or readable text; the product looks identical across shots.

## D. Clips
Identity holds to the last frame; no morphing product; no jumpy camera; action fits the duration; dead time measured with `tools/motion_report.py`.

Fix notes name a concrete change ("cut at 3.5 s", "add: keeps exactly the same shape", "replace with still + zoom"), never "make it better".
