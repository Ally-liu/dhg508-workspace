# artifacts/

Generated / rebuildable outputs live here.

- `suiyuan.db` — the SQLite database, rebuilt from
  `sources/processed/records.json` by `code/build_db.py`. It is small and
  committed so the app and the skill can run straight away; if you delete it,
  regenerate it with:

  ```bash
  py code/extract.py      # raw wikitext -> records.json
  py code/build_db.py     # records.json -> suiyuan.db
  ```

Nothing here is hand-edited. Change `sources/raw/` or `code/`, then re-run the
two scripts.
