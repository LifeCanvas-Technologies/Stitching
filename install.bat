cd /D "%~dp0"

@echo off
echo Copy the 'terastitcher' directory to the C: drive and add 'C:\terastitcher' to the PATH environment variable, then press any key to continue.
pause
echo Download and run the BioFormats installer at: https://github.com/imaris/ImarisConvertBioformats, then press any key to continue.
pause

start /wait msmpisetup.exe
start /wait VC_redist.x64.exe
start /wait vcredist_x64.exe
start /wait .\LVRTE2017SP1_f4Patch-64std\setup.exe
start /wait ni-vision-runtime_20.7_online.exe

call conda env remove -n stitching
call conda env remove -p C:\ProgramData\Anaconda3\envs\stitching

call conda create -p C:\ProgramData\Anaconda3\envs\stitching python=3.8
icacls C:\ProgramData\Anaconda3\envs\stitching /grant Everyone:(RX) /T

call conda activate stitching

call pip install -r Requirements.txt

call pip install zetastitcher cvxpy==1.1.18 qpsolvers==1.8.0 quadprog==0.1.11

call pip install pystripe

@echo off

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set WshShell = CreateObject("Wscript.shell") >> %SCRIPT%
echo Set oLink = WshShell.CreateShortcut("C:\Users\Public\Desktop\Stitch_GUI.lnk") >> %SCRIPT%
echo oLink.TargetPath = "%~dp0Stitch GUI\StitchGUI.exe" >> %SCRIPT%
@REM echo oLink.IconLocation = "%~dp0destripegui\data\lct.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript %SCRIPT%
del %SCRIPT%
pause
