#!/usr/bin/env python3
"""One-line overlay: put a city's old-place dots on its configured modern map.

Usage:
    py code/city_map.py 香港 --open

Reads code/basemaps.json and calls overlay_on_image.py. Writes
artifacts/<city>_overlay.svg (offline; open in a browser).
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = ROOT / "code" / "basemaps.json"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("city")
    ap.add_argument("--open", action="store_true")
    a = ap.parse_args()

    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    e = cfg.get(a.city)
    if not e:
        raise SystemExit(f"no base map configured for: {a.city}")

    out = ROOT / "artifacts" / f"{a.city}_overlay.svg"
    cmd = [
        sys.executable, str(ROOT / "code" / "overlay_on_image.py"),
        "--city", a.city, "--image", str(ROOT / e["image"]),
        "--minlat", str(e["minlat"]), "--maxlat", str(e["maxlat"]),
        "--minlon", str(e["minlon"]), "--maxlon", str(e["maxlon"]),
        "--width", str(e["width"]), "--height", str(e["height"]),
        "--attribution", e.get("attribution", ""), "--out", str(out),
    ]
    subprocess.run(cmd, check=True)
    if a.open:
        import webbrowser
        webbrowser.open(out.as_uri())


if __name__ == "__main__":
    main()
