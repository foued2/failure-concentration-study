from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import random
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

BASE_SEED = 20261024
TRIALS = 500
CASES = 5000
FOLDS = 5
EVAL_SIZES = (9, 9, 23, 23, 31, 3)
DIAG_PER_FAMILY = 5
FAMILIES = 6
N_EVAL = sum(EVAL_SIZES)
MIXTURES = (0.0, 0.25, 0.5, 0.75, 1.0)
DESIGN_SHA256 = "a33b475dedbc66eb2d97e490389f3623f2fea29f6b7a98e6ceefb9536d277fd1"
MATH_DIR = Path(__file__).resolve().parent
DESIGN_PATH = MATH_DIR / "10_THREE_WORLD_SIM_DESIGN.md"
DEFAULT_OUTDIR = MATH_DIR / "results" / "three_world"
SCENARIO_PARAMETERS = {
    "diagnostic_probes_per_family": DIAG_PER_FAMILY,
    "evaluation_cases_per_family": list(EVAL_SIZES),
    "mixtures": list(MIXTURES),
    "W1": {"diagnostic_home": 0.8, "diagnostic_other": 0.05, "evaluation_home": 0.35, "evaluation_other": 0.03},
    "W2": {"diagnostic_home": 1.0, "diagnostic_other": 0.0, "evaluation_home": 1.0, "evaluation_other": 0.0},
    "W3": {"diagnostic_home": 0.8, "diagnostic_other": 0.05, "evaluation_home": 0.15, "evaluation_other": 0.15},
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def design_hash() -> str:
    return sha256_bytes(DESIGN_PATH.read_text(encoding="utf-8").encode("utf-8"))


def setting_specs() -> list[dict[str, object]]:
    specs: list[dict[str, object]] = [
        {"key": "W1", "recipe": "W1", "mixture": None},
        {"key": "W2", "recipe": "W2", "mixture": None},
        {"key": "W3", "recipe": "W3", "mixture": None},
    ]
    for value in MIXTURES:
        label = str(value).replace(".", "_")
        specs.append(
            {
                "key": f"MIX_{label}",
                "recipe": "MIX",
                "mixture": value,
            }
        )
    return specs


@dataclass(frozen=True)
class Case:
    f: tuple[int, ...]
    e: tuple[int, ...]
    bits: tuple[int, ...]
    f_alt: tuple[int, int, int]
    k: int
    c: float | None
    c_alt: float | None
    carrier: int
    home_counts: tuple[int, ...]
    defects: int
    world: str
    s_domain: float
    s_equal: float


def union_reach(homes: Sequence[int], home_value: float, other_value: float) -> list[float]:
    complements = [1.0] * FAMILIES
    for home in homes:
        for family in range(FAMILIES):
            reach = home_value if family == home else other_value
            complements[family] *= 1.0 - reach
    return [1.0 - value for value in complements]


def make_w1_or_w3(rng: random.Random, world: str) -> Case:
    defects = rng.randint(1, 4)
    homes = [rng.randrange(FAMILIES) for _ in range(defects)]
    qd = union_reach(homes, 0.8, 0.05)
    if world == "W1":
        qe = union_reach(homes, 0.35, 0.03)
    else:
        qe = union_reach(homes, 0.15, 0.15)
    bits: list[int] = []
    for family in range(FAMILIES):
        probability = qd[family]
        for _ in range(DIAG_PER_FAMILY):
            bits.append(1 if rng.random() < probability else 0)
    f = tuple(sum(bits[family * 5 : (family + 1) * 5]) for family in range(FAMILIES))
    e = tuple(rng.binomialvariate(EVAL_SIZES[family], qe[family]) for family in range(FAMILIES))
    home_counts = tuple(sum(1 for home in homes if home == family) for family in range(FAMILIES))
    return finish_case(f, e, bits, homes[0], home_counts, defects, world)


def make_w2(rng: random.Random) -> Case:
    home = rng.randrange(FAMILIES)
    bits = [0] * 30
    for index in range(home * 5, (home + 1) * 5):
        bits[index] = 1
    f = tuple(5 if family == home else 0 for family in range(FAMILIES))
    e = tuple(EVAL_SIZES[family] if family == home else 0 for family in range(FAMILIES))
    home_counts = tuple(1 if family == home else 0 for family in range(FAMILIES))
    return finish_case(f, e, bits, home, home_counts, 1, "W2")


def finish_case(
    f: tuple[int, ...],
    e: tuple[int, ...],
    bits: Sequence[int],
    carrier: int,
    home_counts: tuple[int, ...],
    defects: int,
    world: str,
) -> Case:
    total = sum(f)
    c = max(f) / total if total else None
    f_alt = (
        sum(bits[0:10]),
        sum(bits[10:20]),
        sum(bits[20:30]),
    )
    c_alt = max(f_alt) / total if total else None
    s_domain = 1.0 - sum(e) / N_EVAL
    s_equal = 1.0 - sum(value / cap for value, cap in zip(e, EVAL_SIZES)) / FAMILIES
    return Case(
        f=f,
        e=e,
        bits=tuple(bits),
        f_alt=f_alt,
        k=total,
        c=c,
        c_alt=c_alt,
        carrier=carrier,
        home_counts=home_counts,
        defects=defects,
        world=world,
        s_domain=s_domain,
        s_equal=s_equal,
    )


def make_case(rng: random.Random, recipe: str, mixture: float | None) -> Case:
    if recipe == "W1":
        return make_w1_or_w3(rng, "W1")
    if recipe == "W2":
        return make_w2(rng)
    if recipe == "W3":
        return make_w1_or_w3(rng, "W3")
    if recipe != "MIX" or mixture is None:
        raise ValueError(f"unknown recipe {recipe!r}")
    if rng.random() < mixture:
        return make_w1_or_w3(rng, "W1")
    return make_w2(rng)


def dot(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def matvec(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def jacobi_eigh(matrix: Sequence[Sequence[float]]) -> tuple[list[float], list[list[float]]]:
    size = len(matrix)
    a = [list(row) for row in matrix]
    v = [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]
    if size == 1:
        return [a[0][0]], v
    scale = max(1.0, max(abs(a[i][i]) for i in range(size)))
    tolerance = 1e-14 * scale
    for _ in range(30):
        changed = False
        for p in range(size - 1):
            for q in range(p + 1, size):
                apq = a[p][q]
                if abs(apq) <= tolerance:
                    continue
                changed = True
                angle = 0.5 * math.atan2(2.0 * apq, a[q][q] - a[p][p])
                cosine = math.cos(angle)
                sine = math.sin(angle)
                for k in range(size):
                    apk = a[p][k]
                    aqk = a[q][k]
                    a[p][k] = cosine * apk - sine * aqk
                    a[q][k] = sine * apk + cosine * aqk
                for k in range(size):
                    akp = a[k][p]
                    akq = a[k][q]
                    a[k][p] = cosine * akp - sine * akq
                    a[k][q] = sine * akp + cosine * akq
                for k in range(size):
                    vkp = v[k][p]
                    vkq = v[k][q]
                    v[k][p] = cosine * vkp - sine * vkq
                    v[k][q] = sine * vkp + cosine * vkq
        if not changed:
            break
    return [a[i][i] for i in range(size)], v


def cholesky_solve(
    matrix: Sequence[Sequence[float]],
    rhs: Sequence[float],
) -> tuple[list[float] | None, int]:
    size = len(rhs)
    lower = [[0.0] * size for _ in range(size)]
    scale = max(1.0, max(abs(matrix[i][i]) for i in range(size)))
    tolerance = 1e-12 * scale
    for i in range(size):
        for j in range(i + 1):
            value = matrix[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if value <= tolerance:
                    return None, 0
                lower[i][j] = math.sqrt(value)
            else:
                lower[i][j] = value / lower[j][j]
    intermediate = [0.0] * size
    for i in range(size):
        intermediate[i] = (
            rhs[i] - sum(lower[i][k] * intermediate[k] for k in range(i))
        ) / lower[i][i]
    beta = [0.0] * size
    for i in range(size - 1, -1, -1):
        beta[i] = (
            intermediate[i] - sum(lower[k][i] * beta[k] for k in range(i + 1, size))
        ) / lower[i][i]
    return beta, size


def solve_psd(matrix: Sequence[Sequence[float]], rhs: Sequence[float]) -> tuple[list[float], int]:
    beta, rank = cholesky_solve(matrix, rhs)
    if beta is not None:
        return beta, rank
    eigenvalues, eigenvectors = jacobi_eigh(matrix)
    largest = max((abs(value) for value in eigenvalues), default=0.0)
    tolerance = max(1e-12, largest * 1e-10)
    rank = 0
    beta = [0.0] * len(rhs)
    for index, eigenvalue in enumerate(eigenvalues):
        if eigenvalue <= tolerance:
            continue
        rank += 1
        vector = [eigenvectors[row][index] for row in range(len(rhs))]
        coefficient = dot(vector, rhs) / eigenvalue
        for row in range(len(rhs)):
            beta[row] += coefficient * vector[row]
    return beta, rank


class NormalEquation:
    __slots__ = ("p", "xx", "xy_domain", "xy_equal")

    def __init__(self, p: int) -> None:
        self.p = p
        self.xx = [[0.0] * p for _ in range(p)]
        self.xy_domain = [0.0] * p
        self.xy_equal = [0.0] * p

    def add(self, x: Sequence[float], y_domain: float, y_equal: float) -> None:
        for i in range(self.p):
            left = x[i]
            for j in range(i, self.p):
                self.xx[i][j] += left * x[j]
            self.xy_domain[i] += left * y_domain
            self.xy_equal[i] += left * y_equal

    def merge(self, other: "NormalEquation") -> None:
        for i in range(self.p):
            for j in range(i, self.p):
                self.xx[i][j] += other.xx[i][j]
            self.xy_domain[i] += other.xy_domain[i]
            self.xy_equal[i] += other.xy_equal[i]

    def finalize(self) -> list[list[float]]:
        for i in range(self.p):
            for j in range(i + 1, self.p):
                self.xx[j][i] = self.xx[i][j]
        return self.xx

    def sse(self, test: "NormalEquation", test_y2: float, score: str) -> tuple[float, int]:
        rhs = self.xy_domain if score == "domain" else self.xy_equal
        beta, rank = solve_psd(self.finalize(), rhs)
        test_xy = test.xy_domain if score == "domain" else test.xy_equal
        fitted = 2.0 * dot(beta, test_xy) - dot(beta, matvec(test.finalize(), beta))
        return max(0.0, test_y2 - fitted), rank


ELIGIBLE_FEATURES = ("C", "F1", "F2", "F3", "F4", "F5", "FAM1", "FAM2", "FAM3", "FAM4", "FAM5", "D")
ELIGIBLE_INDEX = {name: index for index, name in enumerate(ELIGIBLE_FEATURES)}
ALT_FEATURES = ("C_alt", "F1_alt", "F2_alt", "FAM1", "FAM2", "FAM3", "FAM4", "FAM5", "D")
ALT_INDEX = {name: index for index, name in enumerate(ALT_FEATURES)}
C_INDEX = ELIGIBLE_INDEX["C"]
F_INDICES = tuple(ELIGIBLE_INDEX[name] for name in ("F1", "F2", "F3", "F4", "F5"))
FAM_INDICES = tuple(ELIGIBLE_INDEX[name] for name in ("FAM1", "FAM2", "FAM3", "FAM4", "FAM5"))
D_INDEX = ELIGIBLE_INDEX["D"]
ALT_C_INDEX = ALT_INDEX["C_alt"]
ALT_F_INDICES = tuple(ALT_INDEX[name] for name in ("F1_alt", "F2_alt"))
ALT_FAM_INDICES = tuple(ALT_INDEX[name] for name in ("FAM1", "FAM2", "FAM3", "FAM4", "FAM5"))
ALT_D_INDEX = ALT_INDEX["D"]


def family_indicators(carrier: int) -> list[float]:
    indicators = [0.0] * (FAMILIES - 1)
    if carrier < FAMILIES - 1:
        indicators[carrier] = 1.0
    return indicators


def eligible_features(case: Case) -> list[float]:
    if case.c is None:
        raise ValueError("eligible_features requires k > 0")
    return (
        [float(case.c)]
        + [float(value) for value in case.f[:5]]
        + family_indicators(case.carrier)
        + [float(case.defects)]
    )


def alt_features(case: Case) -> list[float]:
    if case.c_alt is None:
        raise ValueError("alt_features requires k > 0")
    return (
        [float(case.c_alt), float(case.f_alt[0]), float(case.f_alt[1])]
        + family_indicators(case.carrier)
        + [float(case.defects)]
    )


class ZStat:
    __slots__ = ("n", "ne", "sx", "sy_domain", "sy2_domain", "sy_equal", "sy2_equal")

    def __init__(self, width: int) -> None:
        self.n = 0
        self.ne = NormalEquation(width)
        self.sx = [0.0] * width
        self.sy_domain = 0.0
        self.sy2_domain = 0.0
        self.sy_equal = 0.0
        self.sy2_equal = 0.0

    def add(self, z: Sequence[float], case: Case) -> None:
        self.n += 1
        self.ne.add(z, case.s_domain, case.s_equal)
        for index, value in enumerate(z):
            self.sx[index] += value
        self.sy_domain += case.s_domain
        self.sy2_domain += case.s_domain * case.s_domain
        self.sy_equal += case.s_equal
        self.sy2_equal += case.s_equal * case.s_equal

    def merge(self, other: "ZStat") -> None:
        self.n += other.n
        self.ne.merge(other.ne)
        for index in range(len(self.sx)):
            self.sx[index] += other.sx[index]
        self.sy_domain += other.sy_domain
        self.sy2_domain += other.sy2_domain
        self.sy_equal += other.sy_equal
        self.sy2_equal += other.sy2_equal


class BasicCell:
    __slots__ = ("n", "sy_domain", "sy2_domain", "sy_equal", "sy2_equal")

    def __init__(self) -> None:
        self.n = 0
        self.sy_domain = 0.0
        self.sy2_domain = 0.0
        self.sy_equal = 0.0
        self.sy2_equal = 0.0

    def add(self, case: Case) -> None:
        self.n += 1
        self.sy_domain += case.s_domain
        self.sy2_domain += case.s_domain * case.s_domain
        self.sy_equal += case.s_equal
        self.sy2_equal += case.s_equal * case.s_equal

    def merge(self, other: "BasicCell") -> None:
        self.n += other.n
        self.sy_domain += other.sy_domain
        self.sy2_domain += other.sy2_domain
        self.sy_equal += other.sy_equal
        self.sy2_equal += other.sy2_equal


def merge_basic(cells: Iterable[BasicCell]) -> BasicCell:
    merged = BasicCell()
    for cell in cells:
        merged.merge(cell)
    return merged


def merge_z_stats(mappings: Iterable[dict[int, ZStat]]) -> dict[int, ZStat]:
    merged: dict[int, ZStat] = {}
    for mapping in mappings:
        for k, stat in mapping.items():
            if k not in merged:
                merged[k] = ZStat(stat.ne.p)
            merged[k].merge(stat)
    return merged


def assemble_design(
    stats_by_k: dict[int, ZStat],
    categories: Sequence[int],
    z_width: int,
) -> tuple[NormalEquation, float, float]:
    z_base = len(categories)
    ne = NormalEquation(z_base + z_width)
    k_column = {k: index + 1 for index, k in enumerate(categories[1:])}
    y2_domain = 0.0
    y2_equal = 0.0
    for k in categories:
        stat = stats_by_k.get(k)
        if stat is None or stat.n == 0:
            continue
        kd = k_column.get(k)
        ne.xx[0][0] += stat.n
        if kd is not None:
            ne.xx[0][kd] += stat.n
            ne.xx[kd][kd] += stat.n
        for j in range(z_width):
            ne.xx[0][z_base + j] += stat.sx[j]
            if kd is not None:
                ne.xx[kd][z_base + j] += stat.sx[j]
            for l in range(j, z_width):
                ne.xx[z_base + j][z_base + l] += stat.ne.xx[j][l]
            ne.xy_domain[z_base + j] += stat.ne.xy_domain[j]
            ne.xy_equal[z_base + j] += stat.ne.xy_equal[j]
        ne.xy_domain[0] += stat.sy_domain
        ne.xy_equal[0] += stat.sy_equal
        if kd is not None:
            ne.xy_domain[kd] += stat.sy_domain
            ne.xy_equal[kd] += stat.sy_equal
        y2_domain += stat.sy2_domain
        y2_equal += stat.sy2_equal
    return ne, y2_domain, y2_equal


def model_columns(categories: Sequence[int], feature_indices: Sequence[int]) -> list[int]:
    z_base = len(categories)
    return [0] + list(range(1, len(categories))) + [z_base + index for index in feature_indices]


def subset_sse(
    train: NormalEquation,
    test: NormalEquation,
    test_y2: float,
    columns: Sequence[int],
    score: str,
) -> tuple[float, int]:
    train_matrix = train.finalize()
    test_matrix = test.finalize()
    scale = max(1.0, max(abs(train_matrix[index][index]) for index in columns))
    tolerance = 1e-12 * scale
    active = [index for index in columns if train_matrix[index][index] > tolerance]
    if not active:
        return max(0.0, test_y2), 0
    submatrix = [[train_matrix[i][j] for j in active] for i in active]
    train_rhs = train.xy_domain if score == "domain" else train.xy_equal
    test_rhs = test.xy_domain if score == "domain" else test.xy_equal
    beta, rank = solve_psd(submatrix, [train_rhs[index] for index in active])
    test_submatrix = [[test_matrix[i][j] for j in active] for i in active]
    fitted = 2.0 * dot(beta, [test_rhs[index] for index in active]) - dot(beta, matvec(test_submatrix, beta))
    return max(0.0, test_y2 - fitted), rank


def evaluate_models(
    eligible_by_fold: list[dict[int, ZStat]],
    include_oracle: bool,
) -> tuple[dict[str, dict[str, float | int]], dict[str, int]]:
    categories = sorted({k for mapping in eligible_by_fold for k in mapping})
    z_width = len(ELIGIBLE_FEATURES)
    model_features = {
        "M0": (),
        "M0fam": FAM_INDICES,
        "M1": (C_INDEX,),
        "M1fam": (C_INDEX,) + FAM_INDICES,
        "MF": F_INDICES + FAM_INDICES,
    }
    if include_oracle:
        model_features["ORACLE"] = (C_INDEX,) + FAM_INDICES + (D_INDEX,)
        model_features["ORACLE_NOC"] = FAM_INDICES + (D_INDEX,)
    totals: dict[str, dict[str, float]] = {score: {model: 0.0 for model in model_features} for score in ("domain", "equal")}
    counts = {model: 0 for model in model_features}
    rank_warnings = {model: 0 for model in model_features}
    for fold in range(FOLDS):
        train_stats = merge_z_stats(eligible_by_fold[other] for other in range(FOLDS) if other != fold)
        test_stats = eligible_by_fold[fold]
        train, _, _ = assemble_design(train_stats, categories, z_width)
        test, test_y2_domain, test_y2_equal = assemble_design(test_stats, categories, z_width)
        test_n = sum(stat.n for stat in test_stats.values())
        if test_n == 0:
            continue
        for model, feature_indices in model_features.items():
            columns = model_columns(categories, feature_indices)
            deficient = False
            for score in ("domain", "equal"):
                test_y2 = test_y2_domain if score == "domain" else test_y2_equal
                sse, rank = subset_sse(train, test, test_y2, columns, score)
                totals[score][model] += sse
                if rank < len(columns):
                    deficient = True
            counts[model] += test_n
            if deficient:
                rank_warnings[model] += 1
    losses: dict[str, dict[str, float]] = {"domain": {}, "equal": {}}
    for score in ("domain", "equal"):
        for model in model_features:
            losses[score][model] = totals[score][model] / counts[model] if counts[model] else float("nan")
    losses["n"] = {model: counts[model] for model in model_features}
    return losses, rank_warnings


def evaluate_partition(alt_by_fold: list[dict[int, ZStat]]) -> dict[str, object]:
    categories = sorted({k for mapping in alt_by_fold for k in mapping})
    z_width = len(ALT_FEATURES)
    model_features = {
        "M0fam": ALT_FAM_INDICES,
        "M1fam": (ALT_C_INDEX,) + ALT_FAM_INDICES,
        "MF": ALT_F_INDICES + ALT_FAM_INDICES,
    }
    totals = {score: {model: 0.0 for model in model_features} for score in ("domain", "equal")}
    rank_warnings = {model: 0 for model in model_features}
    count = 0
    for fold in range(FOLDS):
        train_stats = merge_z_stats(alt_by_fold[other] for other in range(FOLDS) if other != fold)
        test_stats = alt_by_fold[fold]
        train, _, _ = assemble_design(train_stats, categories, z_width)
        test, test_y2_domain, test_y2_equal = assemble_design(test_stats, categories, z_width)
        test_n = sum(stat.n for stat in test_stats.values())
        if test_n == 0:
            continue
        for model, feature_indices in model_features.items():
            columns = model_columns(categories, feature_indices)
            deficient = False
            for score in ("domain", "equal"):
                test_y2 = test_y2_domain if score == "domain" else test_y2_equal
                sse, rank = subset_sse(train, test, test_y2, columns, score)
                totals[score][model] += sse
                if rank < len(columns):
                    deficient = True
            if deficient:
                rank_warnings[model] += 1
        count += test_n
    output: dict[str, object] = {}
    for score in ("domain", "equal"):
        output[score] = {
            "M0fam": totals[score]["M0fam"] / count if count else float("nan"),
            "M1fam": totals[score]["M1fam"] / count if count else float("nan"),
            "MF": totals[score]["MF"] / count if count else float("nan"),
            "delta_pred": (totals[score]["M0fam"] - totals[score]["M1fam"]) / count if count else float("nan"),
            "delta_f": (totals[score]["M1fam"] - totals[score]["MF"]) / count if count else float("nan"),
        }
    output["rank_warnings"] = rank_warnings
    return output


def evaluate_full_baseline(full_cells_by_fold: list[dict[int, BasicCell]]) -> dict[str, float]:
    output: dict[str, float] = {}
    for score in ("domain", "equal"):
        total_sse = 0.0
        total_n = 0
        for fold in range(FOLDS):
            for k, test_cell in full_cells_by_fold[fold].items():
                if test_cell.n == 0:
                    continue
                train_cells = [
                    full_cells_by_fold[other][k]
                    for other in range(FOLDS)
                    if other != fold and k in full_cells_by_fold[other]
                ]
                if not train_cells:
                    continue
                train = merge_basic(train_cells)
                if score == "domain":
                    mean = train.sy_domain / train.n
                    total_sse += (
                        test_cell.sy2_domain
                        - 2.0 * mean * test_cell.sy_domain
                        + test_cell.n * mean * mean
                    )
                else:
                    mean = train.sy_equal / train.n
                    total_sse += (
                        test_cell.sy2_equal
                        - 2.0 * mean * test_cell.sy_equal
                        + test_cell.n * mean * mean
                    )
                total_n += test_cell.n
        output[score] = max(0.0, total_sse / total_n) if total_n else float("nan")
    return output


def overlap_summary(
    c_sets: dict[int, set[int]],
    group_counts: dict[tuple[int, int], Counter],
    group_sums: dict[tuple[int, int], list[float]],
) -> dict[str, object]:
    by_k: dict[str, dict[str, float | int]] = {}
    for k in sorted(c_sets):
        values = sorted(c_sets[k])
        counts = Counter()
        for (group_k, _), counter in group_counts.items():
            if group_k == k:
                counts.update(counter)
        by_k[str(k)] = {
            "distinct_c": len(values),
            "cases": sum(counts.values()),
            "max_cases_at_one_c": max(counts.values()) if counts else 0,
        }
    fixed_strata = 0
    fixed_cases = 0
    fixed_pairs = 0
    for (_, _), counter in group_counts.items():
        if len(counter) > 1:
            fixed_strata += 1
            size = sum(counter.values())
            fixed_cases += size
            fixed_pairs += (size * size - sum(value * value for value in counter.values())) // 2
    residual = 0.0
    for n, sc, scc in group_sums.values():
        if n:
            residual += scc - sc * sc / n
    return {
        "by_k": by_k,
        "fixed_k_carrier_strata": fixed_strata,
        "fixed_k_carrier_cases": fixed_cases,
        "fixed_k_carrier_pairs": fixed_pairs,
        "residualized_c_variance": residual,
    }


def run_trial(
    spec: dict[str, object],
    trial: int,
    cases: int,
    base_seed: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    seed = base_seed + trial
    rng = random.Random(seed)
    fold_rng = random.Random(seed + 7919)
    eligible_by_fold: list[dict[int, ZStat]] = [
        defaultdict(lambda: ZStat(len(ELIGIBLE_FEATURES))) for _ in range(FOLDS)
    ]
    alt_by_fold: list[dict[int, ZStat]] = [
        defaultdict(lambda: ZStat(len(ALT_FEATURES))) for _ in range(FOLDS)
    ]
    full_cells_by_fold: list[dict[int, BasicCell]] = [defaultdict(BasicCell) for _ in range(FOLDS)]
    c_sets: dict[int, set[int]] = defaultdict(set)
    c_group_counts: dict[tuple[int, int], Counter] = defaultdict(Counter)
    c_group_sums: dict[tuple[int, int], list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0])
    world_c_sets: dict[str, dict[int, set[int]]] = defaultdict(lambda: defaultdict(set))
    world_group_counts: dict[str, dict[tuple[int, int], Counter]] = defaultdict(lambda: defaultdict(Counter))
    world_group_sums: dict[str, dict[tuple[int, int], list[float]]] = defaultdict(
        lambda: defaultdict(lambda: [0.0, 0.0, 0.0])
    )
    world_counts: Counter = Counter()
    world_k0: Counter = Counter()
    world_scores: dict[str, list[float]] = defaultdict(list)
    world_c: dict[str, list[float]] = defaultdict(list)
    raw: list[dict[str, object]] = []
    k0 = 0
    recipe = str(spec["recipe"])
    mixture = spec.get("mixture")
    mixture_value = float(mixture) if mixture is not None else None
    for case_index in range(cases):
        fold = fold_rng.randrange(FOLDS)
        case = make_case(rng, recipe, mixture_value)
        world_counts[case.world] += 1
        world_scores[case.world].append(case.s_domain)
        full_cells_by_fold[fold][case.k].add(case)
        if case.k == 0:
            k0 += 1
            world_k0[case.world] += 1
        else:
            eligible_by_fold[fold][case.k].add(eligible_features(case), case)
            alt_by_fold[fold][case.k].add(alt_features(case), case)
            world_c[case.world].append(float(case.c))
            c_sets[case.k].add(max(case.f))
            key = (case.k, case.carrier)
            c_group_counts[key][max(case.f)] += 1
            c_group_sums[key][0] += 1
            c_group_sums[key][1] += case.c
            c_group_sums[key][2] += case.c * case.c
            world_sets = world_c_sets[case.world]
            world_sets[case.k].add(max(case.f))
            world_group_counts[case.world][key][max(case.f)] += 1
            world_group_sums[case.world][key][0] += 1
            world_group_sums[case.world][key][1] += case.c
            world_group_sums[case.world][key][2] += case.c * case.c
        raw.append(
            {
                "trial": trial,
                "case": case_index,
                "fold": fold,
                "setting": spec["key"],
                "world": case.world,
                "F": list(case.f),
                "E": list(case.e),
                "F_alt": list(case.f_alt),
                "k": case.k,
                "C": case.c,
                "C_alt": case.c_alt,
                "carrier": case.carrier,
                "home_counts": list(case.home_counts),
                "defects": case.defects,
                "S_domain": case.s_domain,
                "S_equal": case.s_equal,
                "diag_bits": "".join(str(bit) for bit in case.bits),
            }
        )
    include_oracle = spec["key"] == "W3"
    losses, rank_warnings = evaluate_models(eligible_by_fold, include_oracle)
    full_baseline = evaluate_full_baseline(full_cells_by_fold)
    for score in ("domain", "equal"):
        losses[score]["M0_full"] = full_baseline[score]
    partition = evaluate_partition(alt_by_fold)
    delta_pred = {
        score: losses[score]["M0fam"] - losses[score]["M1fam"]
        for score in ("domain", "equal")
    }
    delta_f = {
        score: losses[score]["M1fam"] - losses[score]["MF"]
        for score in ("domain", "equal")
    }
    oracle = None
    if include_oracle:
        oracle = {
            score: {
                "delta_c_after_defects": losses[score]["ORACLE_NOC"] - losses[score]["ORACLE"],
                "delta_c_without_defects": losses[score]["M0fam"] - losses[score]["M1fam"],
            }
            for score in ("domain", "equal")
        }
    summary = {
        "setting": spec["key"],
        "recipe": recipe,
        "mixture": mixture_value,
        "trial": trial,
        "seed": seed,
        "n_cases": cases,
        "n_eligible": cases - k0,
        "n_k0": k0,
        "world_counts": dict(world_counts),
        "k0_by_world": dict(world_k0),
        "world_descriptive": {
            world: {
                "n": len(values),
                "n_k0": world_k0[world],
                "mean_s_domain": sum(values) / len(values),
                "mean_c": sum(world_c[world]) / len(world_c[world]) if world_c[world] else None,
            }
            for world, values in world_scores.items()
        },
        "parameters": SCENARIO_PARAMETERS,
        "losses": losses,
        "delta_pred": delta_pred,
        "delta_f": delta_f,
        "partition": partition,
        "overlap": overlap_summary(c_sets, c_group_counts, c_group_sums),
        "overlap_by_world": {
            world: overlap_summary(
                world_c_sets[world],
                world_group_counts[world],
                world_group_sums[world],
            )
            for world in sorted(world_counts)
        },
        "oracle": oracle,
        "rank_warnings": rank_warnings,
    }
    return summary, raw


def quantile(values: Sequence[float], q: float) -> float:
    if not values:
        return float("nan")
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def interval(values: Sequence[float]) -> dict[str, float]:
    return {
        "mean": sum(values) / len(values) if values else float("nan"),
        "low": quantile(values, 0.025),
        "high": quantile(values, 0.975),
        "positive_fraction": sum(1 for value in values if value > 0) / len(values) if values else float("nan"),
    }


def summarize_trials(trials: Sequence[dict[str, object]], key: str) -> dict[str, object]:
    selected = [trial for trial in trials if trial["setting"] == key]
    output: dict[str, object] = {"n_trials": len(selected)}
    for score in ("domain", "equal"):
        output[score] = {
            "delta_pred": interval([float(trial["delta_pred"][score]) for trial in selected]),
            "delta_f": interval([float(trial["delta_f"][score]) for trial in selected]),
            "partition_delta": interval([float(trial["partition"][score]["delta_pred"]) for trial in selected]),
            "m0fam": interval([float(trial["losses"][score]["M0fam"]) for trial in selected]),
            "m1fam": interval([float(trial["losses"][score]["M1fam"]) for trial in selected]),
            "mf": interval([float(trial["losses"][score]["MF"]) for trial in selected]),
            "m0_full": interval([float(trial["losses"][score]["M0_full"]) for trial in selected]),
        }
    output["k0_total"] = sum(int(trial["n_k0"]) for trial in selected)
    output["eligible_total"] = sum(int(trial["n_eligible"]) for trial in selected)
    world_counts: Counter = Counter()
    world_k0: Counter = Counter()
    for trial in selected:
        world_counts.update(trial["world_counts"])
        world_k0.update(trial["k0_by_world"])
    total_cases = sum(world_counts.values())
    output["world_counts"] = dict(world_counts)
    output["world_fractions"] = {
        world: count / total_cases for world, count in world_counts.items()
    } if total_cases else {}
    output["k0_by_world"] = dict(world_k0)
    output["overlap_by_world"] = {
        world: {
            "cases": sum(int(trial["overlap_by_world"][world]["fixed_k_carrier_cases"]) for trial in selected),
            "strata": sum(int(trial["overlap_by_world"][world]["fixed_k_carrier_strata"]) for trial in selected),
            "residualized_c_variance": sum(
                float(trial["overlap_by_world"][world]["residualized_c_variance"]) for trial in selected
            ),
        }
        for world in world_counts
    }
    world_descriptive: dict[str, dict[str, float | int | None]] = {}
    for world in world_counts:
        entries = [trial["world_descriptive"][world] for trial in selected if world in trial["world_descriptive"]]
        n_total = sum(int(entry["n"]) for entry in entries)
        c_entries = [float(entry["mean_c"]) for entry in entries if entry.get("mean_c") is not None]
        world_descriptive[world] = {
            "n": n_total,
            "k0": sum(int(entry["n_k0"]) for entry in entries),
            "mean_s_domain": (
                sum(float(entry["mean_s_domain"]) * int(entry["n"]) for entry in entries) / n_total
                if n_total else None
            ),
            "mean_c": sum(c_entries) / len(c_entries) if c_entries else None,
        }
    output["world_descriptive"] = world_descriptive
    output["overlap_cases"] = sum(int(trial["overlap"]["fixed_k_carrier_cases"]) for trial in selected)
    output["overlap_strata"] = sum(int(trial["overlap"]["fixed_k_carrier_strata"]) for trial in selected)
    output["overlap_pairs"] = sum(int(trial["overlap"]["fixed_k_carrier_pairs"]) for trial in selected)
    output["overlap_residualized_variance"] = sum(
        float(trial["overlap"]["residualized_c_variance"]) for trial in selected
    )
    output["partition_rank_warnings"] = {
        model: sum(int(trial["partition"]["rank_warnings"].get(model, 0)) for trial in selected)
        for model in selected[0]["partition"]["rank_warnings"]
    } if selected else {}
    output["rank_warnings"] = {
        model: sum(int(trial["rank_warnings"].get(model, 0)) for trial in selected)
        for model in selected[0]["rank_warnings"]
    } if selected else {}
    if selected and selected[0].get("oracle") is not None:
        output["oracle"] = {
            score: interval([float(trial["oracle"][score]["delta_c_after_defects"]) for trial in selected])
            for score in ("domain", "equal")
        }
        output["oracle_without_defects"] = {
            score: interval([float(trial["oracle"][score]["delta_c_without_defects"]) for trial in selected])
            for score in ("domain", "equal")
        }
    return output


def write_report(
    trials: Sequence[dict[str, object]],
    specs: Sequence[dict[str, object]],
    outdir: Path,
    manifest: dict[str, object],
) -> None:
    raw_bytes = sum(item["bytes"] for item in manifest["raw"].values())
    lines = [
        "# Three-world concentration simulation result",
        "",
        "**Scope:** Synthetic-data simulation only. Results show implications of the declared assumptions; they are not evidence about real solvers.",
        "",
        f"Trials per setting: {manifest['trials']}; cases per trial: {manifest['cases']}; base seed: {manifest['base_seed']}.",
        f"Frozen design SHA-256: `{manifest['design_sha256']}`; script SHA-256: `{manifest['script_sha256']}`.",
        f"Runtime: {manifest['runtime_seconds']:.2f} s; raw gzip bytes: {raw_bytes}.",
        "World reaches: W1 diagnostic 0.80/0.05, evaluation 0.35/0.03; W2 1/0, 1/0; W3 diagnostic 0.80/0.05, evaluation 0.15/0.15 (home/other).",
        "",
        "The intervals below are central 95% simulation-trial intervals, not confidence intervals about a real population.",
        "",
    ]
    failed: list[str] = []
    for spec in specs:
        key = str(spec["key"])
        summary = summarize_trials(trials, key)
        lines.append(f"## {key}")
        lines.append("")
        lines.append(
            "| Score | C gain mean | C gain 95% interval | Positive trials | F-vs-C mean | F-vs-C 95% interval | Partition C gain mean | Partition 95% interval |"
        )
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for score in ("domain", "equal"):
            item = summary[score]
            c = item["delta_pred"]
            f = item["delta_f"]
            p = item["partition_delta"]
            lines.append(
                f"| {score} | {c['mean']:.6f} | [{c['low']:.6f}, {c['high']:.6f}] | {c['positive_fraction']:.3f} | "
                f"{f['mean']:.6f} | [{f['low']:.6f}, {f['high']:.6f}] | {p['mean']:.6f} | "
                f"[{p['low']:.6f}, {p['high']:.6f}] |"
            )
        lines.append("")
        world_counts = summary["world_counts"]
        world_text = ", ".join(
            f"{world}={world_counts[world]} ({summary['world_fractions'][world]:.3f})"
            for world in sorted(world_counts)
        )
        k0_text = ", ".join(
            f"{world}={summary['k0_by_world'].get(world, 0)}" for world in sorted(world_counts)
        )
        lines.append(
            f"Eligible cases: {summary['eligible_total']}; k=0 cases: {summary['k0_total']} "
            f"({k0_text}); world cases: {world_text}."
        )
        lines.append(
            f"Fixed-k carrier overlap: cases={summary['overlap_cases']}, strata={summary['overlap_strata']}, "
            f"pairs={summary['overlap_pairs']}, residualized C variance={summary['overlap_residualized_variance']:.6g}."
        )
        for world in sorted(summary["overlap_by_world"]):
            item = summary["overlap_by_world"][world]
            lines.append(
                f"Overlap in {world}: cases={item['cases']}, strata={item['strata']}, "
                f"residualized C variance={item['residualized_c_variance']:.6g}."
            )
        lines.append("")
        lines.append("| World | Cases | k=0 | Mean S_domain | Mean C (k>0) |")
        lines.append("| --- | ---: | ---: | ---: | ---: |")
        for world in sorted(summary["world_descriptive"]):
            item = summary["world_descriptive"][world]
            mean_c = "N/A" if item["mean_c"] is None else f"{item['mean_c']:.6f}"
            lines.append(
                f"| {world} | {item['n']} | {item['k0']} | {item['mean_s_domain']:.6f} | {mean_c} |"
            )
        rank_text = ", ".join(f"{model}={count}" for model, count in summary["rank_warnings"].items())
        part_rank_text = ", ".join(
            f"{model}={count}" for model, count in summary["partition_rank_warnings"].items()
        )
        lines.append(f"Rank warnings (primary / alternate partition): {rank_text} / {part_rank_text}.")
        if any(summary["rank_warnings"].values()) or any(summary["partition_rank_warnings"].values()):
            lines.append("Rank warnings mean a fold-level parameterization is not identified; parameter interpretation is unavailable for those fits.")
        lines.append(
            f"Full-cohort M0 baseline (domain/equal): "
            f"{summary['domain']['m0_full']['mean']:.6f} / {summary['equal']['m0_full']['mean']:.6f}."
        )
        lines.append("")
        if "oracle" in summary:
            for score in ("domain", "equal"):
                oracle = summary["oracle"][score]
                primary = summary["oracle_without_defects"][score]
                lines.append(
                    f"W3 oracle C-after-defects {score}: mean={oracle['mean']:.6f}, "
                    f"95%=[{oracle['low']:.6f}, {oracle['high']:.6f}], positive={oracle['positive_fraction']:.3f}. "
                    f"W3 primary C gain {score}: mean={primary['mean']:.6f}, "
                    f"95%=[{primary['low']:.6f}, {primary['high']:.6f}]."
                )
            lines.append("")
        c_positive = all(summary[score]["delta_pred"]["mean"] > 0 for score in ("domain", "equal"))
        c_interval = all(summary[score]["delta_pred"]["low"] > 0 for score in ("domain", "equal"))
        overlap_ok = (
            summary["overlap_cases"] > 0
            and summary["overlap_strata"] > 0
            and summary["overlap_residualized_variance"] > 1e-9
        )
        partition_ok = all(summary[score]["partition_delta"]["mean"] > 0 for score in ("domain", "equal"))
        c_survives = c_positive and c_interval and overlap_ok and partition_ok
        lines.append("### Criteria")
        lines.append("")
        lines.append("| Criterion | Domain | Equal | Outcome |")
        lines.append("| --- | --- | --- | --- |")
        for label, metric in (
            ("Family-adjusted C gain positive with 95% interval above zero", "delta_pred"),
            ("Alternate diagnostic-partition C gain positive", "partition_delta"),
            ("Full vector beats C (95% interval above zero)", "delta_f"),
        ):
            cells = []
            passes = []
            for score in ("domain", "equal"):
                item = summary[score][metric]
                if metric == "delta_f":
                    passed = item["low"] > 0
                else:
                    passed = item["mean"] > 0 and item["low"] > 0
                passes.append(passed)
                cells.append("PASS" if passed else "FAIL")
            lines.append(f"| {label} | {cells[0]} | {cells[1]} | {'PASS' if all(passes) else 'FAIL'} |")
        lines.append(
            f"| Usable fixed-k, different-C overlap | {'PASS' if overlap_ok else 'ABSENT'} | "
            f"{'PASS' if overlap_ok else 'ABSENT'} | {'PASS' if overlap_ok else 'ABSENT'} |"
        )
        if key == "W1":
            outcome = "PASS" if c_survives else "DOES NOT SURVIVE"
            w1_wiring = c_positive and c_interval
            if not w1_wiring:
                failed.append(f"{key}: W1 wiring / positive-direction interval criterion failed")
            for score in ("domain", "equal"):
                if not (summary[score]["delta_pred"]["mean"] > 0 and summary[score]["delta_pred"]["low"] > 0):
                    failed.append(f"{key}/{score}: family-adjusted C gain not positive with interval above zero")
        elif key == "W2":
            w2_unidentifiable = (
                summary["overlap_cases"] == 0
                and summary["overlap_strata"] == 0
                and summary["overlap_residualized_variance"] <= 1e-9
            )
            outcome = "PASS (unidentifiable as expected)" if w2_unidentifiable else "FAILED"
            if not w2_unidentifiable:
                failed.append(f"{key}: W2 supplied within-k C variation; overlap negative control failed")
        elif key == "W3":
            oracle_ok = all(
                not (summary["oracle"][score]["low"] > 0 or summary["oracle"][score]["high"] < 0)
                for score in ("domain", "equal")
            )
            outcome = "PASS" if oracle_ok else "FAILED"
            if not oracle_ok:
                failed.append(f"{key}: W3 oracle C-after-defects interval excludes zero")
        else:
            outcome = "DESCRIPTIVE"
        if key == "W1":
            c_cell = "PASS" if c_survives else "FAIL"
            c_cells = (c_cell, c_cell)
        else:
            c_cells = ("N/A", "N/A")
        lines.append(
            f"| C survives under this simulation's criteria | {c_cells[0]} | {c_cells[1]} | {outcome} |"
        )
        lines.append("")
        for score in ("domain", "equal"):
            if summary[score]["delta_f"]["low"] > 0:
                lines.append(f"{key}/{score}: full vector beats C under the finite-sample predictor.")
        lines.append("")
    lines.append("## Failed checks")
    lines.append("")
    if failed:
        lines.extend(f"- {item}" for item in dict.fromkeys(failed))
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Limits")
    lines.append("")
    lines.append(
        "W1 is constructed to make concentration informative; its positive result is a wiring check, not evidence for the real-world hypothesis. "
        "W2 is an overlap negative control. W3 separates direct concentration effects from proxy information about latent defect count. "
        "The mixture sweep is a stress test, not an estimate of real-world prevalence. The generative model treats diagnostic and evaluation failures as independent Bernoulli draws and does not preserve input-level dependence."
    )
    (outdir / "11_THREE_WORLD_SIM_RESULT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def run(
    trials_count: int,
    cases_count: int,
    base_seed: int,
    outdir: Path,
) -> None:
    expected = design_hash()
    if expected != DESIGN_SHA256:
        raise RuntimeError(f"frozen design hash mismatch: {expected}")
    outdir.mkdir(parents=True, exist_ok=True)
    raw_dir = outdir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    specs = setting_specs()
    per_trial: list[dict[str, object]] = []
    raw_manifest: dict[str, dict[str, object]] = {}
    started = time.perf_counter()
    for spec in specs:
        key = str(spec["key"])
        raw_path = raw_dir / f"{key}.jsonl.gz"
        record_count = 0
        with gzip.open(raw_path, "wt", encoding="utf-8", compresslevel=6) as handle:
            for trial in range(trials_count):
                summary, raw = run_trial(spec, trial, cases_count, base_seed)
                for record in raw:
                    handle.write(json.dumps(record, separators=(",", ":")) + "\n")
                record_count += len(raw)
                per_trial.append(summary)
                if trial % 10 == 0:
                    print(f"{key}: trial {trial + 1}/{trials_count}", file=sys.stderr)
        raw_manifest[key] = {
            "path": str(raw_path.relative_to(outdir)),
            "records": record_count,
            "bytes": raw_path.stat().st_size,
            "sha256": sha256_file(raw_path),
        }
        print(f"{key}: complete", file=sys.stderr)
    elapsed = time.perf_counter() - started
    per_trial_path = outdir / "per_trial.json"
    per_trial_path.write_text(json.dumps(per_trial, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "design_sha256": expected,
        "script_sha256": sha256_file(Path(__file__)),
        "base_seed": base_seed,
        "trials": trials_count,
        "cases": cases_count,
        "settings": [spec["key"] for spec in specs],
        "parameters": SCENARIO_PARAMETERS,
        "per_trial": {
            "path": per_trial_path.name,
            "records": len(per_trial),
            "bytes": per_trial_path.stat().st_size,
            "sha256": sha256_file(per_trial_path),
        },
        "raw": raw_manifest,
        "runtime_seconds": elapsed,
    }
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    write_report(per_trial, specs, outdir, manifest)
    print(json.dumps({"outdir": str(outdir), "runtime_seconds": elapsed, "raw": raw_manifest}, indent=2))


def self_test() -> None:
    assert design_hash() == DESIGN_SHA256
    rng = random.Random(123)
    for world in ("W1", "W2", "W3"):
        for _ in range(100):
            case = make_w1_or_w3(rng, world) if world != "W2" else make_w2(rng)
            assert len(case.f) == 6 and len(case.e) == 6 and len(case.bits) == 30
            assert all(0 <= value <= 5 for value in case.f)
            assert all(0 <= value <= cap for value, cap in zip(case.e, EVAL_SIZES))
            assert sum(case.f) == case.k
            assert sum(case.f_alt) == case.k
            assert abs(case.s_domain - (1.0 - sum(case.e) / N_EVAL)) < 1e-15
            if case.k == 0:
                assert case.c is None
            else:
                assert case.c is not None and case.c_alt is not None
                assert 0.0 <= case.c <= 1.0 and 0.0 <= case.c_alt <= 1.0
    w2 = make_w2(random.Random(9))
    assert w2.c == 1.0 and w2.k == 5
    equation = NormalEquation(2)
    for value in range(-10, 11):
        equation.add([1.0, float(value)], 2.0 + 3.0 * value, 2.0 + 3.0 * value)
    beta, rank = solve_psd(equation.finalize(), equation.xy_domain)
    assert rank == 2
    assert abs(beta[0] - 2.0) < 1e-8 and abs(beta[1] - 3.0) < 1e-8
    singular = NormalEquation(2)
    for value in (1.0, 2.0, 3.0):
        singular.add([1.0, 1.0], value, value)
    beta, rank = solve_psd(singular.finalize(), singular.xy_domain)
    assert rank == 1 and abs(sum(beta) - 2.0) < 1e-8
    summary, raw = run_trial({"key": "W1", "recipe": "W1", "mixture": None}, 0, 200, 20261024)
    assert len(raw) == 200
    assert summary["n_cases"] == 200
    assert summary["n_eligible"] + summary["n_k0"] == 200
    assert any(case["C"] != case["C_alt"] for case in raw if case["C"] is not None)
    assert summary["partition"]["domain"]["M1fam"] != summary["losses"]["domain"]["M1fam"]
    w2_summary, _ = run_trial({"key": "W2", "recipe": "W2", "mixture": None}, 0, 200, 20261024)
    assert abs(w2_summary["delta_pred"]["domain"]) < 1e-12
    assert w2_summary["overlap"]["fixed_k_carrier_cases"] == 0
    assert w2_summary["rank_warnings"]["M1fam"] > 0
    w3_summary, _ = run_trial({"key": "W3", "recipe": "W3", "mixture": None}, 0, 200, 20261024)
    assert w3_summary["oracle"] is not None
    print("SELF-TEST PASS")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=TRIALS)
    parser.add_argument("--cases", type=int, default=CASES)
    parser.add_argument("--seed", type=int, default=BASE_SEED)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.self_test:
        self_test()
        return 0
    run(args.trials, args.cases, args.seed, args.outdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
