# reference/schema.md — 库结构

**先用现成脚本**：`py code/ask.py "<地名>"` → 结果写入 `artifacts/last_query.txt`，用
Read 工具读它（别读控制台）。下面才是手写 SQL 的说明，按需再看。

文件：`artifacts/maps.db`（SQLite，8 张表）。用 Python `sqlite3` 直读。

```
source(id) ──source_id──> 每一张表
city(id) ──city_id──> map(id)
                    └─> place(id)
place_type(code) ──type_code──> place(id)
place(id) ──place_id──> place_name(id)          (一个地方的多个写法/异名)
map_place(map_id, place_id)                      (某地名出现在某张图上，多对多)
```

| 表 | 一行是 | 常用字段 |
|---|---|---|
| `city` | 一座城市 | `name_zh` 今名, `name_en`, `province` |
| `map` | 一张老地图 | `title` 图名, `map_year` 年份, `city_id`, `image_file` 原图路径, `min_lat/max_lat/min_lon/max_lon` 覆盖范围（**香港已填**） |
| `place` | 一个地名 | `name_zh` **图上古名**, `name_en`, `place_type` 自由文本, `type_code` **规范类型**, `modern_name` **今名**, `modern_flag`(=1 表示今名是"对照"), `lat/lon` 现代坐标（**香港已填**，对照近似）, `note` |
| `place_type` | 一个类型码 | `code`, `name_zh`, `category`（大类：城建/区域/建筑/宗教/自然/水系/交通） |
| `place_name` | 一个地名的一种写法 | `place_id`, `form`(zh/roman/variant), `name` |
| `map_place` | "某地名在某图上" | `map_id`, `place_id`, `label_on_map` |
| `profile` | 一个地名的**编者补充** | `place_id`, `rename_year` 改名年, `rename_reason` 改名原因, `blurb` 小百科, `source_id`（二手资料） |
| `source` | 一处出处 | `title`, `year`, `archive`, `url`, `license` |

## 关键理解

- **"现代名 → 古名"**：用输入的现代名去匹配 `place.modern_name`
  **或** `place.name_zh`（古今同名）。**现在 291 个地名都填了 `modern_name`**：
  - 改名过的：`modern_name` = 今名，`modern_flag = 1`（**对照，非原件**）。
  - 未改名的：`modern_name` = 本身，`modern_flag = 0`。
- **"古名 → 位置"**：有两层——"在哪张图"（`map_place` → `map`）和"**今天在哪**"
  （`place.lat/lon`，**现代坐标、对照、近似**）。坐标目前**只填了香港 65 个点**，
  其余城市未填。被问坐标：有就给并标"（对照，近似）"，没有就答"本库未载坐标"。
  （坐标来源记作 `source 7`，非老地图原件内容。）
- **按类筛选**：用 `place.type_code` 连 `place_type.category`，可做规范分类
  （如"所有水系""所有宗教建筑"）。`place.place_type` 是早期自由文本，仅作参考。

## 查询示例（Python）

```python
import sqlite3
con = sqlite3.connect("artifacts/maps.db")

# 现代名 → 古名 + 所在图
q = """
SELECT c.name_zh AS city, p.name_zh AS old_name, p.name_en,
       pt.name_zh AS type, p.modern_name, p.modern_flag,
       m.title AS map, m.map_year, p.id
FROM place p
JOIN city c        ON p.city_id = c.id
LEFT JOIN place_type pt ON p.type_code = pt.code
JOIN map_place mp  ON mp.place_id = p.id
JOIN map m         ON m.id = mp.map_id
WHERE p.modern_name LIKE ? OR p.name_zh LIKE ?
"""
rows = list(con.execute(q, ("%前门%", "%前门%")))
# 每行附 [id] 与地图名；modern_flag=1 时注明"（对照）"；无结果答"本库未载，我不知道。"
```

```python
# 某城某大类的地名
con.execute("""
SELECT p.name_zh, pt.name_zh, p.id
FROM place p JOIN city c ON p.city_id=c.id
JOIN place_type pt ON p.type_code=pt.code
WHERE c.name_zh='广州' AND pt.category='水系'
""")
```
