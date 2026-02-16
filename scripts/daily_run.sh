#!/bin/bash
set -euo pipefail
BASEDIR="$(cd "$(dirname "$0")/.." && pwd)"
DATE=$(date +%Y-%m-%d)
LOGFILE="$BASEDIR/logs/daily_${DATE}.log"
mkdir -p "$BASEDIR/logs"

echo "===== Money Machine Daily: $DATE =====" | tee -a "$LOGFILE"
cd "$BASEDIR"

echo "[$(date +%H:%M:%S)] SIM scraping" | tee -a "$LOGFILE"
python scrapers/sim_scraper.py >> "$LOGFILE" 2>&1 || echo "WARN: scraper" >> "$LOGFILE"

echo "[$(date +%H:%M:%S)] HTML generation" | tee -a "$LOGFILE"
python generators/comparison_generator.py >> "$LOGFILE" 2>&1 || echo "WARN: html" >> "$LOGFILE"

echo "[$(date +%H:%M:%S)] Image generation" | tee -a "$LOGFILE"
python generators/social_image_generator.py >> "$LOGFILE" 2>&1 || echo "WARN: image" >> "$LOGFILE"

echo "[$(date +%H:%M:%S)] Status" | tee -a "$LOGFILE"
python scripts/status.py >> "$LOGFILE" 2>&1 || echo "WARN: status" >> "$LOGFILE"

echo "===== Done: $(date +%H:%M:%S) =====" | tee -a "$LOGFILE"
