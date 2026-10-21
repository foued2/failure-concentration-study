$ErrorActionPreference = 'Continue'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$tests = [System.Collections.Generic.List[object]]::new()
function Add-TestResult([string]$Name, [bool]$Passed, [string]$Detail) {
    $tests.Add([pscustomobject]@{ Test = $Name; Result = $(if ($Passed) { 'PASS' } else { 'FAIL' }); Detail = $Detail })
}

# A deliberately failing child must not terminate the supervisor.
try {
    $crash = Start-Process -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" `
        -ArgumentList '-NoProfile', '-Command', 'exit 37' -Wait -PassThru
    Add-TestResult 'Child crash containment' ($crash.ExitCode -eq 37) "Child exit code=$($crash.ExitCode); harness continued."
} catch { Add-TestResult 'Child crash containment' $false $_.Exception.Message }

# Invalid protocol output must be rejected.
try {
    $null = '{not-json' | ConvertFrom-Json -ErrorAction Stop
    Add-TestResult 'Malformed output rejection' $false 'Malformed JSON was accepted.'
} catch { Add-TestResult 'Malformed output rejection' $true 'Malformed JSON raised a parse error.' }

# The supervisor enforces a two-second timeout and terminates its child.
try {
    $child = Start-Process -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" `
        -ArgumentList '-NoProfile', '-Command', 'Start-Sleep -Seconds 60' -PassThru
    $completed = $child.WaitForExit(2000)
    if (-not $completed) {
        Stop-Process -Id $child.Id -Force -ErrorAction Stop
        $child.WaitForExit()
    }
    Add-TestResult 'Bounded timeout and termination' ((-not $completed) -and $child.HasExited) "Initial wait completed=$completed; child exited=$($child.HasExited)."
} catch { Add-TestResult 'Bounded timeout and termination' $false $_.Exception.Message }

# Confirm the configured VM memory ceiling is visible inside the guest.
try {
    $memoryBytes = (Get-CimInstance Win32_ComputerSystem -ErrorAction Stop).TotalPhysicalMemory
    $memoryMb = [math]::Round($memoryBytes / 1MB)
    Add-TestResult 'Configured memory ceiling visible' ($memoryBytes -le 2.5GB) "Guest reports ${memoryMb} MB; .wsb sets 2048 MB. This checks the visible ceiling, not adversarial memory exhaustion."
} catch { Add-TestResult 'Configured memory ceiling visible' $false "Memory query failed: $($_.Exception.Message)" }

# No host folders are mapped. Try a known host file read and a unique host temp write.
$hostReadPath = '\\tsclient\C\Users\pakla\PycharmProjects\failure-concentration-study\README.md'
try {
    $null = [System.IO.File]::ReadAllText($hostReadPath)
    Add-TestResult 'Host file read blocked' $false 'The host README was readable through the attempted redirection path.'
} catch { Add-TestResult 'Host file read blocked' $true 'Read through the attempted host redirection path failed.' }

$marker = 'codex-sandbox-host-probe-20261021-7f3a9b1c.txt'
$hostWritePath = "\\tsclient\C\Users\pakla\AppData\Local\Temp\$marker"
try {
    [System.IO.File]::WriteAllText($hostWritePath, 'sandbox containment probe')
    Add-TestResult 'Host file write blocked' $false "Write unexpectedly succeeded; host verification marker: $marker"
} catch { Add-TestResult 'Host file write blocked' $true 'Write through the attempted host redirection path failed.' }

# Disabled guest networking should prevent this bounded outbound connection attempt.
$client = [System.Net.Sockets.TcpClient]::new()
try {
    $pending = $client.BeginConnect('1.1.1.1', 443, $null, $null)
    $connectedInTime = $pending.AsyncWaitHandle.WaitOne(2000)
    $blocked = (-not $connectedInTime) -or (-not $client.Connected)
    if ($client.Connected) { $client.EndConnect($pending) }
    Add-TestResult 'Outbound network blocked' $blocked "Connected=$($client.Connected); bounded wait=2000 ms."
} catch { Add-TestResult 'Outbound network blocked' $true "Connection attempt failed: $($_.Exception.GetType().Name)" }
finally { $client.Dispose() }

# Guest-local scratch writes should work and are removed immediately.
$localPath = Join-Path $env:TEMP 'codex-sandbox-local-probe.tmp'
try {
    [System.IO.File]::WriteAllText($localPath, 'guest-local-only')
    $ok = Test-Path -LiteralPath $localPath
    Add-TestResult 'Guest-local write' $ok 'Temporary guest-local file was written.'
} catch { Add-TestResult 'Guest-local write' $false $_.Exception.Message }
finally { Remove-Item -LiteralPath $localPath -Force -ErrorAction SilentlyContinue }

$form = New-Object System.Windows.Forms.Form
$form.Text = 'Windows Sandbox harmless containment checks'
$form.Width = 1000
$form.Height = 560
$form.StartPosition = 'CenterScreen'
$box = New-Object System.Windows.Forms.TextBox
$box.Multiline = $true
$box.ReadOnly = $true
$box.ScrollBars = 'Vertical'
$box.Dock = 'Fill'
$box.Font = New-Object System.Drawing.Font('Consolas', 11)
$lines = @('Sandbox fixture results', "Run time: $(Get-Date -Format o)", 'Configuration: networking/clipboard disabled; no mapped folders; Protected Client enabled; memory cap 2048 MB.', '')
foreach ($test in $tests) { $lines += ('[{0}] {1}: {2}' -f $test.Result, $test.Test, $test.Detail) }
$failed = @($tests | Where-Object Result -ne 'PASS').Count
$lines += ''
$lines += "Summary: $(@($tests).Count - $failed) PASS; $failed FAIL."
$lines += 'Inspect this window, then close the Sandbox to discard the guest.'
$box.Text = $lines -join [Environment]::NewLine
$form.Controls.Add($box)
[void]$form.ShowDialog()
