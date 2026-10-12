"""Let Dudu "watch" a reference video: download it, detect every cut, sheet one frame per shot,
pull captions, save the facts, then delete the video.

Usage:
    python tools/study_video.py "https://www.youtube.com/watch?v=..." [--threshold 0.3] [--keep-video]

Output (library/study/<video-id>/):
    meta.json        title, channel, duration, url
    shots.json       every shot: start, end, length; plus cut statistics
    audio.json       loudness (LUFS) per 0.5 s and per shot, silences
    shots-N.png      one frame per shot, numbered, with its time         (local, git-ignored)
    frames/NNN.jpg   one frame per shot, for the storyboard              (local, git-ignored)
    waveform.png     loudness shape, red lines = cuts, white ticks = 10 s (local, git-ignored)
    spectrogram.png  frequency content (music, hits, voice), same marks  (local, git-ignored)
    transcript.txt   captions as plain text, if the video has them
Dudu then reads these files and writes analysis.md and storyboard.json (see the dudu-study skill).

For private analysis only: the downloaded video is deleted unless --keep-video.
Requires: pip install --user yt-dlp imageio-ffmpeg
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ytdlp(*args):
    # YouTube now requires solving a JS challenge; yt-dlp does it with Node (already needed for Playwright MCP).
    js = ["--js-runtimes", "node", "--remote-components", "ejs:github"] if shutil.which("node") else []
    return subprocess.run([sys.executable, "-m", "yt_dlp", "--no-warnings", "--ffmpeg-location", FF, *js, *args],
                          capture_output=True, text=True)


def vtt_to_text(path):
    lines, last = [], None
    for raw in open(path, encoding="utf-8", errors="ignore"):
        s = raw.strip()
        if not s or "-->" in s or s.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or s.isdigit():
            continue
        s = re.sub(r"<[^>]+>", "", s)
        if s != last:
            lines.append(s)
            last = s
    return "\n".join(lines)


def analyse_audio(video, dur, shots):
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", video, "-vn", "-af",
                        "ebur128=metadata=1,ametadata=print:key=lavfi.r128.M,silencedetect=n=-40dB:d=0.4",
                        "-f", "null", "-"], capture_output=True, text=True)
    pts = [(float(t), float(m)) for t, m in
           re.findall(r"pts_time:([\d.]+)\s*\n.*?lavfi\.r128\.M=(-?[\d.]+)", r.stderr)
           if float(m) > -70]
    if not pts:
        return None
    bins = []
    for b in range(int(dur * 2) + 1):
        seg = [m for t, m in pts if b / 2 <= t < (b + 1) / 2]
        bins.append(round(sum(seg) / len(seg), 1) if seg else None)
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    silences = [{"start": round(max(s, 0), 2), "end": round(e, 2)} for s, e in zip(starts, ends)]
    per_shot = []
    for x in shots:
        seg = [m for t, m in pts if x["start"] <= t < x["end"]]
        per_shot.append({"n": x["n"], "lufs_mean": round(sum(seg) / len(seg), 1) if seg else None,
                         "lufs_peak": round(max(seg), 1) if seg else None})
    integrated = re.findall(r"I:\s*(-?[\d.]+) LUFS", r.stderr)
    return {"integrated_lufs": float(integrated[-1]) if integrated else None,
            "momentary_lufs_per_0_5s": bins, "silences": silences, "per_shot": per_shot}


def audio_images(video, dur, cuts, out):
    marks = ",".join(f"drawbox=x={int(c / dur * 1920)}:y=0:w=2:h=ih:color=red@0.7:t=fill" for c in cuts) or "null"
    secs = ",".join(f"drawbox=x={int(t / dur * 1920)}:y=0:w=1:h=12:color=white:t=fill" for t in range(0, int(dur), 10))
    for name, src in (("waveform.png", "showwavespic=s=1920x260:split_channels=0:colors=0x4fc3f7"),
                      ("spectrogram.png", "showspectrumpic=s=1920x360:legend=0:scale=log:fscale=log")):
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", video, "-filter_complex",
                        f"[0:a]{src},scale=1920:-2,{marks},{secs}", "-frames:v", "1", os.path.join(out, name)])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--threshold", type=float, default=0.3, help="scene-change sensitivity (lower = more cuts)")
    p.add_argument("--keep-video", action="store_true")
    a = p.parse_args()

    meta_r = ytdlp("-J", a.url)
    if meta_r.returncode != 0:
        sys.exit("yt-dlp failed:\n" + meta_r.stderr[-1500:])
    info = json.loads(meta_r.stdout)
    vid = info["id"]
    out = os.path.join(ROOT, "library", "study", vid)
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="dudu-study-")

    # 1. download (<=720p is plenty for analysis) and captions
    r = ytdlp("-f", "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]/b", "--merge-output-format", "mp4",
              "--ignore-errors",  # a failed caption download must not abort the video
              "-o", os.path.join(tmp, "video.%(ext)s"),
              "--write-subs", "--write-auto-subs", "--sub-langs", "he.*,iw.*,en.*", "--sub-format", "vtt",
              a.url)
    got = [f for f in os.listdir(tmp) if f.startswith("video.") and not f.endswith((".vtt", ".part"))]
    if not got:  # some sites only offer webm/mkv; ffmpeg reads those too
        sys.exit("download failed:\n" + r.stderr[-1500:])
    video = os.path.join(tmp, got[0])

    # 2. cuts
    r = subprocess.run([FF, "-hide_banner", "-i", video, "-vf", f"select='gt(scene,{a.threshold})',showinfo",
                        "-f", "null", "-"], capture_output=True, text=True)
    cuts = [float(t) for t in re.findall(r"pts_time:([\d.]+)", r.stderr)]
    dur = float(info.get("duration") or 0)
    bounds = [0.0] + [c for c in cuts if 0.2 < c < dur - 0.1] + [dur]
    shots = [{"n": i + 1, "start": round(s, 2), "end": round(e, 2), "length": round(e - s, 2)}
             for i, (s, e) in enumerate(zip(bounds, bounds[1:])) if e - s > 0.05]
    lengths = sorted(x["length"] for x in shots)
    stats = {
        "shots": len(shots),
        "duration": round(dur, 2),
        "cuts_per_10s": round(len(shots) / dur * 10, 2) if dur else None,
        "median_shot": lengths[len(lengths) // 2] if lengths else None,
        "shortest": lengths[0] if lengths else None,
        "longest": lengths[-1] if lengths else None,
        "threshold": a.threshold,
    }

    # 3. one frame per shot, 12 per sheet, labeled "n  time"
    frames = os.path.join(tmp, "f")
    os.makedirs(frames)
    for x in shots:
        mid = x["start"] + x["length"] / 2
        label = f"{x['n']}  {x['start']:.1f}s  ({x['length']:.1f}s)"
        png = os.path.join(frames, f"{x['n']:04d}.png")
        grab = [FF, "-y", "-loglevel", "error", "-ss", f"{mid:.2f}", "-i", video, "-frames:v", "1", "-vf"]
        labeled = f"scale=480:-2,drawtext=text='{label}':x=8:y=8:fontcolor=yellow:fontsize=22:box=1:boxcolor=black@0.6"
        if subprocess.run(grab + [labeled, png]).returncode != 0:  # drawtext needs a font on some systems
            subprocess.run(grab + ["scale=480:-2", png])
    imgs = sorted(os.listdir(frames))
    for i in range(0, len(imgs), 12):
        batch = os.path.join(tmp, f"batch{i}")
        os.makedirs(batch)
        for j, f in enumerate(imgs[i:i + 12]):
            shutil.copy(os.path.join(frames, f), os.path.join(batch, f"{j:02d}.png"))
        subprocess.run([FF, "-y", "-loglevel", "error", "-framerate", "1", "-i", os.path.join(batch, "%02d.png"),
                        "-vf", "tile=4x3:color=black", "-frames:v", "1",
                        os.path.join(out, f"shots-{i // 12 + 1}.png")])

    # 3b. full-size frame per shot for the storyboard (local only)
    fdir = os.path.join(out, "frames")
    os.makedirs(fdir, exist_ok=True)
    for x in shots:
        mid = x["start"] + x["length"] / 2
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{mid:.2f}", "-i", video, "-frames:v", "1",
                        "-vf", "scale=640:-2", "-q:v", "4", os.path.join(fdir, f"{x['n']:03d}.jpg")])

    # 3c. sound: loudness per 0.5 s, silences, per-shot loudness, waveform + spectrogram with cut lines
    audio = analyse_audio(video, dur, shots)
    if audio:
        json.dump(audio, open(os.path.join(out, "audio.json"), "w"), indent=1)
        audio_images(video, dur, [s["start"] for s in shots[1:]], out)

    # 4. captions
    subs = [f for f in os.listdir(tmp) if f.endswith(".vtt")]
    if subs:
        subs.sort(key=lambda f: (0 if re.search(r"\.(he|iw)", f) else 1, "orig" not in f))
        open(os.path.join(out, "transcript.txt"), "w", encoding="utf-8").write(vtt_to_text(os.path.join(tmp, subs[0])))

    json.dump({"id": vid, "title": info.get("title"), "channel": info.get("channel") or info.get("uploader"),
               "duration": dur, "url": info.get("webpage_url"), "upload_date": info.get("upload_date"),
               "description": (info.get("description") or "")[:1500]},
              open(os.path.join(out, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump({"stats": stats, "shots": shots}, open(os.path.join(out, "shots.json"), "w"), indent=2)

    if a.keep_video:
        shutil.copy(video, os.path.join(out, os.path.basename(video)))
    shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps({"folder": out, **stats, "sheets": len(range(0, len(imgs), 12)),
                      "transcript": bool(subs)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
