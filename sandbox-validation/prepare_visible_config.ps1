$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$guestScript = Join-Path $root 'guest_visible_harness.ps1'
$configPath = Join-Path $root 'restrictive-visible-validation.wsb'
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
[xml]$validated = [System.IO.File]::ReadAllText($configPath)
if ($validated.Configuration.Networking -ne 'Disable' -or
    $validated.Configuration.ClipboardRedirection -ne 'Disable' -or
    $validated.Configuration.ProtectedClient -ne 'Enable' -or
    $null -ne $validated.Configuration.MappedFolders) {
    throw 'Restrictive .wsb settings did not validate.'
}
if ($encoded.Length -gt 20000) { throw "Encoded command is unexpectedly large ($($encoded.Length) characters)." }
[pscustomobject]@{ Config = $configPath; EncodedCommandCharacters = $encoded.Length; MappedFolders = 0; Networking = 'Disable'; ClipboardRedirection = 'Disable'; ProtectedClient = 'Enable'; MemoryInMB = 2048 }
