"""
FENIKS UC SERVICE — bot sozlamalari.

Barcha maxfiy va tez-tez o'zgaradigan qiymatlar (token, admin ID, narxlar)
shu faylda va .env faylida saqlanadi — kodning qolgan qismini o'zgartirmasdan
narxlarni yoki tokenni yangilash mumkin.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

_admin_ids_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(x.strip()) for x in _admin_ids_raw.split(",") if x.strip().isdigit()]

CARD_NUMBER = os.getenv("CARD_NUMBER", "8600 0000 0000 0000")
CARD_HOLDER = os.getenv("CARD_HOLDER", "F.I.SH.")
CONTACT_USERNAME = os.getenv("CONTACT_USERNAME", "@support")

DB_PATH = os.path.join(os.path.dirname(__file__), "orders.db")

# PUBG Mobile UC paketlari va narxlari (so'mda).
# Bu yerdagi raqamlar NAMUNA — o'z narxlaringizni kiriting.
UC_PACKAGES = [
    {"id": "uc_60", "amount": 60, "price": 12.600},
    {"id": "uc_325", "amount": 325, "price": 63.000},
    {"id": "uc_660", "amount": 660, "price": 130.000},
    {"id": "uc_1800", "amount": 1800, "price": 330.000},
    {"id": "uc_3850", "amount": 3850, "price": 660.000},
    {"id": "uc_8100", "amount": 8100, "price": 1.280.000},
]

FAQ_TEXT = (
    "❓ <b>Tez-tez so'raladigan savollar</b>\n\n"
    "<b>UC qancha vaqtda tushadi?</b>\n"
    "To'lov tasdiqlangandan so'ng odatda 5–30 daqiqa ichida hisobingizga tushadi.\n\n"
    "<b>To'lovni qanday amalga oshiraman?</b>\n"
    "Kerakli UC paketini tanlang, PUBG ID raqamingizni yuboring, so'ng ko'rsatilgan "
    "karta raqamiga to'lov qiling va chekni (skrinshot) botga yuboring.\n\n"
    "<b>Agar chek tasdiqlanmasa-chi?</b>\n"
    "Admin chekni tekshiradi. Muammo bo'lsa siz bilan bog'lanadi yoki botdan xabar keladi.\n\n"
    "<b>Qo'shimcha savollar bo'lsa</b>\n"
    f"{CONTACT_USERNAME} ga yozing."
)
