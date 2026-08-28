# Botni haqiqiy ishga tushirish

Bu yerda ikkita savolga javob bor:
1. **Qanday login/parollar kerak** va ularni qayerdan olasiz
2. **Botni qayerda ishlatasiz** — 3 ta variant

---

## 1. Kerakli kalitlar

> ⚠️ **Bu kalitlarni hech kimga yubormang** — na chatga, na skrinshotga, na
> GitHub'ga. Kalit qo'lga tushsa, uni bilgan har kim sizning botingizni va
> Notion'ingizni boshqara oladi. Hammasi faqat `.env` faylida yashaydi, u esa
> `.gitignore` da — GitHub'ga hech qachon tushmaydi.

### 🔴 Majburiy — bittasi

| Nima | Qayerdan olinadi |
|---|---|
| **Telegram bot tokeni** | Telegramda [@BotFather](https://t.me/BotFather) → `/newbot` → botga nom bering → username bering (`..._bot` bilan tugashi shart) → token beradi |

Token shunday ko'rinadi: `7891234567:AAHk3mZ...` — nuqta-vergul chap tomonda raqam, o'ngda uzun harflar.

Shu bittasi bilan bot **allaqachon ishlaydi**: kundalik rejalar, eslatmalar,
«Ha / Yo'q» savoli va statistika — hammasi.

### 🟡 Ixtiyoriy — har biri bitta imkoniyatni qo'shadi

| Nima | Nima beradi | Qayerdan olinadi |
|---|---|---|
| **Anthropic API kaliti** | «Ertaga soat 3 da stomatolog» kabi erkin gaplarni tushunish | [console.anthropic.com](https://console.anthropic.com) → ro'yxatdan o'ting → Settings → API Keys → **Create Key**. Balansga pul tashlash kerak (bir necha dollar uzoqqa yetadi) |
| **Notion kaliti** | Kalendarga yozish va o'qish | [notion.so/my-integrations](https://www.notion.so/my-integrations) → **New integration** → nom bering → **Internal Integration Secret** ni nusxalang |
| **Notion baza ID si** | Qaysi kalendarga yozilsin | Kalendar bazangizni Notion'da oching → havoladagi 32 belgili qism:<br>`notion.so/ish/`**`a1b2c3d4e5f67890abcdef1234567890`**`?v=...` |
| **Ovoz kaliti** | Ovozli xabarlarni tushunish | Whisper'ga mos xizmat, masalan [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |

**Notion uchun yana bitta muhim qadam:** kalitni olganingizdan keyin kalendar
bazangizni oching → yuqori o'ngdagi `•••` → **Connections** → yaratgan
integratsiyangizni tanlang. Busiz bot bazani **ko'rmaydi** (404 xatosi beradi).

Bazada kamida ikkita ustun bo'lsin: **title** turidagi (odatda `Name`) va
**date** turidagi (odatda `Date`). Nomlari boshqacha bo'lsa, sozlashda aytasiz.

### Kalitlarni joylash

Hech qanday faylni qo'lda tahrirlash shart emas — shuni ishga tushiring:

```bash
python -m planner_bot.setup
```

Skript har birini navbat bilan so'raydi, to'g'ri-noto'g'riligini tekshiradi va
`planner_bot/.env` fayliga yozadi. Ixtiyoriylarini Enter bosib o'tkazib
yuborsangiz — o'sha imkoniyat o'chiq qoladi, qolgani ishlayveradi.

---

## 2. Bot qayerda ishlaydi

Bot doim ishlab turishi kerak — eslatma yuborish uchun. Uch variant:

### Variant A — o'z kompyuteringizda (sinash uchun)

```bash
git clone https://github.com/abdullohismoilov766-dot/FENIKS-UC-SHOP.git
cd FENIKS-UC-SHOP

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r planner_bot/requirements.txt

python -m planner_bot.setup       # kalitlarni kiritasiz
python -m planner_bot.bot         # bot ishga tushadi
```

Terminalni yopsangiz yoki kompyuter o'chsa — bot ham to'xtaydi. Sinash uchun
yaxshi, kundalik ishlatish uchun emas.

### Variant B — Railway (eng oson, doim ishlaydi) ⭐

1. [railway.app](https://railway.app) ga GitHub akkauntingiz bilan kiring
2. **New Project** → **Deploy from GitHub repo** → shu repozitoriyni tanlang
3. Branch sifatida `claude/daily-plan-tracker-bot-069e57` ni ko'rsating
   (yoki avval uni `main` ga qo'shib oling)
4. **Variables** bo'limiga o'ting va kalitlarni **shu yerga** yozing —
   `.env` faylini yuklamang:

   | Nomi | Qiymati |
   |---|---|
   | `PLANNER_BOT_TOKEN` | BotFather bergan token |
   | `TIMEZONE` | `Asia/Tashkent` |
   | `DAY_START` | `09:00` |
   | `DAY_END` | `22:00` |
   | `PLANNER_DB_PATH` | `/data/planner.db` |
   | `ANTHROPIC_API_KEY` | (ixtiyoriy) |
   | `NOTION_TOKEN` | (ixtiyoriy) |
   | `NOTION_DATABASE_ID` | (ixtiyoriy) |
   | `STT_API_KEY` | (ixtiyoriy) |

5. **Settings** → **Volumes** → yangi volume qo'shing, mount yo'li: `/data`
   — busiz har qayta ishga tushganda **statistikangiz o'chib ketadi**
6. Deploy tugagach, Telegramda botingizga `/start` yuboring

> Render.com'da ham xuddi shunday, faqat servis turi **Background Worker**
> bo'lsin ("Web Service" emas — bu bot port ochmaydi, polling bilan ishlaydi).

### Variant C — o'z serveringiz (VPS)

```bash
sudo apt update && sudo apt install -y python3-venv git
git clone https://github.com/abdullohismoilov766-dot/FENIKS-UC-SHOP.git /opt/feniks
cd /opt/feniks
python3 -m venv venv
./venv/bin/pip install -r planner_bot/requirements.txt
./venv/bin/python -m planner_bot.setup
```

Keyin systemd xizmati sifatida doimiy ishga tushiring:

```ini
# /etc/systemd/system/feniks-planner.service
[Unit]
Description=FENIKS Planner Telegram bot
After=network-online.target

[Service]
WorkingDirectory=/opt/feniks
ExecStart=/opt/feniks/venv/bin/python -m planner_bot.bot
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now feniks-planner
sudo systemctl status feniks-planner      # holatini ko'rish
journalctl -u feniks-planner -f           # jonli loglar
```

---

## 3. Ishlayotganini tekshirish

Bot ishga tushganda logda shunday chiqadi — qaysi imkoniyat yoqilganini
shu yerdan ko'rasiz:

```
  FENIKS PLANNER ishga tushdi
  ----------------------------------------
  [+] Kundalik rejalar, eslatmalar, statistika
  [+] Erkin matnni tushunish (Claude)
  [ ] Notion kalendar
  [ ] Ovozli xabarlar
  ----------------------------------------
```

Keyin Telegramda:

1. `/start` → menyu chiqishi kerak
2. `➕ Yangi reja` → nom → hozirgi vaqtdan **2 daqiqa keyin** tugaydigan oraliq
   qo'ying (masalan hozir 14:30 bo'lsa: `14:28-14:32`)
3. Kuting — muddat tugagach «Bajardingizmi?» savoli **✅ Ha / ❌ Yo'q** tugmalari
   bilan kelishi kerak
4. Tugmani bosing → `📊 Statistika` da hisobga qo'shilganini ko'rasiz

---

## Tez-tez uchraydigan muammolar

| Belgi | Sababi va yechimi |
|---|---|
| `PLANNER_BOT_TOKEN topilmadi` | `.env` yaratilmagan → `python -m planner_bot.setup` |
| `Unauthorized` xatosi | Token noto'g'ri yoki BotFather'da bekor qilingan → `/revoke` bilan yangisini oling |
| Eslatmalar noto'g'ri vaqtda keladi | Vaqt mintaqasi xato → botda `/settings` → 🌍 Vaqt mintaqasi |
| Notion: `Could not find database` | Bazani integratsiyaga ulamagansiz → baza → `•••` → **Connections** |
| Notion: `property does not exist` | Ustun nomlari boshqacha → `NOTION_TITLE_PROP` / `NOTION_DATE_PROP` ni moslang |
| Qayta ishga tushgach statistika yo'q | Doimiy disk (volume) ulanmagan → `PLANNER_DB_PATH` va volume'ni tekshiring |
| Ovozli xabar ishlamayapti | `STT_API_KEY` qo'yilmagan yoki balans tugagan |

**Agar token boshqa birovga ko'rinib qolsa:** darhol @BotFather → `/revoke` →
botingizni tanlang. Eski token o'sha zahoti ishlamay qoladi, yangisini
`python -m planner_bot.setup` orqali qayta kiritasiz.
