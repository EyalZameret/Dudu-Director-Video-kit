"""Render a storyboard board (HTML) from storyboard.json: one panel per shot with its frame,
camera direction, action and acting, and sound. Works for a studied reference and for your own project.

Usage:
    python tools/storyboard.py library/study/<id>/storyboard.json
    python tools/storyboard.py project/storyboard.json

storyboard.json:
{
  "title": "...", "frames_dir": "frames",            # relative to the json file
  "sequences": [{"name": "Setup", "from": 1, "to": 4}],   # optional
  "shots": [
    {"n": 1, "time": "0:00", "length": 0.8, "frame": "001.jpg",
     "size": "EWS", "angle": "aerial", "lens": "wide", "move": "fast push through street canyon",
     "light": "daylight", "action": "...", "acting": "...", "sound": "...", "why": "..."}
  ]
}
Writes storyboard.html next to the json. Open it in a browser or Read a screenshot of it.
"""
import html
import json
import os
import sys

CSS = """
:root{--bg:#f6f5f2;--card:#fff;--ink:#1d1d1f;--mute:#6b6b70;--line:#e3e1dc;--acc:#b8935a}
@media (prefers-color-scheme:dark){:root{--bg:#121314;--card:#1a1b1d;--ink:#ecebe6;--mute:#9a9a9f;--line:#2a2b2e;--acc:#c9b48a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif;padding:24px}
h1{margin:0 0 4px;font-size:22px}.sub{color:var(--mute);margin-bottom:20px}
h2{font-size:15px;margin:28px 0 10px;color:var(--acc);text-transform:uppercase;letter-spacing:.06em}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.card img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:#000}
.ph{aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;color:var(--mute);background:var(--line)}
.b{padding:10px 12px}.top{display:flex;justify-content:space-between;font-weight:600;margin-bottom:6px}
.t{color:var(--mute);font-weight:400}.tags{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px}
.tag{font-size:11px;border:1px solid var(--line);border-radius:99px;padding:1px 8px;color:var(--mute)}
.row{margin:3px 0}.k{color:var(--acc);font-size:11px;text-transform:uppercase;letter-spacing:.05em;margin-right:4px}
.why{margin-top:6px;color:var(--mute);font-style:italic}
"""


def panel(s, frames_dir):
    img = s.get("frame")
    src = os.path.join(frames_dir, img).replace("\\", "/") if img else ""
    pic = f'<img src="{html.escape(src)}" loading="lazy">' if img else '<div class="ph">no frame yet</div>'
    tags = "".join(f'<span class="tag">{html.escape(str(s[k]))}</span>'
                   for k in ("size", "angle", "lens", "light") if s.get(k))
    rows = "".join(f'<div class="row"><span class="k">{k}</span>{html.escape(str(s[k]))}</div>'
                   for k in ("move", "action", "acting", "sound", "vo") if s.get(k))
    why = f'<div class="why">{html.escape(s["why"])}</div>' if s.get("why") else ""
    length = f'{s["length"]}s' if s.get("length") is not None else ""
    return (f'<div class="card">{pic}<div class="b"><div class="top"><span>#{s["n"]}</span>'
            f'<span class="t">{html.escape(str(s.get("time", "")))} · {length}</span></div>'
            f'<div class="tags">{tags}</div>{rows}{why}</div></div>')


def main(path):
    sb = json.load(open(path, encoding="utf-8"))
    frames_dir = sb.get("frames_dir", "frames")
    shots = {s["n"]: s for s in sb["shots"]}
    seqs = sb.get("sequences") or [{"name": "", "from": min(shots), "to": max(shots)}]
    body = []
    for q in seqs:
        cards = [panel(shots[n], frames_dir) for n in range(q["from"], q["to"] + 1) if n in shots]
        if cards:
            body.append((f'<h2>{html.escape(q["name"])}</h2>' if q["name"] else "") +
                        f'<div class="grid">{"".join(cards)}</div>')
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{html.escape(sb.get("title", "Storyboard"))}</title><style>{CSS}</style></head><body>'
           f'<h1>{html.escape(sb.get("title", "Storyboard"))}</h1>'
           f'<div class="sub">{html.escape(sb.get("subtitle", ""))}</div>{"".join(body)}</body></html>')
    out = os.path.join(os.path.dirname(path), "storyboard.html")
    open(out, "w", encoding="utf-8").write(doc)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
