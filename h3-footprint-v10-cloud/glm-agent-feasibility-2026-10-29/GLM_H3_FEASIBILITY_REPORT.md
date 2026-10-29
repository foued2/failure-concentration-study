# GLM H3 FEASIBILITY REPORT — GLM-Agent Exploratory Footprint Screen

**Date:** 2026-10-29
**Author:** GLM (chat session; research-engineer role per GPT work order "H3 FEASIBILITY RECOVERY")
**Repository:** `foued2/failure-concentration-study`, branch inspected: `gpt/h3-v10-integrity-fix-2026-10-29` at `f9cc893`
**Kind:** Exploratory feasibility screen only. NOT the frozen three-generator H3 gate. NOT held-out evaluation. NOT an H3 scientific result about whether C predicts correctness.

---

## 0. One-paragraph plain-language conclusion

I established that the already-available GLM agent and this sandbox **can** run the full H3 candidate pipeline end to end — independent generation through existing platform access (no paid API, no Copilot, no new credentials), hostile-control-verified isolated execution, and the repository's own trusted scorer unchanged — and that on the prescribed 12-request screen the route produced **one informative natural failure** (k=9, eligible, unsaturated, C=4/9≈0.444) where today's earlier Copilot-Auto screen produced **zero** out of nine unique solvers. What remains blocked: one eligible candidate cannot form a supported cell (m_min=4 per C level), the endpoint-served model (`glm-4-plus`) is not one of the frozen three generators, so even a successful larger run would require a formally documented protocol amendment; and the original 400-batch gate remains frozen and untouched. The single most useful next action: an owner decision on whether to pre-register a bounded GLM-agent generation segment (e.g., one 100-batch-equivalent segment under an amended, pre-frozen design) to test whether the k>0 yield rate (~1/12 here) can supply the variation the Copilot route could not.

---

## 1. Facts established (Step 1)

### 1.1 Current experimental definitions (frozen, v3 harness — unchanged and untouched by this pilot)

Source: `h3-footprint-v3/GATE.md`, `instrument.py`, `expected_values.json`, `FREEZE.json`.

- **Task:** directed single-source/single-target shortest path, non-negative integer edge weights. Candidate interface: `solve(n, edges, s, t)` → integer distance or −1 if unreachable.
- **Instrument:** 30 probes, six families in fixed order R, Z, A, I, S, U, five probes per family. Frozen expected values in `expected_values.json` (hash-verified against `FREEZE.json` during this pilot: 14/14 artifact hashes match).
- **k:** total probe failures for a valid candidate (wrong result, bool, non-integer, exception, or per-probe timeout each count as one failure; invalid candidates receive no k).
- **C (concentration):** max_j f_j / k where f_j is the family failure count; `C = null` when k = 0.
- **Eligible solver:** valid candidate with 2 ≤ k ≤ 24 (at k=1 and k=25..30, C cannot vary for this instrument).
- **Supported cell:** a (base algorithm, k) cell with ≥ 2 C levels, each represented by ≥ m_min = 4 distinct provenance groups.
- **Original go/no-go thresholds (frozen):** PASS = ≥3 supported cells across ≥2 distinct k values with ≥40 unique provenance groups; WEAK = 1–2 supported cells; FAIL = otherwise, or futility checkpoints (fewer than 10/20/30 eligible provenance groups at batches 100/200/300), or eligible saturation rate > 0.80.
- **Frozen generator list (untouched):** `opencode/deepseek-v4.1-flash-free`, `opencode/glm-5.3-flash-free`, `opencode/mimo-v2.6-flash-free`, prompt variants `direct`/`menu`/`simple`, budget up to 400 batches × 8 candidates.

### 1.2 What already exists (not duplicated)

- Frozen v3 instrument, expected values, oracle triple (dijkstra / bellman_ford / brute_force), extraction rules, gate thresholds, futility rule.
- v10 cloud prototype: provider adapters, container executor (`run_container_candidate.py`), supervisor (`isolated_supervisor.py`), trusted child harness (`candidate_child.py`), Copilot-Auto screen (`copilot_auto_pilot.py`) with its published report `observed-results/COPILOT_AUTO_SCREEN_2026-10-29.md`.
- This pilot **reused** `copilot_auto_pilot.py` verbatim (imported, not copied): `prompts()` schedule, `normalize_candidate()` extraction, `classify_base_algorithm()` descriptive classifier, and `run_scoring()` end to end. No scoring logic was rewritten.

### 1.3 Prior screen being extended (the motivation)

The Copilot-Auto screen (12 requests, model `auto`, identity not exposed) yielded 9 unique bodies, all `heap_dijkstra`, all k=0, zero eligible candidates, zero supported cells. Disposition: no eligible failure variation. My pilot asks the same bounded question of the GLM-agent route.

---

## 2. Capability verification (Step 2)

### 2.1 Model identity — recorded honestly

- **This chat session** is GLM, developed by Z.ai. The session runtime does not expose a version string I can independently verify; none is claimed.
- **Generation route:** the `z-ai chat` CLI available in this sandbox. Every one of the 12 candidate responses carried the endpoint-reported model field **`glm-4-plus`** (recorded verbatim per request with usage tokens and completion IDs in `candidate-index.json`).
- **Verification status:** `actual_model_identity_verified = false`. I record what the endpoint declares; I cannot independently attest what serves behind that identifier. This is *more* identity disclosure than the Copilot screen ("not exposed or verified"), but it is still endpoint-reported only.
- **Relationship to the frozen design:** `glm-4-plus` (endpoint-reported) is NOT in the frozen generator list. This pilot therefore cannot be labelled an unchanged V3 run — consistent with the v10 README's rule that any provider substitution requires a formal protocol amendment.

### 2.2 Independent generation calls — verified

12 requests were executed as 12 separate `z-ai chat` processes (one HTTP inference call each), interleaved `direct, menu, simple` × 4, schedule taken **verbatim** from the trusted module's `prompts()`. No request was retried, no provider was switched, no batch was expanded. A pre-pilot "PONG" smoke call (not part of the schedule, not a candidate) verified keyless operation before any candidate request was made.

### 2.3 Safe isolated execution — verified by hostile controls BEFORE candidate execution

Mechanism (full description in `isolation-report.json`): `unshare -r -m -n` (private user+mount+network namespaces) + fresh size-capped tmpfs over `/home/z`, `/root`, `/var/tmp`, `/tmp`, `/dev/shm`, `/run` + minimal **chroot view root** (read-only binds of `/usr`, `/lib`, `/lib64`, `/dev/null`; candidate body at `/candidate`; trusted harness at `/trusted`; **no `/proc`**) + `env -i` (no environment secrets) + RLIMIT_AS 384 MiB / RLIMIT_CPU 8 s / RLIMIT_FSIZE 1 MiB / RLIMIT_NOFILE 32 + per-probe 5.0 s deadline with killpg + session-scoped process-tree leak check + host-side tamper canaries.

| Control | Requirement | Result |
| --- | --- | --- |
| C1 network denial | external connect + DNS must fail | PASS |
| C2 repo/credential invisibility | PROTOCOL.md, `.env`, `/proc` unreachable from inside | PASS |
| C3 write confinement | writes land only in ns tmpfs; host byte-identical after | PASS |
| C4 memory cap | 512 MB allocation must fail under 384 MiB RLIMIT_AS | PASS |
| C5 hostile timeout control | grandchild-spawning, spamming, sleeping solver → status `timeout`, process tree cleaned | PASS |
| C6 control solver | hand-written correct solver → correct answer through full pipeline | PASS |

Host canaries (PROTOCOL.md hash + home listing) unchanged before/after the entire battery. Per GATE.md, the isolation check is recorded **before** any generated candidate was executed.

**Deviations from the container reference (recorded, not hidden):**
1. No Docker in this sandbox; the namespace/tmpfs/chroot/rlimit stack replaces the pinned `python:3.14-slim` container. Execution interpreter: host CPython 3.13.5 (`/usr/bin/python3`), vs the container reference's Python 3.14 and the RepF compute policy's 3.14.0 (that policy governs v0.3-P mathematics, not H3 execution; recorded for transparency).
2. The child runs as mapped-root inside the private user namespace (`newuidmap` unavailable). In-namespace root could in principle attempt umount of overlays or a double-chroot escape; the static forbidden-import filter (`os`, `ctypes`, `subprocess`, …) blocks accepted candidates from attempting it, the view root exposes no `/proc`, and host-side canaries make any successful escape detectable (none occurred). Residual accepted and monitored for this exploratory pilot only.
3. Process-tree leak check is scoped to the child session id rather than container-global PIDs.

---

## 3. The bounded exploratory pilot (Step 3)

Protocol fidelity: identical 12-request schedule, identical prompts (verbatim from `prompts()`), identical extraction and dedup rules (via the trusted module), identical probe inputs (frozen instrument), identical probe timeout policy (5.0 s, fresh process per probe, one call per probe), trusted scorer invoked unchanged. Generation cap 12 (binding, respected); no retries; no provider switching; provenance = request id; dedup by normalized body SHA-256.

### 3.1 Generation outcomes

| Quantity | Result |
| --- | ---: |
| Generation requests attempted | 12 |
| Responses yielding acceptable source code | 12 |
| Exact duplicate responses beyond first occurrence | **0** |
| Unique normalized solver bodies | **12** |
| Invalid candidates (preflight/extraction) | 0 |

All 12 endpoint-reported `glm-4-plus`. Usage tokens and completion IDs recorded per request. For contrast, the Copilot screen had 3 duplicates among 12 responses (9 unique).

### 3.2 Execution outcomes

- Preflight: 12/12 loaded and exposed callable `solve`.
- Probes: 360/360 probe invocations produced protocol-valid prediction records; 0 timeouts, 0 output overflows, 0 process-tree leaks, 0 invalid child outputs. Every candidate received a k (none invalidated).

### 3.3 Scoring outcomes (trusted scorer, unchanged; oracle re-verified independently)

Independent expected-value verification before scoring: `validate_controls.py` **PASS** — 30/30 oracle agreement across dijkstra, bellman-ford, and brute-force implementations; coherence review 30/30; freeze-chain hashes 14/14 match.

| Quantity | Result |
| --- | ---: |
| Valid unique candidates assigned k | 12 |
| k distribution | k=0: 11; k=9: 1 |
| Eligible unique candidates (2 ≤ k ≤ 24) | **1** |
| Same-k, different-C cells observed | 0 |
| Supported cells under m_min = 4 | 0 |
| Cross-C group pairs | 0 |
| Eligible saturation rate | 0.0 |

### 3.4 The informative failure (fingerprint)

`request-03`, prompt variant `simple`, endpoint-reported `glm-4-plus`, body SHA-256 `4075db87413d057c0941d0920501f01b1116dc6f3ee6368e9535032d72463853`, descriptive classifier: `floyd` (source-based classifier, descriptive only).

- k = 9; family counts {A: 4, S: 4, I: 1, R: 0, Z: 0, U: 0}; max_f = 4; **C = 4/9 ≈ 0.4444**; saturated = false; correct probes 21/30.
- Notable descriptive observation (recorded, not acted on): the only failure came from the variant that steers *away* from optimized implementations ("Prefer a straightforward, robust implementation…"), which yielded a Floyd-Warshall solver; all 11 `heap_dijkstra` bodies scored k=0. The failing families A (alternative/parallel routes) and S (shortcuts/dense graphs) are consistent with a Floyd-type implementation defect rather than random noise — but no prompt tuning, no follow-up generation, and no diagnosis beyond this descriptive note was performed, per the cap and the no-tuning rule.

### 3.5 What this pilot does NOT establish

- It does **not** show that the original three-generator gate passes or fails; no original-gate verdict is assigned (field: `NOT_APPLICABLE_TO_12-REQUEST_GLM_AGENT_SCREEN`).
- It does **not** preserve the original frozen experiment: the served generator differs from the frozen generator list, so even a scaled-up GLM-agent run would be a **formally documented design change** (pre-frozen protocol amendment), not "the same study with another model."
- It does **not** support or refute the concentration hypothesis; no held-out evaluation, no predictive model fitting, no effect estimation was performed.
- It does **not** justify exceeding the 12-request cap: generation stopped at exactly 12 requests. The stop-if-no-informative-failures rule did not trigger (one informative failure exists), but the cap binds regardless.

---

## 4. Artifacts (Step 5)

All artifacts are packaged for download in `glm-h3-feasibility-2026-10-29/` with a SHA-256 manifest (`MANIFEST.json`, `MANIFEST.sha256`):

1. `GLM_H3_FEASIBILITY_REPORT.md` — this report.
2. Machine-readable results + provenance: `candidate-index.json` (per-request model fields, usage, hashes, duplicate status), `generation-state.json`, `score-report-final.json` (identity-attributed aggregate), `score-report-RAW-trusted-scorer.json` (untouched trusted-scorer output as evidence).
3. Isolation evidence: `isolation-report.json` (6/6 hostile controls + canaries + mechanism + deviations).
4. Raw responses (`responses/`), normalized bodies (`bodies/`), per-candidate execution reports (`execution-reports/`), `execution-log.json`.
5. Reproduction scripts: `scripts/ns_setup.sh`, `scripts/isolation_check.py`, `scripts/glm_generate.py`, `scripts/local_supervisor.py`, `scripts/score_driver.py`; procedure in `REPRODUCTION.md`.
6. Repository improvement patch: `patch/0001-fix-v03p-a1-gitattributes-BOM.patch` (see §5).

Reproduction requirements: any Linux sandbox with user-namespace support (`unshare -r -m -n`), the `z-ai` CLI, and a clone of the repository at `f9cc893` (or later, without touching frozen branches). Steps: (1) `isolation_check.py` must pass 6/6 first; (2) `glm_generate.py` (12 requests, no retries); (3) `local_supervisor.py`; (4) `score_driver.py`. The scorer and extraction are imported from the repository's own files, so byte-level fidelity to the trusted pipeline is preserved.

---

## 5. Repository improvement patch

`v03p/a1/.gitattributes` (branch `review/a1-package`, introduced at `812c93a`, still present at the inspected tip `f9cc893`) carries a UTF-8 BOM on line 1, causing git to emit `no is not a valid attribute name: v03p/a1/.gitattributes:1` on every checkout. Line 2 (`* -text`) parses and works, so the byte-pinning intent is preserved; the defect is cosmetic but recurring. The patch removes the 3 BOM bytes (100,679-byte RevF and all five A1 manifest hashes are unaffected — the `.gitattributes` file is not one of the five hashed artifacts). Fixed-file SHA-256 would be `381EEB4E239E36B4F19DBF0E2A78D39A0C5898BF58EDCF4A418ED45E31E39EE8` (93 bytes). Test: `patch/test_gitattributes_no_bom.sh` (asserts no BOM and that `git check-attr text` reports `unset` for package files). Changed files: exactly one (`v03p/a1/.gitattributes`). Applying it is an owner/GPT decision; it is supplied as a ready diff, not pushed.

---

## 6. Limitations

1. Single provider route, single endpoint-reported model (`glm-4-plus`), 12 requests — the screen cannot estimate yield rates with useful precision; 1/12 is one observation, not a rate.
2. The isolation stack is a namespace/chroot construction verified by hostile controls, not a pinned container runtime; residual risks are documented in §2.3 and `isolation-report.json` and were acceptable for this exploratory screen only. A frozen amended design should re-evaluate the trust model (as the v10 README itself requires for its hosted path).
3. The `base_algorithm` labels come from the report's source-based descriptive classifier (used verbatim for comparability); they are descriptive, not verified semantics.
4. The endpoint model identity is recorded but not independently verified; if the platform re-routes `z-ai chat` to a different serving stack, this screen's generation results would not be reproducible byte-for-byte (all responses and hashes are preserved).
5. The probe-answer oracle check ran through the repository's own `validate_controls.py` (three independent implementations) on a hash-verified copy; this verifies the reference answers independently of the candidates, but the copy-based execution is itself part of the recorded procedure.

---

## 7. Verdicts

- **Feasibility of the GLM-agent route (this screen): GO-WORTHY-OF-DECISION** — the route works end to end within existing access, produced an eligible natural failure, and the infrastructure (isolation + trusted scoring) held under all hostile controls.
- **The original frozen three-generator gate: UNCHANGED AND UNTOUCHED** — RevF freeze respected; no confirmatory batches; no held-out work; no protocol edits; no thresholds weakened.
- **Next step requiring owner authorization only:** decide whether to pre-register a bounded, amended GLM-agent generation segment with pre-declared thresholds (no retrofitting), or to route the remaining feasibility question through the hosted-executor path once its provider quota question is answered.
