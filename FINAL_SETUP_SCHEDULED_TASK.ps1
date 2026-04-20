#!/usr/bin/env powershell
# FINAL SETUP: Schedule Daily Improvements
# This script sets up Windows Task Scheduler to run daily improvements at 10:05 AM Pakistan Time
# IMPORTANT: Run this as Administrator

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Setting up Daily Improvements Task" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check for admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "ERROR: This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    exit 1
}

$TaskName = "QuantumExperiment_DailyImprovements"
$ScriptPath = "c:\Users\R\Desktop\Quantum Experiment\run_daily_improvements.ps1"

# Check if script exists
if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: Script not found at $ScriptPath" -ForegroundColor Red
    exit 1
}

Write-Host "Creating scheduled task..." -ForegroundColor Yellow
Write-Host "  Task: $TaskName" -ForegroundColor Gray
Write-Host "  Schedule: 10:05 AM daily (Pakistan Time)" -ForegroundColor Gray
Write-Host "  Script: $ScriptPath" -ForegroundColor Gray
Write-Host ""

try {
    # Remove existing task if it exists
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false | Out-Null
        Start-Sleep -Milliseconds 500
    }

    # Create the task
    $Action = New-ScheduledTaskAction -Execute 'powershell.exe' `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""
    
    $Trigger = New-ScheduledTaskTrigger -Daily -At 10:05AM
    
    $Settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable
    
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME `
        -RunLevel Highest
    
    Register-ScheduledTask -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Principal $Principal `
        -Description "Quantum Experiment: Daily improvements, tests, and updates" `
        -Force | Out-Null
    
    Write-Host ""
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Task created and will run daily at 10:05 AM Pakistan Time" -ForegroundColor Green
    Write-Host ""
    
    # Show task details
    Write-Host "Task Details:" -ForegroundColor Cyan
    $task = Get-ScheduledTask -TaskName $TaskName
    $task | Select-Object @{Name="TaskName"; Expression={$_.TaskName}}, @{Name="State"; Expression={$_.State}} | Format-Table -AutoSize
    
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Check the scheduled task in Windows Task Scheduler" -ForegroundColor Gray
    Write-Host "  2. View logs daily at: c:\Users\R\Desktop\Quantum Experiment\logs\" -ForegroundColor Gray
    Write-Host "  3. To test immediately, run:" -ForegroundColor Gray
    Write-Host "     Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
    Write-Host ""
    
} catch {
    Write-Host "ERROR: Failed to create scheduled task" -ForegroundColor Red
    Write-Host "Details: $_" -ForegroundColor Red
    exit 1
}
