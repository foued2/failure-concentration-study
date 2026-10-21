param([string]$Mode = 'normal', [switch]$InjectFailure, [string]$OutputDir = '')
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = [System.Text.Encoding]::Default
$wire = [Console]::In.ReadLine()
if ($null -eq $wire) { exit 64 }
$wire = [regex]::Replace($wire, '^[^A-Za-z0-9+/]+', '')
$line = [Text.UTF8Encoding]::new($false, $true).GetString([Convert]::FromBase64String($wire))
$q = $line | ConvertFrom-Json -ErrorAction Stop
if ($Mode -eq 'crash') { exit 71 }
if ($Mode -eq 'timeout') {
    $child = Start-Process -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -ArgumentList @('-NoProfile','-Command','Start-Sleep -Seconds 120') -PassThru
    [IO.File]::WriteAllText((Join-Path $env:TEMP 'pilot-child.pid'), $child.Id.ToString())
    while ($true) { Start-Sleep -Seconds 10 }
}
if ($Mode -eq 'malformed') { [Console]::Out.Write('{not-json'); exit 0 }
if ($Mode -eq 'oversized') { [Console]::Out.Write(('X' * 70000)); exit 0 }
if ($Mode -eq 'forged') {
    [Console]::Out.Write('{"answer":0,"correct":true,"family_counts":[0,0,0,0,0,0],"k":0,"C":0}')
    exit 0
}
if ($Mode -eq 'unexpected') { [IO.File]::WriteAllText((Join-Path $OutputDir 'worker-forgery.json'), '{"k":0,"C":0}') }

$n = [int]$q.n; $s = [int]$q.s; $t = [int]$q.t
$dist = [double[]]::new($n); $used = [bool[]]::new($n)
for ($i=0; $i -lt $n; $i++) { $dist[$i] = [double]::PositiveInfinity }
$dist[$s] = 0
for ($step=0; $step -lt $n; $step++) {
    $u = -1; $best = [double]::PositiveInfinity
    for ($i=0; $i -lt $n; $i++) { if (-not $used[$i] -and $dist[$i] -lt $best) { $best=$dist[$i]; $u=$i } }
    if ($u -lt 0) { break }; $used[$u]=$true
    foreach ($edge in $q.edges) { if ([int]$edge[0] -eq $u) { $v=[int]$edge[1]; $candidate=$dist[$u]+[double]$edge[2]; if ($candidate -lt $dist[$v]) { $dist[$v]=$candidate } } }
}
$answer = if ([double]::IsPositiveInfinity($dist[$t])) { -1 } else { [long]$dist[$t] }
if ($InjectFailure) { $answer = if ($answer -eq -1) { 0 } else { $answer + 1 } }
if ($Mode -eq 'delayed-child') {
    $child = Start-Process -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -ArgumentList @('-NoProfile','-Command','Start-Sleep -Seconds 120') -PassThru
    [IO.File]::WriteAllText((Join-Path $env:TEMP 'pilot-child.pid'), $child.Id.ToString())
}
[Console]::Out.Write($answer.ToString([Globalization.CultureInfo]::InvariantCulture) + "`n")
