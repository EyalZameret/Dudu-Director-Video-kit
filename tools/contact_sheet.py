"""Make a contact sheet (frames over time) so Claude or a person can review a clip as one image.

Usage:
    python tools/contact_sheet.py project/clips/shot01.mp4            -> 6 frames, saved next to the clip
    python tools/contact_sheet.py project/out/roughcut-v1.mp4 --every 2.5 --cols 6

Use ffmpeg for review, not the browser: browser <video> seeking often returns stale frames.
"""
import argparse
import os
import re
import subprocess

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()


def duration(path):
    r = subprocess.run([FF, "-hide_banner", "-i", path], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    if not m:
        raise SystemExit(f"cannot read {path}: is the path right and is it a video?")
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--every", type=float, default=0, help="seconds between frames (default: 6 frames total)")
    p.add_argument("--cols", type=int, default=3)
    p.add_argument("--out", default="")
    a = p.parse_args()
    d = duration(a.video)
    every = a.every or d / 6
    n = max(1, int(d / every))
    rows = (n + a.cols - 1) // a.cols
    out = a.out or os.path.splitext(a.video)[0] + "-sheet.png"
    vf = (f"select='isnan(prev_selected_t)+gte(t-prev_selected_t\\,{every})',"
          f"scale=480:-2,drawtext=text='%{{pts\\:hms}}':x=8:y=8:fontcolor=yellow:fontsize=20,"
          f"tile={a.cols}x{rows}")
    r = subprocess.run([FF, "-y", "-loglevel", "error", "-i", a.video, "-vf", vf,
                        "-frames:v", "1", "-fps_mode", "vfr", out], capture_output=True, text=True)
    if r.returncode != 0:  # drawtext needs a font on some systems; retry without timestamps
        vf = vf.replace(f"drawtext=text='%{{pts\\:hms}}':x=8:y=8:fontcolor=yellow:fontsize=20,", "")
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", a.video, "-vf", vf,
                        "-frames:v", "1", "-fps_mode", "vfr", out], check=True)
    print(out)
