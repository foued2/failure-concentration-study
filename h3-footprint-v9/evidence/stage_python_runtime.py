"""Stage a pinned, officially verified CPython embeddable distribution.

The V9 preflight maps a *portable* interpreter into Windows Sandbox read-only.
A normal install is not relocatable and a venv keeps host paths, so the only
supported source is the embeddable package from python.org.

This script refuses to stage anything it cannot verify:

1. it reads the official release metadata from python.org's own API and takes
   the published SHA-256 and file size for the exact file it is about to fetch,
   not a hash copied into this repository;
2. it downloads that URL, hashes what arrived, and compares size and SHA-256;
3. only on a match does it extract, then runs ``interpreter_preflight`` and a
   short smoke test with the staged interpreter.

A mismatch deletes the download and exits non-zero. Nothing is extracted.

    python evidence/stage_python_runtime.py --dest C:\\v9-stage\\py-embed

Exit codes: 0 staged and verified; 2 hash/size mismatch; 3 metadata or download
failure; 4 interpreter preflight failed; 5 destination not empty.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
V9 = HERE.parent
sys.path.insert(0, str(V9))

import backend  # noqa: E402

# Pinned on 2026-10-28. 3.13.18 was source-only (no Windows binaries), so the
# newest 64-bit embeddable package with published release metadata is 3.14.10.
PINNED_RELEASE = "3.14.10"
PINNED_FILE = "python-3.14.10-embed-amd64.zip"

API_RELEASE = "https://www.python.org/api/v2/downloads/release/"
API_RELEASE_FILE = "https://www.python.org/api/v2/downloads/release_file/"


def fetch_json(url: str, timeout: int = 60):
    request = urllib.request.Request(url, headers={"User-Agent": "h3-v9-preflight/1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def official_metadata(release: str, filename: str) -> dict:
    releases = fetch_json(API_RELEASE + "?name=" + urllib.parse.quote(f"Python {release}"))
    if not releases:
        raise RuntimeError(f"python.org has no release named Python {release}")
    release_record = releases[0]
    release_id = release_record["resource_uri"].rstrip("/").rsplit("/", 1)[-1]
    files = fetch_json(f"{API_RELEASE_FILE}?release={release_id}")

    match = None
    for item in files:
        if item["url"].rsplit("/", 1)[-1] == filename:
            match = item
            break
    if match is None:
        raise RuntimeError(
            f"python.org lists no file {filename!r} for Python {release}; "
            f"available: {[f['url'].rsplit('/', 1)[-1] for f in files]}"
        )
    if not match.get("sha256_sum"):
        raise RuntimeError("python.org publishes no SHA-256 for this file; refusing to stage")
    return {
        "release": release,
        "release_date": release_record.get("release_date"),
        "release_api": release_record["resource_uri"],
        "file_api": match["resource_uri"],
        "url": match["url"],
        "name": match["name"],
        "published_sha256": match["sha256_sum"],
        "published_filesize": match["filesize"],
        "gpg_signature_file": match.get("gpg_signature_file"),
    }


def download(url: str, target: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    request = urllib.request.Request(url, headers={"User-Agent": "h3-v9-preflight/1"})
    with urllib.request.urlopen(request, timeout=300) as response, open(target, "wb") as fh:
        while True:
            chunk = response.read(256 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            fh.write(chunk)
            total += len(chunk)
    return digest.hexdigest(), total


def tree_manifest(root: Path) -> list[dict]:
    entries = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            entries.append({
                "path": str(path.relative_to(root)).replace("\\", "/"),
                "size": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    return entries


def smoke_test(python_exe: Path, cwd: Path) -> dict:
    import subprocess

    code = ("import json,sys;"
            "print(json.dumps({'implementation':sys.implementation.name,"
            "'version':sys.version,'executable':sys.executable}))")
    try:
        proc = subprocess.run(
            [str(python_exe), "-c", code],
            capture_output=True, text=True, timeout=120, cwd=str(cwd),
            encoding="utf-8", errors="replace",
        )
        return {"rc": proc.returncode, "stdout": proc.stdout.strip()[:500],
                "stderr": proc.stderr.strip()[:500]}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"rc": None, "error": f"{type(exc).__name__}: {exc}"}


def agent_start_check(python_exe: Path) -> dict:
    """Can the staged interpreter actually start the Sandbox agent?

    Host-only. The agent is started with ``--allow-host``, so the record proves
    the embeddable layout can import the runtime and echo a nonce; it is *not*
    Sandbox evidence, and the handshake is explicitly marked untrusted.
    The agent is started before session.json exists, which also exercises the
    polling order.
    """
    import subprocess
    import tempfile
    import uuid

    work = Path(tempfile.mkdtemp(prefix="v9-agent-start-"))
    inbox, outbox = work / "in", work / "out"
    inbox.mkdir(parents=True, exist_ok=True)
    outbox.mkdir(parents=True, exist_ok=True)
    for name in ("sandbox_agent.py", "protocol.py", "supervisor.py",
                 "winjob.py", "child_runner.py"):
        shutil.copy2(V9 / name, inbox / name)

    nonce = uuid.uuid4().hex
    proc = subprocess.Popen(
        [str(python_exe), "-I", str(inbox / "sandbox_agent.py"),
         "--inbox", str(inbox), "--outbox", str(outbox),
         "--handshake-only", "--allow-host", "--session-timeout", "30"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace",
    )
    result: dict = {"note": "host-only check of the staged interpreter; "
                            "inside_sandbox is false and the handshake is not evidence"}
    try:
        time.sleep(1.0)
        result["agent_alive_before_session"] = proc.poll() is None
        (inbox / "session.json").write_text(
            json.dumps({"v9": 1, "nonce": nonce}), encoding="utf-8")
        hello_path = outbox / "hello.json"
        deadline = time.monotonic() + 25
        while time.monotonic() < deadline and not hello_path.exists():
            time.sleep(0.1)
        result["handshake_written"] = hello_path.exists()
        if hello_path.exists():
            hello = json.loads(hello_path.read_text(encoding="utf-8"))
            result.update({
                "nonce_match": hello.get("nonce") == nonce,
                "mode": hello.get("mode"),
                "inside_sandbox": hello.get("inside_sandbox"),
                "user": hello.get("user"),
                "source": hello.get("source"),
                "pid_present": isinstance(hello.get("pid"), int),
            })
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
        result["exit_code"] = proc.returncode
    finally:
        if proc.poll() is None:
            proc.kill()
        stdout, stderr = proc.communicate(timeout=15)
        result["stdout"] = (stdout or "").strip()[:300]
        result["stderr"] = (stderr or "").strip()[:300]
        shutil.rmtree(work, ignore_errors=True)
    return result


def serve_check(python_exe: Path) -> dict:
    """Drive one harmless job through the guest-side runtime, on the host.

    Uses the staged embeddable interpreter to run ``sandbox_agent.py`` in serve
    mode against a hand-authored fixture. This proves the interpreter can import
    the runtime, spawn the child with ``-I``, enforce the Job Object and write a
    response. It is host evidence only: the agent runs with ``--allow-host`` and
    reports ``inside_sandbox: false``.
    """
    import subprocess
    import tempfile

    import backend as backend_module
    import controller as controller_module
    import protocol as protocol_module

    work = Path(tempfile.mkdtemp(prefix="v9-serve-check-"))
    inbox, outbox, scratch = work / "in", work / "out", work / "scratch"
    for path in (inbox, outbox, scratch):
        path.mkdir(parents=True, exist_ok=True)
    for name in ("sandbox_agent.py", "protocol.py", "supervisor.py",
                 "winjob.py", "child_runner.py"):
        shutil.copy2(V9 / name, inbox / name)

    result: dict = {"note": "host-only integration check of the staged interpreter; "
                            "not Sandbox evidence"}
    ctl = controller_module.Controller(
        work / "ctl", transport=backend_module.HostLocalTransport(work / "rt"))
    body = (V9 / "tests" / "fixtures" / "echo_input.py").read_bytes()
    job = ctl._publish(inbox, body, "system", None,
                       {"n": 7, "edges": [], "s": 0, "t": 0})
    result["job_id"] = job["job_id"]
    (inbox / "session.json").write_text(
        json.dumps({"v9": protocol_module.JOB_SCHEMA, "nonce": "serve-check"}),
        encoding="utf-8")

    proc = subprocess.Popen(
        [str(python_exe), "-I", str(inbox / "sandbox_agent.py"),
         "--inbox", str(inbox), "--outbox", str(outbox), "--scratch", str(scratch),
         "--allow-host", "--max-jobs", "1", "--timeout", "10"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace",
    )
    try:
        response_path = protocol_module.response_path(outbox, job["job_id"])
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline and not response_path.exists():
            if proc.poll() is not None and not response_path.exists():
                break
            time.sleep(0.1)
        result["response_written"] = response_path.exists()
        if response_path.exists():
            record = backend_module.read_trusted_response(response_path, job["job_id"])
            result.update({
                "status": record["status"],
                "answer": record.get("answer"),
                "tree_empty": record["tree_empty"],
                "body_sha256_matches": record["body_sha256"] == protocol_module.sha256_bytes(body),
            })
        try:
            proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            proc.kill()
        result["exit_code"] = proc.returncode
    except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
        result["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if proc.poll() is None:
            proc.kill()
        stdout, stderr = proc.communicate(timeout=15)
        result["stdout"] = (stdout or "").strip()[:300]
        result["stderr"] = (stderr or "").strip()[:300]
        shutil.rmtree(work, ignore_errors=True)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", required=True,
                        help="directory to extract the embeddable distribution into")
    parser.add_argument("--release", default=PINNED_RELEASE)
    parser.add_argument("--file", default=PINNED_FILE)
    parser.add_argument("--evidence", default=str(HERE / "python-runtime-2026-10-28.json"))
    args = parser.parse_args()

    report: dict = {
        "stage": "python-runtime",
        "pinned_release": args.release,
        "pinned_file": args.file,
        "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "verified": False,
        "staged": False,
    }
    evidence_path = Path(args.evidence)
    dest = Path(args.dest)

    def finish(code: int, error: str | None = None) -> int:
        if error:
            report["error"] = error
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        evidence_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return code

    try:
        metadata = official_metadata(args.release, args.file)
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        return finish(3, f"official metadata unavailable: {type(exc).__name__}: {exc}")
    report["official_metadata"] = metadata

    if dest.exists() and any(dest.iterdir()):
        return finish(5, f"destination {dest} is not empty; refusing to overwrite")

    download_path = evidence_path.parent / (args.file + ".part")
    download_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        computed, size = download(metadata["url"], download_path)
    except (OSError, urllib.error.URLError) as exc:
        download_path.unlink(missing_ok=True)
        return finish(3, f"download failed: {type(exc).__name__}: {exc}")

    report["download"] = {
        "url": metadata["url"],
        "computed_sha256": computed,
        "computed_filesize": size,
        "published_sha256": metadata["published_sha256"],
        "published_filesize": metadata["published_filesize"],
        "sha256_match": computed == metadata["published_sha256"],
        "size_match": size == metadata["published_filesize"],
    }
    if not (computed == metadata["published_sha256"] and size == metadata["published_filesize"]):
        download_path.unlink(missing_ok=True)
        return finish(2, "the downloaded file does not match the published SHA-256/size; "
                          "nothing was extracted")
    report["verified"] = True

    try:
        dest.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(download_path) as archive:
            names = archive.namelist()
            bad = [n for n in names if n.startswith(("/", "\\")) or ".." in Path(n).parts]
            if bad:
                raise RuntimeError(f"archive contains unsafe paths: {bad[:5]}")
            archive.extractall(dest)
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        download_path.unlink(missing_ok=True)
        shutil.rmtree(dest, ignore_errors=True)
        return finish(3, f"extraction failed: {type(exc).__name__}: {exc}")
    finally:
        download_path.unlink(missing_ok=True)

    report["staged"] = True
    report["staged_at"] = str(dest)
    report["files"] = tree_manifest(dest)

    preflight = backend.interpreter_preflight(dest)
    report["interpreter_preflight"] = preflight
    report["smoke_test"] = smoke_test(dest / "python.exe", dest)
    report["agent_start_check"] = agent_start_check(dest / "python.exe")
    report["serve_check"] = serve_check(dest / "python.exe")

    pth = sorted(dest.glob("python*._pth"))
    report["pth_files"] = {p.name: p.read_text(encoding="utf-8", errors="replace")
                           for p in pth}

    if not preflight["ok"]:
        return finish(4, "staged interpreter failed interpreter_preflight")
    if report["smoke_test"].get("rc") != 0:
        return finish(4, "staged interpreter did not run a trivial program")
    agent = report["agent_start_check"]
    if not (agent.get("agent_alive_before_session") and agent.get("handshake_written")
            and agent.get("nonce_match") and agent.get("mode") == "preflight"
            and agent.get("exit_code") == 0):
        return finish(4, "the staged interpreter could not start the Sandbox agent")
    served = report["serve_check"]
    if not (served.get("response_written") and served.get("status") == "ok"
            and served.get("answer") == 7 and served.get("tree_empty") is True
            and served.get("body_sha256_matches") and served.get("exit_code") == 0):
        return finish(4, "the staged interpreter could not run one job end to end")
    return finish(0)


if __name__ == "__main__":
    raise SystemExit(main())
