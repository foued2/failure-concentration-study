# LC518 M1-si audit bundle

## Restore on Windows

From this directory, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\BUILD_BUNDLE.ps1
```

The script concatenates the five ASCII Base64 chunks (`m1si_audit_bundle.b64.001` through `m1si_audit_bundle.b64.005`), decodes them, verifies the resulting ZIP SHA-256, and extracts the archive at the repository root.

The archive restores:

- `lc518-150/engineering/m1si_audit.py`
- `lc518-150/engineering/m1si_manifest.schema.json`
- `lc518-150/engineering/README.md`
- `tests/test_lc518_m1si_audit.py`

Then run from the repository root:

```powershell
py -m unittest discover -s tests -v
py .\lc518-150\engineering\m1si_audit.py --help
```

## What it checks

The utility audits an already-produced diagnostic manifest against the M1-si support conditions in population-design v0.21 §3.4. It requires the same exact cell `(q, family, k_fail, k_unresolved)`, computes (C_D) exactly as a rational, and requires each qualifying parent to contribute a pair of distinct runnable variants that jointly differ in realization settings, exact (C_D), semantic-source digest and runnable-artifact digest. At least three qualifying parents must contribute to the same exact cell. Cells are never pooled.

It retains invalid/excluded records in the report. A no-failure record has analytical `C_D = NA` and status `NO_OBSERVED_FAILURES`.

## Scope and limits

This is an engineering utility, not protocol adoption or execution authorization. It audits a manifest that has already been produced under the appropriate upstream authorizations. It does not source or select parents, allocate or generate mutations, inspect/build/execute candidate solvers, run diagnostics, access an oracle/bank, fit the B1 model, or establish scientific validity.

The tool validates digest formatting; it does not independently hash external source trees or runnable artifacts. Upstream provenance and build gates must establish those identities. A passing M1-si support audit establishes only the declared structural support condition, not optimiser convergence, model-fit availability, B1 predictive evidence, population representativeness or causality.

The bundled tests are synthetic software tests only.

## Bundle identity

Complete ZIP SHA-256: `0e5cec8b63bd43dae0a3d8e688b9edf66f17167fbef74be588a884c18e36fc56`.

SHA-256 values of the extracted files:

- `m1si_audit.py`: `7a3a48e826c9695298d9d1cd1f55c400f6fe846418a3c39fffa8b3549fa30a91`
- `m1si_manifest.schema.json`: `1c3b5cade9fc5e0c59d51295cbf2638b65e0057ff33377a00eefe2cac91c2861`
- `README.md`: `029e03c7e8dae982ec65c132471fa326108f6d3b43a115a5a883be99fc529929`
- `test_lc518_m1si_audit.py`: `0c59c7cd1c439bdcd5d731c08410827918875beaf33692e9663fabbd9eec403f`
