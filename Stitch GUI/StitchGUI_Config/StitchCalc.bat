title StitchCalc

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


call activate stitching

mpiexec -np 24 python %Parastitcher% -2 --projin=.\xml_import.xml --projout=.\xml_displcomp.xml --subvoldim=sbdim --sV=sV --sH=sH --sD=0

%TERASTITCHER% -3 --projin=.\xml_displcomp.xml

%TERASTITCHER% -4 --projin=.\xml_displproj.xml --threshold=0.5

%TERASTITCHER% -5 --projin=.\xml_displthres.xml

::mpiexec -np 31 python %Parastitcher% -6 --projin=.\xml_merging.xml --volout="..\%OUTPUTDIR%" --volout_plugin="TiledXY|2Dseries" --slicewidth=100000 --sliceheight=150000 

ECHO DONE! Done! 