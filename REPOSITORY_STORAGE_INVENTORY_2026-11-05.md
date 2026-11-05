# REPOSITORY STORAGE INVENTORY — 2026-11-05

**Purpose:** make this repository express exactly what it stores. Every scientific artifact,
its location (branch/commit/archive member), its hash where established, and its exposure
class. Companion register: `CLAIM_AUDIT_MATRIX_2026-11-05.csv` (carries forward the
2026-11-03 matrix and adds the claims generated since).

**Author:** Qoder CLI (independent reviewer). **Status:** review record, committed locally
on `research/concentration-math-spec`; not pushed. **Method:** read-only (`git ls-tree`,
`git cat-file`, in-memory archive inspection, unauthenticated GitHub API). Verification
artifacts: `C:/Users/pakla/AppData/Local/Temp/lc518_r5_review/` (`checkA_out.txt`,
`checkB_out.txt`, `checkB2_out.txt`).

---

## 1. Storage topology — the scientific record is split across 81 refs

The repository does not store its scientific content in one tree. There is **no branch
that carries everything**. Current HEAD (`research/concentration-math-spec` @ `8bb2e82`)
carries only the natural-solver and engineered-solver study material — **no LC518 and no
H3 content whatsoever**.

| Content group | Refs | Refs (representative) |
|---|---|---|
| Natural + engineered study (v0.1 pilot, v0.2, inventory, engineered-study, next-task) | 6 | `research/concentration-math-spec` (HEAD), `review/option-b-construction-audit`, `origin/review/concentration-formulation-2026-10-25`, `origin/review/feasibility-protocol-2026-10-25` |
| Design/review packages for the above (v02 + v03p + rlc0, no engineered-study) | 18 | `master` (local), `review/revd…revg-package`, `review/a1-package`, `review/m3-addendum`, `review/o2-package`, `review/target-bridge-vdraft` |
| LC518 (lc518-150 + v02 + v03p + rlc0) | 23 | **live: `origin/master`, `origin/foued2-patch-1`, `origin/foued2-patch-2`, `origin/gpt/lc518-github-recovery-2026-11-02`**; local containment: `lc518-containment/{master,foued2-patch-1,recovery-2026-11-02}`; packages: `review/lc518-containment-r{3,4,5}-2026-11-04`; design/review: `origin/glm/lc518-150-*`, `origin/gpt/lc518-150-*` |
| H3 footprint (v02, v03p, rlc0, engineered-study, natural-feasibility-pilot, next-task + h3-footprint) | 28 | all `origin/*` branches and `h3-footprint-v2..v8-freeze` tags; **no local branch** |
| Exploratory natural feasibility pilot | 2 | `exploratory/natural-solver-feasibility-pilot` (+origin) |
| LC518 construction work order variant | 1 | `origin/gpt/lc518-150-construction-work-order-2026-11-01` (adds engineered-study to LC518 tree) |
| Transfer artifacts | 1 | `origin/transfer-artifacts` (v02 + rlc0 subset) |
| v0.1 freeze tag | 1 | `refs/tags/v0.1-freeze` |

Head counts at HEAD: pilot 2, v02 21, v03p 35, rlc0 111, gates 2, generation 21,
generation_v02 120, specs 2, study 7, scripts 3, engineered-study 84,
measurement-calibration 4, natural-feasibility-pilot 1,377, next-task 424,
sandbox-validation 15 files.

## 2. LC518 artifact exposure register

Exposure classes: **PUBLIC-LIVE** (committed at a live GitHub tip), **LOCAL-ONLY**
(local branch/worktree, not pushed), **HISTORY-ONLY** (recoverable from git history, not
at any tip), **MISSING** (never reached the repository).

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
| Bank artifact (run 41591572358) | `71f1e76b03161d91…` | containment tips; members incl. `bank/heldout_bank.json` `b273c053…`, `bank/heldout_oracle_outputs.json` `eaae8104…` | PUBLIC-LIVE (at containment tips; bank bytes identical inside publish-set at live `foued2-patch-1`) |
| Publish-set ZIP (12 files) | blob `301e8e16…` | live `foued2-patch-1` tip | PUBLIC-LIVE — **contains diagnostic + held-out banks and both oracle-output files** |
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
| Held-out bank "measures correctness on inputs not used to construct diagnostic features; defines the finite target distribution for Q" (BANK_DESIGN.md §1) | Bank + oracle answers are PUBLIC-LIVE in two artifacts (§2). Structural claims intact (disjointness, 80 records, int32 guard — L03–L06). Secrecy void. | Cannot serve as a sealed confirmatory evaluation set. Usable for development/debugging only. A replacement bank requires an independent custodian after solver-source freeze. |
| "The repository branch and public construction package must not contain per-solver mechanism assignments or defect labels" (work order §4) | Holds — no such assignments exist anywhere (repo-wide path + content search, 2026-11-05). | E1 contrasts undefined: taxonomy, 28+2 pair schedule, S-extra balancing all MISSING. Supply the annex or formally drop the mutation design. |
| GO `LC518-GO-2026-11-03-01` authorizes bank generation only (OWNER_GO_RECORD) | Consumed by run 41591572358; authorizes nothing further (hold documents). | No open authorization exists. |
| Environment `lc518-bank-generation` gates generation dispatch | Verified live: sole reviewer `foued2`, `prevent_self_review=false`, `can_admins_bypass=true`. The agents act through that same identity. | Not a security control. Workflow disable is the only binding immediate lever (pending owner action). |

## 4. Untracked artifacts and provenance hazards (working tree, not in git)

- `CLAIM_AUDIT_MATRIX_2026-11-03.csv` — prior 59-claim audit; untracked until today's companion CSV supersedes it in-tree.
- `PROJECT_DEVELOPMENT_TREE_2026-11-03.*`, `PROJECT_DECISION_TREE_2026-11-03.*`, `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` (tracked), `FREEZE.md`, `PROTOCOL.md` — mixed tracked/untracked; see `git status`.
- `.qoder_*` files — reviewer working notes/summaries, untracked, not project records.
- **`failure-concentration-study/` (nested, untracked)** — a near-copy of the study tree corresponding to commit `886a6d5` (2026-10-24, "Clarify construction audit record and add integrity manifest"): 382 files differ from HEAD, 1 file exists only there (`engineered-study/math/results/three_world/stratum_specific_analysis`), 29 root-level audit artifacts absent. **Hazard:** any tool or reviewer reading the working tree may mistake this 2026-10-24 snapshot for the current study. Recommend the owner relocate or delete it after confirming nothing unique is needed (the one extra file should be compared against `0487bf8`/`d2eb7e6` stratum-contrast outputs first).

## 5. Verification chain (what record-keepers can rely on)

| Date | Verifier | Result |
|---|---|---|
| 2026-11-03 | Qoder (prior session) | 59-claim audit matrix; inventory collector hashes |
| 2026-11-04 | GLM; GPT | r3/r4 packages; environment queries; activation-flip proof (§10.3) |
| 2026-11-05 | Qoder (this session) | r5 archive `8f8c259a…`: 940-row manifest verified vs member bytes; 12 patches replayed from original tips reproducing exact commit hashes; exports byte-identical (304/306/317 files); §10.3 counts 4/5/17=26 absent; Environment config verified live (unauthenticated API); checks A/B: live-tip exposure, kit assembly, annex absent repo-wide; run baseline (none queued/active) |
| 2026-11-05 | GPT | independent remote fetch of live sources and both workflow YAMLs |
| 2026-11-05 | Claude | Composio blob checks of live state1/state2/workflow (generation workflow only; recovery and publish-set rely on Qoder scan) |

Designated Claude review of the r5 ZIP was **not** performed; the r5 integrity record rests on GLM's verification plus the Qoder review above.

## 6. What this inventory does not claim

- It does not claim the live repository is contained (it is not — see L19–L21, L24–L26).
- It does not authorize construction, execution, dispatch, or publication of anything.
- It does not resolve the research-objective decision (panel recommendation: Option 2, separate engineered-population study — owner decision in writing pending).
- Hashes abbreviated to 16 hex chars here are recorded in full in the verification artifacts and prior records.
