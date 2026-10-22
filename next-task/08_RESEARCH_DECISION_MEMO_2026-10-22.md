# Research Decision Memo

Status: **`FINAL_DECISION_MEMO_NO_AUTHORIZATION`**

Date: 2026-10-22

This memo follows the post-hoc audit in
`next-task/07_EXPRESSION_PILOT_AUDIT_2026-10-22.md`. It makes no model calls,
fits no predictive model, starts no pilot, and authorizes no generation. It is a
decision document for Foued, not a preregistration.

## Bottom line

1. The frozen expression result stands: **`REPEATED_K_BUT_NO_C_SEPARATION`**.
   The audit found no integrity defect, so the result is not reclassified.
2. The 19 eligible bodies fall into four observed groups: six `k=0` bodies, nine
   `k=2, C=1.0` bodies, one `k=7` body, and three `k=30, C=1/6` bodies. The nine
   `k=2` bodies have distinct source hashes but one observed behavioral class:
   the same missing-leading-whitespace bug replicated across nine AST evaluators.
   The three `k=30` bodies all crash; their concentration is not evidence of six
   distinct semantic defect families. The `k=7` body is a singleton.
3. The pilot therefore does not justify abandoning the concentration question,
   but its null is not a clean test of it, and it does not justify another
   expression-like task. A further natural study should be a genuinely harder,
   structurally different task, run as the third and final task-level
   natural-solver feasibility study.
4. An engineered-solvers study can test instrumentation and metric behavior under
   a known null. It cannot answer the natural-solver question, and it must not be
   used as a substitute for natural evidence.
5. Recommendation: **do not launch either route now.** If the program continues,
   make the natural-task route the primary scientific path, gated by a new
   independent task-selection rubric and a precommitted terminal rule. Treat the
   engineered study as an optional, separately labeled methodological study.

## What the audit changes

### What the records demonstrate

| Group | Bodies | Observed pattern |
| --- | ---: | --- |
| `k=0` | 6 | 30/30 diagnostic and 30/30 evaluation; baseline group |
| `k=2`, `C=1.0` | 9 | All fail `F6_0`, `F6_3`, `E6_0`, `E6_3`; 28/30 diagnostic and 28/30 evaluation |
| `k=7`, `C=5/7` | 1 | 23/30 diagnostic and 23/30 evaluation; failures in `F4` and `F6` |
| `k=30`, `C=1/6` | 3 | All 180 host-authoritative rows crash; no valid output |

Within those groups, the committed records demonstrate:

- the nine `k=2, C=1.0` bodies are source-distinct but behaviorally identical;
  they share one whitespace-normalization defect;
- the three `k=30, C=1/6` bodies all crash before producing an answer, so their
  concentration is a uniform-crash structure, not a distribution of six semantic
  defect families;
- the `k=7` group has one body and cannot support a fixed-`k` comparison;
- no bank, hash, expected-value, serialization, or scoring defect was found; and
- the execution runtime lacked `ast.Num`, while the generation specification did
  not pin the runtime or API assumptions.

### What remains inference

The records do **not** establish why the nine bodies converged on the same
behavior, or why the pilot produced only one `k=7` body. The generator, task,
prompt, sampling configuration including temperature, instruction-following
redundancy, and the shared execution contract remain possible explanations. One
pilot cannot separate them.

The correct reading of the frozen result is therefore:

> This design did not produce an informative fixed-`k` contrast within the
> declared cap.

It is not:

> Concentration is unrelated to correctness.

The audit also shows that "more model calls on the same kind of task" is unlikely
to help. The next natural task must create room for **independent partial
implementations**, not merely be harder in the ordinary sense.

## Route A: third-and-final natural-task feasibility study

This is the only route that can produce evidence about naturally generated
solvers. It stays closest to the original question.

### A1. Independent task-selection rubric, written before selection

A new rubric must be written and frozen before candidate tasks are identified.
It must not use the expression pilot's per-body outcomes, the SSSP outcomes, or
any preliminary model-generated failure rate. The existing
`01_TASK_SELECTION_RUBRIC_2026-10-22.md` can be used as a template, but the new
rubric must be independently justified for this study.

Mandatory criteria should include:

- deterministic host-side oracle and independent oracle check;
- exact output contract with no tolerance;
- at least six independently describable defect families;
- multiple diagnostic probes per family with exact structural classification;
- disjoint evaluation inputs for every family;
- several plausible **partial** implementations, not only correct or catastrophically
  broken ones;
- bounded, cheap execution in the existing Sandbox path;
- a small generation surface with a short specification;
- clear claim separation from SSSP and from the expression task.

Selection rule: choose one task, freeze it, and do not maintain a fallback list
that is tried until a favorable contrast appears. If no candidate satisfies the
rubric, stop; do not weaken the rubric to manufacture a candidate.

### A2. Prospective behavioral identity, separate from source identity

The expression pilot's identity rule and verdict remain unchanged. For any future
study, define behavioral identity prospectively and keep it distinct from source
identity:

- preserve normalized-source hashes and canonical-body counts as the source
  identity record;
- preregister a **diagnostic behavior profile** per body: family-level outcomes,
  exact failed probe set, terminal error class, and valid-output versus
  execution-failure status;
- report source-distinct and behavior-distinct counts separately;
- use the behavior profile to describe diversity and to define the future
  feasibility contrast, not to reinterpret the expression pilot;
- do not retroactively change the expression pilot's 21 canonical bodies, 19
  eligible bodies, canonical-body rule, or `REPEATED_K_BUT_NO_C_SEPARATION`
  verdict.

This is the audit's main design consequence: source diversity is not a substitute
for behavioral diversity.

### A3. Calibration gate before any generation

The next task must pass a no-model calibration gate:

- reference implementation: 30/30 diagnostic passes and 30/30 evaluation correct;
- six prespecified faulty implementations: 5/5 target-family diagnostic failures
  and 5/5 target-family evaluation failures;
- no non-target family failures;
- every row tree-terminated and not timed out;
- strict output adapter and frozen source/bank hashes;
- pinned execution runtime (CPython version and sandbox image/API assumptions) in
  the task specification and protocol, recorded in the freeze, with a preflight
  for removed aliases such as `ast.Num`;
- zero model calls and zero generation attempts during calibration.

Calibration proves that the banks can distinguish the hand-built defects. It does
not prove that natural solvers will make those defects. The audit's lesson is that
calibration coverage alone is insufficient; the task must also have a plausible
space of partial implementations that can be exercised naturally.

### A4. Pilot design, frozen before generation

- declare one or more generator/prompt conditions before generation, each with a
  fixed model, backend configuration, and request cap;
- if multiple conditions are used, report and analyze each condition separately;
  do not pool conditions unless a pooling rule is preregistered, and do not let
  generator identity become a hidden confound;
- do not select tasks, prompts, or conditions on the basis of favorable pilot
  outcomes;
- fixed one-shot request cap per condition, no retries, no replacement sampling;
- no prompt tuning, no body selection, no outcome-dependent stopping;
- exact output contract and source screen fixed before the run;
- separate diagnostic and evaluation banks, with disjoint inputs;
- host-authoritative expected values, correctness, family counts, `k`, and `C`;
- every attempt, raw response, duplicate, rejection, failure, timeout, and
  exclusion retained;
- the known guest input-visibility limitation reported, not treated as secure
  blinding;
- feasibility rule fixed in advance: a fixed-`k` group with at least two `C`
  values, each supported by at least two distinct behavioral profiles, and
  evaluation correctness differing between the profile sets. Source-distinct
  bodies are reported separately and do not satisfy the behavioral requirement by
  themselves.

No predictive model is fitted unless a qualifying contrast is found and a
separate review authorizes it.

### A5. Stopping rule

The stopping rule must be written before generation and must count at the **task
level**, not the provider-run level:

- SSSP task, including its closed and follow-up provider runs: 1;
- expression task: 2;
- the next natural task: 3, and final.

Each condition has a fixed request cap. A provider outage or API interruption is an
**operational interruption**, not a scientific negative. It must be reported as
such; it does not authorize endless retries, and the preregistration must specify
whether and how an interrupted condition may be resumed before generation.

If the next task does not produce a qualifying fixed-`k`, different-`C` comparison
with evaluation separation, the natural-solver route ends. No fourth task follows
automatically, there is no search across tasks, and there is no post-result
fallback. Any new natural-task study would require explicit authorization outside
this memo. If a qualifying contrast is found, the next step is review of the raw
evidence, not a confirmatory or predictive claim.

If Foued instead counts individual provider runs, the program has already reached
three natural-solver feasibility runs, and the correct action is to stop the
natural route now. The preregistration must state which count governs before any
generation. The conservative reading is that the next task is final.

### A6. Claims and limits

A qualifying result would support only this claim:

> Under the declared task and condition(s), using the preregistered behavioral
> profiles, banks, prompt, and execution procedure, the procedure produced a
> fixed-`k` comparison with differing `C` and differing evaluation correctness.

It would not support:

- a general claim that concentration predicts correctness;
- a prevalence estimate;
- a causal claim;
- a claim about SSSP or about natural solvers in general;
- a confirmatory claim without a separate study.

A null result would support only:

> This procedure did not produce the required comparison within the declared cap.

It would not support the claim that concentration is unrelated to correctness.

## Route B: engineered-solvers study

This is a different research question. It can validate instrumentation and metric
behavior; it cannot establish that natural solvers exhibit the same patterns.

### B1. Question

Can the planned concentration metric and analysis distinguish a known conditional
independence null from a known alternative, and what is its false-positive
behavior at fixed `k`?

### B2. Prespecified null under which concentration adds no information

The null must be stated before construction:

```text
Y ⟂ C | k
```

Evaluation correctness `Y` is conditionally independent of concentration `C` given
failure count `k`. Before construction, specify how family-failure vectors are
produced, how `C` is computed under the frozen rule, and how valid outputs, wrong
answers, crashes, and timeouts are represented. A concrete construction:

1. Fix at least two `k` levels and at least two `C` levels per `k`, with multiple
   solvers in each `(k, C)` cell.
2. For every cell, set `P(Y = 1 | k, C) = p_k`, depending only on `k`.
3. Generate the family-failure vector that realizes `C` without using `Y`.
4. Draw evaluation outcomes independently of the family allocation.
5. Analyze with a stratified or permutation test that preserves the `k` and `C`
   marginals.

Under this design, `C` adds no information about `Y` beyond `k`. The false-positive
rate is the observable check.

A separate alternative can be prespecified as a power check, for example:

```text
P(Y = 1 | k, C) = p_k + delta * g(C)
```

but it must be labeled as a **power check**, not as evidence about natural solvers.

### B3. How the design avoids manufacturing the answer

- Fix the solver/mutation space, generative model, seeds, and exclusion rules
  before observing outcomes.
- Do not select high-`C`/high-`Y` or low-`C`/low-`Y` solvers.
- Randomize family labels and evaluation assignment; do not tune the mapping after
  seeing results.
- Run the null first. Report every cell and every prespecified exclusion, not only
  favorable cells.
- Keep diagnostic and evaluation banks separate and use host-side correctness.
- Score crashes and other execution failures as execution failures, not as wrong
  answers; report their counts separately.
- Report both null and alternative results; a constructed alternative is not a
  natural finding.

The expression pilot already showed that canonical source diversity can hide
behavioral redundancy. The engineered design should therefore measure behavior on
the banks, not rely on source identity or assigned labels alone.

### B4. Claims and limits

An engineered study can support:

- the metric/estimator is calibrated under a known null;
- the analysis has a known false-positive rate;
- the pipeline can recover a prespecified alternative of a given size;
- specific instrumentation defects are detectable.

It cannot support:

- that natural solvers show a concentration-correctness relation;
- a prevalence or causal claim;
- a substitute for the natural feasibility result;
- a claim that the constructed family patterns resemble model-generated bugs.

The constructed solvers are synthetic by definition. Their family labels are
assigned by construction, so the study is a methodological check, not a natural
observation.

## Recommendation

1. **Do not launch another generation run now.** Neither route is authorized by
   this memo.
2. **Primary scientific recommendation:** stop the expression route. If the
   natural-solver program continues, make the next study the third-and-final
   task-level natural feasibility study, but only after a new independent rubric
   selects a task with a credible space of partial implementations. Do not run
   another task that differs only by surface difficulty.
3. **Engineered study:** optional and secondary. Run it only as a separately
   labeled instrument-validation study with the null above. Do not use it to
   justify a natural claim. If it reveals that the metric is not identifiable or
   the analysis is miscalibrated, fix the measurement before any natural run.
4. **Stop condition:** if no task qualifies under the new rubric, or if the
   task-level count is interpreted as already exhausted, stop the natural route.
   Do not manufacture a result with an engineered substitute.

## Decision requested

Foued should decide one of the following before any further work:

- **A. Authorize preparation only:** write the new independent rubric, the
  third-and-final preregistration, and the calibration panel, with no generation.
- **B. Authorize a separate engineered instrumentation study:** define its null,
  generative model, and claims, with no natural-solver claim.
- **C. Stop the natural-solver route:** record that the third task-level study is
  not justified and retain the engineered option only as a methodological study.

No option authorizes a generation run until a separate, explicit launch decision.
