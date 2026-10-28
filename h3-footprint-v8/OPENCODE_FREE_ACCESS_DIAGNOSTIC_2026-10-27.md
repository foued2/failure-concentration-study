# OpenCode free-model access diagnostic (no model calls)

**Date:** 2026-10-27  
**Purpose:** Determine whether the frozen model IDs are absent from the local catalog, hidden by configuration, or visible but blocked at request time.  
**Safety:** These commands query local metadata and the model catalog only. They do not run `opencode run`, call a model for generation, or create study candidates.  
**Amended:** 2026-10-28, to add permission-profile and free-tier compatibility checks.

## Why this check is warranted

The current [OpenCode Console model page](https://dev.opencode.ai/v2/docs/console/models/) still lists all three IDs frozen in the H3 footprint generation schedule: `glm-5.3-flash-free`, `deepseek-v4.1-flash-free`, and `mimo-v2.6-flash-free`. The [Models guide](https://dev.opencode.ai/v2/docs/models/) says catalog availability depends on whether a model is enabled and its provider is available in the current project. It documents `OPENCODE_DISABLE_FREE_MODELS=1` as a way to hide free models. The [October 21, 2026 changelog](https://opencode.ai/changelog) describes explicit feedback when free-message limits are exhausted. Public catalog presence does not establish account-level availability.

## Step 1: identify the executable actually under test

Run in PowerShell without starting a generation job:

```powershell
$op = Join-Path $env:LOCALAPPDATA 'JetBrains\PyCharm2026.2\acp-agents\opencode\1.19.4\opencode.exe'
"Executable exists: $(Test-Path $op)"
if (Test-Path $op) {
    (Get-Item $op).VersionInfo | Format-List FileVersion, ProductVersion, OriginalFilename
    & $op --version
}
Get-Command opencode -ErrorAction SilentlyContinue | Select-Object Source, Version
& $op agent create --help
& $op agent list
```

If the path differs, use the executable the generation job actually calls. Do not update or replace the CLI during diagnosis; version/config changes should be documented before they are made.

## Step 2: check the free-model visibility setting

```powershell
"Process: $env:OPENCODE_DISABLE_FREE_MODELS"
"User:    $([Environment]::GetEnvironmentVariable('OPENCODE_DISABLE_FREE_MODELS','User'))"
"Machine: $([Environment]::GetEnvironmentVariable('OPENCODE_DISABLE_FREE_MODELS','Machine'))"
"OPENCODE_PERMISSION set in process: $([bool]$env:OPENCODE_PERMISSION)"
"OPENCODE_CONFIG set in process: $([bool]$env:OPENCODE_CONFIG)"
"OPENCODE_CONFIG_CONTENT set in process: $([bool]$env:OPENCODE_CONFIG_CONTENT)"
"OPENCODE_CONFIG_DIR set in process: $([bool]$env:OPENCODE_CONFIG_DIR)"
```

A value of `1` or `true` disables free-model visibility in the documented OpenCode versions. A blank value here does not rule out a setting injected into a separate long-running OpenCode service; record whether the generation runner uses a shared service or a direct executable.

## Step 3: inspect the provider catalog without generating text

```powershell
& $op models opencode
```

Check whether each exact frozen ID appears. If the list looks stale, it is safe to refresh metadata without generating text:

```powershell
& $op models --refresh opencode
```

If the executable rejects the refresh syntax, do not guess at other options; capture the usage/error and its version. Do not invoke `opencode run` as a diagnostic because that would be a model call.

## Step 4: classify the evidence

Record the exact result in this small table. Do not include API keys, cookies, auth files, or credentials.

| Item | Record |
|---|---|
| Executable path and version | Exact output |
| `OPENCODE_DISABLE_FREE_MODELS` process/user/machine values | Exact values |
| Catalog visibility for each of the three model IDs | Present / absent / error |
| Error text, if any | Redact secrets only; keep the error category |
| Free-limit reset or retry time, if shown by the UI | Exact time shown |
| Runtime route | Direct CLI or shared service; identify which only |
| Confirmed model generation test | **Not run** |

Interpretation:

- **Absent from catalog**: investigate local visibility/configuration, provider activation, and cache/version. This alone does not prove the service has withdrawn the model globally.
- **Present, but no request has been made**: model access remains unverified. Do not claim the model is usable from a listing alone.
- **Present, with a free-limit message/reset time**: operational quota block, not evidence of catalog removal.
- **Present, with authentication/provider/unavailable/network error**: retain the exact category; each has a different remedy and no model call is required to collect the current error if it was already displayed.
- **Only one or two frozen models usable**: the complete frozen sampling frame is not presently executable. Do not silently replace the missing model(s); any changed frame needs an explicit versioned protocol decision.

## Current status

Until these observations are recorded, the evidence supports `BLOCKED_GENERATION_ACCESS_UNDIAGNOSED` rather than either “all free models were removed” or “generation access is available.” No generation batch is authorized by this document.


## Tool-permission compatibility note

The official [agent-create CLI reference](https://dev.opencode.ai/docs/cli/) documents `opencode agent create --permissions <comma-separated allowlist>` (alias `--tools`); omitted permissions are denied in the generated agent configuration. The [permissions reference](https://dev.opencode.ai/docs/permissions/) documents `OPENCODE_PERMISSION` as an environment-supplied JSON permission config and confirms that `--auto` auto-approves requests not explicitly denied.

Do not use `--auto`. Do not assume `OPENCODE_PERMISSION='{"*":"deny"}'` is a compatible fix for the frozen free models: recent upstream reports include 403 errors when all tools or `bash` are denied for free-tier models ([issue #50627](https://github.com/anomalyco/opencode/issues/50627), [issue #49433](https://github.com/anomalyco/opencode/issues/49433)). This remains a compatibility uncertainty that must be resolved without weakening the no-tools requirement. The environment-variable policy is not intrinsically immutable; run with a controlled/sanitized environment and verify the effective loaded agent/config rather than merely checking one variable.

No model generation should be used as an unrecorded smoke test. If an actual model request is needed to determine whether the frozen no-tools configuration is accepted, it must be treated as the next prespecified generation batch under a properly frozen successor protocol. If the required permission profile is rejected by the fixed provider, stop and record the operational incompatibility; do not relax permissions or substitute a model silently.
