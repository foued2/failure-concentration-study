# Natural-Solver Route Closure and Measurement-Validity Record

Status: **`CLOSURE_RECORD_FOR_APPROVAL_NO_AUTHORIZATION`**

Date: 2026-10-22

Baseline commit: `766b3788d22b8591b24020753f71fd9a17875d7a`

This is a draft closure record for Foued's review. It makes no model calls,
selects no task, changes no frozen artifact, and authorizes no generation. It
records the recommended disposition of the natural-solver route; closure takes
effect only on explicit approval.

## 1. Scope and decision

The recommendation is to close the **natural-solver generation route** for this
program. This is an owner decision under the current program. It is not proof
that the underlying research question is unanswerable, not a claim that failure
concentration has no relationship to correctness, and not a closure of the
broader research question.

The recommendation is not a request for a better-run version of the same
experiment, nor for another deliberately engineered solver population. LC518
already tried the engineered route. The current operationalization has
mathematical-attainability, empirical-attainability, and construct-validity
failures. More samples from the same definition would not automatically repair
any of them.

Run count and task-family count are separate:

- **Three completed feasibility runs:** Codex SSSP, Gemini SSSP, and Gemini
  expression.
- **Two task families:** SSSP and expression.
- No further natural-solver generation is authorized under this closure.

The recommended decision is:

> Stop further natural-solver generation, record a bounded negative feasibility
> result, the attainability failures, and the measurement-validity failure, and
> preserve the frozen and uncommitted preparation for audit.

## 2. The central finding

The project did not merely fail to collect enough samples. It failed to establish
three separate things before building an experimental pipeline:

1. **Mathematical attainability.** The proposed concentration values must be
   possible under the bank's family and probe structure.
2. **Empirical attainability.** Natural generation must actually produce bodies
   that populate the required `(k, C)` combinations with distinct behavior.
3. **Construct validity.** The measured quantity must represent the property the
   research question is about, not merely a property of the test taxonomy.

The first two are design and feasibility failures. The third challenges whether
the current measurement tests the original idea at all. All three should have
been examined before the pipeline was built.

The honest assessment is that the present definition, with these banks, did not
establish concentration as an attainable predictor of generalization. The
experiments were not a successful test of the original idea. They are records of
what was actually operationalized.

## 3. Mathematical attainability

The frozen expression banks each contain 30 probes, with exactly five probes in
each of six families. The bank manifest records this structure and the bank
hashes:

- diagnostic: `ca1ba993ba3bcc6c3c2d011c49cd51e0f5eb32ff8f8cb0421768553c47507847`
- evaluation: `e227c24d9bfea7f734b3a249015d33f15d3a2619e62ff5f3a4d8a557e163946d`

Because a family can contain at most five failures, for `k > 0`:

```text
C_max(k) = min(1, 5/k)
```

The power grid in `10_OFFLINE_POWER_SIMULATION_REPORT_2026-10-22.md` used
`C_high = 1.0` for every `k`. That is infeasible at `k = 6, 12, 24` under the
five-probe family structure.

| `k` | Proposed low `C` | Proposed high `C` | Feasible maximum `C` | Status |
| ---: | ---: | ---: | ---: | --- |
| 2 | 0.500 | 1.000 | 1.000 | feasible |
| 6 | 0.167 | 1.000 | 0.833 | high cell impossible |
| 12 | 0.167 | 1.000 | 0.417 | high cell impossible |
| 24 | 0.167 | 1.000 | 0.208 | high cell impossible |

The low-concentration formula `ceil(k/6)/k` is attainable for these levels. The
defect is the attempted comparison with `C = 1` when more than five probes fail.

The invalidation means the reported **numerical power and request estimates are
invalid for operational planning** under the intended design. It does not mean
that every calculation executed by the simulation script is necessarily
erroneous. No corrected simulation is necessary to decide whether to close the
route.

Any future simulation must first derive the feasible `(k, C)` set from the bank's
actual family and probe structure, and only then choose cells and effect sizes.
It must not choose `C` levels first and check feasibility afterward. In the
expression design, the observed high-`k` bodies were crash or whole-suite
failures; the `k=30` group is an extreme instance of that pattern, not evidence
of six distinct semantic defect families.

The simulation's `beta` was a slope per unit `C`. A high-versus-low group
difference is not interchangeable with that slope when the attainable `C` gap
varies by `k`. The report's conversion to a high-low score difference is not valid
for the proposed grid.

## 4. Empirical attainability

Three completed feasibility runs across two task families produced no qualifying
fixed-`k`, different-`C` comparison with behavioral diversity and evaluation
separation.

The expression pilot produced 19 eligible bodies:

- six `k=0`;
- nine `k=2, C=1.0`;
- one `k=7`;
- three `k=30` crash bodies.

The nine `k=2` bodies were source-distinct but shared one observed
whitespace-normalization defect. The three `k=30` bodies produced 180/180
crashes, not six semantic defect families.

The two outcomes that dominate the data are a shared bug or total breakdown. In
both cases, concentration is largely determined by `k` and supplies little
independent information. The occurrence probability of useful cells under an
untested task or generator remains unknown. If a required cell has zero
probability, no finite request budget can populate it. If its probability is
small, the required budget may be much larger than the invalidated simulation
suggested.

No request count is claimed here as what a future study would require.

## 5. Construct validity

The current concentration measure is not an intrinsic property of a solver. It
depends on the task, the test bank, the number of probes per family, and the way
failures are partitioned into families. Change the taxonomy and the same program
can receive a different `C`.

At `k=2`, two failures can fall in one family (`C=1`) or in two families
(`C=0.5`). Those values are attainable. Variation in `C` does not establish that
the difference has predictive meaning.

The deeper problem is coverage. `C` is computed only from failures in families
the experimenters already imagined. A program with the wrong underlying approach
can pass every anticipated probe and receive `k=0, C=0`, the same score as a
correct program. The measure is blind precisely where the original idea is most
important: at structural boundaries or unseen requirements not represented in the
initial bank.

The earlier v0.2 audit also found an identifiability limitation: on the eligible
support, `C` was deterministic given `k`. That is consistent with the central
problem here: the design did not create enough independent variation for the
measure to carry the intended information.

Concentration was intended to say something about whether a solver's approach was
adequate, not merely how its known failures were grouped. The project did not
establish that the current `C` measures approach adequacy. The construct-validity
gap is the main reason the present definition cannot support the original
predictive claim.

This is a judgment about the current operationalization. It is not a mathematical
proof that no concentration-based measure could ever work, and it is not a finding
that the broader idea is false.

## 6. What this does and does not establish

This closure does not establish:

- that failure concentration is unrelated to correctness;
- that all natural-solver tasks will fail to produce a qualifying contrast;
- that no natural solver can exhibit the required behavioral diversity;
- the occurrence probability of useful `(k, C)` cells under an untested task or
  generator;
- any number of requests as what a future study would require;
- a prevalence estimate, a causal effect, or a general natural-solver result;
- that the expression pilot or the proposed design was a clean test of the
  concentration hypothesis;
- that the current measure is an adequate operationalization of the original
  idea.

The negative result is bounded by the tested tasks, generators, prompts, caps,
banks, and execution procedure. It is a feasibility and measurement-validity
failure, not a predictive null about concentration.

## 7. Disposition of uncommitted preparation

These files are preserved for audit but are **not approved** and must not be used
as a launch design:

- `next-task/09_NEXT_STUDY_DESIGN_AMENDMENT_2026-10-22.md`;
- `next-task/10_OFFLINE_POWER_SIMULATION_REPORT_2026-10-22.md`;
- `next-task/power_simulation/`.

`10` is invalidated for the proposed grid by the `C_max` constraint. Its
conditional request estimates are not operational forecasts. Its recommendation
to consider `beta = 0.10` is withdrawn: selecting the effect size to fit the
budget would be circular. A study powered only for a ten-percentage-point
difference could be useful only if that threshold were independently justified;
a null result would not establish the absence of smaller effects.

The invalidation banners apply to the numerical estimates in `10` and to the
infeasible `C` grid. They do not invalidate every component of `09`. The
continuous score `S`, the execution-eligibility rule, and the checkable
structural task criteria are sound design components that would carry over to a
future study. "Preserved but invalid" means the numbers are not operational; it
does not mean discard the reusable design.

The uncommitted preparation should be preserved, not deleted, and should be
marked as superseded by this closure record if the repository is later committed.

## 8. Preserved records

No frozen record is changed:

- `next-task/banks/diagnostic.json`, `evaluation.json`, `BUILD_MANIFEST.json`, and
  `FREEZE.json`;
- `next-task/03_PILOT_PREREGISTRATION_2026-10-22.md`,
  `03A_PREREGISTRATION_AMENDMENT_2026-10-22.md`,
  `03B_OUTPUT_CONTRACT_AMENDMENT_2026-10-22.md`, and
  `03C_PILOT_LAUNCH_PRECONDITIONS_2026-10-22.md`;
- `next-task/04_READINESS_REPORT_2026-10-22.md`,
  `05_EXPRESSION_RUNNER_READINESS_2026-10-22.md`, and
  `06_EXPRESSION_PILOT_RESULT_2026-10-22.md`;
- `next-task/07_EXPRESSION_PILOT_AUDIT_2026-10-22.md` and
  `08_RESEARCH_DECISION_MEMO_2026-10-22.md`;
- the expression pilot run directory, attempts, raw captures, and
  `PILOT_RESULTS.json`;
- the SSSP runs, `README.md`, and the `v02` records.

## 9. Future boundaries and conceptual review gate

- No further natural-solver generation is authorized by this record.
- There is no fourth task, no fallback task, no task search, and no
  outcome-dependent retry.
- Do not rerun the power simulation. Do not invent a replacement metric to keep
  the project moving.
- Do not build another test bank or run another model until the conceptual claim
  is stated and checked on paper.
- A provider outage does not create a new task-level study.
- The closure is an owner decision under the current program; it is not a finding
  that the research question is unanswerable or that a future natural-solver
  design cannot succeed.
- The engineered-solvers route has already been tried in LC518; it is not a new
  option (section 10). No further synthetic study is authorized by this record.
- Any future engineered design would require a new explicit decision and separate
  authorization. It must not substitute for natural evidence. If ever
  reconsidered, its conditional-independence null would be `S ⟂ C | k` using the
  continuous evaluation score `S`, and its cells must obey the same `C_max`
  constraint derived from its own bank structure.
- Any future natural-solver work requires a new explicit research decision, not
  a revision of this closure record.

Only after closure should anyone consider a conceptual review of the underlying
hypothesis. That review must happen on paper, without generating programs or
building another bank. It must answer:

1. What property of a solution are we trying to infer from its observed failures?
2. What observable evidence could distinguish a fundamentally inadequate approach
   from an adequate one that merely has a local bug?
3. Under what conditions could that evidence be informative about future
   challenges, including structural boundaries not represented in the initial
   tests?

If those questions cannot be answered without quietly redefining the theory to
fit whatever data can be collected, the project should not proceed to
experimentation.

## 10. Relation to LC518

The engineered-solvers route is not a future option. LC518 already constructed 90
intended solvers, 30 each from GPT, Claude, and GLM, with deliberately different
failure behaviors. As reported in the summaries Foued supplied, the investigation
found a reproducible 76/14 clustering partition, robust across 504 methodological
perturbations and nontrivial under the tested nulls. Follow-up analysis attributed
the partition primarily to the brute-force/execution-effort boundary; a single
cost-proxy feature recovered it at ARI approximately 0.94, and the hidden-structure
claim was retired. The primary LC518 artifacts are outside this clean-room
repository and were not re-verified here.

LC518 is important, but it does not establish concentration's incremental
predictive value. It varied algorithm/approach and execution effort, not
concentration at fixed `k` with the algorithm held fixed. Its intended-failure
labels were designed, so the partition partly reflects the designers' assumptions.
It also had known correct answers for its constructed tasks, so it was a
bounded-oracle experiment, not the no-oracle case.

The two bodies of evidence are limited for different reasons:

- the three natural runs produced too little behavioral variety to populate a
  fixed-`k`, different-`C` comparison;
- LC518 produced a strong, reproducible split, but that split was primarily
  approach/effort and did not isolate concentration.

They are complementary evidence about feasibility and construct validity, not a
successful test of the original idea. Laying them side by side is a paper
exercise and should precede any new experiment, metric, or test bank.

## 11. Not done

- A side-by-side comparison of LC518 and the three natural runs: what was varied,
  what was held fixed, what was measured, whether an oracle existed, and which
  hypothesis each tested. It is paper-only; blank cells must remain blank rather
  than guessed.
- A paper-only conceptual review, led by Foued, of what a failure pattern should
  tell us about a solution. No tests, banks, or models until that claim is
  written in plain words.

## 12. Decision requested

Foued should approve or reject the closure. Approval would:

1. record the bounded negative feasibility result;
2. record the mathematical-attainability, empirical-attainability, and
   construct-validity failures;
3. record LC518 as prior engineered-solver evidence and its limits;
4. stop further natural-solver generation;
5. preserve the frozen and uncommitted preparation for audit;
6. leave any future engineered study available only under separate
   authorization.

No model calls, generation, task selection, bank change, commit, push, merge, or
tag is authorized by this draft.

## What this closure does not say

This record does not say that failure concentration lacks predictive value. It
does not declare the broader idea about failure patterns and solution approach
false. It does not say the research question is unanswerable, and it does not
settle what can be observed about a solver when nobody knows the right answer;
both LC518 and the natural runs used known evaluation answers. It says only that
the current operationalization, on these banks and these three runs, encountered
mathematical-attainability, empirical-attainability, and construct-validity
failures. The broader idea remains untouched and open.
