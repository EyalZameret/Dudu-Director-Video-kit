# Apex (The Dor Brothers, 2026), study notes

- **Source:** https://www.youtube.com/watch?v=V5AFQaEbHQU · 3:15 · fully AI-generated ("Yes, this is 100% AI").
- **Type:** cinematic action short and trailer, not a product ad. Studied for pacing, AI shot craft and continuity.
- **Measured** (tools/study_video.py, scene threshold 0.3): 73 shots, **3.7 cuts per 10 s**, median shot **1.6 s**, shortest 0.4 s, longest 15.9 s. Integrated loudness -15.3 LUFS. No captions; only a few spoken lines, so the story is told in pictures and sound.
- **Storyboard:** `storyboard.json` (all 73 shots: size, angle, lens, light, move, action, acting, sound). Render it locally with `python tools/storyboard.py library/study/V5AFQaEbHQU/storyboard.json`.

## Structure
| Time | Beat | What happens | Shot lengths |
|---|---|---|---|
| 0:00-0:31 | Setup (calm) | Fast fly-through of Manhattan (0.8 s), then a **14.6 s** office shot: the heroine on the phone. A TV shows "Breaking News". She looks out at a smoking skyline (14 s). | Very long |
| 0:31-0:57 | Inciting incident | The window explodes; she runs: corridor, elevator, stairs, street exit. | 0.5-3.6 s |
| 0:57-1:40 | Chaos (escalation) | Street on fire, plane crash, the hero vehicle appears, an explosion swallows everything (5.3 s) | 0.7-4.5 s, with one 15.9 s tracking run |
| 1:41-1:53 | Emotional beat | She finds a child in the fire and hugs her | 0.8-4.8 s |
| 1:53-2:37 | Escape (rhythm) | Driving: face, car, chaos, bridge, country road, UFO. A strict alternation of face close-up and wide shot. | 0.6-2.9 s |
| 2:34-2:43 | Climax | Truck crash in fast fragments: 0.4, 0.5, 2.0, 0.6 s | Ultra short |
| 2:43-3:07 | Twist | She sits in an interrogation room (7.9 s), suits, a phone call | 1.5-7.9 s |
| 3:07-3:15 | End card | "To Be Continued" on black (7.8 s) | Long |

## What to steal (and how it maps to our 12-shot ads)
1. **Pace is a curve, not a constant.** It opens with *long* shots (14-15 s) to build calm, goes to 1-2 s cuts in the chaos, and down to 0.4-0.6 s at the climax, then back to long shots for the twist. Our rough cut had every shot the same length; give the hook and the turn room, and compress the problem.
2. **Hard alternation in action scenes:** face close-up, then wide shot of the event, then face again. The face reaction sells each event and hides AI weaknesses in the wide shots. Use it in "agitate" beats (hero face, then the people waiting, then the boss's face).
3. **One hero, one costume, one prop.** The red leather coat and blonde hair make the heroine instantly readable in every shot, even when the face drifts slightly between generations. A colored lanyard or a nose ring can do the same job; keep one strong color signature per character.
4. **Explain the world through a screen inside the scene** (TV with "Breaking News"). In-scene text works when it is composited in the edit, not generated.
5. **Fragment the impossible moments.** The crash is 4 shots under 1 s each, so no single AI clip has to hold up for long. For risky actions (hands, product insert), cut the action into 2-3 short shots instead of one 5 s clip.
6. **Insert shots buy rhythm:** fly-throughs, a UFO, debris. Short cutaways (0.5-1.5 s) between story shots keep energy without new acting.
7. **End on a card plus a hook to the next thing.** For an ad: logo + CTA card held 3-4 s.

## Camera direction (cinematography)
- **Shot-size grammar:** EWS spectacle (event) → MCU/ECU face (reaction) → insert (detail: boots, wheel), repeated. The faces are always tele lens and shallow focus, the events wide lens, low angles.
- **Angles reset the eye** at every new space: top-down at the exit (16), high in the stairwell (15), low at explosions (7, 19, 31), aerial for scale (1, 59).
- **Movement:** long holds are near-static or slow push-ins (2, 4); the chaos is handheld and tracking; the climax uses whips and jolts, then **slow motion** right after the rapid fragments (66) so the impact lands.
- **Light as chapter markers:** soft day office → cold fluorescent stairwell → orange fire → a single spotlight for the child (35) → cold concrete in the interrogation. Every sequence has its own light.
- **Hide AI weaknesses with the lens:** soft foregrounds (14), backs of heads (4, 9), fast inserts; faces get the clean, static tele shots.

## Acting
- **Arc without words:** busy and dismissive (2) → frozen dread from behind (4) → raw panic, a flailing run (5, 9) → breaking voice on the phone (20) → anguish (34) → tenderness (37) → **resolve** (38, 42, 44) → defiance in stillness (67).
- **The micro-expression pivot** (38): fear turns into resolve within one short close-up; furrowed brow, narrowed eyes, clenched jaw. This is the character's turn, done in 0.7 s.
- **Stillness as power** (68, 71): the antagonists move slower than everyone else, relaxed shoulders, an unhurried delivery.
- **Reaction sells the event:** almost every spectacle shot is followed by her face (22→23, 30→29, 56→57).

## Sound design
Measured with `audio.json`, `waveform.png` and `spectrogram.png`, cross-checked with Gemini listening to the video (dialogue lines are Gemini-only and unverified):
| Time | Sound | Technique |
|---|---|---|
| 0:00 | Short loud hit (-11 LUFS) | Energy spike on the first frame |
| 0:01-0:30 | Quiet: room tone, phone voice, news; a sub-bass drone creeps in at the TV; **-30 to -41 LUFS** | Quiet setup = room for contrast. Drone = dread before any event |
| 0:29-0:31 | A rising whoosh that **cuts dead** into the impact | Riser, then hit on the cut |
| 0:31-1:41 | A dense wall: driving percussion and brass stabs, explosions, crowd; **-10 to -16 LUFS**; hits synced to her actions | Rhythmic sync of hits to cuts and moves |
| 1:16 | Music ducks; exterior muffled inside the car; breathless phone line | Interior/exterior contrast so a line can be heard |
| 1:41-1:55 | Percussion stops; ethereal pad; the fire becomes **muffled, highs filtered** (visible as a dark top band in the spectrogram) | The "underwater" drop-out for the emotional beat |
| 1:55 | Hard cut back to full chaos | Snap back |
| 2:36 | **Music hard-stops on the crash**; glass rings out alone; a thud, then silence | Hard stop on impact |
| 2:44-3:06 | Silence, echoey room tone, footsteps, two calm lines | Total contrast; quiet voices dominate |
| 3:12-3:15 | Final hit, then silence (192.6-194.7 s) | Button on the end card |

## What not to copy
- Real people's likenesses (the twist uses recognizable public figures) and a real brand's car as the hero vehicle. Our rules forbid both: no real people, no third-party brands.
- 3+ minutes. A promo ad is 15-60 s; borrow the *pace curve*, not the length.

## For our 30-60 s ads (most reusable)
1. **Sound:** a quiet, tense setup with a low drone → a riser that cuts dead into the turn → **one second of underwater/silence** before the success moment → a hard stop or a single clean hit on the success moment → a warm button on the CTA card.
2. **Camera:** alternate the face (tele, static) with the event (wide, low); give each sequence its own light; slow motion right after the fastest cuts.
3. **Acting:** direct one visible micro-expression pivot per hero (fear → relief), and make the skeptic move slower than everyone else.

## Numbers to reuse
- Action promo pace: about 3-4 cuts per 10 s (median 1.5-2 s), with a long breath at the start and before the CTA.
- Climax fragments: 0.4-0.8 s.
- Emotional or "hold" shots: 4-8 s, at most 1-2 per film.
