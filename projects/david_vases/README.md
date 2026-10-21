# 元至正十一年青花云龙纹象耳瓶（大维德花瓶） David Vases

A Week 7 project: take **one object with a history** — the David Vases, a pair of
Yuan-dynasty blue-and-white altar vases dated **1351** — reconstruct it in its
**1351 state**, generate an image of it, and turn it into a 3D model.

The point is the **contrast**: an image built from museum sources should get the
form, the nine bands of decoration and the elephant-head handles right, where a
pure description-driven image stays vague or wrong.

## The object

- **What:** 元至正十一年青花云龙纹象耳瓶，一对（Yuan dynasty, Jingdezhen 景德镇, 1351）.
- **Why it matters:** the dated inscription makes them the **earliest dated
  blue-and-white porcelain** known; they proved blue-and-white predates the Ming.
  BBC *A History of the World in 100 Objects*.
- **History chosen:** the **1351 state** — as consecrated to a Daoist temple,
  when the elephant-head handles still held their **porcelain rings** (now lost,
  only wear marks remain). See `research/design/design_doc.md`.
- **Now:** Sir Percival David Collection, British Museum Room 95,
  **PDF,B.613** and **PDF,B.614**.

## What is here

- `sources/raw/` — original source images (museum photos), unchanged.
- `sources/processed/source-manifest.md` — sources, licences, what each is for.
- `research/design/design_doc.md` — the plan.
- `research/journal/research_journal.md` — dated progress log.
- `research/outputs/` — A/B comparison images and the three written answers.
- `artifacts/` — large generated files (renders, 3D model); git-ignored.
- `code/` — any script used, if needed.

## Sources

See `sources/processed/source-manifest.md`. Lead record:
British Museum collection, PDF,B.613 — https://www.britishmuseum.org/collection/object/A_PDF-B-613
(and PDF,B.614). Photographs from Wikimedia Commons (public domain / CC BY).

## Deliverables (Week 7)

1. Two images side by side — researched (A) vs. bare-description (B) — with the
   three written answers.
2. A 3D model: screenshots or a short screen recording.
3. A "something" made with it (step 4) — TBD.
4. A tool log: what each service did, what the AI did, what I checked myself,
   and at least one real difficulty.

## Notes

- Keep prompts, inputs, outputs and costs for every tool call.
- Model files over a few MB go in `artifacts/` (git-ignored) or an external link.
- Keep API keys out of git.
