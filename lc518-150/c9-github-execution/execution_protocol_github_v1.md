# LC518 C9 GitHub-hosted execution protocol

**Status:** CONFIGURED_LOCKED_NOT_AUTHORIZED
**Machine JSON SHA-256:** 71ecf5e589baba5b25363f9fabd7aee9ab1702da0eb47611464cf162ba170403
**Bank-generation authorization:** FALSE

## Exact runner identity

- runs-on: ubuntu-24.04
- ImageOS: ubuntu24
- ImageVersion: 20261026.354.1
- Python executable: /opt/hostedtoolcache/Python/3.13.5/x64/bin/python3.13
- sys.version: 3.13.5 (main, Jun 12 2025, 03:51:07) [GCC 13.3.0]
- platform.platform(): Linux-7.0.0-1017-azure-x86_64-with-glibc2.39
- interpreter SHA-256: 9cf89c50189de85411dd34b0f0ec5daaab41bf6cd447628572defe3b3ffd0a04
- GITHUB_WORKSPACE: /home/runner/work/failure-concentration-study/failure-concentration-study

The configured launcher checks the complete interpreter fingerprint and both runner-image variables. Any drift is a hard refusal.

## Paths

- RUN_ROOT: /home/runner/work/failure-concentration-study/failure-concentration-study/lc518_run
- OUTPUT_DIR: /home/runner/work/failure-concentration-study/failure-concentration-study/lc518_run/bank
The run root must be absent; its parent must exist. GitHub hosted runners are ephemeral. An authorized job must upload the full run root, stdout, stderr and manifest as a workflow artifact before teardown.

## Locked activation chain

- Review generator: 6e4281b4bfd79783b53d93e132a538dc3d120177405e44012081c6db083c0e2f
- Generator state 1: f73b189d37d60b8601d5db73270fe5d88945aab2c286632f126377e28c92eaff
- Generator state 2 candidate: b4dfdef828374f321d6b21d6f888bc87f926b5b781e26afa4f49bb009ab7de2c
- Launcher state 1: 2f33f9d30a1392908789650b5423c2185c420255c3206a1db2c4944fdef4e941
- Launcher state 2 candidate: 79e5ba358485e9427441df5c44674e5dab700e9dd87f4f129f1590b47ef1c6bd
- Generator diff SHA-256: 2d68be4af48571ac5a0b138e78494149f056dc5a8c149c510b44ea9a722f2f28
- Launcher diff SHA-256: 728042c524b65851356d9d448cf7100c4c187c70995e92593115c9fcd57d6677
- Generator tests: d6a322bc9c28a9c5537f89a1bb6395bf52a44f79293c07b4f526ad985dfcdf64
- Launcher tests: ab8d95124a19bf3fdf9f9b0a87b3f7d1bb4165acdc1b268edb3ca3e9f45aa58d
- Synthetic tests: 52 expected

The workflow verifies both activation diffs and hashes, runs synthetic tests, checks the launcher refusal, and does not invoke the generator or either state-2 file. A separate owner GO naming this JSON digest and both exact diffs is required before bank generation. No solver execution, private annex, predictive fitting, power study, or merge to master is authorized.
