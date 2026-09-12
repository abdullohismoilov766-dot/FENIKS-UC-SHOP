#!/data/data/com.termux/files/usr/bin/bash
#
# Botni fonda ishga tushiradi (Termux'ni yopsangiz ham ishlayveradi).
#
set -euo pipefail

APP_DIR="$HOME/FENIKS-UC-SHOP"
LOG="$HOME/feniks-planner.log"

if pgrep -f "planner_bot.bot" >/dev/null 2>&1; then
    echo "ℹ️  Bot allaqachon ishlayapti."
    echo "   To'xtatish:  bash scripts/termux-stop.sh"
    exit 0
fi

termux-wake-lock 2>/dev/null || true
cd "$APP_DIR"
nohup python -m planner_bot.bot >> "$LOG" 2>&1 &

sleep 3
if pgrep -f "planner_bot.bot" >/dev/null 2>&1; then
    echo "✅ Bot ishga tushdi. Telegramda /start yuboring."
    echo "   Loglar:      tail -f $LOG"
    echo "   To'xtatish:  bash scripts/termux-stop.sh"
else
    echo "❌ Bot ishga tushmadi. Xato sababi:"
    tail -20 "$LOG"
    exit 1
fi
