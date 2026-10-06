"""
Eslatmalar va "bajardingizmi?" savollarini yuboradigan fon jarayoni.

Har TICK_SECONDS soniyada bir marta barcha foydalanuvchilarni aylanib chiqadi:

  * reja boshlanish vaqti keldi   -> "⏰ vaqt keldi" eslatmasi
  * reja muddati tugadi           -> "Bu rejangizni qildingizmi?" + ✅ Ha / ❌ Yo'q
  * savolga javob bo'lmadi        -> AUTO_MISS_HOURS dan keyin "bajarilmadi"

Har bir reja-kun juftligi uchun task_logs jadvalida bitta yozuv bo'ladi, shuning
uchun bot qayta ishga tushsa ham eslatma ikki marta yuborilmaydi.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

from planner_bot import db
from planner_bot.config import AUTO_MISS_HOURS, TICK_SECONDS
from planner_bot.keyboards import ask_done_kb
from planner_bot.timeutil import now_in, parse_hhmm, repeat_label, runs_on, task_window

logger = logging.getLogger(__name__)


async def _safe_send(bot: Bot, chat_id: int, text: str, **kwargs) -> bool:
    """Bitta foydalanuvchi bloklab qo'ysa, butun sikl to'xtab qolmasin."""
    try:
        await bot.send_message(chat_id, text, **kwargs)
        return True
    except TelegramRetryAfter as exc:
        await asyncio.sleep(exc.retry_after)
        try:
            await bot.send_message(chat_id, text, **kwargs)
            return True
        except Exception:
            logger.exception("Xabar yuborib bo'lmadi (%s)", chat_id)
            return False
    except TelegramForbiddenError:
        logger.info("Foydalanuvchi %s botni bloklagan", chat_id)
        return False
    except Exception:
        logger.exception("Xabar yuborib bo'lmadi (%s)", chat_id)
        return False


def _created_at(task) -> datetime | None:
    try:
        value = datetime.fromisoformat(task["created_at"])
    except (TypeError, ValueError):
        return None
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


async def _process_user(bot: Bot, user) -> None:
    tz_name = user["tz"]
    now = now_in(tz_name)
    # Kechagi kunni ham tekshiramiz — tungi rejalar (23:00–01:00) uchun kerak.
    for day in (now.date(), now.date() - timedelta(days=1)):
        for task in db.get_tasks(user["user_id"]):
            if not runs_on(task["repeat"], task["on_date"], day):
                continue

            start = parse_hhmm(task["start_time"])
            end = parse_hhmm(task["end_time"])
            if not start or not end:
                continue

            start_dt, end_dt = task_window(day, start, end, tz_name)
            if now < start_dt:
                continue

            # Reja yaratilishidan oldingi kunlar uchun savol bermaymiz.
            created_at = _created_at(task)
            if created_at and start_dt < created_at:
                continue

            log_date = day.isoformat()
            log = db.get_log(task["id"], log_date)

            # Bot uzoq o'chib turgan bo'lsa, eskirgan kunlarni ochmaymiz.
            if log is None and now - end_dt > timedelta(hours=AUTO_MISS_HOURS):
                continue
            if log is None:
                log = db.get_or_create_log(task["id"], user["user_id"], log_date)

            # 1. Boshlanish eslatmasi
            if user["remind_on_start"] and not log["started_notified"] and now < end_dt:
                sent = await _safe_send(
                    bot,
                    user["user_id"],
                    f"⏰ <b>Vaqt keldi!</b>\n\n"
                    f"📌 {task['title']}\n"
                    f"🕐 {task['start_time']} – {task['end_time']} "
                    f"({repeat_label(task['repeat'], task['on_date'])})\n\n"
                    f"Muddat tugagach natijani so'rayman.",
                )
                if sent:
                    db.mark_started_notified(task["id"], log_date)

            # 2. Muddat tugadi -> savol
            if now >= end_dt and log["status"] == db.STATUS_PENDING and not log["asked_at"]:
                sent = await _safe_send(
                    bot,
                    user["user_id"],
                    f"❓ <b>Muddat tugadi.</b>\n\n"
                    f"📌 {task['title']}\n"
                    f"🕐 {task['start_time']} – {task['end_time']}\n\n"
                    f"Bu rejangizni bajardingizmi?",
                    reply_markup=ask_done_kb(task["id"], log_date),
                )
                if sent:
                    db.mark_asked(task["id"], log_date)


async def _auto_miss() -> None:
    """Uzoq vaqt javobsiz qolgan savollarni 'bajarilmadi' deb belgilaydi."""
    deadline = datetime.now(timezone.utc) - timedelta(hours=AUTO_MISS_HOURS)
    for log in db.unanswered_logs():
        try:
            asked_at = datetime.fromisoformat(log["asked_at"])
        except (TypeError, ValueError):
            continue
        if asked_at <= deadline:
            db.set_log_status(
                log["task_id"], log["log_date"], db.STATUS_MISSED, answered=False
            )


async def tick(bot: Bot) -> None:
    """Bitta tekshiruv sikli."""
    for user in db.all_users():
        try:
            await _process_user(bot, user)
        except Exception:
            logger.exception("Foydalanuvchi %s uchun sikl xatosi", user["user_id"])
    try:
        await _auto_miss()
    except Exception:
        logger.exception("Avtomatik 'bajarilmadi' belgilashda xatolik")


async def run_forever(bot: Bot) -> None:
    """Bot bilan birga ishlaydigan cheksiz sikl."""
    logger.info("Eslatma sikli ishga tushdi (har %s soniyada)", TICK_SECONDS)
    while True:
        try:
            await tick(bot)
        except Exception:
            logger.exception("Eslatma siklida kutilmagan xatolik")
        await asyncio.sleep(TICK_SECONDS)
