"""Execute one solver call inside the isolated container as an unprivileged child.

This process sees one probe input at a time and has no answer key, repository,
provider token, network, writable root filesystem, or shared output mount.
Its record is an untrusted prediction, never a score.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import selectors
import signal
import subprocess
import sys
import time
from pathlib import Path

MAX_INPUT_BYTES = 64 * 1024
MAX_CAPTURE_CHARS = 16 * 1024
BODY = Path("/candidate/body.py")


class BoundedTextIO(io.TextIOBase):
    """Capture ordinary solver prints without retaining unbounded output."""

    def __init__(self, limit: int = MAX_CAPTURE_CHARS):
        self.limit = limit
        self.parts: list[str] = []
        self.characters = 0
        self.overflow = False

    def writable(self) -> bool:
        return True

    @property
    def encoding(self):
        return "utf-8"

    def write(self, text: str) -> int:
        if not isinstance(text, str):
            text = str(text)
        original_length = len(text)
        available = max(0, self.limit - self.characters)
        if available:
            kept = text[:available]
            self.parts.append(kept)
            self.characters += len(kept)
        if original_length > available:
            self.overflow = True
        return original_length

    def flush(self) -> None:
        return None


def _answer_shape(value) -> tuple[str, int | None]:
    # Exact type checks prevent bool-as-int and avoid calling an untrusted
    # object’s repr/str methods while formatting the response.
    if value is None:
        return "none", None
    if type(value) is bool:
        return "bool", None
    if type(value) is int:
        if -(2**63) <= value <= (2**63 - 1):
            return "int", value
        return "int_out_of_range", None
    if type(value) is str:
        return "str", None
    if type(value) is float:
        return "float", None
    return "other", None


def _validate_input(payload: object) -> tuple[int, list[tuple[int, int, int]], int, int, str, str]:
    if not isinstance(payload, dict):
        raise ValueError("input_not_object")
    probe_id = payload.get("probe_id")
    phase = payload.get("phase", "probe")
    n, edges, source, target = payload.get("n"), payload.get("edges"), payload.get("s"), payload.get("t")
    if phase not in {"probe", "preflight"}:
        raise ValueError("invalid_phase")
    if not isinstance(probe_id, str) or not probe_id or len(probe_id) > 128:
        raise ValueError("invalid_probe_id")
    if type(n) is not int or not 1 <= n <= 10000:
        raise ValueError("invalid_n")
    if type(source) is not int or type(target) is not int or not 0 <= source < max(n, 1) or not 0 <= target < max(n, 1):
        raise ValueError("invalid_endpoints")
    if not isinstance(edges, list) or len(edges) > 100000:
        raise ValueError("invalid_edges")
    parsed = []
    for edge in edges:
        if not isinstance(edge, list) or len(edge) != 3 or any(type(v) is not int for v in edge):
            raise ValueError("invalid_edge")
        u, v, w = edge
        if not (0 <= u < n and 0 <= v < n and w >= 0):
            raise ValueError("edge_out_of_range")
        parsed.append((u, v, w))
    return n, parsed, source, target, probe_id, phase


def _load_solve():
    if not BODY.is_file() or BODY.is_symlink():
        raise ImportError("candidate_body_missing_or_unsafe")
    spec = importlib.util.spec_from_file_location("h3_candidate", BODY)
    if spec is None or spec.loader is None:
        raise ImportError("candidate_has_no_loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    solve = getattr(module, "solve", None)
    if not callable(solve):
        raise AttributeError("missing_solve")
    return solve


MAX_WORKER_OUTPUT_BYTES = 64 * 1024


def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_json_key")
        result[key] = value
    return result


def _parse_worker_response(stdout: bytes, phase: str) -> tuple[str, int | None] | None:
    """Accept only an answer value from the untrusted worker, never its metadata."""
    try:
        text = stdout.decode("utf-8")
        lines = text.splitlines()
        if not text.endswith("\n") or len(lines) != 1:
            return None
        item = json.loads(lines[0], object_pairs_hook=_no_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return None
    if not isinstance(item, dict) or set(item) != {"answer_type", "answer"}:
        return None
    answer_type = item.get("answer_type")
    answer = item.get("answer")
    if type(answer_type) is not str:
        return None
    allowed = {"callable", "none", "bool", "int", "int_out_of_range", "str", "float", "other"}
    if answer_type not in allowed:
        return None
    if phase == "preflight":
        return ("callable", None) if answer_type == "callable" and answer is None else None
    if answer_type == "callable":
        return None
    if answer_type == "int":
        if type(answer) is not int or not (-(2**63) <= answer <= (2**63 - 1)):
            return None
        return answer_type, answer
    if answer is not None:
        return None
    return answer_type, None


def _kill_worker(proc: subprocess.Popen) -> None:
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        try:
            proc.kill()
        except OSError:
            pass
    try:
        proc.wait(timeout=0.5)
    except subprocess.TimeoutExpired:
        try:
            proc.kill()
        except OSError:
            pass


def _run_worker(payload: dict, timeout: float) -> tuple[str, str, int | None]:
    """Run untrusted solver code in a process that cannot write supervisor metadata."""
    phase = payload.get("phase", "probe")
    worker_payload = {
        "phase": phase,
        "n": payload["n"],
        "edges": payload["edges"],
        "s": payload["s"],
        "t": payload["t"],
    }
    raw = json.dumps(worker_payload, separators=(",", ":")).encode("utf-8") + b"\n"
    proc = subprocess.Popen(
        [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--worker"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        close_fds=True, bufsize=0, start_new_session=True,
    )
    stdout = bytearray()
    stderr = bytearray()
    selector = selectors.DefaultSelector()
    total_bytes = 0
    timed_out = False
    overflow = False
    started = time.monotonic()
    deadline = started + max(0.1, timeout - 0.15)
    try:
        proc.stdin.write(raw)
        proc.stdin.close()
        for name, stream in (("stdout", proc.stdout), ("stderr", proc.stderr)):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, name)
        while selector.get_map() or proc.poll() is None:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                _kill_worker(proc)
                break
            for key, _ in selector.select(min(0.025, remaining)):
                try:
                    chunk = os.read(key.fileobj.fileno(), 4096)
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                total_bytes += len(chunk)
                if total_bytes > MAX_WORKER_OUTPUT_BYTES:
                    overflow = True
                    _kill_worker(proc)
                    break
                (stdout if key.data == "stdout" else stderr).extend(chunk)
            if overflow:
                break
        if timed_out:
            return "timeout", "none", None
        if overflow:
            return "output_overflow", "none", None
        try:
            return_code = proc.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            _kill_worker(proc)
            return "timeout", "none", None
        if return_code != 0:
            return "exception", "none", None
        parsed = _parse_worker_response(bytes(stdout), phase)
        if parsed is None:
            return "invalid_child_output", "none", None
        return "ok", parsed[0], parsed[1]
    finally:
        selector.close()
        for stream in (proc.stdin, proc.stdout, proc.stderr):
            try:
                if stream is not None:
                    stream.close()
            except OSError:
                pass


def _worker_main() -> int:
    """Execute the candidate and emit only its answer value; no status metadata."""
    protocol_stdout = sys.stdout
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        return 64
    payload = json.loads(raw.decode("utf-8"))
    # The real probe identifier is intentionally not passed into this process.
    n, edges, source, target, _unused_probe_id, phase = _validate_input({**payload, "probe_id": "worker"})
    captured_out, captured_err = BoundedTextIO(), BoundedTextIO()
    with contextlib.redirect_stdout(captured_out), contextlib.redirect_stderr(captured_err):
        solve = _load_solve()
        if phase == "preflight":
            answer_type, answer_int = "callable", None
        else:
            answer = solve(n, edges, source, target)
            answer_type, answer_int = _answer_shape(answer)
    # These two fields are the only data the coordinator accepts from this process.
    response = {"answer_type": answer_type, "answer": answer_int}
    protocol_stdout.write(json.dumps(response, sort_keys=True, separators=(",", ":")) + "\n")
    protocol_stdout.flush()
    return 0


def _coordinator_main() -> int:
    protocol_stdout = sys.stdout
    args = sys.argv[1:]
    timeout = 5.0
    if args:
        if len(args) != 2 or args[0] != "--probe-timeout":
            return 64
        try:
            timeout = float(args[1])
        except ValueError:
            return 64
        if not 0.2 <= timeout <= 30.0:
            return 64
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        result = {"v": 1, "status": "invalid_input", "error_type": "input_too_large"}
        protocol_stdout.write("H3PRED " + json.dumps(result, sort_keys=True) + "\n")
        protocol_stdout.flush()
        return 0
    try:
        payload = json.loads(raw.decode("utf-8"))
        n, edges, source, target, probe_id, phase = _validate_input(payload)
        # Send normalized graph data only; the true probe ID stays in this process.
        normalized = {"n": n, "edges": [list(edge) for edge in edges], "s": source, "t": target, "phase": phase}
    except Exception as exc:
        result = {"v": 1, "status": "invalid_input", "error_type": type(exc).__name__}
        protocol_stdout.write("H3PRED " + json.dumps(result, sort_keys=True) + "\n")
        protocol_stdout.flush()
        return 0

    status, answer_type, answer = _run_worker(normalized, timeout)
    result = {
        "v": 1,
        "phase": phase,
        "probe_id": probe_id,
        "status": status,
        "answer_type": answer_type,
        "answer": answer,
    }
    protocol_stdout.write("H3PRED " + json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    protocol_stdout.flush()
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        return _worker_main()
    return _coordinator_main()


if __name__ == "__main__":
    raise SystemExit(main())
