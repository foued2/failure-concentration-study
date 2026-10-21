param([string]$RunTag = 'acl-test-2')
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$inputDir = Join-Path $root 'guest-input'
$outputDir = Join-Path $root ('guest-output-' + $RunTag)
$sandboxConfig = Join-Path $root ('trust-channel-' + $RunTag + '.wsb')

if (-not (Test-Path -LiteralPath $inputDir -PathType Container)) { throw 'The reviewed guest-input directory is missing.' }
if (-not (Test-Path -LiteralPath $outputDir)) { New-Item -ItemType Directory -Path $outputDir | Out-Null }
if (@(Get-ChildItem -LiteralPath $outputDir -Force).Count -gt 0) { throw 'Refusing to overwrite nonempty guest-output evidence.' }
if (-not (Test-Path -LiteralPath 'C:\Windows\System32\WindowsSandbox.exe')) { throw 'Windows Sandbox executable is unavailable.' }
$guestHarnessName = 'guest_privilege_test-' + $RunTag + '.ps1'
$guestHarness = Join-Path $inputDir $guestHarnessName
if (Test-Path -LiteralPath $guestHarness) { throw 'Refusing to overwrite an existing guest harness.' }
Copy-Item -LiteralPath (Join-Path $root 'guest_privilege_test.ps1') -Destination $guestHarness

$xml = @"
<Configuration>
  <VGpu>Disable</VGpu>
  <Networking>Disable</Networking>
  <ProtectedClient>Enable</ProtectedClient>
  <ClipboardRedirection>Disable</ClipboardRedirection>
  <AudioInput>Disable</AudioInput>
  <VideoInput>Disable</VideoInput>
  <PrinterRedirection>Disable</PrinterRedirection>
  <MemoryInMB>2048</MemoryInMB>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>$inputDir</HostFolder>
      <SandboxFolder>C:\Users\WDAGUtilityAccount\Desktop\trust-input</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>$outputDir</HostFolder>
      <SandboxFolder>C:\Users\WDAGUtilityAccount\Desktop\trust-output</SandboxFolder>
      <ReadOnly>false</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File C:\Users\WDAGUtilityAccount\Desktop\trust-input\$guestHarnessName</Command>
  </LogonCommand>
</Configuration>
"@
Set-Content -LiteralPath $sandboxConfig -Value $xml -Encoding UTF8
$sandboxProcess = Start-Process -FilePath 'C:\Windows\System32\WindowsSandbox.exe' -ArgumentList ('"' + $sandboxConfig + '"') -WindowStyle Hidden -PassThru
$resultPath = Join-Path $outputDir 'supervisor-results.json'
$deadline = [DateTime]::UtcNow.AddSeconds(120)
while (-not (Test-Path -LiteralPath $resultPath) -and [DateTime]::UtcNow -lt $deadline) { Start-Sleep -Milliseconds 500 }
if (-not (Test-Path -LiteralPath $resultPath)) { throw 'Sandbox did not return the supervisor-owned result file within 120 seconds.' }
$result = Get-Content -LiteralPath $resultPath -Raw | ConvertFrom-Json
$result | ConvertTo-Json -Depth 10
if ($result.summary.failed -gt 0 -or $result.limitations.Count -gt 0) { exit 1 }
