# v0.2 Interpretability Audit — Determinism of C on the Eligible Support

**Date:** 2026-10-14
**Scope:** read-only interpretability audit of the completed v0.2 confirmatory result.
No frozen file was edited; no pipeline stage was re-executed; the decision rule,
threshold, model, and classification are untouched.
**Disposition:** v0.2 remains terminal **NEGATIVE** under the frozen decision rule
(as recorded in `v02/REPORT_V02.md`); this note narrows what that NEGATIVE means.

## 1. Provenance

GPT performed a read-only audit of the frozen v0.2 artifacts and raised two
findings: (F1) the concentration feature C is a deterministic function of the
failure count k on the eligible support, and (F2) the frozen spline basis aliases
C on the observed k-levels. CLAUDE reviewed the claims, required four direct
recomputations on the frozen files (§7, script in Appendix A), and required the
wording corrections recorded below (§5 caveats, §6 design note). The
recomputations in §7 were executed against the frozen repository state on
2026-10-14; GPT did not re-execute the confirmatory pipeline, and neither did
this audit.

## 2. Finding F1 — C is deterministic on the eligible support (verified 90/90)

The pilot's persisted eligible observations (`v02/pilot_v02/pilot_v02_report.json`,
`eligible_observations`, n = 90; cross-checked against the per-instance rows:
90 eligible rows) occupy exactly four (k, C) cells:

| k | C | rows |
|---|---|---|
| 5 | 1.0 | 27 |
| 10 | 0.5 | 9 |
| 20 | 0.25 | 9 |
| 25 | 0.2 | 45 |

Every row satisfies C = 5/k exactly (90/90, max |C − 5/k| = 0.000e+00), and within
each k the number of distinct C values is 1 (within-k variance 0.0 at all four
levels). Mechanically this is expected: the instrument computes C as
(max family failures)/k with 5 probes per family, so on any run where some family
is fully failed, C = 5/k; the eligible support contains only such runs.

**Record limitation:** the confirmatory runner persisted aggregates only
(`eligible_pairs` = 1200, no per-row (k, C); consistent with the persistence
limitations disclosed in `v02/REPORT_V02.md` §3). F1 is therefore verified on the
pilot's 90 persisted rows; extension to the confirmatory 1200 pairs is by
instrument identity (same frozen `study/features.py`, same pack, same builder
families), not by direct recount.

## 3. Finding F2 — the frozen spline basis spans C on the observed k-levels (verified)

The frozen design (`study/models.py`, imported unchanged by `v02/models_v02.py`):
5 knots, `rcs_basis` returns 4 columns; `design_row(k, None)` = intercept + 4 = 5
columns; `design_row(k, C)` appends C = 6 columns. On the 4 distinct eligible
(k, C) points, the 4×5 basis matrix has rank 4 (full row rank); appending the C
column leaves the rank at 4, and the least-squares residual of C on the basis is
1.100e-13 (Appendix B, section (c)).

Interpretation caveat, stated precisely: with 4 points and 5 basis columns, full
row rank makes *any* C vector on those points exactly in-span — the F2 rank fact
alone is not evidence of a special functional form. The load-bearing result is
F1: C is not merely spanned, it is a known deterministic function of k on the
eligible support. Together they imply the B-model's extra column carries no
information the A-model's k-basis does not already encode on this support.

## 4. Consequence for the terminal NEGATIVE

Frozen-rule quantities (`v02/REPORT_V02.md` §2–3): Δ = −2.639 × 10⁻⁹ nats,
95% CI [−1.519 × 10⁻⁶, 1.583 × 10⁻⁶], δ = 0.01, relabel p95 = 2.138 × 10⁻³.
The CI upper bound is far below δ, so the frozen Negative rule fires and the
classification is unchanged by this audit.

What F1/F2 change is the interpretation: the near-zero Δ is *uninformative about
independently varying concentration*, because no such variation exists on the
eligible support — every eligible observation has C fully determined by k, so
the experiment never contrasts equal-k different-C pairs. The NEGATIVE is
consistent with (and structurally expected under) C being a deterministic
transform of k; it does not test, and cannot support or refute, whether family
concentration predicts correctness when it varies independently of count. The
broader theory is neither supported nor refuted.

## 5. Caveats (jointly stated)

- **Exposure:** the confirmatory analysis was unblinded (intermediate metrics
  observed before run completion; ledger in `v02/INTEGRITY_REVIEW_2026-10-12.md`,
  disclosure in `v02/REPORT_V02.md` §1) *and* the concentration feature is
  unidentified on the eligible support (F1, this note). Both limitations apply
  together; neither is repaired by the other.
- **"10 eligible base bodies" is an inference, not a persisted field.** The pilot
  report records solver file ids, not base-body ids. Mapping
  `solver_XXX → base body` via the frozen generator's submission order — the
  header parse verified 120/120, bodies equal to the frozen generator's `S` dict
  120/120, 40 unique bodies × exactly 3 replicas — each pilot instance has 30
  eligible files spanning exactly 10 base bodies, and the base-body set
  {1, 17, 18, 19, 22, 23, 24, 25, 30, 39} is identical across instances
  101/102/103 (Appendix B, section (d)).
- **Probe-suite premise (directly checked, not inferred from code reading).**
  Across 11 seeds (the 3 pilot seeds plus 8 arbitrary), `make_probe_suite`
  output hashes to 1 unique value over all graph-relevant fields; the only
  probe-dict key that varies with the seed is the derived metadata field
  `"seed"`. Probe graphs, predicates, and satisfaction vectors are
  builder-determined and seed-independent (Appendix B, section (a)).

## 6. Design note (not an authorization)

Identifying the incremental predictive value of family concentration would
require eligible submissions with **equal k and different C** — the same number
of probe failures distributed differently across families. Neither v0.1 nor
v0.2 produced or was capable of producing such pairs under its generators. This
sentence is recorded so that any future study version, if ever commissioned by
the repository owner, starts from the corrected premise. **No v0.3 is designed,
specified, or authorized by this note.**

## 7. Verification (counts, not verdicts)

Executed 2026-10-14 against the frozen repository state. Full script: Appendix A.
Full output: Appendix B. Summary of explicit counts:

- (a) seeds tested = 11; probes per suite = 30; unique graph-content hashes = 1;
  unique full-dict hashes = 11 (metadata `"seed"` only); probe keys differing vs
  baseline = `['seed']`.
- (b) eligible observations = 90; table cells = 4 as above; rows satisfying
  C == 5/k = 90/90; max |C − 5/k| = 0.0; within-k variance = 0.0 at k ∈
  {5, 10, 20, 25}; cross-check vs per-instance eligible rows = 90.
- (c) knots = 5; `rcs_basis` columns = 4; `design_row(k, None)` = 5 columns
  (intercept included); `design_row(k, C)` = 6; basis matrix 4×5;
  rank(basis) = 4; rank(basis|C) = 4; col-space dimension = 4;
  max |residual of C on basis| = 1.100e-13.
- (d) frozen generator `S` entries = 40, distinct bodies = 40; pack files = 120;
  header parse = 120/120; bodies matching frozen `S` = 120/120; unique body
  hashes = 40; files per base body = 3 for all 40; per instance: 30 eligible
  files → 10 base bodies, set identical across instances.

### Record integrity at time of writing (pre-commit gate, 2026-10-14)

- `FREEZE_V02.md` file hashes: 14/14 verified. Thirteen entries match their
  frozen hashes on both worktree and git-blob bytes. `v02/run_confirmatory_v02.py`
  matches the *executed* hash `b2c02ddeb0af…` recorded in
  `v02/INTEGRITY_REVIEW_2026-10-12.md`; its frozen record hash `19c4104759…`
  differs only by the disclosed harness-repair diff (record-only).
- Pack (`generation_v02/pack/`, 120 files): no commit since freeze commit
  `8f83ee8` touched the pack; worktree == HEAD.
- `v02/FREEZE_V02.md` itself unchanged since `8f83ee8`.
- v0.1 `FREEZE.md` §5 rlc0 inventory: 26/26 intact.
- This commit touches only this note (new file) and one appended line in the
  non-frozen `README.md`.

## 8. Closure

This note closes the v0.2 interpretability audit. v0.2 remains terminal NEGATIVE
under the frozen decision rule, now with the interpretation limitation recorded
above. v0.1 remains terminal INFEASIBLE. Whether any successor study is ever
designed is a decision for the repository owner and is not contemplated,
authorized, or pre-authorized here.

## Appendix A — verification script (read-only)

```python
"""v0.2 interpretability audit — read-only verification (2026-10-14).

Checks (a)-(d) requested by CLAUDE. Prints explicit counts; no pass/fail shortcuts.
Runs against the frozen repository files only; writes nothing.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\pakla\PycharmProjects\failure-concentration-study")
sys.path.insert(0, str(ROOT))

from study.models import KNOTS, design_row, rcs_basis  # noqa: E402
from study.probes import make_probe_suite  # noqa: E402


def section(title: str) -> None:
    print(f"\n===== {title} =====")


# ---------------------------------------------------------------- (a)
section("(a) probe-suite seed invariance")
SEEDS = [101, 102, 103, 1, 2, 3, 4, 5, 6, 7, 8]  # 3 pilot seeds + 9 arbitrary
GRAPH_KEYS = (
    "probe_id", "family", "variant", "n", "edges", "s", "t",
    "assigned_predicate", "sat_vector",
)


def graph_payload(probes: list[dict]) -> str:
    return json.dumps([{k: p[k] for k in GRAPH_KEYS} for p in probes], sort_keys=True)


suites = {s: make_probe_suite(s) for s in SEEDS}
graph_hashes = {
    hashlib.sha256(graph_payload(suites[s]).encode()).hexdigest() for s in SEEDS
}
full_hashes = {
    hashlib.sha256(json.dumps(suites[s], sort_keys=True).encode()).hexdigest()
    for s in SEEDS
}
base = suites[101]
diff_keys: set[str] = set()
for s in SEEDS:
    if s == 101:
        continue
    for pb, po in zip(base, suites[s]):
        for k in set(pb) | set(po):
            if pb.get(k) != po.get(k):
                diff_keys.add(k)
print(f"seeds_tested={len(SEEDS)} probes_per_suite={len(base)}")
print(f"unique_graph_content_hashes={len(graph_hashes)} (expect 1)")
print(f"unique_full_dict_hashes={len(full_hashes)} (hashes include seed metadata field)")
print(f"probe_dict_keys_differing_vs_seed101={sorted(diff_keys)} (expect ['seed'] only)")
print(f"premise_holds={len(graph_hashes) == 1 and diff_keys == {'seed'}}")

# ---------------------------------------------------------------- (b)
section("(b) pilot eligible (k, C) table; C == 5/k count; within-k variance")
pilot = json.loads(
    (ROOT / "v02" / "pilot_v02" / "pilot_v02_report.json").read_text(encoding="utf-8")
)
obs = pilot["eligible_observations"]
print(f"eligible_observations={len(obs)}")
table = Counter((o["k"], o["C"]) for o in obs)
for (k, c), n in sorted(table.items()):
    print(f"  k={k:<3} C={c!s:<6} rows={n}  5/k={5.0 / k}")
eq = sum(1 for o in obs if abs(o["C"] - 5.0 / o["k"]) <= 1e-12)
maxdiff = max(abs(o["C"] - 5.0 / o["k"]) for o in obs)
print(f"rows_satisfying_C==5/k: {eq}/{len(obs)}  max_abs_diff={maxdiff:.3e}")
byk: dict[int, set[float]] = defaultdict(set)
for o in obs:
    byk[o["k"]].add(o["C"])
for k in sorted(byk):
    var = 0.0 if len(byk[k]) == 1 else float("nan")
    print(f"within_k k={k}: distinct_C={sorted(byk[k])} variance={var}")
rows_elig = sum(
    1 for inst in pilot["instances"].values() for r in inst["rows"] if r["eligible"]
)
print(f"cross_check_instances_rows_eligible={rows_elig} (expect == len(obs))")

# ---------------------------------------------------------------- (c)
section("(c) frozen spline basis: columns, intercept, rank, residual of C on basis")
ks_c = sorted({(o["k"], o["C"]) for o in obs})
print(f"knots={len(KNOTS)} rcs_basis_cols={len(rcs_basis(math.log(1 + 5)))}")
print(f"design_row(k,None)_cols={len(design_row(5, None))} design_row(k,C)_cols={len(design_row(5, 1.0))}")
print(f"distinct_(k,C)_points={ks_c}  points={len(ks_c)}")
X = [design_row(k, None) for k, _ in ks_c]
Cvec = [c for _, c in ks_c]
ncols = len(X[0])


def rank(M: list[list[float]], tol: float = 1e-9) -> int:
    A = [row[:] for row in M]
    rows, cols = len(A), len(A[0])
    r = 0
    for c in range(cols):
        piv = max(range(r, rows), key=lambda i: abs(A[i][c]))
        if abs(A[piv][c]) < tol:
            continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(rows):
            if i != r and abs(A[i][c]) > tol:
                f = A[i][c] / A[r][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
        if r == rows:
            break
    return r


def proj_residual(M: list[list[float]], y: list[float]) -> tuple[list[float], int]:
    cols = list(zip(*M))
    basis: list[list[float]] = []
    for col in cols:
        v = list(col)
        for b in basis:
            dot = sum(x * yy for x, yy in zip(v, b))
            v = [x - dot * bb for x, bb in zip(v, b)]
        nv = math.sqrt(sum(x * x for x in v))
        if nv > 1e-10:
            basis.append([x / nv for x in v])
    proj = [0.0] * len(y)
    for b in basis:
        d = sum(yv * bb for yv, bb in zip(y, b))
        proj = [p + d * bb for p, bb in zip(proj, b)]
    return [yv - pv for yv, pv in zip(y, proj)], len(basis)


rank_X = rank(X)
rank_aug = rank([row + [c] for row, c in zip(X, Cvec)])
resid, bdim = proj_residual(X, Cvec)
print(f"basis_matrix={len(X)}x{ncols} (intercept + {ncols - 1} rcs columns)")
print(f"rank(basis)={rank_X}  rank(basis|C)={rank_aug}  col_space_dim={bdim}")
print(f"max_abs_residual_of_C_on_basis={max(abs(r) for r in resid):.3e}")
print(f"residual_vector={[round(r, 15) for r in resid]}")
print(
    "note: points(4) <= basis_cols(5) => full row rank => any C vector on these "
    "points is exactly in-span; the load-bearing finding is (b): C is a "
    "deterministic function of k on the eligible support (90/90)."
)

# ---------------------------------------------------------------- (d)
section("(d) distinct base solver bodies after header stripping; eligible bases")
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("gen_pack_audit", ROOT / "v02" / "generate_pack.py")
assert spec and spec.loader
gp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gp)  # module-level only; main() is __main__-guarded
s_bodies = {b: hashlib.sha256(b.encode()).hexdigest() for b in gp.S.values()}
print(f"frozen_generator_S_entries={len(gp.S)} distinct_S_bodies={len(set(s_bodies.values()))}")

pack = sorted((ROOT / "generation_v02" / "pack").glob("solver_*.py"))
print(f"pack_files={len(pack)}")
hdr_re = re.compile(r'^"""Submission (\d{3}) \(base body (\d+), replica (\d+)\)\."""\n\n')
body_hashes: list[str] = []
header_ok = 0
match_S = 0
per_base_files: dict[int, list[str]] = defaultdict(list)
for p in pack:
    norm = p.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = hdr_re.match(norm)
    if not m:
        print(f"HEADER_PARSE_FAIL {p.name}")
        continue
    header_ok += 1
    _n, base_no, _rep = int(m.group(1)), int(m.group(2)), int(m.group(3))
    body = norm[m.end():]
    body_hashes.append(hashlib.sha256(body.encode()).hexdigest())
    per_base_files[base_no].append(p.name)
    if body == gp.S[base_no]:
        match_S += 1
print(f"header_parse_ok={header_ok}/{len(pack)}")
print(f"bodies_matching_frozen_generator_S={match_S}/{len(pack)}")
print(f"unique_body_hashes={len(set(body_hashes))} (expect 40)")
rep_counts = Counter(len(v) for v in per_base_files.values())
print(f"files_per_base_body_distribution={dict(rep_counts)} (expect all 3)")
base_sets = {}
for ik, inst in sorted(pilot["instances"].items()):
    elig = [r["solver"] for r in inst["rows"] if r["eligible"]]
    bases = sorted({(int(s.split("_")[1]) - 1) // 3 + 1 for s in elig})
    base_sets[ik] = tuple(bases)
    print(f"instance={ik} eligible_files={len(elig)} distinct_eligible_base_bodies={len(bases)} bases={bases}")
same = len(set(base_sets.values())) == 1
print(f"eligible_base_body_sets_identical_across_instances={same}")
print(
    "note: mapping solver_XXX -> base body via the frozen generator's "
    "submission order (verified by header parse, 120/120); '10 eligible base "
    "bodies' per instance is this inference, not a persisted field."
)
```

## Appendix B — verification output (2026-10-14)

```text
===== (a) probe-suite seed invariance =====
seeds_tested=11 probes_per_suite=30
unique_graph_content_hashes=1 (expect 1)
unique_full_dict_hashes=11 (hashes include seed metadata field)
probe_dict_keys_differing_vs_seed101=['seed'] (expect ['seed'] only)
premise_holds=True

===== (b) pilot eligible (k, C) table; C == 5/k count; within-k variance =====
eligible_observations=90
  k=5   C=1.0    rows=27  5/k=1.0
  k=10  C=0.5    rows=9  5/k=0.5
  k=20  C=0.25   rows=9  5/k=0.25
  k=25  C=0.2    rows=45  5/k=0.2
rows_satisfying_C==5/k: 90/90  max_abs_diff=0.000e+00
within_k k=5: distinct_C=[1.0] variance=0.0
within_k k=10: distinct_C=[0.5] variance=0.0
within_k k=20: distinct_C=[0.25] variance=0.0
within_k k=25: distinct_C=[0.2] variance=0.0
cross_check_instances_rows_eligible=90 (expect == len(obs))

===== (c) frozen spline basis: columns, intercept, rank, residual of C on basis =====
knots=5 rcs_basis_cols=4
design_row(k,None)_cols=5 design_row(k,C)_cols=6
distinct_(k,C)_points=[(5, 1.0), (10, 0.5), (20, 0.25), (25, 0.2)]  points=4
basis_matrix=4x5 (intercept + 4 rcs columns)
rank(basis)=4  rank(basis|C)=4  col_space_dim=4
max_abs_residual_of_C_on_basis=1.100e-13
residual_vector=[-1.2e-14, 4.6e-14, -1.1e-13, 7.5e-14]
note: points(4) <= basis_cols(5) => full row rank => any C vector on these
points is exactly in-span; the load-bearing finding is (b): C is a
deterministic function of k on the eligible support (90/90).

===== (d) distinct base solver bodies after header stripping; eligible bases =====
frozen_generator_S_entries=40 distinct_S_bodies=40
pack_files=120
header_parse_ok=120/120
bodies_matching_frozen_generator_S=120/120
unique_body_hashes=40 (expect 40)
files_per_base_body_distribution={3: 40} (expect all 3)
instance=101 eligible_files=30 distinct_eligible_base_bodies=10 bases=[1, 17, 18, 19, 22, 23, 24, 25, 30, 39]
instance=102 eligible_files=30 distinct_eligible_base_bodies=10 bases=[1, 17, 18, 19, 22, 23, 24, 25, 30, 39]
instance=103 eligible_files=30 distinct_eligible_base_bodies=10 bases=[1, 17, 18, 19, 22, 23, 24, 25, 30, 39]
eligible_base_body_sets_identical_across_instances=True
note: mapping solver_XXX -> base body via the frozen generator's
submission order (verified by header parse, 120/120); '10 eligible base
bodies' per instance is this inference, not a persisted field.
```
