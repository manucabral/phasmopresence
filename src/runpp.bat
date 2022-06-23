@echo off
echo Executing PhasmoPresence.exe ..
Pushd "%~dp0"
start PhasmoPresence.exe
popd
echo PhasmoPresence.exe executed!
echo Executing Phasmophobia.exe ..
timeout /t 3 /nobreak > NUL
start C:\"Program Files (x86)"\Steam\steamapps\common\Phasmophobia\Phasmophobia.exe
echo Executed Phasmophobia.exe!
pause