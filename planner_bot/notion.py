"""
Notion kalendari bilan ishlash.

Ikki amal kerak:
  * create_event(...)  — "buni shu sanaga yozib qo'y" so'rovini kalendarga yozish
  * list_events(...)   — "ertaga nechida bo'sh vaqtim bor?" uchun band vaqtlarni olish

Notion bazangizda kamida ikkita ustun bo'lishi kerak: sarlavha (title) va sana
(date). Ularning nomlari .env dagi NOTION_TITLE_PROP / NOTION_DATE_PROP orqali
sozlanadi.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta

import aiohttp

from planner_bot.config import (
    NOTION_DATABASE_ID,
    NOTION_DATE_PROP,
    NOTION_TITLE_PROP,
    NOTION_TOKEN,
    NOTION_VERSION,
    notion_enabled,
)
from planner_bot.timeutil import combine, tz_of

logger = logging.getLogger(__name__)

API_ROOT = "https://api.notion.com/v1"


class NotionError(RuntimeError):
    """Notion so'rovi muvaffaqiyatsiz tugadi (foydalanuvchiga ko'rsatiladi)."""


@dataclass
class Event:
    title: str
    start: datetime | None
    end: datetime | None
    all_day: bool
    url: str = ""

    def label(self) -> str:
        if self.all_day or not self.start:
            return f"🔸 {self.title} — kun bo'yi"
        end = f"–{self.end.strftime('%H:%M')}" if self.end else ""
        return f"🔸 {self.start.strftime('%H:%M')}{end} — {self.title}"


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


async def _request(method: str, path: str, payload: dict | None = None) -> dict:
    if not notion_enabled():
        raise NotionError(
            "Notion ulanmagan. .env faylida NOTION_TOKEN va NOTION_DATABASE_ID ni to'ldiring."
        )
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.request(
            method, f"{API_ROOT}{path}", json=payload, headers=_headers()
        ) as resp:
            body = await resp.json(content_type=None)
            if resp.status >= 400:
                message = (body or {}).get("message", "noma'lum xato")
                logger.error("Notion %s %s -> %s: %s", method, path, resp.status, message)
                raise NotionError(f"Notion xatosi ({resp.status}): {message}")
            return body or {}


def _plain_title(properties: dict) -> str:
    prop = properties.get(NOTION_TITLE_PROP) or {}
    parts = prop.get("title") or []
    text = "".join(part.get("plain_text", "") for part in parts).strip()
    return text or "(nomsiz)"


def _parse_iso(value: str, tz_name: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=tz_of(tz_name))
    return parsed.astimezone(tz_of(tz_name))


async def create_event(
    title: str,
    day: date,
    start_time: str | None,
    end_time: str | None,
    tz_name: str,
    notes: str = "",
) -> str:
    """Notion kalendariga bitta yozuv qo'shadi va uning havolasini qaytaradi."""
    if start_time:
        start_dt = combine(day, datetime.strptime(start_time, "%H:%M").time(), tz_name)
        date_value: dict = {"start": start_dt.isoformat()}
        if end_time:
            end_dt = combine(day, datetime.strptime(end_time, "%H:%M").time(), tz_name)
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)
            date_value["end"] = end_dt.isoformat()
    else:
        date_value = {"start": day.isoformat()}

    payload: dict = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            NOTION_TITLE_PROP: {"title": [{"text": {"content": title[:200]}}]},
            NOTION_DATE_PROP: {"date": date_value},
        },
    }
    if notes:
        payload["children"] = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": notes[:1900]}}]},
            }
        ]

    page = await _request("POST", "/pages", payload)
    return page.get("url", "")


async def list_events(day_from: date, day_to: date, tz_name: str) -> list[Event]:
    """[day_from; day_to] oralig'idagi yozuvlarni sana bo'yicha tartiblab qaytaradi."""
    payload = {
        "filter": {
            "and": [
                {"property": NOTION_DATE_PROP, "date": {"on_or_after": day_from.isoformat()}},
                {
                    "property": NOTION_DATE_PROP,
                    "date": {"before": (day_to + timedelta(days=1)).isoformat()},
                },
            ]
        },
        "sorts": [{"property": NOTION_DATE_PROP, "direction": "ascending"}],
        "page_size": 100,
    }
    data = await _request("POST", f"/databases/{NOTION_DATABASE_ID}/query", payload)

    events: list[Event] = []
    for page in data.get("results", []):
        properties = page.get("properties", {})
        date_prop = (properties.get(NOTION_DATE_PROP) or {}).get("date") or {}
        raw_start = date_prop.get("start") or ""
        if not raw_start:
            continue
        all_day = "T" not in raw_start
        events.append(
            Event(
                title=_plain_title(properties),
                start=_parse_iso(raw_start, tz_name),
                end=_parse_iso(date_prop.get("end") or "", tz_name),
                all_day=all_day,
                url=page.get("url", ""),
            )
        )
    events.sort(key=lambda e: (e.all_day, e.start or datetime.max.replace(tzinfo=tz_of(tz_name))))
    return events
