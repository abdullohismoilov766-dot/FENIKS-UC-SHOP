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
REQ="$APP_DIR/planner_bot/requirements.txt"

say()  { printf '\n\033[1m%s\033[0m\n' "$*"; }
warn() { printf '\033[33m  %s\033[0m\n' "$*"; }
die()  { printf '\n\033[31m✖ %s\033[0m\n' "$*" >&2; exit 1; }

say "1/5  Kerakli dasturlar o'rnatilmoqda…"
pkg update -y >/dev/null 2>&1 || warn "pkg update to'liq bajarilmadi — davom etamiz."
pkg install -y python git >/dev/null

say "2/5  Kod yuklab olinmoqda…"
if [ -d "$APP_DIR/.git" ]; then
    git -C "$APP_DIR" fetch origin "$BRANCH"
    git -C "$APP_DIR" checkout "$BRANCH"
    git -C "$APP_DIR" pull origin "$BRANCH"
else
    git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi

say "3/5  Kutubxonalar o'rnatilmoqda…"
cd "$APP_DIR"
pip install --quiet --upgrade pip 2>/dev/null || true

install_ok=0

# 1-urinish: tayyor paketlar bilan (tez)
echo "  Tez usul sinalmoqda…"
if pip install -r "$REQ" >/dev/null 2>&1; then
    install_ok=1
fi

# 2-urinish: Termux'ning o'z tayyor paketlaridan foydalanamiz
if [ "$install_ok" -eq 0 ]; then
    warn "Tayyor paket topilmadi. Termux omboridan sinab ko'ramiz…"
    pkg install -y tur-repo >/dev/null 2>&1 || true
    pkg install -y python-pydantic >/dev/null 2>&1 || true
    if pip install -r "$REQ" >/dev/null 2>&1; then
        install_ok=1
    fi
fi

# 3-urinish: joyida kompilyatsiya (sekin, lekin ishonchli)
if [ "$install_ok" -eq 0 ]; then
    warn "Endi kutubxonalar telefonda kompilyatsiya qilinadi."
    warn "Bu 15–40 daqiqa davom etishi mumkin — telefonni zaryadda qoldiring"
    warn "va Termux'ni yopmang. Ekran o'chsa ham davom etadi."
    echo
    pkg install -y clang make binutils libffi openssl rust >/dev/null

    # Termux'da Rust paketlarini yig'ish uchun maqsad platformani ko'rsatish shart
    case "$(uname -m)" in
        aarch64) export CARGO_BUILD_TARGET="aarch64-linux-android" ;;
        armv7l|arm) export CARGO_BUILD_TARGET="armv7-linux-androideabi" ;;
        x86_64)  export CARGO_BUILD_TARGET="x86_64-linux-android" ;;
    esac

    if pip install -r "$REQ"; then
        install_ok=1
    fi
fi

if [ "$install_ok" -eq 0 ]; then
    die "Kutubxonalarni o'rnatib bo'lmadi.
  Yuqoridagi oxirgi xato matnini nusxalab yuboring — boshqa yo'lini topamiz.
  Muqobil variantlar DEPLOY.md faylida bor."
fi
echo "  ✅ Kutubxonalar o'rnatildi."

say "4/5  Avtomatik ishga tushish sozlanmoqda…"
termux-wake-lock 2>/dev/null || warn "termux-wake-lock topilmadi — muhim emas."

mkdir -p "$HOME/.termux/boot"
cp "$APP_DIR/scripts/termux-boot.sh" "$HOME/.termux/boot/feniks-planner.sh"
chmod +x "$HOME/.termux/boot/feniks-planner.sh"
echo "  Telefon qayta yonganda bot o'zi ishga tushadi."
echo "  Buning uchun F-Droid'dan 'Termux:Boot' ilovasini o'rnating va"
echo "  uni bir marta ochib qo'ying — aks holda ishlamaydi."

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

Eslatma: "erkin matnni tushunish" (ovoz/matn -> kalendar) imkoniyati
alohida o'rnatiladi va telefonda uzoq davom etadi:

    pip install -r planner_bot/requirements-ai.txt
MSG
