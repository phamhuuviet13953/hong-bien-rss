@echo off
REM Script fix GUI dependencies - Hong Bien RSS Tool

title Fixing GUI Dependencies

echo ========================================
echo Hong Bien RSS Tool - Fix GUI
echo ========================================
echo.

echo [INFO] This script will fix GUI dependencies issue
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    pause
    exit /b 1
)

echo [OK] Python installed
python --version
echo.

REM Check venv
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
    echo.
)

REM Activate venv
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [INFO] Uninstalling old customtkinter...
pip uninstall -y customtkinter

echo.
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [INFO] Installing dependencies with specific versions...
pip install --upgrade --force-reinstall customtkinter==5.2.2
pip install --upgrade darkdetect Pillow

echo.
echo [INFO] Installing all requirements...
pip install -r requirements.txt

echo.
echo [INFO] Removing old markers...
if exist "venv\.gui_requirements_installed" del venv\.gui_requirements_installed

echo.
echo ========================================
echo [SUCCESS] GUI dependencies fixed!
echo ========================================
echo.
echo You can now run the GUI with: run-gui.bat
echo Or directly: python gui.py
echo.

pause
