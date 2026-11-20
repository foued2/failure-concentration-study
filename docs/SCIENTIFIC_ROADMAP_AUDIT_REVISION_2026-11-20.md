# Scientific roadmap audit — dated revision 2026-11-20

**Revision date:** 2026-11-20
**Base record:** `docs/SCIENTIFIC_ROADMAP_AUDIT_2026-11-18.md`, blob
`e6c1a21815794a20f08bad45342fd6cff3858ee6`, commit
`874915bf98f7cd747c2175eae8347ba15b9d0341` on `docs/scientific-roadmap-audit-2026-11-18`.
**Authority for this revision:** base record §7, which requires updates "only by adding a dated audit
revision that records the new source commit/blob identities and distinguishes changed facts from unchanged
historical evidence."
**Status:** navigational revision. It does not supersede a source record, resolve an open decision, change
a frozen document, authorize work, or merge a branch.

---

## 1. Changed facts since 2026-11-18

### 1.1 Remote head count: 60 to 63, with the set difference UNVERIFIED

`git ls-remote --heads origin` returned **63** heads on 2026-11-20. The base record states **60** at its own
commit. The 60-name enumeration was not archived with the base record or anywhere in this repository: the
count was retained, the names were not.

Consequence, stated as a limit rather than a finding:

- **The difference of three is a count difference, not a verified set difference.**
- Added, deleted, and renamed heads since the snapshot are **UNVERIFIED**.
- Tip commit dates are not branch-creation dates. A head whose tip postdates the snapshot may have been
  created earlier and updated, or created later. No reconstruction of the missing baseline from commit
  timestamps, arithmetic, or guesses is attempted here.
- The current 63-head listing is recorded in Appendix A so that the next revision has a preserved
  reference set from this point forward.

This supersedes only the branch-count row of §3.1 of the base record. Its other static rows are re-verified
and unchanged in §2 below.

### 1.2 B1 v1.7 branch inventory corrected

The base record's §3.3 cites B1 v1.7 without enumerating its containing branches. A later review statement
asserted the file was present on `gpt/b1-computational-plan-2026-11-14` **only**. That word is withdrawn.
The verified inventory is:

| Branch | Tip | B1 v1.7 |
|---|---|---|
| `gpt/b1-computational-plan-2026-11-14` | `46d548f` | present — `lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/B1_ANALYSIS_PLAN_2026-11-14_v1.7.md`, blob `8c666e50` |
| `gpt/lc518-m1si-audit-2026-11-17` | `7365ad5` | present — same path, same blob `8c666e50` |
| `master` | `33dca9b` | absent |
| `docs/scientific-roadmap-audit-2026-11-18` | `874915b` | absent |
| `audit/analytical-validity-2026-11-18` | `15cabef` | absent |
| `research/concentration-math-spec` | `de39291` | absent |

Content identity of blob `8c666e501a31726c728447d155045c0b20adc178`:
SHA-256 `797bd9f72cf94fdc0eff4a03b1544823d4042f8e530b27f4fb70cbd7f2baca7c`, 111,169 bytes, 331
LF-terminated lines, final newline present. The blob is reachable at exactly one path across all refs, so
there is no same-content/different-path copy. B1 v1.7's identity and acceptance are unchanged; only the
branch inventory was wrong.

### 1.3 Analytical-validity review cycle closed

- Canonical-basis support-correction chain: `03f950a` → `405fa9f` → `6663083` → `443b7a9`.
- GPT acceptance is recorded at `950fb93`; the closing record is `15cabef` on
  `audit/analytical-validity-2026-11-18`, file
  `reviews/analytical-validity-2026-11-18/REVIEWER_RESPONSE_2026-11-18.md` §21–§22.
- Independent-verification scope: Claude's pass covered §5.2 only; GLM verified the text of §5.3; GPT
  accepted that textual verification and closed the cycle. The combinatorial audit was not reopened.
- The §5.3 text verification establishes that the frozen text contains the excluded-cell inadmissibility
  rule, the selection-key-only admissibility condition, and the permutation-invariant target population.
  It does not remove the test's conditioning on exchangeability and the declared design-support
  conditions. A rejection alone would not establish that concentration is the unique source of predictive
  information rather than parent-quality or unresolved-placement association.

### 1.4 Provenance recorded, with authorship separated from Git identity

Git author and committer identity is self-reported configuration; it does not establish who wrote the
underlying document. Document authorship, Git identity, and owner acceptance remain three separate facts.

| Branch / scope | Commits | Recorded identities |
|---|---:|---|
| `audit/analytical-validity-2026-11-18` (ahead of `master`) | 156 | foued2 64; DeepSeek 48; GLM 38; MUSE 4; Codex 2 (`codex@local` 1, `codex@localhost` 1) |
| `gpt/b1-computational-plan-2026-11-14` (ahead of `master`) | 124 | foued2 121; `GLM <glm@review-chain.local>` 3 |

The two conventions coexist: owner-authored archive commits on the review branch, and agent-authored
commits on the validity branch. The identity strings are not authorship evidence beyond what Git recorded.

GLM's 21/21 documentary battery is recorded as **GLM-reported verification**. It was not reproduced here,
and its scripts and raw outputs are not in this repository. A reproducible archive needs the individual
check results and hashes of the scripts and output files; until those accompany it, the battery result is
reported, not independently confirmed.

The validity branch also archives a separate independent manifest-validator implementation (v0.2.0),
distinct from the GLM-track `manifest_validator_v0.1` / `v0.2` packages. The two must be cited by path and
hash, not by the bare name "manifest validator". GLM round-1 review blob
`df79d59f208bbf2718f5818d4acdc6907b61f7e8` remains unarchived; that is an owner action.

## 2. Unchanged historical evidence (re-verified at the stated points)

| Object | Identity |
|---|---|
| `master` | `33dca9b`, 308 tracked files |
| `gpt/b1-computational-plan-2026-11-14` | `46d548f`, 379 tracked files |
| `gpt/lc518-m1si-audit-2026-11-17` | `7365ad5`, 386 tracked files |
| B1 v1.7 blob | `8c666e50`; SHA-256 `797bd9f7…baca7c`; 111,169 bytes; 331 LF lines |
| B1 v1.7 acceptance record blob | `ea51d72f`, introduced by `ac06c66` |
| Base roadmap record | `874915b`; blob `e6c1a21…` |

No frozen record, protocol, threshold, bank, population document, or solver was altered by this revision.

## 3. What remains unverified

1. The added, deleted, or renamed heads between the 60-head snapshot and the 63-head listing.
2. The exact membership of the 60-head set.
3. Independent reproduction of GLM's 21/21 battery and its raw outputs.
4. Any empirical claim about solver behaviour, predictive gain, or superiority of the maximum-share
   statistic over the predeclared competing summaries.

## 4. Non-claims and pause

This revision improves the documentary record, not the scientific evidence. There are no solver outcomes,
no demonstrated predictive gain, and no evidence that the maximum-share statistic outperforms the
predeclared competing summaries. The project pause remains in force; nothing here authorizes solver
construction, execution, fitting, sampling, or bank access. The next substantive work, when explicitly
reopened, is Gate 0, measurement validity, and the S1 known-effect validation.

---

## Appendix A — remote heads at 2026-11-20 (63)

Produced by `git ls-remote --heads origin`, sorted by branch name. The SHA is the tip commit.

```
15cabefe08268cc6816407dfa1cff958c2e0e696 audit/analytical-validity-2026-11-18
204500e43a334c5dccd946f493a5e959af7edc44 audit/c09-count-reconciliation-2026-11-18
8daf8d8a914d65f98e244bf5b68b9ab49a51f24b claude/h3-v10-adversarial-fixtures
9422e8e1029f76ec55f264f257ae92ef6ef062b6 dev/h3-footprint-v2-harness
682a40dab3f950fafe10365c6ec3f396e0e6389f dev/h3-footprint-v9-implementation-2026-10-28
874915bf98f7cd747c2175eae8347ba15b9d0341 docs/scientific-roadmap-audit-2026-11-18
766b3788d22b8591b24020753f71fd9a17875d7a exploratory/natural-solver-feasibility-pilot
163d063a216bf0ab6850e5da536c515a2189097b fix/h3-v9-provenance-fail-closed-2026-10-31
f4e47f4e537152c0b893adb439e58b25ba5030f9 fix/h3-v9-provenance-hardening-2026-11-01
e22da84b41d5009628dc55a59f76e0aa442095a3 foued2-patch-1
ef69089b2005a7e3830f68c02be880a251dce951 foued2-patch-2
2d5f9c38f8b52bdf0204287a1a1cb74089a4a267 foued2-patch-3
ead0e02cdb697edc7878875cba4c7611fcd3b97c gate/h3-footprint-2026-10-26
ac05d3032908e2af191b61de27f56a0634967154 gate/h3-footprint-v3-2026-10-27
f82e44b05f9232242b31d1da92541433dce2e013 gate/h3-footprint-v4-2026-10-27
5c1b64ce080ae6fd3db8914fbe7250f71babc044 gate/h3-footprint-v5-2026-10-27
61a8c81cdf2b0f484d024942c3fcc834557a89ad gate/h3-footprint-v6-2026-10-27
1679544a78b0b898044cc7607aec527cd884738b gate/h3-footprint-v7-2026-10-27
d5b002cf0802b54b5a18b81e6bb99a9566cdd5ff gate/h3-footprint-v8-2026-10-27
1bb90b4daa1dbe79436371123ad9f1e493d179e8 glm/h3-feasibility-evidence-2026-10-29
3e9a29c9652a6ab4f6bab0919e386757280b2654 glm/lc518-150-design-handoff-2026-11-01
0e9b3fcea23cacaf81a63e2c910f47df54231005 glm/lc518-150-review-v1.2-2026-11-01
4608922ee08cc579c4bca5b7aef9465504269422 glm/lc518-150-work-order-clean-2026-11-01
46d548f026b6aee23f31e0d2e2fe2a773bef609a gpt/b1-computational-plan-2026-11-14
ac06c6676982eed795db9cb04c6d91803b591ac7 gpt/b1-m1-rev1.2-review-chain-2026-11-14
ad8742d813481ca1e57b25c0840eef602391394e gpt/copilot-ai-review-resolution-2026-11-01
f9cc893acb6d715c2c93c4ca90e548bf9cf5c45f gpt/h3-v10-integrity-fix-2026-10-29
511bc2099ecff74b4f850b169ceef7f853c334a0 gpt/lc518-150-analysis-review-2026-11-02
976ae04c712ad4720baf58f078fbb2518ba2acd1 gpt/lc518-150-construction-work-order-2026-11-01
fa310c0f8dae1c6d3a58456fbb723df3a602bd85 gpt/lc518-150-review-followup-2026-11-01
4169f9b2f6ace5b5a2a7a6d330558d88db8080d1 gpt/lc518-150-v1.2.2-atomic-acceptance-review-2026-11-01
60021ea34d60e341ccbd02b887bec9a2c6234095 gpt/lc518-150-v1.2.2-c9-corrections-2026-11-01
f81301037adb5e868922b192afce3f449adda0b5 gpt/lc518-150-v1.2.2-claude-final-doc-fixes-2026-11-01
0e22a8512f5c41fdfa5da972c9f49e218e97efe4 gpt/lc518-150-v1.2.2-claude-round2-fixes-2026-11-01
d7267b4596ab7909a82838ec1f5e3fdc2b94432f gpt/lc518-150-v1.2.2-heldout-first-2026-11-01
96da10721ef6ec6ddbc43244cb970e0b889bf15f gpt/lc518-150-v1.2.2-heldout-first-claude-fixes-2026-11-01
278429789a5a47b137471d87a9cb490739a723b7 gpt/lc518-claim-b1-primary-2026-11-05
a4ec1148698fe6612c5e873f1193069538a206e3 gpt/lc518-github-recovery-2026-11-02
7365ad5138595cd82736d325aea3fee28c85bcc0 gpt/lc518-m1si-audit-2026-11-17
bb027c1ce247a9a7d09fc09447400e8ff5a2e1cf gpt/nov06-expanded-mutation-search-review-2026-11-10
e4bb6ee009dd57d38c7a3b5f6694d81043918f21 gpt/rev-d-review-corrections
33dca9b61d95b9fb750f750919c32c2e08b2ee90 master
de39291d17a41b35109018b0f0d58541635adbbd research/concentration-math-spec
0d2e2507f4d3aa6b93998449c0480915565f7eec research/h3-v4-anonymous-model-prototype-2026-10-28
4551cacb757ca39aa31b88338f2abd0a67611cb5 review/a1-package
ac38d05f015450c7ff2c63f2f1073df47fcbbdd3 review/b1-analysis-plan-v1.6-transfer-2026-11-14
19b3d82cbbcc5d2a956ec52768c8ba6edbe1f64e review/concentration-formulation-2026-10-25
47ef6923f7c640751a7887d48ac7e4619d029368 review/feasibility-protocol-2026-10-25
ef1bb3730c917455c9c2f33a94b2c43740be1fc3 review/glm-h3-evidence-audit-2026-10-29
ddad85b2600904ef98b37a407b0d46b759cb3e10 review/h3-footprint-v8-postfreeze-audit-2026-10-27
9592d45194c4ae1e60de92a9bee6a01297c09499 review/h3-taxonomy-cell-rules-draft-2026-10-30
922af5a383d9ffec4a86b441c84ecaff0df56b19 review/lc518-c9-dryrun-claude-2026-11-01
c70a3870bc23fb973de4c8c7632f84ce0331bb33 review/m3-addendum
4d7517a1a30f47d3c41fb9f0ee6eed4397e8e05e review/o2-package
bec5d462a5f0c40fe44cac9d8915314943fd1634 review/option-b-construction-audit
eb46a2c9fe165b7f19f8c88f1e932f9e8df5a430 review/revd-package
79f1d1f2c4a603dc7f15984e2697aab982065191 review/reve-package
d9b491e8463358185c94e870fece646bd0fd9ef6 review/revf-package
5ffbb6ed638a8c01e598a3946106ed6f7fee7339 review/revg-package
c884685fa188e1eefd09524dd58c5ebb99de8de7 review/target-bridge-vdraft
94a758ec9672adc7f4b89d89497f19868b4d48ca transfer-artifacts
8be642797c4a3f5c1c585894056920db4c699a78 work/h3-v10-hosted-executor-prototype-2026-10-29
d79996d2b0f5e95283c2db96bddae8ba17406d21 work/h3-v9-battery-hosted-agent-path-2026-10-28
```

## Appendix B — verification commands

```
git ls-remote --heads origin
git ls-tree -r origin/<branch> --name-only
git cat-file blob 8c666e501a31726c728447d155045c0b20adc178
git hash-object <file>
```

Tree and blob presence establishes file identity only. It does not establish that any archived program
works or that any scientific claim is true.
