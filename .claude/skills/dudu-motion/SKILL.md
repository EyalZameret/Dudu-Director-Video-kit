---
name: dudu-motion
description: Used by Dudu (AI promo video director) for stage 6. Picks the animation model with a one-shot A/B test, writes image-to-video motion prompts for Kling (and Veo / Seedance), and reviews every clip with contact sheets and a motion report.
---

# Dudu: animation

## Step 1: A/B test one hard shot before spending credits
Pick the hardest shot (two characters, an action). Generate it in each candidate model with the same keyframe and prompt, then compare contact sheets (`tools/contact_sheet.py`).
Our test (2026-10): **Kling 3.0** kept faces and the room identical at 1080p; **Veo 3.1** (Gemini / Google Vids) acted out the scene nicely but re-framed the room and drifted the main character's face, at 720p. Kling won. Re-test when models change.

## Step 2: prompts
- The image sets the look; the prompt describes only what moves.
- One camera move with a speed ("slow push-in, very slow"; "static locked-off shot").
- One or two small actions per 5 s clip. Kling squeezes three actions into 5 s and it looks rushed.
- Stability lines at the end: `Stable face, natural hands, no camera shake. No text.`
- Product shots: `The product keeps exactly the same shape, size and color from start to end.`

## Step 3: settings and cost (Kling, 2026-10)
1080p, 5 s, 16:9, **Native Audio off** (dialogue/music are added in the edit; audio raised the cost from 40 to 60 credits per clip). Check the credit price on the Generate button before every click.

## Step 4: review every clip
- `python tools/contact_sheet.py clip.mp4` and Read the PNG.
- Known failures: jumpy camera in corridors, a product that morphs (turned silver), a face that changes in the last second.
- Retake at most once with a stricter prompt. If it still fails: keep the good seconds, or replace the shot with the keyframe still and a slow zoom in the edit (that saved our product close-up).
