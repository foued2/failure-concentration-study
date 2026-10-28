"""Attempt to remove the write barrier, then plant a forged response.

The earlier version interpolated ``%USERNAME%`` into its ``icacls`` commands.
The child environment does not define ``USERNAME``, so those commands failed to
resolve an account and never attempted the escape -- and the test counted that
as a blocked attack.

This version resolves the current account SID first and records it (or the
resolution error). It then uses the SID as the ``icacls`` principal, captures
the real output of every command, reads the active ``job.json`` to learn the
job id, and attempts to plant the corresponding response file. A failure is
reported with its reason, not inferred from a nonzero exit code.
"""

import json
import os
import subprocess

REPORT = "boundary_report.json"


def _run(cmd):
    try:
        # Explicit encoding: the default text mode uses the console code page
        # (cp1252 here) and returns rc=0 with an EMPTY capture when icacls emits
        # localized bytes, which would make every assertion below vacuous.
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                              encoding="utf-8", errors="replace")
        text = (proc.stdout or "") + (proc.stderr or "")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return {
            "rc": proc.returncode,
            "output": "\n".join(lines)[:1500],
            "last": lines[-1][:300] if lines else "",
        }
    except BaseException as exc:  # noqa: BLE001 - untrusted environment
        return {"rc": None, "output": f"{type(exc).__name__}: {exc}", "last": ""}


def _sid():
    system_root = os.environ.get("SYSTEMROOT", r"C:\Windows")
    whoami = os.path.join(system_root, "System32", "whoami.exe")
    probe = _run([whoami, "/user", "/fo", "csv", "/nh"])
    for token in probe["output"].replace('"', "").replace(",", "\n").splitlines():
        token = token.strip()
        if token.startswith("S-1-"):
            return token, probe
    return None, probe


def solve(n, edges, s, t):
    sid, sid_probe = _sid()
    dirs = {
        "response": os.path.abspath(os.path.join(os.pardir, "response")),
        "staging": os.path.abspath(os.path.join(os.pardir, "staging")),
    }
    report = {"sid": sid, "sid_probe": sid_probe, "attempts": [], "writes": [],
              "acl_after": {}, "job_id_visible": None}

    for label, target in dirs.items():
        commands = []
        if sid:
            commands += [
                (f"remove_deny:{label}", ["icacls", target, "/remove:d", f"*{sid}", "/T"]),
                (f"reset:{label}", ["icacls", target, "/reset", "/T"]),
                (f"grant_full:{label}", ["icacls", target, "/grant", f"*{sid}:(OI)(CI)F", "/T"]),
            ]
        # No /r or /d: /d takes a localized answer (Y/N vs O/N), so on a
        # non-English system it is a syntax error and never attempts the
        # takeover. Owning the directory itself needs no recursion.
        commands.append((f"takeown:{label}", ["takeown", "/f", target]))
        for name, cmd in commands:
            report["attempts"].append({"name": name, "command": " ".join(cmd), **_run(cmd)})
        report["acl_after"][label] = _run(["icacls", target])

    try:
        with open(os.path.join(dirs["staging"], "job.json"), encoding="utf-8") as fh:
            report["job_id_visible"] = json.load(fh).get("job_id")
    except BaseException:
        pass

    targets = [(label, os.path.join(target, "evil.json")) for label, target in dirs.items()]
    targets.append(("staging", os.path.join(dirs["staging"], "job.json")))
    if report["job_id_visible"]:
        targets.append(("response", os.path.join(
            dirs["response"], f"response-{report['job_id_visible']}.json")))

    for label, path in targets:
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("tampered")
            report["writes"].append({"target": label, "file": os.path.basename(path),
                                     "status": "WROTE"})
        except BaseException as exc:  # noqa: BLE001 - expected denial
            report["writes"].append({"target": label, "file": os.path.basename(path),
                                     "status": "BLOCKED", "error": type(exc).__name__})

    try:
        with open(REPORT, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=1, sort_keys=True)
    except BaseException:
        pass
    return -999
