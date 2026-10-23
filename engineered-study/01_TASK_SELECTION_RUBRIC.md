# Task selection rubric

Status: applied once, before bank construction. Criterion 1 is a gate.

| # | Criterion | Requirement |
| --- | --- | --- |
| 1 | Deterministic oracle | The host must compute the exact expected answer independently of any candidate solver. |
| 2 | Independent check | A second, different method must agree on every declared-domain input. |
| 3 | Exact answer contract | The answer must be a native exact integer, not a float, boolean, or tolerance match. |
| 4 | Complete finite domain | The declared domain must be finite and small enough to enumerate fully. |
| 5 | Exhaustive, disjoint split | Diagnostic and evaluation inputs must partition the domain with no exact-input overlap. |
| 6 | Six structural families | At least five inputs per family, a meaningful concentration range, and evaluation coverage in every family. |
| 7 | Fixed-`k`, different-`C` comparison | At least two attainable concentration values at a fixed positive failure count. |
| 8 | Plausible hand-built controls | The researcher must be able to construct family-localized failures without injecting exact evaluation inputs. |
| 9 | `S` not determined by `k` | Correctness at fixed `k` must be able to vary across profiles. |
| 10 | Bounded execution | One input per process must fit the strict Sandbox timeout without network access. |
| 11 | Claim separation | A result must not depend on the retired hidden-structure claim, and outside-domain behaviour cannot be required. |

## Application

| Criterion | Result |
| --- | --- |
| 1. Deterministic oracle | pass |
| 2. Independent check | pass; all 128 inputs |
| 3. Exact answer contract | pass |
| 4. Complete finite domain | pass; all 128 length-7 strings |
| 5. Exhaustive, disjoint split | pass; 30 + 98 = 128 |
| 6. Six structural families | pass; 8–36 inputs per family, 3–31 evaluation inputs per family |
| 7. Fixed-`k`, different-`C` | pass structurally; `k=5` admits `C=1.0` and `C=0.2` |
| 8. Plausible controls | pass with limitation; controls are deliberately family-specific and not evidence |
| 9. `S` not determined by `k` | pass as a possibility; calibration confirms variation |
| 10. Bounded execution | pass; one input per process under strict Sandbox |
| 11. Claim separation | pass; declared domain only |

Criterion 7 is satisfied as a design possibility, not as evidence about solvers.
Criterion 8 is the weakest: the controls prove the pipeline and expose profile
mechanics, but do not sample the intended study population.
