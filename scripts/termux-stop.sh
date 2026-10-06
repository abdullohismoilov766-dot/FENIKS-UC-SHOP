#!/data/data/com.termux/files/usr/bin/bash
# Botni to'xtatadi.
if pkill -f "planner_bot.bot"; then
    echo "🛑 Bot to'xtatildi."
else
    echo "ℹ️  Bot ishlamayotgan edi."
fi
termux-wake-unlock 2>/dev/null || true
