# Claim and scope

Status: Gate 1 design record. No solver generation has occurred.

## Decision

The study uses **H1a**, the task-specific failure-concentration hypothesis. For
the selected task, higher diagnostic failure concentration `C` is expected to be
associated with higher held-out boundary score `S` at a fixed diagnostic failure
count `k`, after accounting for `k` and generator identity.

H1a is a claim about this declared domain and this task. It is not a claim that
concentration causes generalization everywhere.

## Why this is not the retired H2 claim

The earlier programme claimed that particular generated solvers carried a
recoverable hidden structure, and that this structure explained perturbations.
That claim was retired after a cost proxy recovered the boundary without access
to the intended structure. H1a does not revive it. The diagnostic bank here is
constructed from the declared input domain, and all evaluation inputs are inside
that same domain. No hidden structure is inferred from solver behaviour.

## Terms

- **Diagnostic failure:** a wrong answer on one of the 30 fixed diagnostic
  inputs.
- **Failure vector:** `(f_0, ..., f_5)`, the number of diagnostic failures in
  each of six structural families.
- **`k`:** total diagnostic failures, `sum(f_j)`.
- **`C`:** failure concentration, `max(f_j) / k`; undefined at `k = 0`.
- **Held-out evaluation:** the 98 declared-domain inputs not used for diagnosis.
- **`S`:** fraction of the 98 evaluation inputs answered correctly.
- **Unanticipated:** inputs outside the declared domain. This is outside scope.

“Held-out” means held out from diagnosis within a fixed, fully enumerated
domain. It does not mean unseen, arbitrary, or open-ended.

## Scope

In scope:

- one task, `paren7_min_insertions`;
- one fixed 128-input domain;
- one 30-input diagnostic bank and its disjoint 98-input evaluation complement;
- feasible diagnostic profiles with five probes per family;
- calibration controls built by the researcher;
- an offline power and identification analysis.

Out of scope:

- generation of the 150 study solvers at Gate 1;
- changes to the task, banks, target profiles, or scoring after seeing solvers;
- claims about inputs outside the declared domain;
- causal claims about generator internals;
- any use of the retired hidden-structure claim;
- any model/API call in Gate 1.

## Primary question

At fixed `k = 5`, do profiles with higher `C` have higher mean held-out `S`
after accounting for generator identity and carrier family?

## Secondary questions

- Is there a within-carrier-family fixed-`k` contrast between higher and lower
  `C`?
- How much does `S` vary between generator identities at the same profile?
- How much does `S` vary between structural carrier families at the same `C`?
- Is the observed residual variation compatible with the planned sample size?

## Identification requirements

A GO decision requires all of the following before generation:

1. At least one fixed-`k` contrast where higher and lower `C` occur with the
   same carrier family, not merely different carrier families.
2. Enough distinct configurations to separate `C` from carrier family and from
   family-specific difficulty.
3. Power of at least 0.80 at a justified residual standard deviation, with a
   minimum detectable effect no larger than the prespecified meaningful effect.
4. An empirical or defensible prior estimate of residual `S` variation.

Gate 1 must not convert a calibration limitation into evidence for H1a.
