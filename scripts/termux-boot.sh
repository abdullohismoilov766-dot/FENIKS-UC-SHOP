#!/data/data/com.termux/files/usr/bin/sh
#
# Telefon qayta yonganda botni avtomatik ishga tushiradi.
# Termux:Boot ilovasi shu faylni ~/.termux/boot/ dan o'zi topib ishga tushiradi.
#
termux-wake-lock
cd "$HOME/FENIKS-UC-SHOP" || exit 1
exec python -m planner_bot.bot >> "$HOME/feniks-planner.log" 2>&1
