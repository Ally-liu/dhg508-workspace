# maintain.md — 怎么加料（同一条流水线，不破旧行）

目标：**加新书/新单/新条目，只跑同样的步骤，旧行原封不动。**

## 目录与流水线

```
sources/raw/wikisource/   随园食单、山家清供、饮食须知 原文
sources/raw/books/<书>/   飲膳正要、食療本草、養生隨筆、易牙遺意、養小錄 原文
        │  py code/extract.py            原文 → records.json（含 家常 标记）
        │  py code/make_simplified.py    补简体匹配列 title_s / name_s
        │  py code/make_food.py          食性条目 → 性/味/类/宜忌
        │  py code/make_glosses.py       菜谱条目 → 简体今译
        ▼
sources/processed/records.json
        │  py code/build_db.py
        ▼
artifacts/suiyuan.db      6 表：source/section/recipe/ingredient/recipe_ingredient/food_note
```

**顺序很重要**：`extract.py` 会重置 `records.json`，其后必须再跑
`make_simplified → make_food → make_glosses`，否则简体列、性味、今译会丢。

## 加一本新食书

1. **存原文**：把公版全文放进 `sources/raw/books/<slug>/`（分页存 `01.txt…`，
   并写 `_titles.txt` 记录标题）。
2. **登记书**：在 `code/extract.py` 的 `BOOKS` 里加一项：书名/作者/年代/URL/许可、
   `kind`（`recipe_book` 或 `food_property`）、`default_entry_kind`（`dish`/`food`）、
   以及 `files` 列表。**每个文件可单独指定** `entry_kind` 与 `topic`（如《飲膳正要》
   里"品物"页是 food、"聚珍異饌"页是 dish）。
3. **抽取→补注→建库**：跑上面四步脚本。
4. **核对**：抽样回原文比正文（见 `research/notes/verification-log.md`）。
5. **同步范围**：改 `SKILL.md` 开场白数字，并在 `improvement-log.md` 记一条。
6. **提交**：说明改了什么、为什么。

## 加/改条目

- **优先改原文**：在对应 raw 文件里补 `===名===` 那段，再重跑脚本——数据库始终等于"原文的投影"。
- 不要直接 `UPDATE artifacts/suiyuan.db`：重跑脚本会覆盖。

## 家常判定

- 在 `code/extract.py`：`LUXURY`（珍馐词表）+ `NON_HOME_SECTIONS`（海鮮單、聚珍異饌）。
- 菜名或正文含珍馐词、或属于非家常单 → `home_style=0`，其余 `=1`。改词表后重跑 extract。

## 食材词表

- 在 `code/extract.py` 的 `INGREDIENTS`（按类分组）。加词后重跑全流水线，并重看假阳性。

## 大文件

- 数据库可提交（能由脚本重建）；大部头/扫描图放 `artifacts/` 下并由 `.gitignore` 排除。
