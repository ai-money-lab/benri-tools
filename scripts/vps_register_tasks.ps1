$py = "C:\Program Files\Python312\python.exe"
$xPost = "C:\money-machine\scripts\x_daily_post.py"
$daily = "C:\money-machine\scripts\daily_run.py"
$wd = "C:\money-machine"

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 1)
$principal = New-ScheduledTaskPrincipal -UserId "Administrator" -LogonType S4U -RunLevel Highest

$taskNames = @("MoneyMachine_Daily","MoneyMachine_X_Post_0730","MoneyMachine_X_Post_1215","MoneyMachine_X_Post_2000")
foreach ($name in $taskNames) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction SilentlyContinue
}

$t0 = New-ScheduledTaskTrigger -Daily -At "06:00"
$a0 = New-ScheduledTaskAction -Execute $py -Argument $daily -WorkingDirectory $wd
Register-ScheduledTask -TaskName "MoneyMachine_Daily" -Action $a0 -Trigger $t0 -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "OK: MoneyMachine_Daily (06:00)"

$a1 = New-ScheduledTaskAction -Execute $py -Argument $xPost -WorkingDirectory $wd

$t1 = New-ScheduledTaskTrigger -Daily -At "07:30"
Register-ScheduledTask -TaskName "MoneyMachine_X_Post_0730" -Action $a1 -Trigger $t1 -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "OK: MoneyMachine_X_Post_0730 (07:30)"

$t2 = New-ScheduledTaskTrigger -Daily -At "12:15"
Register-ScheduledTask -TaskName "MoneyMachine_X_Post_1215" -Action $a1 -Trigger $t2 -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "OK: MoneyMachine_X_Post_1215 (12:15)"

$t3 = New-ScheduledTaskTrigger -Daily -At "20:00"
Register-ScheduledTask -TaskName "MoneyMachine_X_Post_2000" -Action $a1 -Trigger $t3 -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "OK: MoneyMachine_X_Post_2000 (20:00)"

Write-Host "All tasks registered."
