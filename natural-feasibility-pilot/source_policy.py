"""Best-effort static screen for obvious solver I/O and process capabilities.

This is a policy filter, not a sandbox or security guarantee. Dynamic Python
features can evade source inspection; the execution boundary remains required.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass


BLOCKED_IMPORT_ROOTS = {
    "builtins", "ctypes", "http", "importlib", "io", "multiprocessing",
    "os", "pathlib", "pickle", "requests", "shutil", "socket", "subprocess",
    "sys", "tempfile", "urllib", "webbrowser",
}
BLOCKED_NAMES = {
    "__builtins__", "__import__", "compile", "eval", "exec", "open",
}


@dataclass(frozen=True)
class ScreenResult:
    accepted: bool
    reasons: tuple[str, ...]


def screen_source(source: str) -> ScreenResult:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return ScreenResult(False, (f"syntax:{exc.msg}",))

    reasons: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in BLOCKED_IMPORT_ROOTS:
                    reasons.add(f"blocked-import:{root}")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            if root in BLOCKED_IMPORT_ROOTS:
                reasons.add(f"blocked-import:{root}")
        elif isinstance(node, ast.Name) and node.id in BLOCKED_NAMES:
            reasons.add(f"blocked-name:{node.id}")
        elif isinstance(node, ast.Attribute) and node.attr in {"__builtins__", "__import__"}:
            reasons.add(f"blocked-attribute:{node.attr}")
    return ScreenResult(not reasons, tuple(sorted(reasons)))
