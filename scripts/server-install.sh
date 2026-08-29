#!/usr/bin/env bash
#
# FENIKS PLANNER — Linux serverga (Oracle Cloud, VPS) o'rnatish.
# Ubuntu/Debian uchun. Bot systemd xizmati sifatida doimiy ishlaydi:
# server qayta yonsa ham o'zi tiklanadi.
#
# Ishlatish:
#   curl -fsSL https://raw.githubusercontent.com/abdullohismoilov766-dot/FENIKS-UC-SHOP/claude/daily-plan-tracker-bot-069e57/scripts/server-install.sh -o install.sh
#   sudo bash install.sh
#
set -euo pipefail

REPO_URL="https://github.com/abdullohismoilov766-dot/FENIKS-UC-SHOP.git"
BRANCH="claude/daily-plan-tracker-bot-069e57"
APP_DIR="/opt/feniks"
APP_USER="feniks"
SERVICE="feniks-planner"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }
die() { printf '\n\033[31m✖ %s\033[0m\n' "$*" >&2; exit 1; }

# Yangi serverda birinchi daqiqalarda avtomatik yangilanish ishlab turadi va
# apt'ni band qiladi. Shuning uchun qayta urinib ko'ramiz.
apt_retry() {
    local n=0
    until DEBIAN_FRONTEND=noninteractive apt-get "$@"; do
        n=$((n + 1))
        if [ "$n" -ge 20 ]; then
            die "apt 5 daqiqa davomida band bo'ldi. Bir necha daqiqadan keyin qayta urinib ko'ring."
        fi
        echo "  apt band (tizim yangilanmoqda) — 15 soniyadan keyin qayta urinamiz ($n/20)…"
        sleep 15
    done
}

[ "$(id -u)" -eq 0 ] || die "Bu skript root huquqi bilan ishlashi kerak: sudo bash $0"
command -v apt-get >/dev/null || die "Bu skript Ubuntu/Debian uchun. Boshqa tizimda qadamlarni DEPLOY.md dan qo'lda bajaring."

say "1/6  Kerakli dasturlar o'rnatilmoqda…"
echo "  Tizim: $(. /etc/os-release && echo "$PRETTY_NAME")  ($(uname -m))"
export DEBIAN_FRONTEND=noninteractive
apt_retry update -qq
apt_retry install -y -qq python3 python3-venv python3-pip git tzdata

say "2/6  Xizmat foydalanuvchisi tayyorlanmoqda…"
if ! id -u "$APP_USER" >/dev/null 2>&1; then
    useradd --system --home-dir "$APP_DIR" --shell /usr/sbin/nologin "$APP_USER"
    echo "  '$APP_USER' foydalanuvchisi yaratildi."
else
    echo "  '$APP_USER' allaqachon mavjud."
fi

say "3/6  Kod yuklab olinmoqda…"
if [ -d "$APP_DIR/.git" ]; then
    git -C "$APP_DIR" fetch origin "$BRANCH"
    git -C "$APP_DIR" checkout "$BRANCH"
    git -C "$APP_DIR" pull origin "$BRANCH"
else
    mkdir -p "$APP_DIR"
    git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

say "4/6  Kutubxonalar o'rnatilmoqda…"
[ -d "$APP_DIR/venv" ] || python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --quiet --upgrade pip

if ! "$APP_DIR/venv/bin/pip" install --quiet -r "$APP_DIR/planner_bot/requirements.txt"; then
    echo "  Tayyor paket topilmadi — kompilyatsiya vositalari o'rnatilmoqda…"
    apt_retry install -y -qq build-essential python3-dev
    "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/planner_bot/requirements.txt" \
        || die "Kutubxonalarni o'rnatib bo'lmadi. Yuqoridagi xato matnini yuboring."
fi
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

say "5/6  Endi kalitlarni kiritamiz."
if [ -f "$APP_DIR/planner_bot/.env" ]; then
    echo "  Mavjud sozlama topildi — Enter bosib eski qiymatlarni saqlab qolasiz."
fi
echo "  BotFather bergan tokenni tayyorlab qo'ying."
echo
cd "$APP_DIR"
# runuser util-linux tarkibida — sudo o'rnatilmagan tizimlarda ham ishlaydi
if command -v runuser >/dev/null; then
    PLANNER_SETUP_EMBEDDED=1 runuser -u "$APP_USER" -- "$APP_DIR/venv/bin/python" -m planner_bot.setup
else
    PLANNER_SETUP_EMBEDDED=1 sudo -u "$APP_USER" "$APP_DIR/venv/bin/python" -m planner_bot.setup
fi
chmod 600 "$APP_DIR/planner_bot/.env"
chown "$APP_USER:$APP_USER" "$APP_DIR/planner_bot/.env"

say "6/6  Doimiy xizmat sozlanmoqda…"
cat > "/etc/systemd/system/${SERVICE}.service" <<UNIT
[Unit]
Description=FENIKS Planner Telegram bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${APP_USER}
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/venv/bin/python -m planner_bot.bot
Restart=always
RestartSec=10

# Xavfsizlik cheklovlari
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=${APP_DIR}

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now "$SERVICE" >/dev/null 2>&1

sleep 4
if systemctl is-active --quiet "$SERVICE"; then
    say "✅ Tayyor! Bot ishlayapti va server qayta yonsa ham o'zi tiklanadi."
    cat <<MSG

Foydali buyruqlar:
    sudo systemctl status ${SERVICE}      # holati
    sudo journalctl -u ${SERVICE} -f      # jonli loglar
    sudo systemctl restart ${SERVICE}     # qayta ishga tushirish

Endi Telegramda botingizga /start yuboring.
MSG
else
    die "Bot ishga tushmadi. Sababini ko'rish uchun:  sudo journalctl -u ${SERVICE} -n 50"
fi
