title StitchImport

:: Locations of things
::
set TERASTITCHER=C:\terastitcher\terastitcher
set Parastitcher=C:\terastitcher\parastitcher.py


:: Set active directory to path of batch file parent folder
cd /d %~dp0

SET WORKINGDIR=%CD%
for %%* in (.) do SET DIRNAME=%%~n*
::SET OUTPUTDIR=%DIRNAME%_Stitched
::mkdir "..\%OUTPUTDIR%"


call activate base

%TERASTITCHER% -1 --volin="%WORKINGDIR%" --ref1=H --ref2=V --ref3=D --vxl1=dX --vxl2=dY --vxl3=2 --projout=xml_import.xml --sparse_data 

ECHO DONE! Done! 