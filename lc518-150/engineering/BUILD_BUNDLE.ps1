$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Part1 = Join-Path $Here "m1si_audit_bundle.part1"
$Part2 = Join-Path $Here "m1si_audit_bundle.part2"
$ZipPath = Join-Path $Here "m1si_audit_bundle.zip"
$RepoRoot = (Resolve-Path (Join-Path $Here "..\..")).Path
$ExpectedSha256 = "0e5cec8b63bd43dae0a3d8e688b9edf66f17167fbef74be588a884c18e36fc56"

foreach ($Path in @($Part1, $Part2)) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing bundle part: $Path"
    }
}

$Output = [System.IO.File]::Open($ZipPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write)
try {
    foreach ($Path in @($Part1, $Part2)) {
        $Input = [System.IO.File]::OpenRead($Path)
        try { $Input.CopyTo($Output) } finally { $Input.Dispose() }
    }
}
finally {
    $Output.Dispose()
}

$ActualSha256 = (Get-FileHash -LiteralPath $ZipPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualSha256 -ne $ExpectedSha256) {
    Remove-Item -LiteralPath $ZipPath -Force
    throw "Bundle hash mismatch. Expected $ExpectedSha256, received $ActualSha256"
}

Expand-Archive -LiteralPath $ZipPath -DestinationPath $RepoRoot -Force
Write-Host "Bundle verified and extracted to $RepoRoot"
Write-Host "ZIP SHA-256: $ActualSha256"
