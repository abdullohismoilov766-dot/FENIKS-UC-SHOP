"""
Statistika: qancha reja bajarildi, qanchasi bajarilmadi va qaysi reja eng ko'p
qoldirilmoqda. Manba — task_logs jadvali (har bir reja x har bir kun uchun bitta yozuv).
"""

from __future__ import annotations

from datetime import date, timedelta

from planner_bot import db
from planner_bot.timeutil import fmt_date

PERIODS = {
    "today": ("Bugun", 0),
    "week": ("Oxirgi 7 kun", 6),
    "month": ("Oxirgi 30 kun", 29),
    "all": ("Butun davr", None),
}


def period_range(period: str, today: date) -> tuple[date, date, str]:
    label, back = PERIODS.get(period, PERIODS["week"])
    if back is None:
        return date(2000, 1, 1), today, label
    return today - timedelta(days=back), today, label


def _bar(percent: int, width: int = 10) -> str:
    filled = round(percent / 100 * width)
    return "▰" * filled + "▱" * (width - filled)


def current_streak(user_id: int, today: date, max_days: int = 180) -> int:
    """Ketma-ket necha kun birorta ham reja qoldirilmagan (bugundan orqaga)."""
    start = today - timedelta(days=max_days)
    totals = {row["log_date"]: row for row in db.daily_totals(user_id, start.isoformat(), today.isoformat())}

    streak = 0
    day = today
    while day >= start:
        row = totals.get(day.isoformat())
        if row is None or row["total"] == 0:
            # Reja bo'lmagan kun ketma-ketlikni buzmaydi, lekin uni ham sanamaydi
            if day == today:
                day -= timedelta(days=1)
                continue
            break
        if row["missed"] > 0:
            break
        if row["done"] == 0 and day != today:
            break
        streak += 1
        day -= timedelta(days=1)
    return streak


def render_stats(user_id: int, period: str, today: date) -> str:
    date_from, date_to, label = period_range(period, today)
    counts = db.status_counts(user_id, date_from.isoformat(), date_to.isoformat())

    done = counts[db.STATUS_DONE]
    missed = counts[db.STATUS_MISSED]
    pending = counts[db.STATUS_PENDING]
    answered = done + missed
    total = answered + pending
    percent = round(done / answered * 100) if answered else 0

    if total == 0:
        return (
            f"📊 <b>{label}</b>\n\n"
            "Bu davr uchun hali ma'lumot yo'q. Reja qo'shing — muddat tugagach "
            "bot so'raydi va natijalar shu yerda to'planadi."
        )

    lines = [f"📊 <b>Statistika — {label}</b>"]
    if period != "today":
        lines.append(f"<i>{fmt_date(date_from)} — {fmt_date(date_to)}</i>")
    lines += [
        "",
        f"{_bar(percent)}  <b>{percent}%</b>",
        "",
        f"✅ Bajarildi: <b>{done}</b>",
        f"❌ Bajarilmadi: <b>{missed}</b>",
        f"⏳ Javob berilmagan: <b>{pending}</b>",
        f"📌 Jami: <b>{total}</b>",
    ]

    streak = current_streak(user_id, today)
    if streak:
        lines.append(f"🔥 Toza kunlar ketma-ketligi: <b>{streak}</b> kun")

    rows = db.per_task_counts(user_id, date_from.isoformat(), date_to.isoformat())
    if rows:
        lines += ["", "<b>Rejalar bo'yicha:</b>"]
        for row in rows[:12]:
            row_answered = (row["done"] or 0) + (row["missed"] or 0)
            row_percent = round((row["done"] or 0) / row_answered * 100) if row_answered else 0
            lines.append(
                f"  • {row['title']} ({row['start_time']}–{row['end_time']}) — "
                f"✅ {row['done'] or 0} / ❌ {row['missed'] or 0}  ({row_percent}%)"
            )

    worst = max(rows, key=lambda r: r["missed"] or 0, default=None)
    if worst is not None and (worst["missed"] or 0) > 0:
        lines += ["", f"⚠️ Eng ko'p qoldirilgan reja: <b>{worst['title']}</b> "
                      f"({worst['missed']} marta)"]

    return "\n".join(lines)


def render_today(user_id: int, today: date) -> str:
    """Bugungi rejalar va ularning joriy holati."""
    rows = db.logs_for_date(user_id, today.isoformat())
    if not rows:
        return (
            "📋 Bugun uchun hali faollashgan reja yo'q.\n\n"
            "Rejalaringiz o'z boshlanish vaqti kelganda shu ro'yxatda paydo bo'ladi."
        )

    lines = [f"📋 <b>Bugungi rejalar — {fmt_date(today)}</b>", ""]
    for row in rows:
        label = db.STATUS_LABELS.get(row["status"], row["status"])
        lines.append(f"{label}  {row['start_time']}–{row['end_time']} — {row['title']}")
    return "\n".join(lines)
