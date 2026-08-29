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

Bu botni qayerda ishlatishingizga bog'liq:

**Bulutda (Railway / Render) — Variant A:** hech qanday fayl kerak emas.
Kalitlarni hosting saytining **Variables** bo'limiga yozasiz, tamom.
Kompyuter ham, terminal ham shart emas.

**Kompyuterda yoki VPS'da — Variant B/C:** shuni ishga tushiring:

```bash
python -m planner_bot.setup
```

Skript har birini navbat bilan so'raydi, to'g'ri-noto'g'riligini tekshiradi va
`planner_bot/.env` fayliga yozadi. Ixtiyoriylarini Enter bosib o'tkazib
yuborsangiz — o'sha imkoniyat o'chiq qoladi, qolgani ishlayveradi.

---

## 2. Bot qayerda ishlaydi

Bot doim ishlab turishi kerak — eslatma yuborish uchun. Telefonda Python
ilovasi bu ish uchun yaramaydi (iOS orqa fonda ishlatmaydi). Variantlar:

### ⭐ Variant A — Railway (telefondan ham bo'ladi, doim ishlaydi)

Kompyuteringiz yo'q bo'lsa ham bo'ladi. iPhone'ga Python o'rnatish **kerak
emas va foyda ham bermaydi** — iOS ilovani orqa fonda uzoq ishlatmaydi, ilova
yopilishi bilan bot to'xtaydi. Buning o'rniga bot bulutda ishlaydi, siz esa
uni brauzerdan boshqarasiz.

Hammasi telefon brauzerida, ~10 daqiqa:

**1-qadam. Token oling (Telegram ilovasida)**
- [@BotFather](https://t.me/BotFather) ga kiring → `/newbot`
- Botga nom bering (masalan: `Mening rejalarim`)
- Username bering — `_bot` bilan tugashi shart (masalan: `abdulloh_reja_bot`)
- BotFather tokenni beradi → uni **uzoq bosib nusxalang** va o'zingizga
  Telegramda "Saved Messages" ga tashlab qo'ying

**2-qadam. Railway'ga kiring**
- Safari'da [railway.app](https://railway.app) → **Login** → **Login with GitHub**
- GitHub akkauntingizga ruxsat bering

**3-qadam. Loyihani ulang**
- **New Project** → **Deploy from GitHub repo**
- Ro'yxatdan `FENIKS-UC-SHOP` ni tanlang
- Ochilgan servis → **Settings** → **Source** → **Branch** →
  `claude/daily-plan-tracker-bot-069e57` ni tanlang

**4-qadam. Kalitlarni kiriting**
- **Variables** bo'limiga o'ting → **New Variable** → quyidagilarni birma-bir
  qo'shing (`.env` faylini yuklamang, faqat shu yerga yozing):

  | Nomi | Qiymati |
  |---|---|
  | `PLANNER_BOT_TOKEN` | BotFather bergan token |
  | `TIMEZONE` | `Asia/Tashkent` |
  | `DAY_START` | `09:00` |
  | `DAY_END` | `22:00` |
  | `PLANNER_DB_PATH` | `/data/planner.db` |

  Claude, Notion va ovoz kalitlarini keyinroq ham qo'shsangiz bo'ladi —
  ularsiz ham rejalar, eslatmalar va statistika to'liq ishlaydi.

**5-qadam. Doimiy disk ulang (muhim!)**
- **Settings** → **Volumes** → **New Volume**
- Mount path: `/data`
- Busiz har yangilanishda **butun statistikangiz o'chib ketadi**

**6-qadam. Tekshiring**
- **Deployments** → oxirgi deploy → **View Logs**
- Logda `FENIKS PLANNER ishga tushdi` yozuvi chiqishi kerak
- Telegramda botingizni oching → `/start`

Shu bilan bot doim yoqiq turadi — telefoningiz o'chgan bo'lsa ham eslatmalar
keladi.

> 💡 **Narx haqida:** Railway'da boshlang'ich bepul kredit bor, u tugagach
> oylik to'lov boshlanadi. Render.com'da ham shunga o'xshash (u yerda servis
> turi **Background Worker** bo'lsin, "Web Service" emas). Tariflar tez-tez
> o'zgaradi — ro'yxatdan o'tishdan oldin joriy narxni saytdan ko'ring.
> Arzonroq variant — oddiy VPS (Variant C).

---

### Variant B — o'z kompyuteringizda (faqat sinash uchun)

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
| `PLANNER_BOT_TOKEN topilmadi` | `.env` yaratilmagan → `python -m planner_bot.setup`, bulutda esa **Variables** bo'limiga yozilmagan |
| Telefonda Python ilovasida ishlamadi | iOS ilovani orqa fonda ishlatmaydi — bot 24/7 turolmaydi. Variant A (Railway) dan foydalaning |
| `Unauthorized` xatosi | Token noto'g'ri yoki BotFather'da bekor qilingan → `/revoke` bilan yangisini oling |
| Eslatmalar noto'g'ri vaqtda keladi | Vaqt mintaqasi xato → botda `/settings` → 🌍 Vaqt mintaqasi |
| Notion: `Could not find database` | Bazani integratsiyaga ulamagansiz → baza → `•••` → **Connections** |
| Notion: `property does not exist` | Ustun nomlari boshqacha → `NOTION_TITLE_PROP` / `NOTION_DATE_PROP` ni moslang |
| Qayta ishga tushgach statistika yo'q | Doimiy disk (volume) ulanmagan → `PLANNER_DB_PATH` va volume'ni tekshiring |
| Ovozli xabar ishlamayapti | `STT_API_KEY` qo'yilmagan yoki balans tugagan |

**Agar token boshqa birovga ko'rinib qolsa:** darhol @BotFather → `/revoke` →
botingizni tanlang. Eski token o'sha zahoti ishlamay qoladi, yangisini
`python -m planner_bot.setup` orqali qayta kiritasiz.
