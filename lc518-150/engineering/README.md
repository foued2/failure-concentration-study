# LC518 M1-si audit bundle

This branch carries the tested M1-si audit utility as a reproducible ZIP bundle split into two binary parts to fit the repository upload interface.

## Rebuild on Windows

From this directory, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\BUILD_BUNDLE.ps1
```

The script joins `m1si_audit_bundle.part1` and `m1si_audit_bundle.part2`, verifies the resulting ZIP SHA-256, and extracts the archive at the repository root. It restores:

- `lc518-150/engineering/m1si_audit.py`
- `lc518-150/engineering/m1si_manifest.schema.json`
- `lc518-150/engineering/README.md`
- `tests/test_lc518_m1si_audit.py`

Then run from the repository root:

```powershell
py -m unittest discover -s tests -v
py .\lc518-150\engineering\m1si_audit.py --help
```

## Scope

The utility audits an already-produced diagnostic manifest against the adopted M1-si support conditions in population-design v0.21 §3.4. It does not source or select parents, allocate or generate mutations, inspect/build/execute candidate solvers, run diagnostics, access an oracle/bank, or fit the B1 model. It is not an execution authorization and has not been adopted as a governing project instrument.

The digest fields are format-checked; the utility does not independently hash external source trees or runnable artifacts. The upstream provenance and build gates must establish those identities.

Synthetic software tests are included in the bundle. A passing synthetic test suite establishes only the tested software behavior, not scientific validity or evidence about the LC518 population.

## Bundle identity

SHA-256 of the complete ZIP: `0e5cec8b63bd43dae0a3d8e688b9edf66f17167fbef74be588a884c18e36fc56`

SHA-256 values of files inside the bundle:

- `m1si_audit.py`: `7a3a48e826c9695298d9d1cd1f55c400f6fe846418a3c39fffa8b3549fa30a91`
- `m1si_manifest.schema.json`: `1c3b5cade9fc5e0c59d51295cbf2638b65e0057ff33377a00eefe2cac91c2861`
- `README.md`: `029e03c7e8dae982ec65c132471fa326108f6d3b43a115a5a883be99fc529929`
- `test_lc518_m1si_audit.py`: `0c59c7cd1c439bdcd5d731c08410827918875beaf33692e9663fabbd9eec403f`
