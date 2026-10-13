# ADDENDUM C — RECORD CORRECTIONS AND V1 RETRY OUTCOME (2026-10-13)

Provenance: prepared 2026-10-13 at GPT's direction (review disposition: "record corrections required; dated
addendum"). This addendum amends the freeze-candidate record without rewriting any prior commit or log.
Original commits and raw logs are preserved verbatim; everything below is either a correction of the record
(text/hashes updated in the candidate files) or a statement of new, raw-cited fact.

Status context (unchanged): `rlc0-freeze` tag NOT created; Phase C NOT authorized; six seeds NOT compiled,
executed, or analyzed by CBMC; C3 independent hash/tag review OPEN; C2 remains OPEN (see section 5).

## 1. V1 bounded retry: executed, outcome TIMEOUT, stopping rule applied

The GPT-authorized bounded retry of V1 (field-sensitivity flag experiment) — previously recorded NOT RUN —
was executed 2026-10-13 under the bounded runner:

- Command (frozen baseline + the single authorized flag `--max-field-sensitivity-array-size 20000`):
  `cbmc.exe canary_n63_IN_F.exe --function main --unwind 64 --unwindset
  "rlc0_build(ptr_struct_tag(identifier=tag-rlc0_input)).0:10001" --unwinding-assertions --bounds-check
  --pointer-check --max-field-sensitivity-array-size 20000`
- Runner: `run_bounded.ps1` v5.1 (job-object hard 8 GB, 1800 s wall watchdog).
- Raw record: `evidence/C2/raw/V1_STATUS.txt` (appended section "AUTHORIZED BOUNDED RETRY"),
  `evidence/C2/raw/v1retry_n63_IN_F.txt`, `.err.txt`, `.status.txt`.

OUTCOME: **WALL_TIMEOUT** (verbatim fields):

```
start:                2026-10-13T18:58:08.5634159+01:00
end:                  2026-10-13T19:28:10.8187753+01:00
elapsed_sec:          1802.3 (budget 1800; killed by watchdog)
mem_budget_bytes:     8589934592
peak_private_bytes:   88670208  (84.6 MiB — well below 8 GB; not an OOM)
exit_code:            none (process tree killed)
stdout:               ends at "Starting Bounded Model Checking"
stderr:               empty
leftover processes:   0
```

**No CBMC verification result exists for the V1 retry.** Never cite this run as SUCCESS, FAILURE, ERROR,
or any other CBMC verdict. The original V1 attempt remains INTERRUPTED/INCONCLUSIVE (preserved verbatim in
V1_STATUS.txt lines 1–30); the retry record is appended, not substituted.

STOPPING RULE (GPT 2026-10-13), now triggered: V1 is inconclusive under the existing limits. STOP. No
`--slice-formula`, no `--refine-arrays`, no other solver, no larger resource budget, no other compiler
version, no further configuration experiment without a new explicit decision.

Scoped statement of record: *full-domain certification was not demonstrated under this pinned stack
(CBMC 6.11.0 + goto-cl / MSVC 18.10.2), this harness, and this budget (1800 s / 8 GB).* This is not a
claim of universal impossibility.

Status correction: FREEZE.md section 8 previously recorded V1 as "INTERRUPTED/INCONCLUSIVE"; it is now
INTERRUPTED (original attempt) + **TIMEOUT** (authorized retry), stopping rule applied.

## 2. `.gitignore`: empty file — the hash was correct; the record now explains it

Verified 2026-10-13:

- File `rlc0/.gitignore` exists and is **0 bytes** (empty file).
- SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` — this is the canonical
  SHA-256 of the empty string, i.e. the hash was never wrong; it hashed zero bytes.
- Git blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` (git's canonical empty blob).
- History: `git log --follow --stat` shows `55b6ca2` created `rlc0/.gitignore` as a **rename-copy of the
  empty `study/__init__.py`** (similarity 100%, 0 insertions, 0 deletions — a copy with no content), and
  `8e8daf9` shows `study/__init__.py` as an empty-file add as part of the same copy pair. No commit ever
  added a line to `rlc0/.gitignore`; it has always been empty.

Explanation of record: the entry in the section 5 hash table is a consistency check over a 0-byte file,
not evidence of a hashing failure or of truncated content. The file is intentionally left as-is (changing
it would itself change a recorded hash); this explanation discharges the review item.

## 3. C1 model-versus-real correspondence: ACCEPTED, BOUNDED SCOPE

GPT disposition 2026-10-13: **C1 = ACCEPTED, BOUNDED SCOPE.** The acceptance covers the frozen operation
set actually used by the study: `std::vector::size()` and in-bounds `operator[]` as encoded in
`rlc0/model/vector` versus the native MSVC STL implementation, supported by (a) the B0.5 differential
evidence (`evidence/B0.5/`: 17/17 identical outputs on cases all inside D across the seed operation set,
byte-identical transcripts, native builds exit 0) and (b) the source-level semantic argument with its
stated limits. It is **not** an equivalence claim for arbitrary std::vector operations, out-of-bounds
behavior (UB in ordinary C++; excluded by design and monitored by the model's index assertion), or any
API beyond the frozen set.

FREEZE.md section 6.1 wording updated accordingly (was "C1 STILL OPEN pending reviewer adequacy
judgment"). The B0.5 evidence text itself is not modified.

## 4. Frozen-command record: `--unwindset` and the full goto-cl line

The command actually executed in every recorded CBMC run (all `.status.txt` sidecars in
`evidence/C2/raw/`) includes:

```
--unwindset "rlc0_build(ptr_struct_tag(identifier=tag-rlc0_input)).0:10001"
```

alongside `--unwind 64` (which remains the global bound for all other loops). The pre-correction record
in `spec.json` (`toolchain.model_route.frozen_cbmc_commands` and `tier3_cbmc.flags`) and FREEZE.md
sections 1/4 omitted the unwindset, and the recorded goto-cl line omitted the `/I` harness include and
the `/D` defines. Both are now amended to match the executed commands exactly:

- `spec.json` frozen line (cbmc): `cbmc.exe <file>.exe --function main --unwind 64 --unwindset
  "rlc0_build(ptr_struct_tag(identifier=tag-rlc0_input)).0:10001" --unwinding-assertions --bounds-check
  --pointer-check`
- `spec.json` frozen line (goto-cl): the full `build_all.cmd` invocation with model + harness `/I`,
  `/DRLC0_SOLVER_HEADER=canary_<x>.h /DOBL_<OBL>`, and the harness source path.
- A `frozen_cbmc_commands_note` records this amendment and its date in `spec.json` itself.
- FREEZE.md sections 1 and 4 amended to the same text.

Rationale of record: the harness loop `rlc0_build` requires ≥10001 unwind for `n = 10000`; the study
would otherwise cut the path via a failed unwinding assertion (vacuous SUCCESS risk). This was always
part of the executed procedure; only the written record lagged.

## 5. Contract timing scope + seed-6 nontermination evidence rule (pre-registered)

### 5.1 Timing scope (contract issue resolved before freeze)

CONTRACT.md section 4 amended (dated sentence): the 1000 ms per-input threshold is an **operational
failure detector for finite native executions (Tiers 1–2)**. An observed timeout is recorded with its
execution environment and raw result — an observed timeout under that environment, not a mathematical
proof of infinite looping. Certificates (NO_FAILURE, CERTIFIED_LOCALIZED) claim functional correctness,
memory safety, and **mathematical termination** (frozen unwind bound + unwinding assertions — a
state-transition/loop-bound argument); they do NOT assert that every input completes within 1000 ms on
any machine. CBMC does not prove real-time completion. Mirrored in `spec.json` under
`failure.timeout_scope`.

### 5.2 Nontermination evidence rule (pre-registered; applies before any authorized seed execution)

Recorded in `spec.json` `failure.nontermination_evidence_rule`:

- **Primary:** a mathematical state-transition argument over the frozen witness. For seed 6 (witness
  `nums [0,2] target 1`), `seeds/seed6.cpp` executes `left = mid` with
  `mid = left + (right - left) / 2`; when `nums[mid] < target`, `left` is unchanged while
  `left <= right` remains true, so the machine state repeats and the loop cannot terminate. The argument
  must cite exact source lines. Source confirmed 2026-10-13: `left = mid` is present in seed6.cpp.
- **Corroborating (native):** a native run of the witness exceeding 1000 ms is an **observed timeout in
  that environment** — record environment and raw result; never call it proof of infinite looping.
- **Corroborating (CBMC):** a violated unwinding assertion on `Solution::search` is **corroboration only**
  — it shows the selected bound was insufficient to establish termination; never sufficient alone.
- **Insufficient alone:** an unwinding-assertion failure by itself; a native timeout presented as proof.

## 6. CBMC property set actually emitted (documented)

Recorded from `evidence/C2/raw/cbmc_canary_n63_IN_F.txt` (canary_n63_IN_F, frozen command):

| Class | Count |
|---|---|
| pointer_dereference | 114 |
| signed_overflow | 7 (`search.overflow.1..5`, `rlc0_build.overflow.1..2`) |
| array_bounds | 5 (`rlc0_build.array_bounds.1..5`) |
| user assertions (`__CPROVER_assert`) | 4 (`rlc0_assert_correct.assertion.1..3`, `operator[].assertion.1`) |
| unwinding assertion | 1 (`search.unwind.0`) |
| **Total** | **131** |

- `probe_domain` emitted 82 properties.
- Result states in the baseline run: 112 SUCCESS, 19 ERROR (ERROR = in-flight property at SAT-checker
  OOM → INCOMPLETE, never a pass/fail verdict).
- Notes: CBMC 6.x emits the standard checks by default (bounds/pointer/signed-overflow/unwinding); the
  signed-overflow properties appear although no `--overflow-check` flag is passed (default UB checking in
  6.11.0). No `rlc0_build.unwind` property was emitted — unwindset 10001 covers the harness loop, so its
  unwinding assertion holds by construction.

Machine-readable copy: `spec.json` `tier3_cbmc.property_set_observed`.

## 7. Harness sources: per-file hashes (now listed in FREEZE.md)

```
24c1301f6300fbf6cf9e64bab22027aa2fab503f178751de629a945629979d53  harness/proof_harness.h
5dad1193d4eec1d629886a7f73d5646108be31898ceeead12bf7b5ed4bd94a9d  harness/proof_main.cpp
f616f9f57765291a49a23681cd9d4bbb3ef3e9a5303779d3059cf3a4fecaf72f  harness/canary_n63.h
b45d8e52fb90b101be01f984a279a2063b49856f90e76537403e2933b6b59a70  harness/canary_large.h
```

Same four values already listed in `evidence/C2/RESULTS.md`; FREEZE.md section 5.3 now carries them in
the freeze record itself.

## 8. Evidence manifest

`evidence/C2/MANIFEST.sha256` covers **all 78 files** in `evidence/C2/raw/` (75 at the C2 package commit
`cfb709b`, plus the 3 V1-retry sidecars added with this addendum). The manifest file itself is hashed in
FREEZE.md section 5.4. Independent recompute command for the reviewer (section 7 of FREEZE.md):

```powershell
cd ...\rlc0\evidence\C2
Get-ChildItem raw -File | Get-FileHash -Algorithm SHA256 |
  ForEach-Object { $_.Hash.ToLower() + "  raw/" + $_.Name } |
  Set-Content -Encoding ascii _recomputed.sha256
fc.exe /W MANIFEST.sha256 _recomputed.sha256   # expect no differences
Get-FileHash -Algorithm SHA256 MANIFEST.sha256
```

## 9. C2 domain-coverage gap: stays OPEN; earlier overclaim withdrawn

GPT review: D1–D9 probe results (D1 FAILURE as expected; D2–D9 SUCCESS) show `n = 10000` reachable and
each constraint class enforced, but do **not** establish universal representability of every boundary and
partition combination of the declared domain D. The FREEZE.md section 6.2 sentence "The harness
represents the full declared domain ... verified by the domain probe" **overclaimed** and is rewritten:
reachability evidence is recorded at source level (constraint audit) and the coverage question remains
**OPEN** as part of C2. No new probe series is run.

## 10. Supersessions and hash changes

Supersessions (prior text preserved in its original commits; superseded here):

- `evidence/C2/RESULTS.md` §9 item 4 (C1 OPEN) → superseded by section 3 (ACCEPTED, BOUNDED SCOPE).
- `evidence/C2/RESULTS.md` §9 item 6 (V1 pending) → superseded by section 1 (TIMEOUT, stopping rule).
- FREEZE.md §6.1 C1 status, §6.2 domain-coverage wording, §8 V1 status → updated as cited above.
- FREEZE.md §5.2's "spec.json frozen_cbmc_commands missing the required --unwindset" OPEN item →
  discharged by section 4.

Frozen-file hash changes caused by this addendum (old → new; old values were correct at their commit;
originals preserved in git history, no amend):

```
CONTRACT.md  1cd457f4b60bf0c591876445e82fdc7082fab4c6e82d4fbbfe3e18b7c22eb67c
           -> 87605031e646ddfd95a2646a92cb8f0684c065835e2756d447f8c9b412aba24e
spec.json    cd9e1e7f952c621d624d45e27548224232ed9318b2a6f4f0743f8eb62f625e4e
           -> b42a0f1a988d2cee19b13f52b3bba51146a472fa07c96d28bb65e9616f741376
```

All other section 5 hashes unchanged; section 5 regenerated with this addendum's own hash and the
manifest hash added. FREEZE.md remains self-excluded from section 5 (covered by the git commit).

C2 remains **OPEN** (canary FAIL not observed: all six baseline invocations ended in cbmc-internal SAT
OOM, exit 6, INCOMPLETE — never SUCCESS, never FAILED; V1 retry TIMEOUT; domain coverage per section 9).
Final freeze + `rlc0-freeze` remain NOT AUTHORIZED; Phase C remains PROHIBITED.
