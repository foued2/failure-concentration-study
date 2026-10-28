from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

import container_eval

ROOT = Path(__file__).resolve().parent


def _write_fixture(root: Path, name: str, source: str) -> Path:
    path = root / name
    path.write_text(source, encoding="utf-8", newline="\n")
    return path


def _run_memory_limit_probe() -> dict[str, Any]:
    """Use a bounded 64 MiB container to test an allocation larger than its cap."""
    image = container_eval.ensure_image()
    name = "h3v4-memory-" + uuid.uuid4().hex[:20]
    command = [
        "docker", "run", "--name", name,
        "--network=none", "--read-only", "--user=65534:65534",
        "--cap-drop=ALL", "--security-opt=no-new-privileges:true",
        "--pids-limit=16", "--memory=67108864", "--memory-swap=67108864",
        "--cpus=1.0", "--ulimit=nofile=64:64", "--ulimit=core=0:0",
        "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=16m,uid=65534,gid=65534,mode=1777",
        "--entrypoint", "python", container_eval.IMAGE_TAG,
        "-c", "x = bytearray(256 * 1024 * 1024); print('ALLOCATION_SURVIVED')",
    ]
    started = time.monotonic()
    try:
        run = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=30, check=False,
        )
    except Exception as exc:
        raise container_eval.ContainerInfrastructureError(
            f"bounded memory probe could not run: {type(exc).__name__}: {exc}"
        ) from exc
    inspect_proc = subprocess.run(
        ["docker", "inspect", name], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=10, check=False,
    )
    container = None
    if inspect_proc.returncode == 0:
        try:
            item = json.loads(inspect_proc.stdout)[0]
            state = item.get("State") or {}
            host = item.get("HostConfig") or {}
            container = {
                "running": state.get("Running"),
                "exit_code": state.get("ExitCode"),
                "oom_killed": state.get("OOMKilled"),
                "memory_bytes": host.get("Memory"),
                "memory_swap_bytes": host.get("MemorySwap"),
            }
        except Exception:
            container = None
    subprocess.run(
        ["docker", "rm", "--force", name], capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=10, check=False,
    )
    return {
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "exit_code": run.returncode,
        "stdout_tail": run.stdout[-500:],
        "stderr_tail": run.stderr[-1000:],
        "container": container,
        "passed": bool(container and container.get("oom_killed") is True
                       and container.get("memory_bytes") == 67108864
                       and container.get("memory_swap_bytes") == 67108864),
    }


def run_battery(report_path: Path) -> dict[str, Any]:
    image = container_eval.ensure_image()
    image_files = sorted(p.name for p in container_eval.IMAGE_CONTEXT.iterdir() if p.is_file())

    with tempfile.TemporaryDirectory(prefix="h3-v4-isolation-") as td:
        temp = Path(td).resolve()
        sentinel_root = temp / "host-private"
        sentinel_root.mkdir()
        sentinel = sentinel_root / "expected-values-sentinel.txt"
        sentinel.write_text("HOST_ONLY_SECRET_SENTINEL", encoding="utf-8")
        host_oracle_path = (Path(os.environ.get("GITHUB_WORKSPACE", str(ROOT))).resolve()
                            / "h3-footprint-v4" / "expected_values.json")

        host_path_literal = json.dumps(str(sentinel))
        oracle_path_literal = json.dumps(str(host_oracle_path))

        host_source = String = (
            "from pathlib import Path\n"
            "def solve(n, edges, s, t):\n"
            f"    host_path = Path({host_path_literal})\n"
            f"    oracle_path = Path({oracle_path_literal})\n"
            "    try:\n"
            "        host_path.read_text(encoding='utf-8')\n"
            "        host_file_denied = False\n"
            "    except OSError as exc:\n"
            "        host_file_denied = True\n"
            "        host_error = type(exc).__name__\n"
            "    else:\n"
            "        host_error = None\n"
            "    try:\n"
            "        oracle_path.read_text(encoding='utf-8')\n"
            "        host_oracle_denied = False\n"
            "    except OSError:\n"
            "        host_oracle_denied = True\n"
            "    source_path = Path(__file__)\n"
            "    source_readable = source_path.read_text(encoding='utf-8').startswith('from pathlib import Path')\n"
            "    try:\n"
            "        source_path.write_text('SHOULD_NOT_BE_WRITABLE', encoding='utf-8')\n"
            "        source_write_denied = False\n"
            "    except OSError:\n"
            "        source_write_denied = True\n"
            "    scratch = Path('/tmp/h3-v4-scratch-positive-control.txt')\n"
            "    scratch.write_text('scratch-ok', encoding='utf-8')\n"
            "    sensitive = ('GITHUB_', 'ACTIONS_', 'TOKEN', 'API_KEY', 'SECRET')\n"
            "    sensitive_env = sorted(k for k in __import__('os').environ if any(x in k.upper() for x in sensitive))\n"
            "    return {'host_file_denied': host_file_denied, 'host_error': host_error, "
            "'host_oracle_denied': host_oracle_denied, 'source_readable': source_readable, "
            "'source_write_denied': source_write_denied, 'scratch_write_allowed': scratch.read_text() == 'scratch-ok', "
            "'sensitive_env_keys': sensitive_env, 'uid': __import__('os').getuid()}\n"
        )
        host_fixture = _write_fixture(temp, "host-boundary-probe.py", host_source)
        source_hash_before = hashlib.sha256(host_fixture.read_bytes()).hexdigest()
        host_result = container_eval.run_fixture(host_fixture, timeout=5.0)
        host_value = host_result.get("value") if host_result.get("status") == "fixture_ok" else None
        source_hash_after = hashlib.sha256(host_fixture.read_bytes()).hexdigest()

        network_source = String = String = (
            "import socket\n"
            "def solve(n, edges, s, t):\n"
            "    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
            "    server.settimeout(1.0)\n"
            "    server.bind(('127.0.0.1', 0))\n"
            "    server.listen(1)\n"
            "    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
            "    client.settimeout(1.0)\n"
            "    client.connect(('127.0.0.1', server.getsockname()[1]))\n"
            "    connection, _ = server.accept()\n"
            "    connection.close(); client.close(); server.close()\n"
            "    external_denied = False; external_error = None\n"
            "    try:\n"
            "        socket.create_connection(('1.1.1.1', 443), timeout=0.75).close()\n"
            "    except OSError as exc:\n"
            "        external_denied = True; external_error = type(exc).__name__\n"
            "    return {'loopback_connected': True, 'external_denied': external_denied, "
            "'external_error': external_error, 'target': '1.1.1.1:443'}\n"
        )
        network_fixture = _write_fixture(temp, "network-boundary-probe.py", network_source)
        network_result = container_eval.run_fixture(network_fixture, timeout=5.0)
        network_value = network_result.get("value") if network_result.get("status") == "fixture_ok" else None

        pids_source = String = (
            "import subprocess\n"
            "def solve(n, edges, s, t):\n"
            "    children = []; cap_hit = False; error_type = None\n"
            "    try:\n"
            "        for _ in range(32):\n"
            "            children.append(subprocess.Popen(['/bin/sleep', '10']))\n"
            "    except OSError as exc:\n"
            "        cap_hit = True; error_type = type(exc).__name__\n"
            "    finally:\n"
            "        for child in children:\n"
            "            try: child.terminate()\n"
            "            except OSError: pass\n"
            "        for child in children:\n"
            "            try: child.wait(timeout=1)\n"
            "            except Exception: pass\n"
            "    return {'pids_limit_hit': cap_hit, 'children_started': len(children), 'error_type': error_type}\n"
        )
        pids_fixture = _write_fixture(temp, "pids-boundary-probe.py", pids_source)
        pids_result = container_eval.run_fixture(pids_fixture, timeout=8.0)
        pids_value = pids_result.get("value") if pids_result.get("status") == "fixture_ok" else None

        exit_fixture = _write_fixture(
            temp, "normal-exit-probe.py",
            "def solve(n, edges, s, t):\n    return {'normal_exit': True}\n",
        )
        exit_result = container_eval.run_fixture(exit_fixture, timeout=5.0)
        exit_value = exit_result.get("value") if exit_result.get("status") == "fixture_ok" else None

        tree_source = String = (
            "import os, subprocess, time\n"
            "def solve(n, edges, s, t):\n"
            "    child = subprocess.Popen(['/bin/sleep', '60'])\n"
            "    os.write(1, ('H3V4_CHILD_PID=' + str(child.pid) + '\\n').encode())\n"
            "    time.sleep(60)\n"
            "    return {'unexpected': 'returned'}\n"
        )
        tree_fixture = _write_fixture(temp, "tree-kill-probe.py", tree_source)
        tree_result = container_eval.run_fixture(tree_fixture, timeout=2.0)
        child_match = re.search(r"H3V4_CHILD_PID=(\d+)", tree_result.get("stdout_tail", ""))
        child_pid_seen = int(child_match.group(1)) if child_match else None

    memory_result = _run_memory_limit_probe()
    limits = container_eval.effective_limits(host_result)

    probes = {
        "host_file_boundary": {
            "status": host_result.get("status"),
            "value": host_value,
            "positive_control_source_readable": bool(host_value and host_value.get("source_readable")),
            "positive_control_scratch_write": bool(host_value and host_value.get("scratch_write_allowed")),
            "host_sentinel_denied": bool(host_value and host_value.get("host_file_denied")),
            "host_oracle_path_denied": bool(host_value and host_value.get("host_oracle_denied")),
            "candidate_source_write_denied": bool(host_value and host_value.get("source_write_denied")),
            "sensitive_environment_keys_absent": bool(host_value and host_value.get("sensitive_env_keys") == []),
            "uid_65534": bool(host_value and host_value.get("uid") == 65534),
            "source_hash_unchanged": source_hash_before == source_hash_after,
        },
        "network_boundary": {
            "status": network_result.get("status"),
            "value": network_value,
            "loopback_control_passed": bool(network_value and network_value.get("loopback_connected")),
            "external_network_denied": bool(network_value and network_value.get("external_denied")),
            "external_error": network_value.get("external_error") if network_value else None,
        },
        "process_limit": {
            "status": pids_result.get("status"),
            "value": pids_value,
            "pids_limit_observed": bool(pids_value and pids_value.get("pids_limit_hit")
                                         and pids_value.get("children_started", 32) < 32),
            "children_started": pids_value.get("children_started") if pids_value else None,
        },
        "process_tree_cleanup": {
            "status": tree_result.get("status"),
            "timed_out": tree_result.get("timed_out") is True,
            "child_pid_reported_by_fixture": child_pid_seen is not None,
            "container_stopped": bool(tree_result.get("container") and tree_result["container"].get("running") is False),
            "container_removed": tree_result.get("container_removed") is True,
            "exit_code": (tree_result.get("container") or {}).get("exit_code"),
        },
        "normal_exit": {
            "status": exit_result.get("status"),
            "value": exit_value,
            "container_stopped": bool(exit_result.get("container") and exit_result["container"].get("running") is False),
            "container_removed": exit_result.get("container_removed") is True,
            "exit_code": (exit_result.get("container") or {}).get("exit_code"),
        },
        "memory_limit": memory_result,
        "container_limits": {
            **limits,
            "observed_user_65534": bool((host_result.get("container") or {}).get("user") == "65534:65534"),
            "single_mount_source": (((host_result.get("container") or {}).get("mounts") or [{}])[0].get("source")),
        },
        "image": image,
        "image_context_files": image_files,
    }

    checks = {
        "minimal_image_context_only": set(image_files) == {"Dockerfile", "sandbox_worker.py"},
        "host_file_denied_with_positive_control": (
            probes["host_file_boundary"]["status"] == "fixture_ok"
            and probes["host_file_boundary"]["host_sentinel_denied"]
            and probes["host_file_boundary"]["host_oracle_path_denied"]
            and probes["host_file_boundary"]["positive_control_source_readable"]
            and probes["host_file_boundary"]["positive_control_scratch_write"]
            and probes["host_file_boundary"]["candidate_source_write_denied"]
            and probes["host_file_boundary"]["sensitive_environment_keys_absent"]
            and probes["host_file_boundary"]["uid_65534"]
            and probes["host_file_boundary"]["source_hash_unchanged"]
        ),
        "network_denied_with_loopback_control": (
            probes["network_boundary"]["status"] == "fixture_ok"
            and probes["network_boundary"]["loopback_control_passed"]
            and probes["network_boundary"]["external_network_denied"]
        ),
        "process_limit_enforced": probes["process_limit"]["status"] == "fixture_ok"
                                  and probes["process_limit"]["pids_limit_observed"],
        "process_tree_killed_on_timeout": (
            probes["process_tree_cleanup"]["timed_out"]
            and probes["process_tree_cleanup"]["container_stopped"]
            and probes["process_tree_cleanup"]["container_removed"]
            and probes["process_tree_cleanup"]["child_pid_reported_by_fixture"]
        ),
        "normal_exit_cleanup": (
            probes["normal_exit"]["status"] == "fixture_ok"
            and probes["normal_exit"]["container_stopped"]
            and probes["normal_exit"]["container_removed"]
            and probes["normal_exit"]["exit_code"] == 0
        ),
        "memory_limit_enforced": probes["memory_limit"]["passed"],
        "docker_resource_controls_observed": all(limits.values())
            and probes["container_limits"]["observed_user_65534"],
    }

    payload = {
        "version": 4,
        "suite": "h3-v4-docker-isolation-battery",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "probes": probes,
        "notes": [
            "Fixed, hand-authored fixtures only. No generated candidate bodies or model calls were used.",
            "Only the current fixture source file was bind-mounted read-only. The Docker image context contains only Dockerfile and sandbox_worker.py.",
            "Each probe used a fresh container with network disabled, read-only rootfs, UID 65534, no added capabilities, no-new-privileges, bounded memory/CPU/PIDs, and tmpfs scratch.",
            "This is an execution-boundary test on a GitHub-hosted Linux runner, not proof of equivalence to Windows Sandbox. The V4 protocol remains unfrozen and candidate generation remains unauthorized.",
        ],
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run only fixed hand-authored V4 Docker isolation probes.")
    parser.add_argument("--report", required=True, help="path for JSON evidence output")
    args = parser.parse_args()
    try:
        result = run_battery(Path(args.report))
    except container_eval.ContainerInfrastructureError as exc:
        print(json.dumps({"status": "BLOCKED", "error": type(exc).__name__, "detail": str(exc)}))
        return 2
    print(json.dumps({"status": result["status"], "checks": result["checks"]}, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
