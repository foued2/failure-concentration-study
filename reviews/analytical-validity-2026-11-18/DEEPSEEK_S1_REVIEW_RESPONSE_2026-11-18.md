# DeepSeek S1 review response — 2026-11-18

**Reviewer:** DeepSeek web chat.  
**Review target:** S1 known predictive-gain calibration specification v0.1.  
**Revised specification:** [S1_KNOWN_GAIN_SPEC_2026-11-18.md](S1_KNOWN_GAIN_SPEC_2026-11-18.md), v0.2.  
**Status:** DRAFT FOR SECOND DEEPSEEK REVIEW. NOT ACCEPTED, NOT FROZEN, NOT AN EXECUTION GO.

This is a response to DeepSeek's uploaded section-by-section review. It records adjudication rather than treating every criticism as automatically correct.

## Disposition summary

1. **Target population:** accepted. The v0.2 estimand is conditional on the fixed 60-item held-out panel and its equal class weights. No input-superpopulation claim is made.
2. **Scoring scale:** accepted. Bernoulli log loss is justified as a strictly proper scoring rule whose optimal predictive gain equals conditional mutual information. Brier score, AUC, and calibration error are different targets.
3. **Binary support:** accepted. \(C_D\) has only two levels, 0.50 and 0.75. This is a binary-proxy calibration, not a general concentration-distribution test.
4. **Parent marginalization:** accepted. The sum over \(H\) and \(U\) is now shown explicitly. \(U\)'s zero mean gives the marginal \(p_x\pm0.6\eta\); shared-parent dependence remains and is handled by cluster-level evaluation.
5. **Signal parameter:** partly accepted. \(\eta\) is an analyst-selected DGP parameter. The pre-run grid \(\{0.06,0.12,0.18\}\) exposes signal-strength sensitivity, with analytically derived \(\Delta^*(\eta)\) values. These values are synthetic assumptions, not empirical calibration.
6. **Full-vector information equality:** accepted and proved for this generator. \(F\) is equivalent to \((Q,A)\), with \(A\) ancillary conditional on \(Q\). Since \(C_D\) is a one-to-one function of \(Q\), the conditional mutual-information equality follows. It is explicitly called favourable and not generalized.
7. **Independent numeric gain:** accepted. The KL formula, class-specific contributions, and full \(\eta\)-grid are included.
8. **B1 alignment:** accepted. Passing S1 validates only the marginal saturated binary-proxy estimator in this generator. It does not validate B1 v1.6; a separate bridge calibration is required.
9. **Fitted-pair target:** accepted. \(\Delta_{\mathrm{fit}}\) is defined as the exact conditional population gain of the fitted pair, not an estimate of the Bayes limit \(\Delta^*\).
10. **Bootstrap scope:** accepted. Parent-cluster bootstrap intervals are conditional on fitted training functions and the fixed panel; they target replication-specific \(\Delta_{\mathrm{fit}}\), not \(\Delta^*\). Training variability is summarized across independent replications.
11. **Matched-null section:** the review's statement that §6 was missing is not accepted as a factual claim about v0.1. That section existed and specified \(\eta=0\) and \(Y=p_x+U_g\). However, v0.2 expands it to state the full unchanged hierarchy and null implications explicitly.
12. **Parent grid:** partly accepted. The v0.2 text explains geometric doubling and relative \(1/\sqrt J\) standard-error scaling. Absolute interval widths remain unknown because the parent-level variance is not yet established; no fabricated width is supplied.
13. **Tolerances:** partly accepted. The v0.2 text provides rationales and sensitivity reporting. Values remain provisional for review, not frozen.
14. **Correct specification:** accepted. The six-cell saturated estimator is favourably matched to the binary-proxy generator. No robustness to misspecification is claimed.
15. **Inference transfer:** accepted. The minimum inference supported by a pass and the non-transfer to B1 or real solvers are explicit.

## Important open matters

- Whether a fixed-panel target is adequate for the first calibration or whether a separate input-superpopulation scenario is necessary.
- Whether the binary-proxy/sufficient-summary construction is too favourable for the purpose of the first calibration.
- Whether the \(\eta\) grid and all tolerance values are defensible.
- Whether the conditional parent-cluster bootstrap is adequate for the declared \(\Delta_{\mathrm{fit}}\) target.
- What exact bridge scenario is required to validate the B1 v1.6 analysis.

No code was written, no simulation or model fit was run, no bank was reused, and no execution GO was requested or inferred.
