# project/

Your film lives here. Everything in this folder stays on your machine and is ignored by Git, except the three example files.

| File / folder | What it holds | Who creates it |
|---|---|---|
| `product.md` | The facts about your product: what it does today, for whom, and which claims are allowed | You (copy `product.example.md`), or Dudu in a short interview |
| `brief.md`, `script.md` | The brief and the script | Dudu |
| `style-bible.md`, `shotlist.md`, `storyboard.json` | Look, characters, shot list and storyboard | Dudu |
| `frames/` | Character sheets, locations and the 12 keyframes | Gemini, driven through Playwright |
| `clips/` | The 12 animated clips | Kling, driven through Playwright |
| `cut.json` | The edit decision list | Dudu (format: `cut.example.json`) |
| `sound-plan.md`, `sound.json`, `sound/` | Cue sheet, mix settings and audio files | Dudu and you |
| `out/` | Rough cuts and the final film | `tools/build_cut.py`, `tools/mix_audio.py` |
| `qa-notes.md` | Every check and decision | Dudu |
