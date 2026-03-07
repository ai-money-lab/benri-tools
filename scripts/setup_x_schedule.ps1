# X自動投稿 タスクスケジューラ登録（1日3回）
# 7:30 朝（通勤時間帯）/ 12:15 昼（昼休み）/ 20:00 夜（ピーク）

# 既存タスク削除
try { Unregister-ScheduledTask -TaskName 'MoneyMachine_X_DailyPost' -Confirm:$false -ErrorAction SilentlyContinue } catch {}

$action = New-ScheduledTaskAction `
    -Execute 'C:\Users\maulo\AppData\Local\Programs\Python\Python312\python.exe' `
    -Argument 'C:\Users\maulo\OneDrive\マネタイズキット\money-machine\scripts\x_daily_post.py' `
    -WorkingDirectory 'C:\Users\maulo\OneDrive\マネタイズキット\money-machine'

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# 朝 7:30
$t1 = New-ScheduledTaskTrigger -Daily -At '07:30'
Register-ScheduledTask -TaskName 'MoneyMachine_X_Post_0730' -Action $action -Trigger $t1 -Settings $settings -Description 'X自動投稿 朝7:30' -Force

# 昼 12:15
$t2 = New-ScheduledTaskTrigger -Daily -At '12:15'
Register-ScheduledTask -TaskName 'MoneyMachine_X_Post_1215' -Action $action -Trigger $t2 -Settings $settings -Description 'X自動投稿 昼12:15' -Force

# 夜 20:00
$t3 = New-ScheduledTaskTrigger -Daily -At '20:00'
Register-ScheduledTask -TaskName 'MoneyMachine_X_Post_2000' -Action $action -Trigger $t3 -Settings $settings -Description 'X自動投稿 夜20:00' -Force

Write-Host "登録完了"
Get-ScheduledTask | Where-Object { $_.TaskName -like 'MoneyMachine_X*' } | Select-Object TaskName, State
