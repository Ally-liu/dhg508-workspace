#!/usr/bin/env python3
"""Overlay a city's old-place coordinates onto a MODERN map image (offline).

Writes an SVG that embeds your map image and draws each place as a dot + label.
Opens in any browser with no network.

Usage:
    py code/overlay_on_image.py --city 香港 --image path/to/modern_map.svg \
        --minlat 22.1200 --maxlat 22.5706 --minlon 113.8222 --maxlon 114.4522 \
        --width 1298 --height 1016 [--attribution "CC BY-SA 3.0 ..."] \
        [--out artifacts/hk_overlay.svg]

Corner lat/lon = the geographic box the image covers:
  minlon,minlat = lower-left;  maxlon,maxlat = upper-right.
The output viewBox auto-zooms to the places (a sub-rect of the image).
"""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "artifacts" / "maps.db"


def main() -> None:
    import sqlite3
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--minlat", type=float, required=True)
    ap.add_argument("--maxlat", type=float, required=True)
    ap.add_argument("--minlon", type=float, required=True)
    ap.add_argument("--maxlon", type=float, required=True)
    ap.add_argument("--width", type=int, default=1000)
    ap.add_argument("--height", type=int, default=1000)
    ap.add_argument("--attribution", default="")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    con = sqlite3.connect(DB_PATH)
    cid = con.execute("SELECT id FROM city WHERE name_zh=?", (args.city,)).fetchone()
    if not cid:
        raise SystemExit("no such city")
    rows = con.execute(
        "SELECT p.name_zh, p.name_en, pt.name_zh, p.lat, p.lon, m.title, m.map_year, p.id "
        "FROM place p LEFT JOIN place_type pt ON p.type_code=pt.code "
        "JOIN map_place mp ON mp.place_id=p.id JOIN map m ON m.id=mp.map_id "
        "WHERE p.city_id=? AND p.lat IS NOT NULL", (cid[0],)).fetchall()
    if not rows:
        raise SystemExit("no coordinates for this city")

    W, H = args.width, args.height
    pts = []
    for name, en, typ, lat, lon, mtitle, myear, pid in rows:
        x = (lon - args.minlon) / (args.maxlon - args.minlon) * W
        y = (args.maxlat - lat) / (args.maxlat - args.minlat) * H
        pts.append((name, x, y))

    xs = [p[1] for p in pts]
    ys = [p[2] for p in pts]
    m = 60
    x0, y0 = max(0, min(xs) - m), max(0, min(ys) - m)
    x1, y1 = min(W, max(xs) + m), min(H, max(ys) + m)
    vw, vh = x1 - x0, y1 - y0
    scale = 1200 / max(vw, vh)  # upscale so text is readable
    Wv, Hv = vw * scale, vh * scale

    import base64
    img = Path(args.image).resolve()
    if img.suffix.lower() == ".svg":
        data = base64.b64encode(img.read_bytes()).decode("ascii")
        href = f"data:image/svg+xml;base64,{data}"
    else:
        mime = "image/png" if img.suffix.lower() == ".png" else "image/jpeg"
        data = base64.b64encode(img.read_bytes()).decode("ascii")
        href = f"data:{mime};base64,{data}"
    base = f'<image x="0" y="0" width="{W}" height="{H}" xlink:href="{href}"/>'
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{Wv:.0f}" height="{Hv:.0f}" viewBox="{x0:.1f} {y0:.1f} {vw:.1f} {vh:.1f}">',
        base,
    ]
    for name, x, y in pts:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="#c00" fill-opacity="0.8" stroke="#fff" stroke-width="0.5"/>')
        parts.append(f'<text x="{x+2.6:.1f}" y="{y+1.2:.1f}" font-family="sans-serif" font-size="4.2" fill="#900" stroke="#fff" stroke-width="0.9" paint-order="stroke">{name}</text>')
    if args.attribution:
        parts.append(f'<text x="{x0+2}" y="{y1-3}" font-family="sans-serif" font-size="3.4" fill="#333">{args.attribution}</text>')
    parts.append("</svg>")
    out = Path(args.out) if args.out else ROOT / "artifacts" / f"{args.city}_overlay.svg"
    out.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", out, "| points:", len(pts), "| view:", f"{vw:.0f}x{vh:.0f}")
    con.close()


if __name__ == "__main__":
    main()
