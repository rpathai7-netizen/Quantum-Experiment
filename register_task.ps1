$Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NoProfile -ExecutionPolicy Bypass -File "c:\Users\R\Desktop\Quantum Experiment\run_daily_improvements.ps1"'
$Trigger = New-ScheduledTaskTrigger -Daily -At 10:05AM
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest
Register-ScheduledTask -TaskName 'QuantumExperiment_DailyImprovements' -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description 'Daily improvements for Quantum Experiment' -Force
