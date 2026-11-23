# Census operating limits — proposal v1

**Status:** PROPOSAL FOR ADOPTION. Author GLM, 2026-11-23. Executes nothing. This is the execution-
protocol pin that `PARENT_DESIGN.md` §8.3 names as a prerequisite ("Execution protocol pinning
interpreter version, runtime and memory budgets: prerequisite to any timeout/resource classification
(contract line 55) and to the reserved feature columns (work order §10)"). Without it, no diagnostic
timeout or resource event can be classified, which is one of the dormant census-authorization
conditions. All numeric limits below are DESIGN values, never observed: **zero variants have been
constructed or executed**, so no calibration data exists.

---

## L1. Interpreter and environment pin

- Single interpreter: CPython 3.12.x, exact patch version recorded at adoption time; the same version
  builds the manifest, runs the census, and classifies every timeout.
- No PyPy, no JIT variants, no NumPy or other non-stdlib runtime dependency inside solver bodies.
- Solver imports restricted to the tactics' named stdlib pieces (`functools`, `sys`, `bisect`) per
  `PARENT_DESIGN.md` §6; any other import in a constructed body is a construction defect, not a
  runtime event.
- Rationale for pinning before construction: `PARENT_DESIGN.md` §2 (F-INT) requires arbitrary-
  precision Python ints; fixed-width machine-integer tactics are pre-registered as rejected, and
  integer performance differs enough across interpreters to change which parents time out.

## L2. Resource caps (DESIGN_NOT_CALIBRATED)

Basis: the frozen complexity analysis is the only pre-execution evidence that exists.

| Parameter | Proposed design value | Derivation |
|---|---|---|
| Wall-clock cap, per diagnostic invocation (one variant x one record) | **120 s** | Heaviest population steps: K5 Cauchy product ≈ 2.5 × 10^7 cell ops, K4 doubling ≈ 2 × 10^7 (`PARENT_DESIGN.md` §3.4–3.5). A 120 s cap is a generous margin over any reasonable interpreted cell-op rate; it must be re-derived after the separately authorized calibration pilot. |
| Resident-memory cap, per diagnostic invocation | **1 GiB** | K2 full-table parents hold O(nA) ≈ 1.5 × 10^6 cells as distinct Python ints; `PARENT_DESIGN.md` §3.2 records a designed risk of several hundred MB on worst-case inputs. 1 GiB bounds that risk with margin. |
| Campaign wall-time budget | **derived at adoption** from the caps once the calibration pilot fixes realistic per-record medians | Not guessable today; recorded as TBD-AFTER-CALIBRATION. |
| Recursion | K3 parents must set `sys.setrecursionlimit(depth_bound + 200)` per the frozen depth derivation (≤ 5301 frames, `PARENT_DESIGN.md` §3.3) or use the explicit-stack tactic (G18) | Frozen design; a body violating it is a construction defect. |

A cap violation is recorded as an observation of a designed risk, never retro-fitted into the design
(`PARENT_DESIGN.md` §5 discipline), and the affected variant's records keep their terminal statuses
(DEFINITE_FAILURE / UNRESOLVED) as observed — a timeout is not silently reclassified as anything else.

## L3. Harness policy

- The harness supplies a fresh copy of every input record per invocation; solver bodies treat inputs
  as read-only (`PARENT_DESIGN.md` §6). Any detected input mutation is recorded separately.
- No network, no file reads, no printing inside solver bodies (contract §4 via `PARENT_DESIGN.md` §6).
- Every invocation produces a host-authoritative receipt: variant_id, record_id, terminal status,
  wall time, peak RSS, interpreter string, receipt SHA-256. Guest-side claims are never authoritative;
  the harness record is (same discipline as the existing guest-capture/host-authoritative splits in
  this repository).
- Clock source UTC; every timestamp RFC3339 with explicit offset, matching the schema's date-time
  format checks.

## L4. Run-start ledger discipline

- Exactly one ledger row per variant, `execution_state` ∈ {NOT_STARTED, STARTED, COMPLETED, ABORTED},
  `started_at_utc` present on every STARTED row (manifest schema 0.6 ledger description).
- The ledger is frozen (hash-identified) at every manifest build; a new execution phase produces a new
  ledger version, never an edit of a frozen one.
- `first_diagnostic_execution_started_at_utc` equals the earliest per-variant start, or null iff every
  row is NOT_STARTED — the exact reconciliation the intake checker expects.

## L5. Retry, abort and unresolved handling

- At most one retry per invocation, and only for host-side infrastructure faults (harness crash,
  OOM-kill by the OS). Outcome-bearing faults (wrong answer, timeout, exception raised by the solver)
  are never retried into a better status.
- Retry events are recorded in the run record and reported in the census; a retried invocation keeps
  the receipt of the authoritative (second) run.
- UNRESOLVED is preserved as its own terminal status; it is never converted into pass or failure
  (protocol lines 210–211, frozen), never counted into `k_fail`, and remains part of the cell identity
  only (`CD_MEASUREMENT_SPEC_2026-11-19.md` §1, §3).
- ABORTED rows carry a reason string and a timestamp; an ABORTED variant is INCOMPLETE at manifest
  level, with retained receipts as required by the schema's INCOMPLETE conditional.

## L6. What adoption of this proposal does and does not authorize

Adoption completes the operating-limits input for the census authorization. It does not authorize
construction, bank generation or access, diagnostic execution, outcome collection, or the census
itself — each remains gated by the standing authorization chain (step-1 scope record 2026-11-22; GPT's
2026-11-23 status statement; owner ratification).
