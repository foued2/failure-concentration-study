# GPT Bounded Adjudication: GLM §2.5 Review and Phase A Scaffold

**Date:** 2026-11-17  
**Artifact class:** GPT bounded analytical adjudication. Not a population-specification amendment, not a new version, not a freeze record, and not an execution authorization.  
**Branch:** gpt/b1-computational-plan-2026-11-14  
**Parent state before this note:** GLM review archived at commit 60cec67f0e486a84c9eacb1e205f91ba01eb556a.

## 1. Disposition

GLM's bounded review is accepted on its five principal questions, subject to the additional qualifications in §§3–5 below.

The following conclusions stand:

1. The v0.21 design does not bind its new diagnostic stage to the accepted Rev 1.4 specification's uniform eight-by-eight capacity composition. The exact 8-by-8 attainable-C_D result is therefore a conditional candidate, not the operative new-population grid.
2. The M1-si requirement of at least three qualifying parents in one exact cell implies the B1 LOPO training-support conditions in that same cell for every held-out parent with test rows there. No separate anchor-cell LOPO support probability belongs in the support calculation.
3. The joint parent cell-profile event is the correct general event for at least one common M1-si cell. Per-cell marginal probabilities alone are insufficient. A pre-specified anchor cell reduces to a Poisson-binomial tail only under across-parent independence.
4. The attrition chain must preserve dependencies across variants, pairs, cells, and parent sets. Multiplication of unrelated marginal attrition rates is not justified.
5. Earlier project pilot outcome records exist, but no directly applicable estimate of between-parent predictive-loss variation for the new nested-parent estimand has been established. Rev 1.4's DGP catalogue is a scenario framework, not empirical calibration of that variation.

No operating parent count is selected. The confirmatory-versus-exploratory route remains an owner decision. No power calculation, simulation, candidate-frame work, source acquisition, parent selection, solver construction, diagnostic probing, protected-data access, fitting, or execution is authorized or performed.

## 2. Independent source and artifact verification

The branch was re-checked. Its head at the end of this publication step is recorded by the GitHub commit result; master remained 33dca9b61d95b9fb750f750919c32c2e08b2ee90.

The canonical GLM review text was recovered from the verbatim block embedded in the first uploaded transcript. Its exact identity is:

- Git blob SHA-1: 65d2eac2d4a133aec96ace19916f45d9c2fa0144
- SHA-256: 81933f77d9c7a98fefc5abb45d2dbbac01f391f362b7a56c506066397476a9aa
- 111 LF-terminated lines; final newline present.

I committed that canonical text as GLM_S25_ADJUDICATION_REVIEW_2026-11-16.md and re-fetched it from the working branch. The returned Git blob matches GLM's reported blob exactly. The separately uploaded Markdown rendition is not byte-identical: it has 107 LF terminators, no final newline, SHA-256 bdfe98d7f2b5f135e0eac7e3abdb6e56ac1d64531dbcf16b89cbf18f6c2cc58f, and blob 8aab304137d43fdb3889c4972d381080ae5df200. It is not used as the canonical archive.

The source objects previously re-fetched for the adjudication remain the controlling references: v0.21 blob 8af908f6b0ad4cd060194a0a63f4914939f07756, B1 v1.7 blob 8c666e501a31726c728447d155045c0b20adc178, Rev 1.4 Amendment E blob 3728146356a74363a94fe75a87fd06c483954ee2, and its acceptance-record blob 074b40980eb96d164cd8411c8995bb1db4af0d46.

## 3. Capacity lemma: accepted with its feasibility condition explicit

For eight strata with integer per-stratum capacities \(c_s\), \(s=1,\ldots,8\), let:

\[
0\le f_s,\quad 0\le u_s,\quad f_s+u_s\le c_s,
\]
\[
k=\sum_s f_s,\qquad \ell=\sum_s u_s,\qquad m=\max_s f_s.
\]

A cell is feasible only when \(k+\ell\le\sum_s c_s\). For feasible \(k>0\), define:

\[
M_{\min}(k)=\min\left\{t\in\mathbb Z_{\ge0}:
\sum_{s=1}^{8}\min(c_s,t)\ge k\right\},
\qquad
M_{\max}(k)=\min\left(k,\max_s c_s\right).
\]

The attainable values of \(m\) are exactly all integers in
\([M_{\min}(k),M_{\max}(k)]\).

The lower bound follows because a vector whose maximum is at most \(t\) can contain at most \(\sum_s\min(c_s,t)\) failures. The upper bound follows because no stratum can contain more than its capacity or the total \(k\). For attainability, take any integer \(m\) in the interval. There is a stratum with capacity at least \(m\); assign \(m\) failures there. Since \(m\ge M_{\min}\), the remaining strata have enough capacity, each capped at \(m\), to distribute the remaining \(k-m\) failures without exceeding \(m\). The total residual capacity is \(\sum_s c_s-k\), which is at least \(\ell\), so the unresolved counts can then be placed in the residual slots. Thus every intermediate maximum is attainable.

For \(c_s=8\) in all eight strata, this reduces to the Rev 1.4 Amendment E §3.2 result:
\[
m\in\{\lceil k/8\rceil,\ldots,\min(k,8)\},
\qquad k+\ell\le64.
\]
With only eight nonnegative integer strata and no bound on their capacities, the outer range is \(\{\lceil k/8\rceil,\ldots,k\}\). Distinct \(C_D=m/k\) values on a fixed-\(k\) cell are separated by at least \(1/k\).

GLM's conditional treatment is correct. The unresolved task is the owner-authorized instrument decision that binds the new diagnostic stage to a fixed capacity vector and freezes it. Neither acceptance of Rev 1.4 nor the unrelated root-level specs/instrument_spec.json draft supplies that missing link.

## 4. M1-si to LOPO implication: accepted

Let \(Q_{g,c}=1\) when parent \(g\) satisfies the full M1-si contribution rule in cell \(c\), including at least two unique valid variants, distinct realization settings, distinct realized \(C_D\) values, and the required source/runnable-artifact distinctness.

If at least three parents satisfy \(Q_{g,c}=1\) in the same cell, then holding out any one parent with test rows in that cell leaves at least two qualifying parents in training. Each remaining qualifying parent contributes at least two distinct \(C_D\) values. Therefore the training set has at least two distinct parents, at least two distinct \(C_D\) values, and \(W_{C,c,-h}^{\mathrm{train}}>0\).

This is a deterministic implication of M1-si, not an extra stochastic attrition stage. It guarantees design-side fold support in that cell only. It does not guarantee outcome discordance, that every selected parent has test rows in that cell, score coverage, or fit availability. Other B1-eligible cells can still fail fold support.

## 5. Remaining qualifications to GLM's scaffold

### 5.1 Joint cell-profile law: the general event is correct; the proposed reduction needs one more joint layer

The event
\[
E_{\mathrm{M1-si}}=
\left\{\max_{c\in\mathcal C}\sum_{g=1}^{P}\mathbf1(c\in\mathcal Q_g)\ge3\right\}
\]
is correct, where \(\mathcal Q_g\) is the complete set of cells in which parent \(g\) qualifies.

The probability form using \(\pi_g(A)=\Pr(\mathcal Q_g=A)\) is also correct. Across-parent independence licenses the product of parent profile laws; otherwise the joint law of \((\mathcal Q_1,\ldots,\mathcal Q_P)\) is required. For a genuinely pre-specified single anchor cell \(c^*\), the event reduces to at least three successes among the parent-specific indicators; this is Poisson-binomial only if those indicators are independent across parents.

One part of GLM's proposed simplification is not yet sufficient as stated. A parent-specific cell-allocation model plus one scalar pair-distinctness probability per cell can supply marginal \(\Pr(Q_{g,c}=1)\), but it does not generally supply the joint law of \((Q_{g,c})_{c\in\mathcal C}\). The finite variant budget, shared realization schedule, and diagnostic outcomes can make qualification events dependent across cells. To derive \(\pi_g(A)\), the model must specify either:

- the full joint conditional law of all cell-qualification indicators given the parent's complete variant-to-cell allocation; or
- an explicit conditional-independence factorization across cells, with a substantive justification and sensitivity to departures from it.

A multinomial cell-allocation assumption alone does not resolve this second layer. The scaffold should therefore retain the joint-profile law as primary and mark any factorization as an additional assumption, not as a consequence of the multinomial allocation step.

### 5.2 Attrition tiers: correct dependence principle, refine the unit of digest distinctness

The three-tier structure is useful, but semantic-source and runnable-artifact uniqueness is relational. A digest is produced per variant, while the decision that two variants are distinct requires comparison within a parent's candidate set or across a proposed pair. Accordingly, record digest production at the per-variant tier, but put duplicate canonicalization and the distinct-digest test at the pair/set tier alongside the exact-cell match, distinct realization settings, and distinct \(C_D\) requirement.

Also distinguish the time at which uncertainty is represented. Before diagnostics, operating-characteristic models may assign probabilities to fold support in non-anchor cells. After the diagnostic table is realized, each LOPO design-support audit is deterministic. Fit availability remains the assignment-level event specified in B1 v1.7 §5.7 V5; it is not a per-variant attrition percentage.

### 5.3 Count-selection rule: floor, sequence, and precision caveat

The M1-si support floor \(P\ge3\) is already imposed by the design rule, conditional on the B1 amendment retaining the proposed operator-class \(q\) coding. It is not an additional free threshold for the owner to choose. The owner decision concerns the confirmatory-versus-exploratory route and, if confirmatory, the prospective precision objective or practically relevant gain.

The template \(P_{\mathrm{op}}=\min\{P:\mathrm{criterion}(P)\text{ is met}\}\) is usable only after the candidate-frame and selection procedure define a comparable parent roster or nested selection sequence for each candidate \(P\). Otherwise each \(P\) could correspond to a different, selectively chosen parent composition and the comparison would be ill-defined or vulnerable to count selection on anticipated support.

Any precision criterion must also be expressly conditional on sufficient outcome-side variation. The design can guarantee some support and estimability conditions; it cannot guarantee outcome discordance or a non-degenerate predictive-loss difference. The B1 conditional randomization test remains conditional on the observed parents and does not create a parent-superpopulation inference merely because \(P\) is varied in an operating-characteristic scenario.

## 6. Accepted Phase A scaffold and boundaries

GLM's S1–S8 is accepted as a symbolic scaffold, with the qualifications above. It is not yet a numerical count justification. Its valid contents are:

- conditional estimand and fold-scope placeholders;
- general capacity-vector envelope and conditional 8-by-8 candidate;
- joint parent cell-profile event;
- deterministic M1-si-to-LOPO implication in the anchor cell;
- dependent, tiered attrition/coverage/availability structure;
- proxy-pathway sensitivity distinct from N5;
- a count-selection template with the route and criterion left open;
- sequencing and non-authorization conditions.

The following remain open: B1 amendment and \(q\)-coding; diagnostic-composition binding and freeze; owner route decision and precision criterion; candidate frame and parent inventory; any admissible evidence or elicitation basis for quantitative scenario assumptions; computational-plan validation; custodian, consent, trigger-(i), isolation, and separate execution GO.

No quantitative parameter is filled by this note. No numerical probability evaluation, power calculation, or simulation is performed.

## 7. Final disposition

- GPT adjudication note 60c2ae5e: **ACCEPTED**.
- GLM bounded review and symbolic scaffold: **ACCEPTED WITH THE QUALIFICATIONS IN §5**.
- Canonical GLM review archived byte-identically; the reformatted upload is not substituted for it.
- Population specification v0.21: unchanged. No v0.22 proposed.
- Operating parent count and confirmatory/exploratory route: open.
- Master: untouched.
- All source acquisition, parent selection, mutation allocation, solver construction/execution, diagnostics, outcomes, fitting, sampling, and simulation remain unauthorized.

The next substantive step is to settle the diagnostic-composition binding and the owner's route decision. Until then, keep Phase A symbolic and do not turn the scaffold into a numerical parent-count recommendation.
