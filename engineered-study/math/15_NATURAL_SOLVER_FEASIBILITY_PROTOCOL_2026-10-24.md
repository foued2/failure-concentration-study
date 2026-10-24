# Natural-solver feasibility-first protocol

**Status: PREPARED, NOT EXECUTED.** Approved scope is limited to planning and an offline inventory of existing solver data. This document does not authorize generating solvers, calling model APIs, executing solver submissions, reopening Gate 1, or changing the frozen three-world simulation.

## 1. Research question

Can existing, independently generated, correctness-qualified solver instances provide within-family, fixed-k variation in diagnostic concentration C, with evaluation scores measured on genuinely unseen inputs? This is a feasibility audit, not a predictive-effect test.

The target research question remains whether C adds held-out predictive value beyond total diagnostic failures k. The previous synthetic W1 result failed its wiring criterion and supplies no evidence about natural solvers.

## 2. Freeze definitions before inspecting score associations

### Unit and independence

The observational unit is one solver body tied to a documented generation lineage. Exact duplicates, replicas of the same body, and outputs copied or lightly edited from a shared parent do not count as independent units. If lineage is missing or independence cannot be established from existing records, mark the unit independence-unknown and exclude it from the pass count. Do not infer independence merely from different filenames or hashes.

### Correctness and data validity

A unit must have a valid, parseable solver artifact and pass the already specified independent validity/correctness checks that establish it can be evaluated. Diagnostic failures are the measurements defining k and C; they are not by themselves grounds for excluding a solver. Invalid outputs, crashes, malformed records, or missing required measurements are ineligible and counted separately.

### Family partition and concentration

Before examining any evaluation scores or C-S association, write a plain-language rationale for the existing diagnostic-family partition: what each family represents, why family membership is meaningful for the task, and how the assignment was made independently of observed outcomes. Do not select or merge families because they improve the C contrast.

For each eligible solver, calculate F, k=sum(F), and C=max(F)/k using the frozen diagnostic mapping. C is undefined at k=0. For a meaningful concentration contrast, require k>=2; k=1 necessarily gives C=1 and cannot offer different-C variation at fixed k.

### Held-out outcome

Evaluation score S must use a predeclared evaluation suite that is independent of the diagnostic battery and has no known exact-input overlap. Record the suite identifier, its construction, the overlap check, score definition, and whether any solver or prompt selection previously used its outcomes. If these cannot be established, mark the outcome as not genuinely held out and stop.

## 3. Offline inventory only

Use existing archives and reports. Do not make new solver/API calls, regenerate cases, execute solver code, or change any evaluation bank. Deduplicate bodies; reconcile lineage; apply correctness and held-out-data checks; then tabulate counts by family, k, and C. Do not inspect or compare S values until the family rationale, inclusion rules, and stop rule are frozen and the eligible inventory is recorded.

Required descriptive output:
- counts of total units, unique bodies, replicas/duplicates, lineage-known units, correctness-qualified units, and eligible units with k>=2;
- within each prespecified family x k stratum, the number of distinct C levels and number of independent units at each level;
- counts excluded for each reason, including missing lineage, invalid artifact, k<2, and non-independent or overlapping evaluation inputs;
- hashes and provenance for every input file used.

## 4. Frozen stop rule

Apply the following deterministic disposition after the inventory; do not relax thresholds after seeing the data.

1. **BLOCKED_DATA_INTEGRITY** if input provenance, archive integrity, solver lineage, diagnostic family mapping, or held-out evaluation independence cannot be audited from existing records. Stop; do not infer or repair missing provenance.
2. **INFEASIBLE_WITH_CURRENT_DATA** if there are zero eligible same-k, different-C pairs within every prespecified family. Stop; no generation or execution is triggered automatically.
3. **VARIATION_EXISTS_BUT_INSUFFICIENT** if any qualifying pair exists but the following minimum feasibility bar is not met: at least 15 independent correctness-qualified units with k>=2 in total, and at least three distinct family x k strata where two or more C levels each have at least two independent units. Report the observed counts and stop. This threshold establishes only repeated structural overlap, not statistical power.
4. **FEASIBLE_FOR_NEXT_DESIGN_STAGE_ONLY** if the preceding minimum bar is met and the held-out suite checks pass. Report the qualifying strata and data provenance. This is permission to design a separate confirmatory protocol only; it is not evidence that C predicts S and does not authorize model fitting, new solver generation, or execution.

A data inventory can be feasible while still being underpowered for a predictive study. No predictive conclusion is allowed in this phase. Any later power analysis must use a justified variance source and be frozen before confirmatory outcomes are examined.

## 5. Constraints and provenance

- The three-world simulation remains frozen; W1 remains **FAILED**. No synthetic rerun or parameter tuning.
- Gate 1 stays closed. This is a separate audit of existing natural-solver records and cannot be used to reopen or bypass Gate 1.
- Do not upload the raw three-world archive to GitHub.
- Do not execute solver code in the host process. This phase is inventory-only and makes no model/API calls. Any later execution requires a separately authorized, reviewed isolation work order with process-tree timeout and memory limits.
- Keep raw data and original records unchanged. Write new reports in a separate analysis directory, record script and input hashes, and preserve exclusion counts.
- The same-volume archive copy is not an off-machine backup; retain that operational item on the checklist.

## 6. Deliverable and stop

Produce one inventory report and machine-readable table with the disposition from Section 4. Do not proceed to predictive modeling from this protocol alone. If the data is infeasible or insufficient, that is the result for the current archive; do not silently initiate generation to fill the gaps.

**Execution status at freeze:** Not started. No natural-solver data has been inventoried under this protocol.