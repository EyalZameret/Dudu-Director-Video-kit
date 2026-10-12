"""Measure how much each clip moves, per half second, to find dead time before cutting.

Usage:
    python tools/motion_report.py project/clips/*.mp4

Reading the numbers (mean frame-to-frame difference, 0-255 scale):
    ~0.1-0.5  almost frozen        -> cut it short or drop it
    ~1-3      slow camera move     -> fine for 2-3 seconds
    3+        real action          -> keep this part
Cut each shot to the half-seconds where the action is; most promo shots end up 1.5-4 s long.
"""
import glob
import re
import subprocess
import sys

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()


def motion(path):
    r = subprocess.run([FF, "-hide_banner", "-i", path, "-vf",
                        "scale=320:-2,format=gray,tblend=all_mode=difference,signalstats,"
                        "metadata=print:key=lavfi.signalstats.YAVG", "-f", "null", "-"],
                       capture_output=True, text=True)
    vals = [float(v) for v in re.findall(r"YAVG=([\d.]+)", r.stderr)]
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    secs = int(dur[1]) * 3600 + int(dur[2]) * 60 + float(dur[3]) if dur else 5.0
    per = len(vals) / secs if vals else 24
    bins = []
    for b in range(int(secs * 2)):
        seg = vals[int(b * per / 2):int((b + 1) * per / 2)]
        bins.append(sum(seg) / len(seg) if seg else 0.0)
    return secs, bins


if __name__ == "__main__":
    files = [f for a in (sys.argv[1:] or ["project/clips/*.mp4"]) for f in sorted(glob.glob(a))]
    for f in files:
        secs, bins = motion(f)
        print(f"{f}  ({secs:.1f}s)\n   " + " ".join(f"{v:4.1f}" for v in bins))
