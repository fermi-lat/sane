@echo off
if .%1==. (set tag=VC8debug ) else set tag=%1
set tempfile=%HOME%\tmpsetup.bat
d:\ground\CMT\v1r14p20031120\VisualC\cmt.exe -quiet -bat -pack=like -version=v1 setup -tag=%tag% >"%tempfile%"
if exist "%tempfile%" call "%tempfile%"
if exist "%tempfile%" del "%tempfile%"
set PATH=%LD_LIBRARY_PATH%;%PATH%