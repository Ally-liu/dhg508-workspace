#!/usr/bin/env python3
"""One-shot lookup for the gazetteer agent.

Usage:
    py code/ask.py 前门
    py code/ask.py 铜锣湾 --city 香港

Matches a name against place.name_zh / place.modern_name / place.name_en /
place_name, writes readable results to artifacts/last_query.txt (UTF-8) and
prints only an ASCII status line, so the console never garbles Chinese.
"""

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "artifacts" / "maps.db"
OUT = ROOT / "artifacts" / "last_query.txt"

SQL = """
SELECT c.name_zh, p.name_zh, p.name_en, pt.name_zh,
       p.modern_name, p.modern_flag,
       group_concat(m.title || '（' || m.map_year || '）', '; ') AS maps,
       p.id, p.lat, p.lon, pr.rename_year, pr.rename_reason, pr.blurb
FROM place p
JOIN city c ON p.city_id = c.id
LEFT JOIN place_type pt ON p.type_code = pt.code
LEFT JOIN map_place mp ON mp.place_id = p.id
LEFT JOIN map m ON m.id = mp.map_id
LEFT JOIN profile pr ON pr.place_id = p.id
WHERE (p.name_zh LIKE ? OR p.modern_name LIKE ? OR p.name_en LIKE ?
       OR p.id IN (SELECT place_id FROM place_name WHERE name LIKE ?))
  AND (? IS NULL OR c.name_zh = ?)
GROUP BY p.id
ORDER BY c.name_zh, p.id
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--city", default=None)
    a = ap.parse_args()
    like = f"%{a.query}%"

    con = sqlite3.connect(DB)
    rows = list(con.execute(SQL, (like, like, like, like, a.city, a.city)))
    con.close()

    lines = [f"查询: {a.query}" + (f"  (限{city})" if (city := a.city) else ""),
             f"命中: {len(rows)} 条", ""]
    for (city, zh, en, typ, mod, flag, maps, pid, lat, lon, ry, rr, blurb) in rows:
        lines.append(f"[{pid}] {zh}" + (f" / {en}" if en else "") + f" | {city} | {typ or ''}")
        if mod and mod != zh:
            lines.append(f"   今名（对照）: {mod}")
        lines.append(f"   出自: {maps}")
        if lat is not None:
            lines.append(f"   坐标（对照，近似）: {lat}, {lon}")
        if ry or rr:
            lines.append(f"   改名: {ry or ''} {rr or ''}".rstrip())
        if blurb:
            lines.append(f"   小百科（编者补充）: {blurb}")
    if not rows:
        lines.append("（无命中）")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"ok n={len(rows)} -> {OUT}")


if __name__ == "__main__":
    main()
