@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64
set CBMCBIN=C:\Users\pakla\AppData\Local\Programs\cbmc\bin
set MODEL=C:\Users\pakla\PycharmProjects\failure-concentration-study\rlc0\model
set HARNESS=C:\Users\pakla\PycharmProjects\failure-concentration-study\rlc0\harness
set WS=C:\Users\pakla\AppData\Local\Temp\opencode\rlc0-c2
cd /d %WS%

echo ==== build probe_domain
%CBMCBIN%\goto-cl.exe /nologo /std:c++17 /EHsc /I"%MODEL%" /I"%HARNESS%" probe_domain.cpp
echo exit: %ERRORLEVEL%
if not exist probe_domain.exe (echo PROBE_DOMAIN COMPILE FAILED)

for %%C in (n63 large) do (
  for %%O in (IN_F D_F FULL_D) do (
    echo ==== build %%C %%O
    if exist proof_main.exe del /q proof_main.exe
    if exist "%HARNESS%\proof_main.exe" del /q "%HARNESS%\proof_main.exe"
    %CBMCBIN%\goto-cl.exe /nologo /std:c++17 /EHsc /I"%MODEL%" /I"%HARNESS%" /DRLC0_SOLVER_HEADER=canary_%%C.h /DOBL_%%O "%HARNESS%\proof_main.cpp"
    echo exit: %ERRORLEVEL%
    if exist proof_main.exe (
      copy /y proof_main.exe canary_%%C_%%O.exe >nul & echo built canary_%%C_%%O.exe
    ) else if exist "%HARNESS%\proof_main.exe" (
      copy /y "%HARNESS%\proof_main.exe" canary_%%C_%%O.exe >nul & echo built canary_%%C_%%O.exe from harness dir & del /q "%HARNESS%\proof_main.exe"
    ) else (
      echo BUILD FAILED %%C %%O
    )
  )
)

echo ==== show-loops (FULL_D binary)
%CBMCBIN%\cbmc.exe canary_n63_FULL_D.exe --show-loops
echo show-loops exit: %ERRORLEVEL%
