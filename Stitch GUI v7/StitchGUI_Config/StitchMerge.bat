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
if not exist "..\%OUTPUTDIR%" (
    echo ERROR: Failed to create directory "..\%OUTPUTDIR%".
    exit /b 1
)


call activate stitching


mpiexec -np 12 python %Parastitcher% -6 --projin=.\xml_merging.xml --volout="..\%OUTPUTDIR%" --volout_plugin="TiledXY|2Dseries" --slicewidth=100000 --sliceheight=150000 

ECHO Done! DONE!

NAS

:: Change directory
cd "..\%OUTPUTDIR%"
:: Error out if cd failed
if errorlevel 1 (
    echo ERROR: Failed to change directory to "..\%OUTPUTDIR%".
    exit /b 1
)


powershell -command "& {&'Get-ChildItem' -Path '.\*_*.tif*' -Recurse | Move-Item -Destination '.\' " }"

:: Append excitation wavelength to stitched image file names
set wavelength=%OUTPUTDIR:~15,3%

:: Run the PowerShell command
powershell -command "& { $wavelength = '%wavelength%'; Get-ChildItem -Path '.\*.tif*' | ForEach-Object { $newName = $_.BaseName + '_' + $wavelength + $_.Extension; Rename-Item -Path $_.FullName -NewName $newName } }"

exit


