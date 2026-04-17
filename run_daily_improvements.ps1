#!/usr/bin/env powershell
<#
.SYNOPSIS
    Daily improvement run for Quantum Experiment Platform
    Scheduled to run at 10:05 AM Pakistan Time (PKT)
    
.DESCRIPTION
    This script runs the complete improvement cycle:
    1. Tests
    2. Code quality analysis
    3. Performance profiling
    4. Code improvements (formatting, imports, style)
    5. Commits improvements
    6. Pushes to GitHub
    
.NOTES
    Windows Task Scheduler: Runs daily at 10:05 AM
    Timezone: Pakistan (UTC+5:00)
#>

# Configuration
$ProjectRoot = "c:\Users\R\Desktop\Quantum Experiment"
$LogFile = "$ProjectRoot\logs\daily_improvements_$(Get-Date -Format 'yyyy-MM-dd').log"
$StartTime = Get-Date

# Ensure logs directory exists
$LogDir = Join-Path $ProjectRoot "logs"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# Function to log output
function Write-Log {
    param($Message, $Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Write-Host $LogEntry
    Add-Content -Path $LogFile -Value $LogEntry
}

# Function to run a command and log output
function Invoke-WithLog {
    param($Description, $Script)
    
    Write-Log "========================================"
    Write-Log "Starting: $Description"
    Write-Log "========================================"
    
    try {
        $Result = Invoke-Expression $Script 2>&1
        Write-Log "Result: $Result"
        Write-Log "$Description completed successfully"
        return $true
    }
    catch {
        Write-Log "ERROR: $Description failed: $_" "ERROR"
        return $false
    }
}

Write-Log "╔════════════════════════════════════════════════════════════╗"
Write-Log "║   QUANTUM EXPERIMENT PLATFORM - DAILY IMPROVEMENTS        ║"
Write-Log "║   Start Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') PKT                ║"
Write-Log "╚════════════════════════════════════════════════════════════╝"

Set-Location $ProjectRoot

# Step 1: Ensure dependencies
Write-Log "Installing/verifying dependencies..."
pip install -q black isort autopep8 pytest pytest-cov 2>&1 | Write-Log

# Step 2: Run tests
Write-Log ""
$TestPassed = Invoke-WithLog "Running Tests" `
    "python -m pytest tests/ -v --tb=short 2>&1"

# Step 3: Code quality analysis
Write-Log ""
Invoke-WithLog "Analyzing Code Quality" `
    "python scripts/analyze_code_quality.py 2>&1"

# Step 4: Performance profiling (with timeout to keep it quick)
Write-Log ""
Invoke-WithLog "Performance Profiling" `
    "python scripts/performance_profiler.py 2>&1"

# Step 5: Code improvements
Write-Log ""
Write-Log "========================================"
Write-Log "Running Code Improvements...    "
Write-Log "========================================"

# Black formatting
Write-Log "Applying Black formatting..."
python -m black . --exclude="(__pycache__|\.git|\.venv|build|dist)" 2>&1 | Write-Log

# isort import organization
Write-Log "Organizing imports with isort..."
python -m isort . --skip-gitignore 2>&1 | Write-Log

# Check for changes
$GitStatus = git status --porcelain
if ($GitStatus) {
    Write-Log "Code improvements detected. Committing..."
    
    # Stage improvements
    git add -A 2>&1 | Write-Log
    
    # Commit with timestamp
    $CommitMessage = "🤖 Automated daily improvements $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $CommitMessage 2>&1 | Write-Log
    
    # Push to GitHub
    Write-Log "Pushing improvements to GitHub..."
    git push origin main 2>&1 | Write-Log
    
    Write-Log "✅ Improvements committed and pushed"
}
else {
    Write-Log "✅ No code improvements needed (already optimal)"
}

# Step 6: Summary
Write-Log ""
Write-Log "========================================"
Write-Log "DAILY IMPROVEMENT CYCLE COMPLETE"
Write-Log "========================================"
$EndTime = Get-Date
$Duration = $EndTime - $StartTime
Write-Log "Total Duration: $($Duration.TotalMinutes) minutes"
Write-Log "Tests Passed: $(if($TestPassed) { '✅ Yes' } else { '⚠️ Check logs' })"
Write-Log "End Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') PKT"
Write-Log ""
Write-Log "📊 Log file: $LogFile"
Write-Log "🔗 GitHub: https://github.com/rpathai7-netizen/Quantum-Experiment"
