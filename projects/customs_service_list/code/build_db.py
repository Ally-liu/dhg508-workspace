#!/usr/bin/env python3
"""Build the 1939 Customs Service List SQLite database from records.json.

Usage:
    py code/build_db.py

Reads sources/processed/records.json and writes artifacts/customs.db.
Every row keeps its source page, source leaf image, and source order so any
answer can be traced back to the scan.
"""

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "sources" / "processed" / "records.json"
DB = ROOT / "artifacts" / "customs.db"

COLUMNS = [
    "id", "year", "department", "grade", "name_en", "name_zh",
    "origin", "origin_kind", "origin_ditto",
    "first_appointment", "appointed_rank", "station", "note",
    "source_page", "source_leaf", "source_order",
]


def main() -> None:
    data = json.loads(RECORDS.read_text(encoding="utf-8"))
    records = data["records"]
    DB.parent.mkdir(parents=True, exist_ok=True)

    if DB.exists():
        DB.unlink()

    con = sqlite3.connect(DB)
    con.execute(
        """
        CREATE TABLE service_list (
            id INTEGER PRIMARY KEY,
            year INTEGER NOT NULL,
            department TEXT NOT NULL,
            grade TEXT NOT NULL,
            name_en TEXT,
            name_zh TEXT,
            origin TEXT,
            origin_kind TEXT,
            origin_ditto INTEGER,
            first_appointment TEXT,
            appointed_rank TEXT,
            station TEXT,
            note TEXT,
            source_page INTEGER,
            source_leaf TEXT,
            source_order INTEGER
        )
        """
    )
    placeholders = ", ".join("?" for _ in COLUMNS)
    rows = [[r.get(c) for c in COLUMNS] for r in records]
    con.executemany(f"INSERT INTO service_list ({', '.join(COLUMNS)}) VALUES ({placeholders})", rows)
    con.commit()

    print(f"wrote {DB}")
    print(f"rows: {con.execute('SELECT COUNT(*) FROM service_list').fetchone()[0]}")
    print("\nrows by grade:")
    for grade, n in con.execute(
        "SELECT grade, COUNT(*) FROM service_list GROUP BY grade ORDER BY COUNT(*) DESC"
    ):
        print(f"  {n:3d}  {grade}")
    print("\nrows by origin_kind:")
    for kind, n in con.execute(
        "SELECT origin_kind, COUNT(*) FROM service_list GROUP BY origin_kind"
    ):
        print(f"  {n:3d}  {kind}")
    con.close()


if __name__ == "__main__":
    main()
