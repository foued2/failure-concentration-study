"""Read-only Windows Sandbox capability diagnostic.

The revision-3 report treated "WindowsSandbox.exe is absent" as if it were a
hardware conclusion. It is not: Windows 10 Pro 19045 is a supported OS, and the
optional feature is simply not installed here. This script gathers the facts
needed to classify the machine, without changing anything.

It records no serial numbers, credentials or machine identifiers.

    python evidence/windows_sandbox_capability.py

Exit codes: 0 diagnostic written; the classification is inside the JSON.
"""

from __future__ import annotations

import ctypes
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def powershell(expression: str, timeout: int = 120) -> dict:
    """Run a PowerShell expression and keep stdout, stderr and exit code."""
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", expression],
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",
        )
        return {
            "rc": proc.returncode,
            "out": (proc.stdout or "").strip(),
            "err": (proc.stderr or "").strip()[:2000],
        }
    except (OSError, subprocess.SubprocessError) as exc:
        return {"rc": None, "out": "", "err": f"{type(exc).__name__}: {exc}"}


def powershell_json(expression: str) -> tuple[object, dict]:
    raw = powershell(expression + " | ConvertTo-Json -Compress -Depth 4")
    if raw["rc"] != 0 or not raw["out"]:
        return None, raw
    try:
        return json.loads(raw["out"]), raw
    except json.JSONDecodeError:
        return None, raw


OPTIONAL_FEATURES = (
    "Containers-DisposableClientVM",
    "Microsoft-Hyper-V",
    "Microsoft-Hyper-V-All",
    "VirtualMachinePlatform",
    "HypervisorPlatform",
)


def fetch_wmi_optional_features() -> dict:
    """Feature state via WMI, which does not require elevation."""
    query = " OR ".join(f"Name='{name}'" for name in OPTIONAL_FEATURES)
    raw = powershell(
        "$rows = @(Get-CimInstance -ClassName Win32_OptionalFeature "
        f"-Filter \"{query}\" | Select-Object Name,InstallState); "
        "ConvertTo-Json -InputObject $rows -Compress -Depth 4")
    if raw["rc"] != 0 or not raw["out"]:
        raise RuntimeError(raw["err"] or "no WMI output")
    data = json.loads(raw["out"])
    if isinstance(data, dict):
        data = [data]
    return {row["Name"]: int(row["InstallState"]) for row in data}


def is_elevated() -> bool:
    """High mandatory integrity level, i.e. an elevated token."""
    if platform.system() != "Windows":
        return False
    try:
        advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        TOKEN_QUERY = 0x0008
        TokenIntegrityLevel = 25

        class SID_AND_ATTRIBUTES(ctypes.Structure):
            _fields_ = [("Sid", ctypes.c_void_p), ("Attributes", ctypes.c_ulong)]

        class TOKEN_MANDATORY_LABEL(ctypes.Structure):
            _fields_ = [("Label", SID_AND_ATTRIBUTES)]

        token = ctypes.c_void_p()
        if not advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), TOKEN_QUERY,
                                         ctypes.byref(token)):
            return False
        try:
            size = ctypes.c_ulong(0)
            advapi32.GetTokenInformation(token, TokenIntegrityLevel, None, 0,
                                         ctypes.byref(size))
            if not size.value:
                return False
            buffer = ctypes.create_string_buffer(size.value)
            if not advapi32.GetTokenInformation(token, TokenIntegrityLevel, buffer, size,
                                                ctypes.byref(size)):
                return False
            label = ctypes.cast(buffer, ctypes.POINTER(TOKEN_MANDATORY_LABEL)).contents
            count = ctypes.c_ulong(0)
            advapi32.GetSidSubAuthorityCount(label.Label.Sid, ctypes.byref(count))
            if count.value < 1:
                return False
            rid = advapi32.GetSidSubAuthority(label.Label.Sid, count.value - 1)
            return ctypes.cast(rid, ctypes.POINTER(ctypes.c_ulong)).contents.value >= 0x3000
        finally:
            kernel32.CloseHandle(token)
    except (OSError, AttributeError):
        return False


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempt-enable", action="store_true",
                        help="also attempt the documented Enable-WindowsOptionalFeature "
                             "command, and record exactly what it says. Never restarts.")
    args = parser.parse_args()

    exe = Path(os.environ.get("WINDIR", r"C:\Windows")) / "System32" / "WindowsSandbox.exe"
    report: dict = {
        "diagnostic": "windows-sandbox-capability",
        "read_only": True,
        "no_changes_made": True,
        "elevated": is_elevated(),
    }

    os_info, os_raw = powershell_json(
        "Get-CimInstance Win32_OperatingSystem | "
        "Select-Object Caption,Version,BuildNumber,OSArchitecture,InstallDate,LastBootUpTime"
    )
    report["os"] = os_info or {"error": os_raw}

    cpu, cpu_raw = powershell_json(
        "Get-CimInstance Win32_Processor | Select-Object Name,Architecture,"
        "NumberOfCores,NumberOfLogicalProcessors,VirtualizationFirmwareEnabled,"
        "VMMonitorModeExtensions,SecondLevelAddressTranslationExtensions"
    )
    report["cpu"] = cpu or {"error": cpu_raw}

    system, system_raw = powershell_json(
        "Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer,Model,"
        "HypervisorPresent,SystemType,TotalPhysicalMemory"
    )
    report["system"] = system or {"error": system_raw}

    disk, disk_raw = powershell_json(
        "Get-CimInstance Win32_LogicalDisk -Filter \"DeviceID='C:'\" | "
        "Select-Object DeviceID,Size,FreeSpace"
    )
    report["disk_c"] = disk or {"error": disk_raw}

    # Serial numbers are deliberately not read.
    bios, bios_raw = powershell_json(
        "Get-CimInstance Win32_BIOS | Select-Object Manufacturer,SMBIOSBIOSVersion,ReleaseDate"
    )
    report["bios"] = bios or {"error": bios_raw}

    hotfix, hotfix_raw = powershell_json(
        "Get-CimInstance Win32_QuickFixEngineering | Sort-Object InstalledOn -Descending | "
        "Select-Object -First 3 HotFixID,InstalledOn"
    )
    report["recent_hotfixes"] = hotfix or {"error": hotfix_raw}

    ubr = powershell(
        "(Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion' "
        "-Name UBR,DisplayVersion -ErrorAction Stop | "
        "Select-Object UBR,DisplayVersion | ConvertTo-Json -Compress)")
    report["build_revision"] = ubr["out"] or {"error": ubr["err"]}

    report["runtime"] = {
        "windows_sandbox_exe": str(exe),
        "windows_sandbox_exe_present": exe.is_file(),
    }

    # Feature state needs elevation. PowerShell returns exit code 0 even when the
    # cmdlet throws (the trailing expression still runs), so failure is detected
    # from an explicit marker, not from rc.
    features = {}
    for name in OPTIONAL_FEATURES:
        result = powershell(
            "$ErrorActionPreference='Stop'; "
            "try { $f = Get-WindowsOptionalFeature -Online -FeatureName " + name +
            " -ErrorAction Stop; 'OK|' + $f.FeatureName + '|' + $f.State } "
            "catch { 'ERROR|' + $_.Exception.Message; exit 2 }")
        marked = result["out"].startswith("OK|")
        features[name] = {
            "rc": result["rc"],
            "state": result["out"].split("|")[2] if marked else None,
            "error": None if marked else (result["out"] or result["err"])[:300],
        }
    report["optional_features"] = features
    feature_state_known = any(f["state"] for f in features.values())

    dism = powershell("dism /online /get-featureinfo /featurename:Containers-DisposableClientVM")
    report["dism_featureinfo"] = {"rc": dism["rc"],
                                  "out": dism["out"][:1500],
                                  "err": dism["err"][:800]}

    # Win32_OptionalFeature is readable without elevation, unlike
    # Get-WindowsOptionalFeature. InstallState: 1 enabled, 2 disabled,
    # 3 absent, 4 unknown. This distinguishes "feature present but off" from
    # "feature missing from the image", which the elevation error cannot.
    wmi_states = {}
    try:
        wmi = fetch_wmi_optional_features()
        for name, state in wmi.items():
            wmi_states[name] = {
                "install_state": state,
                "label": {1: "Enabled", 2: "Disabled", 3: "Absent", 4: "Unknown"}.get(state),
            }
    except (OSError, RuntimeError, ValueError) as exc:
        wmi_states = {"error": f"{type(exc).__name__}: {exc}"}
    report["wmi_optional_features"] = wmi_states
    if not feature_state_known:
        feature_state_known = any(
            isinstance(entry, dict) for entry in wmi_states.values()
        )

    who = powershell("whoami /groups")
    report["token"] = {
        "administrator_group_member": "S-1-5-32-544" in who["out"],
        "elevated": report["elevated"],
        "note": "membership is read from the token group list; a member of "
                "Administrators holding a medium-integrity token is UAC-filtered, "
                "so enabling the feature needs a consent prompt",
    }

    hyperv = powershell("systeminfo")
    report["systeminfo_hyperv_lines"] = [
        line.strip() for line in hyperv["out"].splitlines()
        if any(key.lower() in line.lower() for key in (
            "Hyper-V", "Virtualization", "Virtualisation", "Second Level",
            "Traduction d'adresses", "VM Monitor", "Moniteur de machine virtuelle",
            "Data Execution", "Prévention d'exécution"))
    ]

    computer_info, computer_info_raw = powershell_json(
        "Get-ComputerInfo -Property HyperVRequirementVirtualizationFirmwareEnabled,"
        "HyperVRequirementSecondLevelAddressTranslation,"
        "HyperVRequirementVMMonitorModeExtensions,HyperVRequirementDataExecutionPreventionAvailable,"
        "HyperVisorPresent,WindowsEditionId,WindowsVersion,OsHardwareAbstractionLayer"
    )
    report["computer_info"] = computer_info or {"error": computer_info_raw}

    bcd = powershell("bcdedit /enum '{current}'")
    report["bcdedit"] = {"rc": bcd["rc"], "err": bcd["err"][:400],
                         "hypervisor_launch_type": next(
                             (line.strip() for line in bcd["out"].splitlines()
                              if "hypervisorlaunchtype" in line.lower()), None)}

    # Windows 10 Pro support ended 2025-10-14. ESU enrolment is a licensing state
    # that is not reliably exposed locally, so record what is visible and say so.
    esu = powershell(
        "(Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ESU' "
        "-ErrorAction SilentlyContinue | ConvertTo-Json -Compress)")
    report["extended_security_updates"] = {
        "locally_verifiable": False,
        "note": "ESU enrolment is a licensing state; not established by these checks",
        "registry_probe": (esu["out"] or esu["err"] or "<empty>")[:300],
    }

    # --- classification ---------------------------------------------------
    def value(obj, key):
        return obj.get(key) if isinstance(obj, dict) else None

    total_ram = value(report["system"], "TotalPhysicalMemory")
    free_disk = value(report["disk_c"], "FreeSpace")
    firmware_virt = value(report["cpu"], "VirtualizationFirmwareEnabled")
    vm_ext = value(report["cpu"], "VMMonitorModeExtensions")
    slat = value(report["cpu"], "SecondLevelAddressTranslationExtensions")
    hypervisor = value(report["system"], "HypervisorPresent")
    logical = value(report["cpu"], "NumberOfLogicalProcessors")

    facts = {
        "firmware_virtualization_enabled": firmware_virt,
        "vm_monitor_mode_extensions": vm_ext,
        "second_level_address_translation": slat,
        "hypervisor_present": hypervisor,
        "logical_processors": logical,
        "ram_gib": round(total_ram / 1024 ** 3, 1) if isinstance(total_ram, int) else None,
        "free_disk_gib": round(free_disk / 1024 ** 3, 1) if isinstance(free_disk, int) else None,
        "feature_state_known": feature_state_known,
        "sandbox_exe_present": exe.is_file(),
        "elevated": report["elevated"],
        "administrator_group_member": report["token"]["administrator_group_member"],
    }
    sandbox_state = None
    entry = wmi_states.get("Containers-DisposableClientVM")
    if isinstance(entry, dict):
        sandbox_state = entry["install_state"]
    facts["sandbox_feature_install_state"] = sandbox_state
    facts["sandbox_feature_present"] = sandbox_state in (1, 2)
    report["facts"] = facts

    if facts["firmware_virtualization_enabled"] is False:
        classification = "BLOCKED_FIRMWARE_VIRTUALIZATION"
        reason = "firmware virtualization is disabled; enable VT-x/AMD-V in firmware"
    elif facts["vm_monitor_mode_extensions"] is False:
        classification = "BLOCKED_HARDWARE_REQUIREMENT"
        reason = "CPU does not expose VM monitor mode extensions"
    elif facts["second_level_address_translation"] is False:
        classification = "BLOCKED_HARDWARE_REQUIREMENT"
        reason = "CPU does not expose second-level address translation (EPT/NPT)"
    elif (facts["ram_gib"] or 0) < 4 or (facts["logical_processors"] or 0) < 2:
        classification = "BLOCKED_HARDWARE_REQUIREMENT"
        reason = "less than 4 GB RAM or fewer than 2 logical processors"
    elif sandbox_state == 3:
        classification = "BLOCKED_WINDOWS_FEATURE_OR_POLICY"
        reason = "the Windows Sandbox optional feature is absent from this image"
    elif sandbox_state == 1 and facts["sandbox_exe_present"]:
        classification = "SUPPORTED_AND_READY_TO_ENABLE"
        reason = "Windows Sandbox is already installed and enabled"
    elif not report["elevated"]:
        classification = "BLOCKED_PRIVILEGES"
        reason = ("the feature is present but disabled (Win32_OptionalFeature "
                  "InstallState=" + str(sandbox_state) + ") and enabling it requires an "
                  "elevated session; this session is UAC-filtered and UAC was not bypassed")
    else:
        classification = "SUPPORTED_AND_READY_TO_ENABLE"
        reason = "hardware prerequisites are satisfied and the feature is present; "
        reason += "the optional feature is not enabled"
    report["classification"] = classification
    report["classification_reason"] = reason
    report["recommended_command"] = (
        "Enable-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM "
        "-All -NoRestart"
    )
    report["recommended_command_note"] = (
        "Run from an elevated PowerShell session. No restart was performed by this "
        "diagnostic; a restart may be required before Windows Sandbox can start.")

    target = HERE / "sandbox-capability-2026-10-28.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    if args.attempt_enable:
        attempt = powershell(
            "$ErrorActionPreference='Stop'; "
            "try { $r = Enable-WindowsOptionalFeature -Online "
            "-FeatureName Containers-DisposableClientVM -All -NoRestart -ErrorAction Stop; "
            "'OK|' + $r.RestartNeeded } "
            "catch { 'ERROR|' + $_.Exception.Message; exit 2 }",
            timeout=1800,
        )
        ok = attempt["out"].startswith("OK|")
        record = {
            "command": "Enable-WindowsOptionalFeature -Online -FeatureName "
                       "Containers-DisposableClientVM -All -NoRestart",
            "elevated": report["elevated"],
            "applied": ok,
            "restart_required": (attempt["out"].split("|")[1] if ok else None),
            "rc": attempt["rc"],
            "output": (attempt["out"] or attempt["err"])[:2000],
            "note": "No restart was performed. A non-elevated session cannot apply this "
                    "change; UAC was not bypassed.",
        }
        (HERE / "sandbox-enable-attempt-2026-10-28.json").write_text(
            json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
        report["enable_attempt"] = {k: record[k] for k in
                                    ("applied", "restart_required", "rc", "output")}
        target.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps({"classification": classification, "reason": reason,
                      "facts": facts, "evidence": str(target)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
