# ===========================================
# Money Machine - Windows VPS セットアップ
# ABLENET Win2 SSD (203.183.9.252) 対応
# ===========================================
# 使い方: RDPで接続後、PowerShellを管理者で実行し:
#   Set-ExecutionPolicy Bypass -Scope Process -Force
#   .\vps_windows_setup.ps1
# ===========================================

$ErrorActionPreference = "Stop"
$INSTALL_DIR = "C:\money-machine"
$REPO_URL = "https://github.com/ai-money-lab/benri-tools.git"

Write-Host "=========================================" -ForegroundColor Green
Write-Host "  Money Machine - Windows VPS Setup"
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# --- 1. Python インストール確認 ---
Write-Host "[1/7] Python確認..." -ForegroundColor Cyan
$pythonPath = $null
try {
    $pythonPath = (Get-Command python -ErrorAction Stop).Source
    $pyVer = python --version 2>&1
    Write-Host "  既存: $pyVer ($pythonPath)"
} catch {
    Write-Host "  Pythonが見つかりません。インストール中..."
    $pyInstaller = "$env:TEMP\python-installer.exe"
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe" -OutFile $pyInstaller
    Start-Process -FilePath $pyInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_pip=1" -Wait
    Remove-Item $pyInstaller -Force
    # PATHを更新
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    Write-Host "  Python インストール完了"
}

# --- 2. Git インストール確認 ---
Write-Host "[2/7] Git確認..." -ForegroundColor Cyan
try {
    $gitVer = git --version 2>&1
    Write-Host "  既存: $gitVer"
} catch {
    Write-Host "  Gitが見つかりません。インストール中..."
    $gitInstaller = "$env:TEMP\git-installer.exe"
    Invoke-WebRequest -Uri "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe" -OutFile $gitInstaller
    Start-Process -FilePath $gitInstaller -ArgumentList "/VERYSILENT", "/NORESTART", "/NOCANCEL", "/SP-" -Wait
    Remove-Item $gitInstaller -Force
    $env:Path += ";C:\Program Files\Git\cmd"
    Write-Host "  Git インストール完了"
}

# --- 3. リポジトリ ---
Write-Host "[3/7] リポジトリ準備..." -ForegroundColor Cyan
if (Test-Path "$INSTALL_DIR\.git") {
    Write-Host "  既存リポジトリを更新..."
    Set-Location $INSTALL_DIR
    git pull origin main
} else {
    Write-Host "  クローン中..."
    git clone $REPO_URL $INSTALL_DIR
    Set-Location $INSTALL_DIR
}
Write-Host "  OK"

# --- 4. Python依存パッケージ ---
Write-Host "[4/7] Python依存パッケージ..." -ForegroundColor Cyan
Set-Location $INSTALL_DIR
python -m pip install --upgrade pip --quiet
python -m pip install playwright Pillow --quiet
python -m playwright install chromium
Write-Host "  OK"

# --- 5. ディレクトリ ---
Write-Host "[5/7] ディレクトリ作成..." -ForegroundColor Cyan
$dirs = @("logs", "data", "data\x_browser_profile", "output\social\x_cards")
foreach ($d in $dirs) {
    $fullPath = Join-Path $INSTALL_DIR $d
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
    }
}
Write-Host "  OK"

# --- 6. Git設定 ---
Write-Host "[6/7] Git設定..." -ForegroundColor Cyan
Set-Location $INSTALL_DIR
git config user.name "Money Machine Bot"
git config user.email "bot@money-machine.local"

if ($env:GITHUB_TOKEN) {
    git remote set-url origin "https://x-access-token:$($env:GITHUB_TOKEN)@github.com/ai-money-lab/benri-tools.git"
    Write-Host "  GitHub token設定済み"
} else {
    Write-Host "  WARNING: GITHUB_TOKEN未設定" -ForegroundColor Yellow
    Write-Host "  設定方法: `$env:GITHUB_TOKEN = 'ghp_xxxx'" -ForegroundColor Yellow
}
Write-Host "  OK"

# --- 7. タスクスケジューラ登録 ---
Write-Host "[7/7] タスクスケジューラ登録..." -ForegroundColor Cyan

$pythonExe = (Get-Command python).Source
$xPostScript = "$INSTALL_DIR\scripts\x_daily_post.py"
$dailyScript = "$INSTALL_DIR\scripts\daily_run.py"

# 共通設定（バッテリー制限なし、最高権限）
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# 既存タスク削除
$taskNames = @(
    "MoneyMachine_Daily",
    "MoneyMachine_X_Post_0730",
    "MoneyMachine_X_Post_1215",
    "MoneyMachine_X_Post_2000"
)
foreach ($name in $taskNames) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction SilentlyContinue
}

# Daily Pipeline (06:00)
$trigger0600 = New-ScheduledTaskTrigger -Daily -At "06:00"
$action_daily = New-ScheduledTaskAction -Execute $pythonExe -Argument $dailyScript -WorkingDirectory $INSTALL_DIR
Register-ScheduledTask -TaskName "MoneyMachine_Daily" -Action $action_daily -Trigger $trigger0600 -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "  06:00 - MoneyMachine_Daily"

# X Post 1/3 (07:30)
$trigger0730 = New-ScheduledTaskTrigger -Daily -At "07:30"
$action_xpost = New-ScheduledTaskAction -Execute $pythonExe -Argument $xPostScript -WorkingDirectory $INSTALL_DIR
Register-ScheduledTask -TaskName "MoneyMachine_X_Post_0730" -Action $action_xpost -Trigger $trigger0730 -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "  07:30 - MoneyMachine_X_Post_0730"

# X Post 2/3 (12:15)
$trigger1215 = New-ScheduledTaskTrigger -Daily -At "12:15"
Register-ScheduledTask -TaskName "MoneyMachine_X_Post_1215" -Action $action_xpost -Trigger $trigger1215 -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "  12:15 - MoneyMachine_X_Post_1215"

# X Post 3/3 (20:00)
$trigger2000 = New-ScheduledTaskTrigger -Daily -At "20:00"
Register-ScheduledTask -TaskName "MoneyMachine_X_Post_2000" -Action $action_xpost -Trigger $trigger2000 -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "  20:00 - MoneyMachine_X_Post_2000"

Write-Host "  OK"

# --- 8. OpenSSH有効化（オプション） ---
Write-Host ""
Write-Host "[Optional] OpenSSH Server有効化..." -ForegroundColor Cyan
try {
    $sshStatus = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
    if ($sshStatus.State -ne 'Installed') {
        Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
    }
    Start-Service sshd -ErrorAction SilentlyContinue
    Set-Service -Name sshd -StartupType Automatic -ErrorAction SilentlyContinue
    # ファイアウォールルール
    New-NetFirewallRule -Name "OpenSSH-Server" -DisplayName "OpenSSH Server (sshd)" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 -ErrorAction SilentlyContinue
    Write-Host "  SSH有効化完了 (port 22)"
} catch {
    Write-Host "  SSH有効化スキップ: $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  セットアップ完了"
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  インストール先: $INSTALL_DIR"
Write-Host "  Python: $pythonExe"
Write-Host ""
Write-Host "  タスクスケジューラ登録済み:"
Write-Host "    06:00 - daily_run.py    (データ収集→HTML更新→Git Push)"
Write-Host "    07:30 - x_daily_post.py (X投稿 1/3)"
Write-Host "    12:15 - x_daily_post.py (X投稿 2/3)"
Write-Host "    20:00 - x_daily_post.py (X投稿 3/3)"
Write-Host ""
Write-Host "  手動テスト:"
Write-Host "    cd $INSTALL_DIR"
Write-Host "    python scripts\daily_run.py       # パイプライン"
Write-Host "    python scripts\x_daily_post.py    # X投稿"
Write-Host ""
Write-Host "  初回X投稿時にブラウザが起動しログインが必要です。"
Write-Host ""
