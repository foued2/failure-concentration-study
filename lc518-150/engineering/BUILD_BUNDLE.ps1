$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Names = 1..5 | ForEach-Object { "m1si_audit_bundle.b64.{0:D3}" -f $_ }
$Encoded = ($Names | ForEach-Object {
    $Path = Join-Path $Here $_
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing bundle segment: $Path"
    }
    [System.IO.File]::ReadAllText($Path).Trim()
}) -join ""

try {
    $ZipBytes = [Convert]::FromBase64String($Encoded)
}
catch {
    throw "Bundle segments are not valid concatenated Base64: $($_.Exception.Message)"
}

$ZipPath = Join-Path $Here "m1si_audit_bundle.zip"
[System.IO.File]::WriteAllBytes($ZipPath, $ZipBytes)

$ExpectedSha256 = "0e5cec8b63bd43dae0a3d8e688b9edf66f17167fbef74be588a884c18e36fc56"
$ActualSha256 = (Get-FileHash -LiteralPath $ZipPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualSha256 -ne $ExpectedSha256) {
    Remove-Item -LiteralPath $ZipPath -Force
    throw "Bundle hash mismatch. Expected $ExpectedSha256, received $ActualSha256"
}

$RepoRoot = (Resolve-Path (Join-Path $Here "..\..")).Path
Expand-Archive -LiteralPath $ZipPath -DestinationPath $RepoRoot -Force
Write-Host "Bundle verified and extracted to $RepoRoot"
Write-Host "ZIP SHA-256: $ActualSha256"
