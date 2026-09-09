# Project Design Document

## Project Title

- Founding of the Jingshi Library (京师图书馆), 1909–1912

## Project Files

- [Research Journal](../journal/research_journal.md)

## Background and Context

- Late-Qing "New Policies" built new knowledge institutions: schools, museums,
  and libraries on Western and Japanese models.
- The Jingshi Library (京师图书馆) was approved in 1909 by the Board of
  Education (学部) and is recognized as the predecessor of today's National
  Library of China.
- Interests behind the choice: how bureaucracies record things, and the gap
  between an institution being *ordered* and it actually *working*.

## Research Questions

- When was the Jingshi Library founded, and when did it open to the public?
- What exactly did the founding document (the 1909 memorial) ask for, and what
  did "founding" mean in practice?

## Scope

- Two documents, both before 1950: the 1909 founding memorial and a 1912
  opening record. No broader institutional history.

## Methodology

- Locate digitized scans of both documents (archive.org and other open
  collections); keep scans unchanged in `sources/raw/`.
- OCR at least one scan, in this order: LLM API (OpenRouter/DeepSeek) →
  PaddleOCR → OpenCode's own vision as last resort.
- Check OCR output word by word against the image before using it as evidence.

## Sources

1. 学部《奏筹建京师图书馆折》(1909 memorial) — scan to be located.
2. 1912 opening record (government gazette or contemporary press) — to be
   located.

## Expected Outputs

- `assignments/week-02/answer.md`: question, answer, two sources with
  reliability notes, OCR method notes.
- One scan in `sources/raw/` with its checked OCR text in
  `sources/processed/`.

## Working Hypotheses

- Approved 1909 (Xuantong 1), opened 1912 — to be confirmed or corrected
  against the actual documents, not secondhand summaries.

## Risks and Open Questions

- Early-20th-century Chinese printing (vertical, traditional characters) may
  be hard for OCR; results must be verified against the image.
- "Opened" may be claimed by more than one date; the record itself must be
  allowed to decide.

## Action Items

- [ ] Locate a scan of the 1909 memorial
- [ ] Locate a 1912 opening record
- [ ] OCR at least one scan and verify it
- [ ] Write `assignments/week-02/answer.md` and push
