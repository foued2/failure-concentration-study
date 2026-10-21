# Windows Sandbox containment check

Date: 2026-10-21 (host local time)

## Configuration

Ran `restrictive-visible-validation.wsb` on Windows 11 Pro build 26300. The `.wsb` disables networking, clipboard redirection, vGPU, audio, video, and printer sharing; enables Protected Client; sets `MemoryInMB` to 2048; and has no `MappedFolders` element. The guest harness was launched by `LogonCommand`. It is a trusted PowerShell test harness and did not load or generate solver code.

## Observed results

| Check | Result | What was observed |
|---|---|---|
| Child crash containment | PASS | Child exited with code 37; harness continued. |
| Malformed output rejection | PASS | Invalid JSON raised a parse error. |
| Bounded timeout and termination | PASS | A 60-second sleeping child exceeded the 2-second supervisor wait and was terminated. |
| Configured memory ceiling visible | PASS | Guest reported 2047 MB; the `.wsb` set 2048 MB. This verifies the guest-visible configured ceiling, not behavior under adversarial memory exhaustion. |
| Host file read blocked | PASS | Read of the host README through `\\tsclient\C\...` failed. This tests that attempted redirection path under this configuration. |
| Host file write blocked | PASS | Write through `\\tsclient\C\...` failed. The unique host marker was absent before closing the Sandbox and remained absent afterward. |
| Outbound network blocked | PASS | A bounded TCP connection attempt to `1.1.1.1:443` did not connect. |
| Guest-local write | PASS | Guest-local temporary file creation succeeded and the test removed it. |

The visible guest window showed **8 PASS, 0 FAIL**. `sandbox-window.png` is the captured Sandbox window containing the displayed results.

## Scope and limitations

These checks validate the tested configuration and harness workflow; they do not prove that all Sandbox escapes are impossible. The memory check observed the configured guest-visible ceiling but did not stress memory exhaustion. The host access checks tested the attempted `tsclient` paths, not every possible host access route. The network check tested one outbound TCP destination. No generated solver code ran, and the natural-solver pilot remains at zero generation attempts and zero solver outcomes. The model-generation interface remains a separate blocker.
