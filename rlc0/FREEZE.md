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

Frozen CBMC flags (every invocation): `--function <entry> --unwind 64 --unwinding-assertions --bounds-check --pointer-check`; budget 1800 s wall / 8 GB per invocation; per-input native timeout 1000 ms. Proof-completeness settings: spec.json tier3_cbmc.completeness_criteria (unmodified).

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

Compile (model route; NOTE: goto-cl silently produces no artifact for `/Fe:file` and `/Fo:file` colon forms — default output naming is mandatory):

```
goto-cl.exe /nologo /std:c++17 /EHsc /I"<repo>\rlc0\model" <file>.cpp        -> writes <file>.exe (goto-binary)
cbmc.exe <file>.exe --function main --unwind 64 --unwinding-assertions --bounds-check --pointer-check
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

`evidence/C2/raw/` holds the verbatim logs (75 files: quantifier probes, loop inventory, domain probe, baseline + bounded canary runs with status sidecars, V1 record, bounded-runner self-tests). RESULTS.md lists the four harness file hashes (section 5 uncommitted at its writing, committed with it) and the OPEN items: canary FAIL not observed (all six OOM inside budget, never SUCCESS), spec.json `frozen_cbmc_commands` missing the required `--unwindset ...:10001`, harness-model wording vs adjacent-pair encoding.

## 6. Open conditions before final freeze and tag (GPT review 2026-10-13)

1. **Model-versus-real validation (S2, PROCEDURE B0.5): EVIDENCE RECORDED, C1 STILL OPEN.** Executed 2026-10-13 under GPT's non-seed-only approval: synthetic harness, 17 cases all inside D (lengths 1,2,3,7,8,9,15,16,17,64,1000,9999,10000 plus witness-shaped arrays [1], [0..7], [0], [0,2]), covering exactly the seed operation set (grep-verified: seeds use only `size()` and `operator[]`), found-target and absent-target paths, const and non-const access. Both native cl builds exit 0; `fc /b` reports no differences (exit 0); transcripts byte-identical (SHA-256 5ec802cc...). Full commands, raw log, source, hashes, and the source-level semantic argument with its limits: `rlc0/evidence/B0.5/RESULTS.md`. The OOB negative canary was deliberately NOT compared against real std::vector (UB in ordinary C++); it remains the separate CBMC monitor test. Per GPT condition 4, finite differential passes are evidence on tested cases only; C1 remains OPEN until the reviewer judges the combined differential + source-level justification adequate.
2. **Full-domain harness audit (PROCEDURE B4): EVIDENCE RECORDED (C2), ONE ITEM OPEN.** Audit package `rlc0/evidence/C2/` (RESULTS.md + 75 raw files, section 5.2): harness source, exact constraint encoding with raw goto-cl quantifier-unavailability probes, adapter, two-loop inventory with unwindset 10001 rationale, domain probe D1-D9 (expected results both runs), timeout/completeness semantics, hash recheck matching section 5. The harness represents the full declared domain (symbolic n in [1,10000], symbolic elements with strict-increase/range constraints, symbolic target) — verified by the domain probe, not assumed. OPEN: the two defect canaries never reached FAIL inside 1800 s / 8 GB (all six invocations ended cbmc-internal SAT OOM, exit 6, INCOMPLETE — never SUCCESS, also never FAILED); resolving this requires a GPT-authorized decision (flag experiment, budget change, or acceptance of OOM->INCOMPLETE->UNKNOWN), and spec.json's `frozen_cbmc_commands` must gain the required `--unwindset` before final freeze (frozen file not edited without approval). Finite Tier 1/2 evidence can never substitute for completed proof obligations with full unwinding.
3. **Independent review: OPEN.** A reviewer other than the author must recompute every hash in section 5 and verify the eventual `rlc0-freeze` tag resolves to the reviewed commit. Phase C remains unauthorized until that review reports agreement.

## 7. Hash recomputation (for the independent reviewer)

```powershell
cd C:\Users\pakla\PycharmProjects\failure-concentration-study\rlc0
Get-FileHash -Algorithm SHA256 .\CONTRACT.md, .\PROCEDURE.md, .\classifier.py, .\expected.json, .\spec.json, .\seeds\seed1.cpp, .\seeds\seed2.cpp, .\seeds\seed3.cpp, .\seeds\seed4.cpp, .\seeds\seed5.cpp, .\seeds\seed6.cpp, .\model\vector, .\ADDENDUM_2026-10-13.md, .\ADDENDUM_2026-10-13_B.md, .\.gitignore | Format-Table Hash, Path -AutoSize
Get-FileHash -Algorithm SHA256 .\evidence\B0.5\differential.cpp, .\evidence\B0.5\run_log.txt, .\evidence\B0.5\transcript_model.txt, .\evidence\B0.5\transcript_real.txt | Format-Table Hash, Path -AutoSize
git -C .. log --oneline -1
git -C .. tag -l rlc0-freeze
git -C .. rev-parse rlc0-freeze^{commit}   # after the tag exists
```

Compare every Hash against section 5 (lowercase). The tag, once created, must resolve to the commit that contains exactly these file contents.

## 8. Authorization status

- Freeze candidate prepared: YES (this file).
- B0.5 non-seed differential validation: EXECUTED 2026-10-13 under GPT approval; no discrepancies; evidence in `rlc0/evidence/B0.5/`; C1 still open pending reviewer adequacy judgment (section 6.1).
- C2 non-seed harness audit: EXECUTED 2026-10-13 under CLAUDE's C2 request + GPT's resource-control directive; evidence in `rlc0/evidence/C2/`; canary-FAIL item and spec.json unwindset amendment OPEN (section 6.2); V1 field-sensitivity experiment INTERRUPTED/INCONCLUSIVE, its record kept separate in `evidence/C2/raw/V1_STATUS.txt`.
- Final freeze + `rlc0-freeze` tag: NOT AUTHORIZED (conditions 6.1-6.3 open).
- Phase C (six-seed single execution): PROHIBITED until freeze + independent review complete.
- This candidate itself does not certify anything about the seeds; current evidence supports toolchain feasibility for the modeled setup only.
