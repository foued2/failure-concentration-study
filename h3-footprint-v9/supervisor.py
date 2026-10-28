"""Secret-free Sandbox supervisor.

Responsibilities, and nothing else:
  1. read the single active job,
  2. start the candidate in a separate untrusted child process,
  3. bind that child and all descendants to a Job Object,
  4. capture bounded external output under time/memory/process caps,
  5. terminate the whole tree on timeout and verify it is gone,
  6. only then publish one raw response record.

It holds no expected answers, no probe bank, no family labels and no scoring
code. It must never import `oracle`.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import protocol  # noqa: E402
import winjob  # noqa: E402

CHILD = HERE / "child_runner.py"
CREATE_NO_WINDOW = 0x08000000
MARKER = "V9RESULT"


def _set_low_integrity(path: Path) -> dict:
    """Scratch must be writable by the low-integrity child.

    Returns the outcome *and* the tool's own error text: inside Windows Sandbox
    this fails on a mapped folder (the guest cannot label a redirected path), so
    the scratch directory has to live on the guest's local disk and the failure
    has to be visible in the response rather than guessed at.
    """
    if sys.platform != "win32":
        return {"ok": True, "error": None, "skipped": "non-windows"}
    proc = subprocess.run(
        ["icacls", str(path), "/setintegritylevel", "(OI)(CI)Low"],
        capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace",
    )
    if proc.returncode == 0:
        return {"ok": True, "error": None, "path": str(path)}
    detail = (proc.stderr.strip() or proc.stdout.strip() or f"icacls rc={proc.returncode}")
    return {"ok": False, "error": detail[:500], "path": str(path)}


def _minimal_env(scratch: Path) -> dict[str, str]:
    keep = {
        "PATH": os.environ.get("PATH", ""),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", r"C:\Windows"),
        "WINDIR": os.environ.get("WINDIR", r"C:\Windows"),
        "TEMP": str(scratch),
        "TMP": str(scratch),
        "USERPROFILE": str(scratch),
        "LOCALAPPDATA": str(scratch),
        "NUMBER_OF_PROCESSORS": os.environ.get("NUMBER_OF_PROCESSORS", "1"),
        "PROCESSOR_ARCHITECTURE": os.environ.get("PROCESSOR_ARCHITECTURE", "AMD64"),
        "SYSTEMDRIVE": os.environ.get("SYSTEMDRIVE", "C:"),
        "COMSPEC": os.environ.get("COMSPEC", r"C:\Windows\System32\cmd.exe"),
    }
    return {k: v for k, v in keep.items() if v}


def runtime_paths(inbox: Path, outbox: Path, scratch: Path) -> dict[str, str]:
    """The guest's real mapped directories, resolved once, for a diagnostic probe.

    A probe must not guess these from its working directory: the child's cwd is
    the guest-local scratch folder, so ``../staging`` or ``../response`` resolves
    beside scratch and would test the wrong directory. The agent passes the paths
    it was actually launched with, and these are the paths the probe receives.
    """
    paths = {
        "inbox": str(Path(inbox).resolve()),
        "outbox": str(Path(outbox).resolve()),
        "scratch": str(Path(scratch).resolve()),
    }
    for name, value in paths.items():
        if not value or not os.path.isabs(value):
            raise ValueError(f"runtime path {name} is not absolute: {value!r}")
    if len(set(paths.values())) != len(paths):
        raise ValueError("runtime paths must be distinct directories")
    return paths


def _child_payload(job: dict, paths: dict[str, str] | None) -> str:
    """Serialize the child's input, adding the resolved runtime paths if given.

    The paths are runtime facts, not host expectations, and they are not secret:
    the guest can already read them from its own launch command. They are passed
    explicitly so a probe cannot silently target a look-alike directory.
    """
    payload = job.get("input")
    if paths is not None:
        base: dict = dict(payload) if isinstance(payload, dict) else (
            {} if payload is None else {"input": payload}
        )
        base["paths"] = dict(paths)
        payload = base
    return json.dumps(payload, sort_keys=True)



class _CappedReader(threading.Thread):
    """Read the child's stdout without letting it exhaust supervisor memory."""

    def __init__(self, stream, cap: int) -> None:
        super().__init__(daemon=True)
        self.stream = stream
        self.cap = cap
        self.chunks: list[bytes] = []
        self.total = 0
        self.overflow = False
        self._stop = threading.Event()

    def run(self) -> None:
        try:
            while not self._stop.is_set():
                chunk = self.stream.read(4096)
                if not chunk:
                    break
                self.total += len(chunk)
                if self.total > self.cap:
                    self.overflow = True
                    break
                self.chunks.append(chunk)
        except (OSError, ValueError):
            pass

    def stop(self) -> None:
        self._stop.set()

    def payload(self) -> bytes:
        return b"".join(self.chunks)


def _parse(text: str) -> dict | None:
    """Take the last marker line. The value is untrusted input to the host."""
    found = None
    for line in text.splitlines():
        if line.startswith(MARKER + " "):
            found = line[len(MARKER) + 1:]
    if found is None:
        return None
    try:
        value = json.loads(found)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def run_job(staging: Path, response_dir: Path, scratch: Path, *, timeout: float,
            memory_bytes: int, max_processes: int,
            lock_staging: bool = True, lock_response: bool = True,
            paths: dict[str, str] | None = None) -> dict:
    staging, response_dir, scratch = Path(staging), Path(response_dir), Path(scratch)
    job = protocol.read_job(staging)
    return execute_job(
        job, staging / protocol.BODY_FILENAME, response_dir, scratch,
        timeout=timeout, memory_bytes=memory_bytes, max_processes=max_processes,
        lock_staging=lock_staging, lock_response=lock_response, clear_stale=True,
        paths=paths,
    )


def run_immutable_job(job: dict, body_path: Path, response_dir: Path, scratch: Path, *,
                      timeout: float, memory_bytes: int, max_processes: int,
                      paths: dict[str, str] | None = None) -> dict:
    """Execute one request from the immutable protocol.

    The body path is content-addressed by the host, so there is no staging file to
    rewrite and no stale response to clear: the response name is unique to the
    job id and the write is exclusive.
    """
    return execute_job(
        job, Path(body_path), Path(response_dir), Path(scratch),
        timeout=timeout, memory_bytes=memory_bytes, max_processes=max_processes,
        lock_staging=False, lock_response=False, clear_stale=False,
        paths=paths,
    )


def execute_job(job: dict, body: Path, response_dir: Path, scratch: Path, *,
                timeout: float, memory_bytes: int, max_processes: int,
                lock_staging: bool = True, lock_response: bool = True,
                clear_stale: bool = True,
                paths: dict[str, str] | None = None) -> dict:
    response_dir, scratch = Path(response_dir), Path(scratch)
    ident = winjob.identity()
    base = {
        "v9": protocol.JOB_SCHEMA,
        "job_id": job["job_id"],
        "sequence": job["sequence"],
        "kind": job["kind"],
        "probe_index": job.get("probe_index"),
        "body_sha256": job["body_sha256"],
        "supervisor_pid": os.getpid(),
        "inside_sandbox": ident["inside_sandbox"],
        "identity_user": ident["user"],
    }

    if protocol.sha256_file(body) != job["body_sha256"]:
        record = {**base, "status": "staging_mismatch", "answer": None,
                  "timed_out": False, "tree_empty": True, "exit_code": None,
                  "raw_stdout": "", "stdout_bytes": 0, "stdout_overflow": False}
        protocol.write_response_exclusive(response_dir, record)
        return record

    scratch.mkdir(parents=True, exist_ok=True)
    response_dir.mkdir(parents=True, exist_ok=True)
    if clear_stale:
        for stale in response_dir.glob(f"response-{job['job_id']}.json"):
            stale.unlink()

    scratch_low = _set_low_integrity(scratch)
    # Inside the Sandbox, staging is a read-only host mapping and ACL edits on
    # mapped folders are rejected by design, so locking is optional there: the
    # mapping is the barrier. Writes into the writable mapping are blocked by
    # integrity level (low cannot write up to medium), which the isolation
    # preflight measures rather than assumes.
    locks = []
    if lock_staging:
        locks.append({"target": "staging", **protocol.lock_dir(body.parent)})
    if lock_response:
        locks.append({"target": "response", **protocol.lock_dir(response_dir)})
    if not (scratch_low["ok"] and all(lock["ok"] for lock in locks)):
        if lock_staging:
            protocol.unlock_dir(body.parent)
        if lock_response:
            protocol.unlock_dir(response_dir)
        record = {**base, "status": "boundary_error", "answer": None,
                  "timed_out": False, "tree_empty": True, "exit_code": None,
                  "raw_stdout": "", "stdout_bytes": 0, "stdout_overflow": False,
                  "boundary": {"scratch_low_integrity": scratch_low["ok"],
                               "scratch_error": scratch_low["error"],
                               "scratch_path": scratch_low.get("path"),
                               "locks": locks}}
        protocol.write_response_exclusive(response_dir, record)
        return record

    handle = None
    proc = None
    reader = None
    timed_out = False
    status = "ok"
    exit_code = None
    try:
        handle = winjob.create(memory_bytes, max_processes)
        proc = subprocess.Popen(
            [sys.executable, "-I", str(CHILD), str(body)],
            cwd=str(scratch),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=_minimal_env(scratch),
            creationflags=CREATE_NO_WINDOW,
        )
        winjob.assign(handle, proc.pid)

        payload = _child_payload(job, paths)
        assert proc.stdin is not None
        try:
            proc.stdin.write(b"GO\n" + payload.encode("utf-8") + b"\n")
            proc.stdin.flush()
            proc.stdin.close()
        except OSError:
            pass

        reader = _CappedReader(proc.stdout, job["limits"]["max_stdout_bytes"])
        reader.start()

        deadline = time.monotonic() + timeout
        try:
            exit_code = proc.wait(timeout=max(0.0, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            timed_out = True
            winjob.terminate(handle)
            try:
                exit_code = proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                exit_code = None

        if reader is not None:
            reader.join(timeout=2)
            if reader.overflow:
                status = "output_limit"
    except Exception as exc:  # noqa: BLE001 - keep the record shape
        status = "supervisor_error:" + type(exc).__name__
    finally:
        if handle is not None:
            try:
                if winjob.active_processes(handle) > 0:
                    winjob.terminate(handle)
                protocol.wait_for(lambda: winjob.active_processes(handle) == 0, 3.0)
                tree_empty = winjob.active_processes(handle) == 0
            except OSError:
                tree_empty = False
            finally:
                winjob.close(handle)
        else:
            tree_empty = True
        if lock_staging:
            protocol.unlock_dir(body.parent)
        if lock_response:
            protocol.unlock_dir(response_dir)
        if proc is not None and proc.poll() is None:
            proc.kill()
        if proc is not None and proc.stdout is not None:
            try:
                proc.stdout.close()
            except OSError:
                pass

    raw = reader.payload() if reader is not None else b""
    text = raw.decode("utf-8", "replace")
    parsed = _parse(text)

    if timed_out:
        status = "timeout"
    elif status == "ok" and parsed is None:
        status = "malformed"
    elif status == "ok" and "error" in parsed:
        status = "error"

    record = {
        **base,
        "status": status,
        "answer": parsed.get("answer") if (status == "ok" and parsed) else None,
        "error": parsed.get("error") if parsed else None,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "tree_empty": tree_empty,
        "raw_stdout": text[:2048],
        "stdout_bytes": len(raw),
        "stdout_sha256": protocol.sha256_bytes(raw),
        "stdout_overflow": bool(reader.overflow) if reader else False,
    }
    protocol.write_response_exclusive(response_dir, record)
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staging", required=True)
    parser.add_argument("--response-dir", required=True)
    parser.add_argument("--scratch", required=True)
    parser.add_argument("--timeout", type=float, required=True)
    parser.add_argument("--memory-bytes", type=int, required=True)
    parser.add_argument("--max-processes", type=int, required=True)
    parser.add_argument("--require-sandbox", action="store_true",
                        help="refuse to run unless this process is inside Windows Sandbox")
    args = parser.parse_args()

    ident = winjob.identity()
    if args.require_sandbox and not ident["inside_sandbox"]:
        print(json.dumps({"status": "boundary_error",
                          "error": "not_inside_windows_sandbox",
                          "identity_user": ident["user"]}, sort_keys=True))
        raise SystemExit(2)

    record = run_job(
        Path(args.staging), Path(args.response_dir), Path(args.scratch),
        timeout=args.timeout, memory_bytes=args.memory_bytes,
        max_processes=args.max_processes,
    )
    print(json.dumps(record, sort_keys=True))
    raise SystemExit(0 if record["status"] in ("ok", "error", "timeout") else 2)


if __name__ == "__main__":
    main()
