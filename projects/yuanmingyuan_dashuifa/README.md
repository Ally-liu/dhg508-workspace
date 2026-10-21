# 圆明园大水法 Yuanmingyuan Dashuifa (Great Fountain)

A Week 7 project: reconstruct the **Great Fountain (大水法)** and its setting
in the Western Mansions (西洋楼) of the Yuanming Yuan **as it stood before the
1860 destruction**, using period sources — then turn it into an image and a 3D
model.

The point of the exercise is the **contrast**: an image built from research
should get the forms, materials and setting right where a purely
description-driven image stays vague or wrong.

## Scope

- **Object:** 大水法 (the Great Fountain) with its backdrop 远瀛观, in the
  Western Mansions (西洋楼) of the Yuanming Yuan.
- **Stage chosen:** before 1860 (the pre-destruction state), not the ruin.
- **Question:** can period sources carry enough detail to beat a
  no-research generation, and what does the generator still invent?

## What is here

- `sources/raw/` — original source material, unchanged (images, plates, scans).
- `sources/processed/` — cropped/derived images and a source manifest.
- `research/design/design_doc.md` — the plan.
- `research/journal/research_journal.md` — dated progress log.
- `research/references/` — citations and bibliography.
- `artifacts/` — large generated files (renders, 3D models); ignored by git.
- `code/` — any scripts used, if needed.

## Sources (to collect and cite)

Type of material to gather, with an exact citation and a saved copy for each:

1. **西洋楼铜版画 (engraved plates of the Western Mansions)** — the 18th-c.
   set of views that show 大水法 / 远瀛观 in elevation.
2. **Photographs of the ruins** (e.g. late-19th-c. photographers such as
   John Thomson and Ernst Ohlmer) — for massing and ornament, though ruin
   state, not the pre-1860 state.
3. **Visual records / reconstructions** in scholarship (e.g. the 圆明园四十景图
   and modern studies) — as secondary context only.
4. Written descriptions: imperial records, Jesuit accounts (Castiglione /
   Benoist on the waterworks).

Each source: keep the file in `sources/raw/`, record title, creator, date,
holding institution, URL in the manifest.

## Deliverables (Week 7)

1. Two images side by side — researched vs. from-a-bare-description — with the
   three written answers.
2. A 3D model: screenshots or a short screen recording.
3. A "something" made with it (step 4) — TBD.
4. A tool log: what each service did, what the AI did, what I checked myself,
   and at least one real difficulty.

## Notes

- Keep prompts, inputs, outputs and costs for every tool call.
- Model files over a few MB go in `artifacts/` (git-ignored) or an external
  link.
- Keep API keys out of git.
