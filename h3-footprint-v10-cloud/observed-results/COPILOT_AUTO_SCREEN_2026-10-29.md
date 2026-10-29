# Copilot-Auto exploratory footprint screen, 2026-10-29

**Disposition: no eligible failure variation observed in this screen.**

This record reports one deliberately small, single-provider exploratory screen. It is not the original frozen three-generator H3 gate, not a held-out evaluation, and not a scientific result about whether failure concentration predicts correctness.

## Reproducible run

- GitHub Actions run: https://github.com/foued2/failure-concentration-study/actions/runs/40850263324
- Final evidence artifact: https://github.com/foued2/failure-concentration-study/actions/runs/40850263324/artifacts/12886084161
- Generation/prediction artifact: https://github.com/foued2/failure-concentration-study/actions/runs/40850263324/artifacts/12886882503
- Commit containing the pilot: `34945bd483ebdfa3f248fd0eb7683188d6adec04`
- Request route: GitHub Copilot CLI through GitHub Actions `GITHUB_TOKEN`; requested model `auto`
- Actual selected model identity: **not exposed or verified**
- Maximum requests: 12; no retries; four requests per each of the `direct`, `menu`, and `simple` prompt variants
- Diagnostic instrument: the existing 30 public directed-SSSP probes in `h3-footprint-v3/instrument.py`, six families of five probes each
- Isolation: generated solver code ran in the networkless candidate container; scoring ran in a separate job with the trusted expected answers

## Observed counts

| Quantity | Result |
| --- | ---: |
| Generation requests attempted | 12 |
| Responses yielding acceptable source code | 12 |
| Unique normalized solver bodies | 9 |
| Exact duplicate responses beyond first occurrence | 3 |
| Unique candidates with all 30 probe answers correct | 9 |
| Unique candidates with (k>0) | 0 |
| Eligible unique candidates, (2 \leq k \leq 24) | 0 |
| Same-(k), different-(C) cells observed | 0 |
| Supported cells under (m_{\min}=4) | 0 |

All nine unique source bodies were classified by the report's source-based descriptive classifier as `heap_dijkstra`. Every one had `k=0` and `C=null`. The three duplicates were:
- request 06 duplicates request 03;
- request 08 duplicates request 01;
- request 09 duplicates request 07.

There were no generation request errors or invalid-source rejections. The failure of this screen to furnish usable (k,C) variation was therefore a *lack of eligible variation*, not an API outage or a source-parsing failure.

## Interpretation and limits

This route, these prompts, and this 12-request screen did not supply the candidate variation required to estimate the planned relationship. It gives a practical reason not to proceed directly to a larger H3 run using this single-provider setup unchanged.

It does **not** establish that naturally generated solvers in general will all pass the instrument, that the original three-generator frame is infeasible, or that (C) has no predictive value. The chosen model behind `auto` was not recorded, and only one provider route was sampled. The original three-generator frame and its acceptance thresholds remain unchanged. No original-gate PASS or FAIL is assigned from this 12-request screen.

## Frozen boundaries respected

- No confirmatory H3 batches were started.
- No held-out evaluation or predictive model fitting was performed.
- No repository README, main branch, or frozen three-generator protocol was changed.
- The raw responses, normalized bodies, execution reports, and aggregate JSON report are preserved in the linked Actions artifacts.
