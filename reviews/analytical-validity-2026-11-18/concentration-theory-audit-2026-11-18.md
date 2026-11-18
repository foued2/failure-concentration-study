# Audit — what happened to the concentration hypothesis

**Date:** 2026-11-18
**Scope:** the local clone at `C:\Users\pakla\PycharmProjects\failure-concentration-study`
(local `master` = `origin/master` = `33dca9b`, 0 ahead / 0 behind) plus the GitHub repository
`foued2/failure-concentration-study` as served by the API at the time of this audit.
**Method:** `git log`/`git show`/`git grep`, direct reads of the decision-bearing files, and the
GitHub REST API for branch tips, repository visibility and tags. Nothing was checked out, merged,
committed, or written into the repository. All conclusions below are quoted or counted from a file
that was opened; none are inferred from a summary document alone.

---

## 0. The answer in one paragraph

The concentration hypothesis was never tested. Every attempt to test it stopped at a gate that
comes **before** the statistical comparison: yield (v0.1), aliasing of `C` with `k` (v0.2),
attainability of the required `(k, C)` cells (the 2026-10 power work and LC518 capacity bounds),
or construction of distinguishable mechanisms (the Option B audit and the LC518 v0.21 cell
definition). The one place where fixed-`k`, different-`C` overlap genuinely existed — a 2.5-million
-case **synthetic** simulation — produced a C-gain estimate of `+0.000002` with a 95 % interval of
`[-0.000001, +0.000008]`, i.e. it failed its own frozen criterion. The repository's own current
statement is that the hypothesis "remains unresolved", and that no stored study establishes or
refutes incremental predictive value of `C` beyond `k`, or beyond `k` and `Z`. The derived
conclusion — that the programme has a **design/feasibility** problem, not a **refuted theory** — is
the one the records support.

---

## 1. What the hypothesis actually is (two different estimands)

The repository explicitly refuses to merge two claims (`README.md` lines 6–16):

| Estimand | Baseline | Where | Status |
|---|---|---|---|
| **A. `C` beyond `k` alone** | `k` only, no context covariates | natural-solver v0.2 | executed; NEGATIVE; non-identifying |
| **B. `C` beyond `k` and context `Z`** | `k` + `Z` (+ `k_unresolved`, parent family in LC518 E3) | programme / LC518 target | designed, **never executed** |

> "**No stored study has tested C beyond k-and-Z.**" — `README.md` line 15–16

A third, narrower formulation exists in `engineered-study/00_CLAIM.md` (H1a, lines 7–13): "higher
diagnostic failure concentration `C` is expected to be associated with higher held-out boundary
score `S` at a fixed diagnostic failure count `k`, after accounting for `k` and generator identity."
H1a was closed at Gate 1 before any solver was generated (§3, stage 4).

The mathematical definition used throughout (`engineered-study/09_CONCENTRATION_MATHEMATICAL_SPEC.md`
lines 40–44) is

```
C_i = max_j f_ij / k_i,     k_i = sum_j f_ij,     f_ij in {0..5},  J = 6 families
```

with `C` undefined (not zero) at `k = 0`.

---

## 2. The repository's own verdict, in its own words

Root `README.md` lines 28–29:

> "**The original concentration hypothesis is unresolved.** No stored study establishes or refutes
> incremental predictive value of C beyond k, or beyond k and Z."

Roadmap audit (`origin/docs/scientific-roadmap-audit-2026-11-18`,
`docs/SCIENTIFIC_ROADMAP_AUDIT_2026-11-18.md` §6, line 217):

> "**Do not report 'the concentration hypothesis failed.' Do not report 'the 150-solver experiment
> is ready.' The supported conclusion is that the hypothesis remains unresolved and the LC518
> design-to-execution transition remains blocked by population, provenance, computational-
> validation, custody, and authorization gates.**"

Both statements are consistent with the primary records audited below. Neither is an
interpretation added by this audit.

---

## 3. Chronology — eight stages, and the gate each one died at

| # | Dates | Record | What actually ran | Frozen outcome | Does it test `C`? |
|---|---|---|---|---|---|
| 1 | 2026-10-11 → 10-12 | `pilot/`, tag `v0.1-freeze` | 3 pilot instances × 20 submissions | **INFEASIBLE — stop** | No |
| 2 | 2026-10-12 | `v02/`, tag `v0.2-freeze` | confirmatory pack, 40 instances, 1200 eligible pairs | **NEGATIVE** | No (aliased) |
| 3 | 2026-10-14 | `v02/INTERPRETABILITY_AUDIT_2026-10-14.md` | post-hoc identification audit | NEGATIVE declared uninformative about `C` | — |
| 4 | 2026-10-17 → 10-24 | `engineered-study/` | construction audit + math spec + three-world simulation | Gate 1 **CLOSED**, W1 **FAILED** | No (design failure), then a synthetic null |
| 5 | 2026-10-21 → 10-22 | `natural-feasibility-pilot/`, `next-task/` | 3 generator runs, 1 power simulation | 0 eligible contrasts; power grid invalidated | No |
| 6 | 2026-10-25 | `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md`, `FEASIBILITY_CLOSURE_2026-10-25.md` | offline inventory of all retained data | `INFEASIBLE_WITH_CURRENT_DATA` | No |
| 7 | 2026-10-26 → 11-01 | `h3-footprint-v2…v9` | engineering harnesses, screens | no completed H3 result; 0 and 1 eligible bodies | No |
| 8 | 2026-11-01 → 11-18 | LC518-150 | bank generation only | banks exist; **0/150 solvers**; population still a draft | No |

### Stage 1 — v0.1: yield gate, not a test

`PROTOCOL.md` §11 (lines 206–209): the pilot gate requires "≥ 15 eligible pairs" per instance;
passing "establishes **feasibility only**"; failing means "stop, report INFEASIBLE — a valid
terminal outcome."

`pilot/PILOT_REPORT.md` lines 8–12 and 22–23:

| Instance | Eligible | Gate |
|---|---:|---|
| 101 | 4/20 | FAIL |
| 102 | 4/20 | FAIL |
| 103 | 4/20 | FAIL |

> "Eligible yield was exactly 20 % against a 75 % requirement; among eligible pairs there were no
> Y = 1 cases, so the predictive question could not even be posed on this pack."

16 of 20 submissions solved all 30 probes (`k = 0`). The four multi-failure submissions had
`k ∈ {25, 10, 5, 5}` and `Y = 0` on every instance. Machine record: `pilot_report.json`
`"gate_pass": false`, `"decision": "INFEASIBLE — stop"`.

### Stage 2 — v0.2: the comparison ran, but `C` was a function of `k`

Frozen rule (`v02/PROTOCOL_V02.md` §6, lines 80–85): Positive if the 95 % CI lower bound for
`Δ = L_A − L_B` exceeds `δ = 0.01` nats and the real-family `Δ` beats the 95th percentile of 200
relabelings; Negative if the CI upper bound is below `δ`.

Executed (`v02/REPORT_V02.md` §2):

| Quantity | Value |
|---|---:|
| `Δ` | **−2.639 × 10⁻⁹ nats** |
| 95 % CI | **[−1.519 × 10⁻⁶, +1.583 × 10⁻⁶]** |
| `δ` | 0.01 nats |
| Instances / eligible pairs | 40 / 1200 |
| Outcome | **NEGATIVE** |

The identification audit then removed the result's scientific content (`v02/INTERPRETABILITY_AUDIT_2026-10-14.md`
§2–§4):

- "Every row satisfies C = 5/k exactly (90/90, max |C − 5/k| = 0.000e+00), and within each k the
  number of distinct C values is 1 (within-k variance 0.0 at all four levels)."
- Four cells only: `(k,C) = (5,1.0) 27 rows; (10,0.5) 9; (20,0.25) 9; (25,0.2) 45`.
- Design matrix 4×5, rank 4; "appending the C column leaves the rank at 4, and the least-squares
  residual of C on the basis is 1.100e-13."
- Consequence: "the experiment never contrasts equal-k different-C pairs"; the near-zero `Δ` is
  "uninformative about independently varying concentration."

Structural facts (same audit, plus `v02/FINDINGS_LEDGER_2026-10-19.md` F1/F4): 1200 pairs are
400 distinct (body, instance) cells × 3 byte-identical replicas; **10 distinct eligible base
bodies**; every eligible row has a fully failed family, which is what forces `C = 5/k`.

### Stage 3 — the corpus audit that named the failure mode

`v02/FINDINGS_LEDGER_2026-10-19.md` line 47 states the identity with its scope: "C = 5/k exactly on
the eligible realized support … eligible support only (k in {5,10,20,25}). The identity is
conditional on the failure pattern: guaranteed for k >= 25, not for all k >= 2, and not universal."

That distinction matters: the alias is a property of the **eligibility rule plus the 5-probe family
cap**, not a law about concentration. It is therefore avoidable in principle — and every later
design tried to avoid it and failed for a different reason.

### Stage 4 — engineered-study: construction failure, then a synthetic null

`engineered-study/08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md` line 3:

> "**Status:** NEGATIVE - no separation demonstrated in the bounded audit"

with "Gate 1: CLOSED for this operationalization", "Study solvers generated: 0", "Generator
prompts/calls: 0", "Power simulation run: no". The audit asked whether at least two genuinely
different, non-lookup defect mechanisms could produce matched diagnostic profiles at more than one
concentration level while leaving held-out performance measurable; it could not construct them.

`engineered-study/00_CLAIM.md` records H1a and its retirement note (the earlier H2 "hidden
structure" claim retired after a cost proxy recovered the boundary).

`engineered-study/09_CONCENTRATION_MATHEMATICAL_SPEC.md` then established four mathematical facts
(§9, lines 232–237): multiple `C` at `k=5` are arithmetically possible; `C` loses information
present in the full vector `F`; family sizes change the domain-weighted score at identical `(k,C)`;
and "without a constrained diagnostic-to-evaluation relationship, diagnostic failures do not
determine evaluation outcomes." It explicitly does **not** validate the design: "They do not
establish that concentration predicts real solver performance" (line 239).

The three-world simulation (`engineered-study/math/results/three_world/11_THREE_WORLD_SIM_RESULT.md`)
is the only executed analysis in the whole programme where the identification requirement was met
in the data:

| W1 quantity | Value |
|---|---:|
| Eligible cases / k=0 | 2 499 949 / 51 |
| Fixed-k carrier overlap | cases 2 365 022, strata 49 834, residualized C variance 14 737.3 |
| C gain, domain score | **+1.961346752 × 10⁻⁶**, 95 % **[−1.242089975 × 10⁻⁶, +7.581285807 × 10⁻⁶]** |
| C gain, equal-family | +1.914362824 × 10⁻⁶, 95 % [−1.833270363 × 10⁻⁶, +8.988738209 × 10⁻⁶] |
| Full vector vs C | +0.000790, 95 % [+0.000692, +0.000886] |
| Criterion outcome | **FAIL** ("DOES NOT SURVIVE") |

Line 5 is explicit: "**Frozen outcome: W1 FAILED.** … This report describes a weak positive estimate
but does not claim that the frozen simulation demonstrated predictive value for `C`." W2 has zero
overlap (C constant on eligible support); W3 is a null check with gain `−0.000001`. The report's own
scope line: "Synthetic-data simulation only. Results show implications of the declared assumptions;
they are not evidence about real solvers."

### Stage 5 — natural feasibility: the generators never produced the cells

| Run | Bodies | Eligible `k ≥ 2` | Same-k, different-C |
|---|---:|---:|---:|
| MIMO (`natural-feasibility-pilot/FEASIBILITY_REPORT.md`) | 0 (0/100 attempts) | 0 | 0 |
| Codex SSSP | 10 complete | 0 (all `k=0`, 20/20 correct) | 0 |
| Gemini SSSP | 25 complete | 0 (all `k=0`) | 0 |
| Gemini expression (`next-task/06`) | 19 executed | 19 | **0** — verdict `REPEATED_K_BUT_NO_C_SEPARATION` |

`next-task/10_OFFLINE_POWER_SIMULATION_REPORT_2026-10-22.md` was then **invalidated for operational
planning** by arithmetic: it assumed `C_high = 1.0` at `k = 6, 12, 24`, but with five probes per
family `C_max(k) = min(1, 5/k)`, so those cells cannot exist (`next-task/11_CLOSURE_RECORD_2026-10-22.md`
lines 74–80). `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` line 87: "All eligible support has
`C=5/k` exactly. There are **zero** same-`k`, different-`C` pairs."

### Stage 6 — the archive-wide stop

`natural-feasibility-pilot/offline-inventory-2026-10-25/INVENTORY_REPORT_2026-10-25.md`:

> "No existing retained dataset contains an eligible same-`k`, different-`C` comparison with
> independent solver bodies."

Total protocol-eligible `k ≥ 2` bodies across the whole archive: **14** (4 from v0.1, 10 base bodies
from v0.2, 0 from the expression pilot). Disposition: **`INFEASIBLE_WITH_CURRENT_DATA`**, triggered
by "zero eligible same-`k`, different-`C` pairs in every audited dataset."

### Stage 7 — H3: engineering, not evidence

The H3 footprint line (V2–V9, 2026-10-26 → 11-01) is a containment/instrumentation programme. V8's
freeze is pre-candidate (0 candidates, 0 model calls); V9 is unfrozen and reports Sandbox rendezvous
failed, isolation partial, verdict/support-cell layer not implemented, generation and evaluation
blocked. The only substantive screens found 0 eligible bodies from 9 unique solvers (Copilot-Auto)
and 1 eligible body (`k=9`, `C=4/9`, 21/30 correct; 0 supported cells because `m_min = 4`). No H3
result bears on concentration.

---

## 4. The four independent ways the design failed — and why they are different

It is tempting to read eight stages as eight failures of one idea. They are four distinct failure
mechanisms, and only one of them is about the hypothesis itself.

| Mechanism | Stage | What was missing | Remedy it would require |
|---|---|---|---|
| **A. Yield** | v0.1 | enough eligible multi-failure submissions (4/20 vs ≥15), and any `Y=1` case | a task where solvers actually fail partially |
| **B. Aliasing / rank** | v0.2, W2 | within-`k` variation in `C` | abandon the "fully failed family" eligibility rule |
| **C. Attainability** | next-task power, LC518 capacity | cells that exist under the 5-probe cap | `k` below the cap threshold, e.g. `k ≤ 24` in the six-family scheme |
| **D. Construction / separability** | Option B, LC518 v0.21 | mechanisms that differ without changing the carrier family | engineered variants with controlled mechanism assignment |

### The arithmetic that ties B and C together

With six families of five probes (`00_CLAIM.md` line 46):

- At `k ≥ 25`, the pigeonhole forces `max_j f_ij = 5`, hence `C = 5/k` **exactly**. Every `k = 25`
  observation carries no concentration information beyond `k`.
- At `k = 24`, both `C = 4/24` and `5/24` are feasible.
- The last contrastable `k` under three instrument configurations is 24 (six families × 5), 53
  (canonical-weighted 8 strata) and 56 (record-weighted), by exhaustive enumeration
  (`LC518_POPULATION_MODEL_AUDIT_2026-11-10.md` §1).

v0.2's eligible support was `k ∈ {5, 10, 20, 25}` **with a fully failed family in every row**, so
`C = 5/k` throughout. That is a design choice (eligibility conditioned on a fully failed family),
not a mathematical inevitability. But the natural generators never produced the alternative: in
every natural run, solvers were either perfect (`k=0`) or failed one family overwhelmingly.

### Mechanism D is the one that is currently blocking

`LC518_POPULATION_MODEL_AUDIT_2026-11-10.md` §2 F1 is the sharpest finding in the repository on
this point. The frozen M1 support floor (rev 2.6 §5.2) is **within-parent**:

> "at least three distinct parent groups contribute within-parent C_D variation in that same exact
> (k_fail, k_unresolved) cell. A parent group contributes only if at least two of its five matched
> versions fall in that exact cell and have different C_D values."

The proposed GPT framework instead defines the cell as `(m, z, k_fail, k_unresolved)` and support
as ≥3 distinct parents in the cell. Under a one-mechanism-per-variant labelling, two versions of the
same parent have different `m`, so they land in different cells by construction. The audit's
conclusion: "Under GPT's cell definition, the frozen §5.2 within-parent contribution is empty by
construction and the simulation cannot evaluate the frozen floor at all."

In other words, the current LC518 support rule and the current population model are **mutually
incompatible**, and the mismatch is not clerical — it determines whether any support cell can exist.

---

## 5. What is established, and what is not

### Established by executed records

1. v0.1 terminated INFEASIBLE at the yield gate (4/20 vs ≥15 on all three instances).
2. v0.2's frozen comparison returned `Δ = −2.639 × 10⁻⁹`, CI `[−1.519 × 10⁻⁶, +1.583 × 10⁻⁶]`,
   NEGATIVE — computationally reproducible.
3. On v0.2's eligible support, `C = 5/k` exactly in 1200/1200 rows; within-`k` C-variance is 0;
   the design matrix rank is unchanged by adding `C`; there are 10 distinct eligible base bodies.
4. No retained natural dataset contains a same-`k`, different-`C` pair; 14 protocol-eligible `k≥2`
   bodies exist in total.
5. The parenthesis-task operationalization failed construction: Gate 1 closed with 0 solvers and
   0 generator calls.
6. In the one synthetic dataset with real fixed-`k` overlap (2.5M cases), the C-gain interval
   covered zero and the full vector beat `C`.
7. LC518 produced 64 diagnostic and 80 held-out bank records (78 distinct canonical inputs, 78
   oracle answers) and **0 of 150 solver bodies**.

### Not established — and must not be claimed

1. That concentration has no predictive value. No record supports this.
2. That the hypothesis is false, refuted, or falsified. v0.2's NEGATIVE is explicitly
   non-identifying; W1 is synthetic and criterion-failing, not refuting.
3. That any study tested `C` beyond `k` **and** `Z`. None did.
4. That the LC518 population exists, is buildable, or has a support pass. The M1-si rule has never
   been evaluated on a produced manifest (see §6).
5. That the 150-variant design is adopted. v0.21 records "the 90-version and 150-variant counts are
   not binding".

---

## 6. LC518 — the current route, and why it still cannot answer the question

Current state from the records (`README.md` §3; roadmap audit §4.2–§4.5, §6):

| Item | State |
|---|---|
| Diagnostic bank | 64 records, generated, structurally verified |
| Held-out bank | 80 rows / 78 canonical inputs / 78 oracle integers; **publicly exposed**, development-only |
| Solver bodies | **0 / 150** |
| Candidate outcomes | none |
| Predictive analyses | none |
| Frozen analysis spec v1.0 | E3 baseline `k_fail`, `k_unresolved`, family; **no `C_D` arm** |
| Rev 2.6 analysis spec | review-only draft proposing a `C_D` arm; not design of record |
| B1 plan v1.7 | accepted/frozen as **symbolic only**; not an execution authorization |
| Computational plan v1.0 | draft; not accepted |
| Population design v0.21 | design-only draft; no parent selected, no mechanism assigned |
| M1-si support | rule defined; **no produced manifest, zero audits executed, no demonstrated pass** |
| Mutation allocation (Nov 6) | **not established**; 28+2 roster unproven |
| Custodian / joint consent | absent / open |
| Trigger-(i) interpretation | unratified |

Two structural consequences:

1. **The frozen design cannot test `C` at all.** `lc518-150/glm-handoff/ANALYSIS_SPEC.md` v1.0's E3
   comparison has no concentration feature. Only the review draft rev 2.6 adds one. So even a
   completed LC518 run under the frozen spec would answer a `k`/`k_unresolved`/family question, not
   the concentration question.
2. **The proposed design has no support cells under its own cell definition** (§4, mechanism D),
   and the mutation allocation that would assign mechanisms to parents does not exist in any
   audited record.

The M1-si validator built on 2026-11-18 (`manifest-validator/`, 169 checks, 0 failures) implements
the §4 structural rule with corrections A–I. It is an **engineering** artifact: it can accept or
reject a manifest. It does not create a population, and no manifest has been produced for it to
check. It therefore does not move the scientific status.

---

## 7. Repository and GitHub state of the evidence

| Fact | Value |
|---|---|
| Local `master` | `33dca9b` — identical to `origin/master` (0 ahead, 0 behind) |
| Remote branches | **62** |
| Local branches | 19; **6 exist only locally** — `lc518-containment/master`, `lc518-containment/foued2-patch-1`, `lc518-containment/recovery-2026-11-02`, `review/lc518-containment-r3/r4/r5` (sanitized containment repacks, deliberately unpushed) |
| Tags | 10 (`v0.1-freeze`, `v0.2-freeze`, 8 × `h3-footprint-*`) |
| Repository visibility | public (`"private": false`) |
| Merge base of `master` and the research line | `edae42c` |
| Research branch | `research/concentration-math-spec` at `de39291` |

Where the concentration-relevant records actually live:

- **`master`** — v0.1/v0.2 historical closure, `engineered-study/`, `natural-feasibility-pilot/`,
  `next-task/`, `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md`, `FEASIBILITY_CLOSURE_2026-10-25.md`,
  `LC518_POPULATION_MODEL_AUDIT_2026-11-10.md` (local working tree), H3 harnesses.
- **`research/concentration-math-spec`** — validator, design-history register, storage inventory,
  claim audit matrix (5 commits ahead of `8bb2e82`).
- **`docs/scientific-roadmap-audit-2026-11-18`** — the 2026-11-18 synthesis quoted in §2.
- **`audit/c09-count-reconciliation-2026-11-18`** — the held-out bank recount.
- **`gpt/lc518-m1si-audit-2026-11-17`** — mirrored v0.21, GLM/GPT adjudications, M1-si Base64 bundle.
- **`gpt/b1-computational-plan-2026-11-14`** — B1 v1.7 drafts and population-design history.
- **`review/concentration-formulation-2026-10-25`** — the construct-validity work.
- **`foued2-patch-1`** — the public 12-file publication ZIP containing the exposed held-out bank.

Local/GitHub divergence is therefore not a loss of evidence: the remote holds the newer design
records, and the local clone is missing several of them (including v0.21 itself, which exists on
`gpt/lc518-m1si-audit-2026-11-17` as blob `8af908f6b0ad4cd060194a0a63f4914939f07756`).

---

## 8. Exact open items

1. **v0.21 is not in the local checkout.** It exists only on the remote branch named above. No
   conformance table against it can be produced locally until it is read in full.
2. **No parent roster and no manifest.** M1-si cannot be evaluated; nothing can be said about
   support.
3. **No custodian, no joint-consent record** for any protected-confirmatory route.
4. **Trigger-(i) interpretation unratified;** B1 v1.7 compatibility with a new population undecided.
5. **The Nov 6 mutation allocation remains unestablished** — do not reconstruct it from totals.
6. **Two `C` estimands remain unbridged:** v0.2 tested `C` beyond `k` alone and failed to identify it;
   the programme target (`C` beyond `k` and `Z`) has never been executed.

---

## 9. Source files relied on

| File | Lines used |
|---|---|
| `README.md` | 1–99 |
| `PROTOCOL.md` | 206–209 |
| `pilot/PILOT_REPORT.md` | 8–24 |
| `v02/PROTOCOL_V02.md` | 65–85 |
| `v02/REPORT_V02.md` | 36–58 |
| `v02/INTERPRETABILITY_AUDIT_2026-10-14.md` | 35–78 |
| `v02/FINDINGS_LEDGER_2026-10-19.md` | 47, 50, 180 |
| `engineered-study/00_CLAIM.md` | 7–13, 46 |
| `engineered-study/08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md` | 3, 28–32 |
| `engineered-study/09_CONCENTRATION_MATHEMATICAL_SPEC.md` | 15, 40–44, 167–180, 230–239 |
| `engineered-study/math/results/three_world/11_THREE_WORLD_SIM_RESULT.md` | 3–12, 16–44 |
| `engineered-study/math/results/three_world/12_overlap_by_k_c.md` | 1–20 |
| `natural-feasibility-pilot/FEASIBILITY_REPORT.md` | 5, 20–26 |
| `natural-feasibility-pilot/offline-inventory-2026-10-25/INVENTORY_REPORT_2026-10-25.md` | 8, 12–24, 222–228 |
| `next-task/06_EXPRESSION_PILOT_RESULT_2026-10-22.md` | 13–24, 58–87 |
| `next-task/10_OFFLINE_POWER_SIMULATION_REPORT_2026-10-22.md` | 5–11, 17, 216–221 |
| `next-task/11_CLOSURE_RECORD_2026-10-22.md` | 31–40, 74–80, 285–287 |
| `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` | 46, 67, 87, 104, 114 |
| `LC518_POPULATION_MODEL_AUDIT_2026-11-10.md` | 1, §1–§2 F1 |
| `docs/SCIENTIFIC_ROADMAP_AUDIT_2026-11-18.md` (remote) | 3.3, 4.1–4.7, 5, 6 |

---

# Addendum — remote-only records (branch sweep)

The local checkout does not contain the 2026-11 design line. Seven remote refs were read with
`git show`/`git grep`; nothing was checked out. Three of them change what can be said about the
current state, and none contradicts §0–§8.

## 10. The branch named `lc518-m1si-audit-2026-11-17` contains no audit

This is the most important correction to any prior summary, including my own.

The branch adds 72 files under `lc518-150/`, but `lc518-150/engineering/` holds only:

```
BUILD_BUNDLE.ps1
README.md
m1si_audit_bundle.b64.001 … .005
```

The auditor itself (`m1si_audit.py`, `m1si_manifest.schema.json`, `tests/test_lc518_m1si_audit.py`)
exists **only inside the base64 ZIP**, not as tracked source. And no diagnostic manifest exists
anywhere on the branch — `git ls-tree -r` for "manifest" returns only unrelated rlc0 hashes.

So the honest reporting of M1-si is:

| Quantity | Value |
|---|---|
| Audits executed | **0** |
| Manifests produced | **0** |
| Qualifying parents observed | none (nothing to observe) |
| Qualifying cells observed | 0 |
| Threshold, by contrast, is concrete | ≥3 distinct parents, each contributing ≥2 of its own variants to one exact cell, with ≥2 distinct exact `C_D` inside each parent → **≥6 variants in one cell** |
| Predeclared failure string | "M1-si NOT REALIZED / MATCHED-SUPPORT DESIGN FAILURE" |

The README's own boundary: "This is an engineering utility, not protocol adoption or execution
authorization. It audits a manifest that has already been produced… The bundled tests are synthetic
software tests only."

The validator I built on 2026-11-18 is the same kind of object, one level more testable: it can
decide a manifest, but there is still no manifest.

## 11. v0.21 admits a second confound, beyond family and mechanism

v0.21 §0 item 3 states it directly:

> "Option A, which would condition the primary model on a(v), is not adopted. … The current M1-si
> structure varies a and C_D together; it does not guarantee C_D variation while a is held fixed."

So a **passed** M1-si audit would establish variation in `C_D` across variants that differ in
realization setting `a(v)` — but it would not separate `C` from the realization-setting identity.
That is a third aliasing layer, after "family/carrier" (Gate 1) and "failure count" (v0.2). v0.21 is
explicit that this is a design limitation, not a defect that a support pass would cure.

The same document pre-commits the interpretation of a shortfall (line ~1235): "A realized support
shortfall is a design-feasibility result, not evidence that concentration has no predictive value."

## 12. B1 as adopted is stricter than "`k` and `Z`"

`lc518-150/review-v1.2/AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md` §1:

> "**Claim B1:** Among singly mutated solver versions, does the concentration of definite diagnostic
> failures across the eight input strata carry information about held-out correctness beyond total
> definite failures and unresolved diagnostic outcomes, conditional on both the identity of the
> individual mutation mechanism and the parent algorithm family?"

Support cell is `(individual mutation mechanism, parent family Z, k_fail, k_unresolved)`; qualifying
requires `k_fail ≥ 2`, ≥3 distinct parent groups, ≥2 distinct observed `C_D`, and **no pooling**.
Failure is to be reported as:

> "**NON-IDENTIFICATION / INSUFFICIENT WITHIN-MECHANISM-AND-WITHIN-FAMILY SUPPORT**" … "It is not
> a null concentration effect and does not authorize a switch to Claim A."

Two consequences the general phrase "`C` beyond `k` and `Z`" hides:

- **K5 is excluded outright.** "The frozen parent roster contains only two K5 parent groups. It
  therefore cannot meet the three-parent minimum in a K5 family-cell."
- The schedule itself is thin: "28 unordered pair types across 30 parent assignments: 26 pair types
  occur once and two occur twice."

## 13. The occupancy arithmetic that no design has yet beaten

From `POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.21.md` and
`GPT_ADJUDICATION_S25_GAP_ANALYSIS_2026-11-16.md`:

- Capacity is 8 slots in 8 strata; attainable numerator envelope `M(k,ℓ) = {⌈k/8⌉, …, min(k, 8)}`.
- "for k=2, the only values are C_D in {1/2, 1}"; for `k > 8` the maximum numerator is 8, not `k`.
- "every two different exact C_D values within this cell differ by at least 1/k."

From `engineered-study/06_OPTION_B_IDENTIFICATION_AUDIT.md`:

- `150 / 36 = 4.17` variants per mechanism-profile cell.
- `150 / (36 × 3) = 1.39` variants per mechanism-profile-generator cell — **below 1.5**, i.e. most
  cells cannot hold two variants at all.
- The Option B profile ladder `(5,0) → (4,1) → (3,2)` changes the leading family's failure count
  5 → 4 → 3, so "C is therefore collinear with carrier count within a pair, even though carrier
  identity is held fixed."

That is the same disease as v0.2, one level down: the variation that `C` would need is consumed by
the coordinate that defines the cell.

## 14. Power: no configuration reaches the target

`engineered-study/results/power_analysis.json`, k=5, 120 high-C / 30 low-C slots:

| Residual SD | Power at `δ = 0.10` |
|---:|---:|
| 0.20 | **0.78565** (below 0.80) |
| 0.25 | **0.62135** |

Recorded identification failures: "the six C=1 targets use six different carrier families, so C is
not separated from carrier family"; "there is no within-carrier fixed-k contrast between high and
low C."

And the adjudication on the one number everyone quotes: "the support floor P >= 3 is not an
operating-parent-count justification, and no confirmatory operating count can be inferred from the
current record."

## 15. The one sentence that explains the whole history

`review/concentration-formulation-2026-10-25:concentration-formulation/02_RESEARCH_FORMULATION_NOTE_2026-10-25.md`
§9:

> "`C` has tracked a hidden variable in each earlier setting: algorithm type in the old Doctor
> project, failure count in v0.2, and family size and defect identity in the engineered Gate 1 work."

That is the audit's central finding stated by the project itself, before any of my reading. The
history is not eight unrelated failures; it is one construct repeatedly taking the value of whatever
coordinate the design failed to hold fixed.

The same note supplies the mathematical ceiling: "`C` has no variation at `k = 1` and at every `k`
from 25 through 30; at `k = 0`, `C` is undefined."

## 16. What the remote sweep adds to the evidence table

| Ref | Content | Bearing on `C` |
|---|---|---|
| `gpt/lc518-m1si-audit-2026-11-17` | v0.21, GLM/GPT adjudications, M1-si **tooling only** | support never audited; `a(v)` confound admitted |
| `gpt/lc518-claim-b1-primary-2026-11-05` | exact B1 wording, support rules, mechanical dry runs | B1 is within-mechanism × within-family; K5 excluded |
| `gpt/b1-computational-plan-2026-11-14` | plan v0.1–v1.0 | rank check: failed variation ⇒ "unavailability, never row or cell removal" |
| `review/concentration-formulation-2026-10-25` | formulation note, Gate 1 report, Option B audit, power | the "hidden variable" sentence; 0.78565 power |
| `glm/h3-feasibility-evidence-2026-10-29` | construct-validity assessment, closure, GLM screen | 1 eligible body of 12; 0 supported cells |
| `review/glm-h3-evidence-audit-2026-10-29` | independent audit + erratum | `k=9`, `C=4/9`, 21/30 confirmed; classifier defect |
| `transfer-artifacts` | one zip + one bundle | no scientific content |

## 17. Quality defects found while reading the remote records

These do not change any `C` result, but they bound how much "verified" can mean here.

1. **Classifier defect.** The independent GLM audit found the in-repo algorithm classifier labels
   `request-03` as `floyd` when it is a weighted first-discovery FIFO traversal — "a **repository
   classifier defect**, not a transcription error by GLM." Its own first diagnosis (hop-count BFS)
   was then withdrawn by erratum: hop-count BFS produces 16 failures, not 9. Measured values
   (`k=9`, `C=4/9`, `A:4 I:1 S:4`, 21/30) were confirmed unchanged.
   Consequence: **concentration-cell semantics in that codebase are classifier-dependent**, and a
   `C` value is only as good as the family assignment that produced it.
2. **Provenance mismatch.** The S25 gap adjudication records that the supplied GLM handoff "is not
   byte-verified as the artifact whose hash GLM reported" (supplied `3b26c34e…` vs reported
   `9cab6697…`), plus a document dated 2026-11-17 but adjudicated 2026-11-16.
3. **Dry-run vs generation.** `REPORT_C9_DRYRUN.md` records "Cross-bank canonical disjointness
   (item 8) | **FAILS: 1 collision**". The later generation run manifest records `item8_status =
   PASS`. The defect was found and fixed between dry run and generation — but the dry-run report
   should not be read as describing the final banks.

## 18. Addendum conclusion

Nothing in the seven remote refs contradicts §0. Five of them restate the same negative-epistemic
position in their own words ("not demonstrated … not established that it lacks"; "neither … nor";
"design-feasibility result, not evidence that concentration has no predictive value"). Two of them
add facts that make the current route harder, not easier:

- M1-si has **never been audited** — the branch is a tool, not a result.
- v0.21 already concedes that `C_D` varies together with `a(v)`, so even success would not isolate
  `C`.
- The occupancy arithmetic (`4.17` and `1.39` variants per cell) shows the 150-variant budget cannot
  populate the cells the support rule requires.
- The only power calculation on record misses 0.80 (`0.78565`) at the optimistic SD and collapses
  to `0.62135` at the realistic one.

The repository's own sentence — "`C` has tracked a hidden variable in each earlier setting" — is the
accurate summary of what happened to the concentration theory.

