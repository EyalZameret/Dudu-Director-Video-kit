# Kling prompting notes

Checked 2026-10 against vendor guides and our own runs. When the app behaves differently, trust the app and update this file.

- Structure: subject action (beginning -> middle -> end) -> camera -> style/stability.
- Image-to-video: do not re-describe the image. Describe the change.
- Clip length 5 s or 10 s (3.0 allows longer and multi-shot). Start/end frames are supported.
- One camera move per clip: `static locked-off shot`, `slow push-in`, `slow pull-out`, `slow pan`, `slow orbit, a few degrees`, `handheld follow, subtle`, `rack focus from X to Y`.
- Negatives that help: `morphing, distorted face, extra fingers, warped lines, text, logo, camera shake, sudden cuts`.

| Failure | Fix |
|---|---|
| Text or logos appear | Never generate them; add in the edit |
| Product changes shape or color | Add an explicit "keeps exactly the same shape and color" line; else use the still + zoom |
| Corridor or walk shots jump between distances | `static locked-off shot, no cuts`; else keep only the first 1.5-2 s |
| Face changes near the end | Cut before it |
| Action feels rushed | One action per 5 s, or use 10 s |

Sources: atlabs.ai Kling 3.0 guide, fal.ai Kling 3.0 Pro guide, oakgen.ai, videoai.me troubleshooting, magichour.ai reference guide.
