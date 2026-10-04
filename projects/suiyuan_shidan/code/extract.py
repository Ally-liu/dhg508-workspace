#!/usr/bin/env python3
"""Extract the cookbook + food-property corpus into records.json.

Usage:
    py code/extract.py

Reads raw wikitext from sources/raw/ and writes sources/processed/records.json.
Each book lists its files; each file can say whether its entries are
  dish  (a recipe)  |  food (a food's nature/properties/宜忌)  |  rule (通则/戒律)
Parsing is "flat": every heading with text directly under it becomes an entry;
its section is the nearest shallower heading, or the file's topic.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "sources" / "raw"
OUT = ROOT / "sources" / "processed" / "records.json"

PD = "Public Domain"

BOOKS = [
    {
        "id": 1, "title": "隨園食單", "author": "袁枚（字子才）", "year": 1792,
        "kind": "recipe_book",
        "edition": "清乾隆五十七年（1792）初刻；本文据维基文库整理本",
        "url": "https://zh.wikisource.org/wiki/隨園食單", "license": PD,
        "note": "本库主要菜谱底本。第一節–第五節；第六節为重复孤儿，未采。",
        "default_entry_kind": "dish",
        "rule_sections": ["隨園食單序", "須知單", "戒單"],
        "files": [{"path": f"wikisource/part{i}.txt", "topic": None} for i in range(1, 6)],
    },
    {
        "id": 2, "title": "山家清供", "author": "林洪（南宋）", "year": None,
        "kind": "recipe_book",
        "edition": "南宋食谱，本文据维基文库整理本（取自景明刻本《夷门广牍》）",
        "url": "https://zh.wikisource.org/wiki/山家清供", "license": PD,
        "note": "南宋文人清雅食谱。",
        "default_entry_kind": "dish",
        "rule_sections": ["山家清供序"],
        "files": [{"path": "wikisource/shanjiaqinggong.txt", "topic": None}],
    },
    {
        "id": 3, "title": "飲食須知", "author": "賈銘（元）", "year": None,
        "kind": "food_property",
        "edition": "元人饮食宜忌，本文据维基文库整理本",
        "url": "https://zh.wikisource.org/wiki/飲食須知", "license": PD,
        "note": "按水、火、谷、菜、果、味、鱼、禽、兽等类，逐条记食材性味宜忌。",
        "default_entry_kind": "food",
        "rule_sections": ["飲食須知序"],
        "files": [{"path": "wikisource/yinshixuzhi_main.txt", "topic": None},
                  {"path": "wikisource/yinshixuzhi_00xu.txt", "topic": None}]
                 + [{"path": f"wikisource/yinshixuzhi_{i:02d}.txt", "topic": None} for i in range(1, 9)],
    },
    {
        "id": 4, "title": "飲膳正要", "author": "忽思慧（元）", "year": 1330,
        "kind": "food_property",
        "edition": "元太医院饮膳太医官书，本文据维基文库整理本",
        "url": "https://zh.wikisource.org/wiki/飲膳正要", "license": PD,
        "note": "重点食性书：品物性味、食疗诸病、食物相反/中毒/利害、四时所宜。",
        "default_entry_kind": "food",
        "rule_sections": [],
        "files": [
            {"path": "books/yinshanzhengyao/01.txt", "topic": "三皇聖紀", "entry_kind": "rule"},
            {"path": "books/yinshanzhengyao/02.txt", "topic": "養生避忌", "entry_kind": "rule"},
            {"path": "books/yinshanzhengyao/03.txt", "topic": "姙娠食忌", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/04.txt", "topic": "乳母食忌", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/05.txt", "topic": "飲酒避忌", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/06.txt", "topic": "聚珍異饌", "entry_kind": "dish"},
            {"path": "books/yinshanzhengyao/07.txt", "topic": "諸般湯煎", "entry_kind": "dish"},
            {"path": "books/yinshanzhengyao/08.txt", "topic": "諸水", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/09.txt", "topic": "神仙服餌", "entry_kind": "rule"},
            {"path": "books/yinshanzhengyao/10.txt", "topic": "四時所宜", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/11.txt", "topic": "五味偏走", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/12.txt", "topic": "食療諸病", "entry_kind": "dish"},
            {"path": "books/yinshanzhengyao/13.txt", "topic": "服藥食忌", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/14.txt", "topic": "食物利害", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/15.txt", "topic": "食物相反", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/16.txt", "topic": "食物中毒", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/17.txt", "topic": "禽獸變異", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/18.txt", "topic": "米穀品", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/19.txt", "topic": "獸品", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/20.txt", "topic": "禽品", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/21.txt", "topic": "魚品", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/22.txt", "topic": "菓品", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/23.txt", "topic": "菜品", "entry_kind": "food"},
            {"path": "books/yinshanzhengyao/24.txt", "topic": "料物", "entry_kind": "food"},
        ],
    },
    {
        "id": 5, "title": "食療本草", "author": "孟詵（唐）", "year": None,
        "kind": "food_property",
        "edition": "唐食疗专著，本文据维基文库整理本",
        "url": "https://zh.wikisource.org/wiki/食療本草", "license": PD,
        "note": "逐味食物标性味（寒/温/平/热）与宜忌，两百余种。",
        "default_entry_kind": "food",
        "rule_sections": [],
        "files": [{"path": "books/shiliaobencao/01.txt", "topic": None}],
    },
    {
        "id": 6, "title": "養生隨筆·粥譜", "author": "曹庭棟（清）", "year": 1773,
        "kind": "food_property",
        "edition": "又名《老老恒言》，本文据维基文库整理本（仅取卷五粥谱）",
        "url": "https://zh.wikisource.org/wiki/養生隨筆", "license": PD,
        "note": "清代养生粥谱：上品三十六、中品二十七、下品三十七。",
        "default_entry_kind": "food",
        "rule_sections": ["粥譜說"],
        "files": [{"path": "books/yangshengsuibi/05.txt", "topic": "粥譜"}],
    },
    {
        "id": 7, "title": "易牙遺意", "author": "韓奕（元末明初）", "year": None,
        "kind": "recipe_book",
        "edition": "元末明初家厨书，本文据维基文库整理本",
        "url": "https://zh.wikisource.org/wiki/易牙遺意", "license": PD,
        "note": "家常做法的集子：醞造、脯鮓、籠造、爐造、糕餌、湯餅、齋食、果實、諸湯茶。",
        "default_entry_kind": "dish",
        "rule_sections": ["敘"],
        "files": [{"path": "books/yiyayiyi/01.txt", "topic": None}],
    },
    {
        "id": 8, "title": "養小錄", "author": "顧仲（清）", "year": None,
        "kind": "recipe_book",
        "edition": "清初饮馔书，本文据维基文库整理本",
        "url": "https://zh.wikisource.org/wiki/養小錄", "license": PD,
        "note": "极家常：饮、酱、饵、蔬——醃菜、糟、豆腐、麵筋、粥、笋、茄、瓜。",
        "default_entry_kind": "dish",
        "rule_sections": ["養小錄序"],
        "files": [{"path": "books/yangxiaolu/01.txt", "topic": None}],
    },
]

# 正文中的模板/链接只保留可读文字
INLINE_TEMPLATES = [
    (re.compile(r"\{\{ProperNoun\|([^{}]*)\}\}"), r"\1"),
    (re.compile(r"\{\{YL\|([^{}]*)\}\}"), r"\1"),
    (re.compile(r"\{\{!\}\}"), "|"),
    (re.compile(r"\{\{[^{}]*\}\}"), ""),
    (re.compile(r"\[\[[^\[\]|]*\|([^\[\]]*)\]\]"), r"\1"),
    (re.compile(r"\[\[([^\[\]]*)\]\]"), r"\1"),
    (re.compile(r"'{2,}"), ""),
]

# 家常判定：含下列珍馐词或在下列"非家常"单里，就不算家常
LUXURY = ["海參", "魚翅", "鮑魚", "燕窩", "熊掌", "鹿筋", "鹿尾", "鹿肉", "果子狸", "果子貍",
          "象鼻", "鰣魚", "鱘魚", "魚肚", "魚唇", "魚骨", "魚白", "犀", "駝峰", "猩唇", "猴",
          "虎", "豹", "麋", "獐", "貛", "獾", "鱘", "鰩", "鮠", "河豚"]
NON_HOME_SECTIONS = {"海鮮單", "聚珍異饌"}
# 这些标题一律当作"通则/序跋"，不是菜也不是食材
GENERIC_RULES = {"序", "敘", "叙", "跋", "目録", "目录", "凡例", "緣起", "小引", "自序", "原序"}

# ---------------------------------------------------------------------------
INGREDIENTS = {
    "畜肉": ["豬肉", "豬蹄", "豬爪", "豬腦", "豬肝", "豬肺", "豬肚", "豬腰", "腰子", "豬油",
             "火腿", "家鄉肉", "風肉", "醃肉", "臘肉", "肉", "豬",
             "牛肉", "牛", "羊肉", "羊", "鹿肉", "鹿筋", "鹿尾", "鹿", "兔肉", "兔",
             "狗肉", "獐", "獾", "貛", "熊掌", "象鼻", "果子狸", "果子貍"],
    "禽蛋": ["雞", "雞脯", "雞片", "雞汁", "雞皮", "雞腎", "鴨", "鵝", "鴿", "鶉", "雉", "麻雀",
             "野雞", "雞蛋", "鴨蛋", "蛋", "燕窩"],
    "水產": ["海參", "魚翅", "鮑魚", "魚肚", "魚骨", "魷魚", "鮮魚", "鰻", "鰻魚", "鱉", "甲魚",
             "鱔", "鱔魚", "鯽魚", "鯉魚", "青魚", "鯶魚", "鯿魚", "鱸魚", "鱖魚", "鰣魚", "刀魚",
             "刀鱭", "鯧魚", "帶魚", "烏魚", "白魚", "黃魚", "鰱魚", "草魚", "鯰魚", "泥鰍",
             "河豚", "斑魚", "鱘魚", "鯊魚", "魚鬆", "魚圓", "魚肉", "魚", "鯗",
             "蝦米", "蝦子", "蝦", "蟹粉", "蟹肉", "蟹", "蟶", "蛤", "蜆", "蚶", "螺", "蠔",
             "牡蠣", "干貝", "江珧", "瑤柱", "淡菜", "海蜇", "海菜", "紫菜", "魚唇", "烏賊"],
    "蔬菜": ["冬筍", "春筍", "鮮筍", "鞭筍", "筍乾", "筍脯", "筍油", "筍", "香蕈", "冬菇", "蘑菇",
             "松菌", "菌", "蕈", "木耳", "銀耳", "冬瓜", "黃瓜", "王瓜", "南瓜", "絲瓜", "苦瓜",
             "茭白", "菱白", "白菜", "青菜", "芥菜", "菠菜", "莧菜", "薺菜", "芹菜", "芹",
             "韭", "韭菜", "豆芽", "豆苗", "扁豆", "豇豆", "萵筍", "萵苣", "香椿", "馬蘭", "枸杞",
             "菊", "百合", "荷", "蓮子", "藕", "荸薺", "菱", "芋艿", "芋", "山藥", "蘿蔔",
             "胡蘿蔔", "茄", "辣椒", "瓠", "葫蘆", "蒪菜", "蓴菜", "海帶", "冬菜", "醃菜", "酸菜"],
    "豆麵": ["豆腐", "豆皮", "腐皮", "豆乾", "香乾", "麵筋", "豆", "豆粉", "芡粉", "米粉", "麵粉",
             "麵", "米", "糯米", "飯", "粥", "麥", "薏", "蕎麥"],
    "點心": ["年糕", "饅頭", "餃", "餛飩", "粽子", "月餅", "豆沙", "麵茶", "粽"],
    "乾果": ["紅棗", "棗", "栗子", "栗", "核桃", "杏仁", "松仁", "瓜子", "花生", "蓮子", "芝麻",
             "桂圓", "荔枝", "龍眼"],
    "水果": ["橘", "橙", "梨", "蘋果", "柿", "楊梅", "梅", "桃", "杏", "櫻桃", "橄欖", "甘蔗",
             "西瓜", "荸薺"],
    "調味": ["醬油", "清醬", "秋油", "伏醬", "甜醬", "麵醬", "豆豉", "醬瓜", "醬", "米醋", "醋",
             "酒釀", "料酒", "紹興酒", "惠泉酒", "酒", "冰糖", "白糖", "紅糖", "糖", "香油",
             "麻油", "菜油", "豆油", "油", "鹽水", "鹽", "蔥", "薑", "蒜", "辣", "椒鹽", "八角",
             "花椒", "胡椒", "椒", "桂", "肉桂", "茴香", "大茴", "陳皮", "砂仁", "甘草",
             "芫荽", "芥末", "芥", "糟", "五味", "茶"],
    "乳酪": ["牛乳", "牛奶", "乳酪", "酥油", "奶", "乳", "酥"],
    "補藥": ["人參", "當歸", "黃耆", "茯苓", "天麻", "蟲草", "阿膠", "枸杞"],
}
CATEGORY_OF = {term: cat for cat, terms in INGREDIENTS.items() for term in terms}
SORTED_TERMS = sorted(CATEGORY_OF, key=len, reverse=True)


def strip_markup(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    for pat, repl in INLINE_TEMPLATES:
        text = pat.sub(repl, text)
    return text


def drop_leading_templates(text: str) -> str:
    out = text.lstrip()
    while out.startswith("{{"):
        depth, i = 0, 0
        while i < len(out):
            if out[i:i + 2] == "{{":
                depth += 1; i += 2; continue
            if out[i:i + 2] == "}}":
                depth -= 1; i += 2
                if depth == 0:
                    break
                continue
            i += 1
        out = out[i:].lstrip()
    return out


def match_ingredients(text: str):
    found, used = [], [False] * len(text)
    for term in SORTED_TERMS:
        start = 0
        while True:
            j = text.find(term, start)
            if j < 0:
                break
            if not any(used[j:j + len(term)]):
                for k in range(j, j + len(term)):
                    used[k] = True
                found.append((j, term))
            start = j + len(term)
    found.sort()
    return found


def parse_file(path: Path, topic, default_kind, rule_sections):
    """Flat parse: heading-with-text = entry; section = nearest shallower heading."""
    raw = drop_leading_templates(strip_markup(path.read_text(encoding="utf-8")))
    entries = []          # (section_name, entry_kind, title, text)
    stack = []            # (level, title)
    cur = None            # current entry dict
    for line in raw.splitlines():
        hm = re.match(r"^(=+)\s*(.*?)\s*=+\s*$", line)
        if hm:
            level = len(hm.group(1))
            title = hm.group(2).strip().strip("'")
            while stack and stack[-1][0] >= level:
                stack.pop()
            group = stack[-1][1] if stack else (topic or "(無單)")
            is_rule = title in rule_sections or group in rule_sections or title in GENERIC_RULES
            kind = "rule" if is_rule else default_kind
            cur = {"section": group, "kind": kind, "title": title, "text": ""}
            entries.append(cur)
            stack.append((level, title))
            continue
        if line.strip():
            if cur is None:
                # 正文出现在任何标题之前：用文件主题建一个条目（有些食忌页没有小标题）
                cur = {"section": topic or "(無單)",
                       "kind": ("rule" if (topic in rule_sections) else default_kind),
                       "title": topic or "(正文)", "text": ""}
                entries.append(cur)
            cur["text"] += line.strip() + " "
    # drop empty
    return [e for e in entries if re.sub(r"\s+", "", e["text"])]


def is_home(title, text, section):
    if section in NON_HOME_SECTIONS:
        return 0
    blob = title + text
    return 0 if any(t in blob for t in LUXURY) else 1


def main() -> None:
    sources, sections, recipes, recipe_ings = [], [], [], []
    ing_index = {}
    sec_id, rid = 0, 0
    sec_by_name = {}

    # 保留上一版 records.json 里的标注（重跑不必重新调用 DeepSeek）
    old = {}
    old_ing = {}
    if OUT.is_file():
        try:
            prev = json.loads(OUT.read_text(encoding="utf-8"))
            osecs = {s["id"]: s for s in prev.get("sections", [])}
            for r in prev.get("recipes", []):
                s = osecs.get(r["section_id"])
                if s:
                    old[(s["source_id"], r["title"])] = r
            old_ing = {i["name_zh"]: i.get("name_s") for i in prev.get("ingredients", [])}
        except Exception:
            old = {}
            old_ing = {}

    for book in BOOKS:
        sources.append({"id": book["id"], "title": book["title"], "author": book["author"],
                        "year": book["year"], "edition": book["edition"], "url": book["url"],
                        "license": book["license"], "note": book["note"], "kind": book["kind"]})
        rule_set = set(book.get("rule_sections", []))
        default_kind = book["default_entry_kind"]
        for fi, f in enumerate(book["files"], 1):
            path = RAW / f["path"]
            if not path.is_file():
                continue
            kind = f.get("entry_kind", default_kind)
            for e in parse_file(path, f.get("topic"), kind, rule_set):
                secname = e["section"]
                key = (book["id"], secname)
                if key not in sec_by_name:
                    sec_id += 1
                    sec_by_name[key] = sec_id
                    sections.append({"id": sec_id, "source_id": book["id"], "part": fi,
                                     "name": secname,
                                     "kind": "rule" if e["kind"] == "rule" else "entry",
                                     "entry_kind": e["kind"] if e["kind"] != "rule" else "rule",
                                     "order": sec_id})
                sid = sec_by_name[key]
                text = re.sub(r"\s+", " ", e["text"]).strip()
                rid += 1
                home = is_home(e["title"], text, secname) if e["kind"] == "dish" else None
                o = old.get((book["id"], e["title"]), {})
                recipes.append({"id": rid, "section_id": sid, "title": e["title"],
                                "title_s": o.get("title_s"), "text": text,
                                "gloss": o.get("gloss"), "nature": o.get("nature"),
                                "flavor": o.get("flavor"),
                                "food_category": o.get("food_category"),
                                "home_style": home, "order_in_section": 0})
                seen = set()
                for _, term in match_ingredients(e["title"] + " " + text):
                    if term in seen:
                        continue
                    seen.add(term)
                    if term not in ing_index:
                        ing_index[term] = len(ing_index) + 1
                    recipe_ings.append({"recipe_id": rid, "ingredient_id": ing_index[term],
                                        "term": term, "category": CATEGORY_OF[term]})

    ingredients = [{"id": iid, "name_zh": t, "name_s": old_ing.get(t), "category": CATEGORY_OF[t]}
                   for t, iid in sorted(ing_index.items(), key=lambda kv: kv[1])]

    data = {"sources": sources, "sections": sections, "recipes": recipes,
            "ingredients": ingredients, "recipe_ingredients": recipe_ings}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"wrote {OUT}")
    print(f"sources={len(sources)} sections={len(sections)} recipes={len(recipes)} "
          f"ingredients={len(ingredients)} recipe_ingredients={len(recipe_ings)}")
    from collections import Counter
    for b in sources:
        n = sum(1 for s in sections if s["source_id"] == b["id"])
        print(f"  book {b['id']} {b['title']}: {n} sections")
    c = Counter(s["entry_kind"] for s in sections)
    print("  entry_kind:", dict(c))


if __name__ == "__main__":
    main()
