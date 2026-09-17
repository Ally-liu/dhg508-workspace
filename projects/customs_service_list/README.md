# Customs Service List 1939 (海關題名錄)

The senior staff of the Chinese Maritime Customs in 1939, turned into a small
SQLite database and a named agent — **「稅務司 / The Commissioner」** — that
answers only from the rows, cites every answer, and says "not in this list"
when the question falls outside the database.

## What is here

- `sources/raw/` — the original scanned leaves from the 1939 *Service List*
  (Internet Archive, item `CustomsServiceList1939`, Public Domain Mark 1.0),
  plus single-page halves split from the two-page spreads.
- `sources/processed/records.json` — the transcribed rows (printed pages 1–5).
- `artifacts/customs.db` — SQLite database, table `service_list`, 103 rows.
- `skills/commissioner/SKILL.md` — the agent's instructions and behaviour rules.
- `code/build_db.py` — rebuilds `artifacts/customs.db` from `records.json`.

## Source

China, The Maritime Customs. IV. Service Series: No. 1. *Service List*,
Sixty-fifth Issue (corrected to 1st June 1939). Shanghai: Statistical
Department of the Inspectorate General of Customs, 1939.

Scope: printed pages 1–5 only — Inspector General; Commissioners; Acting
Commissioners; Deputy Commissioners in Charge; Assistants-in-Charge; Deputy
Commissioners; Acting Deputy Commissioners.

## Method

1. Pulled the item's page images via IIIF and split each two-page spread into
   single pages.
2. Transcribed pp.1–5 by reading the images (the plain OCR text layer of this
   volume garbles the multi-column tables).
3. Checked several rows back against the scans (names, Chinese names, origin,
   dates, station) before building the database.

## Use

```bash
py code/build_db.py
```

Then read `artifacts/customs.db` with Python's `sqlite3` (standard library) —
write small queries. See `skills/commissioner/SKILL.md` for the answering rules.

## Large files / git

The scanned images and `artifacts/customs.db` are large or generated and are
kept out of git by `.gitignore` unless the project explicitly decides otherwise.
