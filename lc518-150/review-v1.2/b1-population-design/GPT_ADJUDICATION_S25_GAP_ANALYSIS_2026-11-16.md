# GPT Independent Adjudication: §2.5 Operating-Parent-Count Gap Analysis

**Date:** 2026-11-16  
**Artifact class:** GPT analytical adjudication and symbolic-design note  
**Status:** Design-only working note. Not a population-specification amendment, not a new version, not a freeze record, and not an execution authorization.  
**Repository branch:** gpt/b1-computational-plan-2026-11-14  
**Parent commit checked before publication:** fed3398735dd70608ee5e8a942ed0c26ea8c6673  
**Master observed before publication:** 33dca9b61d95b9fb750f750919c32c2e08b2ee90

## 1. Decision

GLM's fourteen-gap inventory is a useful starting map. I accept its central diagnosis: the support floor P >= 3 is not an operating-parent-count justification, and no confirmatory operating count can be inferred from the current record.

I do **not** accept the inventory without qualification. The following corrections are material:

1. The per-stratum capacity is not simply an unknown numeric input. The accepted Rev 1.4 Amendment E contains an exact 8-strata-by-8-slots capacity construction and the closed-form attainable-C_D envelope. Its applicability and freeze status must be bound explicitly to the new population design before it is called the operative frozen instrument.
2. The M1-si requirement itself guarantees the LOPO design-support conditions for its qualifying common cell. A separate probability of LOPO support failure must not be attached to that same cell. LOPO exclusions remain possible in other B1-eligible cells, and score coverage and fit availability remain separate.
3. The probability of obtaining at least one qualifying cell cannot in general be calculated from independent per-cell marginal probabilities. A parent can qualify for several cells, and the events are dependent within parent. The symbolic machinery must preserve each parent's joint cell-qualification profile.
4. Attrition stages are dependent. Multiplying marginal attrition percentages as though validity, digest distinctness, cell matching, C_D variation, fold support, score coverage, and fit availability were independent would be unjustified.
5. The statement that no pilot outcomes exist is too broad. Earlier pilot evidence exists in the project history, but it does not provide a transportable estimate of between-parent predictive-loss variation for this new nested-parent estimand. The precise statement is that no directly applicable pilot estimate has been identified.
6. The supplied GLM artifact has provenance inconsistencies. Its body is still reviewable as text, but its reported date and reported byte identity are not authenticated by the uploaded copy.

No parent count is selected. No confirmatory/exploratory route is selected on the owner's behalf. No simulation, power calculation, outcome access, source acquisition, parent selection, solver construction, or diagnostic execution is authorized or performed.

## 2. Repository and source checks

The following objects were re-fetched from the working branch:

- Population and Experimental Design v0.21, blob 8af908f6b0ad4cd060194a0a63f4914939f07756.
- B1 Analysis Plan v1.7, blob 8c666e501a31726c728447d155045c0b20adc178.
- Rev 1.4 Amendment E, blob 3728146356a74363a94fe75a87fd06c483954ee2.
- GPT acceptance record for Rev 1.4 Amendment E, blob 074b40980eb96d164cd8411c8995bb1db4af0d46.
- The branch tip was fed3398735dd70608ee5e8a942ed0c26ea8c6673; master was 33dca9b61d95b9fb750f750919c32c2e08b2ee90 at the time checked.

The v0.21 §0.1 expressly identifies Rev 1.4 Amendment E as the controlling symbolic B1/M1 feasibility specification and distinguishes its acceptance from a separate formal freeze. The acceptance record says it is accepted for the symbolic B1/M1 specification, not that it is frozen as the final diagnostic instrument.

The root-level specs/instrument_spec.json is a different artifact: it is labelled DRAFT_v2 and describes six families with five probes per family, thirty probes per instance. It must not be silently treated as the eight-stratum, 8-by-8 diagnostic composition in Rev 1.4. Its relationship to the new LC518 instrument needs an explicit scope label if anyone proposes to use it.

## 3. Corrected capacity result: conditional, not UNKNOWN

Rev 1.4 Amendment E §3.2 states the 8-by-8 design. For each of the eight diagnostic strata s, let f_s be the definite-failure count and u_s the unresolved count. The design capacity is:

\[
0 \le f_s,\quad 0 \le u_s,\quad f_s+u_s \le 8,
\qquad s=1,\ldots,8.
\]

Let:

\[
k=\sum_{s=1}^{8} f_s,\qquad
\ell=\sum_{s=1}^{8} u_s,\qquad
m=\max_s f_s,\qquad C_D=m/k \quad (k\ge1).
\]

For every feasible pair k >= 1, ell >= 0 with k+ell <= 64, Rev 1.4 §3.2 proves the exact cell envelope:

\[
\mathcal M(k,\ell)
=
\left\{\lceil k/8\rceil,\ldots,\min(k,8)\right\},
\qquad
C_D\in\{m/k:m\in\mathcal M(k,\ell)\}.
\]

The construction proves that every integer m in this interval is attainable under the 8-by-8 capacity constraints; it is not merely a loose upper/lower bound. In particular, for k=2, the only values are C_D in {1/2, 1}. For k>8, the maximum numerator is 8, not k.

This corrects the way GLM framed S25-GAP-8. A numeric capacity basis exists in the accepted symbolic specification. What remains unresolved is whether the new population's diagnostic composition is formally bound to this same 8-by-8 design and whether the relevant instrument/profile is frozen. Therefore:

- Do not record all per-stratum capacities as UNKNOWN.
- Do not call the 8-by-8 design formally frozen solely because Rev 1.4 was accepted.
- Record the capacity table as **8 per stratum, conditional on Rev 1.4's 8-by-8 composition governing the new population**.
- Close the remaining applicability/freeze question against the authoritative instrument or diagnostic-composition record.
- Once applicability is confirmed, import the exact envelope above into the §2.5 annex. No simulation is needed for this arithmetic.

This is a correction to the GAP-8 classification, not a claim that a different or newer instrument has been discovered.

## 4. M1-si implies LOPO design support in its anchor cell

For a parent g and exact cell c, define:

\[
S_{g,c}=\{C_D(v):v\in\mathcal V_{g,c}\}.
\]

Let Q_{g,c}=1 when parent g satisfies the full M1-si contribution rule in cell c: at least two unique valid variants, at least two distinct predeclared realization settings, at least two distinct realized C_D values, and the required distinct semantic-source and runnable-artifact digests.

If at least three parents satisfy Q_{g,c}=1 in the same cell, then every one of those parents has |S_{g,c}| >= 2. Consider any selected parent h as the held-out parent:

- If h is one of the qualifying parents, at least two other qualifying parents remain in training.
- If h is not one of the qualifying parents, all three or more qualifying parents remain in training.

Consequently, for every held-out parent h whose fold has test rows in this cell:

\[
G_{c,-h}^{\mathrm{train}}\ge2,\qquad
D_{c,-h}^{\mathrm{train}}\ge2,\qquad
W_{C,c,-h}^{\mathrm{train}}>0.
\]

The last inequality follows because the training set contains at least two distinct exact C_D values. This is a deterministic implication of §3.4, not an additional probability assumption.

Therefore, for the M1-si qualifying anchor cell, LOPO design-support failure is not an independent attrition stage once M1-si success has been established. Do not count it again or multiply a separate fold-survival probability into the anchor-cell support probability.

This does **not** guarantee that every selected parent has test rows in the anchor cell, that every parent is part of the scored-parent set, that every other B1-eligible cell is fold-estimable, or that any model fit will be available. Those are separate coverage and availability questions. Other B1-eligible cells that do not satisfy M1-si can still fail the fold-level design conditions in §3.2.

## 5. Symbolic support event: retain joint cell profiles

Let \(\mathcal C\) be the finite set of exact cells c=(q,Z,k,ell) that the eventual design can produce. For each parent g, define its set of M1-si qualifying cells:

\[
\mathcal Q_g=\{c\in\mathcal C:Q_{g,c}=1\}.
\]

The event that the study obtains at least one M1-si qualifying cell is:

\[
E_{\mathrm{M1-si}}
=
\left\{
\max_{c\in\mathcal C}
\sum_{g=1}^{P}\mathbf 1(c\in\mathcal Q_g)
\ge3
\right\}.
\]

A general symbolic probability requires the joint distribution of each parent's complete cell profile. Let \(\pi_g(A)=\Pr(\mathcal Q_g=A)\) for A a subset of \(\mathcal C\). If, and only if, parent profiles are assumed independent for the operating-characteristic calculation:

\[
\Pr(E_{\mathrm{M1-si}})
=
\sum_{A_1,\ldots,A_P\subseteq\mathcal C}
\left[\prod_{g=1}^{P}\pi_g(A_g)\right]
\mathbf 1\left\{
\max_{c\in\mathcal C}
\sum_{g=1}^{P}\mathbf 1(c\in A_g)\ge3
\right\}.
\]

If parent profiles are dependent, the product is replaced by the declared joint distribution of (Q_1,...,Q_P). If the selected parent frame and all design inputs are fixed, the incidence audit is deterministic; a probability should not be invented merely to make it look stochastic.

Per-cell marginal probabilities p_{g,c}=Pr(Q_{g,c}=1) are insufficient by themselves to calculate the probability of at least one common qualifying cell, because qualification events across cells can be dependent within parent. A calculation such as one minus the product of per-cell failure probabilities would require an additional independence assumption and is not licensed by the current design.

The probability model must also distinguish uncertainty over diagnostic realization for a fixed, selected parent set from any hypothetical sampling model over parent implementations. The accepted B1 v1.7 test is conditional on the observed parents; this count justification must not smuggle in a parent-superpopulation claim.

## 6. Attrition and fold accounting must preserve dependence

The attrition chain in v0.21 §2.5 and §6.5 is a useful reporting taxonomy:

planned -> valid -> unique semantic/runnable variant -> realized distinct C_D -> same exact cell -> fold-estimable -> scored -> fit-available.

It is not a declaration that the stages are independent. Several transitions are structurally linked:

- Invalidity and duplicate identity reduce the number of variants available to form a within-parent pair.
- Cell matching depends jointly on q, Z, k, and ell.
- Distinct C_D depends on the same diagnostic vectors that determine k and ell.
- M1-si requires distinct realization settings and distinct realized C_D in the same cell.
- Fold support depends on the complete cross-parent pattern of cell membership and C_D values.
- Score coverage and fit availability depend on the new protected-set definition and the B1 computational/availability rules.

The scenario table should therefore use conditional transition probabilities or a joint parent-profile model. Multiplying unrelated marginal attrition percentages is not acceptable unless independence is explicitly defended. All values remain UNKNOWN until supported by an admissible source or separately authorized evaluation.

## 7. Gap-by-gap adjudication

| GLM gap | GPT disposition | Correction or qualification |
|---|---|---|
| S25-GAP-1: intended scored-fold set | Retain | Define selected P, intended fold set, scored-parent set, unscored-fold accounting, and estimand scope separately. Do not assume all P parents yield scored test rows. |
| S25-GAP-2: new protected-set estimand binding | Retain | Blocked on the separate B1 amendment. |
| S25-GAP-3: confirmatory or exploratory route | Retain; owner decision | This is a substantive owner choice. No precision threshold or practically relevant gain may be invented by GPT or GLM. |
| S25-GAP-4: variation model | Retain; sharpen | Define the parent-level predictive-loss-difference quantity, its between-parent variation, within-parent variant dependence, and any family structure separately. A conditional B1 estimand does not itself supply these operating-characteristic assumptions. |
| S25-GAP-5: evidence/elicitation basis | Retain; correct wording | Do not say no pilot outcomes exist without qualification. Earlier project pilots exist, but no directly applicable estimate for this new nested-parent loss-variation target has been established. The Rev 1.4 DGP is a scenario framework, not empirical calibration of solver-population variances. |
| S25-GAP-6: realization-setting counts | Retain | Requires the authorized candidate-frame and Stage 2 inventories. |
| S25-GAP-7: same-cell M1-si probability | Retain; strengthen | Define the joint per-parent cell-qualification profile. Marginal cell probabilities alone do not determine the probability of any common qualifying cell. |
| S25-GAP-8: per-stratum capacities | Reclassify | The accepted Rev 1.4 §3.2 contains 8 slots in each of 8 strata and an exact attainable-C_D envelope. Remaining gap: applicability and formal freeze/binding of that 8-by-8 composition for the new population. |
| S25-GAP-9: attrition rates | Retain; strengthen | Values are UNKNOWN, and stages must not be treated as independent without evidence. |
| S25-GAP-10: support combinatorics | Retain; correct structure | Use the joint-profile event in §5. No separate LOPO design-support probability for the M1-si anchor cell: that support is implied by M1-si. Other eligible cells, coverage and fit availability remain distinct. |
| S25-GAP-11: proxy-pathway sensitivity | Retain | Count-level sensitivity is distinct from the B1 amendment's N5 operating-characteristic control. Numeric evaluation remains gated. |
| S25-GAP-12: selection and ratification | Retain | The selection rule and binding/approval artifact depend on the route decision and must precede protected outcomes. |
| S25-GAP-13: candidate frame | Retain; gated | No source acquisition, candidate inventory, parent selection or lineage work without separate owner authorization. |
| S25-GAP-14: sequencing | Retain | Resolve q-coding in the B1 amendment before relying on M1-si; validate any computational precision machinery before citing it; bind the operating count before protected outcomes exist. |

## 8. Phase A work that can proceed now

The authorization-free Phase A deliverable should be a **symbolic §2.5 scaffold**, not a numerical operating-count recommendation and not a new population-specification version. It should contain:

1. A conditional estimand/fold-scope statement with separate symbols for selected parents P and scored parents P_score.
2. The Rev 1.4 8-by-8 capacity table and exact attainable-C_D envelope, visibly conditional on the instrument-applicability/freeze check.
3. The per-parent joint cell-profile support event in §5.
4. The deterministic implication from M1-si support to LOPO support in its anchor cell.
5. A dependent attrition/coverage/availability scenario-table structure with every unfilled rate marked UNKNOWN.
6. A proxy-pathway sensitivity structure, clearly separate from N5.
7. A count-selection-rule template whose precision or practical-gain criterion remains blank until the owner makes the confirmatory/exploratory route decision.
8. The sequencing and authorization conditions in §§2.5, 7, 8 and 9 of v0.21.

The route decision can proceed in parallel, but numeric assumptions, scenario evaluation, power calculations and simulation remain gated. If the owner chooses the exploratory route, the count must not be advertised as power-backed or precision-justified.

## 9. Questions for GLM's independent check

Please review the technical corrections rather than produce another population-specification version:

1. Does Rev 1.4 §3.2's exact 8-by-8 capacity construction apply to the diagnostic composition intended by v0.21 §3.2? Identify the exact instrument/freeze artifact or state that the binding link is absent.
2. Is the proof in §4 correct that M1-si success in one exact cell guarantees the B1 LOPO training-support conditions for every held-out parent with test rows in that cell?
3. Is the joint cell-profile expression in §5 the right general symbolic event, and what assumptions would be needed to simplify it?
4. Does the attrition structure in §6 preserve all material dependencies without double-counting M1-si/LOPO support?
5. Is the qualification of the prior-pilot and Rev 1.4 DGP evidence accurate?

A response should be a bounded analytical review of this note, not a new version of the population specification. No repository write or restricted research activity is requested from GLM.

## 10. Provenance qualifications on the supplied GLM handoff

The uploaded GLM handoff body says its date and assigning GPT instruction date are 2026-11-17. The current date when this adjudication is made is 2026-11-16. That date cannot be accepted as a completed event date on the current record; it is a future-date inconsistency requiring correction or explanation.

The uploaded file Pasted markdown (2).md is 27,396 bytes, has 199 LF line terminators, does not end in a newline, and has SHA-256 3b26c34eaff72259d7a73dcfc62ac2d3b0497eea0e49ec6bfb2450fea1480539. Its Git blob SHA-1 is f628c1689c73f6c4669129d843c8fb86f53cf6fa. These do not match the GLM-transcript-reported artifact dimensions (186 newline-terminated lines) or reported hashes (SHA-256 9cab6697a88879540353513bac2e922dcd8e3d38ded7f67074d0d9d86f43682f; Git blob SHA-1 848aa0df5fd2f9795dc77bd1d8ef5953ee4083d2). The uploaded copy is therefore reviewed as supplied text, but it is not byte-verified as the artifact whose hash GLM reported.

This discrepancy does not by itself disprove the analysis content. It does mean the reported artifact hash, dimensions, date, and local working-tree status must not be repeated as verified facts about the uploaded copy.

## 11. Final disposition

- GLM's overall gap map: **accepted with material corrections**.
- Corrected GAP-8: exact 8-by-8 capacity arithmetic exists in accepted Rev 1.4; applicability/freeze remains to be bound.
- Corrected GAP-10: joint parent cell profiles; M1-si implies LOPO design support in the anchor cell.
- Numerical assumptions and operating P: **OPEN**.
- Confirmatory/exploratory route: **OWNER DECISION OPEN**.
- Candidate-frame work, simulations, diagnostics, solver work, outcomes and fitting: **NOT AUTHORIZED**.
- Population specification v0.21: **unchanged**. No v0.22 is proposed or created by this note.
- Master: **untouched**.

The next useful review is GLM's independent challenge of this adjudication, followed by completion of the symbolic Phase A scaffold. The aim is to close the mathematical design gaps, not to restart the editorial version cycle.
