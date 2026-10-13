# B0.5 — Non-seed differential validation (model vs real MSVC std::vector)

Authorized: GPT 2026-10-13, non-seed testing only. Commit 33703dd remains a freeze candidate. No freeze, no tag, no seeded implementation executed.

## Scope and conditions honored

1. Synthetic harness only: `differential.cpp` (in this directory). No seed file was compiled, executed, or analyzed. 17 input cases, all inside declared LC704 domain D (lengths 1..10000; every value and target strictly between -10000 and 10000; strictly increasing distinct values).
2. Operation coverage vs seeds: grep over `rlc0/seeds/*.cpp` shows the seeds use exactly `std::vector::size()` and `std::vector::operator[]` (read indexing) and nothing else (no push_back, empty, at, front/back calls, iterators, data(), find, etc.). The harness exercises size() queries, valid non-const indexing (full scan + midpoint found-path lookup), const-operator[] access through a `const vector<int>&`, the found-target path (existing middle element, found index always != -1) and the absent-target path (computed missing value, found index always -1 on both builds).
3. OOB canary kept separate: the `v[v.size()]` negative canary was NOT built against real std::vector in this validation (that access is UB in ordinary C++; its native result cannot validate the model's bounds monitor). The existing CBMC negative canary from commit e993597 remains the separate test that the monitor fires.

## Exact commands and versions

Environment: Visual Studio 2026 Developer Command Prompt v18.10.2 (VsDevCmd -arch=amd64 -host_arch=amd64); cl = Microsoft (R) C/C++ Optimizing Compiler Version 19.51.36260 for x64 (path `...\BuildTools\VC\Tools\MSVC\14.51.36231\bin\Hostx64\x64\cl.exe`).

```
cl /nologo /std:c++17 /EHsc "<repo>\rlc0\evidence\B0.5\differential.cpp" /Fodifferential_real.obj /Fe:differential_real.exe
differential_real.exe > transcript_real.txt
cl /nologo /std:c++17 /EHsc /D RLC0_MODEL_BUILD /I"<repo>\rlc0\model" "<repo>\rlc0\evidence\B0.5\differential.cpp" /Fodifferential_model.obj /Fe:differential_model.exe
differential_model.exe > transcript_model.txt
fc /b transcript_real.txt transcript_model.txt
```

The only difference between the two builds is `-D RLC0_MODEL_BUILD /I model`: the adapter `fill()` either push_back-copies into a real vector (real build) or attaches the read-only buffer directly to the model's fields (model build). All observable operations under comparison (size, indexing, found/absent behavior) run on identical logic in both builds.

## Raw results (full log: run_log.txt)

| Step | Exit |
|---|---|
| real compile | 0 |
| real run | 0 |
| model compile | 0 |
| model run | 0 |
| `fc /b` byte comparison | 0 (`aucune difference trouvée` — no differences) |

Transcript (both files, 17 cases): sizes 1,2,3,7,8,9,15,16,17,64,1000,9999,10000 plus witness-shaped arrays [1], [0..7], [0], [0,2]; every line carries n, sum, found index (always the expected midpoint or 0), absent index (always -1), const-scan sum. `transcript_real.txt` and `transcript_model.txt` are byte-identical: same SHA-256 `5ec802cc096ee120a411aef0c907b13bc8d72efbdca58acec421d593cec0aefb`.

No discrepancy found. Per condition 2, this would otherwise be a blocker.

## Artifact hashes

```
e95673292110ad9aabb778290b93b1f922bab33296f0ae87bd9434a404c50eac  differential.cpp
8f88d85eff96e1759335198986f8b909d17afd13b00878d18514644de25f7301  run_log.txt
5ec802cc096ee120a411aef0c907b13bc8d72efbdca58acec421d593cec0aefb  transcript_model.txt
5ec802cc096ee120a411aef0c907b13bc8d72efbdca58acec421d593cec0aefb  transcript_real.txt
```

## Interpretation limit (condition 4)

Passing finite differential tests is evidence of correspondence on the tested cases, not a universal proof. The remaining source-level semantic argument and its limits:

- The model reproduces the only two operations the seeds use: `size()` returns the element count (model: `m_size`; real: library count), and `operator[]` returns a reference to element `i` for `i < size()` (model: direct field access plus the bounds monitor; real: library unchecked access). For in-bounds reads on a constructed vector both are element i, so any function of `size()` and in-bounds element reads computes identically — the identity is an argument from the definitions, not from the test run.
- Limits: the correspondence argument holds for the frozen operation set only (`size`, `operator[]`, both const and non-const). Any future use of other vector members would require a fresh differential validation and an addendum; this is enforced by B0.5 being tied to the frozen operation scan above. The model's `m_data`/`m_size` are public only to allow harness attachment; seeds receive `const/non-const vector<int>&` and never touch fields directly.

C1 stays OPEN until this justification, plus the differential evidence, is judged adequate by the reviewer (GPT) — a passing suite alone does not discharge the obligation.
