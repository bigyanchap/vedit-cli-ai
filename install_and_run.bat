@echo off
echo ========================================
echo    VEdit CLI - Video Editor Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
echo.

REM Install requirements
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Installation completed successfully!
echo ========================================
echo.
echo Starting VEdit CLI...
echo.

REM Start the application
python vedit_cli.py

pause 