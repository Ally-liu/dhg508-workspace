# server.py — 光绪之死：证据审讯室
# stdlib only. Run from project dir:  py code/server.py  → http://localhost:8000
# Cost discipline: ONE DeepSeek call per ask (max_tokens 420), rows shipped once,
# every request logged to artifacts/ask_log.jsonl, no key → rule-mode replay.
import json
import sqlite3
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "artifacts" / "guangxu.db"
STATIC = ROOT / "code" / "static"
LOG = ROOT / "artifacts" / "ask_log.jsonl"

KEY = None
try:
    KEY = __import__("os").environ.get("DEEPSEEK_API_KEY")
except Exception:
    KEY = None

CHOICES = ["慈禧授意", "袁世凯进药", "李莲英近侍", "久病自然亡", "我有新想法"]


def rows_all():
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        src = {r["id"]: dict(r) for r in c.execute("SELECT * FROM source")}
        out = [dict(r) for r in c.execute("SELECT * FROM evidence ORDER BY date_iso, id")]
        pairs = {}
        for r in c.execute("SELECT * FROM contradiction"):
            pairs.setdefault(r["pair"], {"topic": r["topic"], "members": []})["members"].append(r["member"])
        return src, out, pairs


def verdict_stats():
    with sqlite3.connect(DB) as c:
        total = c.execute("SELECT COUNT(*) FROM verdict").fetchone()[0]
        dist = c.execute("SELECT choice, COUNT(*) n FROM verdict GROUP BY choice ORDER BY n DESC").fetchall()
        return total, [(d[0], d[1]) for d in dist]


def rule_interrogation(claim, pairs, ev_by_id):
    parts = ["【规则模式】（未用模型，基于固定题库）"]
    hit = []
    for pid, p in pairs.items():
        for m in p["members"]:
            if m in claim or (m in ev_by_id and any(w in claim for w in ev_by_id[m]["text"][:12])):  # 粗匹配
                ev = ev_by_id.get(m)
                if ev:
                    hit.append(f"证据 [{ev['id']}]（{p['topic']}）说：「{ev['text'][:50]}…」你如何解释它与你的推测的关系？")
    if not hit:
        hit.append("请先明确：你给的说法依据哪一行 [id]？（矛盾对 #1：「入诊者僉云六脈平和」vs 官方脉案恶化曲线——你怎么摆？）")
    parts += hit[:3]
    parts.append("记住：报告只证明死因（砒霜），不指认凶手。")
    return "\n".join(parts)


def deepseek_interrogation(claim, ev_rows, pairs):
    ctx = {
        "sources_tiers": "L1原件/L2可靠出版/L3仅转述；官方/私记/报刊/科学/外国/学术",
        "evidence": [{"id": r["id"], "d": r.get("date_iso"), "stance": r["stance"],
                      "tier": r["tier"], "text": r["text"]} for r in ev_rows],
        "pairs": {k: v for k, v in pairs.items()},
    }
    sysmsg = (
        "你是“史官”，光绪之死证据库的交叉讯问者。规则：只用给出的证据行说话，逐条引 [id]；"
        "发现体验者的说法与证据冲突时，以追问形式提出（你凭什么…？[id] 是否矛盾？）；"
        "不对凶手下结论；提到矛盾对须双面并陈；全程 ≤300 字，结尾一个问题。"
    )
    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": sysmsg + "\n证据JSON：" + json.dumps(ctx, ensure_ascii=False)},
            {"role": "user", "content": f"体验者的推测与理由：\n{claim}\n\n请交叉讯问。"},
        ],
        "max_tokens": 420,
        "temperature": 0.6,
    }
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"},
        method="POST",
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode("utf-8"))
    reply = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    _log({"t": round(time.time() - t0, 1), "usage": usage, "claim": claim[:400], "reply": reply})
    return reply, usage


def _log(entry):
    try:
        entry["mode"] = "deepseek"
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


class H(BaseHTTPRequestHandler):
    def _send(self, obj, code=200):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            page = (STATIC / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
        elif self.path == "/api/timeline":
            src, rows, pairs = rows_all()
            self._send({"sources": src, "rows": rows, "pairs": pairs,
                        "mode": "deepseek" if KEY else "rules"})
        elif self.path == "/api/verdicts":
            total, dist = verdict_stats()
            self._send({"total": total, "dist": dist})
        else:
            self._send({"err": "no such path"}, 404)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
        src, rows, pairs = rows_all()
        ev_by_id = {r["id"]: r for r in rows}
        if self.path == "/api/ask":
            claim = (payload.get("claim") or "").strip()
            order = payload.get("order") or []
            det = []
            for oid in order:
                ev = ev_by_id.get(oid)
                if ev and ev["date_iso"]:
                    det.append(f"{oid}: {ev['date_orig']}（{ev['date_iso']}）")
            enriched = claim + ("\n用户给出的排序：" + "；".join(det) if det else "")
            if KEY:
                try:
                    reply, usage = deepseek_interrogation(enriched, rows, pairs)
                    self._send({"mode": "deepseek", "reply": reply, "tokens": usage})
                    return
                except Exception as e:
                    reply = rule_interrogation(enriched, pairs, ev_by_id)
                    self._send({"mode": "rules(fallback)", "reply": f"模型调用失败（{type(e).__name__}），退回规则库：\n" + reply})
                    return
            self._send({"mode": "rules", "reply": rule_interrogation(enriched, pairs, ev_by_id)})
        elif self.path == "/api/annotate":
            items = payload.get("items") or []
            if not isinstance(items, list) or not items:
                self._send({"err": "empty items"}, 400)
                return
            with sqlite3.connect(DB) as c:
                c.executemany(
                    "INSERT INTO annotation (rumor, stance) VALUES (?, ?)",
                    [(str(x.get("rumor"))[:40], str(x.get("stance"))[:8]) for x in items],
                )
            with sqlite3.connect(DB) as c:
                agg = c.execute("SELECT rumor, stance, COUNT(*) n FROM annotation GROUP BY rumor, stance").fetchall()
            self._send({"ok": True, "agg": [list(a) for a in agg]})
        elif self.path == "/api/verdict":
            choice = payload.get("choice")
            if choice not in CHOICES:
                self._send({"err": "bad choice"}, 400)
                return
            with sqlite3.connect(DB) as c:
                c.execute("INSERT INTO verdict (choice, reason) VALUES (?, ?)",
                          (choice, (payload.get("reason") or "")[:200]))
            total, dist = verdict_stats()
            self._send({"ok": True, "total": total, "dist": dist})
        else:
            self._send({"err": "no such path"}, 404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("serving http://localhost:8000  mode:", "deepseek" if KEY else "RULES")
    ThreadingHTTPServer(("127.0.0.1", 8000), H).serve_forever()
