# Project Design Document

## Project Title

- 老地圖地名庫 — Old-map Gazetteer
- A database of place names read from old maps of Chinese cities, and an agent
  that uses it to answer "where was this / what is it now".

## Project Files

- [Research Journal](../journal/research_journal.md)
- [Source Note](../notes/source-note.md)

## Background and Context

Week 4 of DHG508 ("Keep improving it") requires:

- **A real database**: 3+ tables linked by keys; 200+ rows, each with its source;
  checked against the originals; able to keep growing.
- **A progressive skill**: a short `SKILL.md` with details on demand; a rubric and
  test questions; the corner cases it handles; an improvement log (3+ entries).

The course demo works like a recogniser: show a photo, name the building. This
project does the same with **old maps**: show an old map (or give an old place
name) and get back which city and year it is, which map shows the name, and what
the place is called today.

It is deliberately **mainstream and practical**, and every row comes from a
**primary source** — the map itself, read by eye (as in the demo, where a page is
read by eye and checked against the PDF text layer).

## Research Questions

- Which historical place names appear on old maps of Chinese cities, of what
  type (gate / hill / river / temple / street / district), and on which map?
- What modern name (if any) corresponds to each — flagged as a cross-reference,
  not as original content?
- Can the agent answer only from the rows and cite each one exactly?

## Scope

- **Time**: roughly 1800s–1940s old city maps (a few earlier/later where useful).
- **Place**: a **diverse set of Chinese cities** — not limited to treaty ports.
  Planned and grown city by city (e.g. 北京 Beijing, 南京 Nanjing, 成都 Chengdu,
  开封 Kaifeng, 西安 Xi'an, 太原 Taiyuan, 昆明 Kunming, 长沙 Changsha, 广州
  Guangzhou, 福州 Fuzhou).
- **Out of scope for v1**: a full national gazetteer; modern administrative data;
  anything not present on a map or in a period place-name handbook.

## Methodology

1. Fix the v1 schema (below), with every table traceable to a `source`.
2. Download the old-map image into `sources/raw/`; record its provenance.
3. Read the labels off the map by eye (and compare with any OCR/text, as in the
   demo); transcribe them into `sources/processed/records.json`, each with a
   `source_id`.
4. Build `artifacts/maps.db` with `code/build_db.py` (Python stdlib `sqlite3`).
5. Spot-check sampled rows back against the map image; record what was and was
   not verified.
6. Write a short `SKILL.md` plus on-demand `reference/` files, a `rubric.md`,
   `test_questions.md`, and an `improvement_log.md`.

## Schema (v1)

Six tables. Keys are shown with arrows.

```text
source(id) ──source_id──> every table

city(id) ──city_id──> map(id)
                    └─> place(id)

place(id) ──place_id──> place_name(id)      (one place may have many old forms)

map_place(map_id, place_id)                 (a place appears on a map)  ← M:N
```

| Table | One row is | Key links |
|---|---|---|
| `city` | a city (古今名, 省) | `id` ← `map.city_id`, `place.city_id` |
| `map` | one old map (title, year, type, image) | `city_id` →; `id` ← `map_place.map_id` |
| `place` | one place on a map (old name, type, flagged modern name) | `city_id` →; `id` ← `place_name.place_id`, `map_place.place_id` |
| `place_name` | one written form / variant of a place | `place_id` → |
| `map_place` | a place's appearance on a map (label, sheet) | `map_id` →, `place_id` → |
| `source` | one citable original map or handbook | `source_id` ← every table |

## Sources

- **Wikimedia Commons** — `Category:Old maps of China` and its per-city
  subcategories (北京, 南京, 成都, 开封, 西安, 太原, 昆明, 长沙, 广州, 福州, …).
  Public-domain files with licence and image metadata via the Commons API.
- **archive.org** — period place-name handbooks, e.g. the 1908 *Handbook to map
  of Fu-Chien (G.S.G.S. no. 2165)* (Chinese characters + pronunciation for the
  names on the map; 212 pp.; not in copyright).
- Individual old city maps on archive.org and other public-domain collections.

## Expected Outputs

- `artifacts/maps.db` — SQLite, 6 tables including `source`.
- `skills/<name>/` — short `SKILL.md` + `reference/`, `rubric.md`,
  `test_questions.md`, `improvement_log.md`.
- `research/outputs/demo-script.md` — the five-minute demo.

## Working Hypotheses

- 200+ rows are reachable by reading place names off a dozen city maps.
- The old→modern name link is the most useful, and the most delicate: it must be
  flagged as a cross-reference, because it is not on the original map.

## Risks and Open Questions

- Reading tiny map labels by eye is slow and error-prone; keep `note` for doubt
  and do not guess.
- Licensing: prefer clearly public-domain files (Commons/archive.org PD); record
  the licence per source.
- Some maps label in Chinese, some in romanisation; keep both forms in
  `place_name` rather than forcing one.

## Action Items

- [x] Fix v1 schema (6 tables)
- [x] Build pipeline (`records.json` → `maps.db`) with a smoke-test seed
- [ ] Download maps and transcribe 200+ rows
- [ ] Spot-check against the map images
- [ ] Write the skill, rubric, test questions, and improvement log
- [ ] Write the demo script
