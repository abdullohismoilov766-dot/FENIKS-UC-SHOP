"""
Planner bot sozlamalari.

Barcha maxfiy qiymatlar (tokenlar, kalitlar) .env faylidan o'qiladi —
namuna uchun planner_bot/.env.example ga qarang.
"""

import importlib.util
import os

from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------------- Telegram ---
BOT_TOKEN = os.getenv("PLANNER_BOT_TOKEN") or os.getenv("BOT_TOKEN", "")

# ---------------------------------------------------------------- Umumiy ----
# Standart vaqt mintaqasi. Har bir foydalanuvchi /sozlamalar orqali o'zgartira oladi.
DEFAULT_TZ = os.getenv("TIMEZONE", "Asia/Tashkent")

# Bo'sh vaqt hisoblanadigan "faol kun" oralig'i (standart qiymat).
DEFAULT_DAY_START = os.getenv("DAY_START", "09:00")
DEFAULT_DAY_END = os.getenv("DAY_END", "22:00")

# Bo'sh vaqt sifatida ko'rsatiladigan eng qisqa oraliq (daqiqa).
MIN_FREE_SLOT_MIN = int(os.getenv("MIN_FREE_SLOT_MIN", "20"))

# Deadline savolига javob berilmasa, necha soatdan keyin "bajarilmadi" deb
# belgilansin (foydalanuvchi keyinroq tugmani bossa, holat baribir yangilanadi).
AUTO_MISS_HOURS = int(os.getenv("AUTO_MISS_HOURS", "6"))

# Scheduler necha soniyada bir marta tekshirsin.
TICK_SECONDS = int(os.getenv("TICK_SECONDS", "60"))

# Tekin hosting tariflari (Render, Koyeb) dasturdan port ochishni talab qiladi.
# Ular PORT o'zgaruvchisini o'zi qo'yadi; qo'yilmagan bo'lsa sahifa ochilmaydi.
try:
    PORT = int(os.getenv("PORT", "") or 0)
except ValueError:
    PORT = 0

DB_PATH = os.getenv(
    "PLANNER_DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "planner.db"),
)

# ------------------------------------------------------------- Claude API ---
# Ovozli/matnli erkin xabarlarni ("ertaga soat 3 da stomatolog") tushunish uchun.
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-5")

# ----------------------------------------------------------------- Notion ---
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")
# Notion bazangizdagi ustun (property) nomlari — o'zingiznikiga moslang.
NOTION_TITLE_PROP = os.getenv("NOTION_TITLE_PROP", "Name")
NOTION_DATE_PROP = os.getenv("NOTION_DATE_PROP", "Date")
NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")

# -------------------------------------------------- Ovozni matnga o'girish ---
# OpenAI-mos (Whisper) transkripsiya endpoint'i. Kalit qo'yilmasa, ovozli
# xabarlar o'chirilgan bo'ladi va bot matn yozishni so'raydi.
STT_API_URL = os.getenv("STT_API_URL", "https://api.openai.com/v1/audio/transcriptions")
STT_API_KEY = os.getenv("STT_API_KEY", "")
STT_MODEL = os.getenv("STT_MODEL", "whisper-1")
STT_LANGUAGE = os.getenv("STT_LANGUAGE", "uz")


def claude_enabled() -> bool:
    """Kalit ham, kutubxona ham bor bo'lsagina Claude ishlatiladi."""
    if not ANTHROPIC_API_KEY:
        return False
    return importlib.util.find_spec("anthropic") is not None


def notion_enabled() -> bool:
    return bool(NOTION_TOKEN and NOTION_DATABASE_ID)


def stt_enabled() -> bool:
    return bool(STT_API_KEY)
