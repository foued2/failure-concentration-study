@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64
set CBMCBIN=C:\Users\pakla\AppData\Local\Programs\cbmc\bin
set WS=C:\Users\pakla\AppData\Local\Temp\opencode\rlc0-c2
cd /d %WS%
del /q probe_q.exe probe_split.exe 2>nul

echo ============ probe_q compile
%CBMCBIN%\goto-cl.exe /nologo /std:c++17 /EHsc probe_q.cpp
echo goto-cl exit: %ERRORLEVEL%
if not exist probe_q.exe (echo PROBE_Q COMPILE FAILED & goto :split)
echo ============ probe_q cbmc
%CBMCBIN%\cbmc.exe probe_q.exe --function main --unwind 64 --unwinding-assertions --bounds-check --pointer-check
echo cbmc exit: %ERRORLEVEL%

:split
echo ============ probe_split compile
%CBMCBIN%\goto-cl.exe /nologo /std:c++17 /EHsc probe_split.cpp
echo goto-cl exit: %ERRORLEVEL%
if not exist probe_split.exe (echo PROBE_SPLIT COMPILE FAILED & goto :end)
echo ============ probe_split cbmc
%CBMCBIN%\cbmc.exe probe_split.exe --function main --unwind 64 --unwinding-assertions --bounds-check --pointer-check
echo cbmc exit: %ERRORLEVEL%
:end
