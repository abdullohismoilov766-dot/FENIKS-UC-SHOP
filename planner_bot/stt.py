"""
Ovozli xabarni matnga o'girish (speech-to-text).

Telegram ovozli xabarni .oga (Opus) faylida beradi. Uni Whisper'ga mos
(OpenAI-mos) transkripsiya endpoint'iga yuboramiz. STT_API_KEY qo'yilmagan
bo'lsa, funksiya None qaytaradi va bot foydalanuvchidan matn yozishni so'raydi.
"""

from __future__ import annotations

import logging

import aiohttp

from planner_bot.config import (
    STT_API_KEY,
    STT_API_URL,
    STT_LANGUAGE,
    STT_MODEL,
    stt_enabled,
)

logger = logging.getLogger(__name__)

MAX_VOICE_BYTES = 20 * 1024 * 1024  # 20 MB — API'lar odatda shu atrofda cheklaydi


async def transcribe(audio: bytes, filename: str = "voice.oga") -> str | None:
    """Ovoz baytlarini matnga o'giradi. Xatolik bo'lsa None qaytaradi."""
    if not stt_enabled():
        return None
    if len(audio) > MAX_VOICE_BYTES:
        logger.warning("Ovozli xabar juda katta: %s bayt", len(audio))
        return None

    form = aiohttp.FormData()
    form.add_field("file", audio, filename=filename, content_type="audio/ogg")
    form.add_field("model", STT_MODEL)
    if STT_LANGUAGE:
        form.add_field("language", STT_LANGUAGE)

    headers = {"Authorization": f"Bearer {STT_API_KEY}"}
    timeout = aiohttp.ClientTimeout(total=120)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(STT_API_URL, data=form, headers=headers) as resp:
                if resp.status != 200:
                    logger.error(
                        "STT xatosi %s: %s", resp.status, (await resp.text())[:300]
                    )
                    return None
                payload = await resp.json()
    except Exception:
        logger.exception("Ovozni matnga o'girishda xatolik")
        return None

    text = (payload.get("text") or "").strip()
    return text or None
