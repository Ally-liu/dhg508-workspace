@echo off
setlocal
cd /d "%~dp0..\.."
set PORT=8000
set PAGE=http://localhost:%PORT%/code/virtual_gallery/

where py >nul 2>nul && goto use_py
where python >nul 2>nul && goto use_python
where npx >nul 2>nul && goto use_npx

echo Python or Node.js not found.
echo Install Python: https://www.python.org/downloads/
pause
exit /b

:use_py
echo Starting server with py. Root: %CD%
echo Keep this window open. Press Ctrl+C to stop.
start "" "%PAGE%"
py -m http.server %PORT%
goto :eof

:use_python
echo Starting server with python. Root: %CD%
echo Keep this window open. Press Ctrl+C to stop.
start "" "%PAGE%"
python -m http.server %PORT%
goto :eof

:use_npx
echo Starting server with npx serve. Root: %CD%
echo Keep this window open. Press Ctrl+C to stop.
start "" "%PAGE%"
npx --yes serve -l %PORT% .
goto :eof
