from __future__ import annotations

import difflib
import hashlib
import json
import os
import platform
import re
import shutil
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCE_ZIP = REPO / "lc518_generator_scratch_GLM_review_v1.2.zip"
PACKAGE = REPO / "lc518-150" / "c9-github-execution"

EXPECTED_RUNNER = {
    "python_executable": "/opt/hostedtoolcache/Python/3.13.5/x64/bin/python3.13",
    "sys_version": "3.13.5 (main, Jun 12 2025, 03:51:07) [GCC 13.3.0]",
    "platform": "Linux-7.0.0-1017-azure-x86_64-with-glibc2.39",
    "interpreter_sha256": "9cf89c50189de85411dd34b0f0ec5daaab41bf6cd447628572defe3b3ffd0a04",
    "image_os": "ubuntu24",
    "image_version": "20261026.354.1",
    "workspace": "/home/runner/work/failure-concentration-study/failure-concentration-study",
}
BASE_GENERATOR_SHA256 = "6e4281b4bfd79783b53d93e132a538dc3d120177405e44012081c6db083c0e2f"
GENERATOR_TEST_SHA256 = "d6a322bc9c28a9c5537f89a1bb6395bf52a44f79293c07b4f526ad985dfcdf64"

def hbytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def hfile(path: Path) -> str:
    return hbytes(path.read_bytes())

def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def replace_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    need(count == 1, f"{label}: expected exactly one occurrence, found {count}")
    return source.replace(old, new, 1)

def main() -> int:
    need(sys.version_info[:3] == (3, 13, 5), f"Python version mismatch: {sys.version}")
    interpreter = Path(sys.executable).resolve()
    observed = {
        "python_executable": str(interpreter),
        "sys_version": sys.version,
        "platform": platform.platform(),
        "interpreter_sha256": hfile(interpreter),
        "image_os": os.environ.get("ImageOS"),
        "image_version": os.environ.get("ImageVersion"),
        "workspace": str(Path(os.environ.get("GITHUB_WORKSPACE", "")).resolve()),
    }
    need(observed == EXPECTED_RUNNER,
         "GitHub runner fingerprint drifted; refusing to mint a new protocol:\n"
         + json.dumps({"expected": EXPECTED_RUNNER, "observed": observed}, indent=2, sort_keys=True))
    workspace = Path(observed["workspace"])
    need(workspace.is_dir() and workspace == REPO.resolve(), "GITHUB_WORKSPACE is not the checked-out repository root")
    run_root = workspace / "lc518_run"
    output_dir = run_root / "bank"
    need(not run_root.exists(), f"Run root already exists; refusing reuse: {run_root}")
    need(run_root.parent.is_dir(), "RUN_ROOT parent must already exist")

    build_root = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "lc518-gh-package-build"
    if build_root.exists():
        shutil.rmtree(build_root)
    build_root.mkdir(parents=True)
    with zipfile.ZipFile(SOURCE_ZIP) as zf:
        names = zf.namelist()
        need(len(names) == 10 and len(set(names)) == 10, "Unexpected source ZIP inventory")
        for member in names:
            target = (build_root / member).resolve()
            need(build_root.resolve() in target.parents, f"Unsafe ZIP path: {member}")
        zf.extractall(build_root)

    source_sums = {}
    for line in (build_root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        need(match is not None, f"Malformed source checksum row: {line!r}")
        source_sums[match.group(2)] = match.group(1)
    need(len(source_sums) == 9, "Source archive must have exactly nine internal checksum entries")
    for name, expected in source_sums.items():
        need(hfile(build_root / name) == expected, f"Source archive checksum failed: {name}")
    need(source_sums["lc518_generator.py"] == BASE_GENERATOR_SHA256, "Review generator hash mismatch")

    base_generator = (build_root / "lc518_generator.py").read_text(encoding="utf-8")
    generator_state1 = replace_once(
        base_generator,
        "OUTPUT_DIR: str | None = None",
        f'OUTPUT_DIR: str | None = "{output_dir}"',
        "generator output path",
    )
    need("BANK_GENERATION_AUTHORIZED = False" in generator_state1, "Configured generator unexpectedly unlocked")
    generator_state2 = replace_once(
        generator_state1, "BANK_GENERATION_AUTHORIZED = False",
        "BANK_GENERATION_AUTHORIZED = True", "generator activation",
    )
    generator_state1_sha = hbytes(generator_state1.encode())
    generator_state2_sha = hbytes(generator_state2.encode())

    generator_tests = (build_root / "test_lc518_generator.py").read_text(encoding="utf-8")
    need(hbytes(generator_tests.encode()) == GENERATOR_TEST_SHA256, "Generator test source mismatch")
    launcher_tests = (build_root / "test_lc518_launcher.py").read_text(encoding="utf-8")
    old_test = '''    def test_launcher_refuses_unpinned_protocol_before_creating_a_run_root(self):
        with tempfile.TemporaryDirectory() as td:
            candidate_root = Path(td) / "must-not-be-created"
            with self.assertRaises(RuntimeError):
                launcher.validate_static_configuration()
            self.assertFalse(candidate_root.exists())
'''
    new_test = '''    def test_launcher_refuses_without_owner_go_before_creating_a_run_root(self):
        with self.assertRaisesRegex(RuntimeError, "separate owner GO for bank generation is absent"):
            launcher.validate_static_configuration()

    def test_runner_image_identity_is_pinned(self):
        with mock.patch.dict("os.environ", {
            "ImageOS": launcher.EXPECTED_RUNNER_IMAGE_OS,
            "ImageVersion": "deliberately-wrong-image-version",
        }):
            with self.assertRaisesRegex(RuntimeError, "runner image identity"):
                launcher.validate_static_configuration()
'''
    launcher_tests = replace_once(launcher_tests, old_test, new_test, "launcher refusal test")
    launcher_test_sha = hbytes(launcher_tests.encode())

    protocol = {
        "schema": "lc518-c9-github-execution-protocol-v1",
        "status": "CONFIGURED_LOCKED_NOT_AUTHORIZED",
        "protocol_sha256": None,
        "protocol_hash_policy": "External only. The SHA-256 of this exact JSON is pinned in lc518_launcher.py and required in the separate owner GO.",
        "design_of_record": {
            "commit": "511bc2099ecff74b4f850b169ceef7f853c334a0",
            "file": "lc518-150/review-v1.2/analysis-revision-2026-11-02/C9_GENERATION_SPEC_REVIEW.md",
            "owner_ratified_date": "2026-11-02",
            "sha256": "f291ae879ef6e046c6715bb0e6a84cd5a3f5e69f07ace09e213db9b84d8b87fe",
        },
        "bank_generation_authorized": False,
        "runner": {
            "provider": "GitHub-hosted Actions runner",
            "runs_on": "ubuntu-24.04",
            "image_os": observed["image_os"],
            "image_version": observed["image_version"],
            "python_implementation": "CPython",
            "python_executable": observed["python_executable"],
            "sys_version": observed["sys_version"],
            "platform": observed["platform"],
            "interpreter_binary_sha256": observed["interpreter_sha256"],
            "workspace": str(workspace),
            "run_root": str(run_root),
            "output_dir": str(output_dir),
            "ephemeral": True,
            "drift_policy": "Any mismatch in the pinned Python or runner image identity is a hard refusal.",
        },
        "generator": {
            "review_candidate_sha256": BASE_GENERATOR_SHA256,
            "configured_locked_sha256": generator_state1_sha,
            "predeclared_activation_candidate_sha256": generator_state2_sha,
            "output_dir_constant_pinned": True,
            "bank_generation_authorized": False,
            "reads_environment": False,
            "accepts_command_line_arguments": False,
            "version_triple": [3, 13, 5],
            "activation_rule": "State 2 differs from state 1 only by BANK_GENERATION_AUTHORIZED=False to True. It must not be executed before separate owner GO.",
        },
        "launcher": {
            "configured_locked": True,
            "bank_generation_authorized": False,
            "predeclared_activation_candidate_rule": "Launcher state 2 differs from state 1 only by BANK_GENERATION_AUTHORIZED=False to True.",
            "protocol_source": "execution_protocol_github_v1.json",
            "protocol_sha256_embedded": None,
            "captures_stdout": True,
            "captures_stderr": True,
            "pythonhashseed_for_child": 0,
            "runner_image_os_pin": observed["image_os"],
            "runner_image_version_pin": observed["image_version"],
        },
        "paths": {
            "run_root_absolute": str(run_root),
            "output_dir_absolute": str(output_dir),
            "output_dir_rule": "RUN_ROOT/bank",
            "logs_dir_rule": "RUN_ROOT/logs",
            "generator_publication_rule": "RUN_ROOT/lc518_generator.py",
            "staging_suffix": ".staging",
            "run_root_must_be_absent": True,
            "run_root_parent_must_exist": True,
        },
        "seeds": {"diagnostic": 11052026, "heldout": 20261101},
        "test_suites": {
            "passing_test_count": 52,
            "test_interpreter": "CPython 3.13.5",
            "test_lc518_generator.py": {"sha256": GENERATOR_TEST_SHA256},
            "test_lc518_launcher.py": {"sha256": launcher_test_sha},
        },
        "other_authorities": {
            "candidate_execution": False,
            "merge_to_master": False,
            "power_study": False,
            "predictive_fitting": False,
            "private_annex_access": False,
            "repository_push_by_generator": False,
            "solver_construction": False,
        },
        "required_before_bank_generation": [
            "A separate owner GO naming this JSON protocol SHA-256.",
            "The exact generator activation diff and launcher activation diff must be named in that GO.",
            "The locked launcher refusal check and full 52-test suite must pass on the pinned GitHub runner.",
        ],
        "configuration_pending_fields": [],
    }
    protocol_bytes = (json.dumps(protocol, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()
    protocol_sha = hbytes(protocol_bytes)

    launcher_source = (build_root / "lc518_launcher.py").read_text(encoding="utf-8")
    pins = [
        ("RUN_ROOT: str | None = None", f'RUN_ROOT: str | None = "{run_root}"'),
        ("OUTPUT_DIR: str | None = None", f'OUTPUT_DIR: str | None = "{output_dir}"'),
        ("EXPECTED_PYTHON_EXECUTABLE: str | None = None", f'EXPECTED_PYTHON_EXECUTABLE: str | None = "{observed["python_executable"]}"'),
        ("EXPECTED_SYS_VERSION: str | None = None", f'EXPECTED_SYS_VERSION: str | None = "{observed["sys_version"]}"'),
        ("EXPECTED_PLATFORM: str | None = None", f'EXPECTED_PLATFORM: str | None = "{observed["platform"]}"'),
        ("EXPECTED_INTERPRETER_SHA256: str | None = None", f'EXPECTED_INTERPRETER_SHA256: str | None = "{observed["interpreter_sha256"]}"'),
        ("PROTOCOL_SHA256: str | None = None", f'PROTOCOL_SHA256: str | None = "{protocol_sha}"'),
        ('EXPECTED_GENERATOR_SHA256: str | None = "6e4281b4bfd79783b53d93e132a538dc3d120177405e44012081c6db083c0e2f"',
         f'EXPECTED_GENERATOR_SHA256: str | None = "{generator_state2_sha}"'),
    ]
    for old, new in pins:
        launcher_source = replace_once(launcher_source, old, new, "launcher pin " + old.split(":")[0])
    old_suite_map = '''EXPECTED_TEST_SUITE_SHA256S: dict[str, str] | None = {
    "generator": "d6a322bc9c28a9c5537f89a1bb6395bf52a44f79293c07b4f526ad985dfcdf64",
    "launcher": "febd27e1fd98ed9d27d6e802e50704fa278b504ba2d6555bbab81d0c091953b0",
}'''
    new_suite_map = f'''EXPECTED_TEST_SUITE_SHA256S: dict[str, str] | None = {{
    "generator": "{GENERATOR_TEST_SHA256}",
    "launcher": "{launcher_test_sha}",
}}'''
    launcher_source = replace_once(launcher_source, old_suite_map, new_suite_map, "launcher test hash map")
    launcher_source = replace_once(launcher_source, "TEST_SUITE_PASS_COUNT: int | None = 51",
                                   "TEST_SUITE_PASS_COUNT: int | None = 52", "launcher test count")
    launcher_source = replace_once(launcher_source,
                                   'GENERATOR_SOURCE = SOURCE_DIR / "lc518_generator.py"',
                                   'GENERATOR_SOURCE = SOURCE_DIR / "lc518_generator_state2.py"',
                                   "generator candidate path")
    launcher_source = replace_once(launcher_source,
                                   'PROTOCOL_SOURCE = SOURCE_DIR / "execution_protocol_v1.json"',
                                   'PROTOCOL_SOURCE = SOURCE_DIR / "execution_protocol_github_v1.json"',
                                   "machine protocol path")
    launcher_source = replace_once(
        launcher_source, "EXPECTED_PYTHON_VERSION = (3, 13, 5)\n",
        "EXPECTED_PYTHON_VERSION = (3, 13, 5)\n"
        f'EXPECTED_RUNNER_IMAGE_OS = "{observed["image_os"]}"\n'
        f'EXPECTED_RUNNER_IMAGE_VERSION = "{observed["image_version"]}"\n',
        "runner image pins")
    image_check = (
        '    if os.environ.get("ImageOS") != EXPECTED_RUNNER_IMAGE_OS or os.environ.get("ImageVersion") != EXPECTED_RUNNER_IMAGE_VERSION:\n'
        '        raise RuntimeError("GitHub runner image identity does not match execution protocol pin")\n'
    )
    launcher_source = replace_once(
        launcher_source, "    if sys.version_info[:3] != EXPECTED_PYTHON_VERSION:\n",
        image_check + "    if sys.version_info[:3] != EXPECTED_PYTHON_VERSION:\n",
        "runner image enforcement")

    launcher_state1 = launcher_source
    launcher_state2 = replace_once(
        launcher_state1, "BANK_GENERATION_AUTHORIZED = False",
        "BANK_GENERATION_AUTHORIZED = True", "launcher activation")

    PACKAGE.mkdir(parents=True, exist_ok=True)
    files = {
        "lc518_generator.py": (build_root / "lc518_generator.py").read_bytes(),
        "lc518_generator_state1.py": generator_state1.encode(),
        "lc518_generator_state2.py": generator_state2.encode(),
        "lc518_launcher.py": launcher_state1.encode(),
        "lc518_launcher_state2.py": launcher_state2.encode(),
        "execution_protocol_github_v1.json": protocol_bytes,
        "test_lc518_generator.py": generator_tests.encode(),
        "test_lc518_launcher.py": launcher_tests.encode(),
        "activation_generator.diff": "".join(difflib.unified_diff(
            generator_state1.splitlines(keepends=True), generator_state2.splitlines(keepends=True),
            fromfile="lc518_generator_state1.py", tofile="lc518_generator_state2.py", n=3)).encode(),
        "activation_launcher.diff": "".join(difflib.unified_diff(
            launcher_state1.splitlines(keepends=True), launcher_state2.splitlines(keepends=True),
            fromfile="lc518_launcher.py", tofile="lc518_launcher_state2.py", n=3)).encode(),
    }
    readme = (
        "# LC518 C9 GitHub execution configuration\n\n"
        "**Status: CONFIGURED_LOCKED_NOT_AUTHORIZED.**\n\n"
        f"- Runner: ubuntu-24.04, image {observed['image_os']} / {observed['image_version']}\n"
        f"- Python executable: {observed['python_executable']}\n"
        f"- RUN_ROOT: {run_root}\n- OUTPUT_DIR: {output_dir}\n"
        f"- Machine protocol SHA-256: {protocol_sha}\n\n"
        "The original c9-execution-recovery package remains unchanged. The configured state-1 launcher and generator remain locked. "
        "State-2 files are exact one-line activation candidates and were only compiled/hashed, never executed. "
        "The preflight executes the state-1 launcher only to confirm that it refuses before creating RUN_ROOT. "
        "No bank, solver output, fitting result, or power result exists. GitHub runners are ephemeral; a future authorized run must upload the entire run root as an artifact before teardown.\n"
    )
    files["README.md"] = readme.encode()
    protocol_md = (
        "# LC518 C9 GitHub-hosted execution protocol\n\n"
        "**Status:** CONFIGURED_LOCKED_NOT_AUTHORIZED\n"
        f"**Machine JSON SHA-256:** {protocol_sha}\n"
        "**Bank-generation authorization:** FALSE\n\n"
        "## Exact runner identity\n\n"
        f"- runs-on: ubuntu-24.04\n- ImageOS: {observed['image_os']}\n- ImageVersion: {observed['image_version']}\n"
        f"- Python executable: {observed['python_executable']}\n- sys.version: {observed['sys_version']}\n"
        f"- platform.platform(): {observed['platform']}\n- interpreter SHA-256: {observed['interpreter_sha256']}\n"
        f"- GITHUB_WORKSPACE: {workspace}\n\n"
        "The configured launcher checks the complete interpreter fingerprint and both runner-image variables. Any drift is a hard refusal.\n\n"
        "## Paths\n\n"
        f"- RUN_ROOT: {run_root}\n- OUTPUT_DIR: {output_dir}\n"
        "The run root must be absent; its parent must exist. GitHub hosted runners are ephemeral. An authorized job must upload the full run root, stdout, stderr and manifest as a workflow artifact before teardown.\n\n"
        "## Locked activation chain\n\n"
        f"- Review generator: {BASE_GENERATOR_SHA256}\n- Generator state 1: {generator_state1_sha}\n"
        f"- Generator state 2 candidate: {generator_state2_sha}\n"
        f"- Launcher state 1: {hbytes(launcher_state1.encode())}\n"
        f"- Launcher state 2 candidate: {hbytes(launcher_state2.encode())}\n"
        f"- Generator diff SHA-256: {hbytes(files['activation_generator.diff'])}\n"
        f"- Launcher diff SHA-256: {hbytes(files['activation_launcher.diff'])}\n"
        f"- Generator tests: {GENERATOR_TEST_SHA256}\n- Launcher tests: {launcher_test_sha}\n"
        "- Synthetic tests: 52 expected\n\n"
        "The workflow verifies both activation diffs and hashes, runs synthetic tests, checks the launcher refusal, and does not invoke the generator or either state-2 file. A separate owner GO naming this JSON digest and both exact diffs is required before bank generation. No solver execution, private annex, predictive fitting, power study, or merge to master is authorized.\n"
    )
    files["execution_protocol_github_v1.md"] = protocol_md.encode()
    digest_rows = {name: hbytes(data) for name, data in files.items()}
    files["SHA256SUMS"] = "".join(f"{digest}  {name}\n" for name, digest in sorted(digest_rows.items())).encode()

    for name, data in files.items():
        (PACKAGE / name).write_bytes(data)

    need((PACKAGE / "lc518_generator_state2.py").read_bytes() ==
         (PACKAGE / "lc518_generator_state1.py").read_bytes().replace(
             b"BANK_GENERATION_AUTHORIZED = False", b"BANK_GENERATION_AUTHORIZED = True", 1),
         "Generator activation is not exactly one line")
    need((PACKAGE / "lc518_launcher_state2.py").read_bytes() ==
         (PACKAGE / "lc518_launcher.py").read_bytes().replace(
             b"BANK_GENERATION_AUTHORIZED = False", b"BANK_GENERATION_AUTHORIZED = True", 1),
         "Launcher activation is not exactly one line")
    need(hfile(PACKAGE / "execution_protocol_github_v1.json") == protocol_sha, "Protocol hash changed during publication")
    need(not run_root.exists(), "Run root appeared during package preparation")
    print(json.dumps({
        "status": "GITHUB_LOCKED_PACKAGE_BUILT",
        "package": str(PACKAGE),
        "protocol_sha256": protocol_sha,
        "generator_state1_sha256": generator_state1_sha,
        "generator_state2_sha256": generator_state2_sha,
        "launcher_state1_sha256": hbytes(launcher_state1.encode()),
        "launcher_state2_sha256": hbytes(launcher_state2.encode()),
        "launcher_test_sha256": launcher_test_sha,
        "test_count": 52,
        "run_root_not_created": True,
        "generator_or_state2_executed": False,
    }, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
