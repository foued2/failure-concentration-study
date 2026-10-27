from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path

# Capture trusted references before the candidate module is imported. The
# candidate shares this process, so it can replace sys.stdout, json.dumps, or
# sys.argv; the worker must still emit exactly one nonce-tagged line to the
# parent. The parent, not this process, owns the expected values and decides
# whether a probe failed.
_STDOUT = sys.stdout
_DUMPS = json.dumps


def _emit(nonce: str, payload: dict) -> None:
    _STDOUT.write(nonce + " " + _DUMPS(payload, sort_keys=True) + "\n")
    _STDOUT.flush()


def _drop_to_low_integrity() -> None:
    """Run the candidate at low integrity so it cannot write up to the output root."""
    if sys.platform != "win32":
        return
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

    advapi32.ConvertStringSidToSidW.argtypes = [
        wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_void_p)
    ]
    advapi32.ConvertStringSidToSidW.restype = wintypes.BOOL
    advapi32.GetLengthSid.argtypes = [ctypes.c_void_p]
    advapi32.GetLengthSid.restype = wintypes.DWORD
    advapi32.OpenProcessToken.argtypes = [
        wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)
    ]
    advapi32.OpenProcessToken.restype = wintypes.BOOL
    advapi32.SetTokenInformation.argtypes = [
        wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD
    ]
    advapi32.SetTokenInformation.restype = wintypes.BOOL
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.LocalFree.argtypes = [ctypes.c_void_p]

    sid = ctypes.c_void_p()
    token = wintypes.HANDLE()
    try:
        if not advapi32.ConvertStringSidToSidW("S-1-16-4096", ctypes.byref(sid)):
            raise ctypes.WinError(ctypes.get_last_error())
        if not advapi32.OpenProcessToken(
            kernel32.GetCurrentProcess(),
            TOKEN_QUERY | TOKEN_ADJUST_DEFAULT,
            ctypes.byref(token),
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        label = TOKEN_MANDATORY_LABEL()
        label.Label.Sid = sid
        label.Label.Attributes = SE_GROUP_INTEGRITY
        size = (
            ctypes.sizeof(TOKEN_MANDATORY_LABEL)
            + advapi32.GetLengthSid(sid)
            - ctypes.sizeof(ctypes.c_void_p)
        )
        if not advapi32.SetTokenInformation(
            token, TOKEN_INTEGRITY_LEVEL, ctypes.byref(label), size
        ):
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        if token:
            kernel32.CloseHandle(token)
        if sid:
            kernel32.LocalFree(sid)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("candidate", path)
    if spec is None or spec.loader is None:
        raise ImportError("no loader")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, "solve", None)
    if not callable(fn):
        raise AttributeError("missing solve")
    return fn


def _emit_answer(nonce: str, probe_index: int, out) -> None:
    try:
        _emit(nonce, {"phase": "probe", "probe_index": probe_index, "answer": out})
    except BaseException:
        _emit(nonce, {"phase": "probe", "probe_index": probe_index, "error": "unserializable"})


def main() -> None:
    _drop_to_low_integrity()
    if len(sys.argv) < 3:
        _emit("", {"phase": "harness", "error": "usage: candidate.py --preflight NONCE | --probe INDEX PROBE_JSON NONCE"})
        return
    path = Path(sys.argv[1])
    mode = sys.argv[2]

    if mode == "--preflight":
        if len(sys.argv) != 4:
            _emit("", {"phase": "harness", "error": "preflight requires a nonce"})
            return
        nonce = sys.argv[3]
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                load(path)
            _emit(nonce, {"phase": "preflight", "valid": True, "load_error": None})
        except BaseException as exc:
            _emit(nonce, {"phase": "load", "valid": False, "load_error": f"{type(exc).__name__}: {exc}"})
        return

    if mode != "--probe" or len(sys.argv) != 6:
        _emit("", {"phase": "harness", "error": "usage: candidate.py --preflight NONCE | --probe INDEX PROBE_JSON NONCE"})
        return

    nonce = sys.argv[5]
    try:
        probe_index = int(sys.argv[3])
        probe = json.loads(sys.argv[4])
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            solve = load(path)
    except BaseException as exc:
        _emit(nonce, {"phase": "load", "load_error": f"{type(exc).__name__}: {exc}"})
        return

    edges = [tuple(edge) if isinstance(edge, (list, tuple)) else edge for edge in probe["edges"]]
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            out = solve(probe["n"], edges, probe["s"], probe["t"])
    except BaseException as exc:
        _emit(nonce, {"phase": "probe", "probe_index": probe_index, "error": type(exc).__name__})
        return
    _emit_answer(nonce, probe_index, out)


if __name__ == "__main__":
    main()
