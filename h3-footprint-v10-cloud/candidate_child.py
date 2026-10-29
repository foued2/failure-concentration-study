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
import sys
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


def _validate_input(payload: object) -> tuple[int, list[tuple[int, int, int]], int, int, str]:
    if not isinstance(payload, dict):
        raise ValueError("input_not_object")
    probe_id = payload.get("probe_id")
    n, edges, source, target = payload.get("n"), payload.get("edges"), payload.get("s"), payload.get("t")
    if not isinstance(probe_id, str) or not probe_id or len(probe_id) > 128:
        raise ValueError("invalid_probe_id")
    if type(n) is not int or not 0 <= n <= 10000:
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
    return n, parsed, source, target, probe_id


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


def main() -> int:
    protocol_stdout = sys.stdout
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        result = {"v": 1, "status": "invalid_input", "error_type": "input_too_large"}
        protocol_stdout.write("H3PRED " + json.dumps(result, sort_keys=True) + "\n")
        protocol_stdout.flush()
        return 0
    try:
        payload = json.loads(raw.decode("utf-8"))
        n, edges, source, target, probe_id = _validate_input(payload)
    except Exception as exc:
        result = {"v": 1, "status": "invalid_input", "error_type": type(exc).__name__}
        protocol_stdout.write("H3PRED " + json.dumps(result, sort_keys=True) + "\n")
        protocol_stdout.flush()
        return 0

    captured_out, captured_err = BoundedTextIO(), BoundedTextIO()
    try:
        with contextlib.redirect_stdout(captured_out), contextlib.redirect_stderr(captured_err):
            solve = _load_solve()
            answer = solve(n, edges, source, target)
        answer_type, answer_int = _answer_shape(answer)
        result = {
            "v": 1,
            "probe_id": probe_id,
            "status": "ok",
            "answer_type": answer_type,
            "answer": answer_int,
            "solver_stdout_characters": captured_out.characters,
            "solver_stderr_characters": captured_err.characters,
            "solver_output_overflow": captured_out.overflow or captured_err.overflow,
        }
    except BaseException as exc:
        # Do not serialize exception messages from untrusted code.
        if isinstance(exc, SystemExit):
            error_type = "SystemExit"
        elif isinstance(exc, KeyboardInterrupt):
            error_type = "KeyboardInterrupt"
        else:
            error_type = type(exc).__name__
        result = {
            "v": 1,
            "probe_id": probe_id,
            "status": "exception",
            "error_type": error_type,
            "answer_type": "none",
            "answer": None,
            "solver_stdout_characters": captured_out.characters,
            "solver_stderr_characters": captured_err.characters,
            "solver_output_overflow": captured_out.overflow or captured_err.overflow,
        }

    protocol_stdout.write("H3PRED " + json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    protocol_stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
