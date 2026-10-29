"""Run one candidate against sequential inputs in a no-network Docker container.

This host-side controller does not load the candidate or reference answers.
The container receives only one candidate body and one probe input at a time.
All predictions are untrusted and this program performs no scoring.
"""
from __future__ import annotations

import argparse
import ast
import builtins
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import subprocess
import symtable
import sys
import threading
import time
import uuid
from typing import Any

PYTHON_IMAGE = "python:3.14-slim@sha256:cd89c30eda26ee911a4611b18680086e0ea42e6f5f8cbe653d07fa7958c9cec8"
MEMORY_BYTES = 536870912
MAX_PROCESSES = 8
MAX_LINE_BYTES = 128 * 1024
DEFAULT_RESPONSE_TIMEOUT = 12.0
DEFAULT_PROBE_TIMEOUT_SECONDS = 5.0


class ContainerExecutionError(RuntimeError):
    pass


FORBIDDEN_IMPORTS = {
    "os", "subprocess", "socket", "pathlib", "shutil", "importlib",
    "ctypes", "multiprocessing", "threading", "requests", "urllib", "http",
    "ftplib", "telnetlib", "pickle", "marshal",
}
FORBIDDEN_CALLS = {
    "open", "eval", "exec", "compile", "__import__", "input", "breakpoint",
}


def unsafe_reason(source: str) -> str | None:
    """Exact static import/call policy inherited from the frozen V3 gate."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return f"syntax:{exc.msg}"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                    return f"import:{alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                return f"from:{node.module}"
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_CALLS:
                return f"call:{node.func.id}"
    return None


def undefined_global_names(source: str) -> list[str]:
    """Exact conservative undefined-global warning inherited from the V3 gate."""
    try:
        root = symtable.symtable(source, "<candidate>", "exec")
    except SyntaxError:
        return []
    module_bound = {
        symbol.get_name()
        for symbol in root.get_symbols()
        if symbol.is_assigned() or symbol.is_imported() or symbol.is_namespace()
    }
    runtime_names = {
        "__name__", "__package__", "__spec__", "__builtins__", "__doc__",
        "__loader__", "__file__", "__cached__", "__annotations__",
    }
    allowed = set(dir(builtins)) | runtime_names
    missing: set[str] = set()

    def visit(table) -> None:
        if table.get_type() != "module":
            for symbol in table.get_symbols():
                name = symbol.get_name()
                if symbol.is_referenced() and symbol.is_global() and name not in module_bound and name not in allowed:
                    missing.add(name)
        for child in table.get_children():
            visit(child)

    visit(root)
    return sorted(missing)


def _static_exclusion_report(body: Path, probes: list[dict], timeout: float,
                             reason: str, *, static_checks_enforced: bool = True) -> dict:
    return {
        "version": 1,
        "candidate_sha256": _sha256(body),
        "image": PYTHON_IMAGE,
        "container_config": None,
        "probe_count": 0,
        "expected_probe_count": len(probes),
        "probe_payload_sha256": _probe_payload_sha256(probes),
        "probe_ids": [probe.get("probe_id") for probe in probes],
        "probe_timeout_seconds": timeout,
        "preflight": None,
        "candidate_valid": False,
        "candidate_status": "static_rejection" if static_checks_enforced else "test_fixture",
        "candidate_load_error_type": None,
        "candidate_exclusion_reason": reason,
        "results": [],
        "all_trees_empty": True,
        "execution_performed": False,
        "candidate_generation_performed": False,
        "scoring_performed": False,
        "reference_answers_present": False,
        "host_repository_mounted": False,
        "api_keys_passed_to_container": False,
        "static_checks_enforced": static_checks_enforced,
        "isolation_harness_ok": None,
    }


def _probe_payload_sha256(probes: list[dict]) -> str:
    canonical = json.dumps(probes, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _regular_file(path: Path, name: str) -> Path:
    if path.is_symlink() or not path.is_file():
        raise ContainerExecutionError(f"{name} must be a regular, non-symlink file")
    return path.resolve(strict=True)


def _docker(args: list[str], *, timeout: float = 30.0) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", *args], capture_output=True, text=True, timeout=timeout,
        encoding="utf-8", errors="replace", check=False,
    )


def _inspect_container(container_id: str, body: Path, supervisor: Path, child: Path) -> dict:
    proc = _docker(["inspect", container_id])
    if proc.returncode != 0:
        raise ContainerExecutionError("docker inspect failed")
    try:
        record = json.loads(proc.stdout)[0]
    except (json.JSONDecodeError, IndexError, TypeError):
        raise ContainerExecutionError("docker inspect returned invalid JSON") from None
    host = record.get("HostConfig") or {}
    checks = {
        "network_none": host.get("NetworkMode") == "none",
        "read_only_root": host.get("ReadonlyRootfs") is True,
        "pid_cap": host.get("PidsLimit") == MAX_PROCESSES,
        "memory_cap": host.get("Memory") == MEMORY_BYTES,
        "memory_swap_cap": host.get("MemorySwap") == MEMORY_BYTES,
        "cpu_cap": host.get("NanoCpus") == 1_000_000_000
                   or (host.get("CpuQuota") == 100_000 and host.get("CpuPeriod") == 100_000),
        "capabilities_dropped": "ALL" in (host.get("CapDrop") or []),
        "supervisor_capabilities_minimal": {
            str(cap).upper().removeprefix("CAP_") for cap in (host.get("CapAdd") or [])
        } == {"CHOWN", "SETUID", "SETGID", "KILL"},
        "no_new_privileges": "no-new-privileges" in (host.get("SecurityOpt") or []),
        "root_uid_for_supervisor_only": (record.get("Config") or {}).get("User") in {"0:0", "0"},
        "pinned_image": (record.get("Config") or {}).get("Image") == PYTHON_IMAGE,
        "tmpfs_paths_only_expected": set(host.get("Tmpfs") or {}) == {"/tmp", "/dev/shm"},
        "tmpfs_present": "/tmp" in (host.get("Tmpfs") or {})
                         and "rw" in host["Tmpfs"]["/tmp"]
                         and "noexec" in host["Tmpfs"]["/tmp"]
                         and "nosuid" in host["Tmpfs"]["/tmp"],
        "dev_shm_read_only": "/dev/shm" in (host.get("Tmpfs") or {})
                         and "ro" in host["Tmpfs"]["/dev/shm"]
                         and "noexec" in host["Tmpfs"]["/dev/shm"]
                         and "nosuid" in host["Tmpfs"]["/dev/shm"],
    }
    mounts = {m.get("Destination"): m for m in (record.get("Mounts") or [])}
    expected = {
        "/candidate/body.py": (str(body), True),
        "/trusted/isolated_supervisor.py": (str(supervisor), True),
        "/trusted/candidate_child.py": (str(child), True),
    }
    for target, (source, readonly) in expected.items():
        m = mounts.get(target)
        checks[f"mount_{target}_present"] = bool(m)
        checks[f"mount_{target}_source"] = bool(m and Path(m.get("Source", "")).resolve() == Path(source).resolve())
        checks[f"mount_{target}_readonly"] = bool(m and m.get("RW") is (not readonly))
    checks["no_unexpected_mounts"] = set(mounts) == set(expected)
    violations = [key for key, ok in checks.items() if not ok]
    if violations:
        # These fields contain configuration only, not credentials or candidate output.
        diagnostic = {
            "cap_add": host.get("CapAdd"),
            "cap_drop": host.get("CapDrop"),
            "tmpfs": host.get("Tmpfs"),
            "mount_targets": sorted(mounts),
        }
        raise ContainerExecutionError(
            "container isolation configuration rejected: "
            + ",".join(violations)
            + "; observed="
            + json.dumps(diagnostic, sort_keys=True)
        )
    return {"checks": checks, "verified": True, "image": PYTHON_IMAGE}


def _read_line(stream, pending: bytearray, timeout: float) -> bytes:
    deadline = time.monotonic() + timeout
    while True:
        index = pending.find(b"\n")
        if index >= 0:
            line = bytes(pending[:index])
            del pending[:index + 1]
            return line
        if len(pending) > MAX_LINE_BYTES:
            raise ContainerExecutionError("supervisor output line exceeded byte cap")
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("supervisor response timeout")
        ready, _, _ = __import__("select").select([stream], [], [], remaining)
        if not ready:
            raise TimeoutError("supervisor response timeout")
        chunk = os.read(stream.fileno(), 4096)
        if not chunk:
            raise ContainerExecutionError("supervisor closed output before replying")
        pending.extend(chunk)


def _preflight_payload(probe: dict) -> dict:
    """Create an answer-free import/callability check using one valid input shape."""
    required = ("n", "edges", "s", "t")
    if any(key not in probe for key in required):
        raise ValueError("each probe must contain n, edges, s, and t")
    return {
        "probe_id": "__h3_preflight__",
        "phase": "preflight",
        "n": probe["n"],
        "edges": probe["edges"],
        "s": probe["s"],
        "t": probe["t"],
    }


def _preflight_state(record: dict) -> tuple[bool, str, str | None]:
    """Classify module preflight separately from any probe's outcome."""
    if record.get("phase") != "preflight":
        return False, "preflight_protocol_error", None
    if record.get("status") == "ok" and record.get("answer_type") == "callable" and record.get("answer") is None:
        if record.get("solver_output_overflow") is True:
            return False, "preflight_output_overflow", None
        return True, "valid", None
    status = record.get("status")
    if status == "load_error":
        return False, "load_error", str(record.get("error_type") or "unknown")
    if status == "timeout":
        return False, "preflight_timeout", None
    if status == "exception":
        return False, "preflight_exception", str(record.get("error_type") or "unknown")
    if status == "output_overflow":
        return False, "preflight_output_overflow", None
    return False, "preflight_failed", str(status or "unknown")


def run_candidate(
    body_path: Path,
    trusted_dir: Path,
    probes: list[dict],
    *,
    response_timeout: float = DEFAULT_RESPONSE_TIMEOUT,
    probe_timeout: float = DEFAULT_PROBE_TIMEOUT_SECONDS,
    enforce_static: bool = True,
) -> dict:
    body = _regular_file(Path(body_path), "candidate body")
    trusted_dir = Path(trusted_dir).resolve(strict=True)
    supervisor = _regular_file(trusted_dir / "isolated_supervisor.py", "trusted supervisor")
    child = _regular_file(trusted_dir / "candidate_child.py", "trusted child runner")
    if not probes:
        raise ValueError("at least one probe input is required")
    if not 1 <= response_timeout <= 120:
        raise ValueError("response_timeout must be between 1 and 120 seconds")
    if not 0.2 <= probe_timeout <= 30:
        raise ValueError("probe_timeout must be between 0.2 and 30 seconds")
    probe_ids = [p.get("probe_id") for p in probes if isinstance(p, dict)]
    if len(probe_ids) != len(probes) or any(not isinstance(pid, str) or not pid for pid in probe_ids):
        raise ValueError("every probe must be an object with a non-empty probe_id")
    if len(set(probe_ids)) != len(probe_ids):
        raise ValueError("probe_id values must be unique")

    if enforce_static:
        try:
            candidate_source = body.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return _static_exclusion_report(body, probes, probe_timeout, "encoding:invalid_utf8")
        static_reason = unsafe_reason(candidate_source)
        if static_reason:
            return _static_exclusion_report(body, probes, probe_timeout, static_reason)
        missing = undefined_global_names(candidate_source)
        if missing:
            return _static_exclusion_report(body, probes, probe_timeout, "undefined_name:" + ",".join(missing))

    pull = _docker(["pull", PYTHON_IMAGE], timeout=180.0)
    if pull.returncode != 0:
        raise ContainerExecutionError("pinned Python image could not be pulled")

    container_name = "h3v10-" + uuid.uuid4().hex[:20]
    mounts = [
        f"type=bind,source={body},target=/candidate/body.py,readonly",
        f"type=bind,source={supervisor},target=/trusted/isolated_supervisor.py,readonly",
        f"type=bind,source={child},target=/trusted/candidate_child.py,readonly",
    ]
    cmd = [
        "create", "--interactive", "--name", container_name,
        "--network", "none", "--read-only", "--pids-limit", str(MAX_PROCESSES),
        "--memory", str(MEMORY_BYTES), "--memory-swap", str(MEMORY_BYTES),
        "--cpus", "1", "--user", "0:0",
        "--cap-drop", "ALL", "--cap-add", "CHOWN", "--cap-add", "SETUID", "--cap-add", "SETGID", "--cap-add", "KILL",
        "--security-opt", "no-new-privileges",
        "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m,mode=0711",
        "--tmpfs", "/dev/shm:ro,noexec,nosuid,size=16m",
        "--ulimit", "nofile=32:32",
    ]
    for mount in mounts:
        cmd.extend(["--mount", mount])
    cmd.extend(["--entrypoint", "python", PYTHON_IMAGE, "-I", "/trusted/isolated_supervisor.py", "--probe-timeout", str(probe_timeout)])
    created = _docker(cmd, timeout=30)
    if created.returncode != 0 or not created.stdout.strip():
        raise ContainerExecutionError("docker create failed")
    container_id = created.stdout.strip().splitlines()[-1]
    start = None
    stderr_tail = bytearray()
    stderr_thread = None
    results = []
    fatal = False
    container_config = None
    candidate_hash = _sha256(body)
    try:
        container_config = _inspect_container(container_id, body, supervisor, child)
        start = subprocess.Popen(
            ["docker", "start", "-ai", container_id],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            bufsize=0,
        )

        def drain_stderr():
            while True:
                chunk = start.stderr.read(4096)
                if not chunk:
                    break
                if len(stderr_tail) < 8192:
                    stderr_tail.extend(chunk[:8192 - len(stderr_tail)])

        stderr_thread = threading.Thread(target=drain_stderr, daemon=True)
        stderr_thread.start()
        pending = bytearray()

        # Preflight loads the candidate module and verifies solve() is callable,
        # without invoking solve or exposing expected answers. A load failure
        # invalidates the candidate and receives no k; it is not 30 probe failures.
        preflight_payload = _preflight_payload(probes[0])
        preflight_bytes = json.dumps(preflight_payload, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        if len(preflight_bytes) > MAX_LINE_BYTES:
            raise ContainerExecutionError("preflight input exceeds byte cap")
        start.stdin.write(preflight_bytes)
        start.stdin.flush()
        preflight_line = _read_line(start.stdout, pending, response_timeout)
        try:
            preflight_record = json.loads(preflight_line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ContainerExecutionError("supervisor preflight output was not JSON") from None
        if not isinstance(preflight_record, dict) or preflight_record.get("v") != 1:
            raise ContainerExecutionError("invalid supervisor preflight schema")
        if preflight_record.get("sequence") != 1 or preflight_record.get("probe_id") != "__h3_preflight__":
            raise ContainerExecutionError("supervisor preflight response is not bound to request")
        if preflight_record.get("phase") != "preflight":
            raise ContainerExecutionError("supervisor response phase mismatch during preflight")
        if preflight_record.get("tree_empty") is not True:
            fatal = True
            raise ContainerExecutionError("process tree did not empty after candidate preflight")
        if preflight_record.get("status") == "tree_cleanup_failed" or preflight_record.get("fatal"):
            fatal = True
            raise ContainerExecutionError("supervisor cleanup failed after candidate preflight")

        candidate_valid, candidate_status, candidate_load_error_type = _preflight_state(preflight_record)
        if candidate_valid:
            for sequence, probe in enumerate(probes, start=1):
                payload = json.dumps(probe, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
                if len(payload) > MAX_LINE_BYTES:
                    raise ContainerExecutionError(f"probe input {sequence} exceeds the byte cap")
                if start.poll() is not None:
                    raise ContainerExecutionError(f"container exited before probe {sequence}")
                start.stdin.write(payload)
                start.stdin.flush()
                line = _read_line(start.stdout, pending, response_timeout)
                try:
                    record = json.loads(line.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    raise ContainerExecutionError(f"supervisor output for probe {sequence} was not JSON") from None
                if not isinstance(record, dict) or record.get("v") != 1:
                    raise ContainerExecutionError(f"invalid supervisor response schema at probe {sequence}")
                if record.get("sequence") != sequence + 1 or record.get("probe_id") != probe["probe_id"]:
                    raise ContainerExecutionError(f"supervisor response is not bound to probe {sequence}")
                if record.get("phase") != "probe":
                    raise ContainerExecutionError(f"supervisor response phase mismatch at probe {sequence}")
                if record.get("tree_empty") is not True:
                    fatal = True
                    raise ContainerExecutionError(f"process tree did not empty after probe {sequence}")
                if record.get("status") == "tree_cleanup_failed" or record.get("fatal"):
                    fatal = True
                    raise ContainerExecutionError(f"supervisor cleanup failed after probe {sequence}")
                record["probe_index"] = sequence
                results.append(record)

        start.stdin.close()
        try:
            exit_code = start.wait(timeout=10)
        except subprocess.TimeoutExpired:
            fatal = True
            raise ContainerExecutionError("container supervisor did not exit after input EOF") from None
        if exit_code != 0:
            fatal = True
            raise ContainerExecutionError(f"container supervisor exit code {exit_code}")
        if stderr_thread:
            stderr_thread.join(timeout=1)
    except BaseException:
        if start and start.poll() is None:
            try:
                _docker(["kill", container_id], timeout=10)
            except Exception:
                pass
            try:
                start.kill()
            except OSError:
                pass
            try:
                start.wait(timeout=2)
            except Exception:
                pass
        raise
    finally:
        cleanup = _docker(["rm", "-f", container_id], timeout=20)
        if cleanup.returncode != 0 and "no such container" not in cleanup.stderr.lower():
            raise ContainerExecutionError("Docker failed to remove the candidate container")

    return {
        "version": 1,
        "candidate_sha256": candidate_hash,
        "image": PYTHON_IMAGE,
        "container_config": container_config,
        "probe_count": len(results),
        "expected_probe_count": len(probes),
        "probe_payload_sha256": _probe_payload_sha256(probes),
        "probe_ids": [probe["probe_id"] for probe in probes],
        "probe_timeout_seconds": probe_timeout,
        "preflight": preflight_record,
        "candidate_valid": candidate_valid,
        "candidate_status": candidate_status,
        "candidate_load_error_type": candidate_load_error_type,
        "candidate_exclusion_reason": None,
        "execution_performed": True,
        "static_checks_enforced": enforce_static,
        "results": results,
        "all_trees_empty": preflight_record.get("tree_empty") is True and all(r.get("tree_empty") is True for r in results),
        "candidate_generation_performed": False,
        "scoring_performed": False,
        "reference_answers_present": False,
        "host_repository_mounted": False,
        "api_keys_passed_to_container": False,
        "container_stderr_tail": bytes(stderr_tail).decode("utf-8", "replace"),
        "isolation_harness_ok": (
            not fatal
            and preflight_record.get("tree_empty") is True
            and ((candidate_valid and len(results) == len(probes)) or (not candidate_valid and len(results) == 0))
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--body", required=True)
    parser.add_argument("--trusted-dir", required=True)
    parser.add_argument("--probes-json", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--response-timeout", type=float, default=DEFAULT_RESPONSE_TIMEOUT)
    parser.add_argument("--probe-timeout", type=float, default=DEFAULT_PROBE_TIMEOUT_SECONDS)
    args = parser.parse_args()
    try:
        probe_data = json.loads(Path(args.probes_json).read_text(encoding="utf-8"))
        if not isinstance(probe_data, list):
            raise ValueError("probes-json must contain an array")
        report = run_candidate(
            Path(args.body), Path(args.trusted_dir), probe_data,
            response_timeout=args.response_timeout,
            probe_timeout=args.probe_timeout,
        )
        report_path = Path(args.out)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({
            "isolation_harness_ok": report["isolation_harness_ok"],
            "probe_count": report["probe_count"],
            "expected_probe_count": report["expected_probe_count"],
            "candidate_valid": report["candidate_valid"],
            "candidate_status": report["candidate_status"],
            "candidate_exclusion_reason": report.get("candidate_exclusion_reason"),
            "execution_performed": report.get("execution_performed"),
            "statuses": [r.get("status") for r in report["results"]],
            "all_trees_empty": report["all_trees_empty"],
            "report": str(report_path),
        }, sort_keys=True))
        return 2 if report["isolation_harness_ok"] is False else 0
    except (ContainerExecutionError, ValueError, OSError, subprocess.SubprocessError) as exc:
        message = f"{type(exc).__name__}: {exc}"
        print(json.dumps({"isolation_harness_ok": False, "error": message}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
