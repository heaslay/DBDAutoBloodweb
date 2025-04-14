@echo off
REM Navigate to the script directory
cd /d "%~dp0"

REM Activate the virtual environment
call venv\Scripts\activate

REM Run the Python script
python dbd_auto_prestige.py

REM Deactivate the virtual environment (optional)
deactivate

REM Pause the terminal so it doesn't close immediately
pause
