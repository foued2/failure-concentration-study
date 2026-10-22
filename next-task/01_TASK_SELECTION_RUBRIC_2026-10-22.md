# New-task selection rubric

Status: fixed before task selection; no model-generation calls were made.

## Purpose

Select a task for a fairer feasibility test of the concentration question
without using model-generated failure rates or preliminary outcomes. The
rubric is deliberately static and structural. It is not a search over tasks.

## Mandatory criteria

A candidate task is eligible only if it satisfies every criterion.

1. **Deterministic reference oracle.** A host-side reference can compute the
   exact output for every input without model assistance. An independent
   oracle path or brute-force check must be available for a sample of inputs.
2. **Exact output contract.** The solver returns a single exact value with no
   floating-point tolerance, nondeterminism, or platform-dependent behavior.
3. **Meaningful boundary conditions.** The task has several independently
   describable edge conditions whose expected behavior is fixed by the
   specification, not by convention left to the solver.
4. **Multiple implementation-error families.** At least six distinct,
   prespecifiable defect classes can be triggered by structurally identifiable
   inputs. Each class must correspond to a plausible implementation mistake,
   not merely an arbitrary injected wrong answer.
5. **Separable diagnostic probes.** A diagnostic bank can contain multiple
   probes per defect class, with an exact-one structural classification and a
   deterministic expected output.
6. **Independent evaluation coverage.** Each diagnostic defect class can be
   mapped to separate evaluation inputs, generated on a different input
   identity, without reusing diagnostic inputs.
7. **Practical evaluation cost.** A body can be scored on both banks in a
   short, bounded Sandbox run with no external services, no long compilation,
   and no numerical library dependency.
8. **Simple generation surface.** A single small function with a short
   specification is sufficient; generated bodies should not fail mainly
   because of build systems, package installation, or ambiguous output format.
9. **Claim separation.** The task can be described as a different problem class
   from SSSP; results cannot be presented as a replication or extension of the
   closed SSSP feasibility runs.

## Selection rule

The criteria are conjunctive. A candidate that fails any criterion is
ineligible; no compensation by a high score on another criterion is allowed.
Select one eligible task, freeze its specification, and do not maintain a
fallback list that is tried until one produces favorable model results. If the
chosen task fails the later calibration gate, stop and report the gap; a new
task requires a new authorization.

## Exclusions

The closed SSSP task and its frozen banks are not candidates for this phase.
Any task selected because a preliminary model run produced failures is
ineligible. The rubric is applied before any new solver generation.
