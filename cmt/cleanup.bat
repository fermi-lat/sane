@echo off
if NOT DEFINED CMTROOT set CMTROOT=d:\ground\CMT\v1r14p20031120 & set PATH=%CMTROOT%\%CMTBIN%;%PATH% & set CMTBIN=VisualC & if not defined CMTCONFIG set CMTCONFIG=%CMTBIN%

set cmttempfile="%TEMP%\tmpsetup.bat"
%CMTROOT%\%CMTBIN%\cmt.exe -quiet cleanup -bat  -pack=like -version=v0 -path=%~d0%~p0..\..\..   %1 %2 %3 %4 %5 %6 %7 %8 %9 >%cmttempfile%
if exist %cmttempfile% call %cmttempfile%
if exist %cmttempfile% del %cmttempfile%
set cmttempfile=

