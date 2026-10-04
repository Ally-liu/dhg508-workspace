# 来源说明 — source note

本库收录**八部公版古食书**，数字文本均取自 **維基文庫（Wikisource）**。
作者均逝世逾百年、作品出版逾百年，**公有领域**。

## 菜谱（recipe_book）

### 1. 《隨園食單》 · 袁枚 · 清（1792）
- https://zh.wikisource.org/wiki/隨園食單
- `sources/raw/wikisource/part1..5.txt`（第一節–第五節；第六節为重复孤儿，未采）。

### 2. 《山家清供》 · 林洪 · 南宋
- https://zh.wikisource.org/wiki/山家清供
- `sources/raw/wikisource/shanjiaqinggong.txt`。

### 3. 《易牙遺意》 · 韓奕 · 元末明初
- https://zh.wikisource.org/wiki/易牙遺意
- `sources/raw/books/yiyayiyi/01.txt`。家常做法：醞造、脯鮓、籠造、爐造、糕餌、湯餅、齋食、果實、諸湯茶。

### 4. 《養小錄》 · 顧仲 · 清
- https://zh.wikisource.org/wiki/養小錄
- `sources/raw/books/yangxiaolu/01.txt`。极家常：飲、醬、餌、蔬——醃菜、糟、豆腐、麵筋、粥、筍、茄、瓜。

## 食性（food_property）

### 5. 《飲食須知》 · 賈銘 · 元
- https://zh.wikisource.org/wiki/飲食須知
- `sources/raw/wikisource/yinshixuzhi_*.txt`（主页 + 序 + 卷1–8）。
- 按水、火、谷、菜、果、味、鱼、禽、兽等类，逐条记食材性味宜忌。

### 6. 《飲膳正要》 · 忽思慧 · 元（1330）
- https://zh.wikisource.org/wiki/飲膳正要
- `sources/raw/books/yinshanzhengyao/01..24.txt`（三皇聖紀、養生避忌、食療諸病、
  食物相反、食物中毒、食物利害、服藥食忌、四時所宜、五味偏走、米穀品、獸品、
  禽品、魚品、菓品、菜品、料物 …）。
- 元太医院官书，食性重点：品物性味 + 食疗 + 食忌。

### 7. 《食療本草》 · 孟詵 · 唐
- https://zh.wikisource.org/wiki/食療本草
- `sources/raw/books/shiliaobencao/01.txt`。逐味食物标〈寒/温/平/热〉与宜忌，两百余种。

### 8. 《養生隨筆·粥譜》 · 曹庭棟 · 清（1773）
- https://zh.wikisource.org/wiki/養生隨筆（又名《老老恆言》）
- `sources/raw/books/yangshengsuibi/05.txt`（仅取卷五粥谱：上品三十六、中品二十七、下品三十七）。

## 若日后想加料

- 同书别版、或《隨息居飲食譜》（王士雄·清，食性名著；维基文库暂缺，可另寻 ctext / Internet Archive）。
- 沿用同一条流水线：`extract.py → make_simplified → make_food → make_glosses → build_db.py`。
