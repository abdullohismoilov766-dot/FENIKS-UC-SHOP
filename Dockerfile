# FENIKS PLANNER — Telegram bot konteyneri
FROM python:3.12-slim

# Vaqt mintaqalari ma'lumotlari (Asia/Tashkent va h.k.) uchun
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY planner_bot/requirements.txt ./planner_bot/requirements.txt
RUN pip install --no-cache-dir -r planner_bot/requirements.txt

COPY planner_bot ./planner_bot

# Baza konteyner ichida saqlanadi — hosting'da doimiy disk (volume) ulang,
# aks holda qayta ishga tushganda statistika yo'qoladi.
ENV PLANNER_DB_PATH=/data/planner.db
VOLUME ["/data"]

CMD ["python", "-m", "planner_bot.bot"]
