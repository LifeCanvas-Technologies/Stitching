title StitchMerge

:: Locations of things
::
set TERASTITCHER=C:\terastitcher\terastitcher
set Parastitcher=C:\terastitcher\Parastitcher.py


:: Set active directory to path of batch file parent folder
cd /d %~dp0

SET WORKINGDIR=%CD%
for %%* in (.) do SET DIRNAME=%%~n*
SET OUTPUTDIR=%DIRNAME%_stitched

:: Create output directory and Validate the creation
mkdir "..\%OUTPUTDIR%"
if exist "..\%OUTPUTDIR%\" (
    echo Folder "..\%OUTPUTDIR%" created successfully.
    pause
) else (
    echo ERROR: Failed to create folder "%folder%".
    pause
    exit /b 1
)


call activate base
:: ECHO CURRENT_DIR: "%CD%"

mpiexec -np 12 python %Parastitcher% -6 --projin=.\xml_merging.xml --volout="..\%OUTPUTDIR%" --volout_plugin="TiledXY|2Dseries" --slicewidth=100000 --sliceheight=150000 

ECHO Done! DONE!

NAS

:: Change directory
cd "..\%OUTPUTDIR%"
:: Error out if cd failed
if errorlevel 1 (
    echo ERROR: Failed to change directory to "..\%OUTPUTDIR%".
    pause
    exit /b 1
)

powershell -command "& {&'Get-ChildItem' -Path '.\*_*.tif*' -Recurse | Move-Item -Destination '.\' " }"

:: Append excitation wavelength to stitched image file names
set wavelength=%OUTPUTDIR:~7,3%

:: Run the PowerShell command
powershell -command "& { $wavelength = '%wavelength%'; Get-ChildItem -Path '.\*.tif*' | ForEach-Object { $newName = $_.BaseName + '_' + $wavelength + $_.Extension; Rename-Item -Path $_.FullName -NewName $newName } }"

:: Create an empty file with the dimension info, in the parent directory
for /f %%D in ('dir /b ".\RES*"') do set "dim_dir_name=%%D"
echo. > %CD%\..\"%OUTPUTDIR%_%dim_dir_name%"
echo Created empty file: %CD%\..\%dim_dir_name%
:: remove *_MIDDLE/MIP_*_RES* files
powershell -command "Remove-Item %CD%\..\*MIDDLE*RES*"
powershell -command "Remove-Item %CD%\..\*MIP*RES*"

:: wait for 1 second before deleting the folder
timeout /t 1 /nobreak >nul
:: Remove RES folder
powershell -command "Remove-Item -Recurse %CD%\RES*"

:: INTERNAL USE
:: Write a json file containing channel and directory information
for /f %%A in ('dir /b *.tif* ^| find /c /v ""') do set "file_count=%%A"
echo Current directory: %OUTPUTDIR%
echo Number of files: %file_count%

:: Write to a JSON file
set "json_file=%CD%\..\pp_log.json"
set PPLogger=C:\terastitcher\update_pp_log.py
python "%PPLogger%" "%WORKINGDIR%" "%DIRNAME%" "%OUTPUTDIR%" "%file_count%" "%json_file%"
echo JSON entry updated to: %json_file%

exit