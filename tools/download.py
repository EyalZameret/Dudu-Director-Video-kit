"""Download a generated clip from its CDN URL (Kling exposes the final mp4 URL in the page's network log).

Usage:
    python tools/download.py "<url>" project/clips/shot01.mp4
"""
import os
import shutil
import sys
import urllib.request

if len(sys.argv) != 3:
    sys.exit('usage: python tools/download.py "<url>" <output.mp4>')
url, out = sys.argv[1], sys.argv[2]
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as r, open(out, "wb") as f:
    shutil.copyfileobj(r, f)
print(out)
