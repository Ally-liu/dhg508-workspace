# reference/schema.md — 库结构

文件：`artifacts/suiyuan.db`（SQLite，6 张表）。用 Python `sqlite3` 直读。

```
source(id) ──source_id──> section(id) ──section_id──> recipe(id)
                                                          │
ingredient(id) ──ingredient_id──> recipe_ingredient(recipe_id, ingredient_id)
recipe(id) ──recipe_id──> food_note(ingredient_id, recipe_id)
```

| 表 | 一行是 | 常用字段 | 行数 |
|---|---|---|---|
| `source` | 一部书 | `title`, `author`, `year`, `kind`（recipe_book/food_property） | 8 |
| `section` | 一个类目/单/卷 | `name`, `source_id`, `kind`（rule/entry）, `entry_kind`（dish/food/rule） | 141 |
| `recipe` | 一个条目 | `title`, `title_s`, `text` **原文**, `gloss` **今译/宜忌（编者补充）**, `nature`, `flavor`, `food_category`, `home_style`, `section_id` | 2197 |
| `ingredient` | 一种食材 | `name_zh`, `name_s`, `category`, `nature`, `flavor` | 269 |
| `recipe_ingredient` | "某条目用了某料" | `recipe_id`, `ingredient_id`, `term` | 6750 |
| `food_note` | 某食材的一条宜忌/主治 | `ingredient_id`, `recipe_id`, `text` | 163 |

## 八部书

| id | 书名 | 作者 | 年代 | kind |
|---|---|---|---|---|
| 1 | 隨園食單 | 袁枚 | 1792 | recipe_book |
| 2 | 山家清供 | 林洪 | 南宋 | recipe_book |
| 3 | 飲食須知 | 賈銘 | 元 | food_property |
| 4 | 飲膳正要 | 忽思慧 | 元 | food_property |
| 5 | 食療本草 | 孟詵 | 唐 | food_property |
| 6 | 養生隨筆·粥譜 | 曹庭棟 | 清 | food_property |
| 7 | 易牙遺意 | 韓奕 | 元明 | recipe_book |
| 8 | 養小錄 | 顧仲 | 清 | recipe_book |

## 关键理解

- **`section.entry_kind`**：`dish`＝菜谱，`food`＝食性（食材性味宜忌），`rule`＝序/戒律/通则。
  **按食材找菜、查菜只看 `dish`；查性味只看 `food`。**
- **`recipe.text` 是繁体原文**，最终依据。`recipe.title` 可能含食材，找食材时比对 `title+text`。
- **`recipe.nature/flavor`**：食性条目的**性**（寒/凉/平/温/热/无）与**味**（酸苦甘辛咸淡涩）。
- **`recipe.home_style`**：1＝家常，0＝非家常（含珍馐词或属海鮮單/聚珍異饌）。**排序时家常优先。**
- **`recipe.gloss`**：dish 是简体**今译**、food 是**宜忌注**；均为 DeepSeek 生成，**标"编者补充"**。
- **`title_s` / `name_s` 只是简体匹配列**，原文一律以 `title` / `name_zh` 为准。
- **`food_note`**：把食性条目按食材名归并出的宜忌，供"某食材宜忌"聚合。

## 查询示例

```python
import sqlite3
con = sqlite3.connect("artifacts/suiyuan.db")

# 按食材找菜（家常优先）
con.execute("""
SELECT r.id, r.title, src.title AS book, r.home_style, COUNT(*) hit
FROM recipe_ingredient ri JOIN ingredient i ON i.id=ri.ingredient_id
JOIN recipe r ON r.id=ri.recipe_id JOIN section s ON s.id=r.section_id
JOIN source src ON src.id=s.source_id
WHERE i.name_zh IN ('蝦','豆腐') AND s.entry_kind='dish'
GROUP BY r.id ORDER BY COALESCE(r.home_style,0) DESC, hit DESC LIMIT 8
""")

# 某食材的性味宜忌
con.execute("""
SELECT r.id, r.title, src.title AS book, r.nature, r.flavor, r.gloss, r.text
FROM recipe r JOIN section s ON s.id=r.section_id JOIN source src ON src.id=s.source_id
WHERE s.entry_kind='food' AND (r.title LIKE '%蟹%' OR r.title_s LIKE '%蟹%')
ORDER BY (r.title LIKE '%蟹%') DESC LIMIT 8
""")

# 某道菜的原文 + 今译 + 食材
con.execute("""
SELECT r.id, r.title, src.title AS book, r.text, r.gloss, group_concat(i.name_zh,'、')
FROM recipe r JOIN section s ON s.id=r.section_id JOIN source src ON src.id=s.source_id
LEFT JOIN recipe_ingredient ri ON ri.recipe_id=r.id LEFT JOIN ingredient i ON i.id=ri.ingredient_id
WHERE r.title LIKE '%炒肉絲%' GROUP BY r.id
""")
```
