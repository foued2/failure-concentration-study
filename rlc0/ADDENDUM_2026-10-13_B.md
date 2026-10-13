# RLC-0 ADDENDUM 2026-10-13-B — OPTION SELECTED: MINIMAL MODELED STL INTERFACE

Status: DRAFT-STAGE INVESTIGATION. Dated before any Option-B test run. Freeze remains blocked; all six seeds remain gated; no seed compilation, execution, or CBMC analysis is authorized.

## 1. Decision record

| Decision | Disposition |
|---|---|
| A: Try Build Tools 17.14.41 | REJECTED for now. The failure is in CBMC's C++ parser, not Microsoft's compiler. goto-cl preprocesses with `cl /E`; CBMC then parses the token stream. Downgrading the compiler changes preprocessed output but not the parser. The failing constructs (C++11 `integral_constant` conversion operator, `operator()`) exist in MSVC 14.44 STL as well, so the specific failure is likely to persist. |
| B: Test a minimal modeled STL interface | SELECTED for investigation, narrow scope below. |
| Run any of the six seeds | NOT AUTHORIZED |
| Freeze or create `rlc0-freeze` | BLOCKED |

External evidence supporting the diagnosis: CBMC issue #8663 (CBMC 6.6: widespread parse failures on C++11/14/17 headers and constructs) and CBMC issue #8272 (CBMC contributor: mainstream STLs depend on template metaprogramming CBMC's C++ frontend does not adequately support; suggests simpler/custom standard-library headers). These do not prove CBMC 6.11.0 cannot handle every relevant program; they make another MSVC-version trial a weak next move.

## 2. Narrow scope of Option B

Permitted now:

1. Build ONE project-controlled model header, `rlc0/model/vector`, shadowing `<vector>` on the CBMC path only, covering exactly the operations the seeds invoke: default construction, `size()`, `operator[]` const and non-const. Fixed-capacity backing buffer injected by the harness; harness construction API (e.g. push_back for equivalence builds) is a Phase-B design item to be frozen later.
2. The model must encode `std::vector::operator[]`'s real precondition: reference access valid only for `i < size()`. On the CBMC path this precondition becomes an explicit `__CPROVER_assert` failure, so a real-vector UB is caught by the model instead of silently passing (a raw `p[i]` model alone would miss seed-5-class defects because `i == size()` can still fall inside the backing buffer — that would certify a property of the substitute model, not of the submitted program).
3. Non-seed smoke tests only (canary programs), validating that goto-cl + CBMC parse and verify against the model.

Not permitted: compiling, executing, or CBMC-analyzing any of the six seeds; freezing or tagging; producing any certificate; modifying CBMC or the MSVC pins.

## 3. Semantic correspondence: an explicit proof obligation

The model is a substitute for `std::vector` only if correspondence is discharged, never assumed:

- S1 (operation coverage): a machine-checked scan of the six seeds establishes exactly which vector members they use (expected: construction, `size()`, `operator[]`). The model must implement precisely those with cppreference-defined semantics for valid inputs. Any member used by a seed but absent/mis-modeled in the model is a stop condition.
- S2 (behavioral agreement): in Phase B, one harness is built twice natively with cl — against the real MSVC STL and against the model header. Over the full Tier-1 and Tier-2 case sets plus the frozen witnesses, for every seed, the two builds must agree on: failure flag (wrong answer, crash, UB, timeout) and, where no failure occurred, the exact return value. Disagreement anywhere stops the study. This is evidence-based discharge, not assumption.
- S3 (CBMC-path coverage): on the verification path, the model's index precondition assert plus CBMC bounds/pointer checks must cover every memory-safety violation real `operator[]` would permit. Certificates are only meaningful with this contract recorded in FREEZE.md, and REPORT.md must state that behavior was certified against the recorded model interface.
- Scope statement: correspondence is established over the frozen input domain and case sets by S1-S3; REPORT.md must state this prominently alongside the complexity limitation.

## 4. Stop rule for Option B

If the minimal model cannot be parsed or analyzed soundly by goto-cl + CBMC 6.11.0, stop. Record the outcome as a tool-and-configuration limitation of this environment. It must NOT be reported as evidence that full-domain localization certification is impossible in principle.

## 5. Smoke result: PASS (non-seed canaries, 2026-10-13)

Environment: VS 2026 dev prompt v18.10.2 (cl 19.51.36260), CBMC 6.11.0, model header `rlc0/model/vector` shadowing `<vector>` via goto-cl `/I` (verified with `cl /EP`: model in stream, MSVC STL absent).

Findings from the run (recorded before success):

1. goto-cl silently produces no output for `/Fe:file` and `/Fo:file` colon forms (exit 0, no artifact). Default output naming (`.exe` goto-binary) works. Command lines for the freeze record must use default output or a non-colon form; this is a tool quirk to encode in PROCEDURE, not a tool change.
2. A project-scope declaration of `__CPROVER_assert` gets C++-mangled and CBMC reports `no body for callee`. The declaration must be `extern "C"` so the call binds to CBMC's builtin. Fixed in the model; recorded here because it is a required property of any frozen model header.
3. `__CPROVER__` is predefined by goto-cl (the model's guard activates).

Final outcomes (full log: C:\Users\pakla\AppData\Local\Temp\opencode\model-smoke-out.txt):

```
canary_ok  (correct linear search, non-seed): goto-cl exit 0; cbmc ** VERIFICATION SUCCESSFUL ** — 0 of 38 failed; [operator[].assertion.1] rlc0 model vector: index out of range: SUCCESS; exit 0
canary_oob (v[v.size()] access, non-seed):    goto-cl exit 0; cbmc ** VERIFICATION FAILED ** — 1 of 37 failed; [operator[].assertion.1] line 25 rlc0 model vector: index out of range: FAILURE; exit 10
```

Interpretation: the minimal modeled interface route parses, verifies, and enforces the vector index precondition (the safeguard that makes seed-5-class UB catchable). The positive canary proves no false alarms on correct code. Option B clears the non-seed smoke gate.

## 6. Standing status after this addendum

- The Option-B route is validated for canaries only. No certificate exists; no seed has been compiled, executed, or analyzed by CBMC.
- Before FREEZE: model file + command-line quirks (default output naming, extern-C assert declaration) must be folded into spec.json/PROCEDURE.md; S1-S3 correspondence obligations defined in section 3 must be executable in Phase B; FREEZE.md must hash `rlc0/model/vector`.
- Freeze and `rlc0-freeze` remain blocked pending GPT/CLAUDE review of this result. Phase C remains unauthorized.
