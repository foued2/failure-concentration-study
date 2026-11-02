from __future__ import annotations

import ast
import hashlib
import json
import platform
import re
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ARCHIVE = REPO / "lc518_generator_scratch_GLM_review_v1.2.zip"
WORK = Path("lc518-recovery-work").resolve()
REPORT = Path("lc518-recovery-introspection.txt")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            target = (destination / info.filename).resolve()
            if destination.resolve() not in target.parents and target != destination.resolve():
                raise RuntimeError(f"Unsafe ZIP member path: {info.filename}")
        zf.extractall(destination)


def assignment_report(path: Path, names: set[str]) -> str:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    rows = []
    for node in ast.walk(tree):
        targets = []
        value = None
        if isinstance(node, ast.Assign):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            value = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            targets = [node.target.id]
            value = node.value
        hit = sorted(set(targets) & names)
        if hit:
            rows.append((node.lineno, hit, ast.unparse(value) if value is not None else "<no value>"))
    out = [f"FILE: {path.name}", "ASSIGNMENTS:"]
    out.extend(f"  line {line}: {', '.join(hit)} = {value}" for line, hit, value in sorted(rows))
    lines = source.splitlines()
    out.append("SOURCE CONTEXT:")
    for i, line in enumerate(lines, start=1):
        if any(re.search(r"\b" + re.escape(n) + r"\b", line) for n in names):
            lo, hi = max(1, i - 1), min(len(lines), i + 2)
            out.append(f"  -- lines {lo}-{hi} --")
            out.extend(f"  {j}: {lines[j-1]}" for j in range(lo, hi + 1))
    return "\n".join(out)


def main() -> None:
    if not ARCHIVE.is_file():
        raise SystemExit(f"Missing archive: {ARCHIVE}")
    WORK.mkdir(parents=True, exist_ok=True)
    safe_extract(ARCHIVE, WORK)

    sums_path = WORK / "SHA256SUMS"
    if not sums_path.is_file():
        raise SystemExit("ZIP does not contain SHA256SUMS")
    expected = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise SystemExit(f"Malformed SHA256SUMS row: {line!r}")
        digest, filename = match.groups()
        if filename in expected:
            raise SystemExit(f"Duplicate SHA256SUMS filename: {filename}")
        expected[filename] = digest
    if len(expected) != 9:
        raise SystemExit(f"Expected 9 checksum rows, found {len(expected)}")
    actual_names = {p.name for p in WORK.iterdir() if p.is_file() and p.name != "SHA256SUMS"}
    if actual_names != set(expected):
        raise SystemExit(f"Checksum inventory mismatch. extra={sorted(actual_names-set(expected))}, missing={sorted(set(expected)-actual_names)}")
    checks = []
    for filename, digest in sorted(expected.items()):
        got = sha256(WORK / filename)
        checks.append((filename, digest, got, got == digest))
    if not all(x[3] for x in checks):
        raise SystemExit("At least one ZIP checksum failed")

    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "test_lc518_generator", "test_lc518_launcher"],
        cwd=WORK, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    (WORK / "RECOVERY_TEST_RERUN.txt").write_text(tests.stdout, encoding="utf-8")
    if tests.returncode:
        raise SystemExit(f"Artificial test suite failed with exit code {tests.returncode}")

    names = {
        "OUTPUT_DIR", "BANK_GENERATION_AUTHORIZED", "PROTOCOL_SHA256",
        "EXPECTED_GENERATOR_SHA256", "EXPECTED_GENERATOR_PATH",
        "EXPECTED_TEST_SUITE_SHA256S", "EXPECTED_PYTHON_VERSION",
        "EXPECTED_PYTHON_EXECUTABLE", "EXPECTED_SYS_VERSION",
        "EXPECTED_PLATFORM", "EXPECTED_INTERPRETER_SHA256",
        "RUN_ROOT", "PROTOCOL_PATH", "GENERATOR_PATH",
    }
    gen_report = assignment_report(WORK / "lc518_generator.py", names)
    launcher_report = assignment_report(WORK / "lc518_launcher.py", names)
    draft = (WORK / "EXECUTION_PROTOCOL_DRAFT_V1.2.md").read_text(encoding="utf-8")
    marker = "## 13. Generator authorization activation and final hash chain (OPEN)"
    section13 = draft[draft.find(marker):] if marker in draft else "SECTION 13 NOT FOUND"
    json_obj = json.loads((WORK / "execution_protocol_v1.json").read_text(encoding="utf-8"))

    fingerprint = {
        "python_executable": str(Path(sys.executable).resolve()),
        "sys_version": sys.version,
        "platform": platform.platform(),
        "python_implementation": platform.python_implementation(),
        "version_info": list(sys.version_info[:3]),
        "interpreter_sha256": sha256(Path(sys.executable).resolve()),
        "runner_os": __import__("os").environ.get("RUNNER_OS"),
        "runner_image": __import__("os").environ.get("ImageOS"),
        "runner_image_version": __import__("os").environ.get("ImageVersion"),
    }

    report = [
        "LC518 GitHub recovery introspection",
        f"archive_path={ARCHIVE}",
        f"archive_size={ARCHIVE.stat().st_size}",
        f"archive_sha256={sha256(ARCHIVE)}",
        f"zip_members={len(zipfile.ZipFile(ARCHIVE).namelist())}",
        "",
        "CHECKSUMS:",
        *[f"{'OK' if ok else 'FAIL'} {name} {got}" for name, want, got, ok in checks],
        "",
        "TEST RERUN:",
        tests.stdout,
        "",
        "GITHUB RUNNER FINGERPRINT:",
        json.dumps(fingerprint, indent=2, sort_keys=True),
        "",
        "GENERATOR CONFIGURATION:",
        gen_report,
        "",
        "LAUNCHER CONFIGURATION:",
        launcher_report,
        "",
        "PROTOCOL SECTION 13:",
        section13,
        "",
        "PROTOCOL JSON PENDING FIELDS:",
        json.dumps(json_obj.get("pending_owner_fields"), indent=2),
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    print(f"\nRECOVERY_INTROSPECTION_REPORT={REPORT}")
    print(f"ARTIFACT_SOURCE_DIR={WORK}")
    print("NO_BANK_GENERATION=TRUE")


if __name__ == "__main__":
    main()
