"""Untrusted child wrapper.

This whole process is inside the Job Object and is treated as adversarial. It
imports the candidate module and calls `solve`. Everything it prints is
untrusted data as far as the host is concerned: the host never accepts a
correct/incorrect verdict from here, only a raw value that it compares itself
against a reference the child cannot see.

The process blocks on a start signal so the supervisor can assign it to the Job
Object before any candidate code runs.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys

MARKER = "V9RESULT"

# Captured before the candidate module is imported. A candidate that replaces
# sys.stdout, json.dumps or builtins cannot redirect this write, and the host
# does not trust the payload anyway.
_WRITE = os.write
_DUMPS = json.dumps


def _drop_to_low_integrity() -> bool:
    """Lower this process to low integrity before any candidate code runs.

    The ACL lock alone is insufficient: the owning user can remove a deny ACE
    with WRITE_DAC. Low integrity cannot write up to medium-integrity objects,
    so the job and response directories stay out of reach.
    """
    if sys.platform != "win32":
        return True
    import ctypes
    from ctypes import wintypes

    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    TOKEN_QUERY = 0x0008
    TOKEN_ADJUST_DEFAULT = 0x0080
    TOKEN_INTEGRITY_LEVEL = 25
    SE_GROUP_INTEGRITY = 0x20

    class SID_AND_ATTRIBUTES(ctypes.Structure):
        _fields_ = [("Sid", ctypes.c_void_p), ("Attributes", wintypes.DWORD)]

    class TOKEN_MANDATORY_LABEL(ctypes.Structure):
        _fields_ = [("Label", SID_AND_ATTRIBUTES)]

    advapi32.ConvertStringSidToSidW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_void_p)]
    advapi32.ConvertStringSidToSidW.restype = wintypes.BOOL
    advapi32.GetLengthSid.argtypes = [ctypes.c_void_p]
    advapi32.GetLengthSid.restype = wintypes.DWORD
    advapi32.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
    advapi32.OpenProcessToken.restype = wintypes.BOOL
    advapi32.SetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    advapi32.SetTokenInformation.restype = wintypes.BOOL
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.LocalFree.argtypes = [ctypes.c_void_p]

    sid = ctypes.c_void_p()
    token = wintypes.HANDLE()
    try:
        if not advapi32.ConvertStringSidToSidW("S-1-16-4096", ctypes.byref(sid)):
            return False
        if not advapi32.OpenProcessToken(
            kernel32.GetCurrentProcess(), TOKEN_QUERY | TOKEN_ADJUST_DEFAULT, ctypes.byref(token)
        ):
            return False
        label = TOKEN_MANDATORY_LABEL()
        label.Label.Sid = sid
        label.Label.Attributes = SE_GROUP_INTEGRITY
        size = ctypes.sizeof(TOKEN_MANDATORY_LABEL) + advapi32.GetLengthSid(sid) - ctypes.sizeof(ctypes.c_void_p)
        if not advapi32.SetTokenInformation(token, TOKEN_INTEGRITY_LEVEL, ctypes.byref(label), size):
            return False
        return True
    except OSError:
        return False
    finally:
        if token:
            kernel32.CloseHandle(token)
        if sid:
            kernel32.LocalFree(sid)


def _emit(payload: dict) -> None:
    line = MARKER + " " + _DUMPS(payload, sort_keys=True) + "\n"
    try:
        _WRITE(1, line.encode("utf-8", "replace"))
    except OSError:
        pass


def main() -> None:
    if len(sys.argv) != 2:
        _emit({"error": "usage"})
        return

    if not _drop_to_low_integrity():
        _emit({"error": "integrity_drop_failed"})
        return

    # Barrier: the job object has been assigned by the time this returns.
    sys.stdin.readline()
    raw_input = sys.stdin.readline()

    if raw_input.strip() in ("", "null"):
        job_input = None
    else:
        try:
            job_input = json.loads(raw_input)
        except json.JSONDecodeError:
            _emit({"error": "bad_input"})
            return

    path = sys.argv[1]
    try:
        spec = importlib.util.spec_from_file_location("candidate", path)
        if spec is None or spec.loader is None:
            _emit({"error": "no_loader"})
            return
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        solve = getattr(module, "solve", None)
        if not callable(solve):
            _emit({"error": "missing_solve"})
            return
    except BaseException as exc:  # noqa: BLE001 - untrusted module
        _emit({"error": type(exc).__name__})
        return

    if job_input is None:
        _emit({"loaded": True})
        return

    try:
        edges = [tuple(edge) for edge in job_input["edges"]]
        answer = solve(job_input["n"], edges, job_input["s"], job_input["t"])
    except BaseException as exc:  # noqa: BLE001 - untrusted module
        _emit({"error": type(exc).__name__})
        return

    try:
        _DUMPS(answer)
    except (TypeError, ValueError):
        _emit({"error": "unserializable"})
        return

    _emit({"answer": answer})


if __name__ == "__main__":
    main()
