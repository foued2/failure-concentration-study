"""Frozen scientific constants carried forward from V8.

These values are copied verbatim from the frozen V8 artifact set. They are not
tuned by this implementation. A change to any value here is a protocol change
and requires separate authorization.
"""

from __future__ import annotations

FAMILY_ORDER = ["R", "Z", "A", "I", "S", "U"]
PROBES_PER_FAMILY = 5
PROBE_COUNT = len(FAMILY_ORDER) * PROBES_PER_FAMILY

ELIGIBLE_MIN_K = 2
ELIGIBLE_MAX_K = 24
SATURATION_MAX = 0.80

PROBE_TIMEOUT_SECONDS = 5.0
PREFLIGHT_TIMEOUT_SECONDS = 5.0

MEMORY_LIMIT_BYTES = 512 * 1024 * 1024
MAX_PROCESSES_PER_CANDIDATE = 16
MAX_CHILD_STDOUT_BYTES = 4096

MODELS = [
    "opencode/deepseek-v4.1-flash-free",
    "opencode/glm-5.3-flash-free",
    "opencode/mimo-v2.6-flash-free",
]
PROMPT_VARIANTS = ["direct", "menu", "simple"]
BODIES_PER_BATCH = 8
MAX_BATCHES = 400

FUTILITY_CHECKPOINTS = {100: 10, 200: 20, 300: 30}
M_MIN_GROUPS_PER_LEVEL = 4
PASS_MIN_CELLS = 3
PASS_MIN_DISTINCT_K = 2
PASS_MIN_GROUPS = 40
