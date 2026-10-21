param([string]$CaseId = 'zero', [string]$FailureIds = '', [string]$FixtureMode = 'normal', [string]$Nonce = '', [int]$ProbeLimit = 30)
$ErrorActionPreference = 'Stop'
trap {
    try { [IO.File]::WriteAllText((Join-Path $env:USERPROFILE 'Desktop\pilot-output\guest-error.txt'), (($_ | Format-List * -Force | Out-String) + $_.Exception.ToString()), [Text.UTF8Encoding]::new($false)) } catch {}
    shutdown.exe /s /t 2 /f | Out-Null
    break
}

$native = @'
using System;
using System.IO;
using System.Runtime.InteropServices;
public static class PilotJob {
 [StructLayout(LayoutKind.Sequential)] public struct Basic { public long A,B; public uint Flags; public UIntPtr C,D; public uint E; public UIntPtr F; public uint G,H; }
 [StructLayout(LayoutKind.Sequential)] public struct Io { public ulong A,B,C,D,E,F; }
 [StructLayout(LayoutKind.Sequential)] public struct Extended { public Basic BasicInfo; public Io IoInfo; public UIntPtr ProcessLimit,JobLimit,PeakProcess,PeakJob; }
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr CreateJobObject(IntPtr a,string n);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool SetInformationJobObject(IntPtr j,int c,IntPtr p,uint n);
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr OpenProcess(uint a,bool i,uint p);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool AssignProcessToJobObject(IntPtr j,IntPtr p);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool TerminateJobObject(IntPtr j,uint c);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool CloseHandle(IntPtr h);
 public static IntPtr Create(ulong memory) { var j=CreateJobObject(IntPtr.Zero,null); var x=new Extended(); x.BasicInfo.Flags=0x200|0x2000; x.JobLimit=new UIntPtr(memory); var p=Marshal.AllocHGlobal(Marshal.SizeOf(typeof(Extended))); try { Marshal.StructureToPtr(x,p,false); if(!SetInformationJobObject(j,9,p,(uint)Marshal.SizeOf(typeof(Extended)))) throw new System.ComponentModel.Win32Exception(); } finally { Marshal.FreeHGlobal(p); } return j; }
 public static void Assign(IntPtr j,int id) { var p=OpenProcess(0x100|1,false,(uint)id); if(p==IntPtr.Zero) throw new System.ComponentModel.Win32Exception(); try { if(!AssignProcessToJobObject(j,p)) throw new System.ComponentModel.Win32Exception(); } finally { CloseHandle(p); } }
 public static void Kill(IntPtr j) { if(!TerminateJobObject(j,124)) throw new System.ComponentModel.Win32Exception(); }
 public static void Close(IntPtr j) { if(j!=IntPtr.Zero) CloseHandle(j); }
}
public static class PilotDrain {
 public sealed class Result { public byte[] Bytes; public bool Overflow; }
 public static Result Read(Stream input,int cap) { var result=new Result(); using(var ms=new MemoryStream()) { var b=new byte[4096]; int n; long total=0; while((n=input.Read(b,0,b.Length))>0) { total+=n; int keep=(int)Math.Max(0,Math.Min(n,cap+1-ms.Length)); if(keep>0) ms.Write(b,0,keep); if(total>cap) result.Overflow=true; } result.Bytes=ms.ToArray(); } return result; }
 public static System.Threading.Tasks.Task<Result> ReadAsync(Stream input,int cap) { return System.Threading.Tasks.Task.Factory.StartNew(() => Read(input,cap), System.Threading.CancellationToken.None, System.Threading.Tasks.TaskCreationOptions.LongRunning, System.Threading.Tasks.TaskScheduler.Default); }
}
'@
Add-Type -TypeDefinition $native -Language CSharp

$desktop = Join-Path $env:USERPROFILE 'Desktop\pilot-input'
$outDir = Join-Path $env:USERPROFILE 'Desktop\pilot-output'
$battery = Get-Content -LiteralPath (Join-Path $desktop 'diagnostic_battery.json') -Raw | ConvertFrom-Json
$failureSet = @{}; if ($FailureIds) { foreach ($id in $FailureIds.Split(',')) { $failureSet[$id]=$true } }
$worker = Join-Path $desktop 'sandbox_worker_fixture.ps1'
$powershell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$rows = [System.Collections.Generic.List[object]]::new()

foreach ($probe in @($battery | Select-Object -First $ProbeLimit)) {
    $mode = 'normal'
    if ($FixtureMode -ne 'normal' -and $probe.probe_id -eq 'F1_0') { $mode=$FixtureMode }
    $args = @('-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',('"' + $worker + '"'),'-Mode',$mode)
    if ($failureSet.ContainsKey($probe.probe_id)) { $args += '-InjectFailure' }
    if ($mode -eq 'unexpected') { $args += @('-OutputDir',('"' + $outDir + '"')) }
    $start = [Diagnostics.ProcessStartInfo]::new(); $start.FileName=$powershell; $start.Arguments=$args -join ' '
    $start.UseShellExecute=$false; $start.CreateNoWindow=$true; $start.RedirectStandardInput=$true; $start.RedirectStandardOutput=$true; $start.RedirectStandardError=$true
    $proc=[Diagnostics.Process]::new(); $proc.StartInfo=$start
    $job=[IntPtr]::Zero; $reader=$null; $errorReader=$null; $bytes=[byte[]]@(); $errorBytes=[byte[]]@(); $overflow=$false; $timedOut=$false; $exit=$null; $status='complete'; $treeTerminated=$false
    $childPidFile=Join-Path $env:TEMP 'pilot-child.pid'; Remove-Item -LiteralPath $childPidFile -Force -ErrorAction SilentlyContinue
    try {
        if (-not $proc.Start()) { throw 'worker process did not start' }
        $job=[PilotJob]::Create(128MB); [PilotJob]::Assign($job,$proc.Id)
        $reader=[PilotDrain]::ReadAsync($proc.StandardOutput.BaseStream,65536)
        $errorReader=[PilotDrain]::ReadAsync($proc.StandardError.BaseStream,16384)
        $request = [ordered]@{n=[int]$probe.input.n;edges=$probe.input.edges;s=[int]$probe.input.s;t=[int]$probe.input.t} | ConvertTo-Json -Compress -Depth 8
        $wire = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($request))
        $wireBytes=[Text.Encoding]::ASCII.GetBytes($wire + "`n")
        $proc.StandardInput.BaseStream.Write($wireBytes,0,$wireBytes.Length); $proc.StandardInput.BaseStream.Flush(); $proc.StandardInput.Close()
        $waitMs = if ($mode -eq 'timeout') { 1200 } else { 10000 }
        $finished=$proc.WaitForExit($waitMs)
        if (-not $finished) { $timedOut=$true; $status='timeout'; [PilotJob]::Kill($job); $proc.WaitForExit(5000) | Out-Null }
        if ($proc.HasExited) { $exit=$proc.ExitCode }
        if ($reader.Wait(5000)) { $bytes=$reader.Result.Bytes; $overflow=$reader.Result.Overflow } else { [PilotJob]::Kill($job); $status='timeout'; $timedOut=$true }
        if ($errorReader.Wait(5000)) { $errorBytes=$errorReader.Result.Bytes } else { [PilotJob]::Kill($job); $status='timeout'; $timedOut=$true }
        if ($overflow) { $status='overflow'; $bytes=[byte[]]@() }
        elseif (-not $timedOut -and $exit -ne 0) { $status='crash' }
        if ($job -ne [IntPtr]::Zero) { [PilotJob]::Kill($job) }
        $childPid=0
        if (Test-Path -LiteralPath $childPidFile) { [int]::TryParse((Get-Content -LiteralPath $childPidFile -Raw),[ref]$childPid) | Out-Null }
        $treeTerminated=($childPid -eq 0 -or -not [bool](Get-Process -Id $childPid -ErrorAction SilentlyContinue))
        if (-not $treeTerminated) { throw "worker descendant $childPid remained alive" }
        $rows.Add([ordered]@{probe_id=$probe.probe_id;status=$status;exit_code=$exit;timed_out=$timedOut;tree_terminated=$treeTerminated;stdout_b64=[Convert]::ToBase64String($bytes);stderr_b64=[Convert]::ToBase64String($errorBytes)})
    } finally {
        if ($job -ne [IntPtr]::Zero) { [PilotJob]::Close($job) }
        if ($proc -and -not $proc.HasExited) { try { $proc.Kill() } catch {} }
        $proc.Dispose()
    }
}

$capture=[ordered]@{schema=1;nonce=$Nonce;case_id=$CaseId;probe_rows=@($rows)}
$dest=Join-Path $outDir 'capture.json'
[IO.File]::WriteAllText($dest,($capture | ConvertTo-Json -Depth 8 -Compress),[Text.UTF8Encoding]::new($false))
shutdown.exe /s /t 2 /f | Out-Null
