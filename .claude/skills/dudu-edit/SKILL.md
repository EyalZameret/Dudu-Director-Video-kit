---
name: dudu-edit
description: Used by Dudu (AI promo video director) for stage 7. Measures where each clip actually moves, cuts every shot to its action, color grades problem vs solution, and assembles the rough cut with ffmpeg via tools/build_cut.py.
---

# Dudu: the rough cut

Generators return fixed 5 s clips. Played in full they feel slow: in our first cut a reviewer said "the cuts are very slow", and measuring showed only ~30 of 52 seconds had real action.

## 1. Measure
`python tools/motion_report.py project/clips/*.mp4` prints the movement per half second:
- 0.1-0.5: frozen; 1-3: slow camera move; 3+: action.
For moments that the numbers can't see (a small light changing color), crop and tile that area:
`ffmpeg -i shot10.mp4 -vf "fps=2,crop=360:200:X:Y,tile=5x2" -frames:v 1 detail.png` (the ffmpeg that `imageio-ffmpeg` installed: `python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`)..

## 2. Decide the cut
- Check `library/INDEX.md` for a reference with the pace the owner wants, and match its numbers (cuts per 10 s, median shot).
- **Pace is a curve, not a constant** (see library/study/V5AFQaEbHQU): a calm opening can hold, the problem compresses, the climax fragments to under 1 s, the turn and the CTA breathe.
- Keep only the seconds with action. Most shots end up 1.5-4 s. The opening and the CTA may stay longer (logo and spoken line need time).
- Faster cuts in the problem part build tension; let the turn breathe.
- Cut before any failure (face change, morph). Replace a failed shot with its keyframe still plus a slow zoom.
- Dialogue may run over the next shot (J/L cuts), so a long line does not force a long shot.

## 3. Build
Write `project/cut.json` (see `project/cut.example.json`) and run `python tools/build_cut.py project/cut.json`.
- Grade in the edit: `cold` for the problem shots, `warm` from the turn on. Keep grades gentle; do not push blue into the shadows.
- Output: H.264 High@4.1, yuv420p, bt709, 1080p30. If someone sees blue blotches in an old Windows Media Player, it is the player's decoder; check by extracting a frame with ffmpeg and boosting saturation (`eq=saturation=4`). If the frame is clean, the file is fine.
- Review the result with `python tools/contact_sheet.py project/out/roughcut-vN.mp4 --every 2.5 --cols 6`.

## 4. Next: sound
Lock the picture first, then load `dudu-sound` (stage 8): one continuous music track, effects and voices, mixed with `tools/mix_audio.py`. Per-clip generated audio does not join into one track.
