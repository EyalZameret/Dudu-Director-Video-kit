"""Assemble animated clips (and optional still images) into one rough cut with ffmpeg.

Usage:
    python tools/build_cut.py project/cut.json

cut.json:
{
  "output": "project/out/roughcut-v1.mp4",
  "grades": {"cold": "eq=saturation=0.88,colorbalance=rm=-0.02:bm=0.025:rh=-0.02:bh=0.02",
             "warm": "eq=saturation=1.05,colorbalance=rm=0.025:bm=-0.02:rh=0.02:bh=-0.015"},
  "fade_out": 1.0,
  "shots": [
    {"clip": "project/clips/shot01.mp4", "from": 0, "to": 3, "grade": "cold"},
    {"image": "project/frames/KF07.jpg", "duration": 2, "zoom": [1.0, 1.08], "grade": "cold"}
  ]
}
Paths are relative to the repo root (the current directory).
Requires: pip install imageio-ffmpeg  (ships a portable ffmpeg, no system install).
"""
import json
import subprocess
import sys

import imageio_ffmpeg

FIT = "scale=1920:1080:force_original_aspect_ratio=increase:out_range=tv,crop=1920:1080,fps=30,setsar=1"


def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    grades = cfg.get("grades", {})
    shots = cfg["shots"]
    args, chains, labels = [ff, "-y"], [], []
    for n, s in enumerate(shots):
        grade = grades.get(s.get("grade", ""), "null")
        if "clip" in s:
            args += ["-i", s["clip"]]
            dur = s["to"] - s["from"]
            chain = f"[{n}:v]trim=start={s['from']}:end={s['to']},setpts=PTS-STARTPTS,{FIT},{grade}"
        else:
            dur = s["duration"]
            z0, z1 = s.get("zoom", [1.0, 1.0])
            frames = int(dur * 30)
            args += ["-loop", "1", "-framerate", "30", "-t", str(dur), "-i", s["image"]]  # default 25 fps made stills short
            chain = (f"[{n}:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,zoompan=z='{z0}+{z1 - z0}*on/{frames}'"
                     f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,"
                     f"trim=duration={dur},setpts=PTS-STARTPTS,setsar=1,{grade}")
        if n == len(shots) - 1 and cfg.get("fade_out"):
            chain += f",fade=t=out:st={dur - cfg['fade_out']}:d={cfg['fade_out']}"
        chains.append(chain + f"[s{n}]")
        labels.append(f"[s{n}]")
    chains.append("".join(labels) + f"concat=n={len(shots)}:v=1:a=0,format=yuv420p[out]")
    args += ["-filter_complex", ";".join(chains), "-map", "[out]",
             "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-level", "4.1",
             "-bf", "2", "-refs", "3", "-pix_fmt", "yuv420p",
             "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
             "-movflags", "+faststart", cfg["output"]]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit(r.returncode)
    total = sum((s["to"] - s["from"]) if "clip" in s else s["duration"] for s in shots)
    print(f"OK {cfg['output']}  ({len(shots)} shots, {total:.1f}s)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "project/cut.json")
