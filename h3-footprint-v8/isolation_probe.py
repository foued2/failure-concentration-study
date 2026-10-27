from __future__ import annotations

import argparse
import json
import socket
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_gate  # noqa: E402

ATEXIT_FAKE = '''import atexit
import sys

def solve(n, edges, s, t):
    return -999

atexit.register(lambda: print(sys.argv[-1] + ' {"phase":"probe","probe_index":0,"answer":0}'))
'''
WRONG_SOLVER = 'def solve(n, edges, s, t):\n    return -999\n'


def _io_open_source(*paths: Path) -> str:
    lines = ["import io", "", "def solve(n, edges, s, t):"]
    for path in paths:
        lines.append(f"    for mode in ('a', 'w'):")
        lines.append(f"        try:")
        lines.append(f"            fh = io.open({str(path)!r}, mode)")
        lines.append("            fh.write('tampered')")
        lines.append("            fh.close()")
        lines.append("        except BaseException:")
        lines.append("            pass")
    lines.append("    return -999")
    return "\n".join(lines) + "\n"


def _lock_removal_source(output_root: Path, user: str, *paths: Path) -> str:
    commands = [
        f'icacls "{output_root}" /remove:d {user} /T',
        f'icacls "{output_root}" /grant {user}:(OI)(CI)F /T',
        f'icacls "{output_root}" /reset /T',
        f'takeown /f "{output_root}" /r /d y',
        f'icacls "{output_root}" /setintegritylevel (OI)(CI)Low /T',
    ]
    lines = [
        "import io",
        "import sys",
        "",
        "def solve(n, edges, s, t):",
        '    os_module = sys.modules.get("os")',
        "    if os_module is not None:",
        "        for command in (",
    ]
    for command in commands:
        lines.append(f"            {command!r},")
    lines.extend([
        "        ):",
        "            try:",
        "                os_module.system(command + ' >nul 2>&1')",
        "            except BaseException:",
        "                pass",
    ])
    for path in paths:
        lines.extend([
            "    for mode in ('a', 'w'):",
            "        try:",
            f"            fh = io.open({str(path)!r}, mode)",
            "            fh.write('tampered')",
            "            fh.close()",
            "        except BaseException:",
            "            pass",
        ])
    lines.append("    return -999")
    return "\n".join(lines) + "\n"


def _try_open_for_append(path: Path) -> tuple[bool, str | None]:
    try:
        with path.open("ab"):
            pass
        return True, None
    except BaseException as exc:
        return False, f"{type(exc).__name__}: {exc}"


def _network_check() -> tuple[bool, str]:
    errors = []
    for host, port in (("1.1.1.1", 443), ("8.8.8.8", 53)):
        try:
            sock = socket.create_connection((host, port), timeout=3)
            sock.close()
            return False, f"connected to {host}:{port}"
        except OSError as exc:
            errors.append(f"{host}:{port} {type(exc).__name__}")
    return True, "; ".join(errors)


def _control_row(source: str, name: str) -> dict:
    with tempfile.TemporaryDirectory() as td:
        body = Path(td) / (name + ".py")
        body.write_text(source, encoding="utf-8")
        meta = {body.stem: {"group_id": "isolation-control"}}
        return run_gate.evaluate_body(
            body, meta, expected=run_gate._load_expected(), scratch_dir=Path(td) / "scratch"
        )


def _control_checks() -> tuple[bool, bool, dict]:
    extra_row = _control_row(ATEXIT_FAKE, "atexit_fake")
    wrong_row = _control_row(WRONG_SOLVER, "wrong_solver")
    extra_rejected = extra_row.get("excluded") in ("preflight_invalid_output", "probe_invalid_output")
    wrong_is_k30 = wrong_row.get("excluded") is None and wrong_row.get("k") == 30
    detail = {
        "extra_output_row_excluded": extra_row.get("excluded"),
        "wrong_solver_k": wrong_row.get("k"),
        "wrong_solver_excluded": wrong_row.get("excluded"),
    }
    return extra_rejected, wrong_is_k30, detail


def _output_lock_checks(output_root: Path) -> tuple[bool, bool, bool, bool, dict]:
    canary_dir = Path(tempfile.mkdtemp(prefix="h3-output-canary-", dir=str(output_root)))
    report_canary = canary_dir / "isolation-report.json"
    result_canary = canary_dir / "footprint.json"
    report_canary.write_text("trusted-report", encoding="utf-8")
    result_canary.write_text("trusted-result", encoding="utf-8")
    lock = run_gate.lock_output(Path(output_root))
    if not lock["ok"]:
        run_gate.unlock_output(Path(output_root))
        return False, False, False, False, {"lock_ok": False, "lock_errors": lock["errors"]}
    try:
        direct_report_ok, direct_report_error = _try_open_for_append(report_canary)
        direct_result_ok, direct_result_error = _try_open_for_append(result_canary)
        row = _control_row(_io_open_source(report_canary, result_canary), "io_open_output")
        report_changed = report_canary.read_text(encoding="utf-8") != "trusted-report"
        result_changed = result_canary.read_text(encoding="utf-8") != "trusted-result"
        output_blocked = (
            not direct_report_ok and not direct_result_ok and not report_changed and not result_changed
        )
        candidate_blocked = row.get("excluded") is None and row.get("k") == 30 and output_blocked

        user = run_gate.current_user()
        attack = _control_row(
            _lock_removal_source(Path(output_root), user, report_canary, result_canary),
            "lock_removal",
        )
        direct_after_ok, direct_after_error = _try_open_for_append(report_canary)
        report_changed_after = report_canary.read_text(encoding="utf-8") != "trusted-report"
        result_changed_after = result_canary.read_text(encoding="utf-8") != "trusted-result"
        removal_blocked = (
            not direct_after_ok and not report_changed_after and not result_changed_after
        )
        candidate_removal_blocked = (
            attack.get("excluded") is None and attack.get("k") == 30 and removal_blocked
        )
        detail = {
            "lock_ok": True,
            "direct_report_write_error": direct_report_error,
            "direct_result_write_error": direct_result_error,
            "report_canary_changed": report_changed,
            "result_canary_changed": result_changed,
            "io_open_candidate_k": row.get("k"),
            "io_open_candidate_excluded": row.get("excluded"),
            "direct_after_attack_write_error": direct_after_error,
            "report_canary_changed_after_attack": report_changed_after,
            "result_canary_changed_after_attack": result_changed_after,
            "lock_removal_candidate_k": attack.get("k"),
            "lock_removal_candidate_excluded": attack.get("excluded"),
        }
        return output_blocked, candidate_blocked, removal_blocked, candidate_removal_blocked, detail
    finally:
        run_gate.unlock_output(Path(output_root))
        try:
            report_canary.unlink()
            result_canary.unlink()
            canary_dir.rmdir()
        except OSError:
            pass


def build_report(args: argparse.Namespace) -> dict:
    harness = Path(args.harness_root)
    host_write_ok, host_write_error = _try_open_for_append(Path(args.host_write_target))
    network_blocked, network_detail = _network_check()
    expected_path = harness / "expected_values.json"
    expected_exists = expected_path.exists()
    expected_ok, expected_error = _try_open_for_append(expected_path)
    fixture = harness / "isolation" / "fixtures" / "other_candidate.py"
    fixture_exists = fixture.exists()
    other_ok, other_error = _try_open_for_append(fixture)
    extra_rejected, wrong_is_k30, control_detail = _control_checks()
    output_blocked, candidate_output_blocked, removal_blocked, candidate_removal_blocked, output_detail = (
        _output_lock_checks(Path(args.output_root))
    )
    repo_path = Path(args.repo_path)
    repo_exposed = (repo_path / ".git").exists() or (repo_path / "run_gate.py").exists()
    marker = Path(args.sandbox_marker)
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "python": sys.version,
        "harness_root": str(harness),
        "host_write_target": args.host_write_target,
        "repo_path": args.repo_path,
        "sandbox_marker": args.sandbox_marker,
        "evaluator_inside_sandbox": marker.exists(),
        "network_blocked": network_blocked,
        "host_write_blocked": not host_write_ok,
        "expected_values_write_blocked": expected_exists and not expected_ok,
        "other_candidate_write_blocked": fixture_exists and not other_ok,
        "output_write_blocked": output_blocked,
        "candidate_output_write_blocked": candidate_output_blocked,
        "output_lock_removal_blocked": removal_blocked,
        "candidate_output_lock_removal_blocked": candidate_removal_blocked,
        "extra_output_rejected": extra_rejected,
        "correct_result_after_tamper_attempts": wrong_is_k30,
        "repo_not_present": not repo_exposed,
        "detail": {
            "network": network_detail,
            "host_write_error": host_write_error,
            "expected_values_exists": expected_exists,
            "expected_values_write_error": expected_error,
            "other_candidate_exists": fixture_exists,
            "other_candidate_write_error": other_error,
            "output_root": args.output_root,
            "output_lock": output_detail,
            **control_detail,
        },
    }
    report["ok"] = all(report[name] is True for name in run_gate.REQUIRED_ISOLATION_CHECKS)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness-root", default=str(HERE))
    parser.add_argument("--host-write-target", required=True)
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--sandbox-marker", required=True)
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--out", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        extra_rejected, wrong_is_k30, detail = _control_checks()
        with tempfile.TemporaryDirectory() as td:
            output_blocked, candidate_output_blocked, removal_blocked, candidate_removal_blocked, output_detail = (
                _output_lock_checks(Path(td))
            )
        print(json.dumps({
            "extra_output_rejected": extra_rejected,
            "correct_result_after_tamper_attempts": wrong_is_k30,
            "output_write_blocked": output_blocked,
            "candidate_output_write_blocked": candidate_output_blocked,
            "output_lock_removal_blocked": removal_blocked,
            "candidate_output_lock_removal_blocked": candidate_removal_blocked,
            "detail": detail,
            "output_detail": output_detail,
        }, indent=2, sort_keys=True))
        ok = (
            extra_rejected and wrong_is_k30 and output_blocked
            and candidate_output_blocked and removal_blocked and candidate_removal_blocked
        )
        raise SystemExit(0 if ok else 1)

    if not args.output_root:
        parser.error("--output-root is required outside --self-test")
    report = build_report(args)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
