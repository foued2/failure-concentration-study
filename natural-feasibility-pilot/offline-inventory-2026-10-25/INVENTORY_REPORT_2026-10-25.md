# Offline inventory of existing solver records

**Date:** 2026-10-25
**Protocol:** `engineered-study/math/15_NATURAL_SOLVER_FEASIBILITY_PROTOCOL_2026-10-24.md`
(protocol SHA-256 `8f0a24fe9c387733ee28ef345d527be048c15a6a57ad634ef9f0997feff2fed4`)
**Mode:** offline audit only. No solver code was imported or executed, no model/API call was made,
and no bank, protocol, frozen result, or solver record was modified.
**Disposition:** **`INFEASIBLE_WITH_CURRENT_DATA`**

## 1. Answer

No existing retained dataset contains an eligible same-`k`, different-`C` comparison with
independent solver bodies.

- The SSSP runs have no eligible `k >= 2` bodies at all: every completed body has `k = 0`.
- The expression pilot has `k >= 2` bodies, but each repeated-`k` group has only one `C` level.
- The v0.1 and v0.2 SSSP packs have several `C` values, but only across different `k` values;
  on the audited support `C = 5/k` exactly, so there is no within-`k` `C` variation.
- The v0.2 pack is 40 base bodies replicated three times, not 120 independent bodies.

Under the frozen stop rule this is criterion 2: zero eligible same-`k`, different-`C` pairs in
every prespecified family. It is not criterion 3 or 4.

## 2. What counts as a unit

The unit is one solver body with a documented generation lineage. Exact duplicates and replicas
were collapsed. Independence was not inferred from differing filenames or raw file hashes.

A body is eligible only if it has a parseable artifact, complete diagnostic measurements, a
correctness outcome on a separate evaluation suite, and `k >= 2`. `C` is undefined at `k = 0`.

## 3. Family rationale used for the audit

This rationale comes from the frozen instrument definitions. No family was created, merged, or
redefined by this audit, and no family was selected because it improved a `C` contrast.

**SSSP (v0.1, v0.2, Codex, Gemini).** The six diagnostic families are task properties assigned
when each probe input is constructed, independently of solver outcomes:

| Family | Meaning |
| --- | --- |
| F1 | target unreachable |
| F2 | zero-weight edge present |
| F3 | parallel edges present |
| F4 | self-loop present |
| F5 | at least two minimum paths (tie multiplicity) |
| F6 | weight plateau (at least three edges share a weight) |

Each family has five diagnostic probes. A failure is any recorded diagnostic failure for a
probe in that family. `k = sum(F)` and `C = max(F) / k` for `k > 0`.

**Expression (Gemini expression pilot).** The six diagnostic families are input classes assigned
when the bank was built, independently of solver outcomes:

| Family | Meaning |
| --- | --- |
| F1 | operator precedence |
| F2 | left associativity |
| F3 | parentheses |
| F4 | unary minus |
| F5 | multi-digit tokenization |
| F6 | whitespace |

Each family has five diagnostic probes. The evaluation bank has five separate inputs per family
and is disjoint from the diagnostic bank.

## 4. Inventory by dataset

### 4.1 v0.1 MIMO SSSP pilot

Source: `pilot/pilot_report.json`, `pilot/PILOT_REPORT.md`, `specs/generator_spec.json`.
Generator: `opencode/mimo-v2.6-flash-free`, 20 single-shot submissions from one session.

| `k` | `C` | Body-instance rows | Distinct bodies |
| ---: | ---: | ---: | ---: |
| 0 | 0.0 | 48 | 16 |
| 5 | 1.0 | 6 | 2 |
| 10 | 0.5 | 3 | 1 |
| 25 | 0.2 | 3 | 1 |

Eligible bodies with `k >= 2`: **4**, contributing **12 eligible body-instance rows** (four bodies
on three instances). Same-`k`, different-`C` pairs: **0**. The two `k = 5` bodies both have
`C = 1.0`. The pilot was already terminal `INFEASIBLE` at its frozen yield gate.

### 4.2 v0.2 MIMO SSSP pack

Source: `v02/pilot_v02/pilot_v02_report.json`, `v02/FREEZE_V02.md`,
`v02/INTERPRETABILITY_AUDIT_2026-10-14.md`, `generation_v02/pack/`.

Pack size: 120 files. After stripping the `Submission n (base body x, replica y)` header:
**40 unique base bodies, exactly 3 replicas each (80 replica files beyond the first)**.
The raw files are all hash-distinct, but they are not independent units.

Audited pilot support (90 eligible body-instance rows):

| `k` | `C` | Body-instance rows | Body files | Base bodies |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 1.0 | 27 | 9 | 3 |
| 10 | 0.5 | 9 | 3 | 1 |
| 20 | 0.25 | 9 | 3 | 1 |
| 25 | 0.2 | 45 | 15 | 5 |

Eligible base bodies with `k >= 2`: **10**. Same-`k`, different-`C` pairs: **0**.
All 90 rows satisfy `C = 5/k` exactly; each `k` has exactly one `C` level.

The confirmatory result reports 1,200 eligible pairs, but only as aggregates. Per-row `(k, C)`
was not persisted, so those rows cannot be independently audited at body level. They were
therefore not used to create any qualifying pair.

### 4.3 Codex SSSP, 100-request run

Source: `natural-feasibility-pilot/natural-pilot-20261021T123319Z/PILOT_RESULTS.json`.
Generator: Codex CLI / `gpt-6-luna`.

- Generation requests: 100
- Model-written outputs: 39; generation failures: 61
- Distinct canonical bodies: 15
- Bodies with complete diagnostic and evaluation records: 10
- All 10 complete bodies: `k = 0`, `C = 0`, 20/20 evaluation correct
- Eligible `k >= 2` bodies: **0**
- Same-`k`, different-`C` pairs: **0**

The run halted on a provider usage limit. It is an infrastructure interruption, not a
scientific negative.

### 4.4 Gemini SSSP, 100-request run

Source: `natural-feasibility-pilot/natural-pilot-gemini-20261021T172103Z/PILOT_RESULTS.json`,
`INTEGRITY.json`, `CLOSURE_VALIDATION.json`.
Generator: Google Gemini API / `gemini-3.5-flash-lite`.

- Generation requests: 100; generation failures: 0
- Distinct canonical bodies: 25
- Complete bodies: 25
- All 25 bodies: `k = 0`, `C = 0`, 20/20 evaluation correct
- Eligible `k >= 2` bodies: **0**
- Same-`k`, different-`C` pairs: **0**

The run is closed as `FEASIBILITY_NOT_DEMONSTRATED_WITHIN_CAP`.

### 4.5 Gemini expression pilot

Source: `next-task/expression-pilot-gemini-20261022T163536Z/PILOT_RESULTS.json`,
`next-task/06_EXPRESSION_PILOT_RESULT_2026-10-22.md`,
`next-task/07_EXPRESSION_PILOT_AUDIT_2026-10-22.md`.

| `k` | `C` | Bodies | Evaluation correct per body |
| ---: | ---: | ---: | --- |
| 0 | 0.0 | 6 | 30/30 each |
| 2 | 1.0 | 9 | 28/30 each |
| 7 | 5/7 | 1 | 23/30 |
| 30 | 1/6 | 3 | 0/30 each |

Eligible bodies with `k >= 2`: **13**. Same-`k`, different-`C` pairs: **0**.
`k = 2` has only `C = 1.0`; `k = 30` has only `C = 1/6`; `k = 7` is a singleton.

The existing post-hoc audit also found that the nine `k = 2` bodies share one whitespace bug and
the three `k = 30` bodies are uniform crashes. Source diversity therefore overstates behavioral
diversity in this pilot.

## 5. Exclusions

| Reason | Count / extent |
| --- | --- |
| `k < 2` | 16 v0.1 bodies; 10 Codex bodies; 25 Gemini SSSP bodies; 6 expression bodies |
| Markedly invalid artifact | 2 expression syntax rejects (not executed) |
| Replica / non-independent files | 80 v0.2 files beyond the first copy of each base body |
| No per-row auditable support | 1,200 v0.2 confirmatory pairs (aggregate-only persistence) |
| Constructed, not natural | 6 engineered-study controls; not counted |
| Synthetic simulation | three-world outputs; not solver records |
| Missing lineage | none in the retained natural runs; v0.2 lineage is documented as a frozen pack |
| Overlapping evaluation inputs | none reported for the retained banks; exact evaluation/diagnostic overlap checks passed |
| Zero generated bodies | 1-request Codex follow-up; no units |

## 6. Held-out evaluation checks

**SSSP runs.** Diagnostic and evaluation suites are separate (30 diagnostic probes; 20 hidden
evaluation inputs in the natural runs). The retained records document zero exact
diagnostic/evaluation overlap. Expected values and correctness are host-side. The v0.2 audit
directly checked that the probe suite is seed-independent and that the hidden suite was not used
to select the pack.

**Expression run.** Diagnostic and evaluation banks each have 30 inputs, five per family, and
their exact expression strings are disjoint. Expected values are host-side and were not in the
guest payload. The evaluation outcomes were not used to select or replace bodies.

**Caveat common to all natural runs.** The guest could read other inputs mounted in its suite
session. The source screen was a best-effort policy, not a secure blinding boundary. This does
not alter the observed support, but it bounds any future claim of genuine blinding.

## 7. Stop-rule application

| Rule | Result |
| --- | --- |
| 1. `BLOCKED_DATA_INTEGRITY` | Not triggered for the retained runs. Provenance, family mapping, and evaluation separation are documented and hash-checked. The v0.2 confirmatory rows are aggregate-only, so they were excluded from the auditable support rather than inferred. |
| 2. `INFEASIBLE_WITH_CURRENT_DATA` | **Triggered.** Zero eligible same-`k`, different-`C` pairs in every audited dataset. |
| 3. `VARIATION_EXISTS_BUT_INSUFFICIENT` | Not reached; no qualifying pair exists. |
| 4. `FEASIBLE_FOR_NEXT_DESIGN_STAGE_ONLY` | Not reached. |

The total number of `k >= 2` units across datasets (27 before behavioral de-duplication) is not
the relevant test. The minimum bar in rule 3 additionally requires at least three family x `k`
strata with two or more `C` levels, each supported by at least two independent units. No such
stratum exists.

## 8. What this does not authorize

This disposition does not authorize:

- another generation run, prompt change, task search, or request-cap extension;
- reopening Gate 1 or the three-world simulation;
- predictive modeling or an effect estimate for `C`;
- treating the v0.2 1,200 confirmatory pairs as auditable body-level observations;
- treating source-distinct expression bodies as independent behavioral samples.

It records only that the current archive cannot supply the required fixed-`k`, different-`C`
comparison. A future design would need a new explicit authorization and a procedure capable of
producing independent partial implementations at the same `k` with different `C`.

## 9. Artifacts

- `inventory_data.json` — full machine-readable inventory, including every input hash and
  replica mapping.
- `inventory_table.csv` — flat table of dataset x `k` x `C` support.
- `collect_inventory.py` — read-only script used to produce the JSON/CSV. It reads metadata and
  hashes only; it never imports or executes solver code.

Key input hashes:

| Input | SHA-256 |
| --- | --- |
| protocol | `8f0a24fe9c387733ee28ef345d527be048c15a6a57ad634ef9f0997feff2fed4` |
| v0.1 pilot report JSON | `0dd24c2822be00ce2125c78a4be2a2b2dae285859d6ffceb7584df3a8aa1e344` |
| v0.2 pilot report JSON | `af1c731f64263f625d4c57dc88e347986138bf595d46a348dfec4d311afc2b75` |
| Codex SSSP results | `b37cf35249f3815ec58f7caa3ba49a211008ce0162a5535de3ecbe81520ed2d7` |
| Codex SSSP report | `662524c6c2e70c7ffd5ccbb6aa01c6e17a1102f46075c74173b9795a086c2605` |
| Gemini SSSP results | `7664e3c08671b284f3b20f3a58155fba4524480dc5d1fe4c8113f985d1d4f47d` |
| Gemini SSSP report | `ad962284d9a5ace08f1f4225849a399993b0bd78cfb4ec562a946c1fef13ccfc` |
| expression results | `8c939cd4b1a4c7ab08bdffdab20340e0525a16e6d8108bfafebaaaa35bd0e1f4` |
| expression report | `ce014c91f3ad630205e3071009ef85cc37a318b641e445084f993fb0d6f5e598` |
| expression diagnostic bank | `ca1ba993ba3bcc6c3c2d011c49cd51e0f5eb32ff8f8cb0421768553c47507847` |
| expression evaluation bank | `e227c24d9bfea7f734b3a249015d33f15d3a2619e62ff5f3a4d8a557e163946d` |

The full hash list, including attempts and protocol files, is in `inventory_data.json`.
