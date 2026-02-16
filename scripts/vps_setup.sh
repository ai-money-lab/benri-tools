#!/bin/bash
# ===========================================
# Money Machine VPS セットアップスクリプト
# Ubuntu 22.04+ 対応
# ===========================================
#
# 使い方:
#   1. VPSにSSHで接続
#   2. このスクリプトを実行:
#      bash <(curl -s https://raw.githubusercontent.com/ai-money-lab/benri-tools/main/scripts/vps_setup.sh)
#   3. 手動でやる場合:
#      git clone https://github.com/ai-money-lab/benri-tools.git /opt/money-machine
#      cd /opt/money-machine && bash scripts/vps_setup.sh
#

set -e

INSTALL_DIR="/opt/money-machine"
REPO_URL="https://github.com/ai-money-lab/benri-tools.git"

echo "========================================="
echo "  Money Machine VPS Setup"
echo "========================================="
echo ""

# --- 1. システムパッケージ ---
echo "[1/6] システムパッケージをインストール..."
sudo apt-get update -qq
sudo apt-get install -y -qq \
    python3 python3-pip python3-venv \
    git \
    xvfb \
    fonts-noto-cjk \
    libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 \
    libgbm1 libpango-1.0-0 libcairo2 libasound2 \
    > /dev/null 2>&1
echo "  OK"

# --- 2. リポジトリ ---
echo "[2/6] リポジトリを準備..."
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "  既存のリポジトリを更新..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "  クローン: $REPO_URL"
    sudo git clone "$REPO_URL" "$INSTALL_DIR"
    sudo chown -R $USER:$USER "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi
echo "  OK"

# --- 3. Python仮想環境 ---
echo "[3/6] Python仮想環境をセットアップ..."
cd "$INSTALL_DIR"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

pip install -q --upgrade pip
pip install -q playwright Pillow

# Playwrightブラウザインストール
playwright install chromium
playwright install-deps chromium 2>/dev/null || true
echo "  OK"

# --- 4. ディレクトリ作成 ---
echo "[4/6] ディレクトリ作成..."
mkdir -p "$INSTALL_DIR/logs"
mkdir -p "$INSTALL_DIR/data"
mkdir -p "$INSTALL_DIR/data/x_browser_profile"
echo "  OK"

# --- 5. Git push用の認証設定 ---
echo "[5/6] Git設定..."
cd "$INSTALL_DIR"
git config user.name "Money Machine Bot"
git config user.email "bot@money-machine.local"

# GitHub tokenがあればcredential helperを設定
if [ -n "$GITHUB_TOKEN" ]; then
    git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/ai-money-lab/benri-tools.git"
    echo "  GitHub token設定済み"
else
    echo "  WARNING: GITHUB_TOKEN が未設定です"
    echo "  Git pushを有効にするには:"
    echo "    export GITHUB_TOKEN=ghp_xxxx"
    echo "    git remote set-url origin https://x-access-token:\$GITHUB_TOKEN@github.com/ai-money-lab/benri-tools.git"
fi
echo "  OK"

# --- 6. Cron登録 ---
echo "[6/6] Cron登録..."
PYTHON_PATH="$INSTALL_DIR/venv/bin/python3"
DAILY_SCRIPT="$INSTALL_DIR/scripts/daily_run.py"
X_POST_SCRIPT="$INSTALL_DIR/scripts/x_daily_post.py"

# 既存のmoney-machineエントリを除去して新規追加
(crontab -l 2>/dev/null | grep -v 'money-machine' || true) | {
    cat
    echo "# Money Machine - daily pipeline (06:00 JST)"
    echo "0 6 * * * cd $INSTALL_DIR && $PYTHON_PATH $DAILY_SCRIPT >> $INSTALL_DIR/logs/cron_daily.log 2>&1"
    echo "# Money Machine - X daily post (19:00 JST, with virtual display)"
    echo "0 19 * * * cd $INSTALL_DIR && xvfb-run --auto-servernum $PYTHON_PATH $X_POST_SCRIPT >> $INSTALL_DIR/logs/cron_xpost.log 2>&1"
} | crontab -
echo "  OK"

echo ""
echo "========================================="
echo "  セットアップ完了"
echo "========================================="
echo ""
echo "  インストール先: $INSTALL_DIR"
echo "  Python: $PYTHON_PATH"
echo ""
echo "  Cron登録済み:"
echo "    06:00 - daily_run.py  (データ収集→HTML更新→Git Push)"
echo "    19:00 - x_daily_post.py (X投稿 via xvfb-run)"
echo ""
echo "  手動テスト:"
echo "    cd $INSTALL_DIR && source venv/bin/activate"
echo "    python scripts/daily_run.py              # パイプラインテスト"
echo "    xvfb-run python scripts/x_daily_post.py  # X投稿テスト"
echo ""
echo "  初回X投稿時にログインが必要です。"
echo "  ログインに失敗する場合は手動でブラウザプロファイルを作成:"
echo "    xvfb-run python -c \"from playwright.sync_api import sync_playwright; p=sync_playwright().start(); c=p.chromium.launch_persistent_context('$INSTALL_DIR/data/x_browser_profile', headless=False); input('Login manually then press Enter'); c.close(); p.stop()\""
echo ""
echo "  ログ確認:"
echo "    tail -f $INSTALL_DIR/logs/cron_daily.log"
echo "    tail -f $INSTALL_DIR/logs/cron_xpost.log"
echo ""
echo "  タイムゾーンが JST でない場合:"
echo "    sudo timedatectl set-timezone Asia/Tokyo"
echo ""
