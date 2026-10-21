"""Host-side reconstruction from the already retained generated-smoke captures."""
from __future__ import annotations

import base64
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PILOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PILOT)); sys.path.insert(0, str(REPO))
from integration_runner import CaptureRejected, parse_worker_scalar, validate_capture_directory
from pilot_tool import body_id, input_id
from study.families import FAMILY_ORDER
from study.features import concentration, family_counts
from study.sssp import dijkstra_ref
from source_policy import screen_source


def reconstruct(raw: dict, item: dict, phase: str) -> dict:
    problem = item["input"]
    ref = dijkstra_ref(problem["n"], [tuple(edge) for edge in problem["edges"]], problem["s"], problem["t"])
    oracle = -1 if ref is None else ref
    parsed = None; error = None; correct = False
    if raw["status"] == "complete" and raw["exit_code"] == 0 and not raw["timed_out"]:
        try:
            parsed = parse_worker_scalar(raw)
            correct = parsed == oracle
        except CaptureRejected as exc:
            error = str(exc)
    else:
        error = raw["status"]
    status = "pass" if correct else "wrong" if parsed is not None else "invalid" if raw["status"] == "complete" else raw["status"]
    return {"phase": phase, "probe_id": item.get("probe_id") or item.get("hid"), "family": item.get("family"),
            "input_id": item.get("input_id") or input_id(problem), "input": problem, "status": status,
            "solver_output": parsed, "oracle_output": oracle, "correct": correct, "error": error,
            "raw_stdout_b64": raw["stdout_b64"], "raw_stderr_b64": raw["stderr_b64"],
            "exit_code": raw["exit_code"], "timed_out": raw["timed_out"],
            "tree_terminated": raw["tree_terminated"], "worker_elapsed_ms": raw.get("elapsed_ms")}


def validated_capture(path: Path, case: str, expected: list[dict]) -> tuple[dict, float]:
    untrusted = json.loads((path / "capture.json").read_text(encoding="utf-8"))
    transport = validate_capture_directory(path, untrusted.get("nonce", ""), case)
    expected_ids = [item.get("probe_id") or item.get("hid") for item in expected]
    if [row["probe_id"] for row in transport["probe_rows"]] != expected_ids:
        raise CaptureRejected(f"capture order/IDs do not match {case}")
    return transport, (path / "capture.json").stat().st_mtime


def main(run_dir: Path) -> None:
    source = (run_dir / "generated-solver.py").read_text(encoding="utf-8")
    screen = screen_source(source)
    if not screen.accepted:
        raise SystemExit("retained generated source no longer passes source policy")
    diagnostic = json.loads((PILOT / "diagnostic_battery.json").read_text(encoding="utf-8"))
    evaluation = json.loads((PILOT / "evaluation_bank.json").read_text(encoding="utf-8"))
    diag_transport, diag_stamp = validated_capture(run_dir / "guest-captures/diagnostic", "diagnostic_smoke", diagnostic)
    eval_transport, eval_stamp = validated_capture(run_dir / "guest-captures/evaluation", "evaluation_smoke", evaluation)
    diag = [reconstruct(raw, item, "diagnostic") for raw, item in zip(diag_transport["probe_rows"], diagnostic, strict=True)]
    evalu = [reconstruct(raw, item, "evaluation") for raw, item in zip(eval_transport["probe_rows"], evaluation, strict=True)]
    counts = family_counts([record["status"] != "pass" for record in diag])
    k, c = concentration([record["status"] != "pass" for record in diag])
    (run_dir / "host-authoritative").mkdir(exist_ok=True)
    (run_dir / "host-authoritative/diagnostic.json").write_text(json.dumps({"rows": diag, "family_counts": counts,
        "family_order": FAMILY_ORDER, "k": k, "C": c}, indent=2) + "\n", encoding="utf-8")
    (run_dir / "host-authoritative/evaluation.json").write_text(json.dumps(evalu, indent=2) + "\n", encoding="utf-8")

    gen_cfg_time = (run_dir / "generation-config.json").stat().st_mtime
    source_time = (run_dir / "generated-solver.py").stat().st_mtime
    # Wall timing is reconstructed from host timestamps retained by the first
    # run; per-worker times come from the captured supervisor records.
    end_to_end = eval_stamp - source_time
    generation = source_time - gen_cfg_time
    worker_times = [float(row.get("elapsed_ms", 0)) for row in diag_transport["probe_rows"] + eval_transport["probe_rows"]]
    report = {"status": "PASS" if len(diag) == 30 and len(evalu) == 20 and all(r["tree_terminated"] for r in diag + evalu) else "HOLD",
        "model_generation_attempts": 0, "separate_generation_smoke_requests": 1, "body_id": body_id(source),
        "diagnostic_rows": len(diag), "evaluation_rows": len(evalu), "family_counts": counts, "k": k, "C": c,
        "evaluation_correct": sum(row["correct"] for row in evalu),
        "generation_wall_seconds_approx": generation,
        "complete_50_input_runner_wall_seconds_approx": end_to_end,
        "diagnostic_capture_wall_from_source_timestamp_seconds": diag_stamp - source_time,
        "evaluation_capture_wall_from_diagnostic_capture_seconds": eval_stamp - diag_stamp,
        "worker_ms_sum": sum(worker_times), "worker_ms_mean": statistics.mean(worker_times),
        "worker_ms_min": min(worker_times), "worker_ms_max": max(worker_times),
        "estimated_100_attempts_hours": 100 * (generation + end_to_end) / 3600,
        "estimate_assumption": "linear repetition of this one CLI request and one 50-input runner; excludes between-attempt variation, retries (none allowed), and external contention",
        "timing_caveat": "Suite wall time is reconstructed from host file timestamps because the first orchestrator crashed during report construction after both complete captures were retained; it includes runner setup before/around the sessions and may omit final Sandbox shutdown after the last capture.",
        "orchestrator_issue": "Initial postprocessing indexed evaluation rows by probe_id although the retained evaluation bank identifies them by hid. Both Sandbox sessions and complete captures had finished; host records were then reconstructed offline from retained raw captures, with no solver re-execution.",
        "source_screen": {"accepted": screen.accepted, "reasons": screen.reasons},
        "full_suite_inputs_visible_inside_guest": True, "reference_oracle_mapped": False,
        "host_recomputed_all_labels_features": True, "model_prompt_included_test_inputs": False}
    (run_dir / "SMOKE_RESULTS.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (run_dir / "SMOKE_REPORT.md").write_text(
        "# Generated solver smoke test\n\n" +
        f"Status: **{report['status']}**\n\n" +
        f"Diagnostic: {len(diag)}/30 rows; family failures {counts}; k={k}; C={c}.\n\n" +
        f"Evaluation: {len(evalu)}/20 rows; correct {report['evaluation_correct']}/20.\n\n" +
        f"Complete 50-input runner wall time (approx., host timestamp reconstruction): {end_to_end:.2f}s.\n\n" +
        f"Per-worker time: mean {report['worker_ms_mean']:.1f}ms; range {report['worker_ms_min']:.0f}–{report['worker_ms_max']:.0f}ms; total {report['worker_ms_sum']:.0f}ms.\n\n" +
        f"Linear estimate for 100 attempts: {report['estimated_100_attempts_hours']:.2f} hours, including one generation request per attempt.\n\n" +
        "This was one generated smoke body, not a pilot attempt and not evidence for concentration prediction. The generated prompt contained no diagnostic or evaluation inputs. Static source screening is a best-effort filter only. The guest could read the full suite mapped for its phase; this is an accepted exploratory limitation. Timing reconstruction is approximate because the smoke orchestrator failed during report construction after retaining both complete suites.\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    default = PILOT / "generation-smoke-2026-10-21"
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else default)
