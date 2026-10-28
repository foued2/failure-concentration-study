from __future__ import annotations

import json
import subprocess
import threading
import time
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
IMAGE_CONTEXT = ROOT / "container-image"
IMAGE_TAG = "h3-v4-candidate-sandbox:20261028-r1"
RESULT_PREFIX = "H3V4_RESULT "
MEMORY_BYTES = 128 * 1024 * 1024
CPU_LIMIT = 1.0
PID_LIMIT = 16
DEFAULT_TIMEOUT_SECONDS = 5.0

_image_lock = threading.Lock()
_image_ready = False
_image_info_cache: dict[str, Any] | None = None


class ContainerInfrastructureError(RuntimeError):
    """The isolation runtime failed; do not turn an infrastructure problem into a candidate label."""


def ensure_image() -> dict[str, Any]:
    """Build from the minimal context, which deliberately excludes the repo and oracle."""
    global _image_ready, _image_info_cache
    with _image_lock:
        if _image_ready and _image_info_cache is not None:
            return dict(_image_info_cache)
        if not IMAGE_CONTEXT.is_dir() or not (IMAGE_CONTEXT / "Dockerfile").is_file():
            raise ContainerInfrastructureError(f"container build context missing: {IMAGE_CONTEXT}")
        expected = {"Dockerfile", "sandbox_worker.py"}
        actual = {p.name for p in IMAGE_CONTEXT.iterdir() if p.is_file()}
        unexpected = sorted(actual - expected)
        missing = sorted(expected - actual)
        if unexpected or missing:
            raise ContainerInfrastructureError(
                f"minimal image context mismatch; missing={missing}, unexpected={unexpected}"
            )
        try:
            proc = subprocess.run(
                ["docker", "build", "--pull", "--tag", IMAGE_TAG, str(IMAGE_CONTEXT)],
                cwd=str(IMAGE_CONTEXT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=300,
                check=False,
            )
        except Exception as exc:
            raise ContainerInfrastructureError(
                f"Docker image build could not run: {type(exc).__name__}: {exc}"
            ) from exc
        if proc.returncode != 0:
            raise ContainerInfrastructureError(
                "Docker image build failed: " + (proc.stderr or proc.stdout)[-3000:]
            )
        _image_info_cache = _inspect_image()
        _image_ready = True
        return dict(_image_info_cache)


def _inspect_image() -> dict[str, Any]:
    try:
        proc = subprocess.run(
            ["docker", "image", "inspect", IMAGE_TAG],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
            check=False,
        )
    except Exception as exc:
        raise ContainerInfrastructureError(f"Docker image inspect failed: {exc}") from exc
    if proc.returncode != 0:
        raise ContainerInfrastructureError("Docker image is unavailable: " + proc.stderr[-1200:])
    try:
        item = json.loads(proc.stdout)[0]
    except Exception as exc:
        raise ContainerInfrastructureError("Docker image inspect returned malformed JSON") from exc
    return {
        "tag": IMAGE_TAG,
        "image_id": item.get("Id"),
        "repo_digests": item.get("RepoDigests") or [],
        "created": item.get("Created"),
        "os": item.get("Os"),
        "architecture": item.get("Architecture"),
    }


def _run(
    source_path: str | Path,
    request: dict,
    timeout: float,
    *,
    inspect_container: bool = False,
) -> dict[str, Any]:
    image = ensure_image()
    source = Path(source_path).resolve(strict=True)
    if not source.is_file():
        raise ContainerInfrastructureError(f"candidate source is not a file: {source}")
    # Docker's --mount syntax treats commas as delimiters. Reject instead of
    # constructing a mount expression that could be parsed ambiguously.
    if "," in str(source):
        raise ContainerInfrastructureError("candidate source path contains a comma and cannot be mounted safely")

    name = "h3v4-" + uuid.uuid4().hex[:24]
    command = [
        "docker", "run",
        "--name", name,
        "--interactive",
        "--network=none",
        "--read-only",
        "--user=65534:65534",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges:true",
        f"--pids-limit={PID_LIMIT}",
        f"--memory={MEMORY_BYTES}",
        f"--memory-swap={MEMORY_BYTES}",
        f"--cpus={CPU_LIMIT}",
        "--ulimit=nofile=64:64",
        "--ulimit=core=0:0",
        "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=16m,uid=65534,gid=65534,mode=1777",
        "--env=PYTHONDONTWRITEBYTECODE=1",
        "--mount", f"type=bind,source={source},target=/candidate/solve.py,readonly",
        IMAGE_TAG,
    ]
    started = time.monotonic()
    try:
        proc = subprocess.Popen(
            command,
            cwd=str(IMAGE_CONTEXT),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception as exc:
        raise ContainerInfrastructureError(f"docker run could not start: {type(exc).__name__}: {exc}") from exc

    timed_out = False
    stdout_bytes = b""
    stderr_bytes = b""
    payload = json.dumps(
        {"candidate": "/candidate/solve.py", **request},
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    try:
        stdout_bytes, stderr_bytes = proc.communicate(input=payload, timeout=max(0.1, timeout))
    except subprocess.TimeoutExpired:
        timed_out = True
        # Kill through the Docker daemon first. Killing only the client would
        # leave the untrusted container running after the caller timed out.
        subprocess.run(
            ["docker", "kill", name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            check=False,
        )
        try:
            stdout_bytes, stderr_bytes = proc.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout_bytes, stderr_bytes = proc.communicate()

    elapsed = round(time.monotonic() - started, 4)
    inspect: dict[str, Any] | None = None
    inspect_proc = None
    if inspect_container:
        inspect_proc = subprocess.run(
            ["docker", "inspect", name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            check=False,
        )
    if inspect_proc is not None and inspect_proc.returncode == 0:
        try:
            item = json.loads(inspect_proc.stdout)[0]
            host = item.get("HostConfig") or {}
            state = item.get("State") or {}
            inspect = {
                "name": item.get("Name", "").lstrip("/"),
                "user": (item.get("Config") or {}).get("User"),
                "running": state.get("Running"),
                "exit_code": state.get("ExitCode"),
                "oom_killed": state.get("OOMKilled"),
                "error": state.get("Error"),
                "network_mode": host.get("NetworkMode"),
                "readonly_rootfs": host.get("ReadonlyRootfs"),
                "memory_bytes": host.get("Memory"),
                "memory_swap_bytes": host.get("MemorySwap"),
                "nano_cpus": host.get("NanoCpus"),
                "pids_limit": host.get("PidsLimit"),
                "cap_drop": host.get("CapDrop"),
                "security_opt": host.get("SecurityOpt"),
                "mounts": [
                    {
                        "type": m.get("Type"),
                        "source": m.get("Source"),
                        "destination": m.get("Destination"),
                        "read_only": m.get("RW") is False,
                    }
                    for m in (item.get("Mounts") or [])
                ],
            }
        except Exception:
            inspect = None

    # Remove this exact, randomly named container even when the run timed out.
    cleanup = subprocess.run(
        ["docker", "rm", "--force", name],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=15,
        check=False,
    )
    # A successful Docker rm response is the daemon's acknowledgment that the
    # named container was removed; avoid launching a second inspect process
    # after every one of the 30 independently isolated candidate probes.
    container_removed = cleanup.returncode == 0

    stdout = stdout_bytes.decode("utf-8", "replace")
    stderr = stderr_bytes.decode("utf-8", "replace")
    messages = [
        line[len(RESULT_PREFIX):]
        for line in stdout.splitlines()
        if line.startswith(RESULT_PREFIX)
    ]
    result = None
    if messages:
        try:
            result = json.loads(messages[-1])
        except json.JSONDecodeError:
            result = None

    if timed_out:
        return {
            "status": "timed_out",
            "timed_out": True,
            "stdout_tail": stdout[-1000:],
            "container_name": name,
            "container_removed": container_removed,
            "elapsed_seconds": elapsed,
            "exit_code": proc.returncode,
            "stderr_tail": stderr[-1000:],
            "container": inspect,
            "image": image,
        }
    if result is None:
        return {
            "status": "no_result",
            "timed_out": False,
            "container_name": name,
            "container_removed": container_removed,
            "elapsed_seconds": elapsed,
            "exit_code": proc.returncode,
            "stdout_tail": stdout[-1000:],
            "stderr_tail": stderr[-1000:],
            "container": inspect,
            "image": image,
        }
    result.update({
        "timed_out": False,
        "container_name": name,
        "container_removed": container_removed,
        "elapsed_seconds": elapsed,
        "exit_code": proc.returncode,
        "stderr_tail": stderr[-1000:],
        "container": inspect,
        "image": image,
    })
    return result


def preflight(candidate_path: str | Path, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    return _run(candidate_path, {"mode": "preflight"}, timeout, inspect_container=False)


def run_probe(
    candidate_path: str | Path,
    probe: dict,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    request_probe = {key: probe[key] for key in ("n", "edges", "s", "t")}
    return _run(candidate_path, {"mode": "probe", "probe": request_probe}, timeout, inspect_container=False)


def run_fixture(
    fixture_path: str | Path,
    probe: dict | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Run a fixed, audited isolation fixture; never use this path for generated candidates."""
    request_probe = probe or {"n": 0, "edges": [], "s": 0, "t": 0}
    return _run(fixture_path, {"mode": "fixture", "probe": request_probe}, timeout, inspect_container=True)


def effective_limits(result: dict[str, Any]) -> dict[str, Any]:
    """Extract observed Docker host configuration for an execution result."""
    container = result.get("container") or {}
    mounts = container.get("mounts") or []
    bind_mounts = [mount for mount in mounts if mount.get("type") == "bind"]
    other_mounts = [mount for mount in mounts if mount.get("type") != "bind"]
    return {
        "network_none": container.get("network_mode") == "none",
        "readonly_rootfs": container.get("readonly_rootfs") is True,
        "memory_limit_128m": container.get("memory_bytes") == MEMORY_BYTES,
        "memory_swap_equal_to_memory": container.get("memory_swap_bytes") == MEMORY_BYTES,
        "cpu_limit_1": container.get("nano_cpus") == 1_000_000_000,
        "pids_limit_16": container.get("pids_limit") == PID_LIMIT,
        "all_capabilities_dropped": "ALL" in (container.get("cap_drop") or []),
        "no_new_privileges": any("no-new-privileges" in str(x) for x in (container.get("security_opt") or [])),
        "unprivileged_user": container.get("user") == "65534:65534",
        "exactly_one_readonly_candidate_bind": (
            len(bind_mounts) == 1
            and bind_mounts[0].get("destination") == "/candidate/solve.py"
            and bind_mounts[0].get("read_only") is True
            and all(mount.get("type") == "tmpfs" and mount.get("destination") == "/tmp"
                    for mount in other_mounts)
        ),
    }
