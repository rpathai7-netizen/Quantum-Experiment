# Windows Automatic Startup Configuration Guide

## Overview

Your Quantum Experiment Platform will automatically run improvements every day:
- **10:00 AM** - Windows 10 starts automatically (BIOS configured ✓)
- **10:05 AM** - VS Code opens + improvements begin (this guide configures it)
- **5-7 PM** - You manually turn off the machine

---

## Setup Instructions

### Step 1: Create Windows Task Scheduler Task

1. **Open Task Scheduler**
   - Press `Win + R`
   - Type: `taskschd.msc`
   - Press Enter

2. **Create New Task**
   - Right-click: "Task Scheduler Library"
   - Select: "Create Task..."

3. **Configure General Tab**
   ```
   Name: "Quantum Improvements Startup"
   Description: "Auto-run VS Code and start quantum platform improvements"
   
   ☑ Run with highest privileges
   ☐ Hidden
   ```

4. **Configure Triggers Tab**
   - Click: "New..."
   - Set trigger:
     ```
     Begin the task: At startup
     ```
   - Click: "OK"

5. **Configure Actions Tab**
   - Click: "New..."
   - Set action:
     ```
     Action: Start a program
     Program/script: C:\Windows\System32\cmd.exe
     Add arguments: /c "c:\Users\R\Desktop\Quantum Experiment\startup.bat"
     ```
   - Click: "OK"

6. **Configure Conditions Tab** (Optional but recommended)
   ```
   ☑ Wake the computer to run this task
   ```

7. **Configure Settings Tab**
   ```
   ☑ Allow task to be run on demand
   ☑ Run task as soon as possible after a scheduled start is missed
   ☐ Stop the task if it runs longer than: [uncheck or set to 4 hours]
   ☑ If the running task does not end when requested, force it to stop
   ```

8. **Click: "OK"** to save

---

## Pakistan Time (PKT) Scheduling

**Your machine will:**
1. **10:00 AM PKT** - Start automatically (via BIOS)
2. **10:05 AM PKT** - Windows Task Scheduler triggers startup.bat
3. **10:05 AM PKT** - startup_improvements.ps1 runs
4. **10:05 AM PKT** - VS Code opens
5. **10:05-11:30 AM PKT** - Improvements run (tests, format, push)
6. **5:00-7:00 PM PKT** - You manually turn off

---

## Script Workflow

```
startup.bat (called by Task Scheduler)
    ↓
startup_improvements.ps1 (PowerShell)
    ├─ Opens VS Code
    ├─ Waits until 10:05 AM PKT
    └─ Runs run_daily_improvements.ps1
         ├─ Install dependencies
         ├─ Run tests (pytest)
         ├─ Analyze code quality
         ├─ Profile performance
         ├─ Format code (black)
         ├─ Organize imports (isort)
         ├─ Commit improvements
         └─ Push to GitHub
```

---

## Verification Steps

### Test the Setup (Without Waiting Until 10 AM)

1. **Run startup script manually:**
   ```powershell
   powershell -ExecutionPolicy Bypass `
     -File "c:\Users\R\Desktop\Quantum Experiment\startup_improvements.ps1"
   ```

2. **Expected to see:**
   - VS Code opens with the project
   - Command prompt window waiting for time
   - Improvements start (or wait until 10:05 AM)

### Test Improvements Script Directly

```powershell
powershell -ExecutionPolicy Bypass `
  -File "c:\Users\R\Desktop\Quantum Experiment\run_daily_improvements.ps1"
```

---

## What Gets Logged

Each day, a log file is created:
```
c:\Users\R\Desktop\Quantum Experiment\logs\
├── daily_improvements_2026-04-17.log
├── daily_improvements_2026-04-18.log
├── startup_2026-04-17.log
└── startup_2026-04-18.log
```

**View logs:**
```powershell
Get-Content "c:\Users\R\Desktop\Quantum Experiment\logs\daily_improvements_*.log" -Tail 50
```

---

## Daily Improvement Activities

Your system will automatically:

### Testing (5-10 minutes)
```
✅ Run 40+ unit tests
✅ Check all Python versions (3.8-3.11)
✅ Generate coverage reports
✅ Run security scans
```

### Analysis (2-3 minutes)
```
✅ Analyze code quality
✅ Profile performance
✅ Generate reports
```

### Improvements (3-5 minutes)
```
✅ Format code with Black
✅ Organize imports with isort
✅ Fix PEP8 style issues
✅ Auto-commit if changes found
✅ Push to GitHub
```

**Total time: ~15-25 minutes**

---

## Expected Daily Results

### By 10:30 AM PKT (approximately)
- ✅ VS Code open with project
- ✅ All tests passing
- ✅ Code formatted consistently
- ✅ Changes committed to GitHub
- ✅ Logs created in `logs/` directory

### By 10:05-11:00 AM PKT
- ✅ Performance benchmarks completed
- ✅ Documentation regenerated
- ✅ Ready for your manual work

---

## Troubleshooting

### VS Code doesn't open
```
Issue: Path might be different
Solution: 
  1. Find VS Code path:
     where code
  2. Update C:\Windows\System32\cmd.exe path in startup.ps1
```

### Task doesn't run at startup
```
Issue: Task Scheduler permissions
Solution:
  1. Run: taskschd.msc as Administrator
  2. Ensure "Run with highest privileges" is checked
  3. Check "Wake the computer to run this task"
```

### PowerShell execution policy error
```
Issue: Execution policy too restrictive
Solution: Already handled by startup.bat with -ExecutionPolicy Bypass
  But if issues persist:
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Improvements don't commit/push
```
Issue: Git credentials not saved
Solution:
  1. First-time setup: Run manually
     powershell -ExecutionPolicy Bypass -File startup_improvements.ps1
  2. Enter your GitHub credentials
  3. Check: "Save credentials" box
  4. After that, automated commits work
```

### Task runs too late
```
Issue: Windows startup takes >5 minutes
Solution: Update startup_improvements.ps1 date calculation:
  # Change line with AddMinutes(5) to AddMinutes(10) or more
  $TargetTime = (Get-Date).Date.AddHours(10).AddMinutes(10)
```

---

## Manual Control Options

### Disable automatic startup (keep machine, skip improvements)
```powershell
Disable-ScheduledTask -TaskName "Quantum Improvements Startup"
```

### Re-enable after disabling
```powershell
Enable-ScheduledTask -TaskName "Quantum Improvements Startup"
```

### Run improvements immediately (anytime)
```powershell
powershell -ExecutionPolicy Bypass `
  -File "c:\Users\R\Desktop\Quantum Experiment\run_daily_improvements.ps1"
```

### View all scheduled tasks
```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like "*Quantum*"}
```

### Remove task completely (if no longer needed)
```powershell
Unregister-ScheduledTask -TaskName "Quantum Improvements Startup" -Confirm:$false
```

---

## Your Daily Schedule (Pakistan Time)

| Time | Action | Status |
|------|--------|--------|
| **10:00 AM** | Machine powers on (BIOS) | 🤖 Automatic |
| **10:01 AM** | Windows 10 loads | ⏳ Auto |
| **10:05 AM** | Task Scheduler triggers startup.bat | 🚀 Auto |
| **10:05 AM** | VS Code opens | 🎯 Auto |
| **10:05 AM** | Improvements start | ⚡ Auto |
| **10:30 AM** | Improvements complete | ✅ Done |
| **10:30 AM** | You can start working | 👨‍💻 Manual |
| **5:00-7:00 PM** | You turn off machine | 🛑 Manual |

---

## GitHub Integration

Each day, improvements are automatically pushed to:
```
https://github.com/rpathai7-netizen/Quantum-Experiment
```

**View daily commits:**
1. Go to repository
2. Click "Insights" → "Network"
3. See daily improvement commits at 10:05 AM PKT

---

## Bandwidth/Internet Impact

The improvements system uses:
- **Download**: ~50-100 MB (dependencies check)
- **Upload**: ~1-5 MB (git pushes)
- **Connection time**: ~2-3 minutes
- **Best during**: 10:05-11:00 AM PKT

Ensure you have internet connection when you start the machine.

---

## Monitoring

### View today's log
```powershell
Get-ChildItem "c:\Users\R\Desktop\Quantum Experiment\logs\" -Filter "*$(Get-Date -Format 'yyyy-MM-dd')*" | 
  Foreach { Get-Content $_.FullName -Tail 50 }
```

### Watch logs in real-time
```powershell
Get-Content "c:\Users\R\Desktop\Quantum Experiment\logs\daily_improvements_*.log" -Wait -Tail 10
```

### Check task execution history
```powershell
Get-ScheduledTaskInfo -TaskName "Quantum Improvements Startup"
```

---

## Safety Notes

✅ **Safe to let run overnight:** 
- System will be off 5 PM - 10 AM next day
- No data loss risk

✅ **Safe to interrupt:**
- Press Ctrl+C to stop any script
- Git commits preserve state
- No corruption possible

✅ **Safe for your code:**
- Only formatting/style changes
- No logic modifications
- All changes are committed (reversible)

---

## Summary

After setting up this task in Windows Task Scheduler:

1. **10:00 AM** - Machine turns on automatically
2. **10:05 AM** - VS Code opens + improvements begin
3. **~10:30 AM** - Everything ready for your work
4. **5-7 PM** - You turn it off

**This happens automatically every day** without any intervention needed!

---

## Next Steps

1. ✅ Open Task Scheduler (`taskschd.msc`)
2. ✅ Create new task as described above
3. ✅ Test the task manually (right-click → Run)
4. ✅ Verify logs appear in `logs/` directory
5. ✅ Tomorrow at 10:05 AM, watch the automation begin!

---

**Questions?** Check the logs in `c:\Users\R\Desktop\Quantum Experiment\logs\`

Need help? All scripts have detailed logging and error messages.
