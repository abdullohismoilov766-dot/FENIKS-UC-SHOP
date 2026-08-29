#!/usr/bin/env bash
#
# FENIKS PLANNER — serverdagi botni yangilash.
# Kodni tortib oladi, kutubxonalarni yangilaydi va xizmatni qayta yoqadi.
#
#   sudo bash /opt/feniks/scripts/server-update.sh
#
set -euo pipefail

APP_DIR="/opt/feniks"
APP_USER="feniks"
SERVICE="feniks-planner"

[ "$(id -u)" -eq 0 ] || { echo "Root huquqi kerak: sudo bash $0" >&2; exit 1; }
[ -d "$APP_DIR/.git" ] || { echo "$APP_DIR topilmadi. Avval server-install.sh ni bajaring." >&2; exit 1; }

echo "Kod yangilanmoqda…"
git -C "$APP_DIR" pull --ff-only

echo "Kutubxonalar tekshirilmoqda…"
"$APP_DIR/venv/bin/pip" install --quiet -r "$APP_DIR/planner_bot/requirements.txt"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

echo "Xizmat qayta ishga tushirilmoqda…"
systemctl restart "$SERVICE"
sleep 3

if systemctl is-active --quiet "$SERVICE"; then
    echo "✅ Yangilandi va ishlayapti."
else
    echo "❌ Bot ishga tushmadi:"
    journalctl -u "$SERVICE" -n 30 --no-pager
    exit 1
fi
