# Confirmatory bank and custody requirement — 2026-11-19

**Status:** requirement specification. Design only. No execution, no custody arrangement created.
**Purpose:** state precisely what the existing held-out bank can and cannot support, and what a future
confirmatory evaluation would require.

---

## 1. The record already says the bank is not sealed

This is not a discovery, and it should stop being reported as one. `B1_ANALYSIS_PLAN_2026-11-14_v1.7.md`
§1 states:

> "The same fixed 78-record bank is used across versions; it is **development data, publicly exposed,
> never sealed**."

and repeats it in §12 as a declared boundary. The roadmap audit reaches the same conclusion
(`SCIENTIFIC_ROADMAP_AUDIT_2026-11-18.md:143`): "The 78-record bank is development material, not a sealed
confirmatory evaluation set."

**Consequence 1:** B1 does not claim sealed-confirmatory status, so the plan is not invalidated by the
exposure. The critique that "the bank cannot serve as a confirmatory test set" is correct and is already
the plan's own position.

**Consequence 2:** any *new* claim of sealed confirmatory evaluation on this bank would contradict the
frozen text. That is the failure mode to guard against, not a defect in the existing plan.

---

## 2. What the exposure evidence actually supports

Three statements, at different strengths. Only the first two are established.

| Statement | Status |
|---|---|
| The bank's inputs and oracle outputs were produced as CI artifacts with published digests (`13210063805`; bundle SHA-256 `08c2b121…`) | **Established** by the erratum's identity table |
| The bank is "publicly exposed" and "never sealed" | **Established** — the plan says so in its own words |
| The artifacts were anonymously downloadable by anyone, or were actually inspected by a solver-building party | **Not established** |

GPT's own correction is adopted: the evidence is consistent with authenticated artifact access, and it
does not prove exploitation. Claude's stronger phrasing ("publicly downloadable") overstates the record.

**Why the weaker statement still suffices:** the plan never relied on secrecy. A bank cannot be
"un-exposed" by narrowing the access claim, so the conclusion is unchanged.

---

## 3. The deeper issue: partition and outcomes share one generation event

This is more consequential than access, and neither reviewer stated it.

The eight diagnostic strata are not an external measurement convention applied to the bank. They **are**
the bank's construction: the bank was generated as 8 strata × 8 records (canonical: 8×7 + 4×1), and the
held-out set was generated in the same design event.

Therefore:

- "Prespecified partition" means **prespecified with respect to solver outcomes**. That holds — no
  solver has been evaluated, so the partition cannot have been tuned to solver results.
- It does **not** mean independent of the evaluation material. The partition and the held-out outcomes
  were chosen together, by the same designers, in one act.

This is legitimate for a conditional test. It is **not** legitimate to describe the partition as
externally imposed or as validated by the bank's own structure. A structure that is generated and then
measured with an instrument derived from the same generator can look more reproducible than it is.

The S1 instrument test is the right response, and it is why S1 exists: it separates "the estimator
recovers a known gain" from "the bank's structure makes the partition look informative".

---

## 4. Requirements for any future confirmatory claim

Ordered by dependency. None is currently satisfied.

| # | Requirement | Why |
|---|---|---|
| 1 | **Analysis frozen first.** Estimand, conditioning set, statistic, folds, coverage gate, and decision thresholds fixed and hashed before the evaluation bank exists | otherwise the bank can shape the analysis |
| 2 | **Bank generated after the freeze**, from a construction rule that does not reference the analysis | breaks the shared-generation-event problem of §3 |
| 3 | **Custody separated from the solver-building team.** Inputs and oracle outputs inaccessible to that team until evaluation is locked | removes the tuning channel the exposure creates |
| 4 | **Oracle outputs withheld**, not merely undocumented | a public oracle converts evaluation into fitting |
| 5 | **Access log preserved** | makes "not inspected" checkable rather than asserted |
| 6 | **Replacement, not repair.** The existing bank is not retrofitted into a sealed set | a bank that has been exposed cannot become sealed by policy |

**Requirement 2 is the one usually omitted,** and it is the one that matters here, because the strata are
the bank's design.

---

## 5. Cost and consequence, stated plainly

- A new bank is a **new measurement instrument**, not an increment on the old one. The 8-stratum
  partition must be justified independently of the bank that realizes it, or the same problem recurs.
- Independent custody is an organisational arrangement, not a file permission. It requires a party that
  is not building solvers and not writing the analysis.
- Until requirements 1–6 exist, **no confirmatory claim is available at any sample size.** This is a
  stronger statement than "more data needed", and it is the correct one.

---

## 6. What this does not say

- It does not invalidate B1, which is a conditional analysis plan and says so.
- It does not claim the bank is scientifically worthless. As development data it is exactly what it says
  it is.
- It does not assert misconduct or exploitation. Exposure is established; use is not.
- It does not authorize building anything. It states what building would have to satisfy.
