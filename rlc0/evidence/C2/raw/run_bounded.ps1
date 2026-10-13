param(
  [Parameter(Mandatory=$true)][string]$Label,
  [Parameter(Mandatory=$true)][string]$FilePath,
  [Parameter(Mandatory=$true)][string]$Args,
  [Parameter(Mandatory=$true)][string]$OutFile,
  [int]$WallSec = 1800,
  [long]$MemBytes = 8589934592,
  [int]$PollMs = 250,
  [string]$WorkDir = ""
)
# Bounded runner v5.1: kernel-enforced memory budget via Windows job object
# (JOB_OBJECT_LIMIT_PROCESS_MEMORY, built in C# to avoid PowerShell nested-struct
# copy pitfalls) + wall-clock watchdog polling. Job created BEFORE process start;
# assignment immediately after start (cbmc runs are long-lived, race is irrelevant).
# Child OOM under the job limit surfaces as the child's own failure (cbmc prints
# "SAT checker ran out of memory" -> VERIFICATION ERROR = properties ERROR =
# INCOMPLETE, never SUCCESS); wall breach = taskkill tree.
# Raw stdout -> $OutFile, raw stderr -> "$OutFile.err.txt", status -> "$OutFile.status.txt".
# Outcome: COMPLETED | WALL_TIMEOUT. Exit: 0 = completed+joblimit armed,
# 2 = wall timeout, 3 = completed but job limit could NOT be armed (flag for review).

$ErrorActionPreference = "Stop"
$statusFile = "$OutFile.status.txt"
$errFile = "$OutFile.err.txt"

if (-not ("RLC0.JobLimit" -as [type])) {
  Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
namespace RLC0 {
  public static class JobLimit {
    [StructLayout(LayoutKind.Sequential)]
    public struct IO_COUNTERS {
      public ulong ReadOperationCount, WriteOperationCount, OtherOperationCount,
                   ReadTransferCount, WriteTransferCount, OtherTransferCount;
    }
    [StructLayout(LayoutKind.Sequential)]
    public struct JOBOBJECT_BASIC_LIMIT_INFORMATION {
      public long PerProcessUserTimeLimit, PerJobUserTimeLimit;
      public uint LimitFlags;
      public UIntPtr MinimumWorkingSetSize, MaximumWorkingSetSize;
      public uint ActiveProcessLimit;
      public UIntPtr Affinity;
      public uint PriorityClass, SchedulingClass;
    }
    [StructLayout(LayoutKind.Sequential)]
    public struct JOBOBJECT_EXTENDED_LIMIT_INFORMATION {
      public JOBOBJECT_BASIC_LIMIT_INFORMATION BasicLimitInformation;
      public IO_COUNTERS IoInfo;
      public UIntPtr ProcessMemoryLimit;
      public UIntPtr JobMemoryLimit;
      public UIntPtr PeakProcessMemoryUsed;
      public UIntPtr PeakJobMemoryUsed;
    }
    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    public static extern IntPtr CreateJobObject(IntPtr lpJobAttributes, string lpName);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool SetInformationJobObject(IntPtr hJob, int infoClass,
        ref JOBOBJECT_EXTENDED_LIMIT_INFORMATION info, int cbLength);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool AssignProcessToJobObject(IntPtr hJob, IntPtr hProcess);
    public const int JobObjectExtendedLimitInformation = 9;
    public const uint JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x00000100;

    // Creates a job with a hard per-process commit limit. Returns IntPtr.Zero on failure.
    public static IntPtr CreateLimitedJob(ulong memBytes) {
      IntPtr h = CreateJobObject(IntPtr.Zero, null);
      if (h == IntPtr.Zero) return IntPtr.Zero;
      int size = Marshal.SizeOf(typeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION));
      if (size != 144) return IntPtr.Zero;   // x64 layout guard
      JOBOBJECT_EXTENDED_LIMIT_INFORMATION info = new JOBOBJECT_EXTENDED_LIMIT_INFORMATION();
      info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_PROCESS_MEMORY;
      info.ProcessMemoryLimit = (UIntPtr)memBytes;
      if (!SetInformationJobObject(h, JobObjectExtendedLimitInformation, ref info, size))
        return IntPtr.Zero;
      return h;
    }
    public static bool Assign(IntPtr job, IntPtr process) {
      return AssignProcessToJobObject(job, process);
    }
  }
}
"@
}

$start = Get-Date
$cmdLineStr = "$FilePath $Args"
Write-Output "[$(Get-Date -Format o)] START $Label  wall=${WallSec}s  mem=$((($MemBytes/1GB)))GB (job-object hard limit)"
Write-Output "CMD: $cmdLineStr"

$jobHandle = [RLC0.JobLimit]::CreateLimitedJob([System.UInt64]$MemBytes)
$jobUsable = ($jobHandle -ne [IntPtr]::Zero)

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $FilePath
$psi.Arguments = $Args
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
if ($WorkDir) { $psi.WorkingDirectory = $WorkDir }

$p = [System.Diagnostics.Process]::Start($psi)

$jobLimitApplied = $false
if ($jobUsable) {
  $jobLimitApplied = [RLC0.JobLimit]::Assign($jobHandle, $p.Handle)
}

$outTask = $p.StandardOutput.ReadToEndAsync()
$errTask = $p.StandardError.ReadToEndAsync()

$peakPriv = 0
$outcome = "COMPLETED"
$deadline = $start.AddSeconds($WallSec)

while (-not $p.HasExited) {
  Start-Sleep -Milliseconds $PollMs
  try {
    $p.Refresh()
    if ($p.PrivateMemorySize64 -gt $peakPriv) { $peakPriv = $p.PrivateMemorySize64 }
  } catch {}
  if ((Get-Date) -gt $deadline) { $outcome = "WALL_TIMEOUT"; break }
}

if ($outcome -ne "COMPLETED") {
  & taskkill.exe /PID $p.Id /T /F 2>&1 | Out-Null
  Start-Sleep -Seconds 2
  $exitCode = $null
  $stdoutText = ""; $stderrText = ""
  try { $stdoutText = $outTask.Result; $stderrText = $errTask.Result } catch {}
} else {
  $p.WaitForExit()
  $exitCode = $p.ExitCode
  $stdoutText = $outTask.Result
  $stderrText = $errTask.Result
}

[System.IO.File]::WriteAllText($OutFile, $stdoutText, [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllText($errFile, $stderrText, [System.Text.Encoding]::UTF8)

$end = Get-Date
$elapsed = ($end - $start).TotalSeconds
$lines = @(
  "label: $Label",
  "command: $cmdLineStr",
  "out_file: $OutFile",
  "err_file: $errFile",
  "start: $($start.ToString('o'))",
  "end: $($end.ToString('o'))",
  "elapsed_sec: $([math]::Round($elapsed,1))",
  "wall_budget_sec: $WallSec",
  "mem_budget_bytes: $MemBytes",
  "mem_enforcement: job_object($jobLimitApplied) poll_ms=$PollMs",
  "peak_private_bytes: $peakPriv",
  "outcome: $outcome",
  "exit_code: $exitCode",
  "note: COMPLETED = child exited naturally within budget; exit_code is cbmc raw exit (0 SUCCESS, 10 FAILED, 6/other see log; cbmc-internal SAT OOM prints 'SAT checker ran out of memory' and yields VERIFICATION ERROR = properties ERROR = INCOMPLETE, never SUCCESS). WALL_TIMEOUT = INCOMPLETE. exit 3 = job limit not armed (review)."
)
Set-Content -Path $statusFile -Value $lines -Encoding ASCII
Write-Output "[$(Get-Date -Format o)] END $Label  outcome=$outcome  exit=$exitCode  elapsed=$([math]::Round($elapsed,1))s  peakPriv=$([math]::Round($peakPriv/1MB,1))MB  jobLimit=$jobLimitApplied"
Write-Output "status: $statusFile"
if (-not $jobLimitApplied) { exit 3 }
if ($outcome -eq "COMPLETED") { exit 0 } else { exit 2 }
