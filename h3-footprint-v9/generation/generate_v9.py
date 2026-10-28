"""V9 generator: enforced no-tools profile, per-batch workspace, hard body cap.

V8 asked the model not to use tools and then accepted every code block it
returned. Neither is a control. This module makes both enforceable:

  * every documented permission key is denied, globally and per agent, and no
    `--auto` is ever passed;
  * each batch gets its own workspace, so concurrent batches cannot see each
    other;
  * a response must contain at least the requested number of valid modules;
    fewer is an incomplete response and rejects the batch, while surplus bodies
    are capped at eight in response order and recorded as overflow;
  * any tool event, permission-policy event, malformed event stream, nonzero
    exit or missing response rejects the whole batch.

Generation is additionally gated in code on V9_AUTHORIZE_GENERATION=1, which
this implementation never sets.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import constants

HERE = Path(__file__).resolve().parent
AGENT_DIR = HERE / "agent"
AGENT_NAME = "h3-generator"

PERMISSION_KEYS = (
    "read", "edit", "glob", "grep", "bash", "task", "todowrite", "skill",
    "lsp", "question", "webfetch", "websearch", "external_directory", "doom_loop",
)

TASK = (
    "Write {n} independent Python implementations of a self-contained function "
    "`solve(n, edges, s, t)`. The function computes the shortest directed path distance "
    "from node s to node t in a graph with n nodes labeled 0..n-1 and non-negative integer "
    "edge weights. edges is a list of (u, v, w) tuples; parallel edges and self-loops may occur. "
    "Return the minimum total weight as an int, or -1 if t is unreachable. Use only the Python "
    "standard library. Do not read files, access the network, print, or include tests or example "
    "usage. Each implementation must be independently written from a plausible first approach; "
    "do not copy or repair one another. Return exactly {n} fenced Python code blocks, each "
    "containing one complete `def solve` and no other prose."
)
PROMPTS = {
    "direct": TASK,
    "menu": TASK + " Vary the approaches across the implementations; plausible approaches include heap Dijkstra, Bellman-Ford, list-scan Dijkstra, layered search, Floyd-Warshall, and DFS path enumeration.",
    "simple": TASK + " Prefer the simplest code that seems correct; do not optimize or self-review.",
}
FENCE = chr(96) * 3


def permission_profile() -> dict[str, str]:
    profile = {key: "deny" for key in PERMISSION_KEYS}
    profile["*"] = "deny"
    return profile


def sanitized_env(base: dict[str, str] | None = None) -> dict[str, str]:
    """Drop any inherited OPENCODE_* state, then pin our own deny-all config."""
    source = os.environ if base is None else base
    env = {k: v for k, v in source.items() if not k.startswith("OPENCODE_")}
    env["OPENCODE_CONFIG_CONTENT"] = json.dumps({"permission": permission_profile()})
    env["OPENCODE_PURE"] = "1"
    return env


def normalize(source: str) -> str:
    lines = [line.rstrip() for line in source.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    return "\n".join(lines).strip() + "\n"


def digest(source: str) -> str:
    return hashlib.sha256(normalize(source).encode()).hexdigest()


def extract_bodies(text: str) -> list[str]:
    """Every module containing exactly one top-level synchronous `solve`."""
    blocks = re.findall(FENCE + r"(?:python|py)?\s*\n(.*?)" + FENCE, text, flags=re.S | re.I)
    if not blocks:
        blocks = [text] if "def solve" in text else []
    out: list[str] = []
    for block in blocks:
        source = normalize(block)
        try:
            module = ast.parse(source)
        except SyntaxError:
            continue
        defs = [n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == "solve"]
        if len(defs) != 1:
            continue
        out.append(source)
    return out


def select_accepted(bodies: list[str], limit: int = constants.BODIES_PER_BATCH) -> tuple[list[str], list[str]]:
    """Deterministic overproduction rule: first `limit` in response order."""
    return bodies[:limit], bodies[limit:]


def _event_uses_tools(event: dict) -> bool:
    kind = event.get("type")
    if isinstance(kind, str) and "tool" in kind.lower():
        return True
    part = event.get("part")
    if isinstance(part, dict):
        ptype = part.get("type")
        if isinstance(ptype, str) and ("tool" in ptype.lower() or ptype in PERMISSION_KEYS):
            return True
        if "tool" in part or "permission" in part:
            return True
    return False


def _event_is_permission(event: dict) -> bool:
    """A permission request or decision is a policy event, not model text."""
    kind = event.get("type")
    if isinstance(kind, str) and "permission" in kind.lower():
        return True
    part = event.get("part")
    if isinstance(part, dict):
        ptype = part.get("type")
        if isinstance(ptype, str) and "permission" in ptype.lower():
            return True
        if "permission" in part:
            return True
    return False


def classify_events(stdout: str) -> dict:
    texts: list[str] = []
    tool_events = 0
    permission_events = 0
    parse_errors = 0
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            parse_errors += 1
            continue
        if not isinstance(event, dict):
            parse_errors += 1
            continue
        if _event_is_permission(event):
            permission_events += 1
            continue
        if _event_uses_tools(event):
            tool_events += 1
            continue
        if event.get("type") == "text":
            texts.append(event.get("part", {}).get("text", ""))
    return {"texts": texts, "tool_events": tool_events,
            "permission_events": permission_events, "parse_errors": parse_errors}


def batch_outcome(returncode: int, stdout: str,
                  expected: int = constants.BODIES_PER_BATCH) -> dict:
    """Decide what one batch contributes. Nothing partial is ever accepted.

    A response with fewer than `expected` valid modules is incomplete and is
    rejected: the prompt asks for that many. Surplus modules are a separate
    concern (the eight-body cap) and are counted, hashed and ignored.
    """
    events = classify_events(stdout)
    text = "\n".join(events["texts"])
    bodies = extract_bodies(text)
    accepted, overflow = select_accepted(bodies, expected)
    rejected = None
    if events["tool_events"]:
        rejected = "tool_use_detected"
    elif events["permission_events"]:
        rejected = "permission_event_detected"
    elif events["parse_errors"]:
        rejected = "malformed_event_stream"
    elif returncode != 0:
        rejected = "nonzero_exit"
    elif not events["texts"]:
        rejected = "no_complete_response"
    elif len(bodies) < expected:
        rejected = f"incomplete_response:{len(bodies)}/{expected}"
    return {
        "rejected": rejected,
        "accepted": [] if rejected else accepted,
        "accepted_hashes": [] if rejected else [digest(b) for b in accepted],
        "overflow_count": len(overflow),
        "overflow_hashes": [digest(b) for b in overflow],
        "found": len(bodies),
        "expected": expected,
        "tool_events": events["tool_events"],
        "permission_events": events["permission_events"],
        "parse_errors": events["parse_errors"],
    }


def batch_dir(work_root: Path, batch_id: int) -> Path:
    return work_root / f"batch-{batch_id:03d}"


def build_command(batch_id: int, workdir: Path, opencode: str) -> list[str]:
    model = constants.MODELS[batch_id % len(constants.MODELS)]
    variant = constants.PROMPT_VARIANTS[(batch_id // len(constants.MODELS)) % len(constants.PROMPT_VARIANTS)]
    return [
        opencode, "run",
        "--pure",
        "--format", "json",
        "--agent", AGENT_NAME,
        "--model", model,
        "--dir", str(workdir),
        PROMPTS[variant].format(n=constants.BODIES_PER_BATCH),
    ]


def install_agent_config(workdir: Path) -> Path:
    target = workdir / ".opencode" / "agent" / f"{AGENT_NAME}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text((AGENT_DIR / f"{AGENT_NAME}.md").read_text(encoding="utf-8"), encoding="utf-8")
    return target


def verify_config(opencode: str, probe_dir: Path) -> dict:
    """No model call: version, effective agent permissions, catalog visibility."""
    install_agent_config(probe_dir)
    env = sanitized_env()
    evidence: dict = {"opencode": opencode, "version": None, "agents": None,
                      "agent_loaded": False, "models_present": {}, "ok": False, "errors": []}
    for name, cmd in (
        ("version", [opencode, "--version"]),
        ("agents", [opencode, "debug", "agents"]),
        ("models", [opencode, "models"]),
    ):
        try:
            proc = subprocess.run(cmd, cwd=str(probe_dir), env=env, capture_output=True,
                                  text=True, timeout=120, encoding="utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            evidence["errors"].append(f"{name}: {type(exc).__name__}: {exc}")
            continue
        if proc.returncode != 0:
            evidence["errors"].append(f"{name}: exit {proc.returncode}: {(proc.stderr or '')[-300:]}")
        evidence[name] = proc.stdout.strip()[:4000] if name != "agents" else proc.stdout.strip()
        if name == "agents":
            evidence["agent_loaded"] = AGENT_NAME in proc.stdout
            denied, allowing = agent_is_fully_denied(proc.stdout)
            evidence["agent_fully_denied"] = denied
            evidence["agent_deny_leaks"] = allowing
        if name == "models":
            listed = proc.stdout
            evidence["models_present"] = {m: (m in listed) for m in constants.MODELS}
    evidence["ok"] = (
        not evidence["errors"]
        and evidence["agent_loaded"]
        and evidence.get("agent_fully_denied") is True
        and bool(evidence["models_present"])
        and all(evidence["models_present"].values())
    )
    return evidence


def _matches(pattern: str, value: str) -> bool:
    """Documented wildcard semantics: * and ? only."""
    import fnmatch
    return fnmatch.fnmatchcase(value, pattern)


def effective_effect(rules: list[dict], action: str, resource: str) -> str | None:
    """Resolve one action/resource pair. Last matching rule wins."""
    effect = None
    for rule in rules:
        if _matches(str(rule.get("action", "")), action) and _matches(str(rule.get("resource", "")), resource):
            effect = rule.get("effect")
    return effect


PROBE_ACTIONS = (
    "read", "edit", "glob", "grep", "bash", "shell", "task", "subagent",
    "todowrite", "skill", "lsp", "question", "webfetch", "websearch",
    "external_directory", "doom_loop", "browser", "*",
)
PROBE_RESOURCES = ("*", "C:/repo/secret.py", "https://example.invalid/x", "~/.ssh/id_rsa")


def agent_is_fully_denied(agents_stdout: str, agent_id: str = AGENT_NAME) -> tuple[bool, list[str]]:
    """Acceptable only if every probed action resolves to deny under last-match-wins."""
    try:
        agents = json.loads(agents_stdout)
    except json.JSONDecodeError:
        return False, ["unparseable_agent_list"]
    match = [a for a in agents if a.get("id") == agent_id]
    if len(match) != 1:
        return False, [f"agent_count={len(match)}"]
    rules = match[0].get("permissions") or []
    leaks = []
    for action in PROBE_ACTIONS:
        for resource in PROBE_RESOURCES:
            effect = effective_effect(rules, action, resource)
            if effect != "deny":
                leaks.append(f"{action}@{resource}={effect}")
    return (not leaks), leaks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-config", action="store_true",
                        help="non-generating: record CLI version, agent and model visibility")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--batches", type=int, default=0)
    parser.add_argument("--work-root", default=str(HERE / "work"))
    parser.add_argument("--opencode", default=os.environ.get("OPENCODE_EXE", "opencode"))
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    work_root = Path(args.work_root)
    probe_dir = work_root / "config-probe"
    probe_dir.mkdir(parents=True, exist_ok=True)

    if args.verify_config:
        evidence = verify_config(args.opencode, probe_dir)
        text = json.dumps(evidence, indent=2, sort_keys=True)
        if args.out:
            out = Path(args.out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text + "\n", encoding="utf-8")
        print(text)
        raise SystemExit(0 if evidence["ok"] else 1)

    if args.dry_run:
        plan = []
        for batch_id in range(min(args.batches or constants.MAX_BATCHES, constants.MAX_BATCHES)):
            d = batch_dir(work_root, batch_id)
            plan.append({"batch": batch_id, "dir": str(d), "command": build_command(batch_id, d, args.opencode)})
        print(json.dumps({"plan": plan[:3], "batches": len(plan),
                          "permission": permission_profile()}, indent=2))
        return

    if args.batches < 1:
        parser.error("nothing to do: pass --batches N, --dry-run or --verify-config")
    if os.environ.get("V9_AUTHORIZE_GENERATION") != "1":
        raise SystemExit(
            "Refusing to generate: V9_AUTHORIZE_GENERATION is not 1. "
            "No generation is authorized during V9 implementation."
        )

    raise SystemExit(
        "Generation is NOT IMPLEMENTED in V9. V9_AUTHORIZE_GENERATION=1 unlocks "
        "nothing: the batch runner has not been written, and it must not be written "
        "until the Sandbox preflight passes. Use --dry-run or --verify-config."
    )


if __name__ == "__main__":
    main()
