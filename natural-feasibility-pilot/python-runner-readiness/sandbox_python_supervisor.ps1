param([string]$Nonce, [int]$TimeoutSeconds = 8, [int]$OutputCap = 65536)
$ErrorActionPreference = 'Stop'
$native = @'
using System;
using System.IO;
using System.Runtime.InteropServices;
public static class PythonPilotJob {
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
public static class PythonPilotDrain {
 public sealed class Result { public byte[] Bytes; public bool Overflow; }
 public static Result Read(Stream input,int cap) { var r=new Result(); using(var m=new MemoryStream()) { var b=new byte[4096]; int n; long total=0; while((n=input.Read(b,0,b.Length))>0) { total+=n; int keep=(int)Math.Max(0,Math.Min(n,cap+1-m.Length)); if(keep>0)m.Write(b,0,keep); if(total>cap)r.Overflow=true; } r.Bytes=m.ToArray(); } return r; }
 public static System.Threading.Tasks.Task<Result> ReadAsync(Stream s,int cap) { return System.Threading.Tasks.Task.Factory.StartNew(() => Read(s,cap),System.Threading.CancellationToken.None,System.Threading.Tasks.TaskCreationOptions.LongRunning,System.Threading.Tasks.TaskScheduler.Default); }
}
'@
Add-Type -TypeDefinition $native -Language CSharp
$inputPath = 'C:\fc-input\current-input.json'
$workerPath = 'C:\fc-input\python_worker_fixture.py'
$pythonPath = 'C:\fc-python\python.exe'
$outDir = 'C:\fc-output'
$childPidFile = Join-Path $env:TEMP 'fc-python-child.pid'
$modes = @('normal','access','forge','malformed','oversized','crash','timeout_tree','memory')
$cases = [System.Collections.Generic.List[object]]::new()
$request = Get-Content -LiteralPath $inputPath -Raw | ConvertFrom-Json
$stdinJson = $request | ConvertTo-Json -Compress
$stdinWire = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($stdinJson)) + "`n"
foreach ($mode in $modes) {
    Remove-Item -LiteralPath $childPidFile -Force -ErrorAction SilentlyContinue
    $env:PYTHONHOME='C:\fc-python'; $env:PYTHONPATH=''; $env:PYTHONNOUSERSITE='1'; $env:FC_CHILD_PID_FILE=$childPidFile
    $start=[Diagnostics.ProcessStartInfo]::new(); $start.FileName=$pythonPath
    $start.Arguments='-I -S "' + $workerPath + '" ' + $mode
    $start.UseShellExecute=$false; $start.CreateNoWindow=$true; $start.RedirectStandardInput=$true; $start.RedirectStandardOutput=$true; $start.RedirectStandardError=$true
    $proc=[Diagnostics.Process]::new(); $proc.StartInfo=$start; $job=[IntPtr]::Zero; $read=$null; $errRead=$null
    $stdout=[byte[]]@(); $stderr=[byte[]]@(); $overflow=$false; $timedOut=$false; $exit=$null; $treeGone=$true; $childPid=0; $status='complete'
    try {
        if (-not $proc.Start()) { throw 'Python fixture did not start' }
        $job=[PythonPilotJob]::Create(128MB); [PythonPilotJob]::Assign($job,$proc.Id)
        $read=[PythonPilotDrain]::ReadAsync($proc.StandardOutput.BaseStream,$OutputCap)
        $errRead=[PythonPilotDrain]::ReadAsync($proc.StandardError.BaseStream,16384)
        $stdinBytes=[Text.Encoding]::ASCII.GetBytes($stdinWire)
        $proc.StandardInput.BaseStream.Write($stdinBytes,0,$stdinBytes.Length); $proc.StandardInput.BaseStream.Flush(); $proc.StandardInput.Close()
        $limit=if($mode -eq 'timeout_tree'){1200}else{$TimeoutSeconds*1000}
        if(-not $proc.WaitForExit($limit)) { $timedOut=$true; $status='timeout'; [PythonPilotJob]::Kill($job); $proc.WaitForExit(5000)|Out-Null }
        if($proc.HasExited){$exit=$proc.ExitCode}
        if($read.Wait(5000)){$stdout=$read.Result.Bytes;$overflow=$read.Result.Overflow}else{[PythonPilotJob]::Kill($job);$timedOut=$true;$status='timeout'}
        if($errRead.Wait(5000)){$stderr=$errRead.Result.Bytes}else{[PythonPilotJob]::Kill($job);$timedOut=$true;$status='timeout'}
        if($overflow){$status='overflow';$stdout=[byte[]]@()}elseif(-not $timedOut -and $exit -ne 0){$status='crash'}
        [PythonPilotJob]::Kill($job)
        if(Test-Path -LiteralPath $childPidFile){[int]::TryParse((Get-Content -LiteralPath $childPidFile -Raw),[ref]$childPid)|Out-Null}
        if($childPid){$treeGone=-not [bool](Get-Process -Id $childPid -ErrorAction SilentlyContinue)}
        if(-not $treeGone){throw "Python descendant $childPid survived job termination"}
        $cases.Add([ordered]@{mode=$mode;status=$status;exit_code=$exit;timed_out=$timedOut;stdout_b64=[Convert]::ToBase64String($stdout);stderr_b64=[Convert]::ToBase64String($stderr);overflow=$overflow;child_pid=$childPid;tree_terminated=$treeGone})
    } finally { if($job -ne [IntPtr]::Zero){[PythonPilotJob]::Close($job)}; if($proc -and -not $proc.HasExited){try{$proc.Kill()}catch{}}; $proc.Dispose() }
}
$before=@(Get-ChildItem -LiteralPath $outDir -Force | Select-Object -ExpandProperty Name)
$capture=[ordered]@{schema=1;nonce=$Nonce;cases=@($cases);worker_visible_output_entries=$before;input_wire_debug=$stdinWire;input_json_debug=$stdinJson}
[IO.File]::WriteAllText((Join-Path $outDir 'python-capture.json'),($capture|ConvertTo-Json -Depth 6 -Compress),[Text.UTF8Encoding]::new($false))
shutdown.exe /s /t 2 /f | Out-Null
