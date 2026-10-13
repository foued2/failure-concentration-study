@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64
set CBMCBIN=C:\Users\pakla\AppData\Local\Programs\cbmc\bin
cd /d C:\Users\pakla\AppData\Local\Temp\opencode\rlc0-c2
del /q probe_v1.exe probe_c.exe 2>nul

echo ============ probe_v1 compile (C++, pre-declared quantifier variable)
%CBMCBIN%\goto-cl.exe /nologo /std:c++17 /EHsc probe_v1.cpp
echo goto-cl exit: %ERRORLEVEL%

echo ============ probe_c compile (C mode, declaration-form quantifier)
%CBMCBIN%\goto-cl.exe /nologo probe_c.c
echo goto-cl exit: %ERRORLEVEL%
:end
