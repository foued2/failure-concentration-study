# RLC-0 C2 — TIER-3 HARNESS AUDIT PACKAGE (non-seed, raw evidence)

Status: EXECUTED 2026-10-13 under CLAUDE's C2 request (non-seed harness work only) and GPT's resource-control directive of the same date. No seed was compiled, executed, or submitted to CBMC. Every raw log referenced below is copied verbatim in `evidence/C2/raw/`. Unresolved items are marked OPEN. Nothing in the frozen contract files was edited for this package; FREEZE.md section 5 hashes were recomputed and match (section 8).

## 1. Tier-3 proof harness source (exact file contents)

### `rlc0/harness/proof_harness.h` (1070 bytes, SHA-256 24c1301f6300fbf6cf9e64bab22027aa2fab503f178751de629a945629979d53)

```cpp
extern "C" void __CPROVER_assume(int);

#include <vector>

struct rlc0_input {
    int n;
    int buf[10000];
    int target;
    int present;
};

static void rlc0_build(rlc0_input* p) {
    __CPROVER_assume(p->n >= 1 && p->n <= 10000);
    __CPROVER_assume(p->target > -10000 && p->target < 10000);
    for (int i = 0; i < 10000; i++) {
        if (i < p->n) {
            __CPROVER_assume(p->buf[i] > -10000 && p->buf[i] < 10000);
            if (i + 1 < p->n) {
                __CPROVER_assume(p->buf[i] < p->buf[i + 1]);
            }
            if (p->buf[i] == p->target) {
                p->present = 1;
            }
        }
    }
}

static void rlc0_assert_correct(int r, int n, const int* buf, int target, int present) {
    if (r == -1) {
        __CPROVER_assert(!present, "rlc0: returned -1 but target is present");
    } else {
        __CPROVER_assert(r >= 0 && r < n, "rlc0: return value outside [0, n)");
        if (r >= 0 && r < n) {
            __CPROVER_assert(buf[r] == target, "rlc0: return index does not contain target");
        }
    }
}
```

### `rlc0/harness/proof_main.cpp` (799 bytes, SHA-256 5dad1193d4eec1d629886a7f73d5646108be31898ceeead12bf7b5ed4bd94a9d)

```cpp
#ifndef RLC0_SOLVER_HEADER
#error "RLC0_SOLVER_HEADER must be defined, e.g. /DRLC0_SOLVER_HEADER=canary_n63.h"
#endif
#define RLC0_STRINGIFY2(x) #x
#define RLC0_STRINGIFY(x) RLC0_STRINGIFY2(x)
#include RLC0_STRINGIFY(RLC0_SOLVER_HEADER)
#include "proof_harness.h"

int main() {
    rlc0_input in;
    in.present = 0;
    rlc0_build(&in);
#if defined(OBL_IN_F)
    __CPROVER_assume(in.present == 1);
#elif defined(OBL_D_F)
    __CPROVER_assume(in.present == 0);
#elif defined(OBL_FULL_D)
#else
#error "exactly one of OBL_IN_F / OBL_D_F / OBL_FULL_D must be defined"
#endif
    std::vector<int> v;
    v.m_data = in.buf;
    v.m_size = static_cast<rlc0_size_t>(in.n);
    Solution s;
    int r = s.search(v, in.target);
    rlc0_assert_correct(r, in.n, in.buf, in.target, in.present);
    return 0;
}
```

### `rlc0/harness/canary_n63.h` (578 bytes, SHA-256 f616f9f57765291a49a23681cd9d4bbb3ef3e9a5303779d3059cf3a4fecaf72f) — non-seed canary A, defect `size() >= 64 -> -2`

```cpp
#include <vector>

class Solution {
public:
    int search(std::vector<int>& nums, int target) {
        if (nums.size() >= 64) {
            return -2;
        }
        int left = 0;
        int right = static_cast<int>(nums.size()) - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            }
            if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
};
```

### `rlc0/harness/canary_large.h` (583 bytes, SHA-256 b45d8e52fb90b101be01f984a279a2063b49856f90e76537403e2933b6b59a70) — non-seed canary B, defect `size() >= 9999 -> 12345`

Identical body; only the guard differs: `if (nums.size() >= 9999) { return 12345; }`.

The six builds (2 canaries x 3 obligations) compile `proof_main.cpp` with `/DRLC0_SOLVER_HEADER=canary_<x>.h` and `/DOBL_IN_F|OBL_D_F|OBL_FULL_D`. Build log: `raw/build_all_log.txt` (all `goto-cl exit: 0`).

## 2. Exact symbolic constraints

### 2.1 Why the encoding is loop-based, not quantifier-based (raw probe evidence)

`goto-cl.exe` cannot parse `__CPROVER_forall`/`__CPROVER_exists` in any tested form. Raw probe transcripts:

`raw/probe_run_log.txt`:
```
============ probe_q compile
probe_q.cpp(10): error: parse error before '__CPROVER_forall ( unsigned i'
PARSING ERROR
goto-cl exit: 64
============ probe_split compile
probe_split.cpp(11): error: parse error before '__CPROVER_forall ( unsigned i'
PARSING ERROR
goto-cl exit: 64
```

`raw/probe2_run_log.txt` (C++ with pre-declared quantifier variable; C mode):
```
============ probe_v1 compile (C++, pre-declared quantifier variable)
probe_v1.cpp(9): error: parse error before '__CPROVER_forall ( i ;'
PARSING ERROR
goto-cl exit: 64
============ probe_c compile (C mode, declaration-form quantifier)
probe_c.c(8): error: syntax error before '('
PARSING ERROR
goto-cl exit: 64
```

`raw/probe3_run_log.txt` (C mode, `==>` / `=>` / `||` bodies; C++ form):
```
============ compile qa.c
qa.c(6): error: syntax error before '('
PARSING ERROR
============ compile qb.c
qb.c(6): error: syntax error before '('
PARSING ERROR
============ compile qc.c
qc.c(6): error: syntax error before '('
PARSING ERROR
============ compile qd.cpp
qd.cpp(6): error: parse error before '__CPROVER_forall ( unsigned i'
PARSING ERROR
```

(Probe sources `probe_q.cpp`, `probe_split.cpp`, `probe_v1.cpp`, `probe_c.c`, `qa.c`, `qb.c`, `qc.c`, `qd.cpp` are in `raw/`. The quantifier keyword exists in cbmc.exe's binary strings but not in goto-cl.exe's frontend grammar, so every form dies at parse.)

### 2.2 The constraints actually used (loop-based, equivalent on the harness shape)

All domain constraints are the `__CPROVER_assume` statements inside `rlc0_build` (section 1), applied once per index by a concrete 10000-trip loop:

1. `p->n >= 1 && p->n <= 10000` (length domain, all n reachable because the loop iterates on the fixed capacity, not on n)
2. `p->target > -10000 && p->target < 10000`
3. `i < p->n` guard => `p->buf[i] > -10000 && p->buf[i] < 10000` (element range, for every i < n)
4. `i + 1 < p->n` guard => `p->buf[i] < p->buf[i + 1]` (strict increase; for every adjacent pair in-range this covers all i < j < n by transitivity of `<` on ints)
5. presence flag: `p->buf[i] == p->target` => `p->present = 1` (family F predicate over full domain; `present` starts 0, so `present == 0` iff target absent)

Obligation selection in `proof_main.cpp`: `OBL_IN_F` => `__CPROVER_assume(in.present == 1)`; `OBL_D_F` => `__CPROVER_assume(in.present == 0)`; `OBL_FULL_D` => no extra assume (whole D).

Note (audit observation, OPEN as to spec wording): spec.json `tier3_cbmc.harness_model.elements` says "for all i < j < n: nums[i] < nums[j]"; the harness encodes the adjacent-pair form (constraint 4). Adjacent strict increase implies strict increase for all i < j < n over mathematical integers (three-way comparison is exact for int), so the encodings are equivalent for the declared domain; the wording difference is recorded here rather than edited into the frozen spec (no frozen file was modified).

### 2.3 Domain probe: constraints are active (raw)

`probe_domain.cpp` (in `raw/`) asserts 9 properties D1–D9 over `rlc0_build` output. Frozen command, run twice under identical settings (original `raw/cbmc_domain.txt`, bounded re-run `raw/r2_probe_domain.txt`) — both verbatim:

```
[main.assertion.1] line 7 D1 top of domain reachable (expect FAILURE, witness n=10000): FAILURE
[main.assertion.2] line 8 D2 upper bound enforced (expect SUCCESS): SUCCESS
[main.assertion.3] line 9 D3 strict increase active (expect SUCCESS): SUCCESS
[main.assertion.4] line 10 D4 element range active (expect SUCCESS): SUCCESS
[main.assertion.5] line 12 D5 presence flag set (expect SUCCESS): SUCCESS
[main.assertion.6] line 15 D6 presence flag clear (expect SUCCESS): SUCCESS
[main.assertion.7] line 18 D7 last element constrained at n=10000 (expect SUCCESS): SUCCESS
[main.assertion.8] line 19 D8 last pair strictly increasing at n=10000 (expect SUCCESS): SUCCESS
[main.assertion.9] line 21 D9 presence flag set at last index (expect SUCCESS): SUCCESS
** 1 of 82 failed (2 iterations)
VERIFICATION FAILED
```

D1 is a reachability probe designed to FAIL (it proves the top of the domain is reachable); D2–D9 SUCCESS prove each constraint class is enforced. Bounded-run record: `raw/r2_probe_domain.txt.status.txt` — COMPLETED, exit_code 10 (FAILED = as designed), elapsed 204 s, peak 1 728 040 960 bytes, within 1800 s / 8 GB.

## 3. Adapter (model vector <-> harness buffer)

`proof_main.cpp` lines 21–23:

```cpp
std::vector<int> v;
v.m_data = in.buf;
v.m_size = static_cast<rlc0_size_t>(in.n);
```

The adapter attaches the symbolic buffer by setting the model's public `m_data`/`m_size` fields directly — no loop, no constructor pass, no allocation: the solver under test sees exactly `buf[0..n)` through `size()` and `operator[]`. `operator[]` carries the frozen index monitor (`__CPROVER_assert(i < m_size, ...)`, model file FREEZE.md section 2, hash 6690c2ee...9b418). Include-path shadow proof (model before MSVC STL) is FREEZE.md section 3; harness compilation records: `raw/build_all_log.txt`.

## 4. Loop inventory (raw)

`cbmc.exe <canary_n63_FULL_D.exe> --show-loops` (from `raw/build_all_log.txt`):

```
Loop Solution::search(this,ref_struct_tag(identifier=std::tag-vector<signed_int>),signed_int).0:
  file ...\rlc0\harness\canary_n63.h line 11 function search

Loop rlc0_build(ptr_struct_tag(identifier=tag-rlc0_input)).0:
  file ...\rlc0\harness\proof_harness.h line 15 function rlc0_build
```

Exactly two loops per binary (canary_large identical in shape; `rlc0_assert_correct`, `main`, model `operator[]`/`size()` contain no loops):

| Loop | Body trips | Required unwind | Frozen unwind | Unwinding assertion |
|---|---|---|---|---|
| `rlc0_build ... .0` | exactly 10000 (fixed capacity, i < 10000) | 10001 | 64 via `--unwind`, overridden by `--unwindset ... .0:10001` | satisfied (guard `i < p->n` is an assume-side effect, not a break — loop runs 10000 trips unconditionally) |
| `Solution::search ... .0` | binary search: <= ceil(log2(n+1)) <= 14 for n <= 10000 (defect guards return early) | <= 14 | 64 | satisfied if <= 64 trips; a violating path would produce an unwinding-assertion FAILURE (never vacuous SUCCESS) |

The exact command used for every run (from every `.status.txt`, verbatim):

```
cbmc.exe <binary>.exe --function main --unwind 64 --unwindset rlc0_build(ptr_struct_tag(identifier=tag-rlc0_input)).0:10001 --unwinding-assertions --bounds-check --pointer-check
```

The `--unwindset 10001` is required: without it the 10000-trip build loop exceeds `--unwind 64`, its unwinding assertion fails, and the whole property is inconclusive. The unwindset ID contains no comma (comma-containing IDs break CBMC's unwindset parser — recorded during harness bring-up). OPEN item: `spec.json toolchain.model_route.frozen_cbmc_commands` currently lists the command without the unwindset; spec.json is a frozen file (hash cd9e1e7f...), so this discrepancy is reported, not edited. FREEZE.md section 1 says "Frozen CBMC flags (every invocation): --function <entry> --unwind 64 --unwinding-assertions --bounds-check --pointer-check" — also without unwindset. A record amendment is needed before final freeze (decision belongs to GPT/CLAUDE).

## 5. Non-seed full-domain canary runs through CBMC (raw)

Requirement: canaries must FAIL or report incomplete unwinding, never SUCCESS. All runs used the command in section 4. Status: NOT SATISFIED within the frozen budget — every canary invocation ended in solver OOM (INCOMPLETE, exit 6 / VERIFICATION ERROR), which is neither SUCCESS nor FAILED. No canary ever printed SUCCESS. OPEN — see section 5.4.

### 5.1 Original baseline batch (verify_all, no job object; `raw/verify_all.cmd`, `raw/cbmc_canary_*.txt`)

- `probe_domain`: COMPLETED, exit 10, D1 FAILURE + D2–D9 SUCCESS (section 2.3) — same as bounded re-run.
- `canary_n63_IN_F`: completed with `SAT checker ran out of memory` during propositional reduction, then printed all 131 property results as ERROR/success mix and `** 0 of 131 failed (1 iterations)` / `VERIFICATION ERROR` — i.e. `search.unwind.0 ... ERROR`, `operator[].assertion.1 ... ERROR`, `rlc0_assert_correct.assertion.1..3 ... ERROR`. Exit was not captured (batch tool-timed-out) but VERIFICATION ERROR is cbmc's error state: INCOMPLETE, never SUCCESS. Full raw log: `raw/cbmc_canary_n63_IN_F.txt` (16 030 bytes, 156 lines).
- `canary_n63_D_F`: partial, 378 bytes — batch itself terminated at tool timeout while stuck in `Running propositional reduction`. Raw: `raw/cbmc_canary_n63_D_F.txt`.
- `canary_n63_FULL_D`, `canary_large_*`: never started (batch killed).

### 5.2 Bounded round 1 (run_bounded v4, 1 s memory poll — killed, overshoot recorded)

All six canaries: `outcome: MEMORY_LIMIT`, elapsed 98.9–108.1 s, peak 8 764 260 352–10 260 451 328 bytes (poll overshoot above the 8 589 934 592-byte budget documented in status notes). Raw: `raw/base_canary_*.txt` + `.status.txt`. INCOMPLETE, not a verification verdict.

### 5.3 Bounded round 2 (run_bounded v5.1, kernel job object hard 8 GB cap) — authoritative bounded record

Command, all six: section 4 command. Common stdout (verbatim, e.g. `raw/r2_canary_n63_IN_F.txt`):

```
CBMC version 6.11.0 (cbmc-6.11.0) 64-bit x86_64 windows
Reading GOTO program from file canary_n63_IN_F.exe
Generating GOTO Program
Adding CPROVER library (x86_64)
Removal of function pointers and virtual functions
Generic Property Instrumentation
Starting Bounded Model Checking
Passing problem to propositional reduction
converting SSA
```

Common stderr (verbatim, e.g. `raw/r2_canary_n63_IN_F.txt.err.txt`):

```
SAT checker ran out of memory
Solver ran out of memory during propositional reduction.
Try reducing the problem size or increasing available memory.
Out of memory
```

All six status records (`raw/r2_canary_*.txt.status.txt`), verbatim fields:

| label | start | elapsed_s | peak_private_bytes | outcome | exit_code |
|---|---|---|---|---|---|
| r2_canary_n63_IN_F | 13:06:06 | 107.4 | 7 783 809 024 | COMPLETED | 6 |
| r2_canary_n63_D_F | 13:07:54 | 105.4 | 7 794 507 776 | COMPLETED | 6 |
| r2_canary_n63_FULL_D | 13:09:39 | 105.4 | 7 784 468 480 | COMPLETED | 6 |
| r2_canary_large_IN_F | 13:12:01 | 105.8 | 7 787 364 352 | COMPLETED | 6 |
| r2_canary_large_D_F | 13:13:47 | 104.9 | 7 785 750 528 | COMPLETED | 6 |
| r2_canary_large_FULL_D | 13:15:33 | 105.3 | 7 785 648 128 | COMPLETED | 6 |

(Start/end times from each status file's `start:`/`end:` fields in `raw/`.) All: `mem_budget_bytes: 8589934592`, `mem_enforcement: job_object(True) poll_ms=250`, `wall_budget_sec: 1800`. Exit 6 = cbmc error state (SAT OOM during propositional reduction): no `** N of M failed` line, no `VERIFICATION` line — INCOMPLETE, never SUCCESS, never FAILED.

### 5.4 Canary-FAIL status: OPEN

The two defect canaries were designed to produce a concrete in-F failure (wrong return `n >= 64 -> -2` / `n >= 9999 -> 12345` under `OBL_IN_F`). Within the frozen 1800 s / 8 GB budget the SAT instance for a 10000-capacity symbolic buffer + 64-unwind binary search exceeds available memory during propositional reduction, so no FAIL (and no unwinding-assertion FAILURE) is observed — the runs stop at OOM. The "never SUCCESS" half of the requirement holds (no canary printed SUCCESS in any run, original or bounded). Resolution requires a decision GPT has not yet authorized: either a solver/encoding flag change (explicitly frozen out by GPT's 2026-10-13 instruction: "Do not change the frozen command or try other flags yet"), a budget raise, or acceptance of OOM->INCOMPLETE->UNKNOWN as the canary outcome. No bound was narrowed to make anything pass.

### 5.5 Resource-control record (GPT directive compliance)

- V1 field-sensitivity experiment: `raw/V1_STATUS.txt` + `raw/v1_fieldsens.txt` (676 bytes, ends at "Starting Bounded Model Checking"). OUTCOME: INTERRUPTED / INCONCLUSIVE; no CBMC verdict exists; baseline and V1 kept in separate files; no leftover process.
- Bounded runner `raw/run_bounded.ps1` (v5.1): job object hard 8 GB (`RLC0.JobLimit` C# helper, struct size guard 144 bytes), 1800 s wall watchdog, 250 ms poll, status sidecars. Self-tests: `raw/v51_exit7.*` (exit passthrough = 7), `raw/v51_mem.*` (1 GB selftest: allocator died naturally at peak 1 073 291 264 bytes, exit 2, job arm confirmed `mem_enforcement: job_object(True)`), `raw/v51_wall.*` (`outcome: WALL_TIMEOUT` at 8 s, no leftover processes). Round-1 (`base_*`, poll-only kill) vs round-2 (`r2_*`, kernel cap) both preserved.
- `verify_all` batch confirmed terminated before round 2 (process check: none); current check: no cbmc/goto-cl process remains.

## 6. Timeout semantics and nontermination rule

- CBMC invocation budget: 1800 s wall + 8 GB memory per invocation (spec.json `tier3_cbmc.budget_wall_seconds_per_invocation` / `budget_memory_gb`; FREEZE.md section 1). Enforced externally by `run_bounded.ps1` (wall = watchdog kill; memory = job object). On breach: INCOMPLETE (status `WALL_TIMEOUT` / job-kill), never a verdict. cbmc's own exit codes: 0 = SUCCESS, 10 = FAILED, 6/other = error -> INCOMPLETE.
- Native per-input timeout: 1000 ms, fixed before any seed runs (CONTRACT section 4, spec.json `failure.per_input_timeout_ms`; applies to Tier 1/2 native executions, not to CBMC invocations).
- Nontermination as a failure category (CONTRACT section 4 item (d), spec.json `failure.definition`): a solver that does not terminate is a verified failure on that input; Tier 2 native runs detect it via the 1000 ms per-input timeout, Tier 3 CBMC detects it as a violated unwinding assertion on `Solution::search` (termination is proven by `--unwinding-assertions` with unwind 64 >= max 14 actual trips, so any genuinely nonterminating path trips the assertion -> FAILED, and an unwinding-assertion failure can never be vacuously SUCCESS).
- Pre-registered rule (frozen): labels come from `classifier.py`; incompleteness (timeout, incomplete unwinding, missing obligations, tool/harness failure) maps to UNKNOWN and never to a certificate (spec.json `incomplete_action`, `label_definitions.UNKNOWN`). Immediate-stop rules in spec.json `immediate_stop_rules` — no tool, bound, seed, budget, or timeout may change after first seed execution (CONTRACT section 7).

## 7. Completeness / OOM->UNKNOWN settings (raw)

spec.json `tier3_cbmc.completeness_criteria` (verbatim):

```
1. cbmc exit status SUCCESS for the proof obligation
2. no violated unwinding assertions
3. all bounds, pointer, and undefined-behavior checks passed
4. domain assumptions exactly encode D (or D minus F) as specified above
5. the property is actually asserted (not vacuous by construction)
6. completed within the frozen wall-clock and memory budget
```

`tier3_cbmc.incomplete_action` (verbatim): "Any failed criterion yields UNKNOWN for that obligation; never a certificate."

Applied to today's raw outcomes: every canary invocation fails criteria 1 and 6 (exit 6 OOM / budget breach) => UNKNOWN-classified obligation, never SUCCESS — consistent with CONTRACT section 5 (UNKNOWN: "tool/harness failure") and section 13 (incomplete results reported, nothing changed). The domain probe completed within budget (criteria satisfied for its assertions): D1 FAILURE as designed, D2–D9 SUCCESS.

## 8. Fresh hash state (raw)

Recomputed 2026-10-13 against FREEZE.md section 5 — all 15 match (lowercase):

```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  .gitignore
1cd457f4b60bf0c591876445e82fdc7082fab4c6e82d4fbbfe3e18b7c22eb67c  CONTRACT.md
5aad7b57339097fd1bd6f625601370fb73c7a75845888dafd960b9c622ae217c  PROCEDURE.md
d46203666d25a9aa8e7d5306eee3382dbf79cfd335ff1b08d6b52a30c080738e  classifier.py
a318d6ca2e84ed74ddbb9e58778722bdbad218e8daed8de66bc578ec0a27d60b  expected.json
cd9e1e7f952c621d624d45e27548224232ed9318b2a6f4f0743f8eb62f625e4e  spec.json
341e89e66e1a80047f77aaac34c88343b2aa28c1e0857ee5d418f6e938b3ff83  seeds/seed1.cpp
7cc0fe09369580d72f1398706cc0f8b806c7e7af1a1c6162477317b920ba8a84  seeds/seed2.cpp
1877626489ebedbdce595f2a3d68277170ae4af26d8f84694681be868158c4a1  seeds/seed3.cpp
7477699043e6995d6ea9010165d5e5f1d440e377d1f111de07855b9d985d8452  seeds/seed4.cpp
8b48ea3a44b961e4536d4337e2182ab5be6ee7ab119046b254c4d74d391f3a7d  seeds/seed5.cpp
296e8fc0c3d700adabb7a39daeb64aab58d687fbfa5d1c63afb6f8abf72f6e6d  seeds/seed6.cpp
6690c2eef01f1674c7bd73efec663bd7b6973407ff416d3dceea71350d19b418  model/vector
b934b42c36050943cecd8a4a6c5fe3bc0cd1ad7c9fd810fd7141c6f1460ac64a  ADDENDUM_2026-10-13.md
d4699647ae0386bad8648c17c052f331a60d56f441a78000f4f9ff87f58b271a  ADDENDUM_2026-10-13_B.md
```

Uncommitted-at-package-time harness files (committed together with this package):

```
24c1301f6300fbf6cf9e64bab22027aa2fab503f178751de629a945629979d53  harness/proof_harness.h
5dad1193d4eec1d629886a7f73d5646108be31898ceeead12bf7b5ed4bd94a9d  harness/proof_main.cpp
f616f9f57765291a49a23681cd9d4bbb3ef3e9a5303779d3059cf3a4fecaf72f  harness/canary_n63.h
b45d8e52fb90b101be01f984a279a2063b49856f90e76537403e2933b6b59a70  harness/canary_large.h
```

Git state: HEAD = 69d70f808b595366e5c372c8fb30389869e71b45 ("rlc0: B0.5 non-seed differential validation ..."); `git tag -l rlc0*` = empty (no tag); working tree at package time: only `rlc0/harness/` + this `rlc0/evidence/C2/` new; no v0.1/v0.2 file touched. Free RAM at check time: 7.9 GB of 15.9 GB; no cbmc/goto-cl process running.

## 9. OPEN items (explicit)

1. **C2 canary FAIL not observed** (section 5.4): all six canary invocations OOM inside the frozen budget; never SUCCESS, but also never FAILED/unwinding-FAILURE. Resolution requires a GPT-authorized decision (flag experiment, budget change, or acceptance of OOM->INCOMPLETE); no frozen command or bound was changed.
2. **spec.json `frozen_cbmc_commands` lacks the `--unwindset 10001`** actually required and used for every run (section 4): record amendment needed before final freeze; frozen file not edited here.
3. **spec.json harness_model wording** ("for all i < j < n") vs adjacent-pair encoding (section 2.2): equivalent over ints, wording discrepancy reported not edited.
4. **C1** model-versus-real adequacy: OPEN pending reviewer judgment (FREEZE.md section 6.1).
5. **C3** independent hash recomputation + eventual `rlc0-freeze` tag verification: OPEN; no tag exists; freeze not authorized; Phase C prohibited.
6. **V1 field-sensitivity experiment**: INTERRUPTED / INCONCLUSIVE, awaiting GPT's verdict on whether/when to authorize flag experiments (GPT instruction: not yet).
