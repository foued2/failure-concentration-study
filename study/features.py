"""Feature computation: k, C, Y, eligibility, solver loading."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from .families import FAMILY_ORDER
from .sssp import dijkstra_ref

PROBES_PER_FAMILY = 5
TOTAL_PROBES = 30


def load_solver(path: str | Path):
    path = Path(path)
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    fn = getattr(mod, "solve", None)
    if fn is None or not callable(fn):
        raise AttributeError("missing solve()")
    return fn


def _norm_ref(d: int | None) -> int:
    return -1 if d is None else d


def run_probes(solve, probes: list[dict]) -> list[bool]:
    """True = probe failed. Exception or wrong output = failure."""
    fails: list[bool] = []
    for p in probes:
        expected = _norm_ref(dijkstra_ref(p["n"], p["edges"], p["s"], p["t"]))
        try:
            out = solve(p["n"], p["edges"], p["s"], p["t"])
            bad = isinstance(out, bool) or not isinstance(out, int) or out != expected
        except Exception:
            bad = True
        fails.append(bool(bad))
    return fails


def family_counts(fails: list[bool]) -> dict[str, int]:
    counts = {f: 0 for f in FAMILY_ORDER}
    for i, f in enumerate(FAMILY_ORDER):
        counts[f] = sum(fails[i * PROBES_PER_FAMILY : (i + 1) * PROBES_PER_FAMILY])
    return counts


def concentration(fails: list[bool]) -> tuple[int, float]:
    k = sum(fails)
    if k == 0:
        return 0, 0.0
    counts = family_counts(fails)
    return k, max(counts.values()) / k


def relabelled_concentration(fails: list[bool], groups: list[list[int]]) -> float:
    k = sum(fails)
    if k == 0:
        return 0.0
    return max(sum(fails[i] for i in g) for g in groups) / k


def balanced_groups(instance_seed: int, r: int) -> list[list[int]]:
    import random

    from .probes import stable_seed

    rng = random.Random(stable_seed(instance_seed, "relabel", r))
    idx = list(range(TOTAL_PROBES))
    rng.shuffle(idx)
    return [sorted(idx[i * 5 : (i + 1) * 5]) for i in range(6)]


def run_hidden(solve, hidden: list[dict]) -> int | None:
    """Y = 1 iff all hidden inputs correct. None only if evaluation could not complete at all."""
    try:
        for h in hidden:
            expected = _norm_ref(dijkstra_ref(h["n"], h["edges"], h["s"], h["t"]))
            try:
                out = solve(h["n"], h["edges"], h["s"], h["t"])
                if isinstance(out, bool) or not isinstance(out, int) or out != expected:
                    return 0
            except Exception:
                return 0
        return 1
    except Exception:
        return None


def evaluate_pair(solve, probes: list[dict], hidden: list[dict]) -> dict:
    fails = run_probes(solve, probes)
    k, c = concentration(fails)
    y = run_hidden(solve, hidden)
    eligible = k >= 2 and y is not None
    return {"fails": fails, "k": k, "C": c, "Y": y, "eligible": eligible}
