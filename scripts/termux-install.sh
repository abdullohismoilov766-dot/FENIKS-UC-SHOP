#!/data/data/com.termux/files/usr/bin/bash
#
# FENIKS PLANNER — Android telefonga (Termux) o'rnatish.
#
# Ishlatish (Termux'da):
#   pkg install -y git && \
#   git clone https://github.com/abdullohismoilov766-dot/FENIKS-UC-SHOP.git && \
#   bash FENIKS-UC-SHOP/scripts/termux-install.sh
#
set -euo pipefail

REPO_URL="https://github.com/abdullohismoilov766-dot/FENIKS-UC-SHOP.git"
BRANCH="claude/daily-plan-tracker-bot-069e57"
APP_DIR="$HOME/FENIKS-UC-SHOP"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

say "1/5  Kerakli dasturlar o'rnatilmoqda…"
pkg update -y >/dev/null
pkg install -y python git >/dev/null

say "2/5  Kod yuklab olinmoqda…"
if [ -d "$APP_DIR/.git" ]; then
    git -C "$APP_DIR" fetch origin "$BRANCH"
    git -C "$APP_DIR" checkout "$BRANCH"
    git -C "$APP_DIR" pull origin "$BRANCH"
else
    git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi

say "3/5  Kutubxonalar o'rnatilmoqda (biroz vaqt oladi)…"
cd "$APP_DIR"
pip install --quiet --upgrade pip
pip install --quiet -r planner_bot/requirements.txt

say "4/5  Telefon uxlab qolmasligi sozlanmoqda…"
termux-wake-lock 2>/dev/null || echo "  (termux-wake-lock topilmadi — muhim emas)"

mkdir -p "$HOME/.termux/boot"
cp "$APP_DIR/scripts/termux-boot.sh" "$HOME/.termux/boot/feniks-planner.sh"
chmod +x "$HOME/.termux/boot/feniks-planner.sh"
echo "  Telefon qayta yonganda bot o'zi ishga tushadi."
echo "  Buning uchun F-Droid'dan 'Termux:Boot' ilovasini ham o'rnating"
echo "  va uni bir marta ochib qo'ying."

say "5/5  Endi kalitlarni kiritamiz."
echo "BotFather bergan tokenni tayyorlab qo'ying."
echo
PLANNER_SETUP_EMBEDDED=1 python -m planner_bot.setup

say "✅ Tayyor!"
cat <<'MSG'
Botni ishga tushirish:

    cd ~/FENIKS-UC-SHOP
    bash scripts/termux-start.sh

Keyin Telegramda botingizga /start yuboring.
MSG
