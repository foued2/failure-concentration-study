"""Independent W1 verification for the frozen three-world synthetic simulation.

Work order: GLM independent W1 verification (one bounded verification; W1 remains
FAILED unless a demonstrable implementation defect is established).

Boundaries honoured:
- Standard library only. No NumPy or any third-party numerical package.
- No import of, or call into, 'simulate_worlds.py', 'analyze_three_world_review.py'
  or any other project module. The linear algebra, the generator, and the metrics
  below are implemented here from the frozen design text.
- W1 only. W2, W3 and the mixtures are not touched. Reach probabilities, model
  terms, scoring formulas, folds, eligibility rules, criteria and interval
  definitions follow the frozen design exactly.

What runs:
- Verification A: the W1 data generator is re-implemented from the frozen formulas
  using the same pseudorandom draw order (case RNG and fold RNG are separate
  streams; trial seed = 20261024 + trial_index; the fold is drawn before each case;
  per case: randint(1,4) -> randrange(6) per defect -> 30 rng.random() diagnostic
  bits family-major -> 6 binomialvariate evaluation draws family-major), and every
  generated case is compared semantically, field by field, against the saved
  local-only original archive raw/W1.jsonl.gz. The archive is opened read-only;
  nothing anywhere else is overwritten.
- Verification B: the frozen M0+fam and M1+fam comparison is fitted independently
  from the SAVED original records only (never from the regenerated stream), using
  the original fold assignments: five-fold cross-validation, eligible cases k>0,
  categorical k (one dummy per k except a reference category = the smallest
  eligible k observed in the trial), five anchor-family indicators (family 6
  omitted), ordinary least squares, per-case held-out squared error, loss over all
  held-out eligible cases. The alternate diagnostic partition (original families
  (1,2),(3,4),(5,6), recomputing F, k, C from the same 30 diagnostic bits with the
  evaluation scores unchanged) and the represented-k sensitivity (held-out
  eligible cases whose k occurs in that fold's training data, both models scored
  on exactly the same subset) are computed from the same saved cases and folds.

Only output written: independent_w1_run.json inside this script's own directory.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import platform
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Frozen design quantities, independently transcribed from the design document
# ---------------------------------------------------------------------------
BASE_SEED = 20261024
TRIALS = 500
CASES = 5000
FOLDS = 5
FAMILIES = 6
DIAG_PER_FAMILY = 5
EVAL_SIZES = (9, 9, 23, 23, 31, 3)
N_EVAL = sum(EVAL_SIZES)
FOLD_SEED_OFFSET = 7919
W1_DIAG_HOME = 0.8
W1_DIAG_OTHER = 0.05
W1_EVAL_HOME = 0.35
W1_EVAL_OTHER = 0.03
ALT_GROUP_SLICES = ((0, 10), (10, 20), (20, 30))

HERE = Path(__file__).resolve().parent
THREE_WORLD_DIR = HERE.parent
DESIGN_PATH = THREE_WORLD_DIR.parent.parent / "10_THREE_WORLD_SIM_DESIGN.md"
RAW_W1_PATH = THREE_WORLD_DIR / "raw" / "W1.jsonl.gz"
PER_TRIAL_PATH = THREE_WORLD_DIR / "per_trial.json"
REVIEW_METRICS_PATH = THREE_WORLD_DIR / "12_review_correction_metrics.json"
W1_RAW_SHA256_EXPECTED = "544e920010b23f63b104781966ba3c4b84cd6ef3de47067b02a5e7b83f57ae85"
PER_TRIAL_SHA256_EXPECTED = "b6761998db3a64cecbdc33b05d97625409422ce8919dee9eedfe289ee457556d"
DESIGN_SHA256_EXPECTED = "a33b475dedbc66eb2d97e490389f3623f2fea29f6b7a98e6ceefb9536d277fd1"

# Per-(k, carrier) sufficient statistics carry two features:
#   id 0: C     = max(F)/k     (primary family-adjusted concentration)
#   id 1: C_alt = max(F_alt)/k (alternate diagnostic partition)
NF = 2
MODELS = {"M0fam": (), "M1fam": (0,), "PM1fam": (1,)}
SCORES = ("domain", "equal")


# ---------------------------------------------------------------------------
# Verification A: independent W1 generator (frozen formulas, same draw order)
# ---------------------------------------------------------------------------
def union_reach(homes, home_value, other_value):
    complements = [1.0] * FAMILIES
    for home in homes:
        for family in range(FAMILIES):
            complements[family] *= 1.0 - (home_value if family == home else other_value)
    return [1.0 - value for value in complements]


def make_w1_case(rng):
    """Frozen W1 recipe, implemented from the frozen design text.

    Draw order per case: defects = randint(1, 4); one randrange(6) per defect;
    30 rng.random() diagnostic bits (family-major, 5 probes per family) compared
    against the defect-union reach q_j = 1 - prod_m (1 - r_mj); then six
    binomialvariate(N_j, q^E_j) evaluation draws in family order.
    """
    defects = rng.randint(1, 4)
    homes = [rng.randrange(FAMILIES) for _ in range(defects)]
    qd = union_reach(homes, W1_DIAG_HOME, W1_DIAG_OTHER)
    qe = union_reach(homes, W1_EVAL_HOME, W1_EVAL_OTHER)
    bits = []
    for family in range(FAMILIES):
        prob = qd[family]
        for _ in range(DIAG_PER_FAMILY):
            bits.append(1 if rng.random() < prob else 0)
    f = [sum(bits[family * DIAG_PER_FAMILY:(family + 1) * DIAG_PER_FAMILY]) for family in range(FAMILIES)]
    e = [rng.binomialvariate(EVAL_SIZES[family], qe[family]) for family in range(FAMILIES)]
    k = sum(f)
    c = max(f) / k if k else None
    f_alt = [sum(bits[lo:hi]) for lo, hi in ALT_GROUP_SLICES]
    c_alt = max(f_alt) / k if k else None
    s_domain = 1.0 - sum(e) / N_EVAL
    s_equal = 1.0 - sum(e[family] / EVAL_SIZES[family] for family in range(FAMILIES)) / FAMILIES
    home_counts = [sum(1 for home in homes if home == family) for family in range(FAMILIES)]
    return {
        "F": f,
        "E": e,
        "F_alt": f_alt,
        "k": k,
        "C": c,
        "C_alt": c_alt,
        "carrier": homes[0],
        "home_counts": home_counts,
        "defects": defects,
        "S_domain": s_domain,
        "S_equal": s_equal,
        "diag_bits": "".join(str(bit) for bit in bits),
    }


FLOAT_FIELDS = ("C", "C_alt", "S_domain", "S_equal")


def compare_case(mine, saved, near_counter):
    """Field-by-field semantic comparison against a saved original record.

    Returns (mismatches, ok): mismatches is a list of field details for fields
    that disagree. A float field equal to within 1e-12 relative (but not exactly)
    is counted in near_counter and is not a mismatch; integer/structural fields
    must be exactly equal.
    """
    fields = (
        ("trial", mine["trial"], saved["trial"]),
        ("case", mine["case"], saved["case"]),
        ("fold", mine["fold"], saved["fold"]),
        ("setting", "W1", saved["setting"]),
        ("world", "W1", saved["world"]),
        ("F", mine["F"], saved["F"]),
        ("E", mine["E"], saved["E"]),
        ("F_alt", mine["F_alt"], saved["F_alt"]),
        ("k", mine["k"], saved["k"]),
        ("C", mine["C"], saved["C"]),
        ("C_alt", mine["C_alt"], saved["C_alt"]),
        ("carrier", mine["carrier"], saved["carrier"]),
        ("home_counts", mine["home_counts"], saved["home_counts"]),
        ("defects", mine["defects"], saved["defects"]),
        ("S_domain", mine["S_domain"], saved["S_domain"]),
        ("S_equal", mine["S_equal"], saved["S_equal"]),
        ("diag_bits", mine["diag_bits"], saved["diag_bits"]),
    )
    mismatches = []
    for name, mine_value, saved_value in fields:
        if mine_value == saved_value:
            continue
        if name in FLOAT_FIELDS and mine_value is not None and saved_value is not None:
            diff = abs(mine_value - saved_value)
            scale = max(abs(mine_value), abs(saved_value), 1e-30)
            if diff <= 1e-12 * scale:
                near_counter[0] += 1
                continue
        mismatches.append(
            {"field": name, "independent": repr(mine_value), "saved": repr(saved_value)}
        )
    return mismatches, not mismatches


# ---------------------------------------------------------------------------
# Verification B: independent OLS machinery (own linear algebra, stdlib only)
# ---------------------------------------------------------------------------
def empty_cell():
    return [
        0,                                  # n
        [0.0] * NF,                         # sum x per feature
        [[0.0] * NF for _ in range(NF)],    # sum x_i * x_j (i <= j filled)
        0.0,                                # sum y_domain
        0.0,                                # sum y_equal
        [0.0] * NF,                         # sum x * y_domain
        [0.0] * NF,                         # sum x * y_equal
    ]


def cell_add(cell, xs, y_domain, y_equal):
    cell[0] += 1
    sx = cell[1]
    for i in range(NF):
        sx[i] += xs[i]
    sxx = cell[2]
    for i in range(NF):
        xi = xs[i]
        row = sxx[i]
        for j in range(i, NF):
            row[j] += xi * xs[j]
    cell[3] += y_domain
    cell[4] += y_equal
    for idx, y in ((5, y_domain), (6, y_equal)):
        sxy = cell[idx]
        for i in range(NF):
            sxy[i] += xs[i] * y
    return cell


def merge_cells(dst, src):
    for key, cell in src.items():
        target = dst.get(key)
        if target is None:
            dst[key] = [
                cell[0],
                list(cell[1]),
                [row[:] for row in cell[2]],
                cell[3],
                cell[4],
                list(cell[5]),
                list(cell[6]),
            ]
            continue
        target[0] += cell[0]
        t_sx = target[1]
        s_sx = cell[1]
        for i in range(NF):
            t_sx[i] += s_sx[i]
        t_xx = target[2]
        s_xx = cell[2]
        for i in range(NF):
            t_row = t_xx[i]
            s_row = s_xx[i]
            for j in range(NF):
                t_row[j] += s_row[j]
        target[3] += cell[3]
        target[4] += cell[4]
        for idx in (5, 6):
            t_v = target[idx]
            s_v = cell[idx]
            for i in range(NF):
                t_v[i] += s_v[i]
    return dst


def sym_add(matrix, i, j, value):
    matrix[i][j] += value
    if i != j:
        matrix[j][i] += value


def cholesky_solve(matrix, rhs):
    """Own Cholesky factorisation + forward/back substitution. Returns None when
    a non-positive pivot is encountered; the caller then uses the Moore-Penrose
    pseudoinverse."""
    size = len(rhs)
    lower = [[0.0] * size for _ in range(size)]
    scale = max(1.0, max(abs(matrix[i][i]) for i in range(size)))
    tolerance = 1e-12 * scale
    for i in range(size):
        for j in range(i + 1):
            value = matrix[i][j]
            for t in range(j):
                value -= lower[i][t] * lower[j][t]
            if i == j:
                if not value > tolerance:
                    return None
                lower[i][j] = math.sqrt(value)
            else:
                lower[i][j] = value / lower[j][j]
    intermediate = [0.0] * size
    for i in range(size):
        acc = rhs[i]
        row_i = lower[i]
        for t in range(i):
            acc -= row_i[t] * intermediate[t]
        intermediate[i] = acc / row_i[i]
    beta = [0.0] * size
    for i in range(size - 1, -1, -1):
        acc = intermediate[i]
        for t in range(i + 1, size):
            acc -= lower[t][i] * beta[t]
        beta[i] = acc / lower[i][i]
    return beta


def jacobi_eigen(matrix):
    """Own cyclic Jacobi eigenvalue algorithm for a symmetric matrix."""
    size = len(matrix)
    a = [row[:] for row in matrix]
    v = [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]
    if size == 1:
        return [a[0][0]], v
    scale = max(1.0, max(abs(a[i][i]) for i in range(size)))
    tolerance = 1e-14 * scale
    for _sweep in range(40):
        changed = False
        for p in range(size - 1):
            for q in range(p + 1, size):
                apq = a[p][q]
                if abs(apq) <= tolerance:
                    continue
                changed = True
                theta = 0.5 * math.atan2(2.0 * apq, a[q][q] - a[p][p])
                cosine = math.cos(theta)
                sine = math.sin(theta)
                for idx in range(size):
                    apk = a[p][idx]
                    aqk = a[q][idx]
                    a[p][idx] = cosine * apk - sine * aqk
                    a[q][idx] = sine * apk + cosine * aqk
                for idx in range(size):
                    akp = a[idx][p]
                    akq = a[idx][q]
                    a[idx][p] = cosine * akp - sine * akq
                    a[idx][q] = sine * akp + cosine * akq
                for idx in range(size):
                    vkp = v[idx][p]
                    vkq = v[idx][q]
                    v[idx][p] = cosine * vkp - sine * vkq
                    v[idx][q] = sine * vkp + cosine * vkq
        if not changed:
            break
    return [a[i][i] for i in range(size)], v


def moore_penrose_solve(matrix, rhs):
    """Moore-Penrose least-squares solution via the own Jacobi decomposition.
    Eigenvalues not above max(1e-12, largest * 1e-10) are treated as zero."""
    eigenvalues, eigenvectors = jacobi_eigen(matrix)
    largest = max((abs(value) for value in eigenvalues), default=0.0)
    if largest == 0.0:
        return [0.0] * len(rhs), 0
    tol = max(1e-12, largest * 1e-10)
    size = len(rhs)
    beta = [0.0] * size
    rank = 0
    for index, eig in enumerate(eigenvalues):
        if eig <= tol:
            continue
        rank += 1
        coeff = sum(eigenvectors[row][index] * rhs[row] for row in range(size)) / eig
        for row in range(size):
            beta[row] += coeff * eigenvectors[row][index]
    return beta, rank


def fit_fold(train_cells, categories, features):
    """Ordinary least squares for one training fold.

    Design columns: intercept; one dummy per k in categories[1:] (reference
    category = smallest eligible k observed in the trial; k is never a single
    numeric term); five anchor-family indicators (family 6 omitted); then the
    requested feature columns.

    Rank deficiency handling (recorded, folds never discarded or altered):
    columns whose X'X diagonal is not above tol = 1e-12 * max(1.0, max diagonal
    over this model's columns) are dropped -- this is exactly the k levels absent
    from the training data. The reduced system is solved by own Cholesky when
    positive definite, otherwise by own Moore-Penrose; the same active column set
    is used for both scores.
    """
    n_cats = len(categories)
    n_fam_cols = FAMILIES - 1
    n_feature_cols = len(features)
    p = n_cats + n_fam_cols + n_feature_cols
    matrix = [[0.0] * p for _ in range(p)]
    rhs_domain = [0.0] * p
    rhs_equal = [0.0] * p
    dummy_col = {k: 1 + idx for idx, k in enumerate(categories[1:])}
    fam_base = n_cats
    x_base = n_cats + n_fam_cols
    for (k, carrier), cell in train_cells.items():
        n = cell[0]
        sx = cell[1]
        sxx = cell[2]
        sy_domain = cell[3]
        sy_equal = cell[4]
        sxy_domain = cell[5]
        sxy_equal = cell[6]
        matrix[0][0] += n
        rhs_domain[0] += sy_domain
        rhs_equal[0] += sy_equal
        dummy = dummy_col.get(k)
        fam_col = fam_base + carrier if carrier < n_fam_cols else None
        if dummy is not None:
            sym_add(matrix, 0, dummy, n)
            matrix[dummy][dummy] += n
            rhs_domain[dummy] += sy_domain
            rhs_equal[dummy] += sy_equal
            if fam_col is not None:
                sym_add(matrix, dummy, fam_col, n)
        if fam_col is not None:
            sym_add(matrix, 0, fam_col, n)
            matrix[fam_col][fam_col] += n
            rhs_domain[fam_col] += sy_domain
            rhs_equal[fam_col] += sy_equal
        for a, feature_a in enumerate(features):
            col_a = x_base + a
            sxa = sx[feature_a]
            sym_add(matrix, 0, col_a, sxa)
            if dummy is not None:
                sym_add(matrix, dummy, col_a, sxa)
            if fam_col is not None:
                sym_add(matrix, fam_col, col_a, sxa)
            matrix[col_a][col_a] += sxx[feature_a][feature_a]
            rhs_domain[col_a] += sxy_domain[feature_a]
            rhs_equal[col_a] += sxy_equal[feature_a]
            for b in range(a + 1, n_feature_cols):
                col_b = x_base + b
                sym_add(matrix, col_a, col_b, sxx[feature_a][features[b]])
    scale = max(1.0, max(matrix[i][i] for i in range(p)))
    tol = 1e-12 * scale
    active = [i for i in range(p) if matrix[i][i] > tol]
    deficient = len(active) < p
    beta_domain = [0.0] * p
    beta_equal = [0.0] * p
    rank = 0
    if active:
        sub = [[matrix[i][j] for j in active] for i in active]
        solved_domain = cholesky_solve(sub, [rhs_domain[i] for i in active])
        if solved_domain is not None:
            solved_equal = cholesky_solve(sub, [rhs_equal[i] for i in active])
            if solved_equal is None:
                raise RuntimeError("inconsistent solver state between scores")
            rank = len(active)
            for pos, col in enumerate(active):
                beta_domain[col] = solved_domain[pos]
                beta_equal[col] = solved_equal[pos]
        else:
            solved_domain, rank_domain = moore_penrose_solve(sub, [rhs_domain[i] for i in active])
            solved_equal, rank_equal = moore_penrose_solve(sub, [rhs_equal[i] for i in active])
            rank = min(rank_domain, rank_equal)
            if rank < len(active):
                deficient = True
            for pos, col in enumerate(active):
                beta_domain[col] = solved_domain[pos]
                beta_equal[col] = solved_equal[pos]
    return {
        "beta_domain": beta_domain,
        "beta_equal": beta_equal,
        "deficient": deficient,
        "rank": rank,
        "n_active": len(active),
    }


def build_bases(beta, dummy_col, fam_base, cell_keys):
    """Per-(k, carrier) base predictions for one fitted model and one score:
    intercept + active k dummy + anchor-family indicator part (feature part
    excluded; feature predictions are added per case). A k dummy dropped for rank
    deficiency contributes 0 because its beta entry is left at 0."""
    bases = {}
    for (k, carrier) in cell_keys:
        value = beta[0]
        dummy_index = dummy_col.get(k)
        if dummy_index is not None:
            value += beta[dummy_index]
        if carrier < FAMILIES - 1:
            value += beta[fam_base + carrier]
        bases[(k, carrier)] = value
    return bases


def quantile(values, q):
    """Frozen interval convention: percentiles of the 500 trial-level estimates
    with linear interpolation between adjacent order statistics."""
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def interval(values):
    n = len(values)
    return {
        "mean": sum(values) / n,
        "low": quantile(values, 0.025),
        "high": quantile(values, 0.975),
        "positive_fraction": sum(1 for value in values if value > 0) / n,
        "trials": n,
        "positive_trials": sum(1 for value in values if value > 0),
    }


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_lf_normalized(path):
    data = path.read_bytes()
    normalized = data.replace(b"\r\n", b"\n")
    return len(normalized), hashlib.sha256(normalized).hexdigest()


# ---------------------------------------------------------------------------
# Reference values (work order and preserved original records)
# ---------------------------------------------------------------------------
REFERENCE = {
    "primary_delta_pred_domain_mean": 1.961346752e-06,
    "primary_delta_pred_domain_low": -1.242089975e-06,
    "primary_delta_pred_domain_high": 7.581285807e-06,
    "primary_delta_pred_domain_positive_fraction": 0.804,
    "primary_delta_pred_equal_mean": 1.914362824e-06,
    "primary_delta_pred_equal_low": -1.833270363e-06,
    "primary_delta_pred_equal_high": 8.988738209e-06,
    "primary_delta_pred_equal_positive_fraction": 0.754,
    "eligible_cases": 2499949,
    "baseline_m0fam_domain_mean": 0.003387840,
    "baseline_m0fam_equal_mean": 0.003350860,
    "represented_delta_pred_domain_mean": 1.036293050e-06,
    "represented_delta_pred_domain_low": -1.660447426e-06,
    "represented_delta_pred_domain_high": 5.298823179e-06,
    "represented_delta_pred_domain_positive_fraction": 0.716,
    "represented_delta_pred_equal_mean": 9.790599446e-07,
    "represented_delta_pred_equal_low": -1.851879484e-06,
    "represented_delta_pred_equal_high": 6.079745018e-06,
    "represented_delta_pred_equal_positive_fraction": 0.642,
    "represented_cases": 2499386,
    "represented_baseline_m0fam_domain_mean": 0.003378998,
    "represented_baseline_m0fam_equal_mean": 0.003341825,
    "partition_delta_pred_domain_mean_approx": -6.2470e-07,
    "partition_delta_pred_equal_mean_approx": -6.7787e-07,
    "partition_delta_pred_domain_low_approx": -3.4517e-06,
    "partition_delta_pred_domain_high_approx": 3.1384e-06,
    "partition_delta_pred_equal_low_approx": -3.8943e-06,
    "partition_delta_pred_equal_high_approx": 2.6534e-06,
    "folds_with_unseen_k": 438,
    "unseen_k_instances": 481,
    "affected_eligible_cases": 563,
    "unseen_k_global_levels": [1, 23, 24, 25, 26, 27, 28],
    "affected_cases_by_k": {"1": 183, "23": 26, "24": 218, "25": 114, "26": 18, "27": 3, "28": 1},
    "full_baseline_scored_cases": 2499388,
    "full_baseline_omitted_cases": 612,
    "full_baseline_omitted_k0": 49,
}

TOL_DELTA = 1e-9
TOL_BASELINE = 1e-7
TOL_FRACTION = 0.002


def main(argv=None):
    parser = argparse.ArgumentParser(description="GLM independent W1 verification")
    parser.add_argument("--trials", type=int, default=TRIALS)
    args = parser.parse_args(argv)
    trials = args.trials
    full_run = trials == TRIALS

    run_started = datetime.now(timezone.utc).isoformat()
    clock_start = time.perf_counter()

    source_path = Path(__file__).resolve()
    source_bytes = source_path.stat().st_size
    source_sha = sha256_file(source_path)
    print(
        f"independent source: {source_path.name} bytes={source_bytes} sha256={source_sha}",
        file=sys.stderr,
        flush=True,
    )

    design_lf_length, design_lf_sha = sha256_lf_normalized(DESIGN_PATH)
    raw_w1_sha = sha256_file(RAW_W1_PATH)
    per_trial_sha = sha256_file(PER_TRIAL_PATH)
    review_sha = sha256_file(REVIEW_METRICS_PATH)
    if raw_w1_sha != W1_RAW_SHA256_EXPECTED:
        raise RuntimeError(f"W1 raw archive hash mismatch: {raw_w1_sha}")
    if per_trial_sha != PER_TRIAL_SHA256_EXPECTED:
        raise RuntimeError(f"per_trial.json hash mismatch: {per_trial_sha}")

    verification_a = {
        "records_checked": 0,
        "records_matched_strictly": 0,
        "records_with_mismatched_fields": 0,
        "field_mismatch_counts": {},
        "float_fields_matched_within_1e12_relative_only": 0,
        "first_mismatch": None,
        "trailing_records_after_expected": 0,
        "expected_records": trials * CASES,
        "archive_sha256": raw_w1_sha,
    }
    first_mismatch = None
    near_counter = [0]

    per_trial_rows = []
    max_abs_error = {
        "delta_pred_domain": 0.0,
        "delta_pred_equal": 0.0,
        "l_m0fam_domain": 0.0,
        "l_m0fam_equal": 0.0,
        "l_m1fam_domain": 0.0,
        "l_m1fam_equal": 0.0,
        "partition_delta_domain": 0.0,
        "partition_delta_equal": 0.0,
        "partition_m1fam_domain": 0.0,
        "partition_m1fam_equal": 0.0,
        "represented_delta_domain": 0.0,
        "represented_delta_equal": 0.0,
    }

    per_trial_original = None
    review_represented = None
    if full_run:
        per_trial_original = {
            int(record["trial"]): record
            for record in json.loads(PER_TRIAL_PATH.read_text(encoding="utf-8"))
            if record["setting"] == "W1"
        }
        with REVIEW_METRICS_PATH.open(encoding="utf-8") as handle:
            review = json.load(handle)
        review_represented = {
            int(entry["trial"]): entry for entry in review["settings"]["W1"]["sensitivity"]["trials"]
        }

    deficient_fold_counts = {name: 0 for name in MODELS}
    unseen_fold_fits = 0
    unseen_affected_cases = 0
    unseen_k_instances = 0
    unseen_levels = set()
    unseen_cases_by_k = {}
    eligible_total = 0
    k0_total = 0
    represented_total = 0
    omitted_total = 0
    omitted_trials_with_cases = 0
    full_scored_total = 0
    full_omitted_total = 0
    full_omitted_k0_total = 0

    with gzip.open(RAW_W1_PATH, "rt", encoding="utf-8") as handle:
        for trial in range(trials):
            trial_seed = BASE_SEED + trial
            rng = random.Random(trial_seed)
            fold_rng = random.Random(trial_seed + FOLD_SEED_OFFSET)
            fold_cells = [dict() for _ in range(FOLDS)]
            fold_eligible = [[] for _ in range(FOLDS)]
            fold_all_cases = [[] for _ in range(FOLDS)]
            fold_k_counts = [dict() for _ in range(FOLDS)]
            elig_count = 0
            k0_count = 0

            for case_index in range(CASES):
                fold = fold_rng.randrange(FOLDS)
                mine = make_w1_case(rng)
                saved_line = handle.readline()
                if not saved_line:
                    raise RuntimeError(f"original archive ended at trial {trial} case {case_index}")
                saved = json.loads(saved_line)
                mine["trial"] = trial
                mine["case"] = case_index
                mine["fold"] = fold
                mismatches, ok = compare_case(mine, saved, near_counter)
                verification_a["records_checked"] += 1
                if ok:
                    verification_a["records_matched_strictly"] += 1
                else:
                    verification_a["records_with_mismatched_fields"] += 1
                    counts = verification_a["field_mismatch_counts"]
                    for detail in mismatches:
                        field = detail["field"]
                        counts[field] = counts.get(field, 0) + 1
                    if first_mismatch is None:
                        first_mismatch = {"trial": trial, "case": case_index, "details": mismatches}

                # Verification B reads only the saved record's values.
                k = saved["k"]
                carrier = saved["carrier"]
                y_domain = saved["S_domain"]
                y_equal = saved["S_equal"]
                fold_all_cases[fold].append((k, y_domain, y_equal))
                if k == 0:
                    k0_count += 1
                    continue
                elig_count += 1
                counts_by_k = fold_k_counts[fold]
                counts_by_k[k] = counts_by_k.get(k, 0) + 1
                xs = (float(saved["C"]), float(saved["C_alt"]))
                fold_eligible[fold].append((k, carrier, y_domain, y_equal, xs))
                cell_key = (k, carrier)
                cell = fold_cells[fold].get(cell_key)
                if cell is None:
                    cell = empty_cell()
                    fold_cells[fold][cell_key] = cell
                cell_add(cell, xs, y_domain, y_equal)

            if full_run and trial == trials - 1:
                extra = handle.readline()
                while extra:
                    verification_a["trailing_records_after_expected"] += 1
                    extra = handle.readline()

            categories = sorted({key[0] for fold_map in fold_cells for key in fold_map})
            train_ks = []
            for fold in range(FOLDS):
                union_k = set()
                for other in range(FOLDS):
                    if other != fold:
                        union_k.update(key[0] for key in fold_cells[other])
                train_ks.append(union_k)

            sse = {name: {score: 0.0 for score in SCORES} for name in MODELS}
            sse_represented = {
                name: {score: 0.0 for score in SCORES} for name in ("M0fam", "M1fam")
            }
            count_represented = 0
            count_omitted = 0
            trial_deficient = {name: 0 for name in MODELS}
            trial_unseen_folds = 0
            trial_unseen_affected = 0
            trial_unseen_instances = 0

            for fold in range(FOLDS):
                train_cells = {}
                for other in range(FOLDS):
                    if other != fold:
                        merge_cells(train_cells, fold_cells[other])
                fits = {
                    name: fit_fold(train_cells, categories, features)
                    for name, features in MODELS.items()
                }
                for name in MODELS:
                    if fits[name]["deficient"]:
                        trial_deficient[name] += 1
                        deficient_fold_counts[name] += 1
                unseen = sorted(set(fold_k_counts[fold]) - train_ks[fold])
                if unseen:
                    trial_unseen_folds += 1
                    unseen_fold_fits += 1
                    trial_unseen_instances += len(unseen)
                    unseen_k_instances += len(unseen)
                    for k in unseen:
                        affected = fold_k_counts[fold][k]
                        trial_unseen_affected += affected
                        unseen_affected_cases += affected
                        unseen_cases_by_k[k] = unseen_cases_by_k.get(k, 0) + affected
                        unseen_levels.add(k)

                dummy_col = {k: 1 + idx for idx, k in enumerate(categories[1:])}
                fam_base = len(categories)
                x_base = len(categories) + FAMILIES - 1
                test_keys = fold_cells[fold].keys()
                bases = {
                    (name, score): build_bases(fits[name]["beta_" + score], dummy_col, fam_base, test_keys)
                    for name in MODELS
                    for score in SCORES
                }
                gamma = {
                    (name, score): fits[name]["beta_" + score][x_base]
                    for name in ("M1fam", "PM1fam")
                    for score in SCORES
                }

                for (k, carrier, y_domain, y_equal, xs) in fold_eligible[fold]:
                    c_value, c_alt_value = xs
                    represented = k in train_ks[fold]
                    for score in ("domain", "equal"):
                        y = y_domain if score == "domain" else y_equal
                        base0 = bases[("M0fam", score)][(k, carrier)]
                        base1 = bases[("M1fam", score)][(k, carrier)]
                        basep = bases[("PM1fam", score)][(k, carrier)]

                        residual = y - base0
                        sse["M0fam"][score] += residual * residual
                        residual = y - (base1 + gamma[("M1fam", score)] * c_value)
                        sse["M1fam"][score] += residual * residual
                        residual = y - (basep + gamma[("PM1fam", score)] * c_alt_value)
                        sse["PM1fam"][score] += residual * residual

                        if represented:
                            residual = y - base0
                            sse_represented["M0fam"][score] += residual * residual
                            residual = y - (base1 + gamma[("M1fam", score)] * c_value)
                            sse_represented["M1fam"][score] += residual * residual

                    if represented:
                        count_represented += 1
                    else:
                        count_omitted += 1

            eligible_total += elig_count
            k0_total += k0_count
            represented_total += count_represented
            omitted_total += count_omitted
            if count_omitted:
                omitted_trials_with_cases += 1

            for fold in range(FOLDS):
                train_full_k = set()
                for other in range(FOLDS):
                    if other != fold:
                        train_full_k.update(k for (k, _yd, _ye) in fold_all_cases[other])
                for (k, _yd, _ye) in fold_all_cases[fold]:
                    if k in train_full_k:
                        full_scored_total += 1
                    else:
                        full_omitted_total += 1
                        if k == 0:
                            full_omitted_k0_total += 1

            delta_primary = {
                score: (sse["M0fam"][score] - sse["M1fam"][score]) / elig_count for score in SCORES
            }
            delta_partition = {
                score: (sse["M0fam"][score] - sse["PM1fam"][score]) / elig_count for score in SCORES
            }
            represented_delta = {
                score: (sse_represented["M0fam"][score] - sse_represented["M1fam"][score]) / count_represented
                for score in SCORES
            }
            per_trial_rows.append(
                {
                    "trial": trial,
                    "delta_pred_domain": delta_primary["domain"],
                    "delta_pred_equal": delta_primary["equal"],
                    "l_m0fam_domain": sse["M0fam"]["domain"] / elig_count,
                    "l_m0fam_equal": sse["M0fam"]["equal"] / elig_count,
                    "l_m1fam_domain": sse["M1fam"]["domain"] / elig_count,
                    "l_m1fam_equal": sse["M1fam"]["equal"] / elig_count,
                    "l_pm1fam_domain": sse["PM1fam"]["domain"] / elig_count,
                    "l_pm1fam_equal": sse["PM1fam"]["equal"] / elig_count,
                    "partition_delta_domain": delta_partition["domain"],
                    "partition_delta_equal": delta_partition["equal"],
                    "represented_delta_domain": represented_delta["domain"],
                    "represented_delta_equal": represented_delta["equal"],
                    "represented_l0fam_domain": sse_represented["M0fam"]["domain"] / count_represented,
                    "represented_l0fam_equal": sse_represented["M0fam"]["equal"] / count_represented,
                    "n_eligible": elig_count,
                    "n_represented": count_represented,
                    "n_k0": k0_count,
                    "deficient_folds": trial_deficient,
                    "unseen_folds": trial_unseen_folds,
                    "unseen_affected_cases": trial_unseen_affected,
                    "unseen_instances": trial_unseen_instances,
                }
            )

            if per_trial_original is not None:
                expected = per_trial_original[trial]

                def update(key, mine_value, original_value):
                    max_abs_error[key] = max(
                        max_abs_error[key], abs(mine_value - float(original_value))
                    )

                update("delta_pred_domain", delta_primary["domain"], expected["delta_pred"]["domain"])
                update("delta_pred_equal", delta_primary["equal"], expected["delta_pred"]["equal"])
                update("l_m0fam_domain", per_trial_rows[-1]["l_m0fam_domain"], expected["losses"]["domain"]["M0fam"])
                update("l_m0fam_equal", per_trial_rows[-1]["l_m0fam_equal"], expected["losses"]["equal"]["M0fam"])
                update("l_m1fam_domain", per_trial_rows[-1]["l_m1fam_domain"], expected["losses"]["domain"]["M1fam"])
                update("l_m1fam_equal", per_trial_rows[-1]["l_m1fam_equal"], expected["losses"]["equal"]["M1fam"])
                update("partition_delta_domain", delta_partition["domain"], expected["partition"]["domain"]["delta_pred"])
                update("partition_delta_equal", delta_partition["equal"], expected["partition"]["equal"]["delta_pred"])
                update("partition_m1fam_domain", per_trial_rows[-1]["l_pm1fam_domain"], expected["partition"]["domain"]["M1fam"])
                update("partition_m1fam_equal", per_trial_rows[-1]["l_pm1fam_equal"], expected["partition"]["equal"]["M1fam"])
            if review_represented is not None:
                expected = review_represented[trial]

                def update(key, mine_value, original_value):
                    max_abs_error[key] = max(
                        max_abs_error[key], abs(mine_value - float(original_value))
                    )

                update("represented_delta_domain", represented_delta["domain"], expected["represented"]["domain"]["delta"])
                update("represented_delta_equal", represented_delta["equal"], expected["represented"]["equal"]["delta"])

            if trial % 25 == 0 or trial == trials - 1:
                elapsed = time.perf_counter() - clock_start
                print(f"trial {trial + 1}/{trials} elapsed {elapsed:.1f}s", file=sys.stderr, flush=True)

    verification_a["float_fields_matched_within_1e12_relative_only"] = near_counter[0]
    if first_mismatch is not None:
        verification_a["first_mismatch"] = first_mismatch
    verification_a["all_records_matched_strictly"] = (
        verification_a["records_checked"] > 0
        and verification_a["records_with_mismatched_fields"] == 0
        and verification_a["trailing_records_after_expected"] == 0
        and verification_a["records_matched_strictly"] == verification_a["expected_records"]
    )

    primary_domain = interval([row["delta_pred_domain"] for row in per_trial_rows])
    primary_equal = interval([row["delta_pred_equal"] for row in per_trial_rows])
    represented_domain = interval([row["represented_delta_domain"] for row in per_trial_rows])
    represented_equal = interval([row["represented_delta_equal"] for row in per_trial_rows])
    partition_domain = interval([row["partition_delta_domain"] for row in per_trial_rows])
    partition_equal = interval([row["partition_delta_equal"] for row in per_trial_rows])
    baseline_m0_domain = sum(row["l_m0fam_domain"] for row in per_trial_rows) / trials
    baseline_m0_equal = sum(row["l_m0fam_equal"] for row in per_trial_rows) / trials
    represented_baseline_domain = sum(row["represented_l0fam_domain"] for row in per_trial_rows) / trials
    represented_baseline_equal = sum(row["represented_l0fam_equal"] for row in per_trial_rows) / trials
    m1_domain_mean = sum(row["l_m1fam_domain"] for row in per_trial_rows) / trials
    m1_equal_mean = sum(row["l_m1fam_equal"] for row in per_trial_rows) / trials
    pm1_domain_mean = sum(row["l_pm1fam_domain"] for row in per_trial_rows) / trials
    pm1_equal_mean = sum(row["l_pm1fam_equal"] for row in per_trial_rows) / trials

    comparison_rows = []

    def add_row(label, kind, reference, independent, tolerance):
        if not full_run or reference is None:
            status = "NOT COMPARED (partial run)" if not full_run else "REFERENCE MISSING"
            diff = None
        elif kind == "count":
            diff = int(independent) - int(reference)
            status = "MATCH" if diff == 0 else "MISMATCH"
        elif kind == "levels":
            diff = None
            status = "MATCH" if list(reference) == list(independent) else "MISMATCH"
        else:
            diff = independent - reference
            status = "MATCH" if abs(diff) <= tolerance else "MISMATCH"
        comparison_rows.append(
            {
                "metric": label,
                "reference": reference,
                "independent": independent,
                "difference": diff,
                "tolerance": tolerance,
                "status": status,
            }
        )

    add_row("Primary mean Delta_pred (domain)", "number", REFERENCE["primary_delta_pred_domain_mean"], primary_domain["mean"], TOL_DELTA)
    add_row("Primary central 95% interval low (domain)", "number", REFERENCE["primary_delta_pred_domain_low"], primary_domain["low"], TOL_DELTA)
    add_row("Primary central 95% interval high (domain)", "number", REFERENCE["primary_delta_pred_domain_high"], primary_domain["high"], TOL_DELTA)
    add_row("Primary positive-trial fraction (domain)", "fraction", REFERENCE["primary_delta_pred_domain_positive_fraction"], primary_domain["positive_fraction"], TOL_FRACTION)
    add_row("Primary mean Delta_pred (equal)", "number", REFERENCE["primary_delta_pred_equal_mean"], primary_equal["mean"], TOL_DELTA)
    add_row("Primary central 95% interval low (equal)", "number", REFERENCE["primary_delta_pred_equal_low"], primary_equal["low"], TOL_DELTA)
    add_row("Primary central 95% interval high (equal)", "number", REFERENCE["primary_delta_pred_equal_high"], primary_equal["high"], TOL_DELTA)
    add_row("Primary positive-trial fraction (equal)", "fraction", REFERENCE["primary_delta_pred_equal_positive_fraction"], primary_equal["positive_fraction"], TOL_FRACTION)
    add_row("Eligible cases (k>0)", "count", REFERENCE["eligible_cases"], eligible_total, 0)
    add_row("Mean L(M0+fam) domain baseline", "number", REFERENCE["baseline_m0fam_domain_mean"], baseline_m0_domain, TOL_BASELINE)
    add_row("Mean L(M0+fam) equal baseline", "number", REFERENCE["baseline_m0fam_equal_mean"], baseline_m0_equal, TOL_BASELINE)
    add_row("Represented-k mean Delta_pred (domain)", "number", REFERENCE["represented_delta_pred_domain_mean"], represented_domain["mean"], TOL_DELTA)
    add_row("Represented-k 95% interval low (domain)", "number", REFERENCE["represented_delta_pred_domain_low"], represented_domain["low"], TOL_DELTA)
    add_row("Represented-k 95% interval high (domain)", "number", REFERENCE["represented_delta_pred_domain_high"], represented_domain["high"], TOL_DELTA)
    add_row("Represented-k positive-trial fraction (domain)", "fraction", REFERENCE["represented_delta_pred_domain_positive_fraction"], represented_domain["positive_fraction"], TOL_FRACTION)
    add_row("Represented-k mean Delta_pred (equal)", "number", REFERENCE["represented_delta_pred_equal_mean"], represented_equal["mean"], TOL_DELTA)
    add_row("Represented-k 95% interval low (equal)", "number", REFERENCE["represented_delta_pred_equal_low"], represented_equal["low"], TOL_DELTA)
    add_row("Represented-k 95% interval high (equal)", "number", REFERENCE["represented_delta_pred_equal_high"], represented_equal["high"], TOL_DELTA)
    add_row("Represented-k positive-trial fraction (equal)", "fraction", REFERENCE["represented_delta_pred_equal_positive_fraction"], represented_equal["positive_fraction"], TOL_FRACTION)
    add_row("Represented-k eligible cases", "count", REFERENCE["represented_cases"], represented_total, 0)
    add_row("Represented-k mean L(M0+fam) domain", "number", REFERENCE["represented_baseline_m0fam_domain_mean"], represented_baseline_domain, TOL_BASELINE)
    add_row("Represented-k mean L(M0+fam) equal", "number", REFERENCE["represented_baseline_m0fam_equal_mean"], represented_baseline_equal, TOL_BASELINE)
    add_row("Alternate-partition mean Delta (domain)", "number", REFERENCE["partition_delta_pred_domain_mean_approx"], partition_domain["mean"], TOL_DELTA)
    add_row("Alternate-partition 95% low (domain)", "number", REFERENCE["partition_delta_pred_domain_low_approx"], partition_domain["low"], TOL_DELTA)
    add_row("Alternate-partition 95% high (domain)", "number", REFERENCE["partition_delta_pred_domain_high_approx"], partition_domain["high"], TOL_DELTA)
    add_row("Alternate-partition mean Delta (equal)", "number", REFERENCE["partition_delta_pred_equal_mean_approx"], partition_equal["mean"], TOL_DELTA)
    add_row("Alternate-partition 95% low (equal)", "number", REFERENCE["partition_delta_pred_equal_low_approx"], partition_equal["low"], TOL_DELTA)
    add_row("Alternate-partition 95% high (equal)", "number", REFERENCE["partition_delta_pred_equal_high_approx"], partition_equal["high"], TOL_DELTA)
    add_row("Fold fits with unseen k", "count", REFERENCE["folds_with_unseen_k"], unseen_fold_fits, 0)
    add_row("Unseen-k instances", "count", REFERENCE["unseen_k_instances"], unseen_k_instances, 0)
    add_row("Affected eligible cases (unseen k)", "count", REFERENCE["affected_eligible_cases"], unseen_affected_cases, 0)
    add_row("Unseen k levels", "levels", REFERENCE["unseen_k_global_levels"], sorted(unseen_levels), 0)
    add_row("Affected cases by k", "levels", REFERENCE["affected_cases_by_k"], {str(k): v for k, v in sorted(unseen_cases_by_k.items())}, 0)
    add_row("Full-baseline scored cases", "count", REFERENCE["full_baseline_scored_cases"], full_scored_total, 0)
    add_row("Full-baseline omitted cases", "count", REFERENCE["full_baseline_omitted_cases"], full_omitted_total, 0)
    add_row("Full-baseline omitted k=0 cases", "count", REFERENCE["full_baseline_omitted_k0"], full_omitted_k0_total, 0)

    elapsed_seconds = time.perf_counter() - clock_start
    mism_records = verification_a["records_with_mismatched_fields"]
    summary = {
        "task": "GLM independent W1 verification (single bounded verification)",
        "source_frozen": {
            "path": str(source_path),
            "bytes": source_bytes,
            "sha256": source_sha,
            "hash_recorded_before_first_execution": True,
        },
        "environment": {
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_executable": sys.executable,
            "platform": platform.platform(),
        },
        "runtime": {
            "started_utc": run_started,
            "ended_utc": datetime.now(timezone.utc).isoformat(),
            "seconds": elapsed_seconds,
            "trials": trials,
            "cases_per_trial": CASES,
            "base_seed": BASE_SEED,
            "trial_seed_rule": "trial_seed = 20261024 + trial_index, index starts at 0",
            "full_run": full_run,
        },
        "frozen_design_check": {
            "path": str(DESIGN_PATH),
            "sha256_lf_normalized_expected": DESIGN_SHA256_EXPECTED,
            "sha256_lf_normalized_observed": design_lf_sha,
            "lf_normalized_bytes": design_lf_length,
            "verified": design_lf_sha == DESIGN_SHA256_EXPECTED,
        },
        "inputs_used_read_only": {
            "w1_raw": {
                "path": str(RAW_W1_PATH),
                "sha256": raw_w1_sha,
                "matches_manifest": raw_w1_sha == W1_RAW_SHA256_EXPECTED,
            },
            "per_trial": {
                "path": str(PER_TRIAL_PATH),
                "sha256": per_trial_sha,
                "matches_manifest": per_trial_sha == PER_TRIAL_SHA256_EXPECTED,
            },
            "review_correction_metrics": {"path": str(REVIEW_METRICS_PATH), "sha256": review_sha},
        },
        "verification_a": verification_a,
        "verification_b": {
            "models_fit": {name: list(features) for name, features in MODELS.items()},
            "feature_map": {"feature_id_0": "C = max(F)/k", "feature_id_1": "C_alt = max(F_alt)/k"},
            "fitting_notes": (
                "Independent stdlib implementation. X'X assembled exactly per fold for the "
                "declared design: intercept + categorical k dummies (reference = smallest "
                "observed eligible k of the trial) + five anchor-family indicators (family 6 "
                "reference) + the model's feature. Rank deficiency: columns with a "
                "non-positive training diagonal (k levels absent from the training folds) are "
                "dropped and the fold flagged; the reduced system is solved by own Cholesky "
                "when positive definite, otherwise by own Moore-Penrose eigen solver. "
                "Held-out squared error is accumulated per test case; loss = SSE / eligible "
                "count aggregated over the five folds. The alternate-partition M0+fam design "
                "is identical to the primary M0+fam (same k categories and family coding), so "
                "the partition comparison reuses that fit with C_alt in place of C."
            ),
            "primary": {"domain": primary_domain, "equal": primary_equal},
            "primary_losses": {
                "m0fam_mean": {"domain": baseline_m0_domain, "equal": baseline_m0_equal},
                "m1fam_mean": {"domain": m1_domain_mean, "equal": m1_equal_mean},
                "gain_relative_to_baseline": {
                    "domain": primary_domain["mean"] / baseline_m0_domain,
                    "equal": primary_equal["mean"] / baseline_m0_equal,
                },
            },
            "alternate_partition": {
                "domain": partition_domain,
                "equal": partition_equal,
                "pm1fam_mean": {"domain": pm1_domain_mean, "equal": pm1_equal_mean},
            },
            "represented_k_sensitivity": {
                "domain": represented_domain,
                "equal": represented_equal,
                "represented_cases": represented_total,
                "m0fam_mean": {"domain": represented_baseline_domain, "equal": represented_baseline_equal},
            },
            "omitted_k_subset_descriptive": {
                "cases": omitted_total,
                "trials_with_cases": omitted_trials_with_cases,
            },
            "rank_and_unseen_diagnostics": {
                "deficient_fold_counts_by_model": deficient_fold_counts,
                "fold_fits_with_unseen_k": unseen_fold_fits,
                "unseen_k_instances": unseen_k_instances,
                "affected_eligible_cases": unseen_affected_cases,
                "unseen_k_global_levels": sorted(unseen_levels),
                "affected_cases_by_k": {str(k): v for k, v in sorted(unseen_cases_by_k.items())},
                "full_baseline_scored_cases": full_scored_total,
                "full_baseline_omitted_cases": full_omitted_total,
                "full_baseline_omitted_k0": full_omitted_k0_total,
            },
            "case_counts": {
                "eligible_total": eligible_total,
                "k0_total": k0_total,
                "total_cases": eligible_total + k0_total,
                "represented_total": represented_total,
                "omitted_total": omitted_total,
            },
            "per_trial": per_trial_rows,
            "per_trial_max_abs_error_vs_original": max_abs_error,
        },
        "reference_comparison": comparison_rows,
    }

    out_path = HERE / "independent_w1_run.json"
    out_path.write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)
    print(
        f"Verification A: checked={verification_a['records_checked']} "
        f"mismatch_records={mism_records} all_strict={verification_a['all_records_matched_strictly']}",
        file=sys.stderr,
    )
    print(f"Primary domain: {primary_domain}", file=sys.stderr)
    print(f"Primary equal : {primary_equal}", file=sys.stderr)
    print(
        f"Represented domain: {represented_domain}",
        file=sys.stderr,
    )
    print(
        f"Represented equal : {represented_equal}",
        file=sys.stderr,
    )
    print(f"Partition domain: {partition_domain}", file=sys.stderr)
    print(f"Partition equal : {partition_equal}", file=sys.stderr)
    status_count = sum(1 for row in comparison_rows if row["status"] == "MISMATCH")
    print(f"Reference comparison rows: {len(comparison_rows)} MISMATCH rows: {status_count}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
