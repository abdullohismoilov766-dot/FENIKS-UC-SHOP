"""Vaqt bilan ishlash uchun kichik yordamchilar (hammasi bir joyda)."""

from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

WEEKDAY_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

WEEKDAY_UZ = {
    "mon": "Dushanba",
    "tue": "Seshanba",
    "wed": "Chorshanba",
    "thu": "Payshanba",
    "fri": "Juma",
    "sat": "Shanba",
    "sun": "Yakshanba",
}

_TIME_RE = re.compile(r"^([01]?\d|2[0-3])[:.\s]([0-5]\d)$")
# "09:00-10:30", "9.00 - 10.30", "9:00–10:30" (turli tirelar bilan)
_RANGE_RE = re.compile(
    r"^\s*([01]?\d|2[0-3])[:.\s]([0-5]\d)\s*[-–—]\s*([01]?\d|2[0-3])[:.\s]([0-5]\d)\s*$"
)


def tz_of(name: str) -> ZoneInfo:
    """Nomi noto'g'ri bo'lsa ham bot yiqilmasin — UTC ga qaytamiz."""
    try:
        return ZoneInfo(name)
    except Exception:
        return ZoneInfo("UTC")


def now_in(tz_name: str) -> datetime:
    return datetime.now(tz_of(tz_name))


def parse_hhmm(value: str) -> time | None:
    """'09:00', '9.00', '9 00' -> time(9, 0). Aks holda None."""
    m = _TIME_RE.match((value or "").strip())
    if not m:
        return None
    return time(int(m.group(1)), int(m.group(2)))


def parse_range(value: str) -> tuple[time, time] | None:
    """'09:00-10:30' -> (time(9,0), time(10,30)). Aks holda None."""
    m = _RANGE_RE.match(value or "")
    if not m:
        return None
    start = time(int(m.group(1)), int(m.group(2)))
    end = time(int(m.group(3)), int(m.group(4)))
    return start, end


def fmt_time(value: time) -> str:
    return value.strftime("%H:%M")


def parse_date(value: str) -> date | None:
    """'YYYY-MM-DD' -> date. Aks holda None."""
    try:
        return datetime.strptime((value or "").strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def fmt_date(value: date) -> str:
    return value.strftime("%d.%m.%Y") + f" ({WEEKDAY_UZ[WEEKDAY_KEYS[value.weekday()]]})"


def combine(day: date, moment: time, tz_name: str) -> datetime:
    return datetime.combine(day, moment, tzinfo=tz_of(tz_name))


def task_window(day: date, start: time, end: time, tz_name: str) -> tuple[datetime, datetime]:
    """
    Reja oynasi (boshlanish, tugash). Agar tugash vaqti boshlanishdan kichik
    bo'lsa (masalan 23:00–01:00), tugash keyingi kunga o'tkaziladi.
    """
    start_dt = combine(day, start, tz_name)
    end_dt = combine(day, end, tz_name)
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)
    return start_dt, end_dt


def runs_on(repeat: str, on_date: str | None, day: date) -> bool:
    """Reja shu kunda bajarilishi kerakmi?"""
    repeat = (repeat or "daily").strip().lower()
    if repeat == "daily":
        return True
    if repeat == "once":
        return on_date == day.isoformat()
    if repeat == "weekdays":
        return day.weekday() < 5
    if repeat == "weekends":
        return day.weekday() >= 5
    # 'mon,wed,fri' ko'rinishidagi ro'yxat
    keys = {k.strip() for k in repeat.split(",") if k.strip()}
    return WEEKDAY_KEYS[day.weekday()] in keys


def repeat_label(repeat: str, on_date: str | None) -> str:
    repeat = (repeat or "daily").strip().lower()
    if repeat == "daily":
        return "har kuni"
    if repeat == "weekdays":
        return "ish kunlari (Du–Ju)"
    if repeat == "weekends":
        return "dam olish kunlari"
    if repeat == "once":
        d = parse_date(on_date or "")
        return f"bir marta — {fmt_date(d)}" if d else "bir marta"
    keys = [k.strip() for k in repeat.split(",") if k.strip() in WEEKDAY_KEYS]
    if keys:
        return ", ".join(WEEKDAY_UZ[k] for k in keys)
    return repeat


def merge_intervals(
    intervals: list[tuple[datetime, datetime]]
) -> list[tuple[datetime, datetime]]:
    """Kesishuvchi oraliqlarni birlashtiradi."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def free_slots(
    window_start: datetime,
    window_end: datetime,
    busy: list[tuple[datetime, datetime]],
    min_minutes: int,
) -> list[tuple[datetime, datetime]]:
    """Kun oynasidan band oraliqlarni ayirib, bo'sh oraliqlarni qaytaradi."""
    slots: list[tuple[datetime, datetime]] = []
    cursor = window_start
    for start, end in merge_intervals(busy):
        if end <= window_start or start >= window_end:
            continue
        start = max(start, window_start)
        end = min(end, window_end)
        if start - cursor >= timedelta(minutes=min_minutes):
            slots.append((cursor, start))
        cursor = max(cursor, end)
    if window_end - cursor >= timedelta(minutes=min_minutes):
        slots.append((cursor, window_end))
    return slots


def human_duration(delta: timedelta) -> str:
    minutes = int(delta.total_seconds() // 60)
    hours, minutes = divmod(minutes, 60)
    if hours and minutes:
        return f"{hours} soat {minutes} daqiqa"
    if hours:
        return f"{hours} soat"
    return f"{minutes} daqiqa"
