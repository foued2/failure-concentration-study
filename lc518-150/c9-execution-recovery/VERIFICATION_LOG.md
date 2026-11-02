# LC518 state-package verification log

Configuration freeze date: 2026-11-02 (UTC)
Source of generator bytes: `lc518_generator_scratch_GLM_review_v1.2.zip` (SHA-256 `4a7302072fcdda922cad3e9658056af5209e68ed82e26f6420e52e35dc1036f9`, on repository `master`), whose internal `SHA256SUMS` verified 9/9 OK before any file was used.
No bank, run root, staging directory or oracle output exists. State 2 was never executed.

## Deliverables (this package)

| File | SHA-256 |
|---|---|
| `lc518_generator_state1.py` | `276b9f49f5a3a975c530cc4eca02b0a0f3407ab824d12031f43175a72feb14fe` |
| `lc518_generator_state2.py` | `1335a42d06d64cf7e847981fc68eee07945655128e82e7f08bc43e774d1cb41c` |
| `activation_diff.txt` | `578d17163701d549d17c19e5e1a785709fd1d08bf3572b77ac7058fbc13c8a64` |
| `execution_protocol_v1.md` | `64e7f5033eac5dec3d7278bd48695ffe42b19fc047bd79f14145c49f3a45e293` |

The `execution_protocol_v1.md` digest above is the external protocol SHA-256 that the launcher's `PROTOCOL_SHA256` must pin and that the owner GO must name. It is not contained in the protocol file itself.

## Chain

- Review build `lc518_generator.py` = `6e4281b4bfd79783b53d93e132a538dc3d120177405e44012081c6db083c0e2f` (ZIP pin, re-verified).
- state0 -> state1: exactly one literal changed, `OUTPUT_DIR: str | None = None` -> `OUTPUT_DIR: str | None = "/home/z/lc518_run/bank"`; diff verified programmatically (2 changed diff lines, 1 semantic line).
- state1 -> state2: exactly one literal changed, `BANK_GENERATION_AUTHORIZED = False` -> `True`; packaged `activation_diff.txt` equals `diff -u` of the packaged states byte-for-byte.
- Both states compile under the pinned interpreter (`py_compile`, CPython 3.13.5).

## Verification performed on 2026-11-02 (UTC)

1. ZIP extraction and 9/9 internal checksum verification (recovery introspection run).
2. Artificial acceptance suite rerun under `/usr/bin/python3.13`: **51/51 passed** (`RECOVERY_TEST_RERUN.txt`, 51 `ok` lines, exit 0).
3. Captured target fingerprint: executable `/usr/bin/python3.13`; `sys.version` = `3.13.5 (main, Aug 10 2026, 12:06:59) [GCC 14.2.0]`; `platform.platform()` = `Linux-5.10.134-013.15.kangaroo.al8.x86_64-x86_64-with-glibc2.41`; interpreter binary SHA-256 = `889c603f0d17cb54060951bcf4c4f9b8c9ebd9e52b392c70209bbb9755d797d9`.
4. state1 entry-point refusal check: exit status 1, `REFUSED: separate owner authorization for study-bank generation is absent.`; `/home/z/lc518_run` was not created.
5. state2: bytes hashed only; never executed.

## Open owner actions

1. Ratify `RUN_ROOT = /home/z/lc518_run` (or supply a different absolute path; this regenerates the chain before any GO).
2. Publish the four deliverables and record the protocol digest.
3. Issue the separate bank-generation GO naming the protocol SHA-256 and the activation diff; that GO also enables the launcher authorization literal and applies the §12 launcher pin values.
