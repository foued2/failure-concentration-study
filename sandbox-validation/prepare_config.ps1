$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$guestScript = Join-Path $root 'guest_harmless_tests.ps1'
$configPath = Join-Path $root 'restrictive-validation.wsb'
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
    <Command>powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -EncodedCommand $encoded</Command>
  </LogonCommand>
</Configuration>
"@
[System.IO.File]::WriteAllText($configPath, $xml, [System.Text.UTF8Encoding]::new($false))
Write-Output $configPath
