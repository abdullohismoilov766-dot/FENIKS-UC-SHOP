"""Barcha reply/inline klaviaturalar."""

from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

BTN_ADD = "➕ Yangi reja"
BTN_TODAY = "📋 Bugungi rejalar"
BTN_STATS = "📊 Statistika"
BTN_CALENDAR = "🗓 Kalendar"
BTN_FREE = "🕒 Bo'sh vaqtlarim"
BTN_SETTINGS = "⚙️ Sozlamalar"


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_ADD), KeyboardButton(text=BTN_TODAY)],
            [KeyboardButton(text=BTN_STATS), KeyboardButton(text=BTN_FREE)],
            [KeyboardButton(text=BTN_CALENDAR), KeyboardButton(text=BTN_SETTINGS)],
        ],
        resize_keyboard=True,
    )


def repeat_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔁 Har kuni", callback_data="rep:daily")],
            [InlineKeyboardButton(text="💼 Ish kunlari (Du–Ju)", callback_data="rep:weekdays")],
            [InlineKeyboardButton(text="🌴 Dam olish kunlari", callback_data="rep:weekends")],
            [InlineKeyboardButton(text="1️⃣ Faqat bugun", callback_data="rep:once")],
        ]
    )


def ask_done_kb(task_id: int, log_date: str) -> InlineKeyboardMarkup:
    """Muddat tugagach yuboriladigan savol uchun ikkita tugma."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Ha", callback_data=f"ans:done:{task_id}:{log_date}"),
                InlineKeyboardButton(text="❌ Yo'q", callback_data=f"ans:missed:{task_id}:{log_date}"),
            ]
        ]
    )


def stats_period_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Bugun", callback_data="stats:today"),
                InlineKeyboardButton(text="7 kun", callback_data="stats:week"),
            ],
            [
                InlineKeyboardButton(text="30 kun", callback_data="stats:month"),
                InlineKeyboardButton(text="Hammasi", callback_data="stats:all"),
            ],
        ]
    )


def free_time_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Bugun", callback_data="free:0"),
                InlineKeyboardButton(text="Ertaga", callback_data="free:1"),
                InlineKeyboardButton(text="Indinga", callback_data="free:2"),
            ]
        ]
    )


def calendar_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📅 Bugun", callback_data="cal:0"),
                InlineKeyboardButton(text="📅 Ertaga", callback_data="cal:1"),
            ],
            [InlineKeyboardButton(text="📆 Keyingi 7 kun", callback_data="cal:7")],
        ]
    )


def task_manage_kb(task_id: int, active: bool) -> InlineKeyboardMarkup:
    toggle = (
        InlineKeyboardButton(text="⏸ To'xtatish", callback_data=f"task:pause:{task_id}")
        if active
        else InlineKeyboardButton(text="▶️ Yoqish", callback_data=f"task:resume:{task_id}")
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [toggle, InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"task:del:{task_id}")]
        ]
    )


def confirm_event_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Ha, yozib qo'y", callback_data="pend:yes"),
                InlineKeyboardButton(text="❌ Bekor", callback_data="pend:no"),
            ]
        ]
    )


def settings_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌍 Vaqt mintaqasi", callback_data="set:tz")],
            [InlineKeyboardButton(text="🕘 Faol kun oralig'i", callback_data="set:window")],
            [InlineKeyboardButton(text="🔔 Boshlanish eslatmasi", callback_data="set:remind")],
        ]
    )
