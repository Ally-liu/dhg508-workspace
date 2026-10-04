#!/usr/bin/env python3
"""Build artifacts/suiyuan.db from records.json.

Usage:
    py code/build_db.py

Tables:
    source, section, recipe, ingredient, recipe_ingredient, food_note
- recipe holds every entry (dish / food / rule); nature+flavor+food_category
  describe a food entry; home_style marks a home-style dish.
- ingredient aggregates a food's nature/flavor (matched by name) and is linked
  to food_note (the ancient 宜忌/主治 text).
"""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "sources" / "processed" / "records.json"
DB = ROOT / "artifacts" / "suiyuan.db"

SCHEMA = """
CREATE TABLE source (
    id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT, year INTEGER,
    edition TEXT, url TEXT, license TEXT, note TEXT,
    kind TEXT          -- recipe_book | food_property
);
CREATE TABLE section (
    id INTEGER PRIMARY KEY, source_id INTEGER NOT NULL REFERENCES source(id),
    part INTEGER, name TEXT NOT NULL, kind TEXT NOT NULL,
    entry_kind TEXT NOT NULL,   -- dish | food | rule
    order_index INTEGER
);
CREATE TABLE recipe (
    id INTEGER PRIMARY KEY, section_id INTEGER NOT NULL REFERENCES section(id),
    title TEXT NOT NULL, title_s TEXT, text TEXT NOT NULL,
    gloss TEXT,                 -- 今译（dish）或 宜忌注（food），编者补充
    nature TEXT,                -- 性: 寒/凉/平/温/热/无
    flavor TEXT,                -- 味: 甘、苦 …
    food_category TEXT,         -- 水/火/谷/菜/果/味/鱼/禽/兽/乳/药/其他
    home_style INTEGER,         -- 1 家常 / 0 非家常（仅 dish）
    order_in_section INTEGER, note TEXT
);
CREATE TABLE ingredient (
    id INTEGER PRIMARY KEY, name_zh TEXT NOT NULL UNIQUE, name_s TEXT,
    category TEXT, nature TEXT, flavor TEXT, note TEXT
);
CREATE TABLE recipe_ingredient (
    recipe_id INTEGER NOT NULL REFERENCES recipe(id),
    ingredient_id INTEGER NOT NULL REFERENCES ingredient(id),
    term TEXT NOT NULL, PRIMARY KEY (recipe_id, ingredient_id)
);
CREATE TABLE food_note (
    id INTEGER PRIMARY KEY, ingredient_id INTEGER REFERENCES ingredient(id),
    recipe_id INTEGER REFERENCES recipe(id),
    kind TEXT, text TEXT
);
CREATE INDEX idx_recipe_section ON recipe(section_id);
CREATE INDEX idx_recipe_kind ON recipe(home_style);
CREATE INDEX idx_ri_ingredient ON recipe_ingredient(ingredient_id);
CREATE INDEX idx_foodnote_ing ON food_note(ingredient_id);
"""


def main() -> None:
    data = json.loads(RECORDS.read_text(encoding="utf-8"))
    secs = {s["id"]: s for s in data["sections"]}
    DB.parent.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA)

    con.executemany("INSERT INTO source(id,title,author,year,edition,url,license,note,kind)"
                    " VALUES (?,?,?,?,?,?,?,?,?)",
                    [(s["id"], s["title"], s["author"], s["year"], s["edition"],
                      s["url"], s["license"], s["note"], s.get("kind")) for s in data["sources"]])
    con.executemany("INSERT INTO section(id,source_id,part,name,kind,entry_kind,order_index)"
                    " VALUES (?,?,?,?,?,?,?)",
                    [(s["id"], s["source_id"], s["part"], s["name"], s["kind"],
                      s["entry_kind"], s["order"]) for s in data["sections"]])
    con.executemany("INSERT INTO recipe(id,section_id,title,title_s,text,gloss,nature,flavor,"
                    "food_category,home_style,order_in_section,note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    [(r["id"], r["section_id"], r["title"], r.get("title_s"), r["text"],
                      r.get("gloss"), r.get("nature"), r.get("flavor"), r.get("food_category"),
                      r.get("home_style"), r.get("order_in_section"), None)
                     for r in data["recipes"]])
    con.executemany("INSERT INTO ingredient(id,name_zh,name_s,category,nature,flavor,note)"
                    " VALUES (?,?,?,?,?,?,?)",
                    [(i["id"], i["name_zh"], i.get("name_s"), i["category"], None, None, None)
                     for i in data["ingredients"]])
    con.executemany("INSERT INTO recipe_ingredient(recipe_id,ingredient_id,term) VALUES (?,?,?)",
                    [(r["recipe_id"], r["ingredient_id"], r["term"])
                     for r in data["recipe_ingredients"]])

    # aggregate food nature onto ingredients + build food_note
    by_name = {i["name_zh"]: i["id"] for i in data["ingredients"]}
    by_s = {i.get("name_s"): i["id"] for i in data["ingredients"] if i.get("name_s")}
    fn = 0
    for r in data["recipes"]:
        if secs[r["section_id"]]["entry_kind"] != "food":
            continue
        iid = by_name.get(r["title"]) or by_s.get(r.get("title_s"))
        if not iid:
            continue
        con.execute("UPDATE ingredient SET nature=COALESCE(nature,?), flavor=COALESCE(flavor,?)"
                    " WHERE id=?", (r.get("nature"), r.get("flavor"), iid))
        con.execute("INSERT INTO food_note(ingredient_id,recipe_id,kind,text) VALUES (?,?,?,?)",
                    (iid, r["id"], "宜忌主治", r.get("gloss") or r["text"]))
        fn += 1
    con.commit()

    print(f"wrote {DB}")
    for t in ("source", "section", "recipe", "ingredient", "recipe_ingredient", "food_note"):
        print(f"  {con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]:5d}  {t}")
    for k, n in con.execute("SELECT entry_kind, COUNT(*) FROM section GROUP BY entry_kind"):
        print(f"    section.{k}: {n}")
    print("  recipes by kind:",
          dict(con.execute("SELECT s.entry_kind, COUNT(*) FROM recipe r "
                           "JOIN section s ON s.id=r.section_id GROUP BY s.entry_kind")))
    print("  home-style dishes:",
          con.execute("SELECT COUNT(*) FROM recipe WHERE home_style=1").fetchone()[0])
    con.close()


if __name__ == "__main__":
    main()
