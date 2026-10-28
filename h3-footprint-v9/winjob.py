"""Windows Job Object control: per-candidate process-tree bounds.

V8 used `subprocess.run(timeout=5)`, which kills only the direct child. This
module assigns a child and every descendant to a Job Object configured with:

  - JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE   (nothing survives handle close)
  - JOB_OBJECT_LIMIT_ACTIVE_PROCESS      (process-count cap)
  - JOB_OBJECT_LIMIT_PROCESS_MEMORY      (per-process memory cap)

Termination is explicit (`TerminateJobObject`) and is verified by querying the
job's active-process count, so "the tree is gone" is measured, not assumed.
"""

from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    _k32 = ctypes.WinDLL("kernel32", use_last_error=True)
else:  # pragma: no cover - tests skip on non-Windows
    _k32 = None

JobObjectBasicAccountingInformation = 1
JobObjectExtendedLimitInformation = 9

JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x00000100
JOB_OBJECT_LIMIT_ACTIVE_PROCESS = 0x00000008
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000

PROCESS_SET_QUOTA = 0x0100
PROCESS_TERMINATE = 0x0001
SYNCHRONIZE = 0x00100000
WAIT_TIMEOUT = 0x00000102


class IO_COUNTERS(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_ulonglong),
        ("WriteOperationCount", ctypes.c_ulonglong),
        ("OtherOperationCount", ctypes.c_ulonglong),
        ("ReadTransferCount", ctypes.c_ulonglong),
        ("WriteTransferCount", ctypes.c_ulonglong),
        ("OtherTransferCount", ctypes.c_ulonglong),
    ]


class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]


class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class JOBOBJECT_BASIC_ACCOUNTING_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("TotalUserTime", ctypes.c_int64),
        ("TotalKernelTime", ctypes.c_int64),
        ("ThisPeriodTotalUserTime", ctypes.c_int64),
        ("ThisPeriodTotalKernelTime", ctypes.c_int64),
        ("TotalPageFaultCount", wintypes.DWORD),
        ("TotalProcesses", wintypes.DWORD),
        ("ActiveProcesses", wintypes.DWORD),
        ("TotalTerminatedProcesses", wintypes.DWORD),
    ]


def _require_windows() -> None:
    if not IS_WINDOWS:
        raise OSError("Windows Job Objects are unavailable on this platform")


def _configure_signatures() -> None:
    _k32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    _k32.CreateJobObjectW.restype = wintypes.HANDLE
    _k32.SetInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD
    ]
    _k32.SetInformationJobObject.restype = wintypes.BOOL
    _k32.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p
    ]
    _k32.QueryInformationJobObject.restype = wintypes.BOOL
    _k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    _k32.AssignProcessToJobObject.restype = wintypes.BOOL
    _k32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    _k32.TerminateJobObject.restype = wintypes.BOOL
    _k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _k32.OpenProcess.restype = wintypes.HANDLE
    _k32.CloseHandle.argtypes = [wintypes.HANDLE]
    _k32.CloseHandle.restype = wintypes.BOOL
    _k32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    _k32.WaitForSingleObject.restype = wintypes.DWORD


if IS_WINDOWS:
    _configure_signatures()


def _raise(what: str) -> None:
    raise ctypes.WinError(ctypes.get_last_error())


def create(memory_bytes: int, max_processes: int) -> ctypes.c_void_p:
    _require_windows()
    handle = _k32.CreateJobObjectW(None, None)
    if not handle:
        _raise("CreateJobObjectW")
    info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
    info.BasicLimitInformation.LimitFlags = (
        JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        | JOB_OBJECT_LIMIT_ACTIVE_PROCESS
        | JOB_OBJECT_LIMIT_PROCESS_MEMORY
    )
    info.BasicLimitInformation.ActiveProcessLimit = max_processes
    info.ProcessMemoryLimit = memory_bytes
    if not _k32.SetInformationJobObject(
        handle, JobObjectExtendedLimitInformation,
        ctypes.byref(info), ctypes.sizeof(info),
    ):
        _k32.CloseHandle(handle)
        _raise("SetInformationJobObject")
    return handle


def assign(handle: ctypes.c_void_p, pid: int) -> None:
    _require_windows()
    proc = _k32.OpenProcess(PROCESS_SET_QUOTA | PROCESS_TERMINATE, False, pid)
    if not proc:
        _raise("OpenProcess")
    try:
        if not _k32.AssignProcessToJobObject(handle, proc):
            _raise("AssignProcessToJobObject")
    finally:
        _k32.CloseHandle(proc)


def active_processes(handle: ctypes.c_void_p) -> int:
    _require_windows()
    info = JOBOBJECT_BASIC_ACCOUNTING_INFORMATION()
    if not _k32.QueryInformationJobObject(
        handle, JobObjectBasicAccountingInformation,
        ctypes.byref(info), ctypes.sizeof(info), None,
    ):
        _raise("QueryInformationJobObject")
    return int(info.ActiveProcesses)


def terminate(handle: ctypes.c_void_p, exit_code: int = 1) -> None:
    _require_windows()
    _k32.TerminateJobObject(handle, exit_code)


def close(handle: ctypes.c_void_p) -> None:
    if IS_WINDOWS and handle:
        _k32.CloseHandle(handle)


def is_process_alive(pid: int) -> bool:
    if not IS_WINDOWS:
        return False
    proc = _k32.OpenProcess(SYNCHRONIZE, False, pid)
    if not proc:
        return False
    try:
        return _k32.WaitForSingleObject(proc, 0) == WAIT_TIMEOUT
    finally:
        _k32.CloseHandle(proc)
