#!/usr/bin/env powershell
<#
.SYNOPSIS
    Setup Windows Task Scheduler for daily improvements at 10:05 AM Pakistan Time
    
.DESCRIPTION
    Creates a scheduled task that runs run_daily_improvements.ps1 daily at 10:05 AM PKT
#>

# Requires admin privileges
#Requires -RunAsAdministrator

$TaskName = "QuantumExperiment_DailyImprovements"
$TaskPath = "\Quantum Experiment\"
$ScriptPath = "c:\Users\R\Desktop\Quantum Experiment\run_daily_improvements.ps1"
$LogFile = "c:\Users\R\Desktop\Quantum Experiment\logs\task_scheduler.log"

# Create logs directory if it doesn't exist
$LogDir = Split-Path $LogFile
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

Write-Host "Setting up scheduled task for daily improvements..." -ForegroundColor Cyan
Write-Host "Task Name: $TaskName" -ForegroundColor Yellow
Write-Host "Schedule: 10:05 AM daily (Pakistan Time)" -ForegroundColor Yellow
Write-Host "Script: $ScriptPath" -ForegroundColor Yellow

# Remove existing task if it exists
try {
    $existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }
} catch {
    # Task doesn't exist, continue
}

# Create task action - run PowerShell script
$Action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""

# Create trigger - 10:05 AM daily
$Trigger = New-ScheduledTaskTrigger -Daily -At 10:05AM

# Create task settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -RunOnlyIfNetworkAvailable `
    -RunWithoutNetwork:$false `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5)

# Create principal (run with highest privileges)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME `
    -RunLevel Highest

# Register the task
try {
    $Task = Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Principal $Principal `
        -Description "Daily improvements, testing, and updates for Quantum Experiment Platform"
    
    Write-Host "`n✓ Task created successfully!" -ForegroundColor Green
    Write-Host "  Task will run daily at 10:05 AM Pakistan Time" -ForegroundColor Green
    Write-Host "  Logs: c:\Users\R\Desktop\Quantum Experiment\logs\daily_improvements_*.log" -ForegroundColor Green
    
    # Log the creation
    Add-Content -Path $LogFile -Value "`n[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Task registered successfully: $TaskName"
    
    # Show task details
    Write-Host "`nTask Details:" -ForegroundColor Cyan
    Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State, @{Name="NextRunTime"; Expression={$_.Triggers[0].StartBoundary}}
    
} catch {
    Write-Host "`n✗ Error creating task: $_" -ForegroundColor Red
    Add-Content -Path $LogFile -Value "`n[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] ERROR: Failed to register task - $_"
    exit 1
}

Write-Host "`nTo test the task immediately, run:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Yellow

Write-Host "`nTo view task logs:" -ForegroundColor Yellow
Write-Host "  Get-ScheduledTask -TaskName '$TaskName' | Get-ScheduledTaskInfo" -ForegroundColor Yellow
