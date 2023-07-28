@echo off

echo Checking for python installation ...
python --version 2>NUL
if errorlevel 1 goto noPython

echo Checking for pip installation ...
pip --version 2>NUL
if errorlevel 1 goto noPip

echo Checking for pipenv installation ...
pipenv --version 2>NUL
if errorlevel 1 goto noPipenv

:sync
echo Syncing dependencies ...
pipenv sync

echo Running tool ...
pipenv run start pythonw tool.py --gui
goto:eof

:noPython
echo Error^: Python is not installed.
pause
goto:eof

:noPip
echo Error^: pip is not installed.
pause
goto:eof

:noPipenv
pip install pipenv
goto sync
