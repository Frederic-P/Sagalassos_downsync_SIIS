@echo off
REM Save the current directory
set CUR_DIR=%cd%

REM Navigate to the Scripts directory and activate the virtual environment
cd Scripts
call activate

REM Navigate back to the project root directory
cd ..

REM Run the Python script
cmd /k "python downsync.py"

REM Deactivate the virtual environment
deactivate

REM Navigate back to the original directory
cd %CUR_DIR%

REM Pause to keep the terminal open
pause
