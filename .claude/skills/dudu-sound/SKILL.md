---
name: dudu-sound
description: Used by Dudu (AI promo video director) after the picture cut. Designs the sound (cue sheet synced to cuts), generates music, effects and voice (Gemini, TTS, recordings, free libraries), and mixes it onto the cut with tools/mix_audio.py into a finished film.
---

# Dudu: sound design and mix

Claude cannot hear. Design from structure (cut times, beats, the reference analyses) and verify with measurements (`audio.json`, waveform, spectrogram from `tools/study_video.py` run on our own output) and, when needed, by asking Gemini to listen to an uploaded file.

## 1. Cue sheet (`project/sound-plan.md`)
One row per cue: time, cue (music / sfx / voice / silence), what it does dramatically, source, level.
Default arc for a problem-to-solution ad (from library/study/V5AFQaEbHQU and our own film):
| Beat | Sound |
|---|---|
| Hook | One short hit on the first frame, or a single real sound (a phone buzz) |
| Problem | Room tone plus a low drone that slowly rises; a heartbeat-like pulse or ticking clock |
| Agitate | The pulse speeds up; sounds sync to cuts and actions |
| Turn | A riser that **cuts dead** on the product's arrival |
| Solution | **One second of silence or "underwater" (low-pass) before the success moment**, then one clean success sound |
| Relief | A warm music bed, breathing room |
| CTA | The spoken closing line over a soft button; end on a final note, not a fade into nothing |
Voice: inner voices are dry and close (no room echo); the skeptic is calm and slow; the closing line confident.

## 2. Make the sounds
Ask the owner which sources are allowed (accounts, budget). Options:
- **Music:** Gemini music generation (in the subscription; drive it with `dudu-browser`); or a royalty-free library. Generate **two beds** (tension, warm), not one per clip.
- **SFX:** a free library with a clear license (credit when required), or a generator. Keep a `project/sound/LICENSES.md` with the source and license of every file.
- **Voice:** the owner's or a friend's recording (most authentic, free); or TTS (e.g. ElevenLabs, which supports Hebrew, English and many other languages; needs the owner's account). Never clone a real person's voice without their written consent.
- Do not use Kling's Native Audio for the film: separate per-clip audio does not join into one track and costs more.

## 3. Mix
Write `project/sound.json` and run `python tools/mix_audio.py project/sound.json`:
- Place cues on cut times from `project/cut.json` (sum the shot lengths).
- `until` = a hard stop (music cuts dead on the impact); mark music with `bed: true`; `duck: true` on voice lines dips every bed by 8 dB while the line plays.
- Output is loudness-normalized (-14 LUFS for web and social), AAC at 48 kHz.
Then run `python tools/study_video.py` on the output file path (or `contact_sheet.py` for picture) and check the loudness curve against the plan: quiet where it should be quiet, the silence before success really silent.
