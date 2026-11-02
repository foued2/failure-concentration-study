# LC518 150-Body Study: Revised Analysis Specification

**Revision:** Consolidated review revision 2.6, 2026-11-02  
**Status:** Review-only draft on a dedicated branch. Not frozen and not the design of record.
**Decision status:** B1–B3, M2–M3 and E2–E8 corrections are consolidated. The strict C8/E3 gate is recorded as owner-confirmed in chat on 2026-11-02. M1 is fixed as a same-exact-cell support floor: at least three distinct parent groups must each contribute within-parent C_D variation in the same exact (k_fail, k_unresolved) cell. The sensitivity knots {1,2,3,4,8,16,32,48} are fixed pre-outcome design conventions. The corrected full C9 held-out-first protocol is pinned in C9_GENERATION_SPEC_REVIEW.md revision 2.6 and remains pending focused independent review and owner ratification. The four inherited v1.0 analysis/reporting protections are carried forward; the manifestation taxonomy is newly closed by a pre-run allowlist and a protocol-abort rule.  
**Scope:** Analysis specification and pre-outcome support rules only. No study bank or candidate solver is created by this document.

## 1. Scientific scope and questions

This is an exploratory study of a deliberately constructed population of 30 LC518 parent implementations and 150 matched solver variants. It is not a sample of naturally generated solvers, arbitrary programs, all LC518 implementations, or all tasks.

The primary analysis remains the matched within-parent correctness contrasts among S0, SA, SB, SAB and S-extra. It is distinct from the secondary prediction analysis. Neither analysis is evidence for the other.

The secondary analysis asks two separate questions, each relative to the same baseline:

1. **Concentration question:** Does the observable concentration of definite diagnostic failures across the eight pre-registered diagnostic input strata improve prediction of held-out correctness beyond total diagnostic failures, unresolved diagnostic outcomes and parent algorithm family?
2. **Enriched-profile question:** Does the complete pre-registered diagnostic outcome profile improve that same prediction beyond the same baseline?

The questions are answered by two separate comparisons, A versus B and A versus C. They are not claims about a causal effect. Model C is not tested incrementally against Model B in this design; A-versus-C evaluates the full profile relative to A, not the profile's additional value after concentration has already entered. That different question would require an additional arm containing A, C_D and the complete profile, here called **B+profile**, and a B-versus-B+profile comparison. That comparison is not part of this specification. Do not call it B-versus-D.

## 2. Observable diagnostic quantities

There are eight fixed diagnostic input strata, D1–D8, with eight records per stratum and 64 diagnostic records total. For solver body s and stratum D_j, define:

- f_j(s): the number of records in D_j with a definite FAIL outcome, counting every registered failure manifestation;
- k_fail(s) = sum_j f_j(s);
- k_unresolved(s): the number of diagnostic records with UNRESOLVED outcomes;
- coverage_diag(s): the fraction of diagnostic records resolved as PASS or FAIL.

UNRESOLVED is neither PASS nor FAIL. It does not enter any f_j or k_fail and is counted separately in k_unresolved.

The aggregate coverage variable is:

\[
coverage_{\mathrm{diag}}(s)=\frac{\text{resolved diagnostic records}}{64}
=1-\frac{k_{\mathrm{unresolved}}(s)}{64}.
\]

Report coverage_diag, but exclude it from every predictive design matrix. It is an affine function of k_unresolved and would duplicate information already in the baseline.

Define the observable diagnostic-stratum concentration feature:

\[
C_D(s)=
\begin{cases}
\dfrac{\max_{j=1,\ldots,8} f_j(s)}{k_{\mathrm{fail}}(s)}, & k_{\mathrm{fail}}(s)>0,\\[6pt]
0, & k_{\mathrm{fail}}(s)=0.
\end{cases}
\]

The value 0 when k_fail = 0 is a computational convention labelled **NO OBSERVED FAILURES**. It is not a measured concentration of zero. C_D is an observable feature computed only from diagnostic outcomes. It is not a sealed mutation label, and it is not the same construct as the earlier six-family concentration statistic: it measures concentration across eight input strata, not across verified defect mechanisms.

For k_fail > 0, the eight-stratum definition imposes the general support bound:

\[
\frac{\lceil k_{\mathrm{fail}}/8\rceil}{k_{\mathrm{fail}}}
\le C_D \le 1.
\]

The lower bound follows because at least one of eight nonnegative integer stratum counts summing to k_fail must be at least ceil(k_fail/8). In particular, C_D = 1 whenever k_fail = 1; at k_fail = 2 its possible values are 1/2 and 1; at k_fail = 3 they are 1/3, 2/3 and 1. The k_fail = 0 value remains the labelled NO OBSERVED FAILURES convention. Same-k variation is therefore possible only for k_fail >= 2. The realized audit must report observed values and must not assume that every mathematically possible value occurs.

The eight strata are not eight proven causal mechanisms. D6's reordered records are counted as separate diagnostic record outcomes under the frozen bank definition; dependence between records in a reorder pair must be disclosed.

## 3. Models and pre-processing

All three arms use the same target, outer folds, inner folds, scoring rule, treatment of k_fail, treatment of k_unresolved, and parent-family context Z. Each arm selects its ridge penalty separately from the same fixed grid.

### 3.1 Model A: baseline

Predictors:

- the fixed flexible basis for k_fail defined below;
- k_unresolved;
- Z, the parent algorithm family, represented by training-fold one-hot indicators.

coverage_diag is reported but is not a predictor.

### 3.2 Model B: concentration

All Model A predictors, plus C_D.

### 3.3 Model C: enriched diagnostic profile

All Model A predictors, plus the following pre-registered observable features.

For each diagnostic stratum s in D1–D8:

| Feature | Definition |
|---|---|
| d_pass_s | Count of PASS records in stratum s. |
| d_wrong_answer_s | Count of FAIL records whose typed manifestation is wrong answer in s. |
| d_invalid_return_s | Count of FAIL records whose typed manifestation is invalid return type in s. |
| d_exception_s | Count of FAIL records whose typed manifestation is exception in s. |
| d_other_s | Count of FAIL records whose typed manifestation is on the closed, pre-run other-manifestation allowlist; the allowlist may be empty and excludes timeout/resource breach. |
| d_unresolved_s | Count of UNRESOLVED records in s. This is a coverage variable, never a failure count. |
| d_meandev_s | Mean absolute numerical deviation over wrong exact-int outputs in s; 0 when undefined because there are no such outputs. |
| d_meandev_s_defined | Boolean indicator that d_meandev_s is defined from at least one wrong exact-int output. |
| d_maxdev_s | Maximum absolute numerical deviation over wrong exact-int outputs in s; 0 when undefined because there are no such outputs. |
| d_maxdev_s_defined | Boolean indicator that d_maxdev_s is defined from at least one wrong exact-int output. |
| d_timeout_s | Reserved timeout/resource-breach FAIL count. Null in the current no-execution-protocol state; not zero-filled and excluded from the design matrix while null. |

A wrong integer output means that the returned value has exact Python type int and differs from the expected integer: type(returned) is int and returned != expected. Python bool is not an exact int for this contract and is excluded, even though bool is a subclass of int. Every return whose exact Python type is not int, including bool, is classified as invalid-return-type, not wrong-answer. For every qualifying wrong integer output, the absolute deviation is at least 1. Thus the fixed zero sentinel for an undefined deviation summary cannot be confused with an observed deviation of zero. The companion _defined indicators preserve the distinction.

The d_timeout_s column is retained in the schema as a reserved null column. It may be populated only after a separate execution protocol has been authorized, the runtime and memory budgets and timeout/resource classification have been specified, and the final feature list has been frozen before any candidate runs. While it is null, it is excluded from the design matrix, not converted to zero. If a future protocol populates it, it is a definite FAIL manifestation and contributes to f_j and k_fail. It is never included in d_other_s.

The D6 order-invariance features are also included in Model C:

| Feature | Definition |
|---|---|
| d_order_pairs_resolved | Count of the four D6 canonical pairs for which both orderings have resolved statuses, PASS or FAIL, regardless of manifestation. |
| d_order_pairs_comparable | Count of D6 canonical pairs for which both executions are resolved and both return comparable exact-int values. PASS and wrong-answer outputs qualify. If either ordering has an invalid return type, exception, or another outcome without a comparable exact-int return value, the pair is excluded here but remains counted in d_order_pairs_resolved when both statuses are resolved. |
| d_order_inconsistent | Count, among comparable D6 pairs, whose two returned integer values differ. This is a value-based count. |

Both d_order_inconsistent and its denominator d_order_pairs_comparable enter Model C as counts. The rate d_order_inconsistent / d_order_pairs_comparable may also be reported descriptively; it is null when the denominator is zero, never silently set to zero and never imputed. Identical wrong integer values under both orderings count as consistent, not inconsistent.

The D6 records and the three order features are diagnostic-only. Their pair dependence must be disclosed. Do not treat the eight D6 records as eight independent mathematical instances.

### 3.4 Aggregate columns and typed record

Aggregate columns include k_fail, k_unresolved, family Z and coverage_diag. coverage_diag is calculated and reported as defined in §2, but is excluded from both Model A and all other predictive arms because it is an affine duplicate of k_unresolved.

The typed execution record remains authoritative. The closed manifestation taxonomy for this review phase consists of wrong answer, invalid return type, exception, and an explicitly enumerated other-manifestation allowlist fixed before any run. The allowlist may be empty. Each allowlisted status must be named explicitly in the pre-run feature freeze; the label other is not a catch-all. Timeout/resource breach is not in this allowlist and cannot be classified until a separate authorized execution protocol defines it. Every return whose exact Python type is not int, including bool, is invalid-return-type. Any definite FAIL whose typed manifestation does not match one of the registered categories is a protocol error and aborts the run; it must not be silently reassigned to other, dropped, or reclassified after outcomes are observed. For every stratum, f_j counts all definite FAIL manifestations; k_fail is the sum of f_j over D1–D8. UNRESOLVED remains separate.

Reserved columns that are null are reported as null and excluded from the design matrix. They are never zero-filled. A reserved column may be populated only after the separate execution protocol and pre-run feature-list freeze described above.

### 3.5 Collinearity and coefficient interpretation

The Model C count columns contain exact linear relationships with aggregate counts. For example, summing d_unresolved_s over D1–D8 gives k_unresolved; summing the registered FAIL-manifestation counts over strata gives k_fail; and the per-stratum outcome counts partition the eight records in each stratum, subject to any reserved status column remaining null or later being populated under an authorized protocol. While d_timeout_s is reserved null, the per-stratum partition identity is d_pass_s + d_wrong_answer_s + d_invalid_return_s + d_exception_s + d_other_s + d_unresolved_s = 8 for each stratum. If a separately authorized protocol later populates d_timeout_s, add it to that identity. The zero-filled deviation values and their _defined flags also have a deliberate relationship.

The ridge objective with positive alpha and an unpenalized intercept still gives a unique penalized coefficient solution and unique fitted predictions under this specification. However, exact collinearity means individual Model C coefficients are not separately interpretable as independent effects. Report predictions, MSEs and pre-registered MSE differences, not causal or isolated interpretations of individual coefficients. Do not remove or alter pre-registered columns to improve coefficient interpretability after outcomes are observed.

Model C does not receive sealed mutation identities, mutation descriptions, version-role labels, source code, raw input IDs, raw output text, raw oracle answer values, or solver IDs as predictors. Parent-group IDs are used only for fold formation and group-level reporting. The permitted numerical-deviation summaries are derived outcome features, not raw oracle-answer predictors.

### 3.6 Flexible treatment of total diagnostic failures

Use the following six-column basis for integer k = k_fail >= 0:

\[
B(k)=\left(k,\ (k-1)_+,\ (k-2)_+,\ (k-3)_+,\ (k-4)_+,\ \mathbf{1}[k=0]\right),
\qquad (x)_+=\max(0,x).
\]

The knots 1, 2, 3 and 4 are fixed design conventions, not values chosen from observed outcomes. The unregularized six-column design matrix has rank 5 over k = 0, 1, 2, 3 and 4. Before standardization and regularization, the first four hinge/base columns together with the zero-count indicator can represent arbitrary fitted values at those five levels. The (k-4)_+ column is zero throughout k = 0..4 and changes the continuation slope above 4. The corresponding unregularized fitted values are:

- k=0: beta_5;
- k=1: beta_0;
- k=2: 2 beta_0 + beta_1;
- k=3: 3 beta_0 + 2 beta_1 + beta_2;
- k=4: 4 beta_0 + 3 beta_1 + 2 beta_2 + beta_3.

For k > 4, the unregularized increment per additional failure is constant at beta_0 + beta_1 + beta_2 + beta_3 + beta_4.

**Regularization qualification:** the saturated parameterization applies to the unstandardized, unpenalized basis representation only. The fitted models standardize all six columns and penalize every non-intercept coefficient, so their realized fitted values are generally not saturated at k=0..4. The linear continuation above k=4 is a fixed functional-form assumption, not an empirical finding.

**Correction to earlier proposals:** a basis with hinge terms only at 1, 2 and 4 has rank 4, not 5, on k=0..4. (k-4)_+ is zero at k=4 and cannot independently set the fitted value there. The knot at 3 is required for the stated unregularized low-count flexibility. The zero-failure indicator is the sixth column; after training-fold standardization it is a standardized numeric feature, not a raw 0/1 dummy.

### 3.7 Standardization, ridge penalty and categorical encoding

- Standardize every non-reserved numeric predictor column, including all six k_fail basis columns (the sixth is the I[k_fail=0] indicator), k_unresolved, C_D, Model C counts, deviation summaries and defined indicators, and the three D6 order features, using only the current training partition. For training values x_1,...,x_n, use the population mean mu = sum(x_i)/n and population standard deviation sigma = sqrt(sum((x_i-mu)^2)/n). Apply the resulting transformation to training and validation/test values.
- Apply these transformations separately inside every inner-CV training split. For the final outer-fold refit, recompute them from the full outer-training partition only.
- If a numeric column has zero training-fold variance, map that column to 0 in every training and validation/test row for that fit. Do not divide by zero or create NaN or infinity. Keep the column in the declared schema and report it in the support audit; do not silently drop it. A validation observation whose original value differs from the training constant is unsupported by that fitted representation and must be counted as such.
- A reserved null column such as d_timeout_s is different from a zero-variance numeric column: while null, it is excluded from the design matrix and is not zero-filled. If it is later populated under a separately authorized, pre-run protocol, the complete feature list and treatment must be frozen before candidate runs.
- Encode each parent family observed in the training partition as a 0/1 indicator. Do not standardize these indicators. Use all observed training-family indicators with an intercept; do not select a reference family.
- If a held-out parent family is absent from the training partition, all fitted family indicators for that case are zero. Its prediction is the fitted intercept plus the contributions of the other predictors; no family-specific coefficient is estimated for that family. This is not an arithmetic average over known family coefficients. The intercept is estimated jointly with the penalized family effects. As the ridge penalty tends to infinity, every non-intercept coefficient tends to zero and the intercept tends to the training-partition mean of the outcome. The limiting unseen-family prediction is therefore the training outcome mean. This rule also applies when a family occurs in only one parent group and that group is held out.
- Fit ridge linear regression with an intercept. For each training partition, minimize mean((y - intercept - X beta)^2) + alpha * sum(beta_j^2), where the sum covers every non-intercept coefficient. Do not penalize the intercept. Penalize every other fitted coefficient, including spline, k_unresolved, C_D, Model C numeric features and family indicators, with the same selected ridge penalty. This mean-loss normalization is part of the specification; do not substitute a sum-of-squares objective.
- Fixed candidate penalty grid: alpha in {0.1, 1, 10, 100}. The value is selected separately for A, B and C by the inner procedure below. Ties in inner-CV loss are resolved in favour of the larger alpha. No post-hoc model or penalty changes are allowed.
- Because alpha is selected separately for A, B and C, shared baseline coefficients may receive different effective shrinkage in the different arms. A-versus-B compares two separately tuned regularized prediction procedures. It does not estimate an unrestricted independent effect of concentration. Do not label the comparison categorically conservative: the direction and magnitude of differences caused by separate tuning and shrinkage are not determined in advance.
- Predictions are used as produced by the fitted ridge model; no post-hoc clipping to [0,1] is performed.

## 4. Validation and scoring

### 4.1 Outer validation

Use leave-one-complete-parent-group-out validation: 30 outer folds. All five solver bodies from one parent remain together in the held-out fold. No version from the held-out parent may enter that fold's training data.

### 4.2 Fixed inner buckets

Sort the published parent IDs numerically, G01 through G30. Assign each group to the bucket given by its numeric suffix modulo 5. The resulting fixed buckets are:

| Bucket | Parent groups |
|---|---|
| 0 | G05, G10, G15, G20, G25, G30 |
| 1 | G01, G06, G11, G16, G21, G26 |
| 2 | G02, G07, G12, G17, G22, G27 |
| 3 | G03, G08, G13, G18, G23, G28 |
| 4 | G04, G09, G14, G19, G24, G29 |

The parent IDs are public and are not opaque. The numeric sort and exact bucket table are pinned here to remove any dependence on ambiguous text sorting. In each outer fold, remove the outer-held-out group from its bucket and use the remaining four or five groups in that bucket as that inner fold's validation groups. The other buckets are the corresponding inner-training groups. This yields five inner folds with 5 or 6 validation parent groups each, totalling all 29 outer-training groups exactly once.

### 4.3 K5 family support in inner and outer folds

PARENT_DESIGN defines K5 as G29 and G30 only. With the fixed buckets above:

- In the outer fold holding G29, the inner fold whose validation bucket is 0 also holds G30. K5 is therefore absent from that inner-training partition.
- In the outer fold holding G30, the inner fold whose validation bucket is 4 also holds G29. K5 is therefore absent from that inner-training partition.
- These are exactly 2 of the 150 outer-by-inner split instances. The other 148 inner-training partitions contain at least one K5 parent.
- In the outer refits holding G29 or G30, only the other K5 parent is present in the outer-training partition. The K5 family coefficient is then supported by one parent group (five matched bodies), not by independent replication across K5 parents.

Do not claim that a K5 family-level effect generalizes. With only two K5 parent groups, a family-level contribution cannot be distinguished reliably from either parent's idiosyncrasy. Report the sparse family support and the affected folds. Because family indicators are unstandardized but penalized with the same alpha as other coefficients, the sparse K5 coefficient also has fewer observations supporting it under the fixed penalty; this is a limitation, not a reason to change the penalty after outcomes.

### 4.4 Inner alpha selection

For each candidate alpha and each model arm, collect the validation predictions for all 145 bodies in the 29 outer-training parent groups, with every body appearing exactly once as an inner-validation prediction. Compute one pooled body-level MSE over those 145 predictions. Because each of the 29 parent groups contributes exactly five bodies, this pooled MSE is also exactly the equally weighted mean of the 29 parent-group MSEs.

Do not compute five fold-level MSEs and average those five values. The folds contain different numbers of parent groups after the outer-held-out group is removed; an unweighted mean of fold means would give unequal weight to parent groups and is not the specified tuning criterion.

The same inner fold definitions and scoring rule are used for Models A, B and C. Select alpha separately for each model by the lowest pooled inner-validation MSE. Pre-processing is fitted only on each inner-training partition. After alpha selection, refit the model using the complete outer-training partition, with pre-processing fitted on that partition, and predict the five bodies in the outer-held-out parent group.

In exactly two outer-by-inner split instances, an inner-validation bucket contains the other K5 parent while the inner-training partition contains no K5 parent: outer G29 with validation bucket 0 (which contains G30), and outer G30 with validation bucket 4 (which contains G29). The five validation bodies from that K5 parent are included in the 145-body pooled criterion, but the K5 family is unseen in inner training and its family indicators are therefore all zero for those validation rows. Count these five bodies and their one parent group in the training-unseen-family validation counts required by §5.3 item 5. Do not confuse this categorical unseen-family case with a numeric zero-variance predictor. This fixed fold-geometry effect applies symmetrically to Models A, B and C and is not evidence that a K5 effect was learned.

### 4.5 Outer MSE aggregation and dependence

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

Positive values favour the respective enriched arm. Report the two comparisons separately, alongside all 30 group-level paired differences. Both deltas share Model A and are correlated comparisons, not independent replications. They are exploratory. No power claim, minimum-effect threshold, p-value decision rule, confidence-bound gate, confirmatory conclusion or post-hoc feature/model selection is authorized.

## 5. Concentration-support audit

Complete and report this audit before interpreting Delta_AB. The diagnostic bank contains 64 records, so the design-implied range is 0 <= k_fail <= 64; this is a bound from the frozen bank size, not an observed outcome distribution.

### 5.1 Global, conditional and parent-group support

1. For every observed k_fail, report the number of bodies, number of distinct parent groups, number of distinct C_D values, and the frequency of each value.
2. Restrict same-k concentration-variation claims to k_fail >= 2. At k_fail = 0 report NO OBSERVED FAILURES rather than a concentration value; at k_fail = 1 C_D is mechanically 1.
3. Report the C_D distribution within exact (k_fail, k_unresolved, Z) cells wherever support exists. Include body and distinct-parent-group counts. Mark sparse or unsupported cells; do not pool or merge cells after looking at outcomes.
4. Report the number of parent groups contributing to each (k_fail, C_D) combination. Five versions from one parent count as one parent group for this support assessment, not five independent groups.
5. For each exact (k_fail, k_unresolved) cell with k_fail >= 2, report the number of distinct parent groups that contribute within-parent C_D variation in that same cell. A parent group contributes to that cell only if at least two of its five matched versions fall in the same exact cell and have different C_D values. Also report the less restrictive same-k variation count separately; it does not by itself satisfy the exact-cell support rule.
6. Disclose dependence from D6 reorder pairs. Its two records are separate rows in the frozen diagnostic bank but are not independent mathematical inputs.

### 5.2 Fixed minimum within-parent support criterion

For a particular exact (k_fail, k_unresolved) cell with k_fail >= 2, concentration-specific support is present only when **at least three distinct parent groups contribute within-parent C_D variation in that same cell**. A parent group contributes only if at least two of its five matched versions fall in that exact cell and have different C_D values. Count distinct parent groups, not bodies or pairs. Contributions from different exact cells must not be pooled to reach the three-parent floor. Report the less restrictive same-k variation count alongside the exact-cell parent-group counts so the less restrictive form of variation remains visible without being substituted for exact-cell support.

The three-parent floor is a predeclared operational support convention, not a power or precision claim. It is not a statistically derived cutoff, effect-size threshold, confirmatory criterion, or claim that three groups are sufficient for generalization.

If no exact (k_fail, k_unresolved) cell reaches the three-parent floor, still report the predeclared model predictions and Delta_AB if E3 is otherwise estimable, but label concentration-specific interpretation **INSUFFICIENT_WITHIN_PARENT_SUPPORT**. This is a support limitation, not a null effect: do not interpret the sign or magnitude of Delta_AB as evidence for or against a distinct concentration contribution. A cell supported by fewer than three parent groups remains explicitly unsupported.

### 5.3 Fold-specific support and zero-variance audit

Run this audit for every outer training fold and every inner-CV training split, using the corresponding validation fold:

1. Report distinct k_fail values and the minimum/maximum in the training partition.
2. For each primary spline column, each numeric Model A/B/C predictor, and C_D, report whether the training column has nonzero variance. Report the training mean and scale used for standardization.
3. Report validation values not represented in the training support. For discrete k_fail, report both values outside the training range and integer values absent from the exact training set. For C_D, report distinct values absent from the exact training set and values outside its training range.
4. If a numeric predictor is constant in training, the agreed preprocessing maps it to zero in both training and validation data. Count validation observations whose original value differs from the training constant; report affected solver bodies and distinct parent groups. These observations are unsupported by the fitted representation because the model cannot register that held-out difference after the zero-variance mapping.
5. Report training-unseen parent families separately. Their family indicators are all zero under the declared UNKNOWN-family convention; count affected validation bodies/groups and identify the family. This is the specified encoding, not evidence that the family effect was learned.
6. Apply the same procedure to the alternative count basis in §5.4. Do not use validation/test values to estimate means, scales, knots, categories or coefficients.

A validation value outside the observed training support, or a value differing from a training constant that was mapped to zero, is reported as unsupported extrapolation/representation. It is not counted as successful adjustment. If there is no relevant within-baseline variation in C_D, do not interpret predictive improvement as evidence of an independent concentration contribution.

### 5.4 Fixed secondary concentration sensitivity

The current proposal is a fixed secondary sensitivity basis with knots {1,2,3,4,8,16,32,48}:

\[
B_{\mathrm{sens}}(k)=
\left(k,(k-1)_+,(k-2)_+,(k-3)_+,(k-4)_+,
(k-8)_+,(k-16)_+,(k-32)_+,(k-48)_+,\mathbf{1}[k=0]\right).
\]

This basis has ten columns: the linear term, eight hinge terms and the zero-failure indicator. The primary knots 1, 2, 3 and 4 are retained. Additional knots 8, 16 and 32 are fixed doubling landmarks in the larger count range; 48 is three-quarters of the design maximum and leaves the final 48–64 segment. A knot at 64 would add no variation on the permitted range because (k-64)_+ is zero for every possible input. The complete knot set is fixed before any outcomes are observed and must not be altered in response to results. Its additional hinges at 8, 16, 32 and 48 primarily test whether those higher-count segments have support; they do not guarantee estimable high-count curvature. The sensitivity is mainly informative about low-count functional form unless the high-count hinges have adequate support.

Fit alternative Model A_sens with this basis and alternative Model B_sens with the same basis plus C_D. All other predictors, outer/inner folds, training-only standardization, zero-variance rules, ridge objective, alpha grid, separate alpha selection, pooled inner scoring and outer scoring are identical to the primary A/B comparison. Report:

\[
\Delta_{AB,\mathrm{sens}}=MSE_{A,\mathrm{sens}}-MSE_{B,\mathrm{sens}}.
\]

Report this sensitivity separately; it does not replace primary Delta_AB and does not alter Model C or Delta_AC. It assesses sensitivity to the fixed count functional form. Do not select or modify knots after seeing any outcome.

The additional hinges at 8, 16, 32 and 48 may have zero variance in many inner or outer training partitions, especially if few bodies have large k_fail. Report each fold's zero-variance columns and any validation values unsupported by the zero-variance mapping. In every inner and outer training partition, also report the rank of the unstandardized sensitivity-basis matrix over the distinct observed k_fail values (maximum 10), the number of distinct observed k_fail values, whether k_fail = 0 is present, and the support on each side of every knot, with the sides defined for each knot t as k_fail ≤ t (hinge inactive) and k_fail > t (hinge active). Report both body counts and distinct observed k_fail-value counts on each side; the strict > t side is required for a positive hinge. Mark knot t as STRADDLED only when the training partition contains at least one distinct observed k_fail value on each side; otherwise mark it NOT_STRADDLED. Identify missing knots/segments and rank deficiency explicitly. This is a support diagnostic, not a requirement that the ridge fit be mathematically solvable: positive-alpha ridge remains uniquely defined, but unsupported basis directions do not provide empirical evidence about the corresponding curvature. The sensitivity is pre-registered and must not be dropped or retuned after inspection. If its additional columns are unsupported in most folds, say so explicitly; do not describe the sensitivity as demonstrating robustness to high-count curvature.

## 6. Outcomes and oracle use

The verified reference oracle is used to establish expected answers, classify execution outcomes, derive held-out correctness Q and calculate the pre-registered numerical-deviation summaries. Raw expected-answer values and raw oracle outputs are not predictors. Only the pre-specified derived observable outcome features may enter Model C.

The target Q is mean correctness on the fixed 80-record held-out bank. The strict C8/E3 gate, confirmed by the owner in chat on 2026-11-02, is:

- E3 is estimable only if all 150 bodies have resolved outcomes on all 80 held-out records.
- If any of the 12,000 body-by-held-out-record outcomes is unresolved, E3 is NOT_ESTIMABLE; report unresolved coverage and worst/best possible correctness bounds descriptively. Do not fit A/B/C on a resolved-only subset or silently count unresolved outcomes as failures.

The C8 status statements in `lc518-150/review-v1.2/CORRECTIONS_RECORD_v1.2.2-draft.md` (dated 2026-11-01) predate the owner's 2026-11-02 confirmation recorded here and are superseded for C8/E3 status only by this revision; the historical corrections record remains unchanged.

This strict E3 rule governs the secondary predictive comparison. It does not silently rewrite the separate unresolved-outcome convention for the primary matched contrasts; that primary analysis retains its own pre-registered outcome-handling specification.

## 7. Interpretation boundaries

- The primary matched within-parent correctness contrasts and the secondary predictive comparisons answer different questions and must be reported separately.
- The eight diagnostic strata are input categories, not verified mechanisms. C_D is not a defect-localization measure. The C8/E3 unresolved-outcome rule is owner-confirmed as recorded in §6; this provenance record does not itself freeze the full analysis specification or authorize execution.
- Sealed mutation identities, mutation details and version-role labels are excluded from predictive features. Their use would leak construction ground truth.
- The selected C9 design direction is held-out-first generation with diagnostic-side whole-candidate collision rejection. Its complete, renumbered procedure is pinned in C9_GENERATION_SPEC_REVIEW.md; it remains pending focused independent GLM review and owner ratification, and is not yet frozen or incorporated into the historical BANK_DESIGN.md. Any diagnostic bank generated under that policy would be conditional on the frozen held-out bank; the accepted banks must not be described as statistically independent samples. No bank has been generated under this review draft.
- Results are limited to the declared construction process, LC518 contract, execution protocol and fixed held-out distribution. They do not establish a universal law of solver correctness or transport to natural/independently generated solvers or other tasks.

---

### Carried-forward analysis and reporting protections

The following v1.0 disciplines remain part of the proposed analysis plan and are not waived by the revised E3 specification:

1. **One frozen analysis pass.** Stop after one frozen analysis pass. If data, coverage or unresolved outcomes make a fold or arm not estimable, report NOT_ESTIMABLE with the precise reason. Do not collect more data, change features, or rerun automatically with a replacement model.
2. **Outcome zero-variance sanity check.** If every solver body across every parent group has the same held-out correctness score Q, report ZERO_VARIANCE, not a prediction result. Apply this check only after the strict all-12,000-resolved gate has passed; unresolved outcomes already make E3 NOT_ESTIMABLE.
3. **Coverage in every results table.** Every table reports coverage and unresolved counts alongside failure counts.
4. **Preserve successful executions.** Preserve successful executions and their evidence, not only failures. Typed manifestation records remain available; binary summaries are derived views.

## 8. Frozen-to-revised feature reconciliation

The following table makes explicit how the v1.0 frozen feature inventory is represented in this review draft. It does not modify the frozen v1.0 document.

| Frozen v1.0 column or obligation | Revision 2 disposition | Treatment |
|---|---|---|
| d_pass_s | Retained | Model C predictor, per D1–D8. |
| d_wrong_answer_s | Retained | Model C predictor, per D1–D8. |
| d_invalid_return_s | Retained | Model C predictor, per D1–D8. |
| d_exception_s | Retained | Model C predictor, per D1–D8. |
| d_unresolved_s | Restored | Model C predictor and coverage count, per D1–D8; never a failure count. |
| d_meandev_s | Retained with accepted C4 definition | Zero sentinel when undefined, with companion d_meandev_s_defined. |
| d_meandev_s_defined | Restored | Model C predictor; reports whether a numerical mean exists. |
| d_maxdev_s | Retained with accepted C4 definition | Zero sentinel when undefined, with companion d_maxdev_s_defined. |
| d_maxdev_s_defined | Restored | Model C predictor; reports whether a numerical maximum exists. |
| d_other_s | Added under accepted C5 correction | Counts explicitly defined other FAIL manifestations, excluding timeout/resource breach. |
| d_timeout_s | Restored as reserved | Null now; excluded from the design matrix while null. May be populated only after a separately authorized execution protocol and pre-run feature freeze. |
| d_order_pairs_resolved | Restored under accepted C6 correction | Model C predictor; count of D6 pairs with both orderings resolved. |
| d_order_pairs_comparable | Restored under accepted C6 correction | Model C predictor and denominator for the descriptive order-inconsistency rate. |
| d_order_inconsistent | Restored under accepted C6 correction | Model C predictor; count of comparable pairs whose returned exact integers differ. |
| k_fail | Retained | Aggregate count of all definite diagnostic FAIL outcomes. |
| k_unresolved | Retained | Aggregate count of UNRESOLVED diagnostic outcomes. |
| family Z | Retained | Parent algorithm family context in Model A/B/C. |
| coverage_diag | Restored as report-only aggregate | Calculated as 1 - k_unresolved/64; excluded from predictor matrices as an affine duplicate of k_unresolved. |
| Reserved timeout/resource per-stratum count obligation | Restored explicitly as d_timeout_s | Null and excluded from the matrix until the separate protocol gate is satisfied. |

The accepted C4/C5/C6/C7 corrections are represented in the revised definitions above. The original v1.0 ANALYSIS_SPEC.md, BANK_DESIGN.md, PARENT_DESIGN.md and GLM_WORK_ORDER.md remain unchanged.

### Procedure-level changes from frozen v1.0

The feature reconciliation above is complemented by the following procedure-level changes. These are explicit proposed revisions, not silent edits to the frozen v1.0 source:

| Frozen v1.0 provision | Revision 2.6 disposition |
|---|---|
| Linear k_fail predictor in the E3 baseline | Replaced for E3 by the six-column primary basis with knots 1, 2, 3 and 4, subject to the proposed specification's ratification. |
| Two E3 arms (baseline and enriched profile) | Replaced by Models A, B and C, with separate A-versus-B and A-versus-C exploratory comparisons. B+profile remains out of scope. |
| Ambiguous lowest inner-fold mean squared prediction error | Pinned to one pooled MSE over all 145 inner-validation body predictions, equal to the unweighted mean of the 29 parent-group MSEs. |
| NaN for undefined deviation summaries | Replaced in the proposed E3 profile by a zero sentinel plus the corresponding _defined indicator. |
| No explicit alpha tie rule | Larger alpha wins an exact tie. |

Upon formal ratification only, revision 2.6 supersedes frozen ANALYSIS_SPEC.md v1.0 §§4 and 6 for the secondary E3 analysis. It does not supersede §3 (E1), §5 (E2), or §§7–10, which remain in force. Until ratification, the historical v1.0 documents remain the design-of-record sources; this review draft does not currently supersede them.

## 9. Freeze and authorization boundary

This document remains a review draft. It is not a freeze attestation and does not modify the design-of-record files. No study bank has been generated by this revision; no solver body has been constructed, imported or executed; no private mutation annex has been accessed; no predictive model has been fitted; no power study has been run.

Bank generation, construction of the 150 solver bodies, private-annex access, candidate execution, dynamic mutation validation, predictive fitting and power simulation remain separately gated operations. Publication of this review package on the designated review-only branch does not authorize any of those operations and does not authorize a merge to master.
