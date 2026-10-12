---
name: dudu-visuals
description: Used by Dudu (AI promo video director) for stages 3-5. Builds the style and character bible, the 12-shot list, reference sheets, location frames and the 12 keyframe prompts for Gemini / Nano Banana, and reviews every generated image.
---

# Dudu: style bible, references and keyframes

## Stage 3a: style bible (`project/style-bible.md`)
- **STYLE block** (pasted into every prompt): `Photoreal, looks like a real candid photo, natural light, 35mm lens, shallow depth of field, subtle film grain, unretouched.` plus the brand palette in hex.
- **Character descriptors**, one fixed English sentence per recurring character and for the product, pasted word for word. Give each character one distinctive detail (a nose ring, a lanyard, a watch).
- **NEGATIVE block:** `text, letters, words, logos, watermark, UI, readable screen content, numbers, extra fingers, deformed hands, distorted face, cartoon, 3D render`.
- **Light:** keep generation light natural and consistent; do the cold/warm mood shift in the edit (color grade). Baked-in moods made locations look fake and inconsistent.

## Stage 3b: shot list (`project/shotlist.md`)
Per shot: beat, framing, ONE camera move with speed, start pose -> end pose, refs to attach, what goes in the edit, risk. No two identical framings in a row. Hands and product close-ups are the risky shots: plan extra takes.

## Stage 3c: storyboard (`project/storyboard.json`)
Same schema as the studied references (`tools/storyboard.py`), one entry per shot:
- `size, angle, lens, light, move`: the **camera direction**. Vary the size and angle between neighbouring shots; give each sequence its own light; face shots tele and static, event shots wide.
- `action`: what happens, start pose → end pose.
- `acting`: a direction for the performance in one line: the emotion, the eyes, the body. Plan **one visible micro-expression pivot** per hero (e.g. fear → relief).
- `sound`: what is heard in this shot (feeds `dudu-sound`).
- `why`: the technique and, if borrowed, the reference (`library/study/<id>`).
Before the keyframes exist, panels show "no frame yet". After stage 5, set `frame` to the keyframe file and re-render: `python tools/storyboard.py project/storyboard.json`. Show the owner a screenshot of the board at the gate.

## Stage 4: references first (they decide everything)
1. **Character sheets:** 4 panels on grey (front, 3/4, profile, face close-up), one per character.
2. **Product sheet:** 4 angles of the product, then targeted edits for each state (e.g. a status light off / on, a box closed / open) on the same image.
3. **Locations:** if the owner has a real photo of the kind of place they want, use it as the reference ("generate a new image of a very similar place, change the angle"). That beat every invented location. Generate the other locations with the first location attached so they look like one building.
4. Lock one version of each before any keyframe. Fix small issues with targeted edits ("Edit only ...: ... Change nothing else.").

Lessons:
- Nationality words ("Israeli", "European", "Scandinavian") do little. Describe faces, skin, hair, build and clothes.
- When an attached reference makes the model return the same picture, either start a new chat or invert the job: give the model the image whose *character* is right and ask it to "recreate this exact sheet as a high-resolution photoreal photograph".
- Real brands sneak in (laptop logos, bottle labels, tower signs). Remove them with an edit.

## Stage 5: keyframes
Prompt = `Use image 1 (...), image 2 (...).` + one shot line (framing, who, the moment the motion **starts**, where) + STYLE + `No text, no logos, no readable screens.`
Attach only the refs that shot needs (2-4). Check every result yourself:
- faces and distinctive details match the sheets
- no doppelgangers (an extra who looks like a main character)
- physical truth the audience knows (e.g. a plug matches its socket, a phone has the right number of cameras, a keyboard is the right way round)
- the product is visible where the story needs it
Fix with an edit in the same chat, or accept and solve it in the edit.
