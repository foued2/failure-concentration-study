"""Run the authorized Gemini feasibility pilot; no predictive models are fitted."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import argparse
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PILOT = Path(__file__).resolve().parent
REPO = PILOT.parent
PIPELINE = PILOT / "python-pipeline-integration"
sys.path.insert(0, str(PILOT)); sys.path.insert(0, str(REPO)); sys.path.insert(0, str(PIPELINE))

import run_generated_smoke as pipeline
from pilot_tool import body_id
from source_policy import screen_source
from study.families import FAMILY_ORDER
from study.features import concentration, family_counts

CAP = 100
RUN_LABEL = "natural-pilot-gemini"
PROVIDER = "Google Gemini API"
MODEL = "gemini-3.5-flash-lite"
ENDPOINT_HOST = "generativelanguage.googleapis.com"
ENDPOINT_PATH = f"/v1beta/models/{MODEL}:generateContent"
GENERATION_CONFIG = {"temperature": 1.0, "maxOutputTokens": 4096}
MODEL_AMENDMENT = PILOT / "FOLLOWUP_MODEL_AMENDMENT_2026-10-21.md"
PROVIDER_BLOCK_MARKERS = ("usage limit", "rate limit", "quota", "too many requests", "hard block")
HALT_STATES = {"HALTED_GENERATION_USAGE_LIMIT", "HALTED_GENERATION_FAILURE"}
POPULATION = (f"{PROVIDER}, model {MODEL}, one exact SSSP prompt per attempt; "
              "backend snapshot unavailable")
RUN = PILOT / f"{RUN_LABEL}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def save_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temp, path)


def validate_run_label(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", value):
        raise ValueError("run label must be 1-64 safe path characters")
    return value


def parse_not_before(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("--not-before must include a timezone")
    return parsed.astimezone(timezone.utc)


def redact_secret(value: str, secret: str | None) -> str:
    return value.replace(secret, "[REDACTED]") if secret else value


def extract_gemini_text(payload: dict) -> str:
    parts = []
    for candidate in payload.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if part.get("thought"):
                continue
            if part.get("text"):
                parts.append(part["text"])
    return "".join(parts)


def classify_http_failure(code: int, body: str) -> str:
    text = body.lower()
    if code == 429 or any(marker in text for marker in PROVIDER_BLOCK_MARKERS):
        return "usage_limit"
    if code in (401, 403):
        return "auth"
    return "provider_error"


def retained_state(run: Path) -> str | None:
    path = run / "PILOT_RESULTS.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8")).get("state")


def request_one(attempt_dir: Path, number: int) -> dict:
    response_path = attempt_dir / "generated-response.txt"
    key = os.environ.get("GEMINI_API_KEY")
    endpoint = f"https://{ENDPOINT_HOST}{ENDPOINT_PATH}"
    save_json(attempt_dir / "generation-request.json", {
        "provider": PROVIDER, "model": MODEL, "endpoint": endpoint,
        "generation_config": GENERATION_CONFIG,
        "prompt_sha256": hashlib.sha256(pipeline.PROMPT.encode("utf-8")).hexdigest(),
        "api_key_env": "GEMINI_API_KEY", "api_key_present": bool(key),
    })
    if not key:
        save_json(attempt_dir / "generation-error.json", {"error": "GEMINI_API_KEY is not configured"})
        (attempt_dir / "generation-stderr.txt").write_text("GEMINI_API_KEY is not configured\n", encoding="utf-8")
        return {"status": "generation_failed", "failure_kind": "auth", "elapsed_seconds": 0.0,
                "http_status": None, "response_present": False}
    body = {"contents": [{"role": "user", "parts": [{"text": pipeline.PROMPT}]}],
            "generationConfig": GENERATION_CONFIG}
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    started_at = datetime.now(timezone.utc)
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read()
        elapsed = time.perf_counter() - started
        finished_at = datetime.now(timezone.utc)
        payload = json.loads(raw.decode("utf-8"))
        (attempt_dir / "gemini-response.json").write_bytes(raw)
        text = extract_gemini_text(payload)
        candidate = (payload.get("candidates") or [{}])[0]
        finish_reason = candidate.get("finishReason")
        usage = payload.get("usageMetadata", {})
        save_json(attempt_dir / "generation-metadata.json", {
            "http_status": 200, "finish_reason": finish_reason, "usage": usage,
            "invoked_at_utc": started_at.isoformat(), "finished_at_utc": finished_at.isoformat(),
            "elapsed_seconds": elapsed,
        })
        if not text:
            prompt_block = payload.get("promptFeedback", {}).get("blockReason")
            reason = prompt_block or finish_reason or "empty response"
            failure_kind = "provider_block" if prompt_block else "other"
            (attempt_dir / "generation-stderr.txt").write_text(
                f"Gemini returned no text: {reason}\n", encoding="utf-8")
            return {"status": "generation_failed", "failure_kind": failure_kind,
                    "elapsed_seconds": elapsed, "http_status": 200, "response_present": False,
                    "finish_reason": finish_reason, "invoked_at_utc": started_at.isoformat(),
                    "finished_at_utc": finished_at.isoformat()}
        if finish_reason != "STOP":
            (attempt_dir / "generation-stderr.txt").write_text(
                f"Gemini finishReason={finish_reason}\n", encoding="utf-8")
            return {"status": "generation_failed",
                    "failure_kind": "truncated" if finish_reason == "MAX_TOKENS" else "other",
                    "elapsed_seconds": elapsed, "http_status": 200, "response_present": True,
                    "finish_reason": finish_reason, "invoked_at_utc": started_at.isoformat(),
                    "finished_at_utc": finished_at.isoformat()}
        response_path.write_text(text, encoding="utf-8")
        source = text
        (attempt_dir / "generated-solver.py").write_text(source, encoding="utf-8")
        screen = screen_source(source)
        screened = {"accepted": screen.accepted, "reasons": screen.reasons,
                    "body_id": body_id(source), "source_bytes": len(source.encode("utf-8"))}
        save_json(attempt_dir / "source-screen.json", screened)
        return {"status": "generated", "elapsed_seconds": elapsed, "http_status": 200,
                "finish_reason": finish_reason, "usage": usage, "source": source, "screen": screened,
                "invoked_at_utc": started_at.isoformat(), "finished_at_utc": finished_at.isoformat()}
    except urllib.error.HTTPError as exc:
        elapsed = time.perf_counter() - started
        raw_error = exc.read().decode("utf-8", "replace")
        safe_error = redact_secret(raw_error, key)
        save_json(attempt_dir / "generation-error.json", {
            "http_status": exc.code, "reason": redact_secret(str(exc.reason), key),
            "body": safe_error[:4000], "invoked_at_utc": started_at.isoformat(),
        })
        (attempt_dir / "generation-stderr.txt").write_text(
            f"HTTP {exc.code}: {exc.reason}\n{safe_error[:2000]}\n", encoding="utf-8")
        return {"status": "generation_failed", "failure_kind": classify_http_failure(exc.code, safe_error),
                "elapsed_seconds": elapsed, "http_status": exc.code, "response_present": False,
                "invoked_at_utc": started_at.isoformat(),
                "finished_at_utc": datetime.now(timezone.utc).isoformat()}
    except urllib.error.URLError as exc:
        elapsed = time.perf_counter() - started
        safe_error = redact_secret(str(exc.reason), key)
        save_json(attempt_dir / "generation-error.json", {"error": safe_error,
            "invoked_at_utc": started_at.isoformat()})
        (attempt_dir / "generation-stderr.txt").write_text(safe_error + "\n", encoding="utf-8")
        return {"status": "generation_failed", "failure_kind": "network", "elapsed_seconds": elapsed,
                "http_status": None, "response_present": False,
                "invoked_at_utc": started_at.isoformat(),
                "finished_at_utc": datetime.now(timezone.utc).isoformat()}
    except TimeoutError:
        elapsed = time.perf_counter() - started
        save_json(attempt_dir / "generation-error.json", {"error": "timeout",
            "invoked_at_utc": started_at.isoformat()})
        (attempt_dir / "generation-stderr.txt").write_text("Gemini request timed out\n", encoding="utf-8")
        return {"status": "generation_timeout", "failure_kind": "timeout", "elapsed_seconds": elapsed,
                "http_status": None, "response_present": False,
                "invoked_at_utc": started_at.isoformat(),
                "finished_at_utc": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        elapsed = time.perf_counter() - started
        safe_error = redact_secret(f"{type(exc).__name__}: {exc}", key)
        save_json(attempt_dir / "generation-error.json", {"error": safe_error,
            "invoked_at_utc": started_at.isoformat()})
        (attempt_dir / "generation-stderr.txt").write_text(safe_error + "\n", encoding="utf-8")
        return {"status": "generation_failed", "failure_kind": "other", "elapsed_seconds": elapsed,
                "http_status": None, "response_present": False,
                "invoked_at_utc": started_at.isoformat(),
                "finished_at_utc": datetime.now(timezone.utc).isoformat()}


def summaries(attempts: list[dict]) -> dict:
    bodies = [row for row in attempts if row.get("diagnostic") is not None and row.get("evaluation") is not None]
    support = defaultdict(lambda: defaultdict(list))
    for row in bodies:
        d = row["diagnostic"]
        pair = (d["k"], float(d["C"]))
        support[pair[0]][pair[1]].append(row)
    fixed_k_contrasts = []
    feasible = False
    for k, c_groups in sorted(support.items()):
        if len(c_groups) < 2:
            continue
        eligible_cs = {c: rows for c, rows in c_groups.items() if len({r["body_id"] for r in rows}) >= 2}
        if len(eligible_cs) < 2:
            continue
        selected = [row for rows in eligible_cs.values() for row in rows]
        pass_counts = {row["attempt_id"]: row["evaluation"]["correct_count"] for row in selected}
        outcome_varies = len(set(pass_counts.values())) > 1
        fixed_k_contrasts.append({"k": k, "C_values": sorted(eligible_cs),
            "distinct_bodies_by_C": {str(c): len({r["body_id"] for r in rows}) for c, rows in eligible_cs.items()},
            "evaluation_correct_counts_by_attempt": pass_counts, "outcomes_vary_across_bodies": outcome_varies})
        feasible = feasible or outcome_varies
    return {"eligible_executed_bodies": len(bodies), "fixed_k_contrasts": fixed_k_contrasts,
        "support_by_k_C": {str(k): {str(c): {"attempts": len(rows), "distinct_bodies": len({r['body_id'] for r in rows}),
              "evaluation_correct_counts": [r["evaluation"]["correct_count"] for r in rows]} for c, rows in groups.items()}
              for k, groups in support.items()}, "feasibility_demonstrated": feasible}


def persist(attempts: list[dict], state: str, halt_reason: str | None = None) -> None:
    public = []
    for row in attempts:
        public.append({k: v for k, v in row.items() if k not in {"diagnostic", "evaluation"}} | {
            "diagnostic": row.get("diagnostic"), "evaluation_summary": row.get("evaluation")})
    save_json(RUN / "attempts.json", public)
    summary = summaries(attempts)
    generated = sum(r.get("generation_status") == "generated" for r in attempts)
    generation_failures = sum(r.get("generation_status") != "generated" for r in attempts)
    save_json(RUN / "PILOT_RESULTS.json", {"run_id": RUN.name, "state": state, "attempt_count": len(attempts),
        "attempt_cap": CAP, "generation_requests": len(attempts),
        "model_written_generation_attempts": generated, "generation_failures": generation_failures,
        "distinct_canonical_bodies": len({r["body_id"] for r in attempts if r.get("body_id")}),
        "excluded_or_not_executed": sum(r.get("execution_status") not in {"complete", "duplicate_reused"} for r in attempts),
        "summary": summary, "predictive_model_fitted": False, "halt_reason": halt_reason,
        "population": POPULATION,
        "caveat": "Exploratory feasibility only. Full suite inputs are visible inside their respective guest session; static screen is not a security guarantee."})
    lines = ["# Bounded natural-solver feasibility pilot", "", f"State: **{state}**", "",
        f"Generation requests: {len(attempts)}/{CAP}.",
        f"Model-written generation outputs: {generated}; generation failures: {generation_failures}.",
        f"Distinct canonical bodies: {len({r['body_id'] for r in attempts if r.get('body_id')})}.",
        f"Executed bodies with complete diagnostic and evaluation records: {summary['eligible_executed_bodies']}.",
        "", "No predictive model was fitted and no concentration effect was tested.", ""]
    if halt_reason:
        lines += [f"Halt reason: {halt_reason}", ""]
    lines += [
        "The guest could read the full diagnostic suite during its diagnostic session and the full evaluation bank during its evaluation session. Source screening is a best-effort policy, not a security boundary.", "",
        "Fixed-k feasibility contrasts:"]
    lines.extend([f"- k={x['k']}: C={x['C_values']}; bodies/C={x['distinct_bodies_by_C']}; evaluation outcomes vary={x['outcomes_vary_across_bodies']}." for x in summary["fixed_k_contrasts"]] or ["- None met the minimum support rule."])
    lines += ["", "This pilot can establish only whether this declared generator procedure supplies the required observed comparisons within the cap. It cannot establish that concentration predicts correctness.", ""]
    (RUN / "FEASIBILITY_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    global RUN
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", type=Path, help="continue a retained pilot after a recorded runner defect")
    parser.add_argument("--run-label", default=RUN_LABEL, help="new run directory prefix")
    parser.add_argument("--not-before", help="optional timezone-aware UTC not-before gate")
    parser.add_argument("--smoke-result", type=Path, help="required PASS smoke result for a new run")
    args = parser.parse_args()
    smoke_result = None
    if args.resume:
        RUN = args.resume.resolve()
        if not (RUN / "attempts.json").is_file():
            raise FileNotFoundError(RUN / "attempts.json")
        retained = json.loads((RUN / "attempts.json").read_text(encoding="utf-8"))
        if len(retained) >= CAP:
            raise RuntimeError("retained run already reached the request cap; start a separate run")
        if retained_state(RUN) in HALT_STATES:
            raise RuntimeError("halted runs are final; start a separate run")
    else:
        label = validate_run_label(args.run_label)
        if args.not_before:
            not_before = parse_not_before(args.not_before)
            if datetime.now(timezone.utc) < not_before:
                raise ValueError(f"refusing to start before {not_before.isoformat()}")
        if not os.environ.get("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY is not configured")
        if args.smoke_result is None:
            raise RuntimeError("--smoke-result is required before starting a new Gemini run")
        smoke_result = args.smoke_result.resolve()
        smoke = json.loads(smoke_result.read_text(encoding="utf-8"))
        if smoke.get("status") != "PASS" or smoke.get("provider") != PROVIDER or smoke.get("model") != MODEL:
            raise RuntimeError("smoke result is not a PASS for this provider and model")
        RUN = PILOT / f"{label}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        if RUN.exists():
            raise FileExistsError(RUN)
    if not pipeline.previous.SANDBOX.is_file() or not pipeline.previous.PYTHON_BASE.is_dir():
        raise RuntimeError("required Sandbox or Python runtime unavailable")
    pipeline.previous.check_no_running_sandbox()
    if not args.resume:
        RUN.mkdir()
        (RUN / "prompt.txt").write_text(pipeline.PROMPT + "\n", encoding="utf-8")
        smoke_sha = hashlib.sha256(smoke_result.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        save_json(RUN / "protocol.json", {
        "date": datetime.now(timezone.utc).isoformat(), "provider": PROVIDER, "model": MODEL,
        "endpoint": f"https://{ENDPOINT_HOST}{ENDPOINT_PATH}", "api_version": "v1beta",
        "api_key_env": "GEMINI_API_KEY", "generation_config": GENERATION_CONFIG,
        "backend_version": None, "immutable_snapshot": None,
        "backend_identity_note": "Backend snapshot/version is unavailable; no exact reproducibility claim.",
        "run_label": args.run_label, "not_before_utc": args.not_before,
        "population_changed": True, "not_equivalent_to_codex_population": True,
        "authorization_amendment": "natural-feasibility-pilot/FOLLOWUP_PROVIDER_AMENDMENT_2026-10-21.md",
        "authorization_amendment_sha256": hashlib.sha256((PILOT / "FOLLOWUP_PROVIDER_AMENDMENT_2026-10-21.md").read_text(encoding="utf-8").encode("utf-8")).hexdigest(),
        "model_amendment": str(MODEL_AMENDMENT.relative_to(REPO)),
        "model_amendment_sha256": hashlib.sha256(MODEL_AMENDMENT.read_text(encoding="utf-8").encode("utf-8")).hexdigest(),
        "model_change_reason": "gemini-2.5-flash returned HTTP 503 UNAVAILABLE (high demand); one bounded model switch to gemini-3.5-flash-lite.",
        "frozen_protocol_commit": "74cd419", "decision_memo_commit": "dd5be4a",
        "smoke_result": str(smoke_result), "smoke_result_sha256": smoke_sha,
        "attempt_cap": CAP, "evaluation_input_count": 20, "diagnostic_probe_count": 30,
        "request_accounting": "Every generation invocation counts, including failures.",
        "halt_on_first_generation_failure": True,
        "timeout_ms_per_worker": 10000, "worker_memory_limit_bytes": 128 * 1024 * 1024,
        "networking": "disabled in Windows Sandbox", "generation_prompt_contains_test_inputs": False,
        "containment_disclosure": "Source screen is best-effort; full phase-specific input suite is guest-readable during its Sandbox session."})
    diagnostic = json.loads((PILOT / "diagnostic_battery.json").read_text(encoding="utf-8"))
    evaluation = json.loads((PILOT / "evaluation_bank.json").read_text(encoding="utf-8"))
    if len(diagnostic) != 30 or len(evaluation) != 20 or {x["input_id"] for x in diagnostic} & {x["input_id"] for x in evaluation}:
        raise RuntimeError("prepared input banks failed integrity checks")
    diag_requests = [{"probe_id": x["probe_id"], "input": x["input"]} for x in diagnostic]
    eval_requests = [{"probe_id": x["hid"], "input": x["input"]} for x in evaluation]
    if args.resume:
        attempts = []
        for row in retained:
            restored = dict(row)
            restored["evaluation"] = restored.pop("evaluation_summary", None)
            attempts.append(restored)
        seen_body: dict[str, str] = {}
        for row in attempts:
            if row.get("body_id"):
                seen_body.setdefault(row["body_id"], row["attempt_id"])
        first_index = len(attempts) + 1
        # Attempt directories may have been created immediately before an
        # interruption; an empty one has no generation request and is reused.
    else:
        attempts = []; seen_body = {}; first_index = 1

    with tempfile.TemporaryDirectory(prefix="fc-natural-pilot-") as temp_dir:
        temp = Path(temp_dir); runtime = temp / "python"
        shutil.copytree(pipeline.previous.PYTHON_BASE, runtime, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for index in range(first_index, CAP + 1):
            attempt_id = f"attempt-{index:04d}"
            attempt_dir = RUN / "attempts" / attempt_id
            if attempt_dir.exists() and any(attempt_dir.iterdir()):
                raise RuntimeError(f"unreconciled prior attempt artifacts exist; refusing to rerun {attempt_id}")
            attempt_dir.mkdir(parents=True, exist_ok=True)
            print(f"[{index}/{CAP}] requesting one solver body", flush=True)
            generated = request_one(attempt_dir, index)
            record = {"attempt_id": attempt_id, "generation_order": index,
                "provider": PROVIDER, "model": MODEL,
                "invoked_at_utc": generated.get("invoked_at_utc"),
                "finished_at_utc": generated.get("finished_at_utc"),
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "generation_elapsed_seconds": generated.get("elapsed_seconds"),
                "generation_http_status": generated.get("http_status"),
                "generation_finish_reason": generated.get("finish_reason"),
                "generation_status": generated["status"], "execution_status": "not_run",
                "attempt_directory": str(attempt_dir.relative_to(RUN))}
            if generated["status"] != "generated":
                record["exclusion_reason"] = generated["status"]
                record["generation_failure_kind"] = generated.get("failure_kind", "other")
                attempts.append(record)
                if generated.get("failure_kind") == "usage_limit":
                    state = "HALTED_GENERATION_USAGE_LIMIT"
                    reason = ("Gemini API reported a usage limit on the first failed generation request; "
                              "halted immediately and will not repeat the request.")
                else:
                    state = "HALTED_GENERATION_FAILURE"
                    reason = (f"Generation request failed ({generated.get('failure_kind', 'other')}); "
                              "halted immediately and will not repeat the request.")
                persist(attempts, state, reason)
                print(f"[{index}/{CAP}] {state}: {reason}", flush=True)
                return
            source = generated["source"]; screened = generated["screen"]; record["body_id"] = screened["body_id"]
            record["source_screen"] = {"accepted": screened["accepted"], "reasons": screened["reasons"]}
            if screened["body_id"] in seen_body:
                record.update({"duplicate_of": seen_body[screened["body_id"]], "execution_status": "duplicate_skipped",
                               "exclusion_reason": "duplicate canonical body; retained without replacement sampling"})
                attempts.append(record); persist(attempts, "RUNNING"); continue
            seen_body[screened["body_id"]] = attempt_id
            if not screened["accepted"]:
                record.update({"execution_status": "source_rejected", "exclusion_reason": list(screened["reasons"])})
                attempts.append(record); persist(attempts, "RUNNING"); continue

            pipeline.RUN = attempt_dir
            try:
                diag_transport, diag_wall = pipeline.execute_suite(temp, f"diagnostic_{attempt_id}", f"diagnostic_{attempt_id}", diag_requests, source, runtime)
                diag_rows = [pipeline.outcome(raw, item, source, "diagnostic") for raw, item in zip(diag_transport["probe_rows"], diagnostic, strict=True)]
                fails = [row["status"] != "pass" for row in diag_rows]
                counts = family_counts(fails); k, c = concentration(fails)
                eval_transport, eval_wall = pipeline.execute_suite(temp, f"evaluation_{attempt_id}", f"evaluation_{attempt_id}", eval_requests, source, runtime)
                eval_rows = [pipeline.outcome(raw, item, source, "evaluation") for raw, item in zip(eval_transport["probe_rows"], evaluation, strict=True)]
                evaluation_summary = {"correct_count": sum(row["correct"] for row in eval_rows),
                                      "pass_fraction": sum(row["correct"] for row in eval_rows) / len(eval_rows),
                                      "all_inputs_passed": all(row["correct"] for row in eval_rows),
                                      "records": eval_rows, "suite_wall_seconds": eval_wall}
                diagnostic_summary = {"records": diag_rows, "family_counts": counts,
                    "family_counts_ordered": [counts[f] for f in FAMILY_ORDER], "k": k, "C": c,
                    "eligible": len(diag_rows) == 30, "suite_wall_seconds": diag_wall}
                save_json(attempt_dir / "host-authoritative/diagnostic.json", diagnostic_summary)
                save_json(attempt_dir / "host-authoritative/evaluation.json", eval_rows)
                record.update({"execution_status": "complete", "diagnostic": diagnostic_summary,
                    "evaluation": evaluation_summary, "total_50_input_wall_seconds": diag_wall + eval_wall})
            except Exception as exc:
                record.update({"execution_status": "runner_error", "exclusion_reason": f"{type(exc).__name__}: {exc}"})
            attempts.append(record)
            state = "RUNNING"
            support = summaries(attempts)
            if support["feasibility_demonstrated"]:
                state = "FEASIBILITY_DEMONSTRATED"
            persist(attempts, state)
            print(f"[{index}/{CAP}] {record['execution_status']} body={record.get('body_id')} k={record.get('diagnostic',{}).get('k')} C={record.get('diagnostic',{}).get('C')}", flush=True)
            if state == "FEASIBILITY_DEMONSTRATED":
                break

    final = summaries(attempts)
    state = "FEASIBILITY_DEMONSTRATED" if final["feasibility_demonstrated"] else "FEASIBILITY_NOT_DEMONSTRATED_WITHIN_CAP"
    persist(attempts, state)
    print(json.dumps({"run_dir": str(RUN), "state": state, "attempts": len(attempts),
                      "distinct_bodies": len({r["body_id"] for r in attempts if r.get("body_id")}),
                      "eligible_bodies": final["eligible_executed_bodies"], "fixed_k_contrasts": final["fixed_k_contrasts"]}, indent=2), flush=True)


if __name__ == "__main__":
    main()
