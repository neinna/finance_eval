#!/usr/bin/env python3
"""Run the consumer-finance cases against Gemini. Python 3.8+, standard library only.

  export GEMINI_API_KEY=...            # free key from aistudio.google.com
  python3 run.py                        # all cases, baseline + principle, newest Gemini Pro
  python3 run.py --list-models          # see what your key can use
  python3 run.py --model gemini-2.5-pro --cases c01,c06
  python3 run.py --dry-run              # build requests, send nothing
  python3 run.py --make-manual          # writes manual_runs.md for pasting into the Gemini app

Results go to results/<timestamp>_<model>_<arm>.jsonl. Send those files back for scoring.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://generativelanguage.googleapis.com/v1beta"
HERE = Path(__file__).resolve().parent
EXCLUDE = ("embedding", "tts", "image", "vision", "live", "learnlm", "aqa", "audio", "veo", "imagen")


RETRIES = 5


def call(method, path, key, body=None, retries=None):
    retries = retries or RETRIES
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{API}/{path}", data=data, method=method,
                                 headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 503) and attempt < retries - 1:
                wait = 20 * (attempt + 1)
                print(f"  HTTP {e.code}, retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}") from None
        except urllib.error.URLError as e:
            if attempt < retries - 1:
                time.sleep(10)
                continue
            raise RuntimeError(f"network error: {e.reason}") from None


def list_models(key):
    out = call("GET", "models?pageSize=1000", key)
    return [m["name"].split("/", 1)[1] for m in out.get("models", [])
            if "generateContent" in m.get("supportedGenerationMethods", [])]


def pick_model(names):
    def score(n):
        v = re.search(r"gemini-(\d+(?:\.\d+)?)", n)
        return (float(v.group(1)) if v else 0, "preview" not in n and "exp" not in n, -len(n))
    pro = [n for n in names if "pro" in n and not any(x in n for x in EXCLUDE)]
    return max(pro or names, key=score)


def probe(key):
    names = [n for n in list_models(key) if n.startswith("gemini") and not any(x in n for x in EXCLUDE)]
    def ver(n):
        v = re.search(r"gemini-(\d+(?:\.\d+)?)", n)
        return float(v.group(1)) if v else 0
    names = sorted(names, key=ver, reverse=True)[:8]
    body = {"contents": [{"role": "user", "parts": [{"text": "Reply with the single word OK."}]}]}
    print(f"{'model':40} {'no search':12} search")
    for n in names:
        res = []
        for search in (False, True):
            b = dict(body)
            if search:
                b["tools"] = [{"google_search": {}}]
            try:
                call("POST", f"models/{n}:generateContent", key, b, retries=1)
                res.append("OK")
            except RuntimeError as e:
                res.append(str(e)[:9])
            time.sleep(1)
        print(f"{n:40} {res[0]:12} {res[1]}")


def load_cases(only):
    cases = json.loads((HERE / "cases.json").read_text())["cases"]
    if only:
        wanted = set(only.split(","))
        cases = [c for c in cases if c["id"] in wanted]
    return cases


def build_request(case, arm, search):
    parts = [{"text": case["prompt"]}]
    for name in case["files"]:
        text = (HERE / "files" / name).read_text()
        parts.append({"text": f"Attached file: {name}\n\n{text}"})
    body = {"contents": [{"role": "user", "parts": parts}]}
    if arm == "principle":
        body["systemInstruction"] = {"parts": [{"text": (HERE / "prompts" / "principle.txt").read_text()}]}
    if search:
        body["tools"] = [{"google_search": {}}]
    return body


def parse(resp):
    cand = (resp.get("candidates") or [{}])[0]
    parts = cand.get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    chunks = cand.get("groundingMetadata", {}).get("groundingChunks", [])
    sources = [{"title": c.get("web", {}).get("title"), "uri": c.get("web", {}).get("uri")} for c in chunks]
    return {"answer": text, "finish_reason": cand.get("finishReason"), "sources": sources,
            "model_version": resp.get("modelVersion"), "usage": resp.get("usageMetadata")}


def make_manual(cases):
    out = ["# Manual runs for the Gemini app", "",
           "For each case: open a new chat, paste the prompt, attach the listed files from files/, "
           "send, and paste Gemini's full answer under ANSWER. Run each case in its own new chat.", ""]
    for c in cases:
        out += [f"## {c['id']}: {c['title']}", "", "PROMPT:", "", c["prompt"], "",
                f"ATTACH: {', '.join(c['files']) or 'none'}", "", "ANSWER:", "", "", "---", ""]
    (HERE / "manual_runs.md").write_text("\n".join(out))
    print("wrote manual_runs.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model")
    ap.add_argument("--arm", choices=["baseline", "principle", "both"], default="both")
    ap.add_argument("--cases", help="comma-separated ids, e.g. c01,c06")
    ap.add_argument("--no-search", action="store_true", help="turn off Google Search grounding")
    ap.add_argument("--list-models", action="store_true")
    ap.add_argument("--probe", action="store_true", help="test which models and search your key can use")
    ap.add_argument("--retries", type=int, default=5)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--make-manual", action="store_true")
    ap.add_argument("--pause", type=float, default=4.0, help="seconds between calls (free-tier limits)")
    a = ap.parse_args()
    global RETRIES
    RETRIES = a.retries

    cases = load_cases(a.cases)
    if a.make_manual:
        return make_manual(cases)

    arms = ["baseline", "principle"] if a.arm == "both" else [a.arm]
    search = not a.no_search

    if a.dry_run:
        for c in cases:
            for arm in arms:
                body = build_request(c, arm, search)
                size = len(json.dumps(body))
                print(f"{c['id']} {arm:9} files={len(c['files'])} request_bytes={size}")
        return

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("Set GEMINI_API_KEY first (free key at aistudio.google.com).")

    if a.probe:
        return probe(key)

    if a.list_models:
        for n in sorted(list_models(key)):
            print(n)
        return

    model = a.model or pick_model(list_models(key))
    print(f"model: {model}  arms: {arms}  search: {search}  cases: {len(cases)}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%MZ")
    (HERE / "results").mkdir(exist_ok=True)

    for arm in arms:
        path = HERE / "results" / f"{stamp}_{model}_{arm}.jsonl"
        with path.open("w") as f:
            for c in cases:
                started = time.time()
                row = {"case_id": c["id"], "arm": arm, "model": model, "search": search,
                       "run_at": datetime.now(timezone.utc).isoformat()}
                try:
                    row.update(parse(call("POST", f"models/{model}:generateContent", key,
                                          build_request(c, arm, search))))
                except RuntimeError as e:
                    row["error"] = str(e)
                row["latency_s"] = round(time.time() - started, 1)
                f.write(json.dumps(row) + "\n")
                f.flush()
                status = ("ERROR " + row["error"][:160].replace("\n", " ")) if "error" in row else f"{len(row['answer'])} chars"
                print(f"  {arm:9} {c['id']}  {status}  {row['latency_s']}s")
                time.sleep(a.pause)
        print(f"wrote {path.relative_to(HERE)}")
    print("Done. Send the results/ files back for scoring.")


if __name__ == "__main__":
    main()
