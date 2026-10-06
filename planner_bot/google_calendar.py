"""
Google Calendar bilan ishlash — botning asosiy kalendar backend'i.

Nega Notion emas: KUNDALIK tizimi (Claude suhbati orqali) allaqachon shu
foydalanuvchining haqiqiy Google Calendar'iga yozadi (namoz vaqtlari va
hk). Bot ham SHU kalendarga yozsa — bitta joy, ikkita kirish eshigi
(Telegram va Claude chat), hech qanday ikkilanish yo'q.

Ikki amal kerak (notion.py bilan bir xil interfeys):
  * create_event(...)  — "buni shu sanaga yozib qo'y" so'rovini kalendarga yozish
  * list_events(...)   — "ertaga nechida bo'sh vaqtim bor?" uchun band vaqtlarni olish

Autentifikatsiya: Google Service Account (JSON kalit, .env da
GOOGLE_SERVICE_ACCOUNT_JSON). Bir martalik sozlash kerak — DEPLOY.md ga
qarang: Google Cloud'da service account yaratib, uning email'ini haqiqiy
Google kalendaringizga "Make changes to events" huquqi bilan qo'shasiz.
"""

from __future__ import annotations

import base64
import json
import logging
import time as _time
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from urllib.parse import quote

import aiohttp
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from planner_bot.config import (
    GOOGLE_CALENDAR_ID,
    GOOGLE_SERVICE_ACCOUNT_JSON,
    google_calendar_enabled,
)
from planner_bot.timeutil import combine, tz_of

logger = logging.getLogger(__name__)

API_ROOT = "https://www.googleapis.com/calendar/v3"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = "https://www.googleapis.com/auth/calendar"


class GoogleCalendarError(RuntimeError):
    """Google Calendar so'rovi muvaffaqiyatsiz tugadi (foydalanuvchiga ko'rsatiladi)."""


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


_cached_token: str | None = None
_cached_token_exp: float = 0.0


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _load_service_account() -> dict:
    if not GOOGLE_SERVICE_ACCOUNT_JSON:
        raise GoogleCalendarError(
            "Google Calendar ulanmagan. .env faylida GOOGLE_SERVICE_ACCOUNT_JSON "
            "va GOOGLE_CALENDAR_ID ni to'ldiring."
        )
    try:
        return json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
    except json.JSONDecodeError as exc:
        raise GoogleCalendarError(f"GOOGLE_SERVICE_ACCOUNT_JSON noto'g'ri JSON: {exc}") from exc


def _sign_jwt(account: dict) -> str:
    now = int(_time.time())
    header = {"alg": "RS256", "typ": "JWT"}
    payload = {
        "iss": account["client_email"],
        "scope": SCOPE,
        "aud": TOKEN_URL,
        "iat": now,
        "exp": now + 3600,
    }
    signing_input = (
        _b64url(json.dumps(header, separators=(",", ":")).encode())
        + "."
        + _b64url(json.dumps(payload, separators=(",", ":")).encode())
    )
    private_key = serialization.load_pem_private_key(account["private_key"].encode(), password=None)
    signature = private_key.sign(signing_input.encode(), padding.PKCS1v15(), hashes.SHA256())
    return f"{signing_input}.{_b64url(signature)}"


async def _get_access_token() -> str:
    """Service account uchun OAuth2 access token oladi, muddati tugaguncha keshlaydi."""
    global _cached_token, _cached_token_exp
    if _cached_token and _time.time() < _cached_token_exp - 60:
        return _cached_token

    account = _load_service_account()
    assertion = _sign_jwt(account)

    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(
            TOKEN_URL,
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": assertion,
            },
        ) as resp:
            body = await resp.json(content_type=None)
            if resp.status >= 400:
                logger.error("Google token xatosi %s: %s", resp.status, body)
                raise GoogleCalendarError(
                    f"Google autentifikatsiya xatosi ({resp.status}): "
                    f"{(body or {}).get('error_description', body)}"
                )

    _cached_token = body["access_token"]
    _cached_token_exp = _time.time() + int(body.get("expires_in", 3600))
    return _cached_token


async def _request(method: str, path: str, *, payload: dict | None = None, params: dict | None = None) -> dict:
    if not google_calendar_enabled():
        raise GoogleCalendarError(
            "Google Calendar ulanmagan. .env faylida GOOGLE_SERVICE_ACCOUNT_JSON "
            "va GOOGLE_CALENDAR_ID ni to'ldiring."
        )
    token = await _get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.request(
            method, f"{API_ROOT}{path}", json=payload, params=params, headers=headers
        ) as resp:
            body = await resp.json(content_type=None)
            if resp.status >= 400:
                message = (body or {}).get("error", {}).get("message", "noma'lum xato")
                logger.error("Google Calendar %s %s -> %s: %s", method, path, resp.status, message)
                raise GoogleCalendarError(f"Google Calendar xatosi ({resp.status}): {message}")
            return body or {}


async def create_event(
    title: str,
    day: date,
    start_time: str | None,
    end_time: str | None,
    tz_name: str,
    notes: str = "",
) -> str:
    """Google Calendar'ga bitta hodisa qo'shadi va uning havolasini (htmlLink) qaytaradi."""
    if start_time:
        start_dt = combine(day, datetime.strptime(start_time, "%H:%M").time(), tz_name)
        if end_time:
            end_dt = combine(day, datetime.strptime(end_time, "%H:%M").time(), tz_name)
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)
        else:
            end_dt = start_dt + timedelta(hours=1)
        body: dict = {
            "summary": title[:500],
            "start": {"dateTime": start_dt.isoformat(), "timeZone": tz_name},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": tz_name},
        }
    else:
        body = {
            "summary": title[:500],
            "start": {"date": day.isoformat()},
            "end": {"date": (day + timedelta(days=1)).isoformat()},
        }
    if notes:
        body["description"] = notes[:8000]

    data = await _request(
        "POST", f"/calendars/{quote(GOOGLE_CALENDAR_ID, safe='')}/events", payload=body
    )
    return data.get("htmlLink", "")


def _parse_google_dt(value: dict, tz_name: str) -> tuple[datetime | None, bool]:
    if "date" in value:
        parsed = datetime.fromisoformat(value["date"]).replace(tzinfo=tz_of(tz_name))
        return parsed, True
    if "dateTime" in value:
        parsed = datetime.fromisoformat(value["dateTime"])
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=tz_of(tz_name))
        return parsed.astimezone(tz_of(tz_name)), False
    return None, False


async def list_events(day_from: date, day_to: date, tz_name: str) -> list[Event]:
    """[day_from; day_to] oralig'idagi hodisalarni boshlanish vaqti bo'yicha qaytaradi."""
    time_min = combine(day_from, datetime.min.time(), tz_name).isoformat()
    time_max = combine(day_to + timedelta(days=1), datetime.min.time(), tz_name).isoformat()
    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": "250",
    }
    data = await _request(
        "GET", f"/calendars/{quote(GOOGLE_CALENDAR_ID, safe='')}/events", params=params
    )

    events: list[Event] = []
    for item in data.get("items", []):
        if item.get("status") == "cancelled":
            continue
        start, all_day = _parse_google_dt(item.get("start", {}), tz_name)
        end, _ = _parse_google_dt(item.get("end", {}), tz_name)
        if start is None:
            continue
        events.append(
            Event(
                title=item.get("summary", "(nomsiz)"),
                start=None if all_day else start,
                end=None if all_day else end,
                all_day=all_day,
                url=item.get("htmlLink", ""),
            )
        )
    events.sort(key=lambda e: (e.all_day, e.start or datetime.max.replace(tzinfo=tz_of(tz_name))))
    return events
