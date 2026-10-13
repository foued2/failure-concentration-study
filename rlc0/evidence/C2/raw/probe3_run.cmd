@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64
set CBMCBIN=C:\Users\pakla\AppData\Local\Programs\cbmc\bin
cd /d C:\Users\pakla\AppData\Local\Temp\opencode\rlc0-c2
for %%f in (qa.c qb.c qc.c qd.cpp) do (
  echo ============ compile %%f
  %CBMCBIN%\goto-cl.exe /nologo /std:c++17 /EHsc %%f
  echo goto-cl exit: %ERRORLEVEL%
)
