from __future__ import annotations
import ast, difflib, hashlib, json, os, platform, re, subprocess, sys, zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "lc518-150" / "c9-execution-recovery"
ARCHIVE = REPO / "lc518_generator_scratch_GLM_review_v1.2.zip"
RUN_ID = os.environ.get("GITHUB_RUN_ID", "local")
ATTEMPT = os.environ.get("GITHUB_RUN_ATTEMPT", "1")
WORK = Path(os.environ.get("RUNNER_TEMP", str(REPO))) / f"lc518-recovery-work-{RUN_ID}-{ATTEMPT}"
REPORT = REPO / "lc518-github-recovery-report.json"
TEXT_REPORT = REPO / "lc518-github-recovery-report.txt"

ZIP_MEMBERS = {
    "EXECUTION_PROTOCOL_DRAFT_V1.2.md", "GENERATOR_HANDOFF.md", "TEST_RESULTS.txt",
    "execution_protocol_v1.json", "fixture_reproducibility.json", "SHA256SUMS",
    "lc518_generator.py", "lc518_launcher.py", "test_lc518_generator.py", "test_lc518_launcher.py",
}
EXPECTED_ZIP_FILES = {
    "lc518_generator.py": "6e4281b4bfd79783b53d93e132a538dc3d120177405e44012081c6db083c0e2f",
    "lc518_launcher.py": "c23115b54061cdd490e0d6f87e31e5a067d4ab99d5c4677de19e92ce64eb24a2",
    "test_lc518_generator.py": "d6a322bc9c28a9c5537f89a1bb6395bf52a44f79293c07b4f526ad985dfcdf64",
    "test_lc518_launcher.py": "febd27e1fd98ed9d27d6e802e50704fa278b504ba2d6555bbab81d0c091953b0",
}
EXPECTED_EXTERNAL = {
    "lc518_generator_state1.py": "276b9f49f5a3a975c530cc4eca02b0a0f3407ab824d12031f43175a72feb14fe",
    "lc518_generator_state2.py": "1335a42d06d64cf7e847981fc68eee07945655128e82e7f08bc43e774d1cb41c",
    "activation_diff.txt": "578d17163701d549d17c19e5e1a785709fd1d08bf3572b77ac7058fbc13c8a64",
    "execution_protocol_v1.md": "64e7f5033eac5dec3d7278bd48695ffe42b19fc047bd79f14145c49f3a45e293",
}
STATE1_AUTH = "BANK_GENERATION_AUTHORIZED = False"
STATE2_AUTH = "BANK_GENERATION_AUTHORIZED = True"
BASE_OUTPUT = "OUTPUT_DIR: str | None = None"
CONFIGURED_OUTPUT = 'OUTPUT_DIR: str | None = "/home/z/lc518_run/bank"'

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def parse_sums(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, f"Malformed SHA256SUMS row: {line!r}")
        digest, name = match.groups()
        require(name not in result, f"Duplicate SHA256SUMS entry: {name}")
        result[name] = digest
    return result

def verify_archive():
    require(ARCHIVE.is_file(), f"Missing repository ZIP: {ARCHIVE}")
    archive_hash = sha256_file(ARCHIVE)
    log = (PACKAGE / "VERIFICATION_LOG.md").read_text(encoding="utf-8")
    match = re.search(r"Source of generator bytes:.*?SHA-256 \`([0-9a-f]{64})\`", log)
    require(match is not None, "Verification log does not declare the source ZIP digest")
    declared_hash = match.group(1)
    require(archive_hash == declared_hash, f"ZIP digest mismatch: actual={archive_hash}; log={declared_hash}")
    WORK.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(ARCHIVE) as zf:
        names = zf.namelist()
        require(len(names) == len(set(names)), "ZIP contains duplicate member paths")
        require(set(names) == ZIP_MEMBERS,
                f"ZIP inventory mismatch: extra={sorted(set(names)-ZIP_MEMBERS)}, missing={sorted(ZIP_MEMBERS-set(names))}")
        for info in zf.infolist():
            target = (WORK / info.filename).resolve()
            require(WORK.resolve() in target.parents, f"Unsafe ZIP path: {info.filename}")
            require(not info.is_dir(), f"Unexpected directory member: {info.filename}")
        zf.extractall(WORK)
    sums = parse_sums(WORK / "SHA256SUMS")
    require(len(sums) == 9, f"Expected 9 internal checksum rows, got {len(sums)}")
    actual_names = {p.name for p in WORK.iterdir() if p.is_file() and p.name != "SHA256SUMS"}
    require(actual_names == set(sums),
            f"Internal inventory mismatch: extra={sorted(actual_names-set(sums))}, missing={sorted(set(sums)-actual_names)}")
    rows = []
    for name, expected in sorted(sums.items()):
        actual = sha256_file(WORK / name)
        rows.append({"file": name, "expected_sha256": expected, "actual_sha256": actual, "ok": actual == expected})
    require(all(row["ok"] for row in rows), "At least one ZIP-internal checksum failed")
    for name, expected in EXPECTED_ZIP_FILES.items():
        require(sums.get(name) == expected, f"Unexpected pinned digest for ZIP member {name}")
    return rows, archive_hash, declared_hash

def verify_external_package():
    manifest = parse_sums(PACKAGE / "SHA256SUMS")
    require(manifest == EXPECTED_EXTERNAL, "External package SHA256SUMS differs from pinned manifest")
    rows = []
    for name, expected in sorted(manifest.items()):
        actual = sha256_file(PACKAGE / name)
        rows.append({"file": name, "expected_sha256": expected, "actual_sha256": actual, "ok": actual == expected})
    require(all(row["ok"] for row in rows), "External package checksum failure")
    state1 = (PACKAGE / "lc518_generator_state1.py").read_text(encoding="utf-8")
    state2 = (PACKAGE / "lc518_generator_state2.py").read_text(encoding="utf-8")
    base = (WORK / "lc518_generator.py").read_text(encoding="utf-8")
    diff = (PACKAGE / "activation_diff.txt").read_text(encoding="utf-8")
    require(state1.count(STATE1_AUTH) == 1 and state2.count(STATE2_AUTH) == 1,
            "Generator authorization literals differ from declared states")
    require(state1.count(CONFIGURED_OUTPUT) == 1 and base.count(BASE_OUTPUT) == 1,
            "Generator output-path transition is not unique")
    require(base.replace(BASE_OUTPUT, CONFIGURED_OUTPUT, 1) == state1,
            "State 1 is not exactly the documented output-path-only change from ZIP generator")
    require(state1.replace(STATE1_AUTH, STATE2_AUTH, 1) == state2,
            "State 2 is not exactly the one-line authorization activation from state 1")
    expected_diff = "".join(difflib.unified_diff(
        state1.splitlines(keepends=True), state2.splitlines(keepends=True),
        fromfile="lc518_generator_state1.py", tofile="lc518_generator_state2.py", n=3))
    require(diff == expected_diff, "activation_diff.txt is not the exact state1-to-state2 unified diff")
    compile(state1, "lc518_generator_state1.py", "exec")
    compile(state2, "lc518_generator_state2.py", "exec")
    return rows

def main():
    require(sys.version_info[:3] == (3, 13, 5), f"Expected CPython 3.13.5; got {sys.version}")
    zip_rows, archive_hash, declared_hash = verify_archive()
    external_rows = verify_external_package()
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "test_lc518_generator", "test_lc518_launcher"],
        cwd=WORK, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    test_log = WORK / "RECOVERY_TEST_RERUN.txt"
    test_log.write_text(tests.stdout, encoding="utf-8")
    test_summary = re.search(r"Ran (\d+) tests? in ([0-9.]+)s", tests.stdout)
    require(tests.returncode == 0, f"Synthetic acceptance tests failed (exit {tests.returncode}); see {test_log}")
    require(test_summary is not None and int(test_summary.group(1)) == 51,
            "Synthetic acceptance suite did not report exactly 51 tests")
    interpreter = Path(sys.executable).resolve()
    fingerprint = {
        "python_executable": str(interpreter), "sys_version": sys.version,
        "version_info": list(sys.version_info[:3]), "platform": platform.platform(),
        "python_implementation": platform.python_implementation(),
        "interpreter_sha256": sha256_file(interpreter),
        "runner_os": os.environ.get("RUNNER_OS"), "runner_image": os.environ.get("ImageOS"),
        "runner_image_version": os.environ.get("ImageVersion"),
        "github_workspace": os.environ.get("GITHUB_WORKSPACE"), "runner_temp": os.environ.get("RUNNER_TEMP"),
        "github_run_id": RUN_ID, "github_run_attempt": ATTEMPT,
    }
    report = {
        "result": "RECOVERY_PREFLIGHT_PASS",
        "scope": "archive integrity, external state-chain integrity, synthetic tests, and runner fingerprint only",
        "archive_sha256": archive_hash, "archive_sha256_matches_uploaded_verification_log": archive_hash == declared_hash,
        "zip_member_count": len(ZIP_MEMBERS), "zip_internal_checksums": zip_rows,
        "external_package_checksums": external_rows,
        "synthetic_tests": {"count": int(test_summary.group(1)), "elapsed_seconds": float(test_summary.group(2)),
                            "exit_code": tests.returncode, "log_file": str(test_log)},
        "github_runner": fingerprint,
        "supplied_execution_protocol_compatible_with_github_runner": False,
        "protocol_blocker": "The protocol pins /usr/bin/python3.13, a Kangaroo Linux platform, and /home/z/lc518_run. It is not configured for GitHub-hosted Ubuntu 24.04.",
        "state1_compiled_only": True, "state2_compiled_only": True,
        "state1_or_state2_executed": False, "bank_generation_performed": False,
        "solver_code_executed": False,
        "authorization_warning": "State 2 contains BANK_GENERATION_AUTHORIZED=True; it was never imported or executed.",
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    TEXT_REPORT.write_text(
        "LC518 GITHUB RECOVERY PREFLIGHT\n"
        f"RESULT: {report['result']}\nZIP SHA-256: {archive_hash}\n"
        f"ZIP internal checksum rows: {len(zip_rows)}; all pass\n"
        f"External package checksum rows: {len(external_rows)}; all pass\n"
        f"Synthetic tests: {test_summary.group(1)}/51 pass (exit 0)\n"
        f"Runner Python: {fingerprint['python_executable']}\n"
        f"Runner sys.version: {fingerprint['sys_version']}\n"
        f"Runner platform: {fingerprint['platform']}\n"
        f"Runner image: {fingerprint['runner_image']} {fingerprint['runner_image_version']}\n"
        f"Runner interpreter SHA-256: {fingerprint['interpreter_sha256']}\n"
        "Supplied protocol compatible with this GitHub runner: NO\n"
        "STATE1/STATE2 EXECUTED: NO\nBANK GENERATED: NO\nSOLVER CODE EXECUTED: NO\n"
        "GENERATION STATUS: HOLD; a GitHub-specific protocol and a new locked hash chain are required\n",
        encoding="utf-8")
    print(TEXT_REPORT.read_text(encoding="utf-8"))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
