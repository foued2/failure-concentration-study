# RLC-0 FREEZE RECORD — STATUS: FREEZE CANDIDATE (NOT YET FROZEN)

This is a freeze candidate prepared per GPT review 2026-10-13. The `rlc0-freeze` tag has NOT been created. Final freezing is not authorized until all three conditions in section 6 are discharged, a reviewer other than the author has recomputed every hash in section 5, and the tag has been verified against the reviewed commit. No seed may be compiled, executed, or analyzed by CBMC until then. Date prepared: 2026-10-13.

## 1. Pinned toolchain

| Component | Pin |
|---|---|
| CBMC | 6.11.0 (cbmc-6.11.0), `C:\Users\pakla\AppData\Local\Programs\cbmc\bin`, MSI sha256 8dcb29c2e91329898ecde5b79198dad2f4b5ebc5cb6b7d15e892c4fe26c6ea53 |
| goto-cl / cbmc drivers | goto-cl.exe, cbmc.exe from the same install |
| Build Tools package | winget id Microsoft.VisualStudio.BuildTools, version 18.10.2, installer sha256 5be7256fa9b1a3c18a481d234abb45146f82ccc057c77449b94915e1ae3fd70e, workload VCTools --includeRecommended |
| cl.exe | Microsoft (R) C/C++ Optimizing Compiler Version 19.51.36260 for x64; path C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Tools\MSVC\14.51.36231\bin\Hostx64\x64\cl.exe |
| link.exe | Microsoft (R) Incremental Linker Version 14.51.36260.0 |
| VCToolsVersion | 14.51.36231 |
| Windows SDK | 10.0.26100.0, dir C:\Program Files (x86)\Windows Kits\10\ |
| Developer environment | Visual Studio 2026 Developer Command Prompt v18.10.2 (VsDevCmd.bat -arch=amd64 -host_arch=amd64) |
| Not in toolchain | llvm-mingw clang++ 23.1.1 (inventory only) |
| MSVC STL | 14.51.36231, native Tier 1/2 path ONLY; CBMC 6.11.0 cannot parse it (ADDENDUM_2026-10-13) |

Frozen CBMC flags (every invocation, as executed in every recorded run): `--function <entry> --unwind 64 --unwindset "rlc0_build(ptr_struct_tag(identifier=tag-rlc0_input)).0:10001" --unwinding-assertions --bounds-check --pointer-check` (`--unwind 64` is the global bound for all other loops; the unwindset gives the 10000-trip `rlc0_build` harness loop its required ≥10001 bound); budget 1800 s wall / 8 GB per invocation; per-input native timeout 1000 ms (operational detector — see CONTRACT.md §4 and ADDENDUM_2026-10-13_C.md §5). Proof-completeness settings: spec.json tier3_cbmc.completeness_criteria (unmodified). Commands record amended 2026-10-13 by ADDENDUM_2026-10-13_C.md §4 to match the executed command exactly; property set emitted by cbmc 6.11.0 documented in ADDENDUM_C §6 and spec.json tier3_cbmc.property_set_observed.

## 2. Model header (CBMC path) — exact contents and hash

File: `rlc0/model/vector`, SHA-256 `6690c2eef01f1674c7bd73efec663bd7b6973407ff416d3dceea71350d19b418`.

```cpp
#ifndef RLC0_MODEL_VECTOR_H
#define RLC0_MODEL_VECTOR_H

typedef unsigned long long rlc0_size_t;

#ifdef __CPROVER__
extern "C" void __CPROVER_assert(bool condition, const char* description);
#endif

namespace std {

template <class T>
class vector {
public:
    typedef rlc0_size_t size_type;

    vector() : m_data(0), m_size(0) {}

    size_type size() const {
        return m_size;
    }

    T& operator[](size_type i) {
#ifdef __CPROVER__
        __CPROVER_assert(i < m_size, "rlc0 model vector: index out of range");
#endif
        return m_data[i];
    }

    const T& operator[](size_type i) const {
#ifdef __CPROVER__
        __CPROVER_assert(i < m_size, "rlc0 model vector: index out of range");
#endif
        return m_data[i];
    }

    T* m_data;
    size_type m_size;
};

}

#endif
```

Frozen requirements encoded in this header: `__CPROVER_assert` must stay `extern "C"` (C++ mangling otherwise causes CBMC `no body for callee`, recorded in ADDENDUM_2026-10-13_B finding 2); `__CPROVER__` is predefined by goto-cl; the index precondition is the verification monitor for the study's memory-safety failure category (not a claim about std::vector's ordinary in-bounds behavior).

## 3. Include-path order proof (model shadows real `<vector>`)

Command:

```
cl /nologo /std:c++17 /EP /IC:\Users\pakla\PycharmProjects\failure-concentration-study\rlc0\model <canary>.cpp
```

Recorded result (2026-10-13): model marker `rlc0_size_t` PRESENT in the preprocessed stream; MSVC STL marker `integral_constant` ABSENT. Search order: goto-cl/cl `/I` directory before the system INCLUDE path. Must be re-proven after any header or include-order change.

## 4. Exact frozen commands and canary results

Compile (model route; NOTE: goto-cl silently produces no artifact for `/Fe:file` and `/Fo:file` colon forms — default output naming is mandatory; the full executed build command, including the harness `/I`, the `/DRLC0_SOLVER_HEADER` / `/DOBL_*` defines, and the harness source path, is recorded in spec.json toolchain.model_route.frozen_cbmc_commands and evidence/C2/raw/build_all.cmd):

```
goto-cl.exe /nologo /std:c++17 /EHsc /I"<repo>\rlc0\model" /I"<repo>\rlc0\harness" /DRLC0_SOLVER_HEADER=canary_<x>.h /DOBL_<OBL> "<repo>\rlc0\harness\proof_main.cpp"   (default output naming, then proof_main.exe renamed to canary_<x>_<OBL>.exe)
cbmc.exe <file>.exe --function main --unwind 64 --unwindset "rlc0_build(ptr_struct_tag(identifier=tag-rlc0_input)).0:10001" --unwinding-assertions --bounds-check --pointer-check
```

Non-seed smoke results, raw (2026-10-13, full log C:\Users\pakla\AppData\Local\Temp\opencode\model-smoke-out.txt; smoke canaries used --unwind 16, the study-wide frozen unwind is 64):

```
canary_ok (correct linear search, non-seed):
  goto-cl exit: 0
  [operator[].assertion.1] line 25 rlc0 model vector: index out of range: SUCCESS
  ** 0 of 38 failed (1 iterations)
  VERIFICATION SUCCESSFUL   (cbmc exit 0)

canary_oob (v[v.size()] with backing buffer in bounds, non-seed):
  goto-cl exit: 0
  [operator[].assertion.1] line 25 rlc0 model vector: index out of range: FAILURE
  ** 1 of 37 failed (2 iterations)
  VERIFICATION FAILED       (cbmc exit 10)
```

Positive canary: clean SUCCESS including the model index assertion (no false alarm). Negative canary: the expected failing bounds/index assertion, demonstrating the monitor for the memory-safety failure category. Native cl smoke of the positive canary also passed (exit 0).

## 5. SHA-256 of frozen files (FREEZE.md excluded; its integrity is covered by the git commit)

```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  .gitignore   (0-byte empty file; hash = SHA-256 of empty string, git blob e69de29; history and explanation: ADDENDUM_2026-10-13_C.md §2)
247afbfccd6ee27f313f6ebc4d9207f0e58bb60b2c7b617c566969422d3ee735  CONTRACT.md   (amended 2026-10-13 §4 timing scope only; old: 1cd457f4b60bf0c591876445e82fdc7082fab4c6e82d4fbbfe3e18b7c22eb67c, see ADDENDUM_C §10)
5aad7b57339097fd1bd6f625601370fb73c7a75845888dafd960b9c622ae217c  PROCEDURE.md
d46203666d25a9aa8e7d5306eee3382dbf79cfd335ff1b08d6b52a30c080738e  classifier.py
a318d6ca2e84ed74ddbb9e58778722bdbad218e8daed8de66bc578ec0a27d60b  expected.json
b42a0f1a988d2cee19b13f52b3bba51146a472fa07c96d28bb65e9616f741376  spec.json   (amended 2026-10-13: frozen command + unwindset, nontermination rule, timing scope, property set; old: cd9e1e7f952c621d624d45e27548224232ed9318b2a6f4f0743f8eb62f625e4e, see ADDENDUM_C §10)
341e89e66e1a80047f77aaac34c88343b2aa28c1e0857ee5d418f6e938b3ff83  seeds/seed1.cpp
7cc0fe09369580d72f1398706cc0f8b806c7e7af1a1c6162477317b920ba8a84  seeds/seed2.cpp
1877626489ebedbdce595f2a3d68277170ae4af26d8f84694681be868158c4a1  seeds/seed3.cpp
7477699043e6995d6ea9010165d5e5f1d440e377d1f111de07855b9d985d8452  seeds/seed4.cpp
8b48ea3a44b961e4536d4337e2182ab5be6ee7ab119046b254c4d74d391f3a7d  seeds/seed5.cpp
296e8fc0c3d700adabb7a39daeb64aab58d687fbfa5d1c63afb6f8abf72f6e6d  seeds/seed6.cpp
6690c2eef01f1674c7bd73efec663bd7b6973407ff416d3dceea71350d19b418  model/vector
b934b42c36050943cecd8a4a6c5fe3bc0cd1ad7c9fd810fd7141c6f1460ac64a  ADDENDUM_2026-10-13.md
d4699647ae0386bad8648c17c052f331a60d56f441a78000f4f9ff87f58b271a  ADDENDUM_2026-10-13_B.md
0b6931a971c1933afd63d2ba16da589d0480e49f03520753e3c8414de47f3d49  ADDENDUM_2026-10-13_C.md   (added 2026-10-13: V1 TIMEOUT record, .gitignore explanation, C1 acceptance, command/property/nontermination corrections, CONTRACT reflow-restore incident record, hash-provenance note)
```

If any of these files changes, this candidate is void and the hashes must be regenerated.

### 5.1 B0.5 differential-validation evidence (executed 2026-10-13 under GPT approval; not frozen contract material, hashed for integrity)

```
e95673292110ad9aabb778290b93b1f922bab33296f0ae87bd9434a404c50eac  evidence/B0.5/differential.cpp
8f88d85eff96e1759335198986f8b909d17afd13b00878d18514644de25f7301  evidence/B0.5/run_log.txt
5ec802cc096ee120a411aef0c907b13bc8d72efbdca58acec421d593cec0aefb  evidence/B0.5/transcript_model.txt
5ec802cc096ee120a411aef0c907b13bc8d72efbdca58acec421d593cec0aefb  evidence/B0.5/transcript_real.txt
```

### 5.2 C2 harness-audit evidence (executed 2026-10-13; non-seed, raw logs in evidence/C2/raw/)

```
051e1a4fdc90beb673e2337e38da3d261165b729473e330d1a6a005533ecf59b  evidence/C2/RESULTS.md
```

`evidence/C2/raw/` holds the verbatim logs (78 files: quantifier probes, loop inventory, domain probe, baseline + bounded canary runs with status sidecars, V1 original-attempt record, 3 V1-retry sidecars, bounded-runner self-tests), individually hashed in section 5.4. RESULTS.md lists the four harness file hashes (section 5 uncommitted at its writing, committed with it) and its OPEN items. Item "spec.json frozen_cbmc_commands missing the required --unwindset" is DISCHARGED (amended 2026-10-13, ADDENDUM_C §4); the "canary FAIL not observed" item (all six baseline invocations OOM inside budget — see section 6.2) and the "harness-model wording vs adjacent-pair encoding" item remain OPEN.

### 5.3 Harness sources (each file listed in the freeze record itself; same values as evidence/C2/RESULTS.md)

```
24c1301f6300fbf6cf9e64bab22027aa2fab503f178751de629a945629979d53  harness/proof_harness.h
5dad1193d4eec1d629886a7f73d5646108be31898ceeead12bf7b5ed4bd94a9d  harness/proof_main.cpp
f616f9f57765291a49a23681cd9d4bbb3ef3e9a5303779d3059cf3a4fecaf72f  harness/canary_n63.h
b45d8e52fb90b101be01f984a279a2063b49856f90e76537403e2933b6b59a70  harness/canary_large.h
```

### 5.4 C2 raw-evidence manifest (covers every file in evidence/C2/raw/)

```
dfe43258d4dc9cec2fac7fb1a1cedfea5ca2996d3f489882a7c177a60451c45d  evidence/C2/MANIFEST.sha256   (78 entries, one per raw file; entry format: <sha256>  raw/<name>; independently recomputable via section 7)
```

## 6. Open conditions before final freeze and tag (GPT review 2026-10-13)

1. **Model-versus-real validation (S2, PROCEDURE B0.5): ACCEPTED, BOUNDED SCOPE (GPT disposition 2026-10-13; recorded in ADDENDUM_2026-10-13_C.md §3).** Evidence: executed 2026-10-13 under GPT's non-seed-only approval — synthetic harness, 17 cases all inside D (lengths 1,2,3,7,8,9,15,16,17,64,1000,9999,10000 plus witness-shaped arrays [1], [0..7], [0], [0,2]), covering exactly the seed operation set (grep-verified: seeds use only `size()` and `operator[]`), found-target and absent-target paths, const and non-const access. Both native cl builds exit 0; `fc /b` reports no differences (exit 0); transcripts byte-identical (SHA-256 5ec802cc...). Full commands, raw log, source, hashes, and the source-level semantic argument with its limits: `rlc0/evidence/B0.5/RESULTS.md`. The OOB negative canary was deliberately NOT compared against real std::vector (UB in ordinary C++); it remains the separate CBMC monitor test. **Scope of the acceptance:** the frozen operation set actually used by the study (`size()` + in-bounds `operator[]`), supported by the finite differential passes on tested cases plus the source-level argument. **Not claimed:** equivalence for arbitrary std::vector operations, out-of-bounds behavior, or any API beyond the frozen set. C1 is closed under that bound; no further C1 evidence is required for freeze.
2. **Full-domain harness audit (PROCEDURE B4): EVIDENCE RECORDED (C2), C2 OPEN — MULTIPLE ITEMS OPEN (status per GPT review 2026-10-13, recorded in ADDENDUM_2026-10-13_C.md).** Audit package `rlc0/evidence/C2/` (RESULTS.md + 78 raw files, sections 5.2/5.4): harness source, exact constraint encoding with raw goto-cl quantifier-unavailability probes, adapter, two-loop inventory with unwindset 10001 rationale, domain probe D1-D9 (expected results both runs), timeout/completeness semantics, hash recheck matching section 5. OPEN items:
   - **Canary FAIL never observed:** all six baseline invocations ended in cbmc-internal SAT OOM (exit 6, INCOMPLETE) inside 1800 s / 8 GB — never SUCCESS, never FAILED. The single authorized configuration experiment (V1, field-sensitivity flag) completed as **WALL_TIMEOUT** on retry (1802.3 s, peak 84.6 MiB, no verification result — raw: `raw/v1retry_n63_IN_F.txt*`), triggering the GPT stopping rule: **STOP — no further flags, solvers, budgets, or compiler versions without a new explicit decision.** Scoped statement of record: *full-domain certification was not demonstrated under this pinned stack, harness, and budget (1800 s / 8 GB)* — not a claim of universal impossibility. Resolving this item requires a new GPT decision or acceptance of OOM/timeout → INCOMPLETE → UNKNOWN.
   - **Domain coverage:** the D1-D9 probe results show `n = 10000` reachable and each constraint class enforced (D1 FAILURE as expected; D2-D9 SUCCESS), but do **not** establish universal representability of every boundary/partition combination of the declared domain. The earlier wording "the harness represents the full declared domain — verified by the domain probe" **overclaimed** and is withdrawn (ADDENDUM_C §9); source-level constraint coverage is audited in RESULTS.md §2, and the coverage question remains OPEN as part of C2. No new probe series is run.
   - **Harness-model wording vs adjacent-pair encoding** (from RESULTS.md): OPEN.
   Finite Tier 1/2 evidence can never substitute for completed proof obligations with full unwinding. The `--unwindset` command-record item previously listed here is DISCHARGED (section 1/4; ADDENDUM_C §4).
3. **Independent review: OPEN.** A reviewer other than the author must recompute every hash in section 5 and verify the eventual `rlc0-freeze` tag resolves to the reviewed commit. Phase C remains unauthorized until that review reports agreement.

## 7. Hash recomputation (for the independent reviewer)

```powershell
cd C:\Users\pakla\PycharmProjects\failure-concentration-study\rlc0
Get-FileHash -Algorithm SHA256 .\CONTRACT.md, .\PROCEDURE.md, .\classifier.py, .\expected.json, .\spec.json, .\seeds\seed1.cpp, .\seeds\seed2.cpp, .\seeds\seed3.cpp, .\seeds\seed4.cpp, .\seeds\seed5.cpp, .\seeds\seed6.cpp, .\model\vector, .\ADDENDUM_2026-10-13.md, .\ADDENDUM_2026-10-13_B.md, .\ADDENDUM_2026-10-13_C.md, .\.gitignore | Format-Table Hash, Path -AutoSize
Get-FileHash -Algorithm SHA256 .\evidence\B0.5\differential.cpp, .\evidence\B0.5\run_log.txt, .\evidence\B0.5\transcript_model.txt, .\evidence\B0.5\transcript_real.txt, .\evidence\C2\RESULTS.md | Format-Table Hash, Path -AutoSize
Get-FileHash -Algorithm SHA256 .\harness\proof_harness.h, .\harness\proof_main.cpp, .\harness\canary_n63.h, .\harness\canary_large.h | Format-Table Hash, Path -AutoSize
git -C .. log --oneline -1
git -C .. tag -l rlc0-freeze
git -C .. rev-parse rlc0-freeze^{commit}   # after the tag exists
```

C2 raw-evidence manifest — recompute and compare against `evidence/C2/MANIFEST.sha256` (format `<sha256>  raw/<name>`, one line per file, sorted by name; expect zero differences, then compare the manifest's own hash against section 5.4):

```powershell
cd C:\Users\pakla\PycharmProjects\failure-concentration-study\rlc0\evidence\C2
Get-ChildItem raw -File | Sort-Object Name | Get-FileHash -Algorithm SHA256 |
  ForEach-Object { $_.Hash.ToLower() + "  raw/" + $_.Name } | Set-Content -Encoding ascii _recomputed.sha256
fc.exe /W MANIFEST.sha256 _recomputed.sha256   # expect: no differences
Get-FileHash -Algorithm SHA256 MANIFEST.sha256  # expect: value in section 5.4
Remove-Item _recomputed.sha256
```

Compare every Hash against section 5 (lowercase). The tag, once created, must resolve to the commit that contains exactly these file contents. Hash provenance (clarified 2026-10-13, ADDENDUM_C §10): the recorded values hash the working-tree bytes at the path above — the round-1 convention; this repo has `core.autocrlf=true` and no `.gitattributes`, so git-stored blobs are LF-normalized and `git cat-file` output may hash differently for some files with no content difference (compare content after normalizing line endings if checking blobs).

## 8. Authorization status

- Freeze candidate prepared: YES (this file), record corrected 2026-10-13 per ADDENDUM_2026-10-13_C.md (dated provenance for the spec.json/CONTRACT.md amendments and regenerated section-5 hashes; original commits/logs preserved).
- B0.5 non-seed differential validation: EXECUTED 2026-10-13 under GPT approval; no discrepancies; evidence in `rlc0/evidence/B0.5/`; **C1 ACCEPTED, BOUNDED SCOPE** (section 6.1; `size()` + in-bounds `operator[]` only, no arbitrary-API equivalence claim).
- C2 non-seed harness audit: EXECUTED 2026-10-13 under CLAUDE's C2 request + GPT's resource-control directive; evidence in `rlc0/evidence/C2/` (78 raw files + MANIFEST.sha256); **C2 OPEN** — canary-FAIL not observed (baseline OOM INCOMPLETE ×6; V1 retry **WALL_TIMEOUT**, stopping rule applied), domain-coverage OPEN, harness-model wording OPEN (section 6.2). V1 original attempt INTERRUPTED/INCONCLUSIVE; V1 authorized retry TIMEOUT; both records in `evidence/C2/raw/V1_STATUS.txt`.
- C2 domain-coverage wording correction and seed-6 nontermination/timing rules: PRE-REGISTERED 2026-10-13 (ADDENDUM_C §§5, 9) — before any seed execution.
- Final freeze + `rlc0-freeze` tag: NOT AUTHORIZED (conditions 6.2, 6.3 open; C1 closed under bounded scope).
- Phase C (six-seed single execution): PROHIBITED until freeze + independent review complete.
- This candidate itself does not certify anything about the seeds; current evidence supports toolchain feasibility for the modeled setup only.
