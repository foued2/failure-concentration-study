# REPOSITORY STORAGE INVENTORY — 2026-11-05

**Purpose:** make this repository express exactly what it stores. Every scientific artifact,
its location (branch/commit/archive member), its hash where established, and its exposure
class. Companion register: `CLAIM_AUDIT_MATRIX_2026-11-05.csv` (rev 3, 77 claim rows,
P01–L35; carries
forward the 2026-11-03 matrix and adds the claims generated since; status vocabulary in
Appendix B). Rev-3 correction: earlier revisions said "73 claim rows"; the actual CSV count
is 77 (verified by CSV parse on 2026-11-05).

**Author:** Qoder CLI (independent reviewer). **Status:** Rev 3 (2026-11-05, second
external-review round). Rev 1 was
committed locally as `142c3b8` on the local branch `research/concentration-math-spec`; that
branch is absent from every remote ref as of 2026-11-05, so the committed drafts are a local
record, not yet an auditable published repository record. Rev 2 corrections (uncommitted
working-tree edits, per the 2026-11-05 external review): v0.2 precision and interpretation
split (N03, N09), v1.0-vs-revision-2.6 E3 separation (L29–L30), bank independence caveat
(L31), narrowed provenance wording, storage claims pinned to exact commit SHAs and branches,
separate local-workspace inventory (§5), and an append-only verification-log correction (§6).
Rev 3 corrections (uncommitted working-tree edits, second external-review round): the
sanitized redistribution ZIP's exposure class corrected from PUBLIC-LIVE to **LOCAL-ONLY**
(§2); original Actions artifact contents verified by authenticated retrieval and independent
recomputation (§2, §6; matrix L09/L11/L34/L35); matrix L10 rewritten as DISCREPANCY_OPEN on
the runner-image identity conflict; the exact ref census delivered as Appendix A — resolving
81 refs vs 80 table memberships (`refs/tags/v0.2-freeze` was unaccounted) — and the
claim-status vocabulary delivered as Appendix B; `VERIFICATION_LOG.md` recorded as an
untracked local-only working copy (§4) carrying append-only addendum 2 (§6).
**Method:** read-only (`git ls-tree`,
`git cat-file`, in-memory archive inspection, unauthenticated GitHub API). Verification
artifacts: `C:/Users/pakla/AppData/Local/Temp/lc518_r5_review/` (`checkA_out.txt`,
`checkB_out.txt`, `checkB2_out.txt`).

---

## 1. Storage topology — the scientific record is split across 81 refs

The repository does not store its scientific content in one tree. There is **no branch
that carries everything**. The local science-audit branch `research/concentration-math-spec`
carries only the natural-solver and engineered-solver study material — **no LC518 and no
H3 study content** in its tracked tree. Branch tip: `8bb2e82` at drafting time; `142c3b8`
after the 2026-11-05 audit-record commit (adds only the two audit records). "HEAD" in this
inventory always means that local branch tip, verified by tree listing — it is never a
repository-wide state. In particular the remote default branch `origin/master` tip `b3e9874`
**does** carry LC518 content (`lc518_generator_state1.py`, `lc518_generator_state2.py`,
`lc518_generator_scratch_GLM_review_v1.2.zip`, `.github/workflows/lc518-github-generation.yml`,
`lc518-150/review-v1.2/c9-dryrun/REPORT_C9_DRYRUN.md`), and local `master` (`edae42c`) is a
different, older tree carrying design/review packages only.

Ref-count basis (Appendix A): the 81 refs are the local ref namespace enumerated by
`git for-each-ref` on 2026-11-05 — 18 local heads, 53 `origin/*` remote-tracking heads,
10 tags.

| Content group | Refs | Refs (representative) |
|---|---|---|
| Natural + engineered study (v0.1 pilot, v0.2, inventory, engineered-study, next-task) | 6 | `research/concentration-math-spec` (HEAD), `review/option-b-construction-audit`, `origin/review/concentration-formulation-2026-10-25`, `origin/review/feasibility-protocol-2026-10-25` |
| Design/review packages for the above (v02 + v03p + rlc0, no engineered-study) | 18 | `master` (local), `review/revd…revg-package`, `review/a1-package`, `review/m3-addendum`, `review/o2-package`, `review/target-bridge-vdraft` |
| LC518 (lc518-150 + v02 + v03p + rlc0) | 23 | **live: `origin/master`, `origin/foued2-patch-1`, `origin/foued2-patch-2`, `origin/gpt/lc518-github-recovery-2026-11-02`**; local containment: `lc518-containment/{master,foued2-patch-1,recovery-2026-11-02}`; packages: `review/lc518-containment-r{3,4,5}-2026-11-04`; design/review: `origin/glm/lc518-150-*`, `origin/gpt/lc518-150-*` |
| H3 footprint (v02, v03p, rlc0, engineered-study, natural-feasibility-pilot, next-task + h3-footprint) | 28 | 20 `origin/*` branches + 8 tags: `h3-footprint-freeze-2026-10-26` and `h3-footprint-v2..v8-freeze`; **no local branch** |
| Exploratory natural feasibility pilot | 2 | `exploratory/natural-solver-feasibility-pilot` (+origin) |
| LC518 construction work order variant | 1 | `origin/gpt/lc518-150-construction-work-order-2026-11-01` (adds engineered-study to LC518 tree) |
| Transfer artifacts | 1 | `origin/transfer-artifacts` (v02 + rlc0 subset) |
| v0.1 freeze tag | 1 | `refs/tags/v0.1-freeze` |
| v0.2 freeze tag | 1 | `refs/tags/v0.2-freeze` |

Rev-3 reconciliation: Rev 2's table summed to 80 against 81 refs because
`refs/tags/v0.2-freeze` was covered by no row, while the H3 row's count of 28 already
included `h3-footprint-freeze-2026-10-26` although its text named only the v2–v8 tags (a
text/count mismatch, not a count omission). Both are fixed above; the exact one-row-per-ref
census is Appendix A.

Head counts at the local branch tip `142c3b8`: pilot 2, v02 21, v03p 35, rlc0 111, gates 2, generation 21,
generation_v02 120, specs 2, study 7, scripts 3, engineered-study 84,
measurement-calibration 4, natural-feasibility-pilot 1,377, next-task 424,
sandbox-validation 15 files.

## 2. LC518 artifact exposure register

Exposure classes: **PUBLIC-LIVE** (committed at a live GitHub tip), **LOCAL-ONLY**
(local branch/worktree, not pushed), **HISTORY-ONLY** (recoverable from git history, not
at any tip), **MISSING** (never reached the repository), **AUTH-GATED** (public artifact
store outside git; retrieval requires authentication — anonymous request returns 401).

| Artifact | Hash (SHA-256 of bytes unless noted) | Location | Class |
|---|---|---|---|
| Activated generator (state2, variant A) | `1335a42d06d64cf7…` | tracked at all four live tips (`lc518_generator_state2.py`; recovery also `c9-execution-recovery/`) | PUBLIC-LIVE |
| Activated generator (state2, variant B) | `b4dfdef828374f32…` | tracked at live recovery tip (`c9-github-execution/lc518_generator_state2.py`) | PUBLIC-LIVE |
| Activated launcher | `79e5ba358485e942…` | tracked at live recovery tip (`c9-github-execution/lc518_launcher_state2.py`) | PUBLIC-LIVE |
| Activated generator, neutral name | `848984cac4275479…` | inside `lc518-publish-set-12-files-run-41591572358.zip` at live `foued2-patch-1` (blob `301e8e16…`); kit tar on live recovery | PUBLIC-LIVE |
| Activated launcher, neutral name | `014e45c259771b18…` | same two locations as above | PUBLIC-LIVE |
| Configured state-1 generators | content `276b9f49…` (variant A), `f73b189d…` (variant B) | tracked at all four live tips / live recovery | PUBLIC-LIVE |
| Activation recipes | `activation_diff.txt` (root, 3 tips); `c9-github-execution/activation_generator.diff`, `activation_launcher.diff` (live recovery) | see §3 workflows | PUBLIC-LIVE |
| Generation workflow | blob `729dc5a3…` (identical at all four tips); dispatch-only, `environment: lc518-bank-generation`, `contents: read` | `.github/workflows/` all four live tips | PUBLIC-LIVE |
| Recovery workflow | blob `e9fb2038…`; push+PR+dispatch (dispatch **not receivable** — file absent from default branch), `contents: write`, no environment, auto-commit/push of built package | live recovery tip only | PUBLIC-LIVE |
| c9-github-generation kit (tar, 348,160 B) | assembled from 5 `part-*.b64` (base64→XZ→TAR); contains state2s `848984ca…`/`014e45c2…`, both activation diffs, gate, GO record `5c4cd6eb…` | `lc518-150/c9-github-generation-package-parts/` at live recovery tip | PUBLIC-LIVE |
| Original GitHub Actions run artifact (run 41591572358, ID `13210063805`, 75,523 B) | `6e6d60c1cb703ed8…` (authenticated retrieval 2026-11-05 — GPT and this audit independently; archive digest and all 15 member hashes recomputed, matching `logs/run_manifest.json`; anonymous download still returns 401) | GitHub Actions artifact store (not a git object); 15 members: run manifest, both run logs, both source files, protocol, both test files, six bank artifacts, disjointness report | AUTH-GATED |
| Sanitized bank redistribution ZIP `lc518-bank-artifact-run-41591572358.zip` (containment repack of the run's outputs, 2026-11-03; exactly the two neutral-name executable members removed, other members byte-identical) | `71f1e76b03161d91…` | `lc518-containment/foued2-patch-1` (`SHA256SUMS` records member hashes incl. `bank/heldout_bank.json` `b273c053…`, `bank/heldout_oracle_outputs.json` `eaae8104…`) | **LOCAL-ONLY** (Rev 3 correction: Rev 2 mislabelled this PUBLIC-LIVE; the `lc518-containment/*` branches are local-only and absent from every remote ref; not byte-identical to the original Actions artifact) |
| Publish-set ZIP (12 files) | `16ce5a6a…` (blob `301e8e16…`) | live `foued2-patch-1` tip | PUBLIC-LIVE — **contains diagnostic + held-out banks, both oracle-output files, and the two neutral-name executable copies** |
| Scratch review ZIP (10 members) | `4a730207…` (blob `48029599…`) | all live and containment tips; pre-activation v1.2 review snapshot, flags False | PUBLIC-LIVE (fail-closed as shipped) |
| Message ZIPs (corrections records, verification map) | documents only | all tips | PUBLIC-LIVE (inert) |
| r2 review package | inside `lc518_containment_review_package_2026-11-04_r2.zip` at live `foued2-patch-2`; recursively scanned: zero `=True`, zero activated matches | live `foued2-patch-2` | PUBLIC-LIVE (inert; retain recommended) |
| Review packages r3/r4/r5 | `19880cc3…` / `7f55430a…` / `8f8c259a…` | local branches `review/lc518-containment-r{3,4,5}-2026-11-04` (blobs `3a182efd…`/`aae05bb8…` for r4/r5) | LOCAL-ONLY (not pushed) |
| Containment chains 0001–0004 (3 branches) | tips `fd4bcac9`/`05abb63e`/`38e0b98a`; trees `cf7b480b…`/`f5d8600d…`/`b07a008e…` | local branches `lc518-containment/*` | LOCAL-ONLY |
| Proposed containment for `foued2-patch-2` | — | none exists yet | MISSING (panel-approved four-chain plan) |
| Private mutation annex (eight-mechanism taxonomy; 28+2 pair-allocation schedule; S-extra balancing) | — | nowhere in any ref, any history path, or any archive member; stop rule invoked (`glm-handoff/worklog.md`, work order :45/:47) | MISSING |
| 150 solver bodies | — | 0/150 constructed (CORRECTIONS_RECORD; VERIFICATION_MAP) | MISSING (by design, pending annex) |

## 3. Sealed/missing register — what the repo stores vs what the design assumed

| Design intent (source) | Stored reality | Consequence |
|---|---|---|
| Held-out bank "measures correctness on inputs not used to construct diagnostic features; defines the finite target distribution for Q" (BANK_DESIGN.md §1) | Bank + oracle answers are PUBLIC-LIVE in two artifacts (§2). Structural claims intact (disjointness, 80 records, int32 guard — L03–L06). Secrecy void. Verified canonical disjointness is **not** statistical independence: the C9 held-out-first generation conditions diagnostic-side candidate selection on the frozen held-out bank, and revision 2.6 §7 states the accepted banks must not be described as statistically independent samples (L31). BANK_DESIGN.md §7's generator-independence claim describes the v1.0 design, not the realized C9 procedure. | Cannot serve as a sealed confirmatory evaluation set. Usable for development/debugging only. A replacement bank requires an independent custodian after solver-source freeze. |
| "The repository branch and public construction package must not contain per-solver mechanism assignments or defect labels" (work order §4) | Holds — no such assignments exist anywhere (repo-wide path + content search, 2026-11-05). | E1 contrasts undefined: taxonomy, 28+2 pair schedule, S-extra balancing all MISSING. Supply the annex or formally drop the mutation design. |
| GO `LC518-GO-2026-11-03-01` authorizes bank generation only (OWNER_GO_RECORD) | Consumed by run 41591572358; authorizes nothing further (hold documents). | No open authorization exists. |
| Environment `lc518-bank-generation` gates generation dispatch | Verified live: sole reviewer `foued2`, `prevent_self_review=false`, `can_admins_bypass=true`. The agents act through that same identity. | Not a security control. Workflow disable is the only binding immediate lever (pending owner action). |

## 4. Untracked artifacts in the working tree (not git content)

- `VERIFICATION_LOG.md` — untracked working-tree file at the repository root of local branch
  `research/concentration-math-spec`; not committed on any ref as of 2026-11-05 (the sole
  committed version is blob `a851183e…`, first committed at `552004e`, present at
  `origin/master` tip `b3e9874`). It carries append-only addenda 1–2 (2026-11-05); the
  working-tree SHA-256 after addendum 2 is recorded in §6.
- `LC518_CONCENTRATION_ESTIMAND_REVIEW_2026-11-05.md` — untracked working record
  (repository root): consolidation of the 2026-11-05 scientific review chain — Claude
  memo and its three corrections, the A1a capacity check, the Claim A/B estimand fork,
  the Claim B recommendation (**owner ratification pending**), the B1/B2 fork with the
  annex-free allocation-support arithmetic, and the GLM verification. Recommendation
  only; authorizes nothing. SHA-256 of the working-tree file:
  `720dda25f72bf71624a09c6035ab64aaf3150d80ac2984088591dafa161256cb`.
- `CLAIM_AUDIT_MATRIX_2026-11-03.csv` — prior 59-claim audit; untracked; superseded in-tree by the rev-2 companion CSV.
- `PROJECT_DEVELOPMENT_TREE_2026-11-03.*`, `PROJECT_DECISION_TREE_2026-11-03.*` — untracked analysis artifacts; `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md`, `FREEZE.md`, `PROTOCOL.md` are tracked; see `git status`.
- `.qoder_*` files — reviewer working notes/summaries, untracked, not project records.

## 5. Local-workspace inventory (local storage — not git-tracked repository content)

Recorded separately from the git inventory so local state is never reported as tracked
repository content. Three distinct storage states are inventoried and never mixed:
(1) **Git-tracked files** — §1–§3; (2) **local uncommitted/untracked evidence** — the
preserved stratum pair below; (3) **quarantined historical snapshots** — the moved checkout
below.

| Item | Classification (exact SHAs) | Disposition 2026-11-05 |
|---|---|---|
| `failure-concentration-study/` (nested clone with its own `.git`, branch `research/concentration-math-spec`) | Stale checkout of this same branch: nested HEAD `ae36765` (2026-10-25 06:19, "Publish outstanding local study records and project config") is an ancestor of this branch tip `142c3b8`; the older `886a6d5` (2026-10-24) is also an ancestor of `ae36765`. Rev 1 of this inventory said "corresponds to `886a6d5`" — corrected: the tracked tree is `ae36765`. | Unique evidence extracted (next row); snapshot then quarantined — moved intact to `_quarantine/stale-checkout-ae36765/` with its own `.git` and untracked archives preserved. Not deleted. |
| `engineered-study/math/results/three_world/stratum_specific_analysis/{STRATUM_SPECIFIC_CONTRASTS_2026-10-24.md, stratum_specific_contrasts_2026-10-24.json}` (untracked inside the nested clone only) | Earlier saved-record-only run of the same analysis that produced the committed `15_STRATUM_SPECIFIC_CONTRASTS_REPORT_2026-10-25.md` (commit `0487bf8`): identical manifest hash `16af20b8…` and identical counts (20,000,000 records; 19,999,737 eligible; 263 k=0; 973 strata; 756 multi-C). The committed report is summaries-only (123 lines); the 10-24 pair uniquely retains the full 973-stratum table (3,558 lines, 217 NOT-IDENTIFIABLE rows) and the per-C-level means JSON (1,094,749 bytes). | Preserved 2026-11-05 by copy to `engineered-study/math/results/three_world/stratum_specific_analysis_2026-10-24/` (SHA-256 `89a8efc8…` for the MD, `542ef86d…` for the JSON; copies byte-verified against originals). Descriptive only — the frozen W1 FAILED disposition (S01, S05) is unaffected. Classification: **preserved supplementary analytical evidence, with matching analysis provenance indicators; complete raw-data equivalence (`per_trial.json`, `raw/`) not yet verified** — not a fully reproduced dataset. |
| `_quarantine/stale-checkout-ae36765/` | Quarantine location for the stale checkout. It also holds `per_trial.json` and `raw/` copies; the outer working tree independently retains its own untracked `per_trial.json` and `raw/` under `engineered-study/math/results/three_world/`. Those two sets were **not** byte-compared against each other. | Owner may remove after accepting this comparison record; the unique stratum pair no longer exists solely inside it. |

## 6. Verification chain (what record-keepers can rely on)

| Date | Verifier | Result |
|---|---|---|
| 2026-11-03 | Qoder (prior session) | 59-claim audit matrix; inventory collector hashes |
| 2026-11-04 | GLM; GPT | r3/r4 packages; environment queries; activation-flip proof (§10.3) |
| 2026-11-05 | Qoder (this session) | r5 archive `8f8c259a…`: 940-row manifest verified vs member bytes; 12 patches replayed from original tips reproducing exact commit hashes; exports byte-identical (304/306/317 files); §10.3 counts 4/5/17=26 absent; Environment config verified live (unauthenticated API); checks A/B: live-tip exposure, kit assembly, annex absent repo-wide; run baseline (none queued/active) |
| 2026-11-05 | GPT | independent remote fetch of live sources and both workflow YAMLs |
| 2026-11-05 | Claude | Composio blob checks of live state1/state2/workflow (generation workflow only; recovery and publish-set rely on Qoder scan) |
| 2026-11-05 | Qoder (rev 2) | Review corrections re-verified at source: v0.2 exact values read from `v02/confirmatory_v02/confirmatory_v02_report.json` with rounded display from `REPORT_V02.md` §2; E3 v1.0 §6 vs revision 2.6 §§1/3/4/7/8 read at commit `511bc20` (ref `origin/gpt/lc518-150-analysis-review-2026-11-02`); snapshot lineage verified (`ae36765` ancestor of `142c3b8`); unique 10-24 stratum pair compared and preserved; `VERIFICATION_LOG.md` located as blob `a851183e` (commit `552004e`) and appended append-only |
| 2026-11-05 | Qoder (rev 3) + GPT | Original Actions artifact `13210063805` retrieved through authenticated access independently by both; archive SHA-256 `6e6d60c1…` and all 15 member hashes recomputed and matched to `logs/run_manifest.json` (generator `848984ca…`, launcher `014e45c2…`, exit 0, ACCEPTED); launcher self-hash mechanism verified in the executed bytes (`lc518_launcher.py:326/:391/:451/:370`); runner-image discrepancy recorded (L10); 81-ref census built from `git for-each-ref` plus per-tip `git ls-tree` (Appendix A); `ubuntu24/20261025.353` confirmed absent from `actions/runner-images` releases (HTTP 404; only ubuntu24 releases in that window: `20261026.354`, `20261101.360`); job-log download requires admin authentication (403 anonymously) |

Designated Claude review of the r5 ZIP was **not** performed; the r5 integrity record rests on GLM's verification plus the Qoder review above.

**Provenance wording (narrowed per review).** Exactly two unresolved hash-verification gaps
remain in the claim matrix: N06 (v0.2 pack manifest hash; ledger F9) and E05
(`selected_profiles.json` hash). This must not be read as "only two unresolved provenance
problems": the v0.2 findings ledger separately records the generator-chronology (F10) and
documented-output-path/description (F11) discrepancies as **verified inconsistencies** with no
unresolved hash component, and F12 found no content alteration of the pack, analysis code, or
terminal report.

**Verification-log correction (append-only).** The repository `VERIFICATION_LOG.md` (sole
version: blob `a851183e`, first committed at `552004e`, present at live tips) records on
2026-11-02 that "No bank, run root, staging directory or oracle output exists. State 2 was
never executed." That statement was true when recorded and is preserved unmodified. A dated
2026-11-05 supersession record has been appended to the working-tree copy (created from the
`b3e9874` blob; no prior line edited), documenting the 2026-11-03 authorized bank generation
as four distinct objects: owner GO `LC518-GO-2026-11-03-01` (GO-record file SHA-256
`5c4cd6eb…` at `lc518-containment/recovery-2026-11-02`); C9 source digest `f291ae87…`
(= SHA-256 of `C9_GENERATION_SPEC_REVIEW.md` rev 2.6 at `511bc20`; neither the protocol-v2
digest nor a Git object ID); execution protocol v2 `execution_protocol_github_v2.json`
content SHA-256 `9c54ffc2…`; original Actions artifact `13210063805` SHA-256 `6e6d60c1…`
(GPT remote verification 2026-11-05; anonymous download 401); and the later sanitized
redistribution ZIP `71f1e76b…` at `lc518-containment/foued2-patch-1`, which removed two
executable members from publication set `16ce5a6a…` and is not byte-identical to the
original artifact. Run `41591572358`, head `a4ec114`. Working-tree `VERIFICATION_LOG.md`
after addendum 1 (53 lines) SHA-256:
`bd4383ab1973d99b2390122010d5bbf798acd1b0563f17013c08c51c1c289d7f`.
**Addendum 2 (2026-11-05, append-only, second external-review round)** supersedes addendum
1's "not locally reproduced" characterization — which remains unmodified in the file — with
the accurate record: authenticated retrieval of artifact `13210063805`, independent
recomputation of the archive digest and all 15 member hashes, generator-execution provenance
VERIFIED (matrix L34/L35), the launcher-hash precision finding, the runner-image discrepancy
(L10), and the ref-census correction. Working-tree `VERIFICATION_LOG.md` after addendum 2
(123 lines) SHA-256:
`09a9393cd60a1639a26ac0dd13439ad6168ed2c3d35bca5545356320907335ea`.

**Two revision-2.6 documents — do not merge their statuses.** The C9 **generation**
specification rev 2.6 (`lc518-150/review-v1.2/analysis-revision-2026-11-02/C9_GENERATION_SPEC_REVIEW.md`,
SHA-256 `f291ae87…`) had its exact source owner-ratified for bank generation
(`LC518-GO-2026-11-03-01`). The **analysis** specification rev 2.6
(`ANALYSIS_SPEC_REVIEW_DRAFT.md`, same directory) remains a review-only draft and is not
the frozen analysis design; frozen v1.0 remains the design of record (L14, L29–L30).

## 7. What this inventory does not claim

- It does not claim statistical independence of the generated banks — only verified canonical disjointness, conditional generation, and public exposure (L31, §3).
- It does not claim the live repository is contained (it is not — see L19–L21, L24–L26).
- It does not authorize construction, execution, dispatch, or publication of anything.
- It does not resolve the research-objective decision (panel recommendation: Option 2, separate engineered-population study — owner decision in writing pending).
- Hashes abbreviated to 16 hex chars here are recorded in full in the verification artifacts and prior records.

---

## Appendix A — Exact ref census (81 rows; Rev 3)

**Counting basis.** The 81 refs are the local ref namespace enumerated by `git for-each-ref`
on 2026-11-05: 18 local heads (`refs/heads/*`), 53 remote-tracking heads
(`refs/remotes/origin/*`), 10 tags (`refs/tags/*`). One row per ref; no ref appears twice;
the rows sum to 81. Tips are short SHAs; tags are peeled to their commit. This census is
authoritative over the §1 summary table.

**Content labels** (from each tip's top-level `git ls-tree`): `pilot` v0.1 pilot · `v02` v0.2
study · `v03p` v0.3-P design package · `rlc0` formal localization · `eng` engineered-study ·
`nfp` natural-feasibility-pilot · `next` next-task · `mc` measurement-calibration · `sbx`
sandbox-validation · `h3` h3-footprint (one or more version dirs) · `lc518` lc518-150 · `cf`
concentration-formulation · `reviews` LC518 containment review packages · `transfer` transfer
bundle + worktree ZIP · `revdir` design-review workspace subdir · `wf` `.github/workflows`
present. Common infrastructure present on every ref: `.gitignore`, `FREEZE.md`,
`PROTOCOL.md`, `README.md`, `gates/`, `scripts/`, `specs/`, `study/`; `v02/` on all except
row 80; `v03p/` absent only from rows 69, 80, 81.

**Group assignment rule:** tags named `v0.x-freeze` → own rows; `h3-footprint*` tags → H3;
`exploratory/natural-solver-feasibility-pilot` (both) → EXPL; transfer bundle → TRANSFER;
tree contains `h3` → H3; `lc518`+`eng` → WO-VAR; `lc518` → LC518; `eng`/`cf` → N+E;
otherwise DES-REV.

| # | Ref | Kind | Tip | Group | Content labels |
|---|---|---|---|---|---|
| 1 | `exploratory/natural-solver-feasibility-pilot` | local head | `766b378` | EXPL | mc nfp next pilot rlc0 sbx v02 v03p |
| 2 | `lc518-containment/foued2-patch-1` | local head | `05abb63` | LC518 | lc518 pilot reviews rlc0 v02 v03p |
| 3 | `lc518-containment/master` | local head | `fd4bcac` | LC518 | lc518 pilot reviews rlc0 v02 v03p |
| 4 | `lc518-containment/recovery-2026-11-02` | local head | `38e0b98` | LC518 | lc518 pilot reviews rlc0 v02 v03p |
| 5 | `master` | local head | `edae42c` | DES-REV | pilot rlc0 v02 v03p |
| 6 | `research/concentration-math-spec` | local head | `142c3b8` | N+E | eng mc nfp next pilot rlc0 sbx v02 v03p |
| 7 | `review/a1-package` | local head | `4551cac` | DES-REV | pilot rlc0 v02 v03p |
| 8 | `review/lc518-containment-r3-2026-11-04` | local head | `cdbe43e` | LC518 | wf lc518 pilot reviews rlc0 v02 v03p |
| 9 | `review/lc518-containment-r4-2026-11-04` | local head | `2f42cf3` | LC518 | wf lc518 pilot reviews rlc0 v02 v03p |
| 10 | `review/lc518-containment-r5-2026-11-04` | local head | `a1d3177` | LC518 | wf lc518 pilot reviews rlc0 v02 v03p |
| 11 | `review/m3-addendum` | local head | `c70a387` | DES-REV | pilot revdir rlc0 v02 v03p |
| 12 | `review/o2-package` | local head | `4d7517a` | DES-REV | pilot revdir rlc0 v02 v03p |
| 13 | `review/option-b-construction-audit` | local head | `bec5d46` | N+E | eng mc nfp next pilot rlc0 sbx v02 v03p |
| 14 | `review/revd-package` | local head | `eb46a2c` | DES-REV | pilot rlc0 v02 v03p |
| 15 | `review/reve-package` | local head | `79f1d1f` | DES-REV | pilot rlc0 v02 v03p |
| 16 | `review/revf-package` | local head | `d9b491e` | DES-REV | pilot rlc0 v02 v03p |
| 17 | `review/revg-package` | local head | `5ffbb6e` | DES-REV | pilot revdir rlc0 v02 v03p |
| 18 | `review/target-bridge-vdraft` | local head | `c884685` | DES-REV | pilot rlc0 v02 v03p |
| 19 | `origin/claude/h3-v10-adversarial-fixtures` | remote head | `8daf8d8` | H3 | wf eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 20 | `origin/dev/h3-footprint-v2-harness` | remote head | `9422e8e` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 21 | `origin/dev/h3-footprint-v9-implementation-2026-10-28` | remote head | `682a40d` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 22 | `origin/exploratory/natural-solver-feasibility-pilot` | remote head | `766b378` | EXPL | mc nfp next pilot rlc0 sbx v02 v03p |
| 23 | `origin/fix/h3-v9-provenance-fail-closed-2026-10-31` | remote head | `163d063` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 24 | `origin/fix/h3-v9-provenance-hardening-2026-11-01` | remote head | `f4e47f4` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 25 | `origin/foued2-patch-1` | remote head | `e22da84` | LC518 | wf lc518 pilot reviews rlc0 v02 v03p |
| 26 | `origin/foued2-patch-2` | remote head | `ef69089` | LC518 | wf lc518 pilot reviews rlc0 v02 v03p |
| 27 | `origin/gate/h3-footprint-2026-10-26` | remote head | `ead0e02` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 28 | `origin/gate/h3-footprint-v3-2026-10-27` | remote head | `ac05d30` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 29 | `origin/gate/h3-footprint-v4-2026-10-27` | remote head | `f82e44b` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 30 | `origin/gate/h3-footprint-v5-2026-10-27` | remote head | `5c1b64c` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 31 | `origin/gate/h3-footprint-v6-2026-10-27` | remote head | `61a8c81` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 32 | `origin/gate/h3-footprint-v7-2026-10-27` | remote head | `1679544` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 33 | `origin/gate/h3-footprint-v8-2026-10-27` | remote head | `d5b002c` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 34 | `origin/glm/h3-feasibility-evidence-2026-10-29` | remote head | `1bb90b4` | H3 | wf eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 35 | `origin/glm/lc518-150-design-handoff-2026-11-01` | remote head | `3e9a29c` | LC518 | lc518 pilot rlc0 v02 v03p |
| 36 | `origin/glm/lc518-150-review-v1.2-2026-11-01` | remote head | `0e9b3fc` | LC518 | lc518 pilot rlc0 v02 v03p |
| 37 | `origin/glm/lc518-150-work-order-clean-2026-11-01` | remote head | `4608922` | LC518 | lc518 pilot rlc0 v02 v03p |
| 38 | `origin/gpt/copilot-ai-review-resolution-2026-11-01` | remote head | `ad8742d` | LC518 | lc518 pilot reviews rlc0 v02 v03p |
| 39 | `origin/gpt/h3-v10-integrity-fix-2026-10-29` | remote head | `f9cc893` | H3 | wf eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 40 | `origin/gpt/lc518-150-analysis-review-2026-11-02` | remote head | `511bc20` | LC518 | lc518 pilot rlc0 v02 v03p |
| 41 | `origin/gpt/lc518-150-construction-work-order-2026-11-01` | remote head | `976ae04` | WO-VAR | eng lc518 mc nfp next pilot rlc0 sbx v02 v03p |
| 42 | `origin/gpt/lc518-150-review-followup-2026-11-01` | remote head | `fa310c0` | LC518 | lc518 pilot rlc0 v02 v03p |
| 43 | `origin/gpt/lc518-150-v1.2.2-atomic-acceptance-review-2026-11-01` | remote head | `4169f9b` | LC518 | lc518 pilot rlc0 v02 v03p |
| 44 | `origin/gpt/lc518-150-v1.2.2-c9-corrections-2026-11-01` | remote head | `60021ea` | LC518 | lc518 pilot rlc0 v02 v03p |
| 45 | `origin/gpt/lc518-150-v1.2.2-claude-final-doc-fixes-2026-11-01` | remote head | `f813010` | LC518 | lc518 pilot rlc0 v02 v03p |
| 46 | `origin/gpt/lc518-150-v1.2.2-claude-round2-fixes-2026-11-01` | remote head | `0e22a85` | LC518 | lc518 pilot rlc0 v02 v03p |
| 47 | `origin/gpt/lc518-150-v1.2.2-heldout-first-2026-11-01` | remote head | `d7267b4` | LC518 | lc518 pilot rlc0 v02 v03p |
| 48 | `origin/gpt/lc518-150-v1.2.2-heldout-first-claude-fixes-2026-11-01` | remote head | `96da107` | LC518 | lc518 pilot rlc0 v02 v03p |
| 49 | `origin/gpt/lc518-github-recovery-2026-11-02` | remote head | `a4ec114` | LC518 | wf lc518 pilot reviews rlc0 v02 v03p |
| 50 | `origin/gpt/rev-d-review-corrections` | remote head | `e4bb6ee` | DES-REV | pilot rlc0 v02 v03p |
| 51 | `origin/master` | remote head | `b3e9874` | LC518 | wf lc518 pilot reviews rlc0 v02 v03p |
| 52 | `origin/research/concentration-math-spec` | remote head | `8bb2e82` | N+E | eng mc nfp next pilot rlc0 sbx v02 v03p |
| 53 | `origin/research/h3-v4-anonymous-model-prototype-2026-10-28` | remote head | `0d2e250` | H3 | wf eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 54 | `origin/review/a1-package` | remote head | `4551cac` | DES-REV | pilot rlc0 v02 v03p |
| 55 | `origin/review/concentration-formulation-2026-10-25` | remote head | `19b3d82` | N+E | cf eng mc nfp next pilot rlc0 sbx v02 v03p |
| 56 | `origin/review/feasibility-protocol-2026-10-25` | remote head | `47ef692` | N+E | eng mc nfp next pilot rlc0 sbx v02 v03p |
| 57 | `origin/review/glm-h3-evidence-audit-2026-10-29` | remote head | `ef1bb37` | H3 | wf eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 58 | `origin/review/h3-footprint-v8-postfreeze-audit-2026-10-27` | remote head | `ddad85b` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 59 | `origin/review/h3-taxonomy-cell-rules-draft-2026-10-30` | remote head | `9592d45` | H3 | wf eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 60 | `origin/review/lc518-c9-dryrun-claude-2026-11-01` | remote head | `922af5a` | LC518 | lc518 pilot rlc0 v02 v03p |
| 61 | `origin/review/m3-addendum` | remote head | `c70a387` | DES-REV | pilot revdir rlc0 v02 v03p |
| 62 | `origin/review/o2-package` | remote head | `4d7517a` | DES-REV | pilot revdir rlc0 v02 v03p |
| 63 | `origin/review/option-b-construction-audit` | remote head | `bec5d46` | N+E | eng mc nfp next pilot rlc0 sbx v02 v03p |
| 64 | `origin/review/revd-package` | remote head | `eb46a2c` | DES-REV | pilot rlc0 v02 v03p |
| 65 | `origin/review/reve-package` | remote head | `79f1d1f` | DES-REV | pilot rlc0 v02 v03p |
| 66 | `origin/review/revf-package` | remote head | `d9b491e` | DES-REV | pilot rlc0 v02 v03p |
| 67 | `origin/review/revg-package` | remote head | `5ffbb6e` | DES-REV | pilot revdir rlc0 v02 v03p |
| 68 | `origin/review/target-bridge-vdraft` | remote head | `c884685` | DES-REV | pilot rlc0 v02 v03p |
| 69 | `origin/transfer-artifacts` | remote head | `94a758e` | TRANSFER | transfer pilot rlc0 v02 |
| 70 | `origin/work/h3-v10-hosted-executor-prototype-2026-10-29` | remote head | `8be6427` | H3 | wf eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 71 | `origin/work/h3-v9-battery-hosted-agent-path-2026-10-28` | remote head | `d79996d` | H3 | wf eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 72 | `tag:h3-footprint-freeze-2026-10-26` | tag | `016fb81` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 73 | `tag:h3-footprint-v2-freeze-2026-10-27` | tag | `9422e8e` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 74 | `tag:h3-footprint-v3-freeze-2026-10-27` | tag | `ac05d30` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 75 | `tag:h3-footprint-v4-freeze-2026-10-27` | tag | `f82e44b` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 76 | `tag:h3-footprint-v5-freeze-2026-10-27` | tag | `5c1b64c` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 77 | `tag:h3-footprint-v6-freeze-2026-10-27` | tag | `61a8c81` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 78 | `tag:h3-footprint-v7-freeze-2026-10-27` | tag | `1679544` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 79 | `tag:h3-footprint-v8-freeze-2026-10-27` | tag | `d5b002c` | H3 | eng h3 mc nfp next pilot rlc0 sbx v02 v03p |
| 80 | `tag:v0.1-freeze` | tag | `5bf80b7` | v0.1 tag | (common infra only) |
| 81 | `tag:v0.2-freeze` | tag | `798b446` | v0.2 tag | pilot v02 |

**Reconciliation with the §1 table.** N+E 6 · DES-REV 18 · LC518 23 · H3 28 · EXPL 2 ·
WO-VAR 1 · TRANSFER 1 · v0.1 tag 1 · v0.2 tag 1 = **81**. Rev 2's table summed to 80 because
`refs/tags/v0.2-freeze` (row 81) was covered by no row, while the H3 row's count of 28
already included `h3-footprint-freeze-2026-10-26` (row 72) although its text named only the
v2–v8 tags. The earlier hypothesis of two omitted tags is thus resolved: one genuine
omission (`v0.2-freeze`), one text/count mismatch (the H3 row).

## Appendix B — Claim-status vocabulary (Rev 3)

Normative meanings of the `status` column in `CLAIM_AUDIT_MATRIX_2026-11-05.csv`:

| Status | Meaning |
|---|---|
| `VERIFIED` | Checked directly against the stored bytes or a live source by this audit; the check is described in `independent_check` |
| `RECORDED` | The statement exists in a stored record and was read; content not re-derived |
| `RECORDED_VERIFIED` | Record statement plus an independent check short of full re-execution |
| `CONFIRMED` | Multiple independent stored records agree on cross-read |
| `ARITHMETIC` | Small arithmetic recomputed directly |
| `DESIGN_INTENT` | Describes design documents only; no outcome exists |
| `UNRESOLVED_PROVENANCE` | Provenance of stored bytes could not be established; recorded as open |
| `DISCREPANCY_OPEN` | Two stored observations conflict; both recorded; unresolved pending a defined check (introduced Rev 3 for L10) |
| `FALSE` | The stored record contradicts the claim |
| `FALSE_CATEGORY_ERROR` | The claim is a category error; not evidence of the claimed kind |

`UNVERIFIED_PROVENANCE` (L34 in Rev 2) is retired as of Rev 3: the row it labelled is now
`VERIFIED`. A status is a property of the evidence, not of the underlying claim; a row
marked `VERIFIED` supports only what its `what_it_does_not_support` column permits.
