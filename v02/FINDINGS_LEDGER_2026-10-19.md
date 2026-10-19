# v0.2 Findings Ledger — corrected

**Date:** 2026-10-19
**Status:** audit deliverable for checklist item 8 ("correct the findings ledger so every
conclusion has matching evidence and scope"). Append-only. No frozen file was edited; no
pipeline stage was re-executed for the frozen record (all recomputation below is read-only);
no decision rule, threshold, model, seed, or analysis constant was changed.
v0.1 remains terminal **INFEASIBLE**; v0.2 remains terminal **NEGATIVE** under the frozen
rule. No successor study is designed, specified, or authorized by this note.

**Relation to prior records.** This ledger restates every audit conclusion with its matching
evidence and scope, and records the corrections it makes to
`v02/INTERPRETABILITY_AUDIT_2026-10-14.md` (and addenda B, C) and
`v02/INTEGRITY_REVIEW_2026-10-12.md`. The preserved texts of those records are not edited;
the list of corrected readings is section 4.

**Revision 2 (2026-10-19, post-review).** F3 wording corrected (the column-space result
establishes redundancy of representational contribution, not the cause of the residual
Delta); every finding now carries severity and disposition; reproducible numerical results
are separated from record, execution-history, and provenance findings; unresolved items are
retained as unresolved.

## 1. Method

Read-only recomputation executed 2026-10-19 against the frozen repository state: frozen pack
`generation_v02/pack/` (120 files), frozen `v02/models_v02.py`, `v02/spec_v02.json`,
`v02/PROTOCOL_V02.md`, the frozen `study/` instrument, and the persisted terminal report
`v02/confirmatory_v02/confirmatory_v02_report.json`. The confirmatory scoring
(120 solvers x 40 hidden suites), the LOIO decomposition, the 10 000-resample bootstrap, the
probe/hidden suite builders, and the frozen spline basis were re-run. The recomputation
reproduces the persisted report bitwise (Delta, CI, and all 40 `delta_i`) and is an audit
check, not a new record. Script: Appendix A; output: Appendix B.

**Separation rule.** A reproducible numerical result does not automatically validate every
record describing the experiment. The numerical and content-reproduction findings (F1-F5,
F12) are classified separately from the record, execution-history, and provenance findings
(F6-F11). Severity: High = materially affects interpretation or provenance; Medium = bounded
record/reporting defect; Low = labeling or description defect; Verified = audit check passed
with no defect. Disposition: closed = no further action; corrected = superseded here;
retained = recorded and preserved; unresolved = no resolution available from committed
artifacts.

## 2. Findings ledger

| ID | Class | Conclusion | Evidence | Scope | Severity | Disposition |
|---|---|---|---|---|---|---|
| F1 | Numerical | C = 5/k exactly on the eligible realized support, because every eligible row has a fully failed family | `study/features.py:11,48-60` (5 probes/family; C = max family count / k), `study/families.py:44` (6 families F1-F6), `study/probes.py:74-86` (30 probes); pilot 90/90 (audit A section 2); confirmatory 1200/1200 recomputed (Appendix B section A); max abs diff 0.0; max family count = 5 in 1200/1200 rows | Eligible support only (k in {5,10,20,25}). The identity is conditional on the failure pattern: guaranteed for k >= 25, not for all k >= 2, and not universal | Verified | Closed (direct recount, confirmatory included) |
| F2 | Numerical | The frozen Model A spline basis spans C on the observed support | 5 knots, 4-column `rcs_basis`, `design_row(k,None)` 5 columns (audit A section 3); recomputed: 4x5 basis rank 4, augmented rank 4, max residual of C on basis 1.100e-13 (Appendix B section E) | The 4 observed (k,C) points. Caveat (load-bearing): with 4 points and 5 columns, rank 4 is full row rank, so *any* C vector on these points is in span; the rank fact alone is vacuous. F1 is the substantive fact | Verified | Closed with caveat |
| F3 | Numerical | Model B adds no new function-space capacity on the observed support. The near-zero Delta is consistent with this redundancy, but the result does not test whether independently varying concentration improves prediction beyond failure count | C is in the span of A (F2), so `col(B) = col(A)` and the two model families represent exactly the same prediction functions on the support. Observed Delta = -2.639e-9, CI [-1.519e-6, 1.583e-6], reproduced bitwise (Appendix B section D) | Eligible support and frozen comparison only. The column-space result does not establish that the residual Delta was *caused* by ridge regularization (ridge coefficients are parameterization-dependent), nor that the comparison is universally equivalent under regularization. Says nothing about C's predictive value where C varies at fixed k | Verified | Corrected wording adopted; source of the residual Delta not established |
| F4 | Structure | 1200 eligible solver-instance pairs contain 400 distinct (base body, instance) outcome cells x3 byte-identical replicas; 10 distinct eligible base bodies | Pilot: 90 = 30/instance x3, cells 27/9/9/45 (audit A section 2). Confirmatory: 1200 = 30/instance x40, cells k=5,C=1.0: 360; k=10,C=0.5: 120; k=20,C=0.25: 120; k=25,C=0.2: 600; per-instance composition identical to pilot (9/3/3/15). Pack 120 files = 40 bodies x3 replicas (`v02/generate_pack.py:788-800`); eligible bodies {1,17,18,19,22,23,24,25,30,39} identical across all 40 instances; replicas have identical fail vectors and identical hidden-suite successes in every instance (0/400 groups differ; Appendix B section A/C) | Inference target dependent. Instance-level resampling of the 40 instances may be appropriate for unseen instances with the solver panel held fixed. Generalization to a population of unseen solvers has 10 distinct eligible bodies, not 1200 independent observations; the resampling scheme must be justified against the intended target | High (unit of analysis) | Retained; no solver-population claim supported; resampling justification required before one |
| F5 | Structure | Seed invariance holds for the diagnostic probes (1 graph hash across 40 seeds) and fails for the hidden suites (40/40 distinct); k and C are constant per solver across all instances | Appendix B section F; addenda A section 5, B section 2 | Diagnostic probe generalization is untested (one suite, shared); hidden-suite generalization is tested across the 40 drawn suites only | Verified | Closed; scope as stated |
| F6 | Record | The report's `delta_i` is ordered by sorted instance id; Addendum B's Check 3 table mispairs it with derivation-order seeds | `v02/models_v02.py:93` (`instances = sorted(...)`); corrected mapping (section 3, Appendix B section D) versus Addendum B section 2 Check 3. Example: the table's `i=00 seed=9774360 delta_i=-4.167523369513759e-06` is wrong — that Delta belongs to seed 157040, and seed 9774360's actual Delta is -5.257325645713351e-06 (sorted index 39). Only positions 01, 21, 24, 31 coincide between the two orderings | Record labeling only: the 40 values, their multiset, the CI, and the classification are unaffected; per-instance interpretations were unreliable until corrected | Medium | Corrected in this ledger (section 3); Addendum B text preserved unedited |
| F7 | Execution history | Intermediate Delta/CI and 3 relabel draws were observed before the completed run; no rule, threshold, model, seed, or constant changed; the leaked interval already implied the final classification | `v02/REPORT_V02.md` section 1; `v02/INTEGRITY_REVIEW_2026-10-12.md` table rows 1-5. The 3 observed draws recompute exactly as [0.002137832910273971, -2.8978386594769036e-07, 0.0021377640831307413]; the full-data LOIO Delta recomputes exactly | v0.2 is not a blind confirmation; the arithmetic and frozen-rule classification are unaffected | High (integrity) | Disclosed; retained; arithmetic reproduced bitwise |
| F8 | Record | `REPORT_V02.md` and `INTEGRITY_REVIEW_2026-10-12.md` number the attempts inconsistently | Report section 1: attempts 1-2 crashed pre-scoring; attempt 3 printed the real Delta/CI then was killed; runtime profiling (unnumbered) observed 3 draws and the full-data Delta; attempt 4 aborted after reprinting; attempt 5 completed. Integrity table: rows 1-3 match; row 4 is the timing profile; row 5 is the aborted retry; the completed run is absent | Record-only; affects the timeline reading, not the arithmetic or classification | Low | Reconciled reading recorded (section 4 item 7); original records preserved |
| F9 | Provenance | The recorded pack manifest hash is not reproducible from the committed artifacts, and no committed script computes a manifest | `v02/FREEZE_V02.md:23` records `cc695487c9e31c00424ae283b493ae2ded584eaf087a1bfa63458364a3ff828e` for the described ordered SHA256-of-SHA256 manifest; not reproduced by that scheme or 1000+ tested canonicalizations (LF/CRLF bytes, hex/digest, name+hash, sha256sum, git blob SHA-1/SHA-256, raw concatenations, double hashing, 40-body subsets); `v02/generate_pack.py` contains no manifest computation | Input provenance only; says nothing about pack content. That the pack was altered, or that the discrepancy was intentional, is NOT established | High (provenance) | Retained UNRESOLVED |
| F10 | Provenance | `v02/generate_pack.py` was first committed after the pack, so the freeze line's chronology is not supported by the commit graph | The freeze line `v02/FREEZE_V02.md:22` says "added by addendum before any pack emission; body frozen"; `git cat-file -e 8f83ee8:v02/generate_pack.py` fails; the file first appears at `a6a8439` ("commit generator artifact"), after the pack commit `8f83ee8` (timestamps 15:43 vs 14:13) | Provenance chain not fully reproducible; pack content provenance is intact (120/120 bodies equal the generator's `S`) | Medium | Retained as verified inconsistency; no content effect |
| F11 | Provenance | The documented output path never existed, and the documented pack structure contradicts the implementation | `v02/generate_pack.py:11` sets `OUT` to `v02/pack`; `git log --all -- v02/pack` is empty (the pack is `generation_v02/pack`, committed at `8f83ee8`); the docstring (`:3`) says "20 strategy families x 6 real variants" while `:788-800` emits 40 bodies x 3 replicas, matching the committed pack | Record/description defect; no content effect | Low-Medium | Retained as verified inconsistency |
| F12 | Provenance | Content integrity of the pack, analysis code, and terminal report verified by reconstruction | 13 of 14 frozen file hashes match at audit time; `v02/run_confirmatory_v02.py` matches the disclosed executed hash `b2c02dde...` (repair at `a6a8439`) while its frozen record `19c410...` matches the blob at the freeze tag `798b446`; pack headers 120/120 and bodies 120/120 match the generator's `S`; worktree pack bytes equal HEAD after LF normalization; terminal report reproduced bitwise (F1-F3, F5) | Content only; the manifest record (F9) and generator chronology (F10-F11) are excluded from this verification | Verified | Closed; content alteration not established |
| F13 | Status | v0.1 is INFEASIBLE; v0.2 is NEGATIVE under the frozen rule; no successor is authorized | Frozen decision rule on the reproduced quantities: CI upper 1.583e-6 < 0.01; v0.1 pilot yield gate 4/20 < 15 | The NEGATIVE is a valid frozen-rule classification with no evidential content about concentration's predictive value (F1-F3). The broader theory is neither supported nor refuted | n/a | Unchanged |

## 3. Corrected per-instance `delta_i` mapping (sorted instance-id order)

The frozen report stores `delta_i` in sorted instance-id order (`v02/models_v02.py:93`).
This is the corrected pairing; it supersedes the seed column of Addendum B section 2 Check 3.

| i | seed | delta_i |
|---|---|---|
| 00 | 157040 | -4.167523369513759e-06 |
| 01 | 197002 | -7.724499034189591e-06 |
| 02 | 861348 | 7.62933378695152e-08 |
| 03 | 1055675 | -1.069481216475765e-06 |
| 04 | 1423543 | 1.7247559931377054e-06 |
| 05 | 1834717 | 2.5179544623776806e-06 |
| 06 | 1890265 | -5.1244292776919664e-06 |
| 07 | 1970638 | 6.935942994834576e-06 |
| 08 | 2101043 | -2.3288148078837168e-06 |
| 09 | 2106121 | -3.851658032627547e-06 |
| 10 | 2285332 | 4.614931289892432e-06 |
| 11 | 2387299 | 7.231197568513537e-07 |
| 12 | 2750535 | -3.6699566399178707e-06 |
| 13 | 3036896 | -4.151388433348835e-06 |
| 14 | 3284208 | -2.3007358940230205e-06 |
| 15 | 3490574 | 5.075307776380988e-06 |
| 16 | 3600035 | -9.411245243451383e-06 |
| 17 | 3605375 | 4.871783219617676e-06 |
| 18 | 3751822 | -1.6841098711140035e-06 |
| 19 | 3914224 | -3.2083073620015057e-07 |
| 20 | 4040201 | 3.0268916331177564e-06 |
| 21 | 4629490 | 9.444363571087244e-06 |
| 22 | 4976410 | 1.1183694262895116e-06 |
| 23 | 5047746 | -2.7018968620229344e-06 |
| 24 | 5171755 | 7.874426088516628e-06 |
| 25 | 5952838 | -8.26188460734123e-06 |
| 26 | 6283407 | 2.698397016942522e-08 |
| 27 | 6308794 | -2.37621352483508e-06 |
| 28 | 7261847 | 8.365444202906858e-07 |
| 29 | 7337101 | -6.841061361839706e-08 |
| 30 | 7610233 | 1.9350953650576486e-07 |
| 31 | 7928323 | 1.5722448520438803e-05 |
| 32 | 8195336 | -6.6351297552946775e-06 |
| 33 | 8282449 | 1.9350958546660024e-07 |
| 34 | 8672265 | 1.302400689517924e-07 |
| 35 | 8927684 | 3.6179963699423112e-06 |
| 36 | 9237077 | -1.2627494523353988e-06 |
| 37 | 9420200 | 6.194107738721755e-06 |
| 38 | 9503518 | -2.656753927965383e-06 |
| 39 | 9774360 | -5.257325645713351e-06 |

The derivation-order seed list itself is correct in Addendum B; only the pairing with the
sorted-order `delta_i` column is wrong. Positions 01, 21, 24, 31 coincide by chance; all
other rows of that table are mispaired.

## 4. Corrections to earlier records

1. **Addendum B section 2 Check 3** (F6) — seed/`delta_i` pairing corrected by section 3.
   Values, multiset, CI, and classification unchanged.
2. **Note A section 2 record limitation** ("F1 verified on the pilot's 90 persisted rows;
   extension to the confirmatory 1200 is by instrument identity, not direct recount") — the
   direct recount has now been performed read-only: 1200/1200 rows satisfy C = 5/k, max
   family count 5 in every row. The limitation is closed by audit recomputation; the frozen
   record itself still does not persist per-row (k,C).
3. **Note A section 7 / Addendum B operational statements on the pack** — "worktree == HEAD"
   holds after LF normalization; the worktree bytes differ from HEAD blobs for 120/120 files
   because of `core.autocrlf` CRLF checkout. No commit after `8f83ee8` changes pack content.
4. **`v02/FREEZE_V02.md:23` pack manifest** (F9) — the recorded hash
   `cc695487c9e31c00424ae283b493ae2ded584eaf087a1bfa63458364a3ff828e` is not reproducible
   from committed pack bytes under the described scheme or 1000+ tested canonicalizations,
   and no committed script computes a manifest. Retained as an unresolved provenance gap,
   not as content corruption.
5. **`v02/FREEZE_V02.md:22` generator line** (F10) — "added by addendum before any pack
   emission" is not supported by the commit graph: the freeze line was added at the pack
   commit `8f83ee8`, while `v02/generate_pack.py` was first committed at `a6a8439` ("commit
   generator artifact"). Content provenance is unaffected (120/120 bodies match the
   generator's `S`).
6. **`v02/generate_pack.py:3,11` description and output path** (F11) — the docstring
   "20 strategy families x 6 real variants" contradicts the implementation (40 bodies x 3
   replicas, `:788-800`), and `OUT` (`v02/pack`) never existed in git history (the pack is
   `generation_v02/pack`).
7. **Attempt numbering** (F8) — `v02/REPORT_V02.md` section 1 and the
   `v02/INTEGRITY_REVIEW_2026-10-12.md` table interleave differently: the report's
   unnumbered "runtime profiling" item is table row 4; the report's attempt 4 is table
   row 5; the report's attempt 5 (the completed run) is absent from the table because the
   table was written before completion. Reconciled reading: five numbered attempts, one
   unnumbered read-only profiling step.
8. **Unit-of-analysis disclosure** — previous notes stated 40 unique bodies x 3 replicas
   but did not state that the replicas have identical hidden-suite outcomes within each
   instance (0/400 differing groups) and that the 1200 rows therefore contain 400 distinct
   (body, instance) outcome cells. Added as F4.

None of these corrections changes any frozen-rule quantity or the terminal classification.

## 5. Boundaries (what this audit does not establish)

- No claim about C's predictive value where C varies at fixed k: that variation does not
  exist on either eligible support, so the question is untested by v0.1 and v0.2.
- The column-space result (F2/F3) establishes that Model B adds no representational capacity
  on the support. It does not establish that the residual Delta was caused by ridge
  regularization, and it does not establish that the frozen model comparison is universally
  equivalent under regularization.
- No claim about generalization to a solver population: the panel contains 10 distinct
  eligible base bodies with three byte-identical replicas each; any solver-population
  inference would require a resampling scheme justified against that structure (F4).
- No claim beyond the eligible support, the frozen model classes, the 40 hidden suites, or
  the single shared diagnostic probe suite.
- No authorization, design, or pre-authorization of any successor study.
- The manifest-hash gap (F9) is retained as unresolved; the generator-history inconsistencies
  (F10-F11) are retained as verified inconsistencies. No evidence of content alteration of
  the pack, the analysis code, or the terminal report was found (F12), and the terminal
  report is reproduced bitwise from the frozen artifacts (F1-F3, F5).

## 6. Final scientific disposition

| Question | Current conclusion |
|---|---|
| Is C = 5/k universal? | No. Verified on the eligible realized rows only; it holds whenever a family fully fails (guaranteed for k >= 25, not for all k >= 2) (F1) |
| Was the identity verified on confirmatory data? | Yes, by read-only reconstruction of all 1200 eligible pairs (F1) |
| Does v0.2 establish whether concentration adds independent predictive information? | No. The realized support supplies no equal-k/different-C contrast (F1-F3) |
| Is the near-zero Delta reproducible? | Yes, bitwise: estimate, interval, and all 40 instance-level values (F3, Appendix B section D) |
| Does that prove the frozen model comparison is universally equivalent under regularization? | No. The column-space argument alone does not establish that (F3, section 5) |
| Are the 1200 pairs 1200 independent solver observations? | No. 400 distinct body-by-instance outcome cells x3 replicas; 10 distinct eligible base bodies (F4) |
| Is the analysis fully blind? | No, per the documented exposure timeline (F7) |
| Is provenance fully closed? | No. The manifest-hash gap and generator-history inconsistencies remain unresolved (F9-F11) |

## Appendix A — verification script (read-only)

Executed 2026-10-19 with the repository virtual environment
(`.venv\Scripts\python.exe`), from the repository root. Writes nothing.

```python
"""v0.2 findings-ledger verification (read-only; 2026-10-19).

Recomputes, from frozen artifacts only:
  A. confirmatory eligible counts: 1200 rows, (k,C) cells, C == 5/k, fully-failed family
  B. base-body/replica structure: 120 files, 40 bodies x 3 replicas, eligible base set
  C. replica outcome identity: identical fails vectors / successes within (body, instance)
  D. delta / CI / delta_i reproduction and sorted-order seed mapping (corrects Addendum B labels)
  E. Model A frozen basis on the confirmatory support: rank / residual of C
  F. seed invariance: probe graph hash vs hidden-suite hashes
Writes nothing. Prints explicit counts only.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\pakla\PycharmProjects\failure-concentration-study")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "v02"))

from models_v02 import bootstrap_ci, build_pairs, loo_delta_pairs  # noqa: E402
from study.features import _norm_ref, concentration, load_solver, run_probes  # noqa: E402
from study.instances import make_hidden_suite  # noqa: E402
from study.models import KNOTS, design_row, rcs_basis  # noqa: E402
from study.probes import make_probe_suite  # noqa: E402
from study.sssp import dijkstra_ref  # noqa: E402
from run_confirmatory_v02 import confirmatory_seeds  # noqa: E402


def section(t: str) -> None:
    print(f"\n===== {t} =====")


report = json.loads(
    (ROOT / "v02" / "confirmatory_v02" / "confirmatory_v02_report.json").read_text(encoding="utf-8")
)
freeze = (ROOT / "v02" / "FREEZE_V02.md").read_text(encoding="utf-8")
proto16 = freeze.split("**v0.2 protocol hash:** `")[1][:16]
assert proto16 == report["proto_hash16"], "protocol hash mismatch"
seeds = confirmatory_seeds(proto16)
pack = sorted((ROOT / "generation_v02" / "pack").glob("solver_*.py"))

# ---------------------------------------------------------------- F (cheap)
section("F. seed invariance: probe graphs vs hidden suites (40 confirmatory seeds)")
GRAPH_KEYS = ("probe_id", "family", "variant", "n", "edges", "s", "t", "assigned_predicate", "sat_vector")
probe_hashes, hid_hashes = [], []
for s in seeds:
    probes_s = make_probe_suite(s)
    probe_hashes.append(hashlib.sha256(
        json.dumps([{k: p[k] for k in GRAPH_KEYS} for p in probes_s], sort_keys=True).encode()
    ).hexdigest())
    hid_hashes.append(hashlib.sha256(json.dumps(make_hidden_suite(s), sort_keys=True).encode()).hexdigest())
print(f"seeds={len(seeds)} distinct_seeds={len(set(seeds))}")
print(f"probe_graph_content_hashes={len(set(probe_hashes))} (metadata 'seed' excluded)")
print(f"hidden_suite_hashes={len(set(hid_hashes))}")

# ---------------------------------------------------------------- B (cheap)
section("B. pack structure: files, base bodies, replicas, headers")
hdr_re = re.compile(rb'^"""Submission (\d{3}) \(base body (\d+), replica (\d+)\)\."""\n\n')
body_sha, per_base, header_ok, header_fail = [], defaultdict(list), 0, []
for p in pack:
    b = p.read_bytes().replace(b"\r\n", b"\n")
    m = hdr_re.match(b)
    if not m:
        header_fail.append(p.name)
        continue
    header_ok += 1
    per_base[int(m.group(2))].append(p.name)
    body_sha.append(hashlib.sha256(b[m.end():]).hexdigest())
print(f"pack_files={len(pack)} header_parse_ok={header_ok}/{len(pack)} header_fail={header_fail}")
print(f"distinct_bodies={len(set(body_sha))} files_per_base_body={dict(Counter(len(v) for v in per_base.values()))}")

# ---------------------------------------------------------------- A + C (scoring)
section("A/C. confirmatory eligibility + replica outcome identity (scoring recomputation)")
solvers = [load_solver(p) for p in pack]
base_of = {p.name: int(hdr_re.match(p.read_bytes().replace(b"\r\n", b"\n")).group(2)) for p in pack}
print(f"solvers_loaded={len(solvers)}")
t0 = time.time()
probes = make_probe_suite(seeds[0])
fails_by_solver = [run_probes(fn, probes) for fn in solvers]
print(f"probe_scoring_seconds={time.time() - t0:.1f}")

obs, per_instance = [], {}
rep_groups_equal, rep_groups_total = 0, 0
for seed in seeds:
    hidden = make_hidden_suite(seed)
    expected = [_norm_ref(dijkstra_ref(h["n"], h["edges"], h["s"], h["t"])) for h in hidden]
    rows = []
    for p, fn, fails in zip(pack, solvers, fails_by_solver):
        k, c = concentration(fails)
        if k < 2:
            continue
        succ = 0
        for h, exp in zip(hidden, expected):
            try:
                out = fn(h["n"], h["edges"], h["s"], h["t"])
                ok = not isinstance(out, bool) and isinstance(out, int) and out == exp
            except Exception:
                ok = False
            succ += 1 if ok else 0
        rows.append({"instance": seed, "k": k, "C": c, "successes": succ, "fails": tuple(fails), "base": base_of[p.name]})
        obs.append(rows[-1])
    per_instance[seed] = rows

print(f"eligible_rows={len(obs)} (persisted report eligible_pairs={report['eligible_pairs']})")
cells = Counter((o["k"], o["C"]) for o in obs)
for (k, c), n in sorted(cells.items()):
    print(f"  k={k:<3} C={c!r:<6} rows={n}  5/k={5.0 / k!r}")
eq = sum(1 for o in obs if abs(o["C"] - 5.0 / o["k"]) <= 1e-12)
maxdiff = max(abs(o["C"] - 5.0 / o["k"]) for o in obs)
print(f"rows_satisfying_C==5/k={eq}/{len(obs)} max_abs_diff={maxdiff:.3e}")
fam_max = Counter()
for o in obs:
    counts = defaultdict(int)
    for i, f in enumerate(o["fails"]):
        if f:
            counts[i // 5] += 1
    fam_max[max(counts.values())] += 1
print(f"max_family_count_distribution={dict(fam_max)} (5 == a fully-failed family exists)")

rows_per_instance = Counter(len(v) for v in per_instance.values())
bases_per_instance = {s: tuple(sorted({r["base"] for r in v})) for s, v in per_instance.items()}
print(f"eligible_rows_per_instance_distribution={dict(rows_per_instance)}")
print(f"distinct_eligible_base_sets={len(set(bases_per_instance.values()))} base_set={bases_per_instance[seeds[0]]}")
all_bases = set(bases_per_instance[seeds[0]])
print(f"eligible_base_body_ids={sorted(all_bases)}")
distinct_cells = len({(r["base"], r["instance"]) for r in obs})
print(f"distinct_(base_body,instance)_outcome_cells={distinct_cells} of {len(obs)} rows (replica triplication x3 expected)")

by_group = defaultdict(list)
for r in obs:
    by_group[(r["base"], r["instance"])].append(r)
diff_fails, diff_succ = 0, 0
for g in by_group.values():
    if len({r["fails"] for r in g}) > 1:
        diff_fails += 1
    if len({r["successes"] for r in g}) > 1:
        diff_succ += 1
rep_groups_total = len(by_group)
print(f"replica_groups={rep_groups_total} groups_with_differing_fails={diff_fails} groups_with_differing_successes={diff_succ}")

# ---------------------------------------------------------------- D
section("D. delta / CI / delta_i reproduction + corrected sorted-order seed mapping")
pairs = build_pairs(obs)
delta_i, delta = loo_delta_pairs(pairs)
ci_lo, ci_hi = bootstrap_ci(delta_i)
print(f"delta={delta!r} report={report['delta']!r} equal={delta == report['delta']}")
print(f"ci=({ci_lo!r}, {ci_hi!r}) report={report['ci']!r} equal={[ci_lo, ci_hi] == report['ci']}")
print(f"delta_i_n={len(delta_i)} exact_equal={delta_i == report['delta_i']}")
sorted_seeds = sorted({o["instance"] for o in obs})
print("corrected mapping (report delta_i is ordered by sorted instance id):")
for i, (s, d) in enumerate(zip(sorted_seeds, delta_i)):
    print(f"  i={i:02d} seed={s} delta_i={d!r}")
deriv_pairing = {s: d for s, d in zip(sorted_seeds, delta_i)}
mispair_examples = []
for i in range(min(5, len(seeds))):
    ds = seeds[i]
    mispair_examples.append((i, ds, report["delta_i"][i], deriv_pairing[ds]))
for i, ds, shown, actual in mispair_examples:
    print(f"addendumB_pair i={i:02d} derived_seed={ds} shown_delta={shown!r} actual_delta_for_that_seed={actual!r} match={shown == actual}")

# ---------------------------------------------------------------- E
section("E. Model A frozen basis on the confirmatory support")
ks_c = sorted(cells.keys())
print(f"knots={len(KNOTS)} rcs_basis_cols={len(rcs_basis(math.log(1 + 5)))} design_row(k,None)_cols={len(design_row(5, None))}")
X = [design_row(k, None) for k, _ in ks_c]
Cvec = [c for _, c in ks_c]
ncols = len(X[0])


def rank(M, tol=1e-9):
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


def gram_schmidt_residual(M, y):
    basis = []
    for col in zip(*M):
        v = list(col)
        for b in basis:
            d = sum(x * yy for x, yy in zip(v, b))
            v = [x - d * bb for x, bb in zip(v, b)]
        nv = math.sqrt(sum(x * x for x in v))
        if nv > 1e-10:
            basis.append([x / nv for x in v])
    proj = [0.0] * len(y)
    for b in basis:
        d = sum(yv * bb for yv, bb in zip(y, b))
        proj = [p + d * bb for p, bb in zip(proj, b)]
    return [yv - pv for yv, pv in zip(y, proj)], len(basis)


print(f"points={len(ks_c)} (k,C)={ks_c} basis_matrix={len(X)}x{ncols} (intercept + {ncols - 1} rcs)")
print(f"rank(basis)={rank(X)} rank(basis|C)={rank([r + [c] for r, c in zip(X, Cvec)])}")
resid, bdim = gram_schmidt_residual(X, Cvec)
print(f"max_abs_residual_of_C_on_basis={max(abs(r) for r in resid):.3e} col_space_dim={bdim}")
print(f"elapsed_seconds={time.time() - t0:.1f}")
```

## Appendix B — verification output (2026-10-19)

```text

===== F. seed invariance: probe graphs vs hidden suites (40 confirmatory seeds) =====
seeds=40 distinct_seeds=40
probe_graph_content_hashes=1 (metadata 'seed' excluded)
hidden_suite_hashes=40

===== B. pack structure: files, base bodies, replicas, headers =====
pack_files=120 header_parse_ok=120/120 header_fail=[]
distinct_bodies=40 files_per_base_body={3: 40}

===== A/C. confirmatory eligibility + replica outcome identity (scoring recomputation) =====
solvers_loaded=120
probe_scoring_seconds=0.0
eligible_rows=1200 (persisted report eligible_pairs=1200)
  k=5   C=1.0    rows=360  5/k=1.0
  k=10  C=0.5    rows=120  5/k=0.5
  k=20  C=0.25   rows=120  5/k=0.25
  k=25  C=0.2    rows=600  5/k=0.2
rows_satisfying_C==5/k=1200/1200 max_abs_diff=0.000e+00
max_family_count_distribution={5: 1200} (5 == a fully-failed family exists)
eligible_rows_per_instance_distribution={30: 40}
distinct_eligible_base_sets=1 base_set=(1, 17, 18, 19, 22, 23, 24, 25, 30, 39)
eligible_base_body_ids=[1, 17, 18, 19, 22, 23, 24, 25, 30, 39]
distinct_(base_body,instance)_outcome_cells=400 of 1200 rows (replica triplication x3 expected)
replica_groups=400 groups_with_differing_fails=0 groups_with_differing_successes=0

===== D. delta / CI / delta_i reproduction + corrected sorted-order seed mapping =====
delta=-2.638929627596376e-09 report=-2.638929627596376e-09 equal=True
ci=(-1.5186596329042069e-06, 1.5827074637819738e-06) report=[-1.5186596329042069e-06, 1.5827074637819738e-06] equal=True
delta_i_n=40 exact_equal=True
corrected mapping (report delta_i is ordered by sorted instance id):
  i=00 seed=157040 delta_i=-4.167523369513759e-06
  i=01 seed=197002 delta_i=-7.724499034189591e-06
  i=02 seed=861348 delta_i=7.62933378695152e-08
  i=03 seed=1055675 delta_i=-1.069481216475765e-06
  i=04 seed=1423543 delta_i=1.7247559931377054e-06
  i=05 seed=1834717 delta_i=2.5179544623776806e-06
  i=06 seed=1890265 delta_i=-5.1244292776919664e-06
  i=07 seed=1970638 delta_i=6.935942994834576e-06
  i=08 seed=2101043 delta_i=-2.3288148078837168e-06
  i=09 seed=2106121 delta_i=-3.851658032627547e-06
  i=10 seed=2285332 delta_i=4.614931289892432e-06
  i=11 seed=2387299 delta_i=7.231197568513537e-07
  i=12 seed=2750535 delta_i=-3.6699566399178707e-06
  i=13 seed=3036896 delta_i=-4.151388433348835e-06
  i=14 seed=3284208 delta_i=-2.3007358940230205e-06
  i=15 seed=3490574 delta_i=5.075307776380988e-06
  i=16 seed=3600035 delta_i=-9.411245243451383e-06
  i=17 seed=3605375 delta_i=4.871783219617676e-06
  i=18 seed=3751822 delta_i=-1.6841098711140035e-06
  i=19 seed=3914224 delta_i=-3.2083073620015057e-07
  i=20 seed=4040201 delta_i=3.0268916331177564e-06
  i=21 seed=4629490 delta_i=9.444363571087244e-06
  i=22 seed=4976410 delta_i=1.1183694262895116e-06
  i=23 seed=5047746 delta_i=-2.7018968620229344e-06
  i=24 seed=5171755 delta_i=7.874426088516628e-06
  i=25 seed=5952838 delta_i=-8.26188460734123e-06
  i=26 seed=6283407 delta_i=2.698397016942522e-08
  i=27 seed=6308794 delta_i=-2.37621352483508e-06
  i=28 seed=7261847 delta_i=8.365444202906858e-07
  i=29 seed=7337101 delta_i=-6.841061361839706e-08
  i=30 seed=7610233 delta_i=1.9350953650576486e-07
  i=31 seed=7928323 delta_i=1.5722448520438803e-05
  i=32 seed=8195336 delta_i=-6.6351297552946775e-06
  i=33 seed=8282449 delta_i=1.9350958546660024e-07
  i=34 seed=8672265 delta_i=1.302400689517924e-07
  i=35 seed=8927684 delta_i=3.6179963699423112e-06
  i=36 seed=9237077 delta_i=-1.2627494523353988e-06
  i=37 seed=9420200 delta_i=6.194107738721755e-06
  i=38 seed=9503518 delta_i=-2.656753927965383e-06
  i=39 seed=9774360 delta_i=-5.257325645713351e-06
addendumB_pair i=00 derived_seed=9774360 shown_delta=-4.167523369513759e-06 actual_delta_for_that_seed=-5.257325645713351e-06 match=False
addendumB_pair i=01 derived_seed=197002 shown_delta=-7.724499034189591e-06 actual_delta_for_that_seed=-7.724499034189591e-06 match=True
addendumB_pair i=02 derived_seed=4976410 shown_delta=7.62933378695152e-08 actual_delta_for_that_seed=1.1183694262895116e-06 match=False
addendumB_pair i=03 derived_seed=8282449 shown_delta=-1.069481216475765e-06 actual_delta_for_that_seed=1.9350958546660024e-07 match=False
addendumB_pair i=04 derived_seed=2285332 shown_delta=1.7247559931377054e-06 actual_delta_for_that_seed=4.614931289892432e-06 match=False

===== E. Model A frozen basis on the confirmatory support =====
knots=5 rcs_basis_cols=4 design_row(k,None)_cols=5
points=4 (k,C)=[(5, 1.0), (10, 0.5), (20, 0.25), (25, 0.2)] basis_matrix=4x5 (intercept + 4 rcs)
rank(basis)=4 rank(basis|C)=4
max_abs_residual_of_C_on_basis=1.100e-13 col_space_dim=4
elapsed_seconds=15.9
```
