$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$native = @'
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
public static class BoundedJob {
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
    static extern IntPtr CreateJobObject(IntPtr attributes, string name);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool SetInformationJobObject(IntPtr job, int infoClass, IntPtr info, uint length);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern IntPtr OpenProcess(uint access, bool inherit, uint pid);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool AssignProcessToJobObject(IntPtr job, IntPtr process);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool TerminateJobObject(IntPtr job, uint exitCode);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool CloseHandle(IntPtr handle);

    public static IntPtr CreateMemoryCappedJob(ulong capBytes) {
        IntPtr job = CreateJobObject(IntPtr.Zero, null);
        if (job == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error(), "CreateJobObject failed");
        ExtendedLimitInfo limits = new ExtendedLimitInfo();
        limits.BasicLimitInformation.LimitFlags = 0x00000200 | 0x00002000; // JOB_MEMORY | KILL_ON_JOB_CLOSE
        limits.JobMemoryLimit = new UIntPtr(capBytes);
        IntPtr buffer = Marshal.AllocHGlobal(Marshal.SizeOf(typeof(ExtendedLimitInfo)));
        try {
            Marshal.StructureToPtr(limits, buffer, false);
            if (!SetInformationJobObject(job, 9, buffer, (uint)Marshal.SizeOf(typeof(ExtendedLimitInfo))))
                throw new Win32Exception(Marshal.GetLastWin32Error(), "SetInformationJobObject failed");
        } catch { CloseHandle(job); throw; }
        finally { Marshal.FreeHGlobal(buffer); }
        return job;
    }
    public static void Assign(IntPtr job, int pid) {
        IntPtr process = OpenProcess(0x0100 | 0x0001, false, (uint)pid); // SET_QUOTA | TERMINATE
        if (process == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error(), "OpenProcess failed");
        try {
            if (!AssignProcessToJobObject(job, process))
                throw new Win32Exception(Marshal.GetLastWin32Error(), "AssignProcessToJobObject failed");
        } finally { CloseHandle(process); }
    }
    public static void Terminate(IntPtr job, uint exitCode) {
        if (!TerminateJobObject(job, exitCode)) throw new Win32Exception(Marshal.GetLastWin32Error(), "TerminateJobObject failed");
    }
    public static void Close(IntPtr job) { if (job != IntPtr.Zero) CloseHandle(job); }
}
'@
Add-Type -TypeDefinition $native -Language CSharp

$results = [System.Collections.Generic.List[object]]::new()
function Add-Result([string]$Name, [bool]$Passed, [string]$Detail) {
    $results.Add([pscustomobject]@{ Test=$Name; Result=$(if ($Passed) { 'PASS' } else { 'FAIL' }); Detail=$Detail })
}

$temp = Join-Path $env:TEMP ('bounded-runner-' + [guid]::NewGuid().ToString('N'))
[void][System.IO.Directory]::CreateDirectory($temp)
$powershellExe = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'

# Simulate a runner timeout under a Job Object. The root waits for a gate so it can be
# assigned before creating its child; descendants then inherit job membership.
$gate = Join-Path $temp 'start-tree'
$childPidFile = Join-Path $temp 'grandchild.pid'
$treeCode = @"
while (-not (Test-Path -LiteralPath '$gate')) { Start-Sleep -Milliseconds 20 }
`$grandchild = Start-Process -FilePath '$powershellExe' -ArgumentList '-NoProfile','-Command','Start-Sleep -Seconds 90' -PassThru
[System.IO.File]::WriteAllText('$childPidFile', `$grandchild.Id.ToString())
Start-Sleep -Seconds 90
"@
$treeEncoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($treeCode))
$treeJob = [IntPtr]::Zero
$treeProcess = $null
$grandchildPid = 0
try {
    $treeJob = [BoundedJob]::CreateMemoryCappedJob(256MB)
    $treeProcess = Start-Process -FilePath $powershellExe -ArgumentList @('-NoProfile','-EncodedCommand',$treeEncoded) -PassThru
    [BoundedJob]::Assign($treeJob, $treeProcess.Id)
    [System.IO.File]::WriteAllText($gate, 'go')
    $deadline = [DateTime]::UtcNow.AddSeconds(5)
    while (-not (Test-Path -LiteralPath $childPidFile) -and [DateTime]::UtcNow -lt $deadline) { Start-Sleep -Milliseconds 50 }
    if (Test-Path -LiteralPath $childPidFile) { $grandchildPid = [int][System.IO.File]::ReadAllText($childPidFile) }
    if ($grandchildPid -gt 0) {
        $completedWithinTimeout = $treeProcess.WaitForExit(1500)
        if (-not $completedWithinTimeout) { [BoundedJob]::Terminate($treeJob, 124) }
        $treeProcess.WaitForExit(5000)
        $treeGone = $treeProcess.HasExited
        $grandchildGone = $false
        $checkUntil = [DateTime]::UtcNow.AddSeconds(5)
        while (-not $grandchildGone -and [DateTime]::UtcNow -lt $checkUntil) {
            $grandchildGone = -not [bool](Get-Process -Id $grandchildPid -ErrorAction SilentlyContinue)
            if (-not $grandchildGone) { Start-Sleep -Milliseconds 50 }
        }
        Add-Result 'Timeout terminates full process tree' ((-not $completedWithinTimeout) -and $treeGone -and $grandchildGone) "Timeout fired=$(-not $completedWithinTimeout); parent exited=$treeGone; child exited=$grandchildGone."
    } else {
        Add-Result 'Timeout terminates full process tree' $false 'Grandchild did not start and publish its PID before the 5-second setup bound.'
    }
} catch { Add-Result 'Timeout terminates full process tree' $false $_.Exception.Message }
finally {
    if ($treeJob -ne [IntPtr]::Zero) { try { [BoundedJob]::Close($treeJob) } catch {} }
    if ($treeProcess -and -not $treeProcess.HasExited) { Stop-Process -Id $treeProcess.Id -Force -ErrorAction SilentlyContinue }
    if ($grandchildPid -gt 0 -and (Get-Process -Id $grandchildPid -ErrorAction SilentlyContinue)) { Stop-Process -Id $grandchildPid -Force -ErrorAction SilentlyContinue }
}

# A separate 128 MiB Job Object cap bounds a controlled allocation fixture to the guest.
# It allocates at most eight 32 MiB chunks and records whether the job cap prevents all 256 MiB.
$gate = Join-Path $temp 'start-memory'
$statusFile = Join-Path $temp 'memory-status.txt'
$memoryCode = @"
while (-not (Test-Path -LiteralPath '$gate')) { Start-Sleep -Milliseconds 20 }
`$blocks = [System.Collections.Generic.List[byte[]]]::new()
`$count = 0
try {
  for (`$i=0; `$i -lt 8; `$i++) { `$blocks.Add([byte[]]::new(33554432)); `$count++; Start-Sleep -Milliseconds 50 }
  [System.IO.File]::WriteAllText('$statusFile', "ALLOCATED:`$count")
} catch [System.OutOfMemoryException] {
  [System.IO.File]::WriteAllText('$statusFile', "LIMIT:`$count")
}
"@
$memoryEncoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($memoryCode))
$memoryJob = [IntPtr]::Zero
$memoryProcess = $null
try {
    $memoryJob = [BoundedJob]::CreateMemoryCappedJob(128MB)
    $memoryProcess = Start-Process -FilePath $powershellExe -ArgumentList @('-NoProfile','-EncodedCommand',$memoryEncoded) -PassThru
    [BoundedJob]::Assign($memoryJob, $memoryProcess.Id)
    [System.IO.File]::WriteAllText($gate, 'go')
    $completed = $memoryProcess.WaitForExit(10000)
    if (-not $completed) { [BoundedJob]::Terminate($memoryJob, 125); $memoryProcess.WaitForExit(3000) }
    $status = if (Test-Path -LiteralPath $statusFile) { [System.IO.File]::ReadAllText($statusFile) } else { 'NO_STATUS' }
    $limited = $status -match '^LIMIT:[0-7]$'
    Add-Result 'Bounded per-job memory limit' ($completed -and $limited) "Job cap=128 MiB; allocation ceiling=256 MiB; worker status=$status; completed=$completed."
} catch { Add-Result 'Bounded per-job memory limit' $false $_.Exception.Message }
finally {
    if ($memoryJob -ne [IntPtr]::Zero) { try { [BoundedJob]::Close($memoryJob) } catch {} }
    if ($memoryProcess -and -not $memoryProcess.HasExited) { Stop-Process -Id $memoryProcess.Id -Force -ErrorAction SilentlyContinue }
}

Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
$failed = @($results | Where-Object Result -ne 'PASS').Count
$form = New-Object System.Windows.Forms.Form
$form.Text = 'Windows Sandbox bounded-runner checks'
$form.Width = 1000; $form.Height = 420; $form.StartPosition = 'CenterScreen'
$box = New-Object System.Windows.Forms.TextBox
$box.Multiline = $true; $box.ReadOnly = $true; $box.ScrollBars = 'Vertical'; $box.Dock = 'Fill'
$box.Font = New-Object System.Drawing.Font('Consolas', 11)
$lines = @('Bounded execution fixture results', "Run time: $(Get-Date -Format o)", 'Networking/clipboard disabled; no mapped folders; Protected Client enabled; VM memory cap 2048 MB.', 'Job-object caps: 256 MiB for process-tree test; 128 MiB for bounded allocation test.', '')
foreach ($r in $results) { $lines += ('[{0}] {1}: {2}' -f $r.Result, $r.Test, $r.Detail) }
$lines += ''; $lines += "Summary: $(@($results).Count - $failed) PASS; $failed FAIL."
$lines += 'These fixtures do not execute generated solvers and are not yet integrated with the pilot executor.'
$box.Text = $lines -join [Environment]::NewLine
$form.Controls.Add($box)
[void]$form.ShowDialog()
