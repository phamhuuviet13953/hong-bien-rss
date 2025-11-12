@echo off
REM Hong Bien RSS Tool - GUI Launcher for Windows

title Hong Bien RSS Tool - GUI

echo ======================================
echo Hong Bien RSS Tool - GUI
echo ======================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python installed
python --version
echo.

REM Check/Create venv
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
    echo.
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
if not exist "venv\.gui_requirements_installed" (
    echo [INFO] Installing GUI dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo. > venv\.gui_requirements_installed
    echo [OK] Dependencies installed
    echo.
) else (
    echo [OK] Dependencies ready
    echo.
)

REM Launch GUI
echo [INFO] Launching GUI...
echo.

python gui.py

if errorlevel 1 (
    echo.
    echo [ERROR] An error occurred!
    pause
)
