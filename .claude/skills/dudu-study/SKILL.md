---
name: dudu-study
description: Used by Dudu (AI promo video director) to learn from a reference video link (YouTube and most video sites). Downloads it for private analysis, detects every cut, reviews one frame per shot, writes a structured analysis into library/study/<id>/analysis.md and updates library/INDEX.md, then deletes the video. Use when the owner shares a link and says "learn from this", "study this", "do it like this", or asks for a style taken from an ad.
---

# Dudu: learning from reference videos

Claude cannot watch a link directly: opening a YouTube URL only shows the title and description. This skill gives Dudu "eyes" with yt-dlp and ffmpeg.

## 1. Extract
```bash
python tools/study_video.py "<url>"            # --threshold 0.2 for soft cuts, 0.4 for busy action
```
It writes to `library/study/<video-id>/`:
- `meta.json`: title, channel, duration
- `shots.json`: every shot's start, end, length, plus statistics (cuts per 10 s, median shot)
- `shots-N.png`: one labeled frame per shot, 12 per sheet
- `transcript.txt`: captions, if any
The downloaded video is deleted at the end.

If the download fails with **HTTP 403** or "page needs to be reloaded", update yt-dlp (`pip install --user -U yt-dlp`) and make sure Node is on PATH: the tool passes `--js-runtimes node --remote-components ejs:github` to solve YouTube's JS challenge.

## 2. Look (picture)
Read **every** `shots-N.png` and `shots.json`. Study five crafts:
- **Directing:** beats, where the story slows down and speeds up, what each sequence is for.
- **Camera:** per shot, size (EWS/WS/MS/MCU/CU/ECU/insert/POV), angle, lens feel (wide/normal/tele), light, movement.
- **Acting:** expressions, eyes, body, the emotional arc, the moments that sell the story.
- **Storyboard:** the shot-by-shot grammar (event → reaction → detail).
- **Sound:** see step 3.

## 3. Listen (sound)
Claude cannot hear, so use two sources and cross-check them:
1. **Measurements:** Read `audio.json` (loudness per 0.5 s and per shot, silences), `waveform.png` and `spectrogram.png` (red lines = cuts, white ticks = 10 s). Loud dense bands = action music or effects; a dark top band = highs filtered ("underwater"); clear horizontal lines = tones or voice; gaps = silence.
2. **Gemini's ears** (optional, ask the owner): Gemini can watch a YouTube link with audio. With `dudu-browser`, open a new Gemini chat (plain chat, no tool) and ask, in English, for a section-by-section sound breakdown with timestamps (music, sfx, silence, dialogue, hits on cuts) and an acting breakdown, telling it to say "not sure" when unsure.
If the owner has no Gemini, rely on the measurements alone and say so in `analysis.md`. Keep what both sources agree on. Mark anything only Gemini reported (exact dialogue lines especially) as "per Gemini, unverified".

## 4. Write `storyboard.json` and `analysis.md` (same folder)
- `storyboard.json`: every shot with `size, angle, lens, light, move, action, acting, sound, why`, grouped into `sequences`. Schema in `tools/storyboard.py`. Render with `python tools/storyboard.py library/study/<id>/storyboard.json`, and screenshot it to check.
- `analysis.md`: header (source, length, type, the measured numbers) → **Structure** → **What to steal** → **Camera direction** → **Acting** → **Sound design** (a time / sound / technique table) → **For our 30-60 s ads** (the 3 most reusable moves) → **What not to copy** (real people, brands, length) → **Numbers to reuse**.
Write techniques, not descriptions: "alternate face close-up and wide event shot in action beats", not "she drives a car".

## 5. Update the library index
Add one row to `library/INDEX.md`: id, title, type, pace (cuts per 10 s, median), and the 1-2 techniques that make this reference worth reusing.

## 6. Use it
When writing a brief, script, shot list or cut, check `library/INDEX.md` for matching references and say which technique you are borrowing and from where. When the owner says "like that ad", open its `analysis.md` first.

## Rules
- Study only, never reuse footage, frames, music or likenesses. The download is for private analysis and is deleted; tell the owner once that downloading may conflict with the site's terms.
- Frame sheets stay local (git-ignored). `analysis.md`, `shots.json` and `meta.json` may be committed.
- Report back to the owner in their language: the 3-5 most useful techniques, with shot numbers as evidence.
