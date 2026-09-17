# Research Journal

Chronological log of decisions and progress. Newest entries at the bottom.

- [Design Document](../design/design_doc.md)

## 2026-09-17

- Chose the Week 3 topic: a database from the Chinese Maritime Customs
  *Service List* (題名錄), and an agent that answers only from it.
- Reconnaissance: Internet Archive has three issues — `CustomsServiceList1939`
  (No. 65, English-only), `CustomsServiceList1947` (No. 73) and
  `CustomsServiceList1948` (No. 74), both bilingual with garbled Chinese OCR.
  Also noted Academia Sinica's Chinese Maritime Customs database (Service List
  1875–1947) as a possible cross-check.
- Picked the **1939** issue (clean printed English tables, public domain).
- Scope decision: **senior posts only**, printed pp.1–5. Grades:
  Inspector General, Commissioners, Acting Commissioners, Deputy Commissioners
  in Charge, Assistants-in-Charge, Deputy Commissioners, Acting Deputy
  Commissioners. (Chosen for a small, clean, traceable dataset that still
  supports the "who reached the top" question.)
- Created project from `templates/project_template`. Downloaded leaves 4–9 via
  IIIF and split each spread into left/right pages into `sources/raw/`.
- Discovered two things that matter for grounding: (a) the `origin` column
  gives a **province** for Chinese staff and a **nationality** for foreigners;
  (b) dates/values repeat with a vertical ditto mark. Decided to store `origin`
  resolved (flagged `origin_ditto`) and keep dates literal with `〃` for ditto.
- Transcribed pp.1–5 into `sources/processed/records.json` (103 rows).
- Built `artifacts/customs.db` with `code/build_db.py` (Python stdlib sqlite3).
- Spot-checked ids 5–10 and 82–84 against the scans: all matched.
- Chose the agent: name **「稅務司 / The Commissioner」**, tone: a meticulous
  Customs Commissioner (despatch style, citations, no improvisation),
  out-of-database behaviour: "not in this list" + a pointer to where it might
  be found. Wrote `skills/commissioner/SKILL.md`.

## 2026-09-17 (continued)

- Added an opening statement (range navigation) to the skill; simplified-Chinese
  answers; bilingual Chinese/English names and places.
- Verified the place-name translations against treaty-port and customs
  references (Lappa = 拱北 per Macau customs-history sources; Liuchow = 柳州 per
  postal romanization; Santuao = 三都澳; Kuantou = 琯头; Tungchung = 东冲;
  Chung-shan Port = 中山港). Skill now says: use only verified renderings,
  otherwise English only.
- Resolved the 5 rows whose `station` had been kept as the source ditto mark
  (ids 63, 72, 94, 99, 103) and rebuilt the database.
- Wrote the five-minute demo script: `research/outputs/demo-script.md`.
- Source note added: `research/notes/source-note.md`.

