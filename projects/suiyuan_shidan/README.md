# 随园食单 · 掌勺 / The Suiyuan Cook

**像古人一样吃**：把**八部公版古食书**做成数据库，再包成一个小 app——
报上食材，看古人怎么做（**家常优先**）；也可以问某样东西的**性味宜忌**，怎么正确吃。

## 跑起来

```powershell
setx DEEPSEEK_API_KEY "sk-..."      # 一次；然后重开终端
py code\server.py                   # 打开 http://localhost:8000
```

没设 key 时退回**规则模式**，页面仍可演示（页脚会标明）。

## 八部书

- **菜谱**：《随园食单》（袁枚·清）、《山家清供》（林洪·南宋）、
  《易牙遗意》（韩奕·元明）、《养小录》（顾仲·清）。
- **食性**：《饮食须知》（贾铭·元）、《饮膳正要》（忽思慧·元）、
  《食疗本草》（孟诜·唐）、《养生随笔·粥谱》（曹庭栋·清）。

## 规模

**8 部书 · 151 类目 · 2215 条目**（菜谱 1090 / 食性 1051 / 通则 74）·
**269 种食材 · 6913 条"条目–食材"关系**；**家常菜 952 道**、**食性 1051 条**带性味宜忌。

## 结构

```
suiyuan_shidan/
├── code/
│   ├── extract.py        八部书原文 → records.json（含家常标记）
│   ├── make_simplified.py 补简体匹配列
│   ├── make_food.py      食性条目 → 性/味/类/宜忌（真 DeepSeek）
│   ├── make_glosses.py   菜谱条目 → 简体今译（真 DeepSeek）
│   ├── build_db.py       records.json → suiyuan.db
│   ├── server.py         网页 + 真 DeepSeek 调用 + 查库
│   └── static/index.html 两个入口：①有食材怎么做 ②这食材什么性
├── sources/raw/          公版原文（wikisource/ 与 books/），只增不改
├── sources/processed/records.json
├── artifacts/suiyuan.db  6 表：source/section/recipe/ingredient/recipe_ingredient/food_note
└── skills/suiyuan/       渐进式 skill（索引 + answering/maintain/principles + reference）
```

## 重建顺序

```
py code/extract.py && py code/make_simplified.py && py code/make_food.py && py code/make_glosses.py && py code/build_db.py
```

`extract.py` 会重置 `records.json`，其后必须再跑三个 `make_*`，否则简体列/性味/今译会丢。

## 来源与许可

八书作者均逝世逾百年、出版逾百年，**公有领域**；数字文本取自维基文库。
详见 `research/notes/source-note.md`。

## 说明

- 性味/宜忌、今译均为 **DeepSeek 生成的编者补充**，不是原文；食材是机器初标。
- **食疗属古籍记载，非医疗建议。**
- key 与大文件不进 Git。
