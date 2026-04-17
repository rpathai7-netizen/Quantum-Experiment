@echo off
REM Quantum Experiment Platform - Windows Installer
REM Run this script to install the application

echo ================================================
echo Quantum Experiment Platform - Installer
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo Step 1: Installing Python dependencies...
pip install qiskit qiskit-aer numpy
if errorlevel 1 (
    echo Warning: Some packages may have failed to install
)

echo.
echo Step 2: Launching Quantum Experiment Platform...
echo.

REM Launch the GUI
python "C:\Users\R\Desktop\Quantum Experiment\gui_application.py"

pause
