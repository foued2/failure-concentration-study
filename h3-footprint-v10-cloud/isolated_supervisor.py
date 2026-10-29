"""Container-local supervisor for one-candidate, one-probe-at-a-time execution.

Run as container PID 1 with only SETUID, SETGID and KILL capabilities. Each
solver invocation runs as UID/GID 65534, in a fresh process and private tmpdir.
The supervisor is deliberately blind to reference answers and never scores.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import sys
import time
import uuid

CHILD = "/trusted/candidate_child.py"
MAX_LINE_BYTES = 64 * 1024
MAX_CHILD_OUTPUT_BYTES = 64 * 1024
DEFAULT_TIMEOUT_SECONDS = 5.0
UID = 65534
GID = 65534


def _other_pids() -> list[int]:
    own = os.getpid()
    found = []
    try:
        entries = os.listdir("/proc")
    except OSError:
        return [-1]
    for entry in entries:
        if not entry.isdigit():
            continue
        pid = int(entry)
        if pid != own:
            found.append(pid)
    return found


def _reap_children() -> None:
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
        except (ChildProcessError, OSError):
            return
        if pid <= 0:
            return


def _kill_other_processes(timeout: float = 1.0) -> bool:
    """Kill all container processes except this supervisor and reap descendants."""
    deadline = time.monotonic() + timeout
    while True:
        pids = _other_pids()
        for pid in pids:
            if pid <= 0:
                continue
            try:
                os.kill(pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                pass
        _reap_children()
        remaining = _other_pids()
        if not remaining:
            return True
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.02)


def _clear_tmp() -> None:
    root = Path("/tmp")
    root.mkdir(mode=0o711, parents=True, exist_ok=True)
    os.chmod(root, 0o711)
    for item in root.iterdir():
        try:
            if item.is_symlink() or item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        except FileNotFoundError:
            pass


def _drop_child_privileges() -> None:
    import resource

    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CPU, (8, 9))
    resource.setrlimit(resource.RLIMIT_AS, (384 * 1024 * 1024, 384 * 1024 * 1024))
    os.setgroups([])
    os.setgid(GID)
    os.setuid(UID)


def _read_child(proc: subprocess.Popen, timeout: float) -> dict:
    started = time.monotonic()
    deadline = started + timeout
    streams = {}
    selector = selectors.DefaultSelector()
    for name, stream in (("stdout", proc.stdout), ("stderr", proc.stderr)):
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ, name)
        streams[name] = bytearray()
    overflow = False
    timed_out = False

    while selector.get_map() or proc.poll() is None:
        now = time.monotonic()
        if not timed_out and now >= deadline:
            timed_out = True
            _kill_other_processes()
            try:
                proc.wait(timeout=0.2)
            except subprocess.TimeoutExpired:
                try:
                    proc.kill()
                except OSError:
                    pass
        for key, _ in selector.select(0.025):
            name = key.data
            try:
                chunk = os.read(key.fileobj.fileno(), 4096)
            except BlockingIOError:
                continue
            if not chunk:
                selector.unregister(key.fileobj)
                continue
            current = streams[name]
            if len(current) + len(chunk) > MAX_CHILD_OUTPUT_BYTES:
                overflow = True
                available = max(0, MAX_CHILD_OUTPUT_BYTES - len(current))
                if available:
                    current.extend(chunk[:available])
                if not timed_out:
                    _kill_other_processes()
                    try:
                        proc.wait(timeout=0.2)
                    except subprocess.TimeoutExpired:
                        try:
                            proc.kill()
                        except OSError:
                            pass
                timed_out = False
            elif not overflow:
                current.extend(chunk)
        if proc.poll() is not None and not selector.get_map():
            break

    try:
        return_code = proc.wait(timeout=0.5)
    except subprocess.TimeoutExpired:
        try:
            proc.kill()
        except OSError:
            pass
        return_code = proc.wait(timeout=0.5)

    stdout = bytes(streams["stdout"])
    stderr = bytes(streams["stderr"])
    result = {
        "timed_out": timed_out,
        "output_overflow": overflow,
        "return_code": return_code,
        "stdout_bytes": len(stdout),
        "stderr_bytes": len(stderr),
        "stdout": stdout.decode("utf-8", "replace"),
        "stderr_sha256": __import__("hashlib").sha256(stderr).hexdigest(),
        "elapsed_seconds": round(time.monotonic() - started, 4),
    }
    selector.close()
    return result


def _parse_prediction(stdout: str, probe_id: str) -> dict | None:
    records = []
    for line in stdout.splitlines():
        if line.startswith("H3PRED "):
            try:
                value = json.loads(line[len("H3PRED "):])
            except json.JSONDecodeError:
                return None
            if isinstance(value, dict):
                records.append(value)
    if len(records) != 1:
        return None
    item = records[0]
    if item.get("v") != 1 or item.get("probe_id") != probe_id:
        return None
    if item.get("status") not in {"ok", "exception", "invalid_input"}:
        return None
    if item.get("status") == "ok":
        if item.get("answer_type") == "int":
            if type(item.get("answer")) is not int:
                return None
        elif item.get("answer") is not None:
            return None
    return item


def _run_one(payload: dict, sequence: int, timeout: float) -> dict:
    if not _kill_other_processes():
        return {
            "v": 1, "sequence": sequence, "probe_id": payload.get("probe_id"),
            "status": "boundary_error", "answer": None, "tree_empty": False,
        }
    _clear_tmp()
    tmpdir = Path("/tmp") / ("h3-" + uuid.uuid4().hex)
    tmpdir.mkdir(mode=0o700)
    os.chown(tmpdir, UID, GID)
    env = {
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "HOME": str(tmpdir),
        "TMPDIR": str(tmpdir),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
    }
    try:
        proc = subprocess.Popen(
            [sys.executable, "-I", CHILD, "/candidate/body.py"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            close_fds=True, bufsize=0, env=env, preexec_fn=_drop_child_privileges,
            start_new_session=True,
        )
        line = json.dumps(payload, separators=(",", ":")).encode("utf-8") + b"\n"
        if len(line) > MAX_LINE_BYTES:
            try:
                proc.kill()
            except OSError:
                pass
            return_code = proc.wait(timeout=1)
            return {
                "v": 1, "sequence": sequence, "probe_id": payload.get("probe_id"),
                "status": "invalid_input", "answer": None, "tree_empty": _kill_other_processes(),
                "return_code": return_code,
            }
        proc.stdin.write(line)
        proc.stdin.close()
        child = _read_child(proc, timeout)
        tree_before_cleanup = bool(_other_pids())
        tree_empty = _kill_other_processes()
        prediction = None if child["timed_out"] or child["output_overflow"] else _parse_prediction(
            child["stdout"], str(payload.get("probe_id"))
        )
        status = "ok"
        if child["timed_out"]:
            status = "timeout"
        elif child["output_overflow"]:
            status = "output_overflow"
        elif not tree_empty:
            status = "tree_cleanup_failed"
        elif tree_before_cleanup:
            status = "process_tree_leak"
        elif prediction is None or child["return_code"] != 0:
            status = "invalid_child_output"
        elif prediction.get("status") == "exception":
            status = "exception"
        elif prediction.get("status") == "invalid_input":
            status = "invalid_input"

        answer = prediction.get("answer") if status == "ok" and prediction else None
        answer_type = prediction.get("answer_type") if status == "ok" and prediction else "none"
        result = {
            "v": 1,
            "sequence": sequence,
            "probe_id": str(payload.get("probe_id")),
            "status": status,
            "answer_type": answer_type,
            "answer": answer,
            "tree_empty_before_cleanup": not tree_before_cleanup,
            "tree_empty": tree_empty,
            "timed_out": child["timed_out"],
            "output_overflow": child["output_overflow"],
            "child_return_code": child["return_code"],
            "child_stdout_bytes": child["stdout_bytes"],
            "child_stderr_bytes": child["stderr_bytes"],
            "child_stderr_sha256": child["stderr_sha256"],
            "elapsed_seconds": child["elapsed_seconds"],
            "solver_stdout_characters": (prediction or {}).get("solver_stdout_characters"),
            "solver_stderr_characters": (prediction or {}).get("solver_stderr_characters"),
            "solver_output_overflow": (prediction or {}).get("solver_output_overflow"),
        }
        if not tree_empty:
            # Fail closed: the host should terminate the entire container.
            result["fatal"] = True
        return result
    except BaseException as exc:
        _kill_other_processes()
        return {
            "v": 1, "sequence": sequence, "probe_id": payload.get("probe_id"),
            "status": "supervisor_error", "error_type": type(exc).__name__,
            "answer": None, "tree_empty": not bool(_other_pids()),
        }
    finally:
        try:
            shutil.rmtree(tmpdir)
        except OSError:
            pass


def main() -> int:
    if os.geteuid() != 0:
        print(json.dumps({"v": 1, "status": "supervisor_must_start_as_root"}), flush=True)
        return 70
    os.chmod("/tmp", 0o711)
    sequence = 0
    for raw in sys.stdin.buffer:
        sequence += 1
        if len(raw) > MAX_LINE_BYTES:
            record = {
                "v": 1, "sequence": sequence, "status": "invalid_input",
                "answer": None, "tree_empty": not bool(_other_pids()),
            }
        else:
            try:
                payload = json.loads(raw.decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("not_object")
                record = _run_one(payload, sequence, DEFAULT_TIMEOUT_SECONDS)
            except Exception as exc:
                record = {
                    "v": 1, "sequence": sequence, "status": "invalid_input",
                    "error_type": type(exc).__name__, "answer": None,
                    "tree_empty": not bool(_other_pids()),
                }
        sys.stdout.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
        sys.stdout.flush()
        if record.get("fatal") or not record.get("tree_empty", False):
            return 70
    _kill_other_processes()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
