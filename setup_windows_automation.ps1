#!/usr/bin/env powershell
<#
.SYNOPSIS
    Automated setup script for Windows Task Scheduler
    
.DESCRIPTION
    Creates the required Task Scheduler task for automatic startup
    You must run this as Administrator
    
.PARAMETER TaskName
    Name of the scheduled task (default: "Quantum Improvements Startup")
    
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1
    
.NOTES
    Must be run as Administrator
    Pakistan Time (PKT = UTC+5:00)
#>

param(
    [string]$TaskName = "Quantum Improvements Startup"
)

# Verify running as Administrator
$IsAdmin = ([Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544"
if (-not $IsAdmin) {
    Write-Host "❌ ERROR: This script must run as Administrator!" -ForegroundColor Red
    Write-Host "Solution: Right-click PowerShell → Run as administrator → Try again"
    exit 1
}

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  QUANTUM EXPERIMENT - WINDOWS TASK SCHEDULER SETUP        ║" -ForegroundColor Cyan
Write-Host "║  Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')                              ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$ProjectRoot = "c:\Users\R\Desktop\Quantum Experiment"
$StartupBat = "$ProjectRoot\startup.bat"
$LogPath = "$ProjectRoot\logs"

Write-Host "📋 Configuration:" -ForegroundColor Yellow
Write-Host "   Task Name: $TaskName"
Write-Host "   Project Root: $ProjectRoot"
Write-Host "   Startup Script: $StartupBat"
Write-Host "   Log Directory: $LogPath"
Write-Host ""

# Verify files exist
Write-Host "✓ Verifying files..." -ForegroundColor Yellow

$FilesToCheck = @{
    "startup.bat" = $StartupBat
    "startup_improvements.ps1" = "$ProjectRoot\startup_improvements.ps1"
    "run_daily_improvements.ps1" = "$ProjectRoot\run_daily_improvements.ps1"
}

$AllFilesExist = $true
foreach ($FileName in $FilesToCheck.Keys) {
    $FilePath = $FilesToCheck[$FileName]
    if (Test-Path $FilePath) {
        Write-Host "  ✅ Found: $FileName"
    }
    else {
        Write-Host "  ❌ Missing: $FileName at $FilePath" -ForegroundColor Red
        $AllFilesExist = $false
    }
}

if (-not $AllFilesExist) {
    Write-Host ""
    Write-Host "❌ ERROR: Some required files are missing!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Create logs directory if it doesn't exist
if (-not (Test-Path $LogPath)) {
    Write-Host "📁 Creating logs directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $LogPath -Force | Out-Null
    Write-Host "   ✅ Created: $LogPath"
    Write-Host ""
}

# Check if task already exists
Write-Host "🔍 Checking for existing task..." -ForegroundColor Yellow
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "   Found existing task: $TaskName" -ForegroundColor Yellow
    Write-Host ""
    
    $Response = Read-Host "   Replace existing task? (Y/N)"
    if ($Response -ne 'Y' -and $Response -ne 'y') {
        Write-Host "   ❌ Cancelled. Task setup not modified."
        exit 0
    }
    
    Write-Host "   Removing existing task..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "   ✅ Removed: $TaskName"
}

Write-Host ""
Write-Host "🚀 Creating new task..." -ForegroundColor Cyan
Write-Host ""

try {
    # Create task trigger (at system startup)
    $Trigger = New-ScheduledTaskTrigger -AtStartup
    Write-Host "   ✅ Trigger created: At system startup"
    
    # Create task action
    $Action = New-ScheduledTaskAction `
        -Execute "cmd.exe" `
        -Argument "/c `"$StartupBat`""
    Write-Host "   ✅ Action created: Run $StartupBat"
    
    # Create task settings
    $Settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable `
        -ExecutionTimeLimit (New-TimeSpan -Hours 4)
    
    $Settings.WakeToRun = $true
    Write-Host "   ✅ Settings created"
    
    # Register the task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Trigger $Trigger `
        -Action $Action `
        -Settings $Settings `
        -RunLevel Highest `
        -Description "Automatically opens VS Code and runs quantum platform improvements at 10:05 AM Pakistan Time" `
        -Force | Out-Null
    
    Write-Host "   ✅ Task registered: $TaskName"
}
catch {
    Write-Host "   ❌ Error creating task: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Task created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Task Details:" -ForegroundColor Yellow
Write-Host "   Name: $TaskName"
Write-Host "   Trigger: At system startup"
Write-Host "   Run Level: Highest privileges"
Write-Host "   Wakeup: Yes (wake computer to run)"
Write-Host "   Execution Timeout: 4 hours"
Write-Host ""

# Verify task was created
$NewTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($NewTask) {
    Write-Host "🔍 Verifying task..." -ForegroundColor Yellow
    Write-Host "   ✅ Task found in Task Scheduler"
    Write-Host "   Status: $($NewTask.State)"
    Write-Host ""
}

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  Test the task (optional but recommended):" -ForegroundColor Cyan
Write-Host "   • Open Task Scheduler (taskschd.msc)"
Write-Host "   • Find: $TaskName"
Write-Host "   • Right-click → Run"
Write-Host "   • Watch for: VS Code opens, logs appear"
Write-Host ""
Write-Host "2️⃣  Check logs after test:" -ForegroundColor Cyan
Write-Host "   Get-ChildItem '$LogPath' | Get-Content -Tail 50"
Write-Host ""
Write-Host "3️⃣  Your daily schedule:" -ForegroundColor Cyan
Write-Host "   • 10:00 AM PKT: Machine turns on (BIOS)"
Write-Host "   • 10:05 AM PKT: VS Code opens + improvements start"
Write-Host "   • ~10:30 AM PKT: Improvements complete"
Write-Host "   • 5-7 PM PKT: You turn off machine"
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "✨ Setup Complete! Your system is ready for automation." -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "📖 For detailed information, see:" -ForegroundColor Yellow
Write-Host "   $ProjectRoot\WINDOWS_AUTOMATION_SETUP.md"
Write-Host ""

# Optional: Ask if user wants to test now
Write-Host ""
$RunTest = Read-Host "Would you like to test the task now? (Y/N)"
if ($RunTest -eq 'Y' -or $RunTest -eq 'y') {
    Write-Host ""
    Write-Host "🧪 Testing task... (you have 30 seconds to cancel with Ctrl+C)" -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    Write-Host "Starting task..."
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "✅ Task started. Check logs in a moment."
}
