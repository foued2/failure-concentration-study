"""Run the authorized exploratory pilot; no predictive models are fitted."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
import argparse
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
RUN = PILOT / f"natural-pilot-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def save_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temp, path)


def request_one(attempt_dir: Path, number: int) -> dict:
    response_path = attempt_dir / "generated-response.txt"
    command = ["powershell.exe", "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(pipeline.CODEX_PS),
               "exec", "--ephemeral", "--sandbox", "read-only", "--model", "gpt-6-luna", "--json",
               "--output-last-message", str(response_path), "-C", str(attempt_dir), pipeline.PROMPT]
    started = time.perf_counter()
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=600, cwd=attempt_dir)
        elapsed = time.perf_counter() - started
        (attempt_dir / "generation-events.jsonl").write_text(completed.stdout, encoding="utf-8")
        (attempt_dir / "generation-stderr.txt").write_text(completed.stderr, encoding="utf-8")
        if completed.returncode != 0 or not response_path.is_file():
            return {"status": "generation_failed", "elapsed_seconds": elapsed,
                    "exit_code": completed.returncode, "response_present": response_path.is_file()}
        source = response_path.read_text(encoding="utf-8")
        (attempt_dir / "generated-solver.py").write_text(source, encoding="utf-8")
        screen = screen_source(source)
        screened = {"accepted": screen.accepted, "reasons": screen.reasons,
                    "body_id": body_id(source), "source_bytes": len(source.encode("utf-8"))}
        save_json(attempt_dir / "source-screen.json", screened)
        return {"status": "generated", "elapsed_seconds": elapsed, "exit_code": completed.returncode,
                "source": source, "screen": screened}
    except subprocess.TimeoutExpired as exc:
        (attempt_dir / "generation-stdout-partial.txt").write_bytes(exc.stdout or b"")
        (attempt_dir / "generation-stderr-partial.txt").write_bytes(exc.stderr or b"")
        return {"status": "generation_timeout", "elapsed_seconds": time.perf_counter() - started}


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
    save_json(RUN / "PILOT_RESULTS.json", {"state": state, "attempt_count": len(attempts),
        "attempt_cap": CAP, "generation_requests": len(attempts),
        "model_written_generation_attempts": generated, "generation_failures": generation_failures,
        "distinct_canonical_bodies": len({r["body_id"] for r in attempts if r.get("body_id")}),
        "excluded_or_not_executed": sum(r.get("execution_status") not in {"complete", "duplicate_reused"} for r in attempts),
        "summary": summary, "predictive_model_fitted": False, "halt_reason": halt_reason,
        "population": "Codex CLI 0.160.1, --model gpt-6-luna, one exact SSSP prompt per attempt; backend snapshot unavailable",
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
    args = parser.parse_args()
    if args.resume:
        RUN = args.resume.resolve()
        if not (RUN / "attempts.json").is_file():
            raise FileNotFoundError(RUN / "attempts.json")
    elif RUN.exists():
        raise FileExistsError(RUN)
    if not pipeline.previous.SANDBOX.is_file() or not pipeline.previous.PYTHON_BASE.is_dir() or not pipeline.CODEX_PS.is_file():
        raise RuntimeError("required Codex CLI, Sandbox, or Python runtime unavailable")
    pipeline.previous.check_no_running_sandbox()
    if not args.resume:
        RUN.mkdir()
        (RUN / "prompt.txt").write_text(pipeline.PROMPT + "\n", encoding="utf-8")
        save_json(RUN / "protocol.json", {"date": datetime.now(timezone.utc).isoformat(), "model": "gpt-6-luna",
        "codex_cli_version": "0.160.1", "backend_version": None, "immutable_snapshot": None,
        "attempt_cap": CAP, "evaluation_input_count": 20, "diagnostic_probe_count": 30,
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
        retained = json.loads((RUN / "attempts.json").read_text(encoding="utf-8"))
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
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "generation_elapsed_seconds": generated.get("elapsed_seconds"),
                "generation_status": generated["status"], "execution_status": "not_run",
                "attempt_directory": str(attempt_dir.relative_to(RUN))}
            if generated["status"] != "generated":
                record["exclusion_reason"] = generated["status"]
                attempts.append(record); persist(attempts, "RUNNING"); continue
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
