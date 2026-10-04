#!/usr/bin/env python3
"""Fill recipe.gloss (one-line simplified 今译) for dish entries via DeepSeek.

Usage:
    py code/make_glosses.py     # needs DEEPSEEK_API_KEY
    py code/build_db.py

Only dish entries are handled here; food entries get their note from
make_food.py. Batched (15 per call). Resumable.
"""
import json
import os
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
B = 15

SYSTEM = (
    "你是古籍食谱的注解者。对每一条，只根据我给的原文写一句简体中文今译："
    "先概述做法，若有明确用量或火候就带上，不确定就略过，绝不编造。"
    "不要书名号，不要称'这道菜'，每条不超过60字。只输出 JSON 数组。"
)


def call(items):
    lines = [f"{i}. {t}：{x[:260]}" for i, (t, x) in enumerate(items, 1)]
    user = ("逐条写今译，输出 JSON 数组，每项形如 {\"gloss\":\"...\"}，顺序一致：\n\n"
            + "\n".join(lines))
    body = {"model": MODEL, "temperature": 0.3, "response_format": {"type": "json_object"},
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": user + "\n\n只输出 {\"items\":[{\"gloss\":\"...\"}]}"}]}
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
            if secs[r["section_id"]]["entry_kind"] == "dish" and not r.get("gloss")]
    print(f"dish entries to gloss: {len(todo)}")
    done = 0
    for s in range(0, len(todo), B):
        chunk = todo[s:s + B]
        try:
            res = call([(r["title"], r["text"]) for r in chunk])
            for r, v in zip(chunk, res):
                g = (v.get("gloss") or "").strip()
                if g:
                    r["gloss"] = g
            done += len(chunk)
        except Exception as e:
            print(f"  batch {s} failed: {type(e).__name__} {e}")
        if (s // B) % 10 == 0:
            RECORDS.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  ... {done}/{len(todo)}")
        time.sleep(0.2)
    RECORDS.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"done. glossed={done}")


if __name__ == "__main__":
    main()
