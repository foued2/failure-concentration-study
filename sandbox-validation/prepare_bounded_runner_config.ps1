$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$guestScript = Join-Path $root 'guest_bounded_runner_harness.ps1'
$configPath = Join-Path $root 'restrictive-bounded-runner-validation.wsb'
$scriptText = [System.IO.File]::ReadAllText($guestScript)
$encoded = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($scriptText))
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
  <LogonCommand>
    <Command>powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -STA -EncodedCommand $encoded</Command>
  </LogonCommand>
</Configuration>
"@
[System.IO.File]::WriteAllText($configPath, $xml, [System.Text.UTF8Encoding]::new($false))
[xml]$check = [System.IO.File]::ReadAllText($configPath)
if ($check.Configuration.Networking -ne 'Disable' -or
    $check.Configuration.ClipboardRedirection -ne 'Disable' -or
    $check.Configuration.ProtectedClient -ne 'Enable' -or
    $null -ne $check.Configuration.MappedFolders -or
    [int]$check.Configuration.MemoryInMB -ne 2048) { throw 'Restrictive config validation failed.' }
if ($encoded.Length -gt 30000) { throw "Encoded command is too large for the Windows command-line limit ($($encoded.Length))." }
[pscustomobject]@{ Config=$configPath; EncodedCommandCharacters=$encoded.Length; MappedFolders=0; Networking='Disable'; ClipboardRedirection='Disable'; ProtectedClient='Enable'; MemoryInMB=2048 }
