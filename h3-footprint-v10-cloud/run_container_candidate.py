"""Run one candidate against sequential inputs in a no-network Docker container.

This host-side controller does not load the candidate or reference answers.
The container receives only one candidate body and one probe input at a time.
All predictions are untrusted and this program performs no scoring.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import selectors
import subprocess
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
        "supervisor_capabilities_minimal": set(host.get("CapAdd") or []) == {"CHOWN", "SETUID", "SETGID", "KILL"},
        "no_new_privileges": "no-new-privileges" in (host.get("SecurityOpt") or []),
        "root_uid_for_supervisor_only": (record.get("Config") or {}).get("User") in {"0:0", "0"},
        "pinned_image": (record.get("Config") or {}).get("Image") == PYTHON_IMAGE,
        "tmpfs_present": "/tmp" in (host.get("Tmpfs") or {})
                         and "noexec" in host["Tmpfs"]["/tmp"]
                         and "nosuid" in host["Tmpfs"]["/tmp"],
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
        checks[f"mount_{target}_source"] = bool(m and Path(m.get("Source", "")).resolve() == Path(source))
        checks[f"mount_{target}_readonly"] = bool(m and m.get("RW") is (not readonly))
    checks["no_unexpected_mounts"] = set(mounts) == set(expected)
    violations = [key for key, ok in checks.items() if not ok]
    if violations:
        raise ContainerExecutionError("container isolation configuration rejected: " + ",".join(violations))
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


def run_candidate(
    body_path: Path,
    trusted_dir: Path,
    probes: list[dict],
    *,
    response_timeout: float = DEFAULT_RESPONSE_TIMEOUT,
    probe_timeout: float = DEFAULT_PROBE_TIMEOUT_SECONDS,
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
            if record.get("sequence") != sequence or record.get("probe_id") != probe["probe_id"]:
                raise ContainerExecutionError(f"supervisor response is not bound to probe {sequence}")
            if record.get("tree_empty") is not True:
                fatal = True
                raise ContainerExecutionError(f"process tree did not empty after probe {sequence}")
            if record.get("status") == "tree_cleanup_failed" or record.get("fatal"):
                fatal = True
                raise ContainerExecutionError(f"supervisor cleanup failed after probe {sequence}")
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
        _docker(["rm", "-f", container_id], timeout=20)

    return {
        "version": 1,
        "candidate_sha256": candidate_hash,
        "image": PYTHON_IMAGE,
        "container_config": container_config,
        "probe_count": len(probes),
        "probe_timeout_seconds": probe_timeout,
        "results": results,
        "all_trees_empty": all(r.get("tree_empty") is True for r in results),
        "candidate_generation_performed": False,
        "scoring_performed": False,
        "reference_answers_present": False,
        "host_repository_mounted": False,
        "api_keys_passed_to_container": False,
        "container_stderr_tail": bytes(stderr_tail).decode("utf-8", "replace"),
        "isolation_harness_ok": not fatal and len(results) == len(probes),
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
            "statuses": [r.get("status") for r in report["results"]],
            "all_trees_empty": report["all_trees_empty"],
            "report": str(report_path),
        }, sort_keys=True))
        return 0 if report["isolation_harness_ok"] else 2
    except (ContainerExecutionError, ValueError, OSError, subprocess.SubprocessError) as exc:
        message = f"{type(exc).__name__}: {exc}"
        print(json.dumps({"isolation_harness_ok": False, "error": message}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
