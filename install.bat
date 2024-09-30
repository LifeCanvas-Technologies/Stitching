@echo off
echo Create an empty 'c:/terastitcher' folder if it doesn't exist.  Add 'c:/terastitcher' to path.
pause

del /s /f /q c:\terastitcher\*.*
for /f %%f in ('dir /ad /b c:\terastitcher\') do rd /s /q c:\terastitcher\%%f
echo f | xcopy /s /e /q ".\terastitcher" "C:\terastitcher"
pause

start /wait msmpisetup.exe
start /wait VC_redist.x64.exe
start /wait vcredist_x64.exe
start /wait .\LVRTE2017SP1_f4Patch-64std\setup.exe
start /wait ni-vision-runtime_20.7_online.exe

call conda env remove -n stitching

call conda create -n stitching python=3.8

call conda activate stitching

call pip install -r Requirements.txt

call pip install zetastitcher cvxpy==1.1.18 qpsolvers==1.8.0 quadprog==0.1.11

call pip install pystripe

@echo off

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set WshShell = CreateObject("Wscript.shell") >> %SCRIPT%
echo Set oLink = WshShell.CreateShortcut("%USERPROFILE%\Desktop\Stitch_GUI.lnk") >> %SCRIPT%
echo oLink.TargetPath = "%~dp0Stitch GUI\StitchGUI.exe" >> %SCRIPT%
@REM echo oLink.IconLocation = "%~dp0destripegui\data\lct.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript %SCRIPT%
del %SCRIPT%
pause
