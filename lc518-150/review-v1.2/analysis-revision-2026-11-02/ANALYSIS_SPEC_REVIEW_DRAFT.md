# LC518 150-Body Study: Revised Analysis Specification

**Status:** Owner-approved research direction; review-only draft, published on a dedicated review branch for independent review. Not frozen and not the design-of-record.
**Scope:** Analysis-specification text only. No study bank or candidate solver is created by this document.

## 1. Scientific scope and questions

This is an exploratory study of a deliberately constructed population of 30 LC518 parent implementations and 150 matched solver variants. It is not a sample of naturally generated solvers, arbitrary programs, all LC518 implementations, or all tasks.

The primary analysis remains the matched within-parent correctness contrasts among S0, SA, SB, SAB and S-extra. It is distinct from the secondary prediction analysis. Neither analysis is evidence for the other.

The secondary analysis asks two separate questions, each relative to the same baseline:

1. **Concentration question:** Does the observable concentration of definite diagnostic failures across the eight pre-registered diagnostic input strata improve prediction of held-out correctness beyond total diagnostic failures, unresolved diagnostic outcomes and parent algorithm family?
2. **Enriched-profile question:** Does the complete pre-registered diagnostic outcome profile improve that same prediction beyond the same baseline?

The questions are answered by two separate comparisons, A versus B and A versus C. They are not claims about a causal effect. Model C is not tested incrementally against Model B in this design; A-versus-C evaluates the full profile relative to A, not the profile's additional value after concentration has already entered. A separate B-versus-D comparison would be required for that different question and is not part of this specification.

## 2. Observable diagnostic quantities

There are eight fixed diagnostic input strata, D1–D8. For solver body `s` and stratum `D_j`, let:

- `f_j(s)` be the number of diagnostic records in D_j with a definite `FAIL` outcome;
- `k_fail(s) = sum_j f_j(s)`;
- `k_unresolved(s)` be the number of diagnostic records with `UNRESOLVED` outcomes.

A record has one retained execution status. `UNRESOLVED` is neither `PASS` nor `FAIL`; it does not enter any `f_j` or `k_fail` and is counted separately in `k_unresolved`.

Define the observable diagnostic-stratum concentration feature:

\[
C_D(s)=\begin{cases}
\dfrac{\max_{j=1,\ldots,8} f_j(s)}{k_{\mathrm{fail}}(s)}, & k_{\mathrm{fail}}(s)>0,\\[6pt]
0, & k_{\mathrm{fail}}(s)=0.
\end{cases}
\]

The value 0 when `k_fail = 0` is a computational convention labelled **NO OBSERVED FAILURES**. It is not a measured concentration of zero. `C_D` is an observable feature computed only from diagnostic outcomes. It is not a sealed mutation label, and it is not the same construct as the earlier six-family concentration statistic: it measures concentration across eight input strata, not across verified defect mechanisms.

The eight strata are not eight proven causal mechanisms. D6's reordered records are counted as separate diagnostic record outcomes under the frozen bank definition; dependence between records in a reorder pair must be disclosed.

## 3. Models and pre-processing

All three arms use the same target, outer folds, inner folds, scoring rule, treatment of `k_fail`, treatment of `k_unresolved`, and parent-family context `Z`. Each arm selects its ridge penalty separately from the same fixed grid.

### Model A: baseline

Predictors:

- the fixed flexible basis for `k_fail` defined below;
- `k_unresolved`;
- `Z`, the parent algorithm family, represented by training-fold one-hot indicators.

### Model B: concentration

All Model A predictors, plus `C_D`.

### Model C: enriched diagnostic profile

All Model A predictors, plus the following pre-registered observable features, separately by each D1–D8 stratum:

- counts of `PASS`, wrong-answer, invalid-return-type and exception outcomes;
- mean and maximum absolute numerical deviation among wrong integer outputs, where such outputs exist.

If a deviation summary has no qualifying wrong integer output in a stratum, its value is set to 0 as a missing-summary convention; the associated outcome counts remain available to distinguish no numerical error from other outcome types. Timeout/resource features are excluded unless a separate execution protocol first defines and authorizes a runtime and memory budget.

Model C does not receive sealed mutation identities, mutation descriptions, version-role labels, source code, raw input IDs, raw output text, raw oracle answer values, or solver IDs as predictors. Parent-group IDs are used only for fold formation and group-level reporting. The permitted numerical-deviation summaries are derived outcome features, not raw oracle-answer predictors.

### Flexible treatment of total diagnostic failures

Use the following six-column basis for integer `k = k_fail >= 0`:

\[
B(k)=\left(k,\ (k-1)_+,\ (k-2)_+,\ (k-3)_+,\ (k-4)_+,\ \mathbf{1}[k=0]\right),
\qquad (x)_+=\max(0,x).
\]

The knots 1, 2, 3 and 4 are fixed design conventions, not values chosen from observed outcomes. The unregularized six-column design matrix has rank 5 over k = 0, 1, 2, 3 and 4. Before standardization and regularization, the first four hinge/base columns together with the zero-count indicator can therefore represent arbitrary fitted values at those five levels. The `(k-4)_+` column is zero throughout k = 0..4 and changes the continuation slope above 4. The corresponding unregularized fitted values are:

- k=0: `beta_5`;
- k=1: `beta_0`;
- k=2: `2 beta_0 + beta_1`;
- k=3: `3 beta_0 + 2 beta_1 + beta_2`;
- k=4: `4 beta_0 + 3 beta_1 + 2 beta_2 + beta_3`.

For k > 4, the unregularized increment per additional failure is constant at `beta_0 + beta_1 + beta_2 + beta_3 + beta_4`.

**Regularization qualification:** the saturated parameterization applies to the unstandardized, unpenalized basis representation only. The fitted models standardize all six columns and penalize every non-intercept coefficient, so their realized fitted values are generally not saturated at k=0..4. The linear continuation above k=4 is a fixed functional-form assumption, not an empirical finding.

**Correction to earlier proposals:** a basis with hinge terms only at 1, 2 and 4 has rank 4, not 5, on k=0..4. `(k-4)_+` is zero at k=4 and cannot independently set the fitted value there. The knot at 3 is required for the stated unregularized low-count flexibility. The zero-failure indicator is the sixth column; after training-fold standardization it is a standardized numeric feature, not a raw 0/1 dummy.

### Standardization, ridge penalty and categorical encoding

- Standardize every numeric predictor column, including all six `k_fail` basis columns, the `I[k_fail=0]` indicator, `k_unresolved`, `C_D`, and numeric Model C features, using only the current training partition. For a column with training values `x_1,...,x_n`, use the population mean `mu = sum(x_i)/n` and population standard deviation `sigma = sqrt(sum((x_i-mu)^2)/n)`. Apply `(x-mu)/sigma` to training and validation/test values. Thus the zero-failure indicator is a standardized numeric feature, not a raw 0/1 column in the fitted design matrix.
- Apply these transformations separately inside every inner-CV training split. For the final outer-fold refit, recompute them from the full outer-training partition only.
- If a numeric column has zero training-fold variance, map that column to 0 in both training and validation/test data for that fit. Do not estimate a scale or mean from held-out data.
- Encode each parent family observed in the training partition as a 0/1 indicator. Do not standardize these indicators. Use all observed training-family indicators with an intercept; do not select a reference family.
- If a held-out parent family is absent from the training partition, all fitted family indicators for that case are zero. Its prediction is the fitted intercept plus the contributions of the other predictors; no family-specific coefficient is estimated for that family. This is not an arithmetic average over known family coefficients. The intercept is estimated jointly with the penalized family effects. As the ridge penalty tends to infinity, every non-intercept coefficient tends to zero and the intercept tends to the training-partition mean of the outcome. The limiting unseen-family prediction is therefore the training outcome mean. This rule also applies when a family occurs in only one parent group and that group is held out.
- Fit ridge linear regression with an intercept. For each training partition, minimize the explicitly normalized objective `mean((y - intercept - X beta)^2) + alpha * sum(beta_j^2)`, where the sum covers every non-intercept coefficient. Do not penalize the intercept. Penalize every other coefficient, including spline, `k_unresolved`, `C_D`, Model C numeric features and family indicators, with the same selected ridge penalty. This mean-loss normalization is part of the specification; do not substitute a sum-of-squares objective.
- Fixed candidate penalty grid: `alpha in {0.1, 1, 10, 100}`. The value is selected separately for A, B and C by the inner procedure below. Ties in inner-CV loss are resolved in favour of the larger alpha. No post-hoc model or penalty changes are allowed.
- Because alpha is selected separately for A, B and C, shared baseline coefficients may receive different effective shrinkage in the different arms. A-versus-B compares two separately tuned regularized prediction procedures. It does not estimate an unrestricted independent effect of concentration. Do not label the comparison categorically conservative: the direction and magnitude of differences caused by separate tuning and shrinkage are not determined in advance.
- Predictions are used as produced by the fitted ridge model; no post-hoc clipping to [0,1] is performed.

## 4. Validation and scoring

### Outer validation

Use leave-one-complete-parent-group-out validation: 30 outer folds. All five solver bodies from one parent remain together in the held-out fold. No version from the held-out parent may enter that fold's training data.

### Inner tuning

Use five-fold group-wise CV over the 29 outer-training parent groups. Preassign the 30 parent-group IDs to five fixed buckets by sorting the opaque parent-group IDs and assigning them round-robin. In each outer fold, remove the outer-held-out group from its bucket and use the remaining bucket membership for inner validation. This yields five inner folds with 5 or 6 parent groups each.

The same inner fold definitions and scoring rule are used for Models A, B and C. Select alpha separately for each model by the lowest mean inner-validation MSE across parent groups. Pre-processing is fitted only on each inner-training partition. After alpha selection, refit the model using the complete outer-training partition, with pre-processing fitted on that partition, and predict the five bodies in the outer-held-out parent group.

### MSE aggregation and dependence

The primary reported prediction score is the pooled out-of-fold body-level MSE across 150 predictions:

\[
MSE_m=\frac{1}{150}\sum_{g=1}^{30}\sum_{v=1}^{5}(Q_{gv}-\widehat Q^{(m)}_{gv})^2.
\]

Because every parent group contributes exactly five bodies, this is exactly equal to the unweighted mean of the 30 parent-group mean squared errors. Report the per-parent-group MSEs and the 30 paired group-level differences as well as the overall MSEs. The effective independent grouping level for interpretation is **30 parent groups**, not 150 independent solver bodies. Do not use the 150 body predictions as 150 independent observations for uncertainty claims.

Define:

\[
\Delta_{AB}=MSE_A-MSE_B,\qquad
\Delta_{AC}=MSE_A-MSE_C.
\]

Positive values favour the respective enriched arm. Report the two comparisons separately, alongside all 30 group-level paired differences. They are exploratory. No power claim, minimum-effect threshold, p-value decision rule, confidence-bound gate, confirmatory conclusion or post-hoc feature/model selection is authorized.

## 5. Concentration-support audit

Complete and report this audit before interpreting `Delta_AB`. The diagnostic bank contains 64 records, so the design-implied range is `0 <= k_fail <= 64`; this is a bound from the frozen bank size, not an observed outcome distribution.

### 5.1 Realized and conditional support

1. For every observed `k_fail`, report the number of bodies, number of distinct parent groups, number of distinct `C_D` values, and the frequency of each value.
2. Report the `C_D` distribution within exact `(k_fail, k_unresolved, Z)` cells wherever support exists. Include body and distinct-parent-group counts. Mark sparse or unsupported cells; do not pool or merge cells after looking at outcomes.
3. Report the number of parent groups contributing to each `(k_fail, C_D)` combination. Five versions from one parent count as one parent group for this support assessment, not five independent groups.
4. State the mechanical restrictions: `C_D=1` whenever `k_fail=1`; at `k_fail=0`, the value is only the labelled NO OBSERVED FAILURES convention; with two failures, the possible values are 1 and 1/2; with three failures, the possible values are 1, 2/3 and 1/3. The audit reports realized support and must not assume every mathematically possible value occurs.
5. Disclose dependence from D6 reorder pairs. Its two records are separate rows in the frozen diagnostic bank but are not independent mathematical inputs.

### 5.2 Fold-specific support and zero-variance audit

Run this audit for every outer training fold and every inner-CV training split, using the corresponding validation fold:

1. Report the distinct `k_fail` values and its minimum/maximum in the training partition.
2. For each primary spline column, each numeric Model A/B/C predictor, and `C_D`, report whether the training column has nonzero variance. Report the training mean and scale used for standardization.
3. Report validation values not represented in the training support. For discrete `k_fail`, report both values outside the training range and integer values absent from the exact training set. For `C_D`, report distinct values absent from the exact training set and values outside its training range.
4. If a numeric predictor is constant in training, the agreed preprocessing maps it to zero in both training and validation data. Count validation observations whose original value differs from the training constant; report the number of affected solver bodies and distinct parent groups. These observations are **unsupported by the fitted representation**, because the model cannot register that held-out difference after the zero-variance mapping.
5. Report training-unseen parent families separately. Their family indicators are all zero under the declared UNKNOWN-family convention; count the affected validation bodies/groups and identify the family. This is the specified encoding, not evidence that the family effect was learned.
6. Apply the same procedure to the alternative count basis in §5.3. Do not use validation/test values to estimate means, scales, knots, categories, or coefficients.

A validation value outside the observed training support, or a value differing from a training constant that was mapped to zero, is reported as unsupported extrapolation/representation. It is not counted as successful adjustment. If there is no relevant within-baseline variation in `C_D`, do not interpret predictive improvement as evidence of an independent concentration contribution. Even when variation exists, report how many distinct parent groups supply it. A predictive gain alone does not prove a within-`k_fail` contrast.

### 5.3 Pre-registered secondary concentration sensitivity

The diagnostic bank has 64 records, so `k_fail` cannot exceed 64. For independent review, the proposed secondary sensitivity repeats only the A-versus-B concentration comparison using this fixed alternative count basis:

\[
B_{sens}(k)=\left(k,(k-1)_+,(k-2)_+,(k-3)_+,(k-4)_+,
(k-8)_+,(k-16)_+,(k-32)_+,(k-48)_+,\mathbf{1}[k=0]\right).
\]

This basis has ten columns: the linear term, eight hinge terms and the zero-failure indicator. The primary knots 1, 2, 3 and 4 are retained. Additional knots 8, 16 and 32 are fixed doubling landmarks in the larger count range; 48 is three-quarters of the design maximum and leaves the final 48–64 segment. A knot at 64 would add no variation on the permitted range because `(k-64)_+` is zero for every possible input. These are design conventions, not data-selected knots. The exact alternative set is proposed for GLM review and is not yet frozen.

Fit alternative Model A_sens with this basis and alternative Model B_sens with the same basis plus `C_D`. All other predictors, outer/inner folds, training-only standardization, zero-variance rules, ridge objective, alpha grid, separate alpha selection, and scoring are identical to the primary A/B comparison. Report:

\[
\Delta_{AB,sens}=MSE_{A,sens}-MSE_{B,sens}.
\]

Report this sensitivity separately; it does not replace the primary `Delta_AB` and does not alter Model C or `Delta_AC`. It is used only to assess whether the primary concentration comparison is sensitive to the fixed count functional form. Do not select or modify knots after seeing any outcome. If support is absent for an added hinge in a training fold, report the zero-variance mapping and unsupported validation values under §5.2. The sensitivity comparison remains exploratory and is not a confirmatory test.

## 6. Outcomes and oracle use

The verified reference oracle is used to establish expected answers, classify execution outcomes, derive held-out correctness `Q`, and calculate the pre-registered numerical-deviation summaries. Raw expected-answer values and raw oracle outputs are not predictors. Only the pre-specified derived observable outcome features may enter Model C.

The target `Q` is mean correctness on the fixed 80-record held-out bank. The strict C8/E3 gate is:

- E3 is estimable only if all 150 bodies have resolved outcomes on all 80 held-out records.
- If any of the 12,000 body-by-held-out-record outcomes is unresolved, E3 is `NOT_ESTIMABLE`; report the unresolved coverage and worst/best possible correctness bounds descriptively. Do not fit A/B/C on a resolved-only subset or silently count unresolved outcomes as failures.

This strict E3 rule governs the secondary predictive comparison. It does not silently rewrite the separate unresolved-outcome convention for the primary matched contrasts; that primary analysis retains its own pre-registered outcome-handling specification.

## 7. Interpretation boundaries

- The primary matched within-parent correctness contrasts and the secondary predictive comparisons answer different questions and must be reported separately.
- The eight diagnostic strata are input categories, not verified mechanisms. `C_D` is not a defect-localization measure.
- Sealed mutation identities, mutation details and version-role labels are excluded from predictive features. Their use would leak construction ground truth.
- The accepted diagnostic bank is conditional on the frozen held-out bank under the selected held-out-first collision policy. The accepted banks must not be described as statistically independent samples.
- Results are limited to the declared construction process, LC518 contract, execution protocol and fixed held-out distribution. They do not establish a universal law of solver correctness or transport to natural/independently generated solvers or other tasks.