param([string]$Nonce, [string]$CaseId, [int]$TimeoutMs = 10000, [int]$OutputCap = 65536)
$ErrorActionPreference = 'Stop'
trap {
    try { [IO.File]::WriteAllText('C:\fc-output\guest-error.txt', (($_ | Format-List * -Force | Out-String) + $_.Exception.ToString()), [Text.UTF8Encoding]::new($false)) } catch {}
    shutdown.exe /s /t 2 /f | Out-Null
    break
}
$native = @'
using System;
using System.IO;
using System.Runtime.InteropServices;
public static class SuitePilotJob {
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
public static class SuitePilotDrain {
 public sealed class Result { public byte[] Bytes; public bool Overflow; }
 public static Result Read(Stream input,int cap) { var r=new Result(); using(var m=new MemoryStream()) { var b=new byte[4096]; int n; long total=0; while((n=input.Read(b,0,b.Length))>0) { total+=n; int keep=(int)Math.Max(0,Math.Min(n,cap+1-m.Length)); if(keep>0)m.Write(b,0,keep); if(total>cap)r.Overflow=true; } r.Bytes=m.ToArray(); } return r; }
 public static System.Threading.Tasks.Task<Result> ReadAsync(Stream s,int cap) { return System.Threading.Tasks.Task.Factory.StartNew(() => Read(s,cap),System.Threading.CancellationToken.None,System.Threading.Tasks.TaskCreationOptions.LongRunning,System.Threading.Tasks.TaskScheduler.Default); }
}
'@
Add-Type -TypeDefinition $native -Language CSharp
$inputDir='C:\fc-input'; $outDir='C:\fc-output'; $python='C:\fc-python\python.exe'; $adapter='C:\fc-runner\python_adapter.py'
$suite=Get-Content -LiteralPath (Join-Path $inputDir 'suite.json') -Raw | ConvertFrom-Json -ErrorAction Stop
if(-not $suite.requests -or $suite.requests.Count -lt 1){throw 'suite has no requests'}
$rows=[System.Collections.Generic.List[object]]::new()
foreach($request in $suite.requests) {
    $clock=[Diagnostics.Stopwatch]::StartNew()
    $start=[Diagnostics.ProcessStartInfo]::new(); $start.FileName=$python; $start.Arguments='-I -S "'+$adapter+'"'; $start.UseShellExecute=$false; $start.CreateNoWindow=$true; $start.RedirectStandardInput=$true; $start.RedirectStandardOutput=$true; $start.RedirectStandardError=$true
    $env:PYTHONHOME='C:\fc-python'; $env:PYTHONPATH=''; $env:PYTHONNOUSERSITE='1'
    $proc=[Diagnostics.Process]::new(); $proc.StartInfo=$start; $job=[IntPtr]::Zero; $outRead=$null; $errRead=$null
    $stdout=[byte[]]@(); $stderr=[byte[]]@(); $overflow=$false; $timeout=$false; $exit=$null; $status='complete'; $treeTerminated=$false
    try {
        if(-not $proc.Start()){throw 'Python worker failed to start'}
        $job=[SuitePilotJob]::Create(128MB); [SuitePilotJob]::Assign($job,$proc.Id)
        $outRead=[SuitePilotDrain]::ReadAsync($proc.StandardOutput.BaseStream,$OutputCap); $errRead=[SuitePilotDrain]::ReadAsync($proc.StandardError.BaseStream,16384)
        $wireJson=[ordered]@{mode='normal';input=$request.input}|ConvertTo-Json -Compress -Depth 12
        $wire=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($wireJson))+"`n"; $bytes=[Text.Encoding]::ASCII.GetBytes($wire)
        $proc.StandardInput.BaseStream.Write($bytes,0,$bytes.Length); $proc.StandardInput.BaseStream.Flush(); $proc.StandardInput.Close()
        if(-not $proc.WaitForExit($TimeoutMs)){$timeout=$true;$status='timeout';[SuitePilotJob]::Kill($job);$proc.WaitForExit(5000)|Out-Null}
        if($proc.HasExited){$exit=$proc.ExitCode}
        if($outRead.Wait(5000)){$stdout=$outRead.Result.Bytes;$overflow=$outRead.Result.Overflow}else{$timeout=$true;$status='timeout'}
        if($errRead.Wait(5000)){$stderr=$errRead.Result.Bytes}else{$timeout=$true;$status='timeout'}
        if($overflow){$status='overflow'}elseif($timeout){$status='timeout'}elseif($exit -ne 0){$status='crash'}
        [SuitePilotJob]::Kill($job); $treeTerminated=$true
        $rows.Add([ordered]@{probe_id=[string]$request.probe_id;status=$status;exit_code=$exit;timed_out=$timeout;tree_terminated=$treeTerminated;stdout_b64=[Convert]::ToBase64String($stdout);stderr_b64=[Convert]::ToBase64String($stderr);elapsed_ms=[long]$clock.ElapsedMilliseconds})
    } finally {if($job -ne [IntPtr]::Zero){[SuitePilotJob]::Close($job)};if($proc -and -not $proc.HasExited){try{$proc.Kill()}catch{}};$proc.Dispose()}
}
$capture=[ordered]@{schema=1;nonce=$Nonce;case_id=$CaseId;probe_rows=@($rows)}
[IO.File]::WriteAllText((Join-Path $outDir 'capture.json'),($capture|ConvertTo-Json -Depth 6 -Compress),[Text.UTF8Encoding]::new($false))
shutdown.exe /s /t 2 /f | Out-Null
