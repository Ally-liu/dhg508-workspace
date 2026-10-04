#!/usr/bin/env python3
"""Fill *_s simplified-Chinese fields (for robust name matching) via DeepSeek.

Usage:
    py code/make_simplified.py     # needs DEEPSEEK_API_KEY
    py code/build_db.py

Adds:
  recipe.title_s       simplified of recipe.title
  ingredient.name_s    simplified of ingredient.name_zh

These exist ONLY to make matching tolerant: the user types simplified, the
book is traditional. The original text (title/text/name_zh) is untouched and
stays the authority. Resumable: re-run fills only what is still empty.
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

SYSTEM = (
    "你是简繁转换器。把我给你的每一行繁体中文转成简体中文，一字不改别的内容，"
    "保持原有顺序和标点。只输出转换后的行，每行一条，不要编号，不要解释。"
)


def convert(items):
    """items: list[str] traditional -> list[str] simplified (same length)."""
    user = "\n".join(items)
    body = {"model": MODEL, "temperature": 0,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": user}]}
    req = urllib.request.Request(
        API_URL, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode("utf-8"))
    out = d["choices"][0]["message"]["content"].strip().split("\n")
    out = [re.sub(r"^\s*\d+[\.、\)]\s*", "", x).strip() for x in out]
    if len(out) != len(items):
        raise ValueError(f"length mismatch {len(out)} != {len(items)}")
    return out


def fill(rows, src_key, dst_key):
    todo = [(i, r) for i, r in enumerate(rows) if not r.get(dst_key)]
    print(f"  {dst_key}: {len(todo)} to fill of {len(rows)}")
    B = 40
    done = 0
    for s in range(0, len(todo), B):
        chunk = todo[s:s + B]
        try:
            conv = convert([r[src_key] for _, r in chunk])
            for (_, r), v in zip(chunk, conv):
                r[dst_key] = v
            done += len(chunk)
        except Exception as e:
            print(f"    batch {s} failed: {type(e).__name__} {e}")
        time.sleep(0.3)
    return done


def main():
    if not API_KEY:
        print("DEEPSEEK_API_KEY not set. Aborting."); sys.exit(1)
    data = json.loads(RECORDS.read_text(encoding="utf-8"))
    fill(data["recipes"], "title", "title_s")
    fill(data["ingredients"], "name_zh", "name_s")
    RECORDS.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
