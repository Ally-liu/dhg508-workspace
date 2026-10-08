# build_db.py — rebuilds artifacts/guangxu.db from sources/processed/records.json
# Run: py code/build_db.py  (Python 3.12+, stdlib only)
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "sources" / "processed" / "records.json"
DB = ROOT / "artifacts" / "guangxu.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS source (
    id    TEXT PRIMARY KEY,        -- S1, S2, ...
    title TEXT NOT NULL,
    tier  TEXT NOT NULL,           -- L1/L2/L3
    note  TEXT
);

CREATE TABLE IF NOT EXISTS evidence (
    id        TEXT PRIMARY KEY,    -- E01, D01, ...
    source_id TEXT NOT NULL REFERENCES source(id),
    date_orig TEXT,                -- 原文纪年，原样保留
    date_iso  TEXT,                -- 换算后的公历（可能带 ?，未核）
    kind      TEXT NOT NULL,       -- quote_event / quote_official / fact / finding / hypothesis_summary
    tier      TEXT NOT NULL,
    stance    TEXT NOT NULL,       -- official / private / press / science / academic
    text      TEXT NOT NULL,       -- 原文摘录或忠实转写
    note      TEXT
);

CREATE TABLE IF NOT EXISTS contradiction (
    pair      INTEGER NOT NULL,    -- 矛盾对编号
    member    TEXT NOT NULL REFERENCES evidence(id),
    topic     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS verdict (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    choice   TEXT NOT NULL,        -- 四假说之一 / "证据不足"
    reason   TEXT,                 -- 可空：体验者一句话理由
    created  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def main() -> None:
    data = json.loads(RECORDS.read_text(encoding="utf-8"))
    DB.parent.mkdir(exist_ok=True)
    if DB.exists():
        DB.unlink()
    with sqlite3.connect(DB) as conn:
        conn.executescript(SCHEMA)
        conn.executemany(
            "INSERT INTO source (id, title, tier, note) VALUES (?, ?, ?, ?)",
            [(s["id"], s["title"], s["tier"], s.get("note")) for s in data["sources"]],
        )
        conn.executemany(
            "INSERT INTO evidence (id, source_id, date_orig, date_iso, kind, tier, stance, text, note)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (r["id"], r["source"], r.get("date_orig"), r.get("date_iso"),
                 r["kind"], r["tier"], r["stance"], r["text"], r.get("note"))
                for r in data["rows"]
            ],
        )
        conn.executemany(
            "INSERT INTO contradiction (pair, member, topic) VALUES (?, ?, ?)",
            [
                (p["pair"], m, p["topic"])
                for p in data["contradict_pairs"]
                for m in p["members"]
            ],
        )
        counts = {
            "sources": conn.execute("SELECT COUNT(*) FROM source").fetchone()[0],
            "evidence": conn.execute("SELECT COUNT(*) FROM evidence").fetchone()[0],
            "contradiction_members": conn.execute("SELECT COUNT(*) FROM contradiction").fetchone()[0],
        }
    print("built", DB.name, counts)


if __name__ == "__main__":
    main()
