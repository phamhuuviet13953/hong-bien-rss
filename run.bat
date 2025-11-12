@echo off
REM Hong Bien RSS Tool - Start Script for Windows

echo ======================================
echo Hong Bien RSS Tool
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\.requirements_installed" (
    echo [INFO] Installing dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo. > venv\.requirements_installed
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

REM Check if config.json exists
if not exist "config.json" (
    echo [WARN] Configuration not found
    echo [INFO] Running setup...
    python setup.py

    if not exist "config.json" (
        echo [ERROR] Setup was not completed
        pause
        exit /b 1
    )
)

REM Start the bot
echo.
echo ======================================
echo Starting Hong Bien RSS Bot...
echo ======================================
echo Press Ctrl+C to stop
echo.

python rss_telegram.py
pause
