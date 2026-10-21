$ErrorActionPreference = 'Continue'
$results = [ordered]@{}

# Process remains usable after a deliberately failing child.
$crash = Start-Process -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" `
    -ArgumentList '-NoProfile', '-Command', 'exit 37' -Wait -PassThru
$results['crash_child_exit_code'] = $crash.ExitCode
$results['parent_survived_crash'] = ($crash.ExitCode -eq 37)

# Malformed protocol output must be rejected, not treated as a valid result.
try {
    $null = '{not-json' | ConvertFrom-Json -ErrorAction Stop
    $results['malformed_output_rejected'] = $false
} catch {
    $results['malformed_output_rejected'] = $true
}

# A sleeping child is killed by a bounded supervisor timeout.
$child = Start-Process -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" `
    -ArgumentList '-NoProfile', '-Command', 'Start-Sleep -Seconds 60' -PassThru
$completed = $child.WaitForExit(2000)
$results['timeout_triggered'] = (-not $completed)
if (-not $completed) {
    Stop-Process -Id $child.Id -Force -ErrorAction SilentlyContinue
    $child.WaitForExit()
}
$results['timed_out_child_terminated'] = $child.HasExited

# Check the guest-visible memory ceiling configured in the .wsb file.
try {
    $memoryBytes = (Get-CimInstance Win32_ComputerSystem -ErrorAction Stop).TotalPhysicalMemory
    $results['guest_memory_mb'] = [math]::Round($memoryBytes / 1MB)
    $results['guest_memory_within_2048mb_cap'] = ($memoryBytes -le 2.5GB)
} catch {
    $results['guest_memory_query_error'] = $_.Exception.Message
    $results['guest_memory_within_2048mb_cap'] = $false
}

# Read and write probes target RDP drive redirection only. The .wsb has no mapped folders.
$hostReadPath = '\\tsclient\C\Users\pakla\PycharmProjects\failure-concentration-study\README.md'
try {
    $null = [System.IO.File]::ReadAllText($hostReadPath)
    $results['host_file_read_blocked'] = $false
} catch {
    $results['host_file_read_blocked'] = $true
}
$hostWritePath = "\\tsclient\C\Users\pakla\AppData\Local\Temp\codex-sandbox-escape-$([guid]::NewGuid().ToString('N')).tmp"
try {
    [System.IO.File]::WriteAllText($hostWritePath, 'harmless containment probe')
    $results['host_file_write_blocked'] = $false
    Remove-Item -LiteralPath $hostWritePath -Force -ErrorAction SilentlyContinue
} catch {
    $results['host_file_write_blocked'] = $true
}

# Disabled networking should prevent a short outbound TCP connection attempt.
$client = [System.Net.Sockets.TcpClient]::new()
try {
    $async = $client.BeginConnect('1.1.1.1', 443, $null, $null)
    $connectedInTime = $async.AsyncWaitHandle.WaitOne(2000)
    $results['outbound_network_blocked'] = (-not $connectedInTime -or -not $client.Connected)
    if ($client.Connected) { $client.EndConnect($async) }
} catch {
    $results['outbound_network_blocked'] = $true
} finally {
    $client.Dispose()
}

$results['guest_local_write_works'] = $false
$localPath = Join-Path $env:TEMP 'codex-sandbox-local-probe.tmp'
try {
    [System.IO.File]::WriteAllText($localPath, 'sandbox-local-only')
    $results['guest_local_write_works'] = (Test-Path -LiteralPath $localPath)
} finally {
    Remove-Item -LiteralPath $localPath -Force -ErrorAction SilentlyContinue
}

Write-Output 'SANDBOX_FIXTURE_RESULTS_BEGIN'
$results | ConvertTo-Json -Depth 4
Write-Output 'SANDBOX_FIXTURE_RESULTS_END'
Write-Output 'Fixture complete; leaving this disposable sandbox open for review.'
Start-Sleep -Seconds 300
