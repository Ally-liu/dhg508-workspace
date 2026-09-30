#!/usr/bin/env python3
"""Build the old-map gazetteer SQLite database from records.json.

Usage:
    py code/build_db.py

Reads sources/processed/records.json and writes artifacts/maps.db.

Schema, tables linked by keys:

    source(id)  <-- source_id -- every table
    city(id)    <-- city_id -- map, place
    map(id)     <-- map_id -- map_place
    place_type(code) <-- type_code -- place
    place(id)   <-- place_id -- place_name, map_place
    place_name  (one place may have several old written forms)

Every row keeps a source_id so any answer can be traced back to the exact map.
Coordinate columns (place.lat/lon, map.min_lat...) exist but are not yet filled.
Tables with no rows yet are still created, so the database can keep growing.
"""

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "sources" / "processed" / "records.json"
DB = ROOT / "artifacts" / "maps.db"

SCHEMA = """
CREATE TABLE source (
    id          INTEGER PRIMARY KEY,
    title       TEXT NOT NULL,
    title_en    TEXT,
    author      TEXT,
    year        TEXT,
    publisher   TEXT,
    archive     TEXT,
    url         TEXT,
    license     TEXT,
    access_date TEXT,
    note        TEXT
);

CREATE TABLE city (
    id          INTEGER PRIMARY KEY,
    name_zh     TEXT NOT NULL,
    name_en     TEXT,
    province    TEXT,
    modern_note TEXT,
    source_id   INTEGER REFERENCES source(id)
);

CREATE TABLE map (
    id         INTEGER PRIMARY KEY,
    city_id    INTEGER REFERENCES city(id),
    title      TEXT NOT NULL,
    map_year   TEXT,
    map_type   TEXT,
    publisher  TEXT,
    scale      TEXT,
    image_file TEXT,
    min_lat    REAL,
    max_lat    REAL,
    min_lon    REAL,
    max_lon    REAL,
    note       TEXT,
    source_id  INTEGER REFERENCES source(id)
);

CREATE TABLE place_type (
    code    TEXT PRIMARY KEY,
    name_zh TEXT NOT NULL,
    category TEXT
);

CREATE TABLE place (
    id          INTEGER PRIMARY KEY,
    city_id     INTEGER REFERENCES city(id),
    name_zh     TEXT,
    name_en     TEXT,
    place_type  TEXT,
    type_code   TEXT REFERENCES place_type(code),
    modern_name TEXT,
    modern_flag INTEGER DEFAULT 0,
    lat         REAL,
    lon         REAL,
    note        TEXT,
    source_id   INTEGER REFERENCES source(id)
);

CREATE TABLE place_name (
    id        INTEGER PRIMARY KEY,
    place_id  INTEGER NOT NULL REFERENCES place(id),
    form      TEXT,
    name      TEXT NOT NULL,
    note      TEXT,
    source_id INTEGER REFERENCES source(id)
);

CREATE TABLE map_place (
    id           INTEGER PRIMARY KEY,
    map_id       INTEGER NOT NULL REFERENCES map(id),
    place_id     INTEGER NOT NULL REFERENCES place(id),
    label_on_map TEXT,
    sheet        TEXT,
    note         TEXT,
    source_id    INTEGER REFERENCES source(id)
);

CREATE TABLE profile (
    place_id      INTEGER PRIMARY KEY REFERENCES place(id),
    rename_year   TEXT,
    rename_reason TEXT,
    blurb         TEXT,
    source_id     INTEGER REFERENCES source(id)
);
"""

# Insertion order respects foreign keys.
TABLES = ["source", "city", "map", "place_type", "place", "place_name",
          "map_place", "profile"]

COLUMNS = {
    "source": ["id", "title", "title_en", "author", "year", "publisher",
               "archive", "url", "license", "access_date", "note"],
    "city": ["id", "name_zh", "name_en", "province", "modern_note", "source_id"],
    "map": ["id", "city_id", "title", "map_year", "map_type", "publisher",
            "scale", "image_file", "min_lat", "max_lat", "min_lon", "max_lon",
            "note", "source_id"],
    "place_type": ["code", "name_zh", "category"],
    "place": ["id", "city_id", "name_zh", "name_en", "place_type", "type_code",
              "modern_name", "modern_flag", "lat", "lon", "note", "source_id"],
    "place_name": ["id", "place_id", "form", "name", "note", "source_id"],
    "map_place": ["id", "map_id", "place_id", "label_on_map", "sheet", "note",
                  "source_id"],
    "profile": ["place_id", "rename_year", "rename_reason", "blurb", "source_id"],
}


def build() -> None:
    data = json.loads(RECORDS.read_text(encoding="utf-8"))
    DB.parent.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA)

    for table in TABLES:
        rows_in = data.get(table, [])
        if not rows_in:
            continue
        cols = COLUMNS[table]
        placeholders = ", ".join("?" for _ in cols)
        sql = (f"INSERT INTO {table} ({', '.join(cols)}) "
               f"VALUES ({placeholders})")
        con.executemany(sql, [[r.get(c) for c in cols] for r in rows_in])

    con.commit()

    print(f"wrote {DB}")
    for table in TABLES:
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {n:4d}  {table}")

    print("\nplaces by city:")
    for name, n in con.execute(
        "SELECT c.name_zh, COUNT(*) FROM place p "
        "JOIN city c ON p.city_id = c.id "
        "GROUP BY c.name_zh ORDER BY COUNT(*) DESC"
    ):
        print(f"  {n:4d}  {name}")

    con.close()


if __name__ == "__main__":
    build()
