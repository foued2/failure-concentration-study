from __future__ import annotations
import ast, os
from pathlib import Path

run_id = os.environ.get("GITHUB_RUN_ID", "local")
attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")
root = Path(os.environ.get("RUNNER_TEMP", "/tmp"))
source_path = root / f"lc518-recovery-work-{run_id}-{attempt}" / "lc518_launcher.py"
output_path = Path.cwd() / "lc518-launcher-static-audit.txt"
if not source_path.is_file():
    raise SystemExit(f"Missing extracted launcher: {source_path}")

source = source_path.read_text(encoding="utf-8")
tree = ast.parse(source, filename=str(source_path))
lines = source.splitlines()
rows = []
for node in ast.walk(tree):
    targets = []
    value = None
    if isinstance(node, ast.Assign):
        targets = [x.id for x in node.targets if isinstance(x, ast.Name)]
        value = node.value
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        targets = [node.target.id]
        value = node.value
    names = [name for name in targets if name.isupper()]
    if names:
        rows.append((node.lineno, sorted(set(names)), ast.unparse(value) if value is not None else "<no value>"))

functions = []
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        functions.append(f"{node.lineno}: {type(node).__name__} {node.name}")

out = [
    "LC518 LAUNCHER STATIC AUDIT",
    "Method: AST parsing only. The launcher was not imported or executed.",
    f"Source: {source_path}",
    "",
    "MODULE-LEVEL / UPPERCASE ASSIGNMENTS:",
]
for line_no, names, value in sorted(rows):
    out.append(f"line {line_no}: {', '.join(names)} = {value}")
out += ["", "TOP-LEVEL DEFINITIONS:", *functions, "", "SOURCE CONTEXT FOR EXECUTION PINS:"]
pin_names = (
    "BANK_GENERATION_AUTHORIZED", "RUN_ROOT", "OUTPUT_DIR", "PROTOCOL_PATH",
    "PROTOCOL_SHA256", "EXPECTED_GENERATOR_PATH", "EXPECTED_GENERATOR_SHA256",
    "EXPECTED_TEST_SUITE_SHA256S", "EXPECTED_PYTHON_VERSION",
    "EXPECTED_PYTHON_EXECUTABLE", "EXPECTED_SYS_VERSION", "EXPECTED_PLATFORM",
    "EXPECTED_INTERPRETER_SHA256", "GENERATOR_PATH",
)
for i, line in enumerate(lines, 1):
    if any(name in line for name in pin_names):
        lo, hi = max(1, i-1), min(len(lines), i+1)
        out.append(f"-- {lo}-{hi} --")
        out.extend(f"{j}: {lines[j-1]}" for j in range(lo, hi+1))
text = "\n".join(out) + "\n"
output_path.write_text(text, encoding="utf-8")
print(text)
