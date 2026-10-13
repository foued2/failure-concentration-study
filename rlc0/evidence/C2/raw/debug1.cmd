@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64 >nul
set CBMCBIN=C:\Users\pakla\AppData\Local\Programs\cbmc\bin
set MODEL=C:\Users\pakla\PycharmProjects\failure-concentration-study\rlc0\model
set HARNESS=C:\Users\pakla\PycharmProjects\failure-concentration-study\rlc0\harness
cd /d C:\Users\pakla\AppData\Local\Temp\opencode\rlc0-c2

echo ==== T1 bare proof_main.cpp
%CBMCBIN%\goto-cl.exe /nologo /std:c++17 /EHsc /I"%MODEL%" /I"%HARNESS%" proof_main.cpp
echo exit: %ERRORLEVEL%

echo ==== T2 with OBL only
%CBMCBIN%\goto-cl.exe /nologo /std:c++17 /EHsc /I"%MODEL%" /I"%HARNESS%" /DOBL_IN_F proof_main.cpp
echo exit: %ERRORLEVEL%

echo ==== T3 with SOLVER_HEADER only
%CBMCBIN%\goto-cl.exe /nologo /std:c++17 /EHsc /I"%MODEL%" /I"%HARNESS%" /DRLC0_SOLVER_HEADER=canary_n63.h proof_main.cpp
echo exit: %ERRORLEVEL%
