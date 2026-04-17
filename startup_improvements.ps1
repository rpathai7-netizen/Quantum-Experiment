#!/usr/bin/env powershell
<#
.SYNOPSIS
    Startup script that opens VS Code and schedules daily improvements
    
.DESCRIPTION
    This script:
    1. Opens VS Code with the Quantum Experiment project
    2. Waits until 10:05 AM Pakistan Time (if earlier)
    3. Starts daily improvement process
    4. Repeats daily
    
.NOTES
    Add to Windows Task Scheduler to run at system startup
#>

# Configuration
$ProjectRoot = "c:\Users\R\Desktop\Quantum Experiment"
$VSCodePath = "C:\Program Files\Microsoft VS Code\Code.exe"
$ImprovementScript = "$ProjectRoot\run_daily_improvements.ps1"
$LogFile = "$ProjectRoot\logs\startup_$(Get-Date -Format 'yyyy-MM-dd').log"

# Ensure logs directory exists
$LogDir = "$ProjectRoot\logs"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

function Write-Log {
    param($Message, $Level = "INFO")
    $Timestamp = Get-Date -Format "HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Write-Host $LogEntry
    Add-Content -Path $LogFile -Value $LogEntry
}

Write-Log "╔════════════════════════════════════════════════╗"
Write-Log "║   QUANTUM EXPERIMENT - STARTUP SEQUENCE       ║"
Write-Log "║   Machine Time: $(Get-Date -Format 'HH:mm:ss')                       ║"
Write-Log "╚════════════════════════════════════════════════╝"

# Step 1: Open VS Code
Write-Log "Opening Visual Studio Code..."
try {
    # Open VS Code with the project folder
    if (Test-Path $VSCodePath) {
        & $VSCodePath $ProjectRoot
        Write-Log "✅ VS Code opened successfully"
    }
    else {
        Write-Log "⚠️ VS Code not found at $VSCodePath, trying default path..." "WARN"
        code $ProjectRoot
    }
}
catch {
    Write-Log "⚠️ Could not open VS Code: $_" "WARN"
}

# Step 2: Wait for 10:05 AM Pakistan Time
Write-Log ""
Write-Log "Waiting for 10:05 AM Pakistan Time (PKT)..."

$TargetTime = (Get-Date).Date.AddHours(10).AddMinutes(5)  # 10:05 AM today

while ((Get-Date) -lt $TargetTime) {
    $CurrentTime = Get-Date -Format "HH:mm:ss"
    $TimeUntil = ($TargetTime - (Get-Date)).TotalSeconds
    $MinutesUntil = [Math]::Ceiling($TimeUntil / 60)
    
    # Log every 5 minutes to avoid excessive logging
    if ($MinutesUntil % 5 -eq 0 -or $MinutesUntil -lt 2) {
        Write-Log "Current: $CurrentTime | Time until improvements: $MinutesUntil minutes"
    }
    
    Start-Sleep -Seconds 60  # Check every minute
}

Write-Log ""
Write-Log "=========================================="
Write-Log "✨ It's now 10:05 AM! Starting improvements..."
Write-Log "=========================================="

# Step 3: Run improvements
try {
    & powershell.exe -ExecutionPolicy Bypass -File $ImprovementScript
    Write-Log "✅ Daily improvement cycle completed"
}
catch {
    Write-Log "❌ Error running improvements: $_" "ERROR"
}

Write-Log ""
Write-Log "Script will run again tomorrow at 10:05 AM PKT"
Write-Log "Keep your machine on or ensure it's scheduled to turn on at 10 AM"
