# Expression pilot report

State: **REPEATED_K_BUT_NO_C_SEPARATION**

Run: `expression-pilot-gemini-20261022T163536Z`.
Generation requests: 30/30.
Model-written generation outputs: 27; generation failures: 3.
Distinct canonical bodies: 21.
Eligible executed bodies: 19.
Feasibility demonstrated: false.

Missing condition(s): REPEATED_K_BUT_NO_C_SEPARATION

## Bodies

| Attempt | Body | k | C | Evaluation correct | Eligible |
| --- | --- | ---: | ---: | ---: | --- |
| attempt-0002 | `c80287fe075d` | 30 | 0.167 | 0/30 | True |
| attempt-0003 | `5c3c14c19b83` | 0 | 0.000 | 30/30 | True |
| attempt-0004 | `433b73584024` | 2 | 1.000 | 28/30 | True |
| attempt-0006 | `9ff39e024cf6` | 2 | 1.000 | 28/30 | True |
| attempt-0007 | `0393483b6fad` | 2 | 1.000 | 28/30 | True |
| attempt-0008 | `0d9fb91e23d8` | 0 | 0.000 | 30/30 | True |
| attempt-0009 | `b8024a66c595` | 30 | 0.167 | 0/30 | True |
| attempt-0011 | `5cecbd1e100d` | 2 | 1.000 | 28/30 | True |
| attempt-0012 | `ba8bad3d20c3` | 2 | 1.000 | 28/30 | True |
| attempt-0013 | `a974e6703094` | 2 | 1.000 | 28/30 | True |
| attempt-0015 | `f1f6a1e7e29c` | 30 | 0.167 | 0/30 | True |
| attempt-0017 | `5cd26bb56c06` | 0 | 0.000 | 30/30 | True |
| attempt-0018 | `f57ad1c8bcc8` | 0 | 0.000 | 30/30 | True |
| attempt-0020 | `41753a30d479` | 2 | 1.000 | 28/30 | True |
| attempt-0021 | `f0a0d8aa310e` | 0 | 0.000 | 30/30 | True |
| attempt-0022 | `f4f1ab638ff6` | 7 | 0.714 | 23/30 | True |
| attempt-0025 | `b0abb598e272` | 2 | 1.000 | 28/30 | True |
| attempt-0026 | `1873a80b916c` | 2 | 1.000 | 28/30 | True |
| attempt-0030 | `798619031081` | 0 | 0.000 | 30/30 | True |

## Fixed-k contrasts

- k=2: C=[1.0]; bodies/C={'1.0': 9}; cross-C evaluation contrast=False.
- k=30: C=[0.16666666666666666]; bodies/C={'0.16666666666666666': 3}; cross-C evaluation contrast=False.

No predictive model was fitted and no concentration effect was tested.

The guest could read the other expressions in its current suite. Expected values, family labels, oracle code, and host records were not in the guest payload. Source screening is a best-effort policy, not a security boundary.

This is an exploratory feasibility check on one declared generator procedure and task; it is not a confirmatory or prevalence claim.
