"""
"Ertaga nechidan nechigacha bo'sh vaqtim bor?" savoliga javob tayyorlash.

Band vaqtlar ikki manbadan yig'iladi:
  1. Notion kalendaridagi aniq vaqtli yozuvlar (kun bo'yi bo'lganlari alohida eslatiladi)
  2. Botdagi kundalik rejalar (shu kunga tushadiganlari)

Ular foydalanuvchining faol kun oralig'idan ayriladi va qolgani bo'sh vaqt bo'ladi.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

from planner_bot import db
from planner_bot.config import MIN_FREE_SLOT_MIN, notion_enabled
from planner_bot.notion import Event, NotionError, list_events
from planner_bot.timeutil import (
    combine,
    fmt_date,
    free_slots,
    human_duration,
    parse_hhmm,
    runs_on,
    task_window,
)

logger = logging.getLogger(__name__)


@dataclass
class DayPlan:
    day: date
    busy: list[tuple[datetime, datetime, str]]
    all_day_events: list[Event]
    free: list[tuple[datetime, datetime]]
    notion_error: str = ""


async def build_day_plan(user, day: date) -> DayPlan:
    """Bir kun uchun band/bo'sh vaqt manzarasini yig'adi."""
    tz_name = user["tz"]
    busy: list[tuple[datetime, datetime, str]] = []
    all_day: list[Event] = []
    notion_error = ""

    # 1. Botdagi kundalik rejalar
    for task in db.get_tasks(user["user_id"]):
        if not runs_on(task["repeat"], task["on_date"], day):
            continue
        start = parse_hhmm(task["start_time"])
        end = parse_hhmm(task["end_time"])
        if not start or not end:
            continue
        start_dt, end_dt = task_window(day, start, end, tz_name)
        busy.append((start_dt, end_dt, task["title"]))

    # 2. Notion kalendari
    if notion_enabled():
        try:
            for event in await list_events(day, day, tz_name):
                if event.all_day or not event.start:
                    all_day.append(event)
                elif event.end and event.end > event.start:
                    busy.append((event.start, event.end, event.title))
                else:
                    # Tugash vaqti ko'rsatilmagan — 1 soat deb hisoblaymiz
                    busy.append((event.start, event.start + timedelta(hours=1), event.title))
        except NotionError as exc:
            notion_error = str(exc)
        except Exception:
            logger.exception("Notion yozuvlarini olishda kutilmagan xatolik")
            notion_error = "Notion bilan bog'lanib bo'lmadi."

    window_start = combine(day, parse_hhmm(user["day_start"]) or time(9, 0), tz_name)
    window_end = combine(day, parse_hhmm(user["day_end"]) or time(22, 0), tz_name)

    free = free_slots(
        window_start,
        window_end,
        [(start, end) for start, end, _ in busy],
        MIN_FREE_SLOT_MIN,
    )
    busy.sort(key=lambda item: item[0])
    return DayPlan(day=day, busy=busy, all_day_events=all_day, free=free, notion_error=notion_error)


def render_day_plan(plan: DayPlan) -> str:
    """DayPlan ni foydalanuvchiga ko'rsatiladigan matnga aylantiradi."""
    lines = [f"🗓 <b>{fmt_date(plan.day)}</b>", ""]

    if plan.all_day_events:
        lines.append("<b>Kun bo'yi:</b>")
        lines += [f"  {event.title}" for event in plan.all_day_events]
        lines.append("")

    if plan.busy:
        lines.append("<b>Band vaqtlar:</b>")
        for start, end, title in plan.busy:
            lines.append(f"  ⛔ {start.strftime('%H:%M')}–{end.strftime('%H:%M')} — {title}")
    else:
        lines.append("<b>Band vaqtlar:</b> yo'q — kuningiz butunlay bo'sh 🎉")
    lines.append("")

    if plan.free:
        lines.append("<b>Bo'sh vaqtlaringiz:</b>")
        for start, end in plan.free:
            lines.append(
                f"  ✅ {start.strftime('%H:%M')}–{end.strftime('%H:%M')} "
                f"({human_duration(end - start)})"
            )
    else:
        lines.append("<b>Bo'sh vaqtlaringiz:</b> bu kuni bo'sh oraliq qolmadi 😅")

    if plan.notion_error:
        lines += ["", f"⚠️ {plan.notion_error}"]

    return "\n".join(lines)
