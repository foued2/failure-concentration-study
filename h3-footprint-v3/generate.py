from __future__ import annotations

import argparse
import ast
import hashlib
import os
import json
import re
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEN = ROOT / "generated"
RAW = GEN / "raw"
BODIES = GEN / "bodies"
WORK = GEN / "work"
ATTEMPTS = GEN / "attempts.jsonl"
OPENCODE = Path(os.environ.get("OPENCODE_EXE", "opencode"))

MODELS = [
    "opencode/deepseek-v4.1-flash-free",
    "opencode/glm-5.3-flash-free",
    "opencode/mimo-v2.6-flash-free",
]
VARIANTS = ["direct", "menu", "simple"]
BODIES_PER_BATCH = 8
MAX_BATCHES = 400

TASK = (
    "Write {n} independent Python implementations of a self-contained function "
    "`solve(n, edges, s, t)`. The function computes the shortest directed path distance "
    "from node s to node t in a graph with n nodes labeled 0..n-1 and non-negative integer "
    "edge weights. edges is a list of (u, v, w) tuples; parallel edges and self-loops may occur. "
    "Return the minimum total weight as an int, or -1 if t is unreachable. Use only the Python "
    "standard library. Do not read files, access the network, print, or include tests or example "
    "usage. Each implementation must be independently written from a plausible first approach; "
    "do not copy or repair one another. Return exactly {n} fenced Python code blocks, each "
    "containing one complete `def solve` and no other prose."
)

PROMPTS = {
    "direct": TASK,
    "menu": TASK
    + " Vary the approaches across the implementations; plausible approaches include heap Dijkstra, "
    "Bellman-Ford, list-scan Dijkstra, layered search, Floyd-Warshall, and DFS path enumeration.",
    "simple": TASK + " Prefer the simplest code that seems correct; do not optimize or self-review.",
}

lock = threading.Lock()


def normalize(source: str) -> str:
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in source.split("\n")]
    return "\n".join(lines).strip() + "\n"


def digest(source: str) -> str:
    return hashlib.sha256(normalize(source).encode()).hexdigest()


def extract(text: str) -> list[str]:
    """Preserve each complete candidate module, including its leading prelude."""
    fence = chr(96) * 3
    blocks = re.findall(fence + r"(?:python|py)?\s*\n(.*?)" + fence, text, flags=re.S | re.I)
    if not blocks:
        blocks = [text]
    out: list[str] = []
    for block in blocks:
        source = normalize(block)
        try:
            module = ast.parse(source)
        except SyntaxError:
            continue
        solve_defs = [node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == "solve"]
        if len(solve_defs) != 1:
            continue
        out.append(source)
    return out


def call_batch(batch_id: int) -> dict:
    model = MODELS[batch_id % len(MODELS)]
    variant = VARIANTS[(batch_id // len(MODELS)) % len(VARIANTS)]
    prompt = PROMPTS[variant].format(n=BODIES_PER_BATCH)
    raw_path = RAW / f"batch-{batch_id:03d}.txt"
    cmd = [
        str(OPENCODE),
        "run",
        "--pure",
        "--format",
        "json",
        "--model",
        model,
        "--dir",
        str(WORK),
        prompt,
    ]
    record = {
        "batch_id": batch_id,
        "model": model,
        "prompt_variant": variant,
        "requested": BODIES_PER_BATCH,
        "raw_path": str(raw_path.relative_to(ROOT)),
    }
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(WORK),
            capture_output=True,
            text=True,
            timeout=600,
            encoding="utf-8",
            errors="replace",
        )
        raw_path.write_text(proc.stdout, encoding="utf-8")
        texts: list[str] = []
        parse_errors = 0
        for line in proc.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                parse_errors += 1
                continue
            if event.get("type") == "text":
                texts.append(event.get("part", {}).get("text", ""))
        text = "\n".join(texts)
        found = extract(text)
        unique: list[str] = []
        duplicates: list[str] = []
        candidate_records: list[dict] = []
        for candidate_index, body in enumerate(found):
            h = digest(body)
            target = BODIES / f"{h}.py"
            is_new = False
            try:
                with target.open("x", encoding="utf-8", newline="\n") as fh:
                    fh.write(body)
                unique.append(h)
                is_new = True
            except FileExistsError:
                duplicates.append(h)
            candidate_records.append({"candidate_index": candidate_index, "body_hash": h, "stored_new": is_new})
        record.update(
            returncode=proc.returncode,
            extracted=len(found),
            unique_new=len(unique),
            duplicate_hashes=duplicates,
            body_hashes=[item["body_hash"] for item in candidate_records],
            unique_body_hashes=unique,
            candidate_records=candidate_records,
            parse_errors=parse_errors,
            stderr_tail=proc.stderr[-1000:],
        )
    except Exception as exc:
        record.update(error=f"{type(exc).__name__}: {exc}", extracted=0, unique_new=0, body_hashes=[])
    with lock:
        with ATTEMPTS.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batches", type=int, default=MAX_BATCHES)
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()
    for d in (RAW, BODIES, WORK):
        d.mkdir(parents=True, exist_ok=True)
    ATTEMPTS.touch(exist_ok=True)
    done = set()
    for line in ATTEMPTS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            done.add(json.loads(line)["batch_id"])
    todo = [i for i in range(min(args.batches, MAX_BATCHES)) if i not in done]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for rec in pool.map(call_batch, todo):
            print(
                f"batch={rec['batch_id']:03d} model={rec['model'].split('/')[-1]} "
                f"variant={rec['prompt_variant']} extracted={rec.get('extracted', 0)} "
                f"new={rec.get('unique_new', 0)} error={rec.get('error', '')}"
            )


if __name__ == "__main__":
    main()
