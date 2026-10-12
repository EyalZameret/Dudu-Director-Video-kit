---
name: dudu-script
description: Used by Dudu (AI promo video director) for stages 1-2. Interviews the owner for the brief and writes a 12-shot promo script (problem-agitate-solve, about 70/30 problem/solution, minimal dialogue, one CTA) into project/brief.md and project/script.md.
---

# Dudu: brief and script

## Stage 0: product facts (`project/product.md`)
If the file is missing, ask in one round and write it:
1. What the product is, in one sentence. Who buys it, who uses it.
2. The 3-5 most painful situations it solves (real scenarios, not features).
3. What it does **today** versus what is planned.
4. The claims you may make, each with its source (pilot data, docs). Anything without a source is not a claim.
5. Brand: name, colors (hex), tone, things never to say.

## Stage 1: brief (`project/brief.md`)
At most 6 short questions, each with a recommended default:
1. **The one pain** the video is about. Suggest 3-4 scenarios from `product.md`; the most visual one wins.
2. **Hero:** a relatable underdog (for B2B: the junior employee who must fix it) and an antagonist or skeptic (the boss, the client).
3. **Proof moment:** what the viewer sees that makes it believable.
4. **CTA:** one only.
5. **Specs:** length, aspect ratio, language, dialogue amount. Default: 12 shots, 16:9, minimal dialogue, one spoken closing line.
6. **Tone.** Default: tension and dry humor in the problem, calm relief in the solution.

Sections: Goal, Audience, The one pain, Characters, Key message (one sentence), Proof, CTA, Specs, Tone, Owner decisions, Must avoid, Open questions.

## Stage 2: script (`project/script.md`)
### Structure (12 shots)
| Shots | Beat | Job |
|---|---|---|
| 1 | Hook | Concrete pain in the first 3 seconds. No logo, no product. |
| 2-4 | Problem | The trouble lands on the hero. |
| 5-7 | Agitate | The cost rises: time, boss, people waiting. |
| 8 | Turn | Lowest point, then the product appears. |
| 9-11 | Solution | Product in action, then a result the viewer can **see** (a light, a reaction), not a feature list. |
| 12 | CTA | Name, one-line promise, one CTA. |

Write 3-5 hooks first and let the owner choose. Then the full table:

| # | Time | Beat | Dialogue / inner voice | What we see | Added in edit (text, UI, logo) | Words |

### Writing rules
- **Inner voices beat dialogue:** characters *thinking* ("I hope this works...") need no lip sync and work in any language. Keep spoken lines to 12 words or fewer per shot.
- Plan pacing for the edit: shots will be cut to the action (1.5-4 s each), so a ~60 s script usually becomes a ~30 s film. That is good; tell the owner early.
- Leave at least 2 shots silent; one full second of silence before the success moment.
- Under the table: the key message, the CTA, and a **Claims used** table (claim, source, today or vision).
