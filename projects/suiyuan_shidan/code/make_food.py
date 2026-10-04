#!/usr/bin/env python3
"""Annotate food entries with 性/味/类/宜忌 via DeepSeek (batched).

Usage:
    py code/make_food.py       # needs DEEPSEEK_API_KEY
    py code/build_db.py

For every entry whose section is a "food" section, ask DeepSeek to read the
original text and return, per entry:
    nature   one of 寒/凉/平/温/热/无   (微寒->寒, 微温->温, 大热->热)
    flavor   subset of 酸/苦/甘/辛/咸/淡/涩 joined by 、 (or 无)
    category one of 水/火/谷/菜/果/味/鱼/禽/兽/乳/药/其他
    note     one short Chinese line (<=40 字): 宜忌/主治
Marked as 编者补充 in the app. Resumable: fills only entries still empty.
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "sources" / "processed" / "records.json"
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip()
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
B = 20

SYSTEM = (
    "你是本草/食疗文献的结构化助手。只依据我给的原句提取，不臆造。只输出 JSON 数组。"
    "nature 只能取 寒/凉/平/温/热/无 之一；flavor 取 酸/苦/甘/辛/咸/淡/涩 的若干（用、连接），无则填 无；"
    "category 取 水/火/谷/菜/果/味/鱼/禽/兽/乳/药/其他 之一；"
    "note 用一句不超过40字的中文写它的宜忌或主治（没有就写 无）。"
)


def call(items):
    lines = []
    for i, (t, x) in enumerate(items, 1):
        lines.append(f"{i}. 名：{t}\n   文：{x[:220]}")
    user = ("逐条提取，输出 JSON 数组，每项形如 "
            '{"nature":"...","flavor":"...","category":"...","note":"..."}，顺序与下面一致：\n\n'
            + "\n".join(lines))
    body = {"model": MODEL, "temperature": 0, "response_format": {"type": "json_object"},
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": user + "\n\n只输出 {\"items\":[...]}"}]}
    req = urllib.request.Request(
        API_URL, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode("utf-8"))
    out = json.loads(d["choices"][0]["message"]["content"])["items"]
    if len(out) != len(items):
        raise ValueError("len mismatch")
    return out


def main():
    if not API_KEY:
        print("DEEPSEEK_API_KEY not set. Aborting."); sys.exit(1)
    data = json.loads(RECORDS.read_text(encoding="utf-8"))
    secs = {s["id"]: s for s in data["sections"]}
    todo = [r for r in data["recipes"]
            if secs[r["section_id"]]["entry_kind"] == "food" and not r.get("food_category")]
    print(f"food entries to annotate: {len(todo)}")
    done = 0
    for s in range(0, len(todo), B):
        chunk = todo[s:s + B]
        try:
            res = call([(r["title"], r["text"]) for r in chunk])
            for r, v in zip(chunk, res):
                r["nature"] = (v.get("nature") or "无").strip()
                r["flavor"] = (v.get("flavor") or "无").strip()
                r["food_category"] = (v.get("category") or "其他").strip()
                r["gloss"] = (v.get("note") or "").strip() or None
            done += len(chunk)
        except Exception as e:
            print(f"  batch {s} failed: {type(e).__name__} {e}")
        if (s // B) % 5 == 0:
            RECORDS.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  ... {done}/{len(todo)}")
        time.sleep(0.2)
    RECORDS.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"done. annotated={done}")


if __name__ == "__main__":
    main()
