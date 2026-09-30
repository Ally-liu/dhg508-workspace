# Source note: old maps of Chinese cities

## The subject

Historical maps of Chinese cities (roughly 1800s–1940s), and the place names
written on them: city walls and gates, hills, rivers, temples, streets, and
districts. The maps are the **primary sources**; every row is read off a map by
eye, as in the course demo where a page is read by eye and checked against the
machine text.

## Source hierarchy

Every row cites one source. Prefer clearly public-domain maps.

### T1 — the maps themselves (primary)

- **Wikimedia Commons, `Category:Old maps of China`** and its per-city
  subcategories, e.g. `Old maps of Beijing`, `Old maps of Nanjing`,
  `Old maps of Chengdu`, `Old maps of Guangzhou`, `Old maps of Xi'an`,
  `Old maps of Kaifeng`, `Old maps of Taiyuan`, `Old maps of Kunming`,
  `Old maps of Changsha`, `Old maps of Fuzhou`. Each file page gives the licence
  and a direct image URL (via the Commons API).
- Individual old city maps on **archive.org** (public domain), e.g. the 1948
  Shanghai aerial maps.

### T1 — period place-name handbook (primary)

- Great Britain, War Office, General Staff, Geographical Section, *Handbook to
  map of Fu-Chien (G.S.G.S. no. 2165), giving Chinese characters and
  pronunciation for the names shewn on the map … with a list of some Chinese
  words used in geographical nomenclature* (London: H.M. Stationery Office,
  [1908]). archive.org item `handbooktomapoff00grearich` — 212 pp.; PDF, JP2,
  and OCR text; reported not in copyright (University of California Libraries).

### T2 — supporting (cross-reference only, never the sole basis)

- Modern gazetteers and maps, used **only** to fill the flagged `modern_name`
  cross-reference column (which is not original map content).

## What we check, and how

- For each sampled row, open the map image and confirm the name is written as
  transcribed; record the result here.
- Where a label is illegible or ambiguous, keep the doubt in `note`; do not guess.

## Conventions

- `place.name_zh` / `place_name` hold the form **as written on the map**. The
  modern name, if any, goes in `place.modern_name` with `modern_flag = 1`.
- Romanised forms found on foreign-produced maps ("Canton", "Nanking") are kept
  in `place_name` alongside the Chinese.

## Limits

- Old maps are selective: they show what mattered then.
- Boundary and spelling conventions change over time; the same place may appear
  under several names on different maps.
