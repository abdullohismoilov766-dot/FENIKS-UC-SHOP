"""
FENIKS PLANNER — kundalik rejalar, eslatmalar, statistika va Notion kalendar boti.

Nima qiladi:
  1. Kundalik rejalar ro'yxati — har biri "nechidan nechigacha" vaqt oynasi bilan.
  2. Reja boshlanganda eslatma yuboradi.
  3. Muddat tugagach "Bu rejangizni bajardingizmi?" deb so'raydi — ✅ Ha / ❌ Yo'q.
  4. Javoblarni yig'ib, statistika chiqaradi (bugun / 7 kun / 30 kun / butun davr).
  5. Matn yoki ovozli xabarni tushunib, Notion kalendariga yozib qo'yadi.
  6. "Ertaga nechida bo'sh vaqtim bor?" savoliga bo'sh oraliqlar bilan javob beradi.

Ishga tushirish: `python -m planner_bot.bot` (README.md ga qarang).
"""

from __future__ import annotations

import asyncio
import logging
from datetime import date, timedelta
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramNetworkError,
    TelegramUnauthorizedError,
)
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, CallbackQuery, Message

from planner_bot import db, notion, stats
from planner_bot.config import (
    BOT_TOKEN,
    DEFAULT_TZ,
    PORT,
    claude_enabled,
    notion_enabled,
    stt_enabled,
)
from planner_bot.freetime import build_day_plan, render_day_plan
from planner_bot.keyboards import (
    BTN_ADD,
    BTN_CALENDAR,
    BTN_FREE,
    BTN_SETTINGS,
    BTN_STATS,
    BTN_TODAY,
    calendar_kb,
    confirm_event_kb,
    free_time_kb,
    main_menu,
    repeat_kb,
    settings_kb,
    stats_period_kb,
    task_manage_kb,
)
from planner_bot.nlp import understand
from planner_bot.states import AddTask, Settings
from planner_bot.stt import transcribe
from planner_bot.timeutil import (
    fmt_date,
    now_in,
    parse_date,
    parse_hhmm,
    parse_range,
    repeat_label,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

dp = Dispatcher()

MENU_BUTTONS = {BTN_ADD, BTN_TODAY, BTN_STATS, BTN_FREE, BTN_CALENDAR, BTN_SETTINGS}

HELP_TEXT = (
    "🤖 <b>Men nima qila olaman</b>\n\n"
    "<b>1. Kundalik rejalar</b>\n"
    f"«{BTN_ADD}» — reja nomi va vaqt oralig'ini kiritasiz "
    "(masalan <code>07:00-08:00</code>).\n"
    "Reja boshlanganda eslatma yuboraman, muddat tugagach "
    "«Bajardingizmi?» deb so'rayman.\n\n"
    "<b>2. Statistika</b>\n"
    f"«{BTN_STATS}» — nechta reja bajarildi, nechtasi yo'q, necha foiz.\n\n"
    "<b>3. Kalendar (Notion)</b>\n"
    "Menga oddiy qilib yozing yoki ayting:\n"
    "<i>«Ertaga soat 3 da stomatologga boraman, kalendarga yozib qo'y»</i>\n"
    "— men uni Notion kalendaringizga qo'shaman.\n\n"
    "<b>4. Bo'sh vaqt</b>\n"
    "<i>«Ertaga nechida bo'sh vaqtim bor?»</i> — kundalik rejalaringiz va Notion "
    "kalendaringizni solishtirib, bo'sh oraliqlarni chiqaraman.\n\n"
    "<b>Buyruqlar:</b>\n"
    "/add — yangi reja\n"
    "/today — bugungi rejalar\n"
    "/tasks — barcha rejalarim\n"
    "/stats — statistika\n"
    "/free — bo'sh vaqtlarim\n"
    "/calendar — kalendar yozuvlari\n"
    "/settings — sozlamalar\n"
    "/cancel — joriy amalni bekor qilish"
)


def _user(message_or_callback):
    """Foydalanuvchini bazadan oladi (bo'lmasa yaratadi)."""
    src = message_or_callback.from_user
    return db.ensure_user(src.id, src.full_name, src.username)


def _today(user) -> date:
    return now_in(user["tz"]).date()


# ------------------------------------------------------------- /start ------
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    user = _user(message)
    await message.answer(
        f"👋 Assalomu alaykum, <b>{message.from_user.full_name}</b>!\n\n"
        "Men sizning kundalik reja va vaqt yordamchingizman.\n"
        f"Vaqt mintaqangiz: <b>{user['tz']}</b>, faol kun oralig'i: "
        f"<b>{user['day_start']}–{user['day_end']}</b> "
        "(<code>/settings</code> orqali o'zgartirasiz).\n\n"
        "Boshlash uchun quyidagi menyudan foydalaning 👇",
        reply_markup=main_menu(),
    )
    await message.answer(HELP_TEXT)


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    _user(message)
    await message.answer(HELP_TEXT, reply_markup=main_menu())


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🚫 Bekor qilindi.", reply_markup=main_menu())


# -------------------------------------------------- Yangi reja qo'shish ----
@dp.message(Command("add"))
@dp.message(F.text == BTN_ADD)
async def add_start(message: Message, state: FSMContext) -> None:
    _user(message)
    await state.set_state(AddTask.waiting_title)
    await message.answer(
        "📝 Reja nomini yozing.\n\n"
        "Masalan: <i>Ertalabki yugurish</i>, <i>Ingliz tili</i>, <i>Kitob o'qish</i>\n\n"
        "Bekor qilish: /cancel"
    )


@dp.message(AddTask.waiting_title)
async def add_title(message: Message, state: FSMContext) -> None:
    title = (message.text or "").strip()
    if title.startswith("/") or title in MENU_BUTTONS:
        await message.answer(
            "⏳ Hozir yangi reja qo'shyapmiz. Avval reja nomini yozing "
            "yoki /cancel bilan bekor qiling."
        )
        return
    if not title or len(title) > 120:
        await message.answer("⚠️ Reja nomi 1–120 belgidan iborat bo'lsin.")
        return
    await state.update_data(title=title)
    await state.set_state(AddTask.waiting_range)
    await message.answer(
        f"🕐 <b>{title}</b> — nechidan nechigacha?\n\n"
        "Vaqt oralig'ini shu ko'rinishda yozing: <code>07:00-08:00</code>"
    )


@dp.message(AddTask.waiting_range)
async def add_range(message: Message, state: FSMContext) -> None:
    parsed = parse_range(message.text or "")
    if not parsed:
        await message.answer(
            "⚠️ Vaqt oralig'ini tushunmadim.\n"
            "Namuna: <code>07:00-08:00</code> yoki <code>21:30-22:15</code>"
        )
        return
    start, end = parsed
    if start == end:
        await message.answer("⚠️ Boshlanish va tugash vaqti bir xil bo'lmasin.")
        return
    await state.update_data(start_time=start.strftime("%H:%M"), end_time=end.strftime("%H:%M"))
    await state.set_state(AddTask.waiting_repeat)
    await message.answer("🔁 Bu reja qanchalik tez-tez takrorlanadi?", reply_markup=repeat_kb())


@dp.callback_query(AddTask.waiting_repeat, F.data.startswith("rep:"))
async def add_repeat(callback: CallbackQuery, state: FSMContext) -> None:
    repeat = callback.data.split(":", 1)[1]
    data = await state.get_data()
    await state.clear()

    user = _user(callback)
    on_date = _today(user).isoformat() if repeat == "once" else None
    db.create_task(
        user_id=user["user_id"],
        title=data["title"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        repeat=repeat,
        on_date=on_date,
    )

    await callback.message.edit_text(
        f"✅ Reja qo'shildi!\n\n"
        f"📌 <b>{data['title']}</b>\n"
        f"🕐 {data['start_time']} – {data['end_time']}\n"
        f"🔁 {repeat_label(repeat, on_date)}\n\n"
        f"Boshlanish vaqtida eslataman, muddat tugagach natijani so'rayman."
    )
    await callback.answer("Saqlandi ✅")


# ------------------------------------------------------ Rejalar ro'yxati ---
@dp.message(Command("today"))
@dp.message(F.text == BTN_TODAY)
async def show_today(message: Message) -> None:
    user = _user(message)
    await message.answer(stats.render_today(user["user_id"], _today(user)))


@dp.message(Command("tasks"))
async def show_tasks(message: Message) -> None:
    user = _user(message)
    tasks = db.get_tasks(user["user_id"], only_active=False)
    if not tasks:
        await message.answer(
            "Sizda hali reja yo'q.\n"
            f"«{BTN_ADD}» tugmasi orqali birinchi rejangizni qo'shing."
        )
        return

    await message.answer(f"📚 <b>Barcha rejalaringiz ({len(tasks)} ta):</b>")
    for task in tasks:
        state_mark = "" if task["active"] else "  ⏸ <i>to'xtatilgan</i>"
        await message.answer(
            f"📌 <b>{task['title']}</b>{state_mark}\n"
            f"🕐 {task['start_time']} – {task['end_time']}\n"
            f"🔁 {repeat_label(task['repeat'], task['on_date'])}",
            reply_markup=task_manage_kb(task["id"], bool(task["active"])),
        )


@dp.callback_query(F.data.startswith("task:"))
async def manage_task(callback: CallbackQuery) -> None:
    _, action, raw_id = callback.data.split(":", 2)
    task_id = int(raw_id)
    task = db.get_task(task_id)
    user = _user(callback)

    if not task or task["user_id"] != user["user_id"]:
        await callback.answer("Bu reja topilmadi.", show_alert=True)
        return

    if action == "del":
        db.delete_task(task_id)
        await callback.message.edit_text(f"🗑 <b>{task['title']}</b> o'chirildi.")
        await callback.answer("O'chirildi")
        return

    active = action == "resume"
    db.set_task_active(task_id, active)
    state_mark = "" if active else "  ⏸ <i>to'xtatilgan</i>"
    await callback.message.edit_text(
        f"📌 <b>{task['title']}</b>{state_mark}\n"
        f"🕐 {task['start_time']} – {task['end_time']}\n"
        f"🔁 {repeat_label(task['repeat'], task['on_date'])}",
        reply_markup=task_manage_kb(task_id, active),
    )
    await callback.answer("Yoqildi" if active else "To'xtatildi")


# ------------------------------------- Muddat savoliga javob (Ha / Yo'q) ---
@dp.callback_query(F.data.startswith("ans:"))
async def answer_prompt(callback: CallbackQuery) -> None:
    _, answer, raw_id, log_date = callback.data.split(":", 3)
    task_id = int(raw_id)
    task = db.get_task(task_id)
    user = _user(callback)

    if not task or task["user_id"] != user["user_id"]:
        await callback.answer("Bu reja topilmadi.", show_alert=True)
        return

    status = db.STATUS_DONE if answer == "done" else db.STATUS_MISSED
    db.get_or_create_log(task_id, user["user_id"], log_date)
    db.set_log_status(task_id, log_date, status)

    verdict = (
        "✅ <b>Zo'r! Bajarilgan deb belgiladim.</b>"
        if status == db.STATUS_DONE
        else "❌ <b>Bajarilmagan deb belgiladim.</b> Ertaga albatta uddalaysiz 💪"
    )
    await callback.message.edit_text(
        f"📌 {task['title']}\n"
        f"🕐 {task['start_time']} – {task['end_time']}\n\n"
        f"{verdict}"
    )
    await callback.answer("Yozib oldim")


# --------------------------------------------------------- Statistika -----
@dp.message(Command("stats"))
@dp.message(F.text == BTN_STATS)
async def show_stats(message: Message) -> None:
    user = _user(message)
    await message.answer(
        stats.render_stats(user["user_id"], "week", _today(user)),
        reply_markup=stats_period_kb(),
    )


@dp.callback_query(F.data.startswith("stats:"))
async def stats_period(callback: CallbackQuery) -> None:
    period = callback.data.split(":", 1)[1]
    user = _user(callback)
    text = stats.render_stats(user["user_id"], period, _today(user))
    try:
        await callback.message.edit_text(text, reply_markup=stats_period_kb())
    except TelegramBadRequest:
        pass  # matn o'zgarmagan bo'lsa Telegram xato qaytaradi — muhim emas
    await callback.answer()


# --------------------------------------------------------- Bo'sh vaqt -----
@dp.message(Command("free"))
@dp.message(F.text == BTN_FREE)
async def show_free(message: Message) -> None:
    _user(message)
    await message.answer("Qaysi kun uchun bo'sh vaqtlaringizni ko'rsatay?", reply_markup=free_time_kb())


@dp.callback_query(F.data.startswith("free:"))
async def free_for_day(callback: CallbackQuery) -> None:
    offset = int(callback.data.split(":", 1)[1])
    user = _user(callback)
    await callback.answer("Hisoblayapman…")
    plan = await build_day_plan(user, _today(user) + timedelta(days=offset))
    await callback.message.answer(render_day_plan(plan))


# ---------------------------------------------------- Kalendar (Notion) ---
@dp.message(Command("calendar"))
@dp.message(F.text == BTN_CALENDAR)
async def show_calendar_menu(message: Message) -> None:
    _user(message)
    if not notion_enabled():
        await message.answer(
            "🗓 Notion hali ulanmagan.\n\n"
            "<code>.env</code> faylida <code>NOTION_TOKEN</code> va "
            "<code>NOTION_DATABASE_ID</code> ni to'ldiring — shundan keyin "
            "«ertaga soat 3 da uchrashuv» deb yozsangiz, kalendarga yozib qo'yaman."
        )
        return
    await message.answer("Qaysi davr uchun kalendar yozuvlarini ko'rsatay?", reply_markup=calendar_kb())


@dp.callback_query(F.data.startswith("cal:"))
async def show_calendar(callback: CallbackQuery) -> None:
    span = int(callback.data.split(":", 1)[1])
    user = _user(callback)
    today = _today(user)
    day_from = today if span != 1 else today + timedelta(days=1)
    day_to = today + timedelta(days=span) if span > 1 else day_from

    await callback.answer("Notion'dan olyapman…")
    try:
        events = await notion.list_events(day_from, day_to, user["tz"])
    except notion.NotionError as exc:
        await callback.message.answer(f"⚠️ {exc}")
        return

    if not events:
        await callback.message.answer(
            f"🗓 {fmt_date(day_from)}"
            + (f" — {fmt_date(day_to)}" if day_to != day_from else "")
            + "\n\nBu davrda kalendaringizda yozuv yo'q."
        )
        return

    lines = [f"🗓 <b>Kalendar — {fmt_date(day_from)}</b>"]
    if day_to != day_from:
        lines[0] = f"🗓 <b>Kalendar: {fmt_date(day_from)} — {fmt_date(day_to)}</b>"
    lines.append("")
    current_day = None
    for event in events:
        event_day = event.start.date() if event.start else day_from
        if day_to != day_from and event_day != current_day:
            current_day = event_day
            lines.append(f"\n<b>{fmt_date(event_day)}</b>")
        lines.append(event.label())
    await callback.message.answer("\n".join(lines))


# --------------------------------------------------------- Sozlamalar -----
@dp.message(Command("settings"))
@dp.message(F.text == BTN_SETTINGS)
async def show_settings(message: Message) -> None:
    user = _user(message)
    on_off = "yoqilgan" if user["remind_on_start"] else "o'chirilgan"
    claude_state = "ulangan" if claude_enabled() else "ulanmagan"
    notion_state = "ulangan" if notion_enabled() else "ulanmagan"
    voice_state = "yoqilgan" if stt_enabled() else "o'chirilgan"
    await message.answer(
        "⚙️ <b>Sozlamalar</b>\n\n"
        f"🌍 Vaqt mintaqasi: <b>{user['tz']}</b>\n"
        f"🕘 Faol kun oralig'i: <b>{user['day_start']}–{user['day_end']}</b>\n"
        f"🔔 Boshlanish eslatmasi: <b>{on_off}</b>\n\n"
        f"🤖 Claude (matn/ovoz tushunish): <b>{claude_state}</b>\n"
        f"🗓 Notion kalendar: <b>{notion_state}</b>\n"
        f"🎙 Ovozli xabar: <b>{voice_state}</b>",
        reply_markup=settings_kb(),
    )


@dp.callback_query(F.data.startswith("set:"))
async def settings_action(callback: CallbackQuery, state: FSMContext) -> None:
    action = callback.data.split(":", 1)[1]
    user = _user(callback)

    if action == "tz":
        await state.set_state(Settings.waiting_timezone)
        await callback.message.answer(
            "🌍 Vaqt mintaqangizni yozing (IANA formatida).\n"
            f"Masalan: <code>{DEFAULT_TZ}</code>, <code>Europe/Moscow</code>, "
            "<code>Asia/Almaty</code>"
        )
    elif action == "window":
        await state.set_state(Settings.waiting_day_window)
        await callback.message.answer(
            "🕘 Faol kun oralig'ingizni yozing — bo'sh vaqt shu oraliq ichida hisoblanadi.\n"
            "Namuna: <code>08:00-23:00</code>"
        )
    elif action == "remind":
        new_value = 0 if user["remind_on_start"] else 1
        db.update_user(user["user_id"], remind_on_start=new_value)
        await callback.message.answer(
            "🔔 Boshlanish eslatmasi yoqildi."
            if new_value
            else "🔕 Boshlanish eslatmasi o'chirildi. Muddat tugagandagi savol baribir keladi."
        )
    await callback.answer()


@dp.message(Settings.waiting_timezone)
async def set_timezone(message: Message, state: FSMContext) -> None:
    name = (message.text or "").strip()
    try:
        ZoneInfo(name)
    except Exception:
        await message.answer("⚠️ Bunday vaqt mintaqasi topilmadi. Masalan: <code>Asia/Tashkent</code>")
        return
    user = _user(message)
    db.update_user(user["user_id"], tz=name)
    await state.clear()
    await message.answer(f"✅ Vaqt mintaqasi <b>{name}</b> qilib o'rnatildi.", reply_markup=main_menu())


@dp.message(Settings.waiting_day_window)
async def set_day_window(message: Message, state: FSMContext) -> None:
    parsed = parse_range(message.text or "")
    if not parsed:
        await message.answer("⚠️ Namuna: <code>08:00-23:00</code>")
        return
    start, end = parsed
    if end <= start:
        await message.answer("⚠️ Tugash vaqti boshlanishdan katta bo'lsin.")
        return
    user = _user(message)
    db.update_user(
        user["user_id"],
        day_start=start.strftime("%H:%M"),
        day_end=end.strftime("%H:%M"),
    )
    await state.clear()
    await message.answer(
        f"✅ Faol kun oralig'i <b>{start.strftime('%H:%M')}–{end.strftime('%H:%M')}</b> "
        "qilib o'rnatildi.",
        reply_markup=main_menu(),
    )


# ------------------------------------------------- Ovozli xabar -> matn ----
@dp.message(F.voice | F.audio)
async def handle_voice(message: Message, state: FSMContext, bot: Bot) -> None:
    _user(message)
    if not stt_enabled():
        await message.answer(
            "🎙 Ovozli xabarlarni tushunish hozircha yoqilmagan.\n"
            "Iltimos, xohishingizni matn ko'rinishida yozing — masalan:\n"
            "<i>«Ertaga soat 3 da stomatolog»</i>"
        )
        return

    notice = await message.answer("🎙 Ovozni tinglayapman…")
    voice = message.voice or message.audio
    buffer = await bot.download(voice.file_id)
    text = await transcribe(buffer.read(), filename="voice.oga")

    if not text:
        await notice.edit_text(
            "⚠️ Ovozni matnga o'gira olmadim. Iltimos, matn ko'rinishida yozing."
        )
        return

    await notice.edit_text(f"🎙 <i>«{text}»</i>")
    await route_free_text(message, state, text)


# --------------------------------------------- Erkin matn -> Claude -------
@dp.message(F.text)
async def handle_text(message: Message, state: FSMContext) -> None:
    await route_free_text(message, state, message.text or "")


async def route_free_text(message: Message, state: FSMContext, text: str) -> None:
    """Erkin xabarni tushunib, tegishli amalga yo'naltiradi."""
    user = _user(message)
    today = _today(user)

    thinking = await message.answer("🤔 Tushunishga harakat qilyapman…")
    parsed = await understand(text, today)
    intent = parsed["intent"]

    if intent == "free_time":
        day = parse_date(parsed["date"]) or today
        await thinking.edit_text("🕒 Bo'sh vaqtlaringizni hisoblayapman…")
        plan = await build_day_plan(user, day)
        await thinking.delete()
        await message.answer(render_day_plan(plan))
        return

    if intent == "stats":
        await thinking.delete()
        await message.answer(
            stats.render_stats(user["user_id"], "week", today),
            reply_markup=stats_period_kb(),
        )
        return

    if intent == "list_tasks":
        await thinking.delete()
        await message.answer(stats.render_today(user["user_id"], today))
        return

    if intent == "add_task":
        start = parse_hhmm(parsed["start_time"])
        end = parse_hhmm(parsed["end_time"])
        if not (parsed["title"] and start and end):
            await thinking.edit_text(
                "🤔 Rejani tushundim, lekin vaqt oralig'i aniq emas.\n"
                f"«{BTN_ADD}» tugmasi orqali qo'shsangiz aniqroq bo'ladi."
            )
            return
        repeat = parsed["repeat"] or "daily"
        await state.update_data(
            pending={
                "kind": "task",
                "title": parsed["title"],
                "start_time": start.strftime("%H:%M"),
                "end_time": end.strftime("%H:%M"),
                "repeat": repeat,
                "date": parsed["date"],
            }
        )
        await thinking.edit_text(
            "🔁 <b>Kundalik reja sifatida qo'shaymi?</b>\n\n"
            f"📌 {parsed['title']}\n"
            f"🕐 {start.strftime('%H:%M')} – {end.strftime('%H:%M')}\n"
            f"🔁 {repeat_label(repeat, parsed['date'] or None)}",
            reply_markup=confirm_event_kb(),
        )
        return

    if intent == "add_event":
        day = parse_date(parsed["date"])
        if not parsed["title"] or not day:
            await thinking.edit_text(
                "🤔 Tushunmadim. Sanani ham qo'shib yozing — masalan:\n"
                "<i>«Ertaga soat 15:00 da stomatolog»</i>"
            )
            return
        if not notion_enabled():
            await thinking.edit_text(
                "🗓 Notion ulanmagani uchun kalendarga yoza olmayman.\n"
                "<code>.env</code> da <code>NOTION_TOKEN</code> va "
                "<code>NOTION_DATABASE_ID</code> ni to'ldiring."
            )
            return

        await state.update_data(
            pending={
                "kind": "event",
                "title": parsed["title"],
                "date": day.isoformat(),
                "start_time": parsed["start_time"],
                "end_time": parsed["end_time"],
                "notes": parsed["notes"],
            }
        )
        when = (
            f"{parsed['start_time']} – {parsed['end_time']}"
            if parsed["start_time"]
            else "kun bo'yi"
        )
        note_line = f"\n📝 {parsed['notes']}" if parsed["notes"] else ""
        await thinking.edit_text(
            "🗓 <b>Notion kalendariga yozaymi?</b>\n\n"
            f"📌 {parsed['title']}\n"
            f"📅 {fmt_date(day)}\n"
            f"🕐 {when}{note_line}",
            reply_markup=confirm_event_kb(),
        )
        return

    await thinking.edit_text(
        "🤔 Buni tushunmadim.\n\n" + HELP_TEXT,
    )


@dp.callback_query(F.data.startswith("pend:"))
async def confirm_pending(callback: CallbackQuery, state: FSMContext) -> None:
    decision = callback.data.split(":", 1)[1]
    data = await state.get_data()
    pending = data.get("pending")
    await state.update_data(pending=None)

    if decision == "no" or not pending:
        await callback.message.edit_text("🚫 Bekor qilindi.")
        await callback.answer()
        return

    user = _user(callback)

    if pending["kind"] == "task":
        on_date = pending.get("date") or None
        db.create_task(
            user_id=user["user_id"],
            title=pending["title"],
            start_time=pending["start_time"],
            end_time=pending["end_time"],
            repeat=pending["repeat"],
            on_date=on_date if pending["repeat"] == "once" else None,
        )
        await callback.message.edit_text(
            f"✅ Reja qo'shildi!\n\n"
            f"📌 <b>{pending['title']}</b>\n"
            f"🕐 {pending['start_time']} – {pending['end_time']}\n"
            f"🔁 {repeat_label(pending['repeat'], on_date)}"
        )
        await callback.answer("Saqlandi ✅")
        return

    day = parse_date(pending["date"])
    try:
        url = await notion.create_event(
            title=pending["title"],
            day=day,
            start_time=pending["start_time"] or None,
            end_time=pending["end_time"] or None,
            tz_name=user["tz"],
            notes=pending.get("notes", ""),
        )
    except notion.NotionError as exc:
        await callback.message.edit_text(f"⚠️ {exc}")
        await callback.answer()
        return
    except Exception:
        logger.exception("Notion yozuvini yaratishda xatolik")
        await callback.message.edit_text("⚠️ Notion'ga yozib bo'lmadi. Keyinroq urinib ko'ring.")
        await callback.answer()
        return

    link = f'\n\n<a href="{url}">Notion\'da ochish</a>' if url else ""
    await callback.message.edit_text(
        f"✅ Kalendarga yozib qo'ydim!\n\n"
        f"📌 <b>{pending['title']}</b>\n"
        f"📅 {fmt_date(day)}"
        + (f"\n🕐 {pending['start_time']} – {pending['end_time']}" if pending["start_time"] else "")
        + link,
        disable_web_page_preview=True,
    )
    await callback.answer("Yozildi ✅")


# ------------------------------------------------------------- ishga tushirish ---
async def _set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Botni ishga tushirish"),
            BotCommand(command="add", description="Yangi reja qo'shish"),
            BotCommand(command="today", description="Bugungi rejalar"),
            BotCommand(command="tasks", description="Barcha rejalarim"),
            BotCommand(command="stats", description="Statistika"),
            BotCommand(command="free", description="Bo'sh vaqtlarim"),
            BotCommand(command="calendar", description="Kalendar yozuvlari"),
            BotCommand(command="settings", description="Sozlamalar"),
            BotCommand(command="help", description="Yordam"),
        ]
    )


def _startup_report() -> str:
    """Ishga tushganda qaysi imkoniyatlar yoqilganini ko'rsatadi (kalitlarsiz)."""
    rows = [
        ("Kundalik rejalar, eslatmalar, statistika", True),
        ("Erkin matnni tushunish (Claude)", claude_enabled()),
        ("Notion kalendar", notion_enabled()),
        ("Ovozli xabarlar", stt_enabled()),
    ]
    lines = ["", "  FENIKS PLANNER ishga tushdi", "  " + "-" * 40]
    for label, enabled in rows:
        lines.append(f"  {'[+]' if enabled else '[ ]'} {label}")
    lines.append("  " + "-" * 40)
    return "\n".join(lines)


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "PLANNER_BOT_TOKEN topilmadi.\n"
            "Sozlash uchun ishga tushiring:  python -m planner_bot.setup"
        )

    db.init_db()
    logger.info(_startup_report())

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Tokenni darhol tekshiramiz — xato bo'lsa uzun traceback o'rniga
    # tushunarli xabar chiqsin.
    try:
        me = await bot.get_me()
    except TelegramUnauthorizedError:
        logger.error(
            "Telegram tokenni qabul qilmadi (401 Unauthorized).\n"
            "  Tekshiring:\n"
            "   1. Token to'liq nusxalanganmi (bo'sh joy yoki yetishmayotgan belgisiz)\n"
            "   2. @BotFather -> /mybots -> botingiz -> API Token orqali qayta oling\n"
            "   3. Sozlashni qayta bajaring:  python -m planner_bot.setup"
        )
        await bot.session.close()
        return
    except TelegramNetworkError as exc:
        logger.error(
            "Telegram serveriga ulanib bo'lmadi: %s\n"
            "  Internet aloqasini tekshiring va qaytadan urinib ko'ring.",
            exc,
        )
        await bot.session.close()
        return

    logger.info("Ulandi: @%s", me.username)
    await _set_commands(bot)

    from planner_bot.scheduler import run_forever

    # Tekin hosting tariflari port ochishni talab qiladi (pastdagi izohga qarang).
    health_runner = None
    if PORT:
        from planner_bot.health import start_health_server

        health_runner = await start_health_server(PORT)

    reminder_task = asyncio.create_task(run_forever(bot))
    try:
        await dp.start_polling(bot)
    finally:
        reminder_task.cancel()
        if health_runner is not None:
            await health_runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
