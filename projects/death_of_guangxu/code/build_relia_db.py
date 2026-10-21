# build_relia_db.py — rebuilds artifacts/relia.db from sources/processed/relia.json
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "sources" / "processed" / "relia.json"
DB = ROOT / "artifacts" / "relia.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS relic_tier (
    tier       INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    era        TEXT NOT NULL,
    fact       TEXT NOT NULL,
    uncertain  TEXT,
    img        TEXT NOT NULL
);
"""


def main() -> None:
    raw = DATA.read_text(encoding="utf-8")
    # 容忍文件头以 # 开头的注释行
    raw = "\n".join(ln for ln in raw.splitlines() if not ln.lstrip().startswith("#"))
    data = json.loads(raw)
    DB.parent.mkdir(exist_ok=True)
    if DB.exists():
        DB.unlink()
    with sqlite3.connect(DB) as conn:
        conn.executescript(SCHEMA)
        conn.executemany(
            "INSERT INTO relic_tier (tier, name, era, fact, uncertain, img) VALUES (?, ?, ?, ?, ?, ?)",
            [(t["tier"], t["name"], t["era"], t["fact"], t.get("uncertain_note"), t["img"])
             for t in data["tiers"]],
        )
        n = conn.execute("SELECT COUNT(*) FROM relic_tier").fetchone()[0]
    print("built", DB.name, "rows:", n)


if __name__ == "__main__":
    main()
