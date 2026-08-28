"""
Erkin matnni (yoki ovozdan o'girilgan matnni) tushunish — Claude API orqali.

Foydalanuvchi "ertaga soat 3 da stomatologga boraman, uni kalendarga yozib qo'y"
deb yozganda yoki aytganda, shu modul uni tuzilgan JSON ga aylantiradi:

    {"intent": "add_event", "title": "Stomatolog", "date": "2026-08-29",
     "start_time": "15:00", "end_time": "16:00", ...}

Claude kaliti (ANTHROPIC_API_KEY) qo'yilmagan bo'lsa, modul oddiy regex bilan
ishlaydigan zaxira rejimiga o'tadi — bot baribir ishlaydi, faqat kamroq tushunadi.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import date, datetime, timedelta

from planner_bot.config import ANTHROPIC_API_KEY, CLAUDE_MODEL, claude_enabled
from planner_bot.timeutil import WEEKDAY_KEYS, parse_hhmm

logger = logging.getLogger(__name__)

INTENTS = ("add_event", "add_task", "free_time", "stats", "list_tasks", "unknown")

# Barcha maydonlar majburiy — bo'sh qiymat "" bilan beriladi (strict JSON schema).
_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string", "enum": list(INTENTS)},
        "title": {"type": "string"},
        "date": {"type": "string"},
        "start_time": {"type": "string"},
        "end_time": {"type": "string"},
        "repeat": {
            "type": "string",
            "enum": ["", "once", "daily", "weekdays", "weekends"],
        },
        "notes": {"type": "string"},
        "reply": {"type": "string"},
    },
    "required": [
        "intent",
        "title",
        "date",
        "start_time",
        "end_time",
        "repeat",
        "notes",
        "reply",
    ],
    "additionalProperties": False,
}

_SYSTEM = """You are the language-understanding layer of an Uzbek-language Telegram
planner bot. The user writes or speaks in Uzbek (sometimes mixed with Russian or
English). Turn their message into one structured record.

Choose exactly one intent:
- "add_event"  — a one-off appointment/meeting/event that belongs on the calendar
                 ("ertaga soat 3 da stomatolog", "shanba kuni to'y bor",
                 "buni 5-sentabrga yozib qo'y").
- "add_task"   — a recurring daily routine with a time window
                 ("har kuni 7 dan 8 gacha yugurish", "kunda ertalab ingliz tili").
- "free_time"  — asking when they are free ("ertaga nechida bo'sh vaqtim bor?",
                 "bugun qachon bo'shman?").
- "stats"      — asking about their progress ("qanchasini bajardim?",
                 "shu haftadagi statistikam").
- "list_tasks" — asking what is planned ("bugun nima rejalarim bor?").
- "unknown"    — anything else.

Field rules:
- "date": ISO "YYYY-MM-DD". Resolve relative words against the CURRENT DATE given
  below ("bugun" = today, "ertaga" = tomorrow, "indinga" = day after tomorrow,
  weekday names = the next such weekday). Empty string if no date applies.
- "start_time" / "end_time": 24-hour "HH:MM". Uzbek speakers often mean the
  afternoon: "soat 3 da" for an appointment means 15:00, "kechqurun 8" means
  20:00, "ertalab 7" means 07:00. If only a start time is given for an event,
  set "end_time" to one hour later. Empty string if no time applies.
- "repeat": "once" for add_event; for add_task use "daily", "weekdays",
  "weekends" or "once" as the message implies. Empty string otherwise.
- "title": short, clean, capitalized Uzbek title of the thing itself — no dates,
  no times, no "yozib qo'y" style instructions.
- "notes": any extra detail worth keeping (address, person, phone). May be empty.
- "reply": ONE short friendly sentence in Uzbek confirming what you understood.

Answer with the JSON record only."""


def _fallback(text: str, today: date) -> dict:
    """Claude ulanmaganda ishlaydigan juda oddiy tahlil."""
    lowered = (text or "").lower()

    if any(w in lowered for w in ("bo'sh vaqt", "bosh vaqt", "bo'shman", "qachon bo'sh")):
        intent = "free_time"
    elif any(w in lowered for w in ("statistik", "qancha", "nechta bajar", "hisobot")):
        intent = "stats"
    elif any(w in lowered for w in ("rejalarim", "nima reja", "bugungi reja")):
        intent = "list_tasks"
    else:
        intent = "add_event"

    day = today
    if "ertaga" in lowered:
        day = today + timedelta(days=1)
    elif "indinga" in lowered:
        day = today + timedelta(days=2)

    start = ""
    end = ""
    match = re.search(r"(\d{1,2})[:.](\d{2})", lowered)
    if match:
        parsed = parse_hhmm(f"{match.group(1)}:{match.group(2)}")
        if parsed:
            start = parsed.strftime("%H:%M")
            end = (datetime.combine(day, parsed) + timedelta(hours=1)).strftime("%H:%M")

    return {
        "intent": intent,
        "title": (text or "").strip()[:80],
        "date": day.isoformat() if intent in ("add_event", "free_time") else "",
        "start_time": start,
        "end_time": end,
        "repeat": "once" if intent == "add_event" else "",
        "notes": "",
        "reply": "",
    }


def _normalize(data: dict, today: date) -> dict:
    """Model qaytargan qiymatlarni xavfsiz ko'rinishga keltirish."""
    result = {key: str(data.get(key, "") or "").strip() for key in _SCHEMA["properties"]}
    if result["intent"] not in INTENTS:
        result["intent"] = "unknown"

    for key in ("start_time", "end_time"):
        parsed = parse_hhmm(result[key])
        result[key] = parsed.strftime("%H:%M") if parsed else ""

    try:
        datetime.strptime(result["date"], "%Y-%m-%d")
    except ValueError:
        result["date"] = ""

    # Boshlanish bor, tugash yo'q -> bir soat qo'shamiz.
    if result["start_time"] and not result["end_time"]:
        start = datetime.strptime(result["start_time"], "%H:%M")
        result["end_time"] = (start + timedelta(hours=1)).strftime("%H:%M")

    if result["intent"] == "free_time" and not result["date"]:
        result["date"] = today.isoformat()

    return result


async def understand(text: str, today: date, weekday_hint: str = "") -> dict:
    """Xabarni tuzilgan yozuvga aylantiradi. Hech qachon istisno tashlamaydi."""
    if not claude_enabled():
        return _fallback(text, today)

    try:
        import anthropic
    except ImportError:
        logger.warning("anthropic kutubxonasi o'rnatilmagan — zaxira rejim ishlatilmoqda")
        return _fallback(text, today)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    context = (
        f"CURRENT DATE: {today.isoformat()} ({weekday_hint or WEEKDAY_KEYS[today.weekday()]})\n"
        f"USER MESSAGE: {text}"
    )

    try:
        response = await client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2000,
            system=_SYSTEM,
            messages=[{"role": "user", "content": context}],
            output_config={
                "effort": "low",
                "format": {"type": "json_schema", "schema": _SCHEMA},
            },
        )
    except Exception:
        logger.exception("Claude so'rovi muvaffaqiyatsiz — zaxira rejim ishlatilmoqda")
        return _fallback(text, today)

    raw = next((block.text for block in response.content if block.type == "text"), "")
    try:
        return _normalize(json.loads(raw), today)
    except (json.JSONDecodeError, TypeError):
        logger.warning("Claude javobini JSON sifatida o'qib bo'lmadi: %r", raw[:200])
        return _fallback(text, today)
