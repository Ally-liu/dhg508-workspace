#!/usr/bin/env python3
"""随园食单 app — 一个网页 + 这个小服务器 + 你的数据库 + 真 DeepSeek 调用。

    py code/server.py          然后打开 http://localhost:8000
    PORT=8765 py code/server.py

只用 Python 标准库。API key 放环境变量 DEEPSEEK_API_KEY，绝不写进文件/仓库。
没有 key 时自动退回"规则模式"，页面仍可演示（会标明）。
"""
import json
import os
import sqlite3
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "artifacts" / "suiyuan.db"
PORT = int(os.environ.get("PORT", 8000))
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip()
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
MED_DISCLAIMER = "以上为古籍（本草/食疗文献）记载，仅供参考，不构成医学建议，也不能代替医生的诊断与处方；如有身体不适或正在服药、怀孕、哺乳，请先咨询医生。"

SYSTEM = (
    "你是《随园食单》等八部古食书数据库的助手，重点在【古人的吃法与食物宜性】。"
    "你只能依据我给你的库中行回答，绝不使用你自己的美食/医药知识，"
    "绝不编造库中没有的菜、火候、用量或年代。引原文时照录繁体，不要改写。"
    "用简体中文叙述；涉及健康时提示这是古籍记载、非医疗建议。"
)


# --------------------------------------------------------------------------
# 数据库读取
# --------------------------------------------------------------------------
def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def vocab():
    con = db()
    names = [r["name_s"] or r["name_zh"] for r in
             con.execute("SELECT name_zh, name_s FROM ingredient")]
    sections = [r["name"] for r in con.execute("SELECT name FROM section WHERE kind='entry'")]
    con.close()
    return names, sections


# --------------------------------------------------------------------------
# DeepSeek 调用
# --------------------------------------------------------------------------
def deepseek(messages, json_mode=False):
    body = {"model": MODEL, "messages": messages, "temperature": 0.2}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def parse_question(q):
    """把自然语言问题拆成结构化查询。有 key 用 DeepSeek，否则用规则。"""
    names, sections = vocab()
    if API_KEY:
        prompt = (
            "只输出 JSON。字段：\n"
            '  intent: "by_ingredients" | "recipe" | "list_section" | "food" | "wellness" | "out_of_scope"\n'
            "  ingredients: 食材数组，只能取自我给的食材词表\n"
            "  dish: 菜名（intent=recipe 时）\n"
            "  section: 类目名，只能取自我给的类目表（intent=list_section 时）\n"
            "  food: 一个食材名（intent=food 时），只能取自我给的食材词表\n"
            "  kw: 一个检索词（intent=wellness 时），如 夏/冬/孕妇/酒/脾胃\n"
            f"\n食材词表：{('、'.join(names))}\n"
            f"类目表：{('、'.join(sections))}\n"
            "\n本库收八部古食书（《随园食单》《山家清供》《易牙遗意》《养小录》为菜谱；"
            "《饮食须知》《饮膳正要》《食疗本草》《养生随笔·粥谱》讲食性宜忌）。判定：\n"
            "· 用户报出自己有某些食材、问能做什么 → by_ingredients（把食材翻成词表里的繁体名）。\n"
            "· 用户问某道菜怎么做/是什么 → recipe。\n"
            "· 用户问某个类目里有什么 → list_section。\n"
            "· 用户问某食材的性味/宜忌/能不能吃/性质/寒热/养生（如'蟹的性味''猪肉有什么宜忌'"
            "'夏天该吃什么'）→ food，food 填该食材在词表里的名字（食物性味由食性书讲）。\n"
            "· 用户问**季节/体质/病候/食忌**（如'夏天该吃什么''孕妇有什么食忌''酒后忌什么''脾胃虚吃什么'）"
            "→ wellness，kw 填检索词（夏/娠/酒/脾胃）。\n"
            "· 只有确实和这八部书无关的问题才 → out_of_scope。**不要把库里有记载的食材判成 out_of_scope。**"
        )
        try:
            raw = deepseek(
                [{"role": "system", "content": SYSTEM},
                 {"role": "user", "content": prompt + "\n\n问题：" + q}],
                json_mode=True,
            )
            return json.loads(raw)
        except Exception as e:  # 网络/额度问题 -> 退回规则
            print("  [deepseek parse failed]", type(e).__name__)
    return parse_rules(q, names, sections)


def parse_rules(q, names, sections):
    hit_ing = [n for n in names if n in q]
    hit_sec = [s for s in sections if s in q]
    if hit_sec:
        return {"intent": "list_section", "section": hit_sec[0], "ingredients": []}
    if any(k in q for k in ("性味", "宜忌", "能不能吃", "性质", "能不能", "禁忌")):
        return {"intent": "food", "food": (hit_ing[0] if hit_ing else q.strip())}
    if hit_ing:
        return {"intent": "by_ingredients", "ingredients": hit_ing}
    return {"intent": "recipe", "dish": q.strip()}


# --------------------------------------------------------------------------
# 查询
# --------------------------------------------------------------------------
ING_SQL = """(SELECT group_concat(i2.name_zh, '、') FROM recipe_ingredient ri2
              JOIN ingredient i2 ON i2.id=ri2.ingredient_id WHERE ri2.recipe_id=r.id)"""
COLS = ("r.id, r.title, s.name AS section, src.title AS book, r.text, r.gloss, "
        "r.nature, r.flavor, r.food_category, r.home_style, " + ING_SQL + " AS ings")


def rows_by_ingredients(ings, limit=8):
    if not ings:
        return []
    ph = ",".join("?" for _ in ings)
    con = db()
    q = f"""
        SELECT {COLS}, COUNT(*) AS hit
        FROM recipe_ingredient ri
        JOIN ingredient i ON i.id=ri.ingredient_id
        JOIN recipe r ON r.id=ri.recipe_id
        JOIN section s ON s.id=r.section_id
        JOIN source src ON src.id=s.source_id
        WHERE (i.name_zh IN ({ph}) OR i.name_s IN ({ph}))
              AND s.entry_kind='dish' AND s.kind='entry'
        GROUP BY r.id
        ORDER BY COALESCE(r.home_style,0) DESC, hit DESC, r.id LIMIT ?
    """
    return [dict(x) for x in con.execute(q, (*ings, *ings, limit))]


def rows_recipe(dish, limit=6):
    con = db()
    q = f"""
        SELECT {COLS}
        FROM recipe r
        JOIN section s ON s.id=r.section_id
        JOIN source src ON src.id=s.source_id
        WHERE s.entry_kind='dish'
          AND (r.title LIKE ? OR r.title_s LIKE ? OR r.text LIKE ?)
        ORDER BY (r.title LIKE ? OR r.title_s LIKE ?) DESC,
                 COALESCE(r.home_style,0) DESC, r.id LIMIT ?
    """
    like = f"%{dish}%"
    return [dict(x) for x in con.execute(q, (like, like, like, like, like, limit))]


def rows_section(section, limit=200):
    con = db()
    q = f"""
        SELECT {COLS}
        FROM recipe r
        JOIN section s ON s.id=r.section_id
        JOIN source src ON src.id=s.source_id
        WHERE s.name = ? ORDER BY COALESCE(r.home_style,0) DESC, r.order_in_section LIMIT ?
    """
    return [dict(x) for x in con.execute(q, (section, limit))]


def rows_food(name, limit=8):
    """某食材的性味宜忌（食性书里的条目）。"""
    con = db()
    q = f"""
        SELECT {COLS}
        FROM recipe r
        JOIN section s ON s.id=r.section_id
        JOIN source src ON src.id=s.source_id
        WHERE s.entry_kind='food' AND (r.title LIKE ? OR r.title_s LIKE ? OR r.text LIKE ?)
        ORDER BY (r.title LIKE ? OR r.title_s LIKE ?) DESC, r.id LIMIT ?
    """
    like = f"%{name}%"
    return [dict(x) for x in con.execute(q, (like, like, like, like, like, limit))]


WELLNESS_SECTIONS = ("四時所宜", "食療諸病", "養生避忌", "姙娠食忌", "乳母食忌",
                     "飲酒避忌", "食物相反", "食物中毒", "食物利害", "服藥食忌", "五味偏走")


def rows_wellness(kw, limit=8):
    """按季节/体质/病候，在养生·食忌诸条里检索。"""
    if not kw:
        kw = "四時"
    con = db()
    ph = ",".join("?" for _ in WELLNESS_SECTIONS)
    q = f"""
        SELECT {COLS}
        FROM recipe r
        JOIN section s ON s.id=r.section_id
        JOIN source src ON src.id=s.source_id
        WHERE s.name IN ({ph})
          AND (r.title LIKE ? OR r.title_s LIKE ? OR r.text LIKE ? OR s.name LIKE ?)
        ORDER BY (r.title LIKE ? OR r.title_s LIKE ? OR s.name LIKE ?) DESC, r.id LIMIT ?
    """
    like = f"%{kw}%"
    return [dict(x) for x in con.execute(q, (*WELLNESS_SECTIONS, like, like, like, like,
                                             like, like, like, limit))]


def extract_kw(q):
    """从一句话里取一个检索关键词（季节/体质/病候）。"""
    rules = [("孕", "娠"), ("娠", "娠"), ("哺乳", "乳母"), ("乳母", "乳母"), ("产", "乳母"),
             ("祛湿", "濕"), ("濕", "濕"), ("湿", "濕"),
             ("酒", "酒"), ("醉", "酒"), ("春", "春"), ("夏", "夏"), ("秋", "秋"), ("冬", "冬"),
             ("脾胃", "脾胃"), ("肾", "肾"), ("腰", "腰"), ("咳", "咳"), ("目", "目"),
             ("虚", "虚"), ("渴", "渴"), ("气", "氣"), ("火", "火"), ("寒", "寒")]
    for k, v in rules:
        if k in q:
            return v
    if API_KEY:
        try:
            r = deepseek([{"role": "system", "content": "只输出一个检索关键词，不要标点。"},
                          {"role": "user",
                           "content": "从这句话取一个检索词（如 夏/冬/孕妇/酒/脾胃/虚劳），只输出词本身：" + q}],
                         json_mode=False)
            return r.strip().strip("。，,、 ")
        except Exception:
            pass
    return q.strip()


# --------------------------------------------------------------------------
# 组织回答
# --------------------------------------------------------------------------
def compose(question, parsed, rows):
    if not rows:
        return "本库未载。"
    if not API_KEY:
        return rule_answer(parsed, rows)
    payload = json.dumps(rows, ensure_ascii=False)
    prompt = (
        "下面是用户的问题，以及我从数据库查到的行（JSON）。只根据这些行回答，用简体中文，"
        "1–3 句，最后给出处 [id] 与书名/单名。\n"
        "· 若行是【菜谱】（有 text 做法）：优先讲那些 home_style=1 的【家常】做法；"
        "可摘一两句繁体原文。\n"
        "· 若行是【食性】（有 nature/flavor）：先报它的性（寒/凉/平/温/热）与味，"
        "再讲宜忌/主治，引用原文。\n"
        "· 若行是【养生/食忌】（季节、体质、病候、食物相反/中毒等）：照原文归纳该注意什么，引用原文。\n"
        "不得添加这些行以外的任何内容；食疗属古籍记载，涉及健康时提示非医疗建议。\n\n"
        f"问题：{question}\n\n查到的行：{payload}"
    )
    try:
        return deepseek([{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": prompt}]).strip()
    except Exception as e:
        print("  [deepseek compose failed]", type(e).__name__)
        return rule_answer(parsed, rows)


def rule_answer(parsed, rows):
    if parsed.get("intent") == "by_ingredients":
        top = rows[0]
        return (f"按你给的食材，库里命中最多的做法是《{top['title']}》"
                f"（{top['section']}）[id {top['id']}]。")
    if parsed.get("intent") == "list_section":
        return f"《{parsed.get('section','该单')}》共 {len(rows)} 条。"
    top = rows[0]
    return f"库里查到的《{top['title']}》（{top['section']}）[id {top['id']}]。"


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    def send(self, status, body, kind):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self.send(200, (HERE / "static" / "index.html").read_bytes(),
                             "text/html; charset=utf-8")
        if self.path == "/api/meta":
            con = db()
            sections = [dict(x) for x in con.execute(
                "SELECT s.name, src.title AS book, s.entry_kind FROM section s "
                "JOIN source src ON src.id=s.source_id WHERE s.kind='entry' ORDER BY s.id")]
            cnt = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                   for t in ("source", "section", "recipe", "ingredient", "recipe_ingredient")}
            con.close()
            return self.send(200, json.dumps(
                {"sections": sections, "counts": cnt, "model": MODEL,
                 "has_key": bool(API_KEY)}, ensure_ascii=False),
                "application/json; charset=utf-8")
        self.send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/ask":
            return self.send(404, "not found", "text/plain")
        n = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return self.send(400, json.dumps({"error": "bad json"}), "application/json")
        q = (payload.get("q") or "").strip()
        if payload.get("force") == "food" and q:
            p = parse_question(q)
            name = (p.get("food") or (p.get("ingredients") or [None])[0]
                    or p.get("dish") or q)
            parsed = {"intent": "food", "food": name}
        elif payload.get("force") == "wellness" and q:
            parsed = {"intent": "wellness", "kw": extract_kw(q)}
        else:
            parsed = parse_question(q) if q else {"intent": "out_of_scope"}
        intent = parsed.get("intent")
        if intent == "by_ingredients":
            rows = rows_by_ingredients(parsed.get("ingredients", []))
        elif intent == "list_section":
            rows = rows_section(parsed.get("section", ""))
        elif intent == "recipe":
            rows = rows_recipe(parsed.get("dish", ""))
        elif intent == "food":
            rows = rows_food(parsed.get("food", ""))
        elif intent == "wellness":
            rows = rows_wellness(parsed.get("kw", ""))
        else:
            rows = []
        answer = ("本库未载。" if (intent == "out_of_scope" or not rows)
                  else compose(q, parsed, rows))
        out = {"question": q, "parsed": parsed, "answer": answer,
               "rows": rows[:8], "model": MODEL, "mode": "deepseek" if API_KEY else "rules",
               "disclaimer": (MED_DISCLAIMER if (intent in ("food", "wellness") and rows) else None)}
        self.send(200, json.dumps(out, ensure_ascii=False),
                  "application/json; charset=utf-8")

    def log_message(self, fmt, *args):
        try:
            print("  " + (fmt % args).encode("ascii", "replace").decode("ascii"))
        except Exception:
            pass


if __name__ == "__main__":
    if not DB.is_file():
        print(f"database missing: {DB}\nrun: py code/build_db.py")
        raise SystemExit(1)
    if not API_KEY:
        print("DEEPSEEK_API_KEY not set — running in rules-only mode.")
    print(f"Open http://localhost:{PORT}   (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
