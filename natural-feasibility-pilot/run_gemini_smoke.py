"""Run one Gemini-generated solver through the real Sandbox execution path."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PILOT = Path(__file__).resolve().parent
REPO = PILOT.parent
sys.path.insert(0, str(PILOT)); sys.path.insert(0, str(REPO))
sys.path.insert(0, str(PILOT / "python-pipeline-integration"))

import run_gemini_pilot as pilot
import run_generated_smoke as pipeline

AMENDMENT = PILOT / "FOLLOWUP_PROVIDER_AMENDMENT_2026-10-21.md"


def save_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    run = PILOT / f"gemini-smoke-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    if run.exists():
        raise FileExistsError(run)
    if not pipeline.previous.SANDBOX.is_file() or not pipeline.previous.PYTHON_BASE.is_dir():
        raise RuntimeError("required Sandbox or Python runtime unavailable")
    pipeline.previous.check_no_running_sandbox()
    run.mkdir()
    (run / "prompt.txt").write_text(pipeline.PROMPT + "\n", encoding="utf-8")
    save_json(run / "protocol.json", {
        "date": datetime.now(timezone.utc).isoformat(), "stage": "gemini_smoke",
        "provider": pilot.PROVIDER, "model": pilot.MODEL,
        "endpoint": f"https://{pilot.ENDPOINT_HOST}{pilot.ENDPOINT_PATH}",
        "generation_config": pilot.GENERATION_CONFIG,
        "api_key_env": "GEMINI_API_KEY", "backend_version": None, "immutable_snapshot": None,
        "authorization_amendment": str(AMENDMENT.relative_to(REPO)),
        "authorization_amendment_sha256": hashlib.sha256(AMENDMENT.read_text(encoding="utf-8").encode("utf-8")).hexdigest(),
        "frozen_protocol_commit": "74cd419", "decision_memo_commit": "dd5be4a",
        "request_count": 1, "pilot_cap": 100, "smoke_separate_from_pilot": True,
        "smoke_criteria": "source accepted; 30/30 diagnostic rows complete and pass; 20/20 evaluation rows complete and correct; complete SDK records",
        "containment_disclosure": "Source screen is best-effort; full phase-specific input suite is guest-readable during its Sandbox session.",
    })
    attempt_id = "attempt-0001"
    attempt_dir = run / "attempts" / attempt_id
    attempt_dir.mkdir(parents=True)
    print("[smoke] requesting one solver body from Gemini", flush=True)
    generated = pilot.request_one(attempt_dir, 1)
    record = {
        "attempt_id": attempt_id, "generation_order": 1,
        "provider": pilot.PROVIDER, "model": pilot.MODEL,
        "invoked_at_utc": generated.get("invoked_at_utc"),
        "finished_at_utc": generated.get("finished_at_utc"),
        "generation_elapsed_seconds": generated.get("elapsed_seconds"),
        "generation_http_status": generated.get("http_status"),
        "generation_finish_reason": generated.get("finish_reason"),
        "generation_status": generated["status"], "execution_status": "not_run",
        "attempt_directory": str(attempt_dir.relative_to(run)),
    }
    if generated["status"] != "generated":
        record["exclusion_reason"] = generated["status"]
        record["generation_failure_kind"] = generated.get("failure_kind", "other")
        save_json(attempt_dir / "attempt.json", record)
        result = {"status": "FAIL", "stage": "generation", "run": run.name,
                  "provider": pilot.PROVIDER, "model": pilot.MODEL,
                  "failure_kind": generated.get("failure_kind", "other"),
                  "generation_status": generated["status"],
                  "http_status": generated.get("http_status"),
                  "request_count": 1, "pilot_started": False,
                  "halt_reason": "Gemini smoke generation failed; no pilot was started."}
        save_json(run / "SMOKE_RESULT.json", result)
        print(json.dumps(result, indent=2), flush=True)
        raise SystemExit(1)
    source = generated["source"]
    screened = generated["screen"]
    record["body_id"] = screened["body_id"]
    record["source_screen"] = {"accepted": screened["accepted"], "reasons": screened["reasons"]}
    if not screened["accepted"]:
        record.update({"execution_status": "source_rejected", "exclusion_reason": list(screened["reasons"])})
        save_json(attempt_dir / "attempt.json", record)
        result = {"status": "FAIL", "stage": "source_screen", "run": run.name,
                  "provider": pilot.PROVIDER, "model": pilot.MODEL,
                  "body_id": screened["body_id"], "source_screen": record["source_screen"],
                  "request_count": 1, "pilot_started": False,
                  "halt_reason": "Gemini smoke source was rejected by the frozen source screen."}
        save_json(run / "SMOKE_RESULT.json", result)
        print(json.dumps(result, indent=2), flush=True)
        raise SystemExit(1)

    diagnostic = json.loads((PILOT / "diagnostic_battery.json").read_text(encoding="utf-8"))
    evaluation = json.loads((PILOT / "evaluation_bank.json").read_text(encoding="utf-8"))
    diag_requests = [{"probe_id": x["probe_id"], "input": x["input"]} for x in diagnostic]
    eval_requests = [{"probe_id": x["hid"], "input": x["input"]} for x in evaluation]
    with tempfile.TemporaryDirectory(prefix="fc-gemini-smoke-") as temp_dir:
        temp = Path(temp_dir)
        runtime = temp / "python"
        shutil.copytree(pipeline.previous.PYTHON_BASE, runtime, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        pipeline.RUN = run
        diag_transport, diag_wall = pipeline.execute_suite(
            temp, f"diagnostic_{attempt_id}", f"diagnostic_{attempt_id}",
            diag_requests, source, runtime)
        diag_rows = [pipeline.outcome(raw, item, source, "diagnostic")
                     for raw, item in zip(diag_transport["probe_rows"], diagnostic, strict=True)]
        eval_transport, eval_wall = pipeline.execute_suite(
            temp, f"evaluation_{attempt_id}", f"evaluation_{attempt_id}",
            eval_requests, source, runtime)
        eval_rows = [pipeline.outcome(raw, item, source, "evaluation")
                     for raw, item in zip(eval_transport["probe_rows"], evaluation, strict=True)]
    diag_pass = sum(row["status"] == "pass" for row in diag_rows)
    eval_correct = sum(row["correct"] for row in eval_rows)
    host = attempt_dir / "host-authoritative"
    host.mkdir()
    save_json(host / "diagnostic.json", {
        "records": diag_rows, "suite_wall_seconds": diag_wall,
    })
    save_json(host / "evaluation.json", {
        "records": eval_rows, "suite_wall_seconds": eval_wall,
    })
    passed = (len(diag_rows) == 30 and diag_pass == 30 and
              len(eval_rows) == 20 and eval_correct == 20)
    record.update({
        "execution_status": "complete",
        "diagnostic_pass_count": diag_pass,
        "evaluation_correct_count": eval_correct,
        "total_50_input_wall_seconds": diag_wall + eval_wall,
    })
    save_json(attempt_dir / "attempt.json", record)
    result = {
        "status": "PASS" if passed else "FAIL",
        "stage": "sandbox_smoke",
        "run": run.name,
        "provider": pilot.PROVIDER,
        "model": pilot.MODEL,
        "endpoint": f"https://{pilot.ENDPOINT_HOST}{pilot.ENDPOINT_PATH}",
        "generation_config": pilot.GENERATION_CONFIG,
        "body_id": screened["body_id"],
        "source_screen": record["source_screen"],
        "diagnostic_pass_count": diag_pass,
        "diagnostic_total": len(diag_rows),
        "evaluation_correct_count": eval_correct,
        "evaluation_total": len(eval_rows),
        "request_count": 1,
        "pilot_started": False,
        "smoke_criteria": "source accepted; 30/30 diagnostic rows complete and pass; 20/20 evaluation rows complete and correct",
        "halt_reason": None if passed else "Gemini smoke did not meet the known-task execution criteria.",
    }
    save_json(run / "SMOKE_RESULT.json", result)
    print(json.dumps(result, indent=2), flush=True)
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
