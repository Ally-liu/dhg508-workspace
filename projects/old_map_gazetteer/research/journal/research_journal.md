# Research Journal

Chronological log of decisions and progress. Newest entries at the bottom.

- [Design Document](../design/design_doc.md)
- [Source Note](../notes/source-note.md)

## 2026-09-29

- Week 4 brief read: "Keep improving it" — a real database (3+ tables, keys,
  200+ rows, each with a source, checked, growable) and a progressive skill
  (short `SKILL.md`, rubric, test questions, corner cases, improvement log).
- Topic search. Ruled out the Maritime Customs line (too niche / user's call).
  Compared candidates for "mainstream + practical + all primary": missionaries,
  Who's Who in China, commercial directories — but those are look-up, not
  playable. Chose **old maps & place names**: it mirrors the course demo (show an
  image, identify it), is understandable, and is genuinely useful.
- Scope decision: **a diverse set of Chinese cities** (not limited to treaty
  ports); a few old city maps each, plus a period place-name handbook for bulk.
- Deleted the earlier unused scaffold `china_postal_stamps`; created this project
  from `templates/project_template` as `projects/old_map_gazetteer`.
- Fixed the v1 schema: `city`, `map`, `place`, `place_name`, `map_place`,
  `source` (6 tables, with a many-to-many `map_place`).
- Verified downloadable primary sources: Wikimedia Commons `Old maps of China`
  and per-city subcategories (北京/南京/成都/广州/西安/开封/太原/昆明 …); the 1908
  *Handbook to map of Fu-Chien* on archive.org (212 pp, PDF/JP2/OCR, not in
  copyright); scattered old city maps on archive.org.
- Wrote `code/build_db.py` and a smoke-test seed to prove the pipeline.
- Range widened to a larger, diverse set of cities; added the Guangdong group
  (廣州/潮州/汕頭/江門) plus 香港 and 澳門.
- Downloaded the 1928 *南京市城市全圖* from Wikimedia Commons (28 MB, PD), made a
  readable 2400px copy plus full-resolution crops, and read the labels by eye.
  Noted that this map prints labels **right-to-left** (title reads 圖全市城京南).
- Transcribed **64 Nanjing places** (gates, hills, lakes, temples, schools,
  government offices, bridges, streets, granaries, grounds) into `records.json`,
  plus 12 `place_name` variants (romanised / map-order forms) and 64 `map_place`
  links. Database now: 143 rows across 6 tables. Spot-checked a three-table join.
- Console note: Chinese in the PowerShell console shows as mojibake; the stored
  data and the database are correct (verified by re-reading via files).
- Transcribed four cities from public-domain maps, reading labels by eye from
  full-resolution crops made in `artifacts/crops/`:
  - 香港, 1888 *A Map of Hong-Kong, with British Kowloon* (BnF) — 65 places,
    incl. the map's own "Names of Villages" index.
  - 廣州, 1936 *廣州市馬路圖* (廣州市工務局) — 58 places; labels right-to-left?
    checked; small labels marked where doubtful.
  - 澳門, 1945 War Office *China. Macao. Plan of town* (1:5000) — 50 places.
- Database now **521 rows** across 6 tables (place 237, map_place 237,
  place_name 35, source/city/map 4 each). Wrote a summary to
  `research/outputs/db_summary.md`.
- Stop per plan (target ~500). Further cities (北京/成都/西安/…) remain as an
  improvement-log increment.
- Added 北京 (清代《京师城内首善全图》, 52 places) and converted the whole database
  to **Simplified Chinese** (character-level mapping, since pip/zhconv was
  unavailable).
- Wrote the skill `skills/gazetteer/`: a short `SKILL.md` with a startup message
  (lists the 5 cities and what can be asked), strict DB-only rules, a professional
  assistant tone, plus `reference/`, `rubric.md`, `test-questions.md`,
  `improvement-log.md`.
- Upgrade pass: filled `modern_name` for **all 289 places** (26 marked
  `modern_flag=1` as cross-references); added a controlled `place_type` vocabulary
  (45 codes) and `place.type_code`; added coordinate columns (`place.lat/lon`,
  `map.min_lat…`) left empty on purpose. Database now **678 rows / 7 tables**.
