# Sandbox integration calibration

Controlled software fixtures only. No model-generated solver ran.

Cases passed: 11/11

| Case | Result | Details |
| --- | --- | --- |
| fixture_normal | PASS | supervisor recorded complete; tree_terminated=true |
| pattern_zero | PASS | host validation and expected behavior matched; family counts=[0, 0, 0, 0, 0, 0]; k=0; C=0.0 |
| pattern_one_family | PASS | host validation and expected behavior matched; family counts=[4, 0, 0, 0, 0, 0]; k=4; C=1.0 |
| pattern_two_families | PASS | host validation and expected behavior matched; family counts=[2, 2, 0, 0, 0, 0]; k=4; C=0.5 |
| pattern_four_families | PASS | host validation and expected behavior matched; family counts=[1, 1, 1, 1, 0, 0]; k=4; C=0.25 |
| fixture_timeout_tree | PASS | supervisor recorded timeout; tree_terminated=true |
| fixture_crash | PASS | supervisor recorded crash; tree_terminated=true |
| fixture_malformed | PASS | unsafe stdout rejected: worker output is not one strict integer |
| fixture_oversized | PASS | unsafe stdout rejected: bounded stdout limit exceeded |
| fixture_forged_claims | PASS | unsafe stdout rejected: worker output is not one strict integer |
| fixture_unexpected_sidecar | PASS | unsafe output rejected: unexpected or missing output file |

Scope limits: this used a hand-built PowerShell control worker, not a generic Python solver adapter. The worker receives one probe over stdin but can also read the mapped diagnostic battery; input isolation for model-written solver code is therefore NOT VERIFIED. The pilot is not ready to execute generated solvers. The tested capture path does not claim resistance to Sandbox escape.
