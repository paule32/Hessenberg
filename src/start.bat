@echo off
set PY=python.exe
set BASEDIR=%cd%

set VERSION=cpython-313
set CLTAPP=hess4

echo Create Byte-Code...
%PY% -m compileall %BASEDIR%\%CLTAPP%.py
cd __pycache__
%PY% %BASEDIR%\__pycache__\%CLTAPP%.%VERSION%.pyc
