# RLC-0 CONTRACT (DRAFT — NOT FROZEN)

Status: DRAFT. Toolchain pins for `cl.exe` are pending installation. This file is frozen only when `rlc0/FREEZE.md` records hashes, tool versions, and the `rlc0-freeze` tag exists. No seed may be compiled, executed, or analyzed by CBMC before that freeze.

## 1. Purpose

Determine whether formal behavioral localization is technically feasible and operationally stable, using CBMC on six LeetCode 704 C++17 seed solvers with frozen family structure, domain bounds, labels, and success criteria. RLC-0 makes no claim about repair quality, causal localization, or complexity.

## 2. Problem and domain (D)

LeetCode 704 "Binary Search" (https://leetcode.com/problems/binary-search/description/), C++17, entry point `Solution::search(std::vector<int>& nums, int target) -> int`.

Domain D, exactly as confirmed from the live problem statement:

- 1 <= nums.length <= 10000
- -10000 < nums[i] < 10000 for every element
- -10000 < target < 10000
- all elements distinct; nums sorted in ascending order
- specification-correct answer: index of target if present, else -1

## 3. Family (F)

F = inputs in D where the target is present (exists i: nums[i] == target). Complement D minus F = target absent; correct behavior there is always -1. F and its complement are disjoint and exhaustive over D.

## 4. Failure

A solver fails on an input iff, under the frozen harness, one of: wrong return value; crash; memory-safety violation (bounds/pointer/UB check); timeout or nontermination; malformed output. Per-input timeout: 1000 ms, fixed before any seed runs.

## 5. Labels

- REFUTED: verified failure in D minus F.
- CERTIFIED_LOCALIZED: verified failure in F, plus a complete formal proof of correctness over D minus F (safety and termination included).
- NO_FAILURE: complete formal proof over all of D.
- CANDIDATE_ONLY: verified failure in F, none found in D minus F, no complete D-minus-F proof.
- UNKNOWN: everything else (timeout, incomplete unwinding, missing obligations, tool/harness failure).

Completeness criteria for any "complete" proof are frozen in `spec.json` (tier3_cbmc.completeness_criteria). A failed criterion yields UNKNOWN; never a certificate.

## 6. Seeds and frozen witnesses

Six seeds in `rlc0/seeds/`, defects and witnesses exactly as ratified:

1. correct implementation -> expected NO_FAILURE
2. returns -1 when nums[mid] == target -> expected CERTIFIED_LOCALIZED, witness [1], target 1
3. correct only for length 1, returns -1 otherwise -> expected CERTIFIED_LOCALIZED, witness [1], target 1
4. found-target defect plus length>=8/target-above-max defect returning size()-1 -> expected REFUTED, witness [0..7], target 8
5. right = nums.size() enabling out-of-bounds access -> expected REFUTED, witness [0], target 1
6. left = mid (missing +1) causing nontermination -> expected REFUTED, witness [0,2], target 1

Expected outcomes live in `rlc0/expected.json`.

## 7. Success rule and immediate stops

RLC-0 succeeds only if all six seeds receive their expected outcomes, every certificate meets the frozen completeness criteria, and an independent checker agrees with `classifier.py` on all six labels.

Immediate stops (frozen): any of seeds 4/5/6 labeled CERTIFIED_LOCALIZED; seed 1 labeled UNKNOWN (voids certification claims for seeds 2/3 as a legitimate end state); any UNKNOWN (report, change nothing); any classifier/checker disagreement. No tool, bound, seed, budget, or timeout may be changed after first seed execution.

## 8. Tiers (summary; full spec in spec.json)

- Tier 1 exhaustive small: lengths 1..6, values [-3,3], targets [-4,4]; closed-form count 1134; count mismatch stops the study.
- Tier 2 adversarial (refutation only): frozen witnesses, boundary lengths {1,2,3,7,8,9,15,16,17,9999,10000}, 200 fixed-seed (20261012) random cases; exact generator algorithm frozen in spec.json.
- Tier 3 CBMC: unwind 64 with unwinding assertions, bounds and pointer checks, 1800 s / 8 GB per invocation; property set and harness model frozen in spec.json.

## 9. Toolchain

- CBMC 6.11.0 (release cbmc-6.11.0, MSI sha256 8dcb29c2e91329898ecde5b79198dad2f4b5ebc5cb6b7d15e892c4fe26c6ea53), installed per-user; compile driver goto-cl.exe.
- MSVC cl.exe from Microsoft.VisualStudio.BuildTools with workload VCTools: PENDING_INSTALL (version and path recorded at freeze).
- llvm-mingw clang++ 23.1.1 was verified during inventory but is NOT part of the frozen toolchain; all native Tier 1/2 executions use cl.exe.

If the required compiler or CBMC cannot be installed and version-pinned, that is a blocker reported before freezing. No substitute toolchain without a separate decision.

## 10. Complexity limitation (prominent)

RLC-0 does not verify O(log n), iteration counts, or any complexity bound. Certificates cover functional behavior, memory safety, and termination only. This limitation must appear prominently in REPORT.md.

## 11. Authorization boundary

Phase A (this contract, seeds, expected outcomes, classifier, procedure) may be prepared as DRAFT. Freezing requires: complete version-pinned toolchain, non-seed smoke test success, SHA-256 of every frozen file, commit, tag rlc0-freeze, and the tag commit hash recorded in FREEZE.md. Phase C (single execution over the six seeds) is authorized only after the freeze gate AND an independent recomputation of every FREEZE.md hash by a reviewer other than the author, with the rlc0-freeze tag commit confirmed to match. RLC-0 is a separate project from C_genuine and from the terminated v0.1/v0.2 studies; no file of those studies may be touched. The final report must end with: "RLC-0 is complete. No follow-up is authorized."

## 12. Pre-freeze review flags (closed)

- Flag 1 (domain): LC 704 bounds were checked against the live problem page (https://leetcode.com/problems/binary-search/description/, fetched 2026-10-12): 1 <= nums.length <= 10^4; -10^4 < nums[i], target < 10^4; unique; ascending. Mirrored in section 2 and spec.json (problem.official_bounds_confirmed).
- Flag 2 (seed 4 trigger): the triggering input is named in the frozen files — witness nums [0,1,2,3,4,5,6,7], target 8 (section 6, expected.json, spec.json tier2.frozen_witnesses). Defect path: size >= 8 and target > nums.back() returns size()-1 = 7 instead of -1.
- Flag 3 (seed 1 gate): seed 1 is the certification gate. Its NO_FAILURE label requires a complete full-D proof under the frozen completeness criteria (spec.json tier3_cbmc.completeness_criteria); if seed 1 is UNKNOWN, certification claims for seeds 2 and 3 are void (section 7). The full_d_proof property is executed for all six seeds so the gate is exercised uniformly.

## 13. Verdict-specific evidence acceptance

The evidence required for each expected verdict is fixed per seed (mirrored in expected.json):

- Seed 1 (NO_FAILURE): a complete full-domain correctness proof under the frozen completeness criteria. No verified failure anywhere in D.
- Seeds 2 and 3 (CERTIFIED_LOCALIZED): a verified failure inside F plus a complete proof of correctness throughout the complement D minus F. An incomplete full_d_proof on these seeds is expected, because a failure exists inside F; that incompleteness is not a pipeline failure.
- Seeds 4, 5 and 6 (REFUTED): a verified failure outside F. That alone suffices to refute localization for the seed; these seeds are not supposed to pass full-domain correctness proofs, and incomplete d_f_proof/full_d_proof results on them are expected refutation-side evidence, never interpreted as missing certificates.
- Any UNKNOWN on any seed: report the outcome; change nothing.

The full_d_proof invocation on seeds 2-6 is diagnostic uniformity only; acceptance is judged strictly per this section.

