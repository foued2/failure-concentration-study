# Follow-up decision memo: post-result interpretation

**Dated: 2026-10-21, before collection**

**Status: frozen pre-collection interpretation**

This memo records how the follow-up result will be classified before any follow-up
data are collected. It references the frozen protocol
`FOLLOWUP_PROTOCOL_2026-11-19.md` and its machine-readable manifest
`FOLLOWUP_PROTOCOL_2026-11-19.json`, frozen in commit `74cd419`.

This memo is interpretive only. It does not amend the protocol, change the
feasibility criterion, or authorize any additional run. If this memo and the frozen
protocol conflict, the protocol governs. The protocol, runner, prompt, source screen,
input banks, and feasibility criterion remain unchanged.

## Relationship to the closed run

The closed run `natural-pilot-20261021T123319Z` remains closed at 100 generation
requests: 39 model-written outputs, 61 usage-limit failures, 15 distinct canonical
bodies, and 10 complete bodies. All ten complete bodies had `k=0`, `C=0`, and 20/20
correct evaluation answers.

That pattern is relevant to expected yield: it suggests this generation procedure may
produce too few nonzero-failure bodies for the research question. It is not a
scientific result about concentration and correctness. The follow-up is a bounded
final test of whether this specific generation procedure can supply the required
comparisons, not a promise that another 100 requests will do so.

The 61 failed requests remain part of the closed run's request budget. They are not
solver observations and must not be analyzed as such.

## Pre-start conditions

- Do not start before `2026-11-19T18:55:00Z`.
- Before the first generation request, check the provider's displayed usage status.
- The first generation request is the availability check.
- If it returns a usage limit or equivalent hard block, record the attempt and stop
  immediately. Do not repeat the request.
- Do not tune the prompt, source screen, input banks, runner, or feasibility criterion
  using the closed run's results.

## Prespecified outcome classification

### 1. Full feasibility criterion met

The frozen criterion is met: some eligible fixed-`k` comparison has at least two
distinct `C` values, at least two distinct canonical bodies at each compared `(k,C)`
level, meaningful variation in independently measured correctness, and passing input
separation and record-integrity checks.

**Interpretation:** The procedure supplied the required observed comparisons for this
exploratory question.

**Next step:** Design a separate confirmatory study with its own protocol, sampling
plan, and analysis. Do not claim the hypothesis is proven. Do not treat this
feasibility result as confirmatory evidence.

### 2. Partial variation

At least one fixed-`k` comparison contains different `C` values, but the full criterion
fails. This includes insufficient distinct bodies at one or more compared `(k,C)`
levels, inadequate correctness variation, or failure of another required condition.

**Interpretation:** The procedure produced some of the intended variation, but not
enough support for the full comparison.

**Next step:** Report exactly which condition failed, with the observed counts and
the frozen criterion. Use the runner's `support_by_k_C` record, which retains all
observed `(k,C)` support even when the full rule is not met, to distinguish partial
variation from no useful contrasts. Do not design a confirmatory study yet. Do not
automatically launch another identical run. Any further run requires a new question
or a separately justified protocol.

### 3. No useful contrasts

No eligible fixed-`k` comparison contains different `C` values. This includes a
follow-up dominated by zero-failure bodies or by concentration that does not vary at
fixed failure counts.

**Interpretation:** The required comparisons were not demonstrated under this specific
generation procedure.

**Next step:** Report the absence of useful contrasts and the observed yield. Do not
automatically authorize a third identical run. Do not present this as evidence that
concentration does or does not predict correctness.

### 4. Provider limit

The provider rejects the availability check or a later generation request with a usage
limit or equivalent hard block. No model output is available for that request.

**Interpretation:** The run is operationally interrupted. Missing outputs are not
solver observations.

**Next step:** Stop immediately, retain the attempt, and report the interruption and
request accounting. Draw no scientific conclusion from the missing outputs.

### 5. Runner or integrity failure

The measurement process cannot produce trustworthy, complete records. Examples include
a hard generation failure other than a provider limit, a Sandbox or runner failure that
invalidates capture, missing required records, or a failed integrity check.

**Interpretation:** The run is operationally invalid or incomplete, not scientifically
negative.

**Next step:** Stop collection, preserve the evidence, and classify the run as
operationally invalid or incomplete. If the defect is discovered only after completion,
classify the affected run after the fact rather than treating it as a scientific
negative. Do not treat it as evidence for or against the research hypothesis.

## Cross-cutting rules

- A partial result must not be promoted to a positive result because it looks
  promising.
- A partial result must not be discarded as if nothing was learned; it identifies
  which part of the intended comparison is missing.
- No third identical run is authorized automatically after any outcome.
- The engineered route is a different research question. Deliberately constructed
  solvers may validate instrumentation or clarify metric behavior, but they do not
  establish that naturally generated solvers exhibit the same patterns or that those
  patterns predict correctness in a real solver population. An engineered study
  requires its own question and protocol.
- The known input-visibility limitation remains in force: source screening is a
  best-effort policy, not a security guarantee, and a solver may be able to inspect
  other inputs in its mounted suite. This limits interpretation even when the runner
  behaves correctly.

## Bounded endpoint

After the follow-up, the result will be classified into exactly one of the five
categories above. The outcome will be one of the following:

1. The comparisons needed to justify designing a confirmatory study.
2. A precise account of why the comparison was unavailable.
3. An operationally interrupted or invalid run with no scientific conclusion.

No outcome requires presenting the original hypothesis as proved or disproved.
