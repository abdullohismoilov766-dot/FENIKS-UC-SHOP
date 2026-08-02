import telebot
from telebot import types
import json
import os

# ============ SOZLAMALAR ============
BOT_TOKEN = "8619621800:AAHWPEWxenFy8eBRO1GKGrH5RADZ0v3KClE"  # @BotFather'dan olingan token
ADMIN_ID = 1127783022                                      # Sizning Telegram ID raqamingiz (@userinfobot orqali oling)
WEBAPP_URL = "https://abdullohismoilov766-dot.github.io/FENIKS-UC-SHOP/feniks-uc-shop.html"  # Hostlangan buyurtma sahifasi manzili
# =====================================

bot = telebot.TeleBot(BOT_TOKEN)

PACKAGES = [
    {"uc": 30,    "price": 6000},
    {"uc": 60,    "price": 12200},
    {"uc": 325,   "price": 60000},
    {"uc": 660,   "price": 122000},
    {"uc": 1800,  "price": 303000},
    {"uc": 3850,  "price": 610000},
    {"uc": 8100,  "price": 1220000},
    {"uc": 16200, "price": 2420000},
    {"uc": 24300, "price": 3600000},
    {"uc": 32400, "price": 4990000},
    {"uc": 40500, "price": 6150000},
    {"uc": 48600, "price": 7330000},
    {"uc": 81000, "price": 12110000},
]

ORDERS_FILE = "orders.json"


def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_orders(data):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fmt(n):
    return f"{n:,}".replace(",", " ")


def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("🛒 UC sotib olish", web_app=types.WebAppInfo(WEBAPP_URL)))
    kb.add(types.KeyboardButton("💰 Narxlar"), types.KeyboardButton("📦 Buyurtmalarim"))
    kb.add(types.KeyboardButton("❓ Yordam"))
    return kb


@bot.message_handler(commands=["start"])
def cmd_start(message):
    text = (
        "🔥 *FENIKS UC SHOP*ga xush kelibsiz!\n\n"
        "Bu yerda PUBG Mobile UC'ni eng maqbul narxda sotib olishingiz mumkin.\n\n"
        "Boshlash uchun pastdagi tugmalardan birini tanlang 👇"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu(), parse_mode="Markdown")


@bot.message_handler(commands=["buy"])
def cmd_buy(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("🛒 Buyurtma sahifasini ochish", web_app=types.WebAppInfo(WEBAPP_URL)))
    bot.send_message(message.chat.id, "Paket tanlash uchun tugmani bosing 👇", reply_markup=kb)


@bot.message_handler(commands=["prices"])
def cmd_prices(message):
    lines = ["💰 *Narxlar jadvali:*\n"]
    for p in PACKAGES:
        lines.append(f"• {fmt(p['uc'])} UC — {fmt(p['price'])} so'm")
    bot.send_message(message.chat.id, "\n".join(lines), parse_mode="Markdown")


@bot.message_handler(commands=["myorders"])
def cmd_myorders(message):
    orders = load_orders()
    user_orders = orders.get(str(message.from_user.id), [])
    if not user_orders:
        bot.send_message(message.chat.id, "Sizda hali buyurtmalar yo'q.")
        return
    lines = ["📦 *Sizning buyurtmalaringiz:*\n"]
    for o in user_orders[-10:]:
        lines.append(f"• {fmt(o['package_uc'])} UC — {fmt(o['price_uzs'])} so'm — {o.get('nickname', '-')} — {o.get('status', 'kutilmoqda')}")
    bot.send_message(message.chat.id, "\n".join(lines), parse_mode="Markdown")


@bot.message_handler(commands=["help"])
def cmd_help(message):
    text = (
        "❓ *Yordam*\n\n"
        "/buy — UC sotib olish\n"
        "/prices — Narxlar jadvali\n"
        "/myorders — Buyurtmalaringiz tarixi\n\n"
        "Savollar bo'lsa, admin bilan bog'laning."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


# Menyudagi matnli tugmalar bosilganda ham ishlashi uchun
@bot.message_handler(func=lambda m: m.text == "💰 Narxlar")
def btn_prices(message):
    cmd_prices(message)


@bot.message_handler(func=lambda m: m.text == "📦 Buyurtmalarim")
def btn_orders(message):
    cmd_myorders(message)


@bot.message_handler(func=lambda m: m.text == "❓ Yordam")
def btn_help(message):
    cmd_help(message)


# Web App orqali yuborilgan buyurtmani qabul qilish
@bot.message_handler(content_types=["web_app_data"])
def handle_webapp_data(message):
    try:
        data = json.loads(message.web_app_data.data)
    except Exception:
        bot.send_message(message.chat.id, "Xatolik: buyurtma o'qilmadi.")
        return

    data["status"] = "kutilmoqda"
    data["user_id"] = message.from_user.id
    data["username"] = message.from_user.username or message.from_user.first_name

    orders = load_orders()
    uid = str(message.from_user.id)
    orders.setdefault(uid, []).append(data)
    save_orders(orders)

    bot.send_message(
        message.chat.id,
        "✅ Buyurtmangiz qabul qilindi!\n\n"
        f"{fmt(data['package_uc'])} UC — {fmt(data['price_uzs'])} so'm\n"
        f"PUBG ID: {data['pubg_id']}\n"
        f"Nickname: {data.get('nickname', '-')}\n\n"
        "Tez orada tasdiqlanadi.",
    )

    admin_text = (
        "🆕 Yangi buyurtma!\n\n"
        f"Mijoz: @{data['username']} (ID: {data['user_id']})\n"
        f"Paket: {fmt(data['package_uc'])} UC\n"
        f"Narx: {fmt(data['price_uzs'])} so'm\n"
        f"PUBG ID: {data['pubg_id']}\n"
        f"Nickname: {data.get('nickname', '-')}"
    )
    bot.send_message(ADMIN_ID, admin_text)


print("Bot ishga tushdi...")
bot.remove_webhook()
bot.infinity_polling()
