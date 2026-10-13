@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64 >nul
set CBMCBIN=C:\Users\pakla\AppData\Local\Programs\cbmc\bin
set MODEL=C:\Users\pakla\PycharmProjects\failure-concentration-study\rlc0\model
set HARNESS=C:\Users\pakla\PycharmProjects\failure-concentration-study\rlc0\harness
set WS=C:\Users\pakla\AppData\Local\Temp\opencode\rlc0-c2
set UWS="rlc0_build(ptr_struct_tag(identifier=tag-rlc0_input)).0:10001"
cd /d %WS%
if not exist logs mkdir logs

echo ==== rebuild probe_domain
%CBMCBIN%\goto-cl.exe /nologo /std:c++17 /EHsc /I"%MODEL%" /I"%HARNESS%" probe_domain.cpp
echo exit: %ERRORLEVEL%

echo ==== probe_domain START %TIME%
%CBMCBIN%\cbmc.exe probe_domain.exe --function main --unwind 64 --unwindset %UWS% --unwinding-assertions --bounds-check --pointer-check > logs\cbmc_domain.txt 2>&1
echo probe_domain exit: %ERRORLEVEL% END %TIME%

for %%C in (n63 large) do (
  for %%O in (IN_F D_F FULL_D) do (
    echo ==== canary_%%C_%%O START %TIME%
    %CBMCBIN%\cbmc.exe canary_%%C_%%O.exe --function main --unwind 64 --unwindset %UWS% --unwinding-assertions --bounds-check --pointer-check > logs\cbmc_canary_%%C_%%O.txt 2>&1
    echo canary_%%C_%%O exit: %ERRORLEVEL% END %TIME%
  )
)
echo ALL DONE %TIME%
