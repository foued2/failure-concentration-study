@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64 >nul
set CBMCBIN=C:\Users\pakla\AppData\Local\Programs\cbmc\bin
cd /d C:\Users\pakla\AppData\Local\Temp\opencode\rlc0-c2

echo ==== probe_domain cbmc (property list)
%CBMCBIN%\cbmc.exe probe_domain.exe --function main --unwind 64 --unwindset "rlc0_build(ptr_struct_tag(identifier=tag-rlc0_input)).0:10001" --unwinding-assertions --bounds-check --pointer-check
echo cbmc exit: %ERRORLEVEL%
