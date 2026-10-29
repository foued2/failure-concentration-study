"""Pure planning/extraction helpers for a future V10 generator.

This module makes no provider requests and writes no candidate files. It copies
the frozen V3 batch mapping and prompt text for review, while explicitly marking
the proposed direct-provider configuration as unfrozen and not executable.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V3_GENERATOR_PATH = ROOT / "h3-footprint-v3" / "generate.py"
V3_FREEZE_PATH = ROOT / "h3-footprint-v3" / "FREEZE.json"
PLAN_STATUS = "DRAFT_NOT_FROZEN"
GENERATION_PERMITTED = False
BODIES_PER_BATCH = 8
MAX_BATCHES = 400
ROUTE_IDS = ("deepseek", "glm", "mimo")
EXPECTED_VARIANTS = ("direct", "menu", "simple")


def _verify_v3_generator_source(path: Path, freeze_path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError("frozen V3 generator source is unavailable")
    if not freeze_path.is_file():
        raise FileNotFoundError("V3 freeze manifest is unavailable")
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    expected = (freeze.get("artifact_hashes_sha256") or {}).get("generate.py")
    if not isinstance(expected, str) or len(expected) != 64:
        raise ValueError("V3 freeze manifest has no valid generate.py SHA-256")
    actual = hashlib.sha256(path.read_bytes().replace(b"\\r\\n", b"\\n")).hexdigest()
    if actual != expected:
        raise ValueError("V3 generate.py does not match the frozen SHA-256")
    return actual


V3_GENERATOR_SOURCE_SHA256 = _verify_v3_generator_source(V3_GENERATOR_PATH, V3_FREEZE_PATH)


def _load_v3_generator():
    spec = importlib.util.spec_from_file_location("h3_v3_generation_reference", V3_GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load frozen V3 generator source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_V3 = _load_v3_generator()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_source(source: str) -> str:
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in source.split("\n")]
    return "\n".join(lines).strip() + "\n"


def source_sha256(source: str) -> str:
    return _sha256_text(normalize_source(source))


def plan_batch(batch_id: int) -> dict[str, Any]:
    """Return the exact V3 prompt/assignment for a proposed batch, with execution disabled."""
    if type(batch_id) is not int or not 0 <= batch_id < MAX_BATCHES:
        raise ValueError(f"batch_id must be an integer from 0 through {MAX_BATCHES - 1}")
    route_id = ROUTE_IDS[batch_id % len(ROUTE_IDS)]
    variant = EXPECTED_VARIANTS[(batch_id // len(ROUTE_IDS)) % len(EXPECTED_VARIANTS)]
    prompt = _V3.PROMPTS[variant].format(n=BODIES_PER_BATCH)
    return {
        "batch_id": batch_id,
        "provenance_group": f"batch-{batch_id:03d}",
        "route_id": route_id,
        "original_route_alias": _V3.MODELS[batch_id % len(_V3.MODELS)],
        "prompt_variant": variant,
        "requested_bodies": BODIES_PER_BATCH,
        "prompt": prompt,
        "prompt_sha256": _sha256_text(prompt),
        "v3_generator_source_sha256": V3_GENERATOR_SOURCE_SHA256,
        "plan_status": PLAN_STATUS,
        "generation_permitted": False,
        "temperature": None,
        "max_output_tokens": None,
        "request_timeout_seconds": None,
        "sampling_configuration_status": "NOT_FROZEN",
        "network_request_performed": False,
    }


def extract_candidates(response_text: str) -> list[str]:
    """Use the same safe AST extraction rule as V3; never import or execute source."""
    if not isinstance(response_text, str):
        raise TypeError("response_text must be text")
    return _V3.extract(response_text)


def record_response_metadata(batch_id: int, response_text: str) -> dict[str, Any]:
    """Produce a redacted in-memory batch record without persisting candidate content."""
    plan = plan_batch(batch_id)
    bodies = extract_candidates(response_text)
    records = []
    for index, body in enumerate(bodies):
        normalized = normalize_source(body)
        try:
            parsed = ast.parse(normalized)
            solve_defs = [
                node for node in parsed.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "solve"
            ]
        except SyntaxError:
            solve_defs = []
        if len(solve_defs) != 1 or isinstance(solve_defs[0], ast.AsyncFunctionDef):
            raise ValueError("extractor returned a body outside the frozen solve() contract")
        records.append({
            "candidate_index": index,
            "body_sha256": _sha256_text(normalized),
            "normalized_source_characters": len(normalized),
            "provenance_group": plan["provenance_group"],
        })
    count = len(records)
    if count < BODIES_PER_BATCH:
        outcome = "UNDERPRODUCED"
    elif count > BODIES_PER_BATCH:
        outcome = "OVERPRODUCED"
    else:
        outcome = "COMPLETE"
    return {
        "batch_id": batch_id,
        "provenance_group": plan["provenance_group"],
        "route_id": plan["route_id"],
        "original_route_alias": plan["original_route_alias"],
        "prompt_variant": plan["prompt_variant"],
        "requested_bodies": BODIES_PER_BATCH,
        "extracted_bodies": count,
        "batch_outcome": outcome,
        "body_hashes_in_response_order": [record["body_sha256"] for record in records],
        "candidate_records": records,
        "response_sha256": _sha256_text(response_text),
        "response_characters": len(response_text),
        "raw_response_persisted": False,
        "provider_call_performed_by_helper": False,
        "retries_observed_by_helper": None,
        "best_of_selection_performed_by_helper": False,
        "generation_permitted": False,
        "plan_status": PLAN_STATUS,
    }


def assert_generation_disabled() -> None:
    """Fail closed until a separately reviewed, hashed V10 freeze exists."""
    raise RuntimeError(
        "V10 candidate generation is disabled: provider smoke, quota review, "
        "protocol amendment, and pre-candidate freeze are incomplete"
    )
