"""Lay a sound design onto a picture cut: music beds, sound effects and voice lines, each placed in
time with its own gain and fades, mixed and muxed into a new mp4.

Usage:
    python tools/mix_audio.py project/sound.json

sound.json:
{
  "video": "project/out/roughcut-v3.mp4",
  "output": "project/out/final-v1.mp4",
  "target_lufs": -14,
  "cues": [
    {"file": "project/sound/tension.mp3", "at": 0,    "gain_db": -6, "fade_in": 0.5, "fade_out": 0.3, "until": 17.5, "bed": true},
    {"file": "project/sound/success.wav", "at": 18.5, "gain_db": 0},
    {"file": "project/sound/vo-line1.wav", "at": 6.2, "gain_db": 2, "duck": true}
  ]
}
- "at": start time in the picture (seconds). "trim": [start, end] inside the source file (optional).
- "until": stop the cue at this picture time (hard stop, or with fade_out). A hard stop on an impact
  ("music cuts dead on the crash") is just "until" with no fade_out.
- "bed": marks a music bed. "duck": while this cue (usually a voice line) plays, every bed dips by 8 dB.
- "target_lufs": loudness of the final mix; -14 suits web and social video.
Output audio: AAC 192 kb/s, 48 kHz stereo.
Requires: pip install imageio-ffmpeg
"""
import json
import re
import subprocess
import sys

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()


def duration(path):
    r = subprocess.run([FF, "-hide_banner", "-i", path], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    if not m:
        sys.exit(f"cannot read {path}: is the path right and is it a media file?")
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])


def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    video, cues = cfg["video"], cfg["cues"]
    total = duration(video)
    for c in cues:
        if "until" in c and c["until"] <= c["at"]:
            sys.exit(f"cue {c['file']}: 'until' ({c['until']}) must be after 'at' ({c['at']})")
    ducks = []
    for c in cues:
        if c.get("duck"):
            length = c["trim"][1] - c["trim"][0] if "trim" in c else duration(c["file"])
            end = min(c["at"] + length, c.get("until", float("inf")))
            ducks.append((c["at"], end))
    args, chains, labels = [FF, "-y", "-i", video], [], []
    for i, c in enumerate(cues, start=1):
        args += ["-i", c["file"]]
        f = [f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo"]
        if "trim" in c:
            f.append(f"atrim={c['trim'][0]}:{c['trim'][1]},asetpts=PTS-STARTPTS")
        length = (c["until"] - c["at"]) if "until" in c else None
        if length:
            f.append(f"atrim=0:{length}")
        if c.get("fade_in"):
            f.append(f"afade=t=in:d={c['fade_in']}")
        if c.get("fade_out") and length:
            f.append(f"afade=t=out:st={max(length - c['fade_out'], 0)}:d={c['fade_out']}")
        f.append(f"volume={c.get('gain_db', 0)}dB")
        if c.get("bed") and ducks:  # music bed: dip under every voice line
            expr = "+".join(f"between(t+{c['at']},{a},{b})" for a, b in ducks)
            f.append(f"volume='if({expr},0.4,1)':eval=frame")
        delay = int(c["at"] * 1000)
        f.append(f"adelay={delay}|{delay}")
        chains.append(",".join(f) + f"[a{i}]")
        labels.append(f"[a{i}]")
    target = cfg.get("target_lufs", -14)
    chains.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,"
                  f"atrim=0:{total},loudnorm=I={target}:TP=-1.5:LRA=11,aresample=48000[aout]")  # loudnorm outputs 192 kHz
    args += ["-filter_complex", ";".join(chains), "-map", "0:v", "-map", "[aout]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", cfg["output"]]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit(r.returncode)
    print(f"OK {cfg['output']}  ({len(cues)} cues, {total:.1f}s, target {target} LUFS)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "project/sound.json")
