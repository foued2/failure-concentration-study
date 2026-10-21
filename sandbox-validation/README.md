# Windows Sandbox containment validation

This directory is separate from the frozen feasibility pilot and diagnostic calibration. `guest_harmless_tests.ps1` contains only harmless tests; it does not load or generate a solver. `prepare_config.ps1` embeds that script into `restrictive-validation.wsb` so no host folder needs to be mapped into the sandbox.

The configuration disables networking, clipboard, vGPU, audio, video, and printer redirection; enables Protected Client; caps guest memory at 2048 MB; and declares no mapped folders. The guest script tests a bounded child timeout, crash recovery, malformed JSON rejection, guest memory visibility, host-drive read/write attempts through `\\tsclient`, outbound TCP blocking, and guest-local scratch-file operation. Any host write uses a random temporary filename and is immediately removed if it succeeds.

The tests must be run only inside Windows Sandbox. A visible result is required to record pass/fail. Do not run `guest_harmless_tests.ps1` directly on the host. No generated solver code is included or executed.
