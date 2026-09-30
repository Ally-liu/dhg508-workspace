# Old-map Gazetteer (老地圖地名庫)

A small SQLite database built from **old maps of Chinese cities**, and a named
agent that answers only from the rows: given an old place name or an old map, it
tells you where it is, which map shows it, and (as a flagged cross-reference)
what it is called today — and says "not in this database" when the question
falls outside.

Week 4 of DHG508 asks for a *real database* (3+ tables linked by keys, 200+ rows
each with its source, checked against the originals, able to keep growing) and a
*progressive skill* (a short `SKILL.md` with details on demand, a rubric and test
questions, corner cases, an improvement log).

## Why this topic

- **Mainstream and practical**: like the course demo "show a photo, name the
  building", but with old city maps — anyone can play, and it is genuinely useful
  for reading old maps and looking up old place names.
- **All primary sources**: the maps themselves are the originals; every row is
  read off a map (or a period place-name handbook) and cites it.
- **Diverse cities**, not limited to the treaty ports.

## The chain (as in the course demo)

    old map image → read its labels → rows with a source → SQLite → one skill

## What is here

- `sources/raw/` — the downloaded old-map images, with provenance recorded.
- `sources/processed/records.json` — the transcribed rows, each carrying a
  `source_id`.
- `artifacts/maps.db` — SQLite database (generated; not committed).
- `code/build_db.py` — rebuilds `artifacts/maps.db` from `records.json`.
- `skills/` — the agent's instructions and supporting files.

## Status

- [x] Project scaffold
- [x] 6-table schema and build pipeline (smoke-test seed)
- [ ] Download old maps and transcribe place names (200+ rows)
- [ ] Spot-check against the map images
- [ ] Skill: short `SKILL.md`, rubric, test questions, improvement log
- [ ] Five-minute demo

## Use

```bash
py code/build_db.py
```

Then read `artifacts/maps.db` with Python's `sqlite3` (standard library). See
`skills/` for the answering rules.

## Large files / git

Map images and `artifacts/*.db` are large or generated and are kept out of git by
`.gitignore` unless the project explicitly decides otherwise.
