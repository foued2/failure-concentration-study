# M3 specification addendum (draft)

**Status: provisional draft for reviewer disposition; NOT frozen. Committed to the
repository for durable reference on branch `review/m3-addendum` (first commit
`2c18d3333f6d5e4a0a6d04606a3954cc81f81aa4`; see this folder's README and MANIFEST for
the record). Not part of the O2 package, Revision F unaltered, no complete-rule
probability computed.**
Author: GLM (local agent), 2026-10-17. Basis: A1 rev 3 imported read-only; probe
`m3_cond_probe.py` + `m3_cond_results.json` (same folder; pinned CPython 3.14.0 venv,
s < 40 s, no third-party packages).

Rev b, 2026-10-17 (applies GPT review of the same date):
1. notation fixed: unscaled residual r vs standardized column x = r/s_ref; the statistic
   divides the raw residual sum of squares by s_ref^2 exactly once (no double division);
2. coefficient scale and z_req meaning stated explicitly; the worked c* numbers are tied
   to the per-reference-sd convention and are not acceptable for freeze until the owner
   decisions in section 9 are recorded;
3. rank equivalence restricted to the stated design (no generalization to larger designs);
4. condition-number results tied to explicit matrices and normalization operations, and
   retained as representation-bound diagnostics, not as scientific gates.
5. Correction found while writing out the derivation: the unit-column-normalized
   reference-cell bound previously stated as sqrt(3) was not exact for that convention
   (it silently used the centered correlation). The exact value under the stated
   normalization is 1+sqrt(2) ~= 2.4142 (section 5); all affected statements updated.

Rev c, 2026-10-17 (applies GPT review of Rev b, correcting Rev b item 5 and the
implied "vacuous gate" statement):
1. The 1+sqrt(2) bound requires w <= 1/2, which TrainRa does not establish. It holds
   only if the dummy is assigned to the smaller bucket (data-dependent coding
   convention). With the fixed dummy I(k=10), section 5 now states the exact scaled
   matrix, identifies the dummy, and proves the exact maximum over the admissible
   splits by NTR: 18.3847 / 21.1187 / 36.6879 / 42.4028 at (1, NTR-1).
2. "The normalized gate is vacuous" is retracted as a universal statement. It holds
   for cell-means coding only (kappa_2 = 1 for every admissible split). Under fixed
   reference-cell coding the kappa_2 <= 30 gate is equivalent to the count condition
   "not (t5 = 1 and t10 >= 225)" (breach boundary w = (899/901)^2; 0/0/112/225
   breaching split points at NTR 85/112/337/450). Raw coding remains a separate case.

Rev d, 2026-10-17 (annotation; no mathematical changes): records the GPT disposition
of Rev c. GPT: derivation and threshold counts check out; provisionally accepted for
mathematical specification, not frozen; the condition-number threshold must not be
frozen as a scientific eligibility gate (it is a representation-dependent proxy for
bucket imbalance, not a neutral identifiability test); recommendation confirmed:
cell-means + unit-normalized columns for the diagnostic, residual-variation criterion
c >= c* as the separate candidate information gate awaiting an owner-approved
scientific rationale; any retained fixed reference-cell kappa_2 <= 30 rule must be
approved and described explicitly as a count-pattern restriction, and must not
silently redefine the frozen O2 event. Section 5 gains one clarifying sentence on the
reference asymmetry.

GPT follow-up (same date, after Rev d): Rev d consistent; no further mathematical
objection. The M3 record is stable at: condition-number diagnostic = cell-means with
unit-normalized columns (kappa_2 = 1 under the specified full-rank design); candidate
information criterion c >= c* not frozen; fixed reference-cell threshold = count-
pattern restriction requiring explicit approval if ever retained; O2 and Revision F
untouched, no complete-rule probability, no Phase 1 authorization. Outstanding items
are the owner decisions in section 9.

This addendum answers GPT's disposition of 2026-10-17: define the design matrix, its
column scaling, the residual-variation statistic, proposed thresholds; derive the
Option B condition-number results; separate exact results from endpoint-based bounds.

## 0. Scope

M3 is at hypothesis stage. Nothing here is frozen: constants marked **[decide]** require
estimand/owner sign-off. The addendum does not compute, and does not authorize, any
complete-rule probability; it only characterizes the gates that a future complete rule
would apply.

## 1. Design definition

Row set: the training-block bodies with k in {5,10}; counts (t5, t10), TrainRa as in O2
(t5,t10 >= 1; t5+t10 >= 8); upper bound t5+t10 <= NTR of the split (85/112/337/450).

Column construction, Option B (recommended). Let C be the largest-family share of a body
and define the UNSCALED within-bucket residual vector
    r = (I - P_D) C,   D = span of the bucket dummies (equivalently span{1, I(k=10)}).
The standardized design column is x = r / s_ref, with s_ref = 0.12703 (fixed A1 rev3
reference pooled within-bucket sd; never recomputed from the realized sample). Two
equivalent codings:
- reference-cell: X = [1, I(k=10), x]
- cell-means:     X = [I(k=5), I(k=10), x]
Notational rule: formulas that divide by s_ref^2 act on r; formulas written in x already
carry the scaling. r itself is never a design column. (This rule resolves the earlier
notation collision; no reported number below was affected.)

Attainable C grids (exact, A1 rev3 enumeration, family cap 5):
- k=5:  {0.2, 0.4, 0.6, 0.8, 1.0}; min gap 0.2; range 0.8
- k=10: {0.2, 0.3, 0.4, 0.5};     min gap 0.1; range 0.3

Scaling convention for the result table: raw coding as written above. For the
collinearity diagnostics (section 5) columns are additionally normalized to unit
Euclidean norm; the normalization operation is part of the result and must be frozen
before any threshold is mentioned.

## 2. What M3 must measure

Two distinct limitations:
- (G1) scale/robustness: arbitrary column units, degenerate splits (near-singleton
  bucket dummies) inflate raw kappa_2 without indicating genuine information loss;
- (G2) information beyond bucket identity: whether C carries enough residual variation
  to identify the intended coefficient at the preregistered resolution.
A raw kappa_2 gate conflates G1 and G2. Recommended mapping:
- G1 -> explicit count constraint (minimum trained bodies per bucket) and/or frozen
  coding; NOT a kappa gate;
- G2 -> (a) full rank (exact, section 3) and (b) an explicit minimum residual-variation
  criterion (section 4);
- collinearity -> a scale-free normalized kappa_2, recorded with the frozen convention
  (section 5); for Option B its value is fully determined by coding and counts: exactly
  1 under cell-means, and exactly sqrt((1+sqrt(w))/(1-sqrt(w))), w = t10/(t5+t10),
  under fixed reference-cell with maximum 18.3847/21.1187/36.6879/42.4028 over the
  admissible splits (a universal 1+sqrt(2) bound holds only for a dummy-on-smaller-
  bucket convention). It is therefore a coding-verification diagnostic, not a
  scientific gate and not evidence of scientific adequacy.

## 3. Rank result (exact, for the stated design only)

For a design consisting of the two bucket-indicator columns and the one additional C
column (either coding in section 1), and given both buckets are represented (TrainRa:
t5,t10 >= 1), full column rank holds if and only if C varies within at least one trained
bucket - the literal CVD-atleastone condition. Equivalently, rank deficiency occurs iff
C is constant within each trained bucket, in which case r = 0. This equivalence must not
be generalized to larger designs with additional regressors or interactions without a
new check. Policy: failure -> M3 missing; no ridge rescue (already agreed).

## 4. Residual-variation statistic and threshold derivation

Statistic (scale-free, count-pattern-deterministic):
    c = r' r / s_ref^2 = sum over buckets of SS_b / s_ref^2,
    SS_b = sum_i (C_i - C_bar_b)^2 (in C units),
equivalently c = x' x with x = r/s_ref. The raw residual sum of squares is divided by
s_ref^2 exactly once; all floor, ceiling and worked-threshold numbers below use this
definition.
c is a deterministic function of the bucket multiset of C values, hence of the count
pattern; it adds no continuous randomness and is compatible with exact enumeration.

Exact floor over CVD-admissible patterns (min-gap two-point split):
    c_floor(t) = delta_k^2 (t-1)/t / s_ref^2,   delta_5 = .2, delta_10 = .1.
Examples: t=2: 1.239 (k5) / 0.310 (k10); t=40: 2.416 / 0.604; t=449: 2.473 / 0.618.
Exact maximum over patterns for a bucket of size t (half at each extreme):
    c_ceil(t) = R_k^2 floor(t^2/4)/t / s_ref^2,   R_5 = .8, R_10 = .3.

Derivation template for a scientifically justified threshold [decide]:
working model y = a + tau*I(k=10) + beta*x + e, x = r/s_ref, Var(e|X) <= sigma_max^2.
Then Var(beta_hat) = sigma^2 / c, so requiring |beta| >= beta_min with
|beta_hat|/SE(beta_hat) >= z_req is equivalent to
    c* = (sigma_max * z_req / beta_min)^2.
Units and meaning (must be stated in the frozen record):
- beta is the coefficient on the standardized column x: y-units per one reference sd of
  C. The worked constants below use this convention.
- Effect per original C unit (beta_C): beta = beta_C * s_ref, hence
  c* = (sigma_max * z_req * s_ref / beta_C)^2.
- z_req is a required standardized effect magnitude. By itself it is not a power
  guarantee. If the intent is two-sided level alpha with power 1-gamma against beta_min,
  then z_req = z_{1-alpha/2} + z_{1-gamma}; otherwise the record must state the decision
  rule that defines z_req. [decide]
- sigma_max: bound on Var(e|X). Binary y gives sigma_max <= 0.5; a preregistered
  conservative bound may be used instead. [decide]
Worked constants (per-reference-sd convention; not acceptable for freeze until the
meanings above are fixed): sigma_max = .5, z_req = 2.5 => beta_min .20 -> c* = 39.1;
.10 -> 156.3; .05 -> 625.0.
Illustrative expected c under A1 reference distributions:
(t=40, k5) ~ 64; (t=100, k5) ~ 161; (t=100, k10) ~ 36; (t=225, k5) ~ 365.
The criterion c >= c* is honest only if the constants come from the estimand; it must
not be tuned to produce an acceptable feasibility probability [GPT 2026-10-17].

## 5. Collinearity diagnostics (exact; diagnostic only)

Normalization operation (frozen): divide each column of X by its Euclidean norm.
Dummy identification (frozen): in the reference-cell coding the single dummy is
I(k=10); k=5 is the reference bucket. This choice matters (see below).

Exact scaled matrices:
- cell-means X = [I(k=5), I(k=10), x]. After column normalization the three columns are
  mutually orthogonal (the two dummies are disjoint; x = r/s_ref is orthogonal to both
  by construction), so the scaled Gram matrix is the identity and kappa_2 = 1 exactly,
  for every admissible split.
- reference-cell X = [1, I(k=10), x]. After column normalization the scaled Gram is
    [[1, sqrt(w), 0], [sqrt(w), 1, 0], [0, 0, 1]],   w = t10/(t5+t10),
  with eigenvalues 1+sqrt(w), 1, 1-sqrt(w) (all positive since t5 >= 1 => w < 1), so
    kappa_2 = sqrt((1+sqrt(w))/(1-sqrt(w))),
  exact for every admissible split.

Maximum over the actual admissible split set (section 1: t5,t10 >= 1, t5+t10 >= 8,
t5+t10 <= NTR). kappa_2 is strictly increasing in w; w = t10/(t5+t10) is maximized on
this set by t5 = 1, t10 = NTR-1 (for fixed t5=1, w increases in t10; for t5 >= 2,
w <= (NTR-2)/NTR). Hence the maximum is attained at (1, NTR-1):

| NTR | argmax (t5,t10) | max kappa_2 | admissible splits whose kappa_2 > 30 |
|-----|-----------------|-------------|-------------------------------------|
| 85  | (1, 84)  | 18.3847 | 0 |
| 112 | (1, 111) | 21.1187 | 0 |
| 337 | (1, 336) | 36.6879 | 112 (all of form t5 = 1, t10 in [225, 336]) |
| 450 | (1, 449) | 42.4028 | 225 (all of form t5 = 1, t10 in [225, 449]) |

Boundary derivation: kappa_2 > 30 iff w > (899/901)^2 = 0.99556544..., i.e. iff
t5 = 1 and t10 >= 225 (t10/(1+t10) > 0.99556544 iff t10 > 224.50). So under the fixed
reference-cell coding the normalized kappa_2 <= 30 gate is NOT vacuous: it is exactly
equivalent to the count condition "not (t5 = 1 and t10 >= 225)". The universal bound
kappa_2 <= 1+sqrt(2) ~= 2.4142 holds only if the dummy is assigned to the smaller
bucket in each split (w = min(t5,t10)/(t5+t10) <= 1/2), a data-dependent coding
convention that must be documented rather than silently assumed. With the dummy fixed
to I(k=10), the mirror singleton (t10 = 1) is harmless (w -> small, kappa_2 -> 1):
which singleton breaches depends on which bucket is the reference, although the column
space is identical - one more reason these numbers are representation-bound.

Three-case summary:

| design | consequence |
|--------|-------------|
| cell-means, columns normalized | kappa_2 = 1 for every admissible split; a kappa_2 <= 30 gate adds no information (rank and residual-variation requirements remain separate and active) |
| fixed reference-cell, columns normalized | kappa_2 = sqrt((1+sqrt(w))/(1-sqrt(w))); the universal 2.4142 bound is not established; breaches 30 exactly at t5 = 1, t10 >= 225 (0/0/112/225 split points at NTR 85/112/337/450) |
| raw coding | the condition number also reflects column-scale differences, so it is not a pure collinearity measure (section 6) |

A condition number is a property of the specified matrix representation: these results
hold only for the columns and the normalization written here; changing the coding, the
normalization operation, or adding columns invalidates them. They are retained as
diagnostics for the stated construction, NOT as evidence of scientific adequacy and NOT
as a scientific gate. Statement "the normalized gate is vacuous" applies to the
cell-means convention only; under fixed reference-cell it is equivalent to the count
condition above, i.e. again a count statement, not a collinearity statement. It is
also not a neutral identifiability test: with k=5 as the reference, (t5,t10) = (1,449)
fails while the mirrored (449,1) passes; reversing the reference bucket swaps which
split is penalized although the column space is unchanged. A neutral test would not
depend on the arbitrary choice of reference.

Consequence for the raw convention: freezing raw kappa_2 <= 30 (section 6) operates as
a proxy for rejecting splits with a near-singleton bucket. That eligibility restriction
is not a property of the matrix representation and is better expressed directly as a
count constraint [open item 3]; it stays out of the frozen O2 definition unless
separately approved.

## 6. Option B condition-number results and derivation

Exactness basis (all of): rows = included trained bodies only; admissible = TrainRa
(t5,t10 >= 1, total >= 8) and CVD-atleastone; split grid t5+t10 <= NTR; s_ref fixed;
endpoint constructions below are attainable; coding as stated.

Derivation. r (equivalently x) is exactly orthogonal to both dummy columns, so X'X is
block diagonal: a 2x2 dummy block and the scalar c. Reference-cell: the block has trace
(t+t10), determinant t5 t10, eigenvalues
    lambda_pm = ((t+t10) +- sqrt((t+t10)^2 - 4 t5 t10))/2,
so kappa_2(c) = sqrt(max(lambda_p, c) / min(lambda_m, c)): decreasing for c < lambda_m,
constant for lambda_m <= c <= lambda_p, increasing for c > lambda_p. Any admissible
total residual variation c lies between attainable endpoints c_min (one bucket min-gap
two-point) and c_max (one bucket half/half extremes); both endpoints are attainable, so
the maximum over all admissible patterns and all splits equals the maximum of the
endpoint values over the (t5,t10) grid. Cell-means: kappa_2(c) = sqrt(max(t5,t10,c) /
min(t5,t10,c)) with the same valley shape, hence same conclusion.

Resulting exact maxima (raw coding), and unweighted counts of (t5,t10) grid points
whose worst pattern exceeds 30 (of 3549 / 6195 / 56595 / 101004 admissible points):

| N   | NTR | any i | any ii | each i | each ii |
|-----|-----|-------|--------|--------|---------|
| 113 | 85  | 29.03 | 28.86  | 20.57  | 20.32   |
| 150 | 112 | 33.32 | 33.17  | 23.60  | 23.38   |
| 450 | 337 | 57.80 | 57.72  | 40.89  | 40.77   |
| 600 | 450 | 66.80 | 66.72  | 47.25  | 47.14   |

any = CVD-atleastone; each = both buckets vary; i = reference-cell; ii = cell-means.
Worst points are (t5,t10) = (449,1), (448,2), ... at the c_max endpoint with k5 the
large bucket; failures require one bucket at ~4 or fewer trained bodies. Typical splits
give kappa_2 ~ 5-15. Unit-normalized values are in section 5 (exact; fixed
reference-cell maximum per split set, attained at (1, NTR-1): 18.3847 / 21.1187 /
36.6879 / 42.4028; = 1 for cell-means). The inflation at the worst points is
column-scale disparity, not collinearity. The normalized maxima occur at the same
near-singleton splits that drive the raw maxima, so both gates again reduce to count
statements about the most imbalanced admissible splits.

Option A (standardization by pooled reference moments, pooled sd .14067, mean .46816):
figures found by scanning the min-deviation family with extremal level pairs; this is an
endpoint-based/indicative result, not an exact worst case (the true maximum could exceed
it; no global optimization was attempted). Reported as >= :
raw up to 469.8 / 540.6 / 942.8 / 1090.2 (coding i), 298.9 / 344.0 / 599.7 / 693.4
(ii); unit-normalized up to 159.6 / 183.5 / 319.4 / 369.2 (i), 137.3 / 158.0 / 275.5 /
318.5 (ii), with some admissible pattern above 30 at essentially every split. These are
sufficient to reject a raw kappa gate under A, but must not be quoted as established
bounds.

## 7. Failure handling

- rank deficiency (equivalently: no bucket varies, i.e. CVD fails) -> M3 missing;
- c < c* -> M3 missing for that realization (no ridge, no refit);
- optional minimum trained bodies per bucket (G1 guard) [decide] -> M3 missing.
No estimator fallback of any kind.

## 8. Exact vs indicative

Exact (given section 6 basis): attainable grids; reference moments and scenario-weight
correlations/VIFs (-0.3774/-0.4020/-0.4295; 1.1661/1.1928/1.2262); rank equivalence;
c floor and ceilings; section 5 normalized kappa_2, its exact per-split-set maxima and
the t5 = 1, t10 >= 225 breach boundary (representation-bound); all table values above
up to the endpoint-derivation argument. Indicative: every Option A figure
(section 6), and the unweighted grid-point counts (they are combinatorial counts, not
probabilities).
Not computed: any complete-rule probability; P(gate fails) per scenario (this would be
a bounded exact count-pattern enumeration in the style of O2, only when authorized).

## 9. Open items

1. c* constants and their meanings: beta_min scale (per reference sd of C vs per
   original C unit), z_req interpretation (pure effect magnitude vs alpha/power
   specification), sigma_max basis [decide].
2. Coding + normalization freeze [decide]: cell-means + unit column scaling makes the
   normalized gate vacuous by construction; fixed reference-cell makes it equivalent to
   the count condition "not (t5 = 1 and t10 >= 225)"; a dummy-on-smaller-bucket
   convention restores the 1+sqrt(2) bound but introduces data-dependent coding.
   In every case the count form is preferable as the actual eligibility rule;
   diagnostics only, never a scientific gate.
3. Whether to add a minimum trained-bodies-per-bucket count m. Note: this narrows
   TrainRa (currently >= 1) and remains OUT of the frozen O2 definition; any future
   eligibility restriction must be explicit and separately approved, and the O2 record
   (TrainRa >= 1) must not be retro-fitted.
4. Estimator sign-off: linear information argument used above; a logistic M3 would
   need a model-based information measure instead.
5. If Option A were ever pursued: exact worst-case optimization over all admissible
   patterns (not done; indicative only).
