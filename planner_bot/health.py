"""
Kichik HTTP sahifa — tekin hosting tariflari uchun.

Ko'p tekin tariflar (Render, Koyeb va h.k.) faqat "web service" ni tekin
beradi, ya'ni dastur porti ochib turishini talab qiladi. Bu bot esa polling
bilan ishlaydi va portga muhtoj emas. Shuning uchun `PORT` o'zgaruvchisi
berilgan bo'lsa (hosting uni o'zi qo'yadi), bot yonida shu kichik sahifa
ham ishga tushadi — hosting "ishlayapti" deb hisoblaydi.

Bundan tashqari, bu sahifa uxlab qolishning oldini olish uchun ham kerak:
tekin tariflar bir necha daqiqa so'rov kelmasa dasturni to'xtatib qo'yadi.
UptimeRobot yoki cron-job.org kabi tekin xizmat har 5 daqiqada shu manzilga
kirib tursa, bot uyg'oq qoladi.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from aiohttp import web

logger = logging.getLogger(__name__)

STARTED_AT = datetime.now(timezone.utc)


async def _health(_request: web.Request) -> web.Response:
    uptime = datetime.now(timezone.utc) - STARTED_AT
    return web.json_response(
        {
            "status": "ok",
            "service": "feniks-planner",
            "uptime_seconds": int(uptime.total_seconds()),
        }
    )


async def start_health_server(port: int) -> web.AppRunner:
    """Sahifani ishga tushiradi va uni to'xtatish uchun runner qaytaradi."""
    app = web.Application()
    app.router.add_get("/", _health)
    app.router.add_get("/health", _health)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    logger.info("Health sahifasi %s portda ochildi (tekin hosting uchun)", port)
    return runner
