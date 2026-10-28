from __future__ import annotations

import argparse
import ast
import hashlib
import json
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEN = ROOT / "generated"
RAW = GEN / "raw"
BODIES = GEN / "bodies"
WORK = GEN / "work"
ATTEMPTS = GEN / "attempts.jsonl"

# Anonymous OVHcloud AI Endpoints. No API key or Authorization header is used.
# This is a V4 proposal only; V3's named generator population remains unchanged.
ENDPOINT = "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/chat/completions"
MODEL = "gpt-oss-120b"
VARIANTS = ["direct", "menu", "simple"]
BODIES_PER_BATCH = 8
MAX_BATCHES = 400
MIN_REQUEST_START_INTERVAL_SECONDS = 35.0
REQUEST_TIMEOUT_SECONDS = 180
MAX_TRANSIENT_ATTEMPTS = 5

TASK = (
    "Write {n} independent Python implementations of a self-contained function "
    "solve(n, edges, s, t). The function computes the shortest directed path distance "
    "from node s to node t in a graph with n nodes labeled 0..n-1 and non-negative integer "
    "edge weights. edges is a list of (u, v, w) tuples; parallel edges and self-loops may occur. "
    "Return the minimum total weight as an int, or -1 if t is unreachable. Use only the Python "
    "standard library. Do not read files, access the network, print, or include tests or example "
    "usage. Each implementation must be independently written from a plausible first approach; "
    "do not copy or repair one another. Return exactly {n} fenced Python code blocks, each "
    "containing one complete solve function and no other prose."
)

PROMPTS = {
    "direct": TASK,
    "menu": TASK
    + " Vary the approaches across the implementations; plausible approaches include heap Dijkstra, "
    "Bellman-Ford, list-scan Dijkstra, layered search, Floyd-Warshall, and DFS path enumeration.",
    "simple": TASK + " Prefer the simplest code that seems correct; do not optimize or self-review.",
}

_lock = threading.Lock()
_last_request_started: float | None = None


def normalize(source: str) -> str:
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in source.split("\n")]
    return "\n".join(lines).strip() + "\n"


def digest(source: str) -> str:
    return hashlib.sha256(normalize(source).encode("utf-8")).hexdigest()


def extract(text: str) -> list[str]:
    """Preserve complete fenced modules, including their leading imports/helpers."""
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
        solve_defs = [
            node for node in module.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "solve"
        ]
        if len(solve_defs) != 1 or isinstance(solve_defs[0], ast.AsyncFunctionDef):
            continue
        out.append(source)
    return out


def _wait_for_request_slot() -> None:
    """Keep request starts at least 35 seconds apart on the anonymous 2-RPM lane."""
    global _last_request_started
    now = time.monotonic()
    if _last_request_started is not None:
        delay = MIN_REQUEST_START_INTERVAL_SECONDS - (now - _last_request_started)
        if delay > 0:
            time.sleep(delay)
    _last_request_started = time.monotonic()


def _write_attempt(record: dict) -> None:
    with _lock:
        with ATTEMPTS.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")


def _request_completion(prompt: str) -> tuple[int, dict, dict]:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "stream": False,
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    _wait_for_request_slot()
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            status = response.status
            raw = response.read()
            headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        status = exc.code
        raw = exc.read()
        headers = dict(exc.headers.items())
    elapsed = round(time.monotonic() - started, 3)
    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        data = {
            "_response_parse_error": f"{type(exc).__name__}: {exc}",
            "_raw_prefix": raw[:1000].decode("utf-8", "replace"),
        }
    meta = {
        "http_status": status,
        "elapsed_seconds": elapsed,
        "retry_after": headers.get("Retry-After") or headers.get("retry-after"),
        "response_id": data.get("id") if isinstance(data, dict) else None,
        "returned_model": data.get("model") if isinstance(data, dict) else None,
        "usage": data.get("usage") if isinstance(data, dict) else None,
        "finish_reason": (
            data.get("choices", [{}])[0].get("finish_reason")
            if isinstance(data, dict) and data.get("choices") else None
        ),
    }
    return status, data, meta


def call_batch(batch_id: int) -> dict:
    variant = VARIANTS[batch_id % len(VARIANTS)]
    prompt = PROMPTS[variant].format(n=BODIES_PER_BATCH)
    prompt_sha256 = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    raw_path = RAW / f"batch-{batch_id:03d}.txt"
    response_path = RAW / f"batch-{batch_id:03d}-response.json"
    record = {
        "batch_id": batch_id,
        "model": MODEL,
        "provider": "ovhcloud-ai-endpoints-anonymous",
        "endpoint": ENDPOINT,
        "prompt_variant": variant,
        "prompt_sha256": prompt_sha256,
        "requested": BODIES_PER_BATCH,
        "raw_path": str(raw_path.relative_to(ROOT)),
        "raw_response_path": str(response_path.relative_to(ROOT)),
        "completed": False,
        "transient_errors": [],
    }

    for attempt in range(1, MAX_TRANSIENT_ATTEMPTS + 1):
        try:
            status, data, meta = _request_completion(prompt)
        except Exception as exc:
            record["transient_errors"].append({
                "attempt": attempt,
                "error": f"{type(exc).__name__}: {exc}",
            })
            if attempt < MAX_TRANSIENT_ATTEMPTS:
                time.sleep(min(60.0, 5.0 * attempt))
                continue
            record.update(deferred=True, error="network_error_retries_exhausted", attempts=attempt)
            _write_attempt(record)
            return record

        if status == 429 or status >= 500:
            record["transient_errors"].append({"attempt": attempt, **meta})
            if attempt < MAX_TRANSIENT_ATTEMPTS:
                try:
                    retry_delay = float(meta["retry_after"]) if meta.get("retry_after") else 35.0
                except (TypeError, ValueError):
                    retry_delay = 35.0
                time.sleep(max(35.0, min(retry_delay, 300.0)))
                continue
            record.update(
                deferred=True,
                error="rate_limit_or_server_retries_exhausted",
                http_status=status,
                attempts=attempt,
            )
            response_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            _write_attempt(record)
            return record

        if status != 200:
            record.update(
                deferred=True,
                terminal_error=True,
                error=f"http_status_{status}",
                http_status=status,
                attempts=attempt,
            )
            response_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            _write_attempt(record)
            return record

        raw_text = ""
        try:
            choice = data["choices"][0]
            message = choice["message"]
            raw_text = message.get("content") or ""
            if not isinstance(raw_text, str):
                raw_text = str(raw_text)
            record["returned_model"] = data.get("model")
            record["response_id"] = data.get("id")
            record["finish_reason"] = choice.get("finish_reason")
            record["usage"] = data.get("usage")
        except Exception as exc:
            record["response_shape_error"] = f"{type(exc).__name__}: {exc}"

        # Preserve the exact model text and complete response envelope.
        raw_path.write_text(raw_text, encoding="utf-8", newline="\n")
        response_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        found = extract(raw_text)
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
            candidate_records.append({
                "candidate_index": candidate_index,
                "body_hash": h,
                "stored_new": is_new,
            })

        record.update(
            completed=True,
            deferred=False,
            http_status=status,
            returncode=0,
            extracted=len(found),
            unique_new=len(unique),
            duplicate_hashes=duplicates,
            body_hashes=[item["body_hash"] for item in candidate_records],
            unique_body_hashes=unique,
            candidate_records=candidate_records,
            attempts=attempt,
            **meta,
        )
        _write_attempt(record)
        return record

    raise AssertionError("unreachable retry state")


def completed_batch_ids() -> set[int]:
    done: set[int] = set()
    if not ATTEMPTS.exists():
        return done
    for line in ATTEMPTS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("completed") is True:
            done.add(int(row["batch_id"]))
    return done


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-batch", type=int, default=0)
    parser.add_argument("--end-batch", type=int, default=MAX_BATCHES,
                        help="exclusive upper bound; default processes through batch 399")
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    if args.workers != 1:
        parser.error("anonymous endpoint protocol is serial; --workers must equal 1")
    if not (0 <= args.start_batch <= args.end_batch <= MAX_BATCHES):
        parser.error(f"expected 0 <= start-batch <= end-batch <= {MAX_BATCHES}")

    for directory in (RAW, BODIES, WORK):
        directory.mkdir(parents=True, exist_ok=True)
    ATTEMPTS.touch(exist_ok=True)
    done = completed_batch_ids()
    todo = [i for i in range(args.start_batch, args.end_batch) if i not in done]
    for batch_id in todo:
        row = call_batch(batch_id)
        print(
            f"batch={batch_id:03d} model={MODEL} variant={row['prompt_variant']} "
            f"completed={row.get('completed', False)} "
            f"extracted={row.get('extracted', 0)} new={row.get('unique_new', 0)} "
            f"deferred={row.get('deferred', False)} "
            f"error={row.get('error', '')}",
            flush=True,
        )
        if row.get("terminal_error"):
            raise SystemExit(1)
        if row.get("deferred"):
            raise SystemExit(75)


if __name__ == "__main__":
    main()
