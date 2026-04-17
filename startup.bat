@echo off
REM Startup batch file for Quantum Experiment improvements
REM This file is called by Windows Task Scheduler at system startup

echo ========================================
echo Quantum Experiment Platform - Startup
echo Time: %date% %time%
echo ========================================

REM Change to project directory
cd /d "c:\Users\R\Desktop\Quantum Experiment"

REM Run PowerShell startup script with execution policy bypass
powershell.exe -ExecutionPolicy Bypass -File "c:\Users\R\Desktop\Quantum Experiment\startup_improvements.ps1"

REM Keep window visible for debugging (optional, remove for production)
REM pause
