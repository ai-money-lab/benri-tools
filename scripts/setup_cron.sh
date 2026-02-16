#!/bin/bash
SCRIPT="$(cd "$(dirname "$0")" && pwd)/daily_run.sh"
chmod +x "$SCRIPT"
(crontab -l 2>/dev/null | grep -v daily_run; echo "0 6 * * * $SCRIPT") | crontab -
echo "Cron set: daily_run.sh at 06:00"
