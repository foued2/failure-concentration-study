# Python Runner Readiness Check

Status: **BLOCKED**

No model-written solver was generated or executed. This used only harmless hand-built Python fixtures.

| Check | Result | Evidence |
|---|---|---|
| python_runtime_and_current_input | PASS | status=complete, stdout=b'42\r\n' |
| input_isolation | PASS | {"accessible_protected_names": [], "host_project_path_exists": false} |
| guest_forgery_is_untrusted | PASS | guest-created entries=['capture.json', 'forged-extra.json']; host trusted-record store remained host-owned |
| malformed_output_retained_as_raw_untrusted_bytes | PASS | raw=b'\xff\xfe\xfa\n'; host does not parse it as a record |
| oversized_output_capped | PASS | status=overflow; overflow=True; cap=65536 |
| crash_recorded | PASS | status=crash; exit=73 |
| timeout_kills_entire_python_process_tree | PASS | timed_out=True; child_pid=764; tree_terminated=True |
| job_memory_limit_enforced | PASS | status=crash; exit=1; job_limit=128 MiB; attempted=256 MiB |
| guest_sidecar_detected_as_untrusted | FAIL | unexpected guest files=['capture.json', 'forged-extra.json']; only the deliberate harmless forgery is expected |
| readonly_input_mount_unchanged | PASS | Host-side input fixture hashes match after Sandbox exit |

The Sandbox received one current test input, a read-only Python runtime and fixture, and a writable untrusted capture mount. It did not receive the repository, diagnostic battery, evaluation bank, oracle, or host authoritative records. Host-side records were written only after session closure.

This validates the tested configuration and harmless fixtures only. It does not establish resistance to Sandbox escapes or validate a production diagnostic runner.

Generation attempts: **0**. Solver outcomes: **0**.
