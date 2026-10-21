$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

Add-Type -TypeDefinition @'
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;

public static class TrustTestJob {
    [StructLayout(LayoutKind.Sequential)] public struct BasicLimitInfo {
        public long PerProcessUserTimeLimit, PerJobUserTimeLimit;
        public uint LimitFlags;
        public UIntPtr MinimumWorkingSetSize, MaximumWorkingSetSize;
        public uint ActiveProcessLimit;
        public UIntPtr Affinity;
        public uint PriorityClass, SchedulingClass;
    }
    [StructLayout(LayoutKind.Sequential)] public struct IoCounters {
        public ulong ReadOperationCount, WriteOperationCount, OtherOperationCount;
        public ulong ReadTransferCount, WriteTransferCount, OtherTransferCount;
    }
    [StructLayout(LayoutKind.Sequential)] public struct ExtendedLimitInfo {
        public BasicLimitInfo BasicLimitInformation;
        public IoCounters IoInfo;
        public UIntPtr ProcessMemoryLimit, JobMemoryLimit, PeakProcessMemoryUsed, PeakJobMemoryUsed;
    }
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    public static extern IntPtr CreateJobObject(IntPtr attributes, string name);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool SetInformationJobObject(IntPtr job, int infoClass, IntPtr info, uint length);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern IntPtr OpenProcess(uint access, bool inherit, uint pid);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool AssignProcessToJobObject(IntPtr job, IntPtr process);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool TerminateJobObject(IntPtr job, uint exitCode);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool CloseHandle(IntPtr handle);
    public static IntPtr CreateBoundedJob(ulong memoryBytes) {
        IntPtr job = CreateJobObject(IntPtr.Zero, null);
        if (job == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error(), "CreateJobObject failed");
        ExtendedLimitInfo limits = new ExtendedLimitInfo();
        limits.BasicLimitInformation.LimitFlags = 0x00000200 | 0x00002000; // JOB_MEMORY | KILL_ON_JOB_CLOSE
        limits.JobMemoryLimit = new UIntPtr(memoryBytes);
        IntPtr buffer = Marshal.AllocHGlobal(Marshal.SizeOf(typeof(ExtendedLimitInfo)));
        try {
            Marshal.StructureToPtr(limits, buffer, false);
            if (!SetInformationJobObject(job, 9, buffer, (uint)Marshal.SizeOf(typeof(ExtendedLimitInfo))))
                throw new Win32Exception(Marshal.GetLastWin32Error(), "SetInformationJobObject failed");
            return job;
        } catch { CloseHandle(job); throw; }
        finally { Marshal.FreeHGlobal(buffer); }
    }
    public static void Assign(IntPtr job, int pid) {
        IntPtr process = OpenProcess(0x0100 | 0x0001, false, (uint)pid);
        if (process == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error(), "OpenProcess failed");
        try {
            if (!AssignProcessToJobObject(job, process))
                throw new Win32Exception(Marshal.GetLastWin32Error(), "AssignProcessToJobObject failed");
        } finally { CloseHandle(process); }
    }
}
'@ -Language CSharp

$root = 'C:\Users\WDAGUtilityAccount\Desktop'
$inputDir = Join-Path $root 'trust-input'
$outputDir = Join-Path $root 'trust-output'
$workspace = 'C:\Users\fc_trust_worker\work'
$workerName = 'fc_trust_worker'
$timeLimitSeconds = 2
$results = [ordered]@{ run_as = [Security.Principal.WindowsIdentity]::GetCurrent().Name; tests = @(); limitations = @() }

function Add-Test([string]$name, [bool]$passed, [string]$detail) {
    $script:results.tests += [ordered]@{ name = $name; passed = $passed; detail = $detail }
}
function Quote-PS([string]$value) { return "'" + $value.Replace("'", "''") + "'" }

try {
    $currentSid = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
    $systemSid = 'S-1-5-18'
    $passwordText = ([guid]::NewGuid().ToString('N') + 'aA1!')
    $securePassword = ConvertTo-SecureString $passwordText -AsPlainText -Force
    if (-not (Get-LocalUser -Name $workerName -ErrorAction SilentlyContinue)) {
        New-LocalUser -Name $workerName -Password $securePassword -PasswordNeverExpires -UserMayNotChangePassword | Out-Null
    }
    $worker = Get-LocalUser -Name $workerName
    $credential = [pscredential]::new("$env:COMPUTERNAME\$workerName", $securePassword)

    New-Item -ItemType Directory -Force -Path $workspace | Out-Null
    $workerSid = $worker.Sid.Value
    & icacls.exe $workspace /inheritance:r /grant "*$workerSid`:(OI)(CI)M" "*$currentSid`:(OI)(CI)F" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Could not establish worker-only workspace ACL.' }

    $protectedRunner = Join-Path $inputDir (Split-Path -Leaf $PSCommandPath)
    $protectedInput = Join-Path $inputDir 'trusted-input-marker.txt'
    $hostChannel = Join-Path $outputDir 'secure-channel'
    New-Item -ItemType Directory -Force -Path $hostChannel | Out-Null
    $markerFiles = @{}
    foreach ($name in @('read.txt', 'overwrite.txt', 'delete.txt')) {
        $p = Join-Path $hostChannel $name
        [IO.File]::WriteAllText($p, "trusted:$name")
        $markerFiles[$name] = $p
    }

    & icacls.exe $hostChannel /inheritance:r /grant "*$currentSid`:(OI)(CI)F" "*$systemSid`:(OI)(CI)F" | Out-Null
    $aclApplied = ($LASTEXITCODE -eq 0)
    if (-not $aclApplied) { throw "Could not apply supervisor-only ACL to the mapped output channel; icacls exit=$LASTEXITCODE." }
    Add-Test 'Supervisor can create and read its result channel' ((Get-Content -LiteralPath $markerFiles['read.txt'] -Raw) -eq 'trusted:read.txt') 'Supervisor created protected canary records.'

    $workerScript = @'
$ErrorActionPreference = 'Stop'
$req = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'request.json') -Raw | ConvertFrom-Json
$r = [ordered]@{ read=false; overwriteDenied=false; deleteDenied=false; forgeDenied=false; runnerModifyDenied=false; inputModifyDenied=false; systemWriteDenied=false; workspaceWrite=false; identity=[Security.Principal.WindowsIdentity]::GetCurrent().Name }
try { [void][IO.File]::ReadAllText($req.readPath); $r.read = $true } catch { }
try { [IO.File]::WriteAllText($req.overwritePath, 'forged') } catch { $r.overwriteDenied = $true }
try { Remove-Item -LiteralPath $req.deletePath -Force } catch { $r.deleteDenied = $true }
try { [IO.File]::WriteAllText($req.forgePath, '{"correct":true,"k":0,"C":0}') } catch { $r.forgeDenied = $true }
try { [IO.File]::WriteAllText($req.runnerPath, 'tampered') } catch { $r.runnerModifyDenied = $true }
try { [IO.File]::WriteAllText($req.inputPath, 'tampered') } catch { $r.inputModifyDenied = $true }
try { [IO.File]::WriteAllText($req.systemPath, 'tampered') } catch { $r.systemWriteDenied = $true }
try { [IO.File]::WriteAllText((Join-Path $PSScriptRoot 'worker-writable.txt'), 'ok'); $r.workspaceWrite = $true } catch { }
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'worker-result.json'), ($r | ConvertTo-Json -Compress))
'@
    $workerScriptPath = Join-Path $workspace 'worker.ps1'
    Set-Content -LiteralPath $workerScriptPath -Value $workerScript -Encoding UTF8
    $request = [ordered]@{
        readPath=$markerFiles['read.txt']; overwritePath=$markerFiles['overwrite.txt']; deletePath=$markerFiles['delete.txt'];
        forgePath=(Join-Path $hostChannel 'forged.json'); runnerPath=$protectedRunner; inputPath=$protectedInput;
        systemPath='C:\Windows\System32\fc-trust-escape-marker.txt'
    }
    Set-Content -LiteralPath (Join-Path $workspace 'request.json') -Value ($request | ConvertTo-Json -Compress) -Encoding UTF8
    $workerStdout = Join-Path $workspace 'access-worker.stdout.txt'
    $workerStderr = Join-Path $workspace 'access-worker.stderr.txt'
    [IO.File]::WriteAllText($workerStdout, '')
    [IO.File]::WriteAllText($workerStderr, '')
    $proc = Start-Process -FilePath (Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe') -Credential $credential -PassThru -Wait -ArgumentList @('-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',$workerScriptPath) -RedirectStandardOutput $workerStdout -RedirectStandardError $workerStderr
    $workerRecordPath = Join-Path $workspace 'worker-result.json'
    $workerRecord = if (Test-Path -LiteralPath $workerRecordPath) { Get-Content -LiteralPath $workerRecordPath -Raw | ConvertFrom-Json } else { $null }
    if ($workerRecord) {
        Add-Test 'Separate worker identity is unprivileged' ($workerRecord.identity -match [regex]::Escape($workerName)) $workerRecord.identity
        Add-Test 'Worker cannot read supervisor result channel' (-not $workerRecord.read) ('read=' + $workerRecord.read)
        Add-Test 'Worker cannot overwrite, delete, or forge channel records' ($workerRecord.overwriteDenied -and $workerRecord.deleteDenied -and $workerRecord.forgeDenied) ('overwriteDenied={0}; deleteDenied={1}; forgeDenied={2}' -f $workerRecord.overwriteDenied,$workerRecord.deleteDenied,$workerRecord.forgeDenied)
        Add-Test 'Worker cannot modify trusted runner or input' ($workerRecord.runnerModifyDenied -and $workerRecord.inputModifyDenied) ('runnerDenied={0}; inputDenied={1}' -f $workerRecord.runnerModifyDenied,$workerRecord.inputModifyDenied)
        Add-Test 'Worker cannot write protected system path' $workerRecord.systemWriteDenied ('systemWriteDenied=' + $workerRecord.systemWriteDenied)
        Add-Test 'Worker can write within its designated workspace' $workerRecord.workspaceWrite ('workspaceWrite=' + $workerRecord.workspaceWrite)
    } else {
        $workerError = if (Test-Path -LiteralPath $workerStderr) { Get-Content -LiteralPath $workerStderr -Raw } else { '' }
        $workerOut = if (Test-Path -LiteralPath $workerStdout) { Get-Content -LiteralPath $workerStdout -Raw } else { '' }
        Add-Test 'Separate worker identity completed access checks' $false "exit=$($proc.ExitCode); no worker result; stderr=$workerError; stdout=$workerOut"
    }
    Add-Test 'Supervisor channel records remain unchanged' ((Get-Content -LiteralPath $markerFiles['overwrite.txt'] -Raw) -eq 'trusted:overwrite.txt' -and (Get-Content -LiteralPath $markerFiles['delete.txt'] -Raw) -eq 'trusted:delete.txt' -and -not (Test-Path -LiteralPath (Join-Path $hostChannel 'forged.json'))) 'Supervisor re-read canaries after worker exit.'
    Add-Test 'Read-only mounted runner and input remain unchanged' ((Get-Content -LiteralPath $protectedRunner -Raw) -eq 'trusted-runner-v1' -and (Get-Content -LiteralPath $protectedInput -Raw) -eq 'trusted-input-v1') 'Host fixture bytes checked after worker exit.'

    # A worker waits at a trusted gate so the supervisor can assign it to the job
    # before it starts a descendant or allocates memory.
    $gate = Join-Path $workspace 'tree-gate'
    $childPidFile = Join-Path $workspace 'child.pid'
    $sleepCode = 'Start-Sleep -Seconds 90'
    $sleepEncoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($sleepCode))
    $treeCode = @"
while (-not (Test-Path -LiteralPath $(Quote-PS $gate))) { Start-Sleep -Milliseconds 20 }
`$child = Start-Process -FilePath '$(Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe')' -ArgumentList @('-NoProfile','-EncodedCommand','$sleepEncoded') -PassThru
[IO.File]::WriteAllText('$(Quote-PS $childPidFile)', `$child.Id.ToString())
Start-Sleep -Seconds 90
"@
    $treePath = Join-Path $workspace 'tree-worker.ps1'
    Set-Content -LiteralPath $treePath -Value $treeCode -Encoding UTF8
    $job = [IntPtr]::Zero; $tree = $null; $childPid = 0
    try {
        $job = [TrustTestJob]::CreateBoundedJob(256MB)
        $tree = Start-Process -FilePath (Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe') -Credential $credential -PassThru -ArgumentList @('-NoLogo','-NoProfile','-File',$treePath)
        [TrustTestJob]::Assign($job, $tree.Id)
        Set-Content -LiteralPath $gate -Value 'go' -NoNewline
        $deadline = [DateTime]::UtcNow.AddSeconds(5)
        while (-not (Test-Path -LiteralPath $childPidFile) -and [DateTime]::UtcNow -lt $deadline) { Start-Sleep -Milliseconds 50 }
        if (Test-Path -LiteralPath $childPidFile) { $childPid = [int](Get-Content -LiteralPath $childPidFile -Raw) }
        $finishedBeforeTimeout = $tree.WaitForExit(1500)
        if (-not $finishedBeforeTimeout) { [void][TrustTestJob]::TerminateJobObject($job,124); $tree.WaitForExit(5000) }
        $parentGone = $tree.HasExited
        $childGone = $false
        $until = [DateTime]::UtcNow.AddSeconds(5)
        while ($childPid -gt 0 -and -not $childGone -and [DateTime]::UtcNow -lt $until) { $childGone = -not [bool](Get-Process -Id $childPid -ErrorAction SilentlyContinue); if (-not $childGone) { Start-Sleep -Milliseconds 50 } }
        Add-Test 'Job timeout terminates worker and descendant' ((-not $finishedBeforeTimeout) -and $parentGone -and $childGone) "timeout=$(-not $finishedBeforeTimeout); parentGone=$parentGone; childGone=$childGone; childStarted=$($childPid -gt 0)"
    } catch { Add-Test 'Job timeout terminates worker and descendant' $false $_.Exception.Message }
    finally { if ($job -ne [IntPtr]::Zero) { [void][TrustTestJob]::CloseHandle($job) }; if ($tree -and -not $tree.HasExited) { Stop-Process -Id $tree.Id -Force -ErrorAction SilentlyContinue } }

    $memoryGate = Join-Path $workspace 'memory-gate'
    $memoryStatus = Join-Path $workspace 'memory-status.txt'
    $memoryCode = @"
while (-not (Test-Path -LiteralPath $(Quote-PS $memoryGate))) { Start-Sleep -Milliseconds 20 }
`$blocks = [System.Collections.Generic.List[byte[]]]::new(); `$count=0
try { for (`$i=0; `$i -lt 8; `$i++) { `$blocks.Add([byte[]]::new(33554432)); `$count++; Start-Sleep -Milliseconds 40 }; [IO.File]::WriteAllText('$(Quote-PS $memoryStatus)', "ALLOCATED:`$count") }
catch [OutOfMemoryException] { [IO.File]::WriteAllText('$(Quote-PS $memoryStatus)', "LIMIT:`$count") }
"@
    $memoryPath = Join-Path $workspace 'memory-worker.ps1'
    Set-Content -LiteralPath $memoryPath -Value $memoryCode -Encoding UTF8
    $memoryJob = [IntPtr]::Zero; $memoryProc = $null
    try {
        $memoryJob = [TrustTestJob]::CreateBoundedJob(128MB)
        $memoryProc = Start-Process -FilePath (Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe') -Credential $credential -PassThru -ArgumentList @('-NoLogo','-NoProfile','-File',$memoryPath)
        [TrustTestJob]::Assign($memoryJob, $memoryProc.Id)
        Set-Content -LiteralPath $memoryGate -Value 'go' -NoNewline
        $completed = $memoryProc.WaitForExit(10000)
        if (-not $completed) { [void][TrustTestJob]::TerminateJobObject($memoryJob,125); $memoryProc.WaitForExit(3000) }
        $mem = if (Test-Path -LiteralPath $memoryStatus) { Get-Content -LiteralPath $memoryStatus -Raw } else { 'NO_STATUS' }
        Add-Test 'Job memory cap applies to separate worker' ($completed -and $mem -match '^LIMIT:[0-7]$') "cap=128MiB; plannedAllocation=256MiB; workerStatus=$mem; completed=$completed"
    } catch { Add-Test 'Job memory cap applies to separate worker' $false $_.Exception.Message }
    finally { if ($memoryJob -ne [IntPtr]::Zero) { [void][TrustTestJob]::CloseHandle($memoryJob) }; if ($memoryProc -and -not $memoryProc.HasExited) { Stop-Process -Id $memoryProc.Id -Force -ErrorAction SilentlyContinue } }
} catch {
    $results.limitations += ($_.Exception.ToString())
} finally {
    $results.summary = [ordered]@{ total=$results.tests.Count; passed=@($results.tests | Where-Object passed).Count; failed=@($results.tests | Where-Object { -not $_.passed }).Count }
    $results.hostOutputChannel = $outputDir
    $results.workerAccount = $workerName
    $results.aclApplied = $aclApplied
    $results | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $outputDir 'supervisor-results.json') -Encoding UTF8
    shutdown.exe /s /t 3 /f | Out-Null
}
