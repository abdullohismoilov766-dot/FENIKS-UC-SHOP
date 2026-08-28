"""
Sozlash yordamchisi — `.env` faylini interaktiv tarzda yaratadi.

Ishlatish (repozitoriy ildizidan):

    python -m planner_bot.setup

Skript har bir qiymatni so'raydi, tekshiradi va planner_bot/.env fayliga
yozadi. Maxfiy qiymatlar ekranga qayta chiqarilmaydi va fayl faqat siz
o'qiy oladigan huquq bilan saqlanadi.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent / ".env"

TOKEN_RE = re.compile(r"^\d{6,}:[A-Za-z0-9_-]{30,}$")
HHMM_RE = re.compile(r"^([01]?\d|2[0-3]):[0-5]\d$")


@dataclass
class Field:
    key: str
    prompt: str
    help_text: str = ""
    default: str = ""
    secret: bool = False
    required: bool = False
    validator: object = None
    enables: str = ""
    group: str = ""
    depends_on: str = ""


def _valid_token(value: str) -> str:
    if not TOKEN_RE.match(value):
        return "Token '123456789:AAE...' ko'rinishida bo'lishi kerak."
    return ""


def _valid_tz(value: str) -> str:
    try:
        from zoneinfo import ZoneInfo

        ZoneInfo(value)
    except Exception:
        return "Bunday vaqt mintaqasi topilmadi. Masalan: Asia/Tashkent"
    return ""


def _valid_hhmm(value: str) -> str:
    if not HHMM_RE.match(value):
        return "Vaqt HH:MM ko'rinishida bo'lsin, masalan 09:00"
    return ""


def _valid_notion_db(value: str) -> str:
    cleaned = value.replace("-", "")
    if len(cleaned) != 32 or not re.fullmatch(r"[0-9a-fA-F]{32}", cleaned):
        return "Baza ID 32 ta belgidan iborat bo'lishi kerak (havoladan olinadi)."
    return ""


FIELDS: list[Field] = [
    Field(
        key="PLANNER_BOT_TOKEN",
        prompt="Telegram bot tokeni",
        help_text=(
            "@BotFather ga /newbot yuboring, bot nomini va username'ini tanlang.\n"
            "  BotFather sizga '123456789:AAE...' ko'rinishidagi tokenni beradi."
        ),
        secret=True,
        required=True,
        validator=_valid_token,
        group="Telegram",
    ),
    Field(
        key="TIMEZONE",
        prompt="Vaqt mintaqangiz",
        help_text="O'zbekiston uchun Asia/Tashkent. Boshqa: Europe/Moscow, Asia/Almaty",
        default="Asia/Tashkent",
        validator=_valid_tz,
        group="Umumiy",
    ),
    Field(
        key="DAY_START",
        prompt="Kuningiz necha soatda boshlanadi",
        help_text="Bo'sh vaqt shu oraliq ichida hisoblanadi.",
        default="09:00",
        validator=_valid_hhmm,
        group="Umumiy",
    ),
    Field(
        key="DAY_END",
        prompt="Kuningiz necha soatda tugaydi",
        default="22:00",
        validator=_valid_hhmm,
        group="Umumiy",
    ),
    Field(
        key="ANTHROPIC_API_KEY",
        prompt="Anthropic (Claude) API kaliti",
        help_text=(
            "console.anthropic.com -> Settings -> API Keys -> Create Key.\n"
            "  Bu 'ertaga soat 3 da stomatolog' kabi erkin gaplarni tushunish uchun.\n"
            "  Bo'sh qoldirsangiz bot oddiy rejimda ishlaydi (kamroq tushunadi)."
        ),
        secret=True,
        enables="erkin matnni tushunish",
        group="Claude",
    ),
    Field(
        key="NOTION_TOKEN",
        prompt="Notion integratsiya kaliti",
        help_text=(
            "notion.so/my-integrations -> New integration -> Internal Integration Secret.\n"
            "  Keyin kalendar bazangizni oching -> ••• -> Connections -> shu integratsiyani ulang."
        ),
        secret=True,
        enables="Notion kalendar",
        group="Notion",
    ),
    Field(
        key="NOTION_DATABASE_ID",
        prompt="Notion kalendar bazasining ID si",
        help_text=(
            "Baza havolasidagi 32 belgili qism:\n"
            "  notion.so/ish/[a1b2c3d4e5f6...]?v=... — kvadrat qavs ichidagisi."
        ),
        validator=_valid_notion_db,
        depends_on="NOTION_TOKEN",
        group="Notion",
    ),
    Field(
        key="NOTION_TITLE_PROP",
        prompt="Bazadagi sarlavha ustuni nomi",
        default="Name",
        depends_on="NOTION_TOKEN",
        group="Notion",
    ),
    Field(
        key="NOTION_DATE_PROP",
        prompt="Bazadagi sana ustuni nomi",
        default="Date",
        depends_on="NOTION_TOKEN",
        group="Notion",
    ),
    Field(
        key="STT_API_KEY",
        prompt="Ovozni matnga o'giruvchi xizmat kaliti",
        help_text=(
            "Whisper'ga mos xizmat kaliti (masalan OpenAI: platform.openai.com/api-keys).\n"
            "  Bo'sh qoldirsangiz ovozli xabarlar o'chiq bo'ladi, matn baribir ishlaydi."
        ),
        secret=True,
        enables="ovozli xabarlar",
        group="Ovoz",
    ),
]


def _mask(value: str) -> str:
    if len(value) <= 8:
        return "•" * len(value)
    return f"{value[:4]}{'•' * 8}{value[-4:]}"


def _read_existing() -> dict[str, str]:
    if not ENV_PATH.exists():
        return {}
    values: dict[str, str] = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values


def _ask(field: Field, existing: str) -> str:
    if field.help_text:
        print(f"\n  ℹ️  {field.help_text}")

    shown_default = existing or field.default
    hint = ""
    if existing:
        hint = f" [hozirgi: {_mask(existing) if field.secret else existing}]"
    elif field.default:
        hint = f" [{field.default}]"
    elif not field.required:
        hint = " [ixtiyoriy — Enter bilan o'tkazib yuboring]"

    while True:
        answer = input(f"  {field.prompt}{hint}: ").strip()
        if not answer:
            answer = shown_default
        if not answer:
            if field.required:
                print("  ⚠️  Bu qiymat majburiy.")
                continue
            return ""
        if field.validator:
            error = field.validator(answer)
            if error:
                print(f"  ⚠️  {error}")
                continue
        return answer


def main() -> int:
    print("=" * 62)
    print("  FENIKS PLANNER — sozlash")
    print("=" * 62)
    print(
        "\nHar bir savolga javob yozing. Ixtiyoriy savollarni Enter bosib\n"
        "o'tkazib yuborsangiz, o'sha imkoniyat o'chiq qoladi — bot baribir ishlaydi."
    )

    existing = _read_existing()
    if existing:
        print(f"\n📄 Mavjud sozlama topildi: {ENV_PATH}")
        print("   Enter bossangiz eski qiymat saqlanib qoladi.")

    values: dict[str, str] = {}
    current_group = ""

    for field in FIELDS:
        if field.depends_on and not values.get(field.depends_on):
            continue
        if field.group != current_group:
            current_group = field.group
            print(f"\n{'─' * 62}\n  {current_group}\n{'─' * 62}")
        values[field.key] = _ask(field, existing.get(field.key, ""))

    # Foydalanuvchi so'ramagan, lekin kerak bo'ladigan qiymatlar
    passthrough = {
        "CLAUDE_MODEL": existing.get("CLAUDE_MODEL", "claude-opus-5"),
        "MIN_FREE_SLOT_MIN": existing.get("MIN_FREE_SLOT_MIN", "20"),
        "AUTO_MISS_HOURS": existing.get("AUTO_MISS_HOURS", "6"),
        "TICK_SECONDS": existing.get("TICK_SECONDS", "60"),
        "STT_API_URL": existing.get(
            "STT_API_URL", "https://api.openai.com/v1/audio/transcriptions"
        ),
        "STT_MODEL": existing.get("STT_MODEL", "whisper-1"),
        "STT_LANGUAGE": existing.get("STT_LANGUAGE", "uz"),
    }

    lines = ["# FENIKS PLANNER sozlamalari — bu faylni hech kimga bermang!", ""]
    for field in FIELDS:
        value = values.get(field.key, "")
        lines.append(f"{field.key}={value}")
    lines.append("")
    for key, value in passthrough.items():
        lines.append(f"{key}={value}")
    lines.append("")

    ENV_PATH.write_text("\n".join(lines))
    try:
        os.chmod(ENV_PATH, 0o600)
    except OSError:
        pass

    print(f"\n{'=' * 62}")
    print(f"✅ Saqlandi: {ENV_PATH}")
    print("=" * 62)
    print("\nYoqilgan imkoniyatlar:")
    print("  ✅ Kundalik rejalar, eslatmalar, Ha/Yo'q savoli, statistika")
    for field in FIELDS:
        if field.enables:
            mark = "✅" if values.get(field.key) else "⬜"
            print(f"  {mark} {field.enables.capitalize()}")

    print("\nEndi botni ishga tushiring:\n\n    python -m planner_bot.bot\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n🚫 Bekor qilindi. Hech narsa saqlanmadi.")
        sys.exit(1)
