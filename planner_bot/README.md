# FENIKS PLANNER — kundalik reja va vaqt boti

Telegram bot: kundalik rejalaringizni eslatib turadi, muddat tugagach
«bajardingizmi?» deb so'raydi, javoblaringizdan statistika yig'adi,
aytganingizni Google Calendar'ga yozib qo'yadi va «ertaga nechida bo'sh
vaqtim bor?» degan savolga javob beradi.

> 🗓 **Bitta kalendar, ikkita eshik.** Bot shu foydalanuvchining haqiqiy
> Google Calendar'iga yozadi — xuddi shu kalendarga Claude chat (KUNDALIK
> tizimi) namoz vaqtlarini va boshqa rejalarni yozadi. Demak Telegram'dan
> qo'shsangiz ham, Claude'ga aytsangiz ham — bitta kalendarda ko'rinadi.

> Bu bot repozitoriydagi UC-shop botidan **mustaqil** — o'z papkasi, o'z
> tokeni va o'z bazasi bilan ishlaydi. Ikkalasini bir vaqtda ishlatsa bo'ladi.

---

## Nima qiladi

### 1. Kundalik rejalar — «nechidan nechigacha»
`➕ Yangi reja` tugmasi orqali reja qo'shasiz:

```
Nomi:    Ertalabki yugurish
Vaqti:   07:00-08:00
Takror:  🔁 Har kuni / 💼 Ish kunlari / 🌴 Dam olish kunlari / 1️⃣ Faqat bugun
```

### 2. Eslatma va muddat savoli
- **07:00 da** — «⏰ Vaqt keldi! Ertalabki yugurish»
- **08:00 dan keyin** — «❓ Muddat tugadi. Bu rejangizni bajardingizmi?»
  ostida ikkita tugma: **✅ Ha** va **❌ Yo'q**

Javobingiz bazaga yoziladi. 6 soat javob bermasangiz (`AUTO_MISS_HOURS`),
avtomatik «bajarilmadi» bo'ladi — lekin tugmani keyin bossangiz ham o'zgaradi.

### 3. Statistika
`📊 Statistika` — bugun / 7 kun / 30 kun / butun davr kesimida:

```
▰▰▰▰▰▰▰▰▱▱  75%

✅ Bajarildi: 12
❌ Bajarilmadi: 4
⏳ Javob berilmagan: 1
🔥 Toza kunlar ketma-ketligi: 5 kun

Rejalar bo'yicha:
  • Ertalabki yugurish (07:00–08:00) — ✅ 6 / ❌ 1  (86%)
  • Ingliz tili (20:00–21:00) — ✅ 6 / ❌ 3  (67%)

⚠️ Eng ko'p qoldirilgan reja: Ingliz tili (3 marta)
```

### 4. Google Calendar'ga yozish — matn yoki ovoz orqali
Botga shunchaki yozing yoki **ovozli xabar** yuboring:

> «Ertaga soat 3 da stomatologga boraman, kalendarga yozib qo'y»

Bot tushunadi, tasdiqlash so'raydi va Google Calendar'ingizga qo'shadi:

```
🗓 Google Calendar'ga yozaymi?

📌 Stomatolog
📅 29.08.2026 (Shanba)
🕐 15:00 – 16:00

[✅ Ha, yozib qo'y]  [❌ Bekor]
```

### 5. «Ertaga nechida bo'sh vaqtlarim bor?»
Bot **kundalik rejalaringiz** va **Google Calendar'ingizni** birlashtirib,
faol kun oralig'ingizdan bo'sh oraliqlarni ajratib beradi:

```
🗓 29.08.2026 (Shanba)

Band vaqtlar:
  ⛔ 07:00–08:00 — Ertalabki yugurish
  ⛔ 15:00–16:00 — Stomatolog

Bo'sh vaqtlaringiz:
  ✅ 09:00–15:00 (6 soat)
  ✅ 16:00–22:00 (6 soat)
```

---

## O'rnatish

```bash
git clone <repo>
cd FENIKS-UC-SHOP

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r planner_bot/requirements.txt
```

## Sozlash

```bash
python -m planner_bot.setup
```

Skript kerakli kalitlarni navbat bilan so'raydi, to'g'riligini tekshiradi va
`planner_bot/.env` fayliga yozadi. (Qo'lda qilishni xohlasangiz:
`cp planner_bot/.env.example planner_bot/.env` va tahrirlang.)

**Faqat bitta narsa majburiy:**

| O'zgaruvchi | Nima uchun |
|---|---|
| `PLANNER_BOT_TOKEN` | [@BotFather](https://t.me/BotFather) → `/newbot` → token |

Qolganlari ixtiyoriy — har biri bitta imkoniyatni yoqadi:

| O'zgaruvchi | Yoqadigan imkoniyat | Bo'sh bo'lsa |
|---|---|---|
| `ANTHROPIC_API_KEY` + `pip install -r planner_bot/requirements-ai.txt` | Erkin matnni tushunish («ertaga soat 3 da…») | Oddiy regex rejimi — kamroq tushunadi, tugmalar ishlayveradi |
| `GOOGLE_SERVICE_ACCOUNT_JSON` + `GOOGLE_CALENDAR_ID` | Kalendarga yozish va o'qish | Kalendar bo'limi o'chiq, bo'sh vaqt faqat bot rejalaridan hisoblanadi |
| `STT_API_KEY` | Ovozli xabarlar | Bot matn yozishni so'raydi |

### Google Calendar'ni ulash (service account)

1. [console.cloud.google.com](https://console.cloud.google.com) da yangi loyiha
   oching (yoki mavjudini tanlang) → **APIs & Services → Library** → "Google
   Calendar API" ni toping → **Enable**.
2. **APIs & Services → Credentials → Create Credentials → Service account**
   → nom bering (masalan `kundalik-bot`) → yaratilgandan keyin uni oching →
   **Keys → Add Key → Create new key → JSON** → fayl kompyuteringizga tushadi.
3. Shu JSON faylni ochib, **butun matnini** nusxalang — `GOOGLE_SERVICE_ACCOUNT_JSON`
   shu bo'ladi (bitta uzun qator sifatida, hosting saytining Variables
   bo'limiga qo'ysangiz bo'ladi — JSON ichidagi qator ko'chirishlar muammo
   qilmaydi).
4. JSON faylda `"client_email": "...@...gserviceaccount.com"` qatorini toping.
   Google Calendar'ingizni (calendar.google.com) oching → sozlamalar →
   **Share with specific people** → shu email'ni qo'shing → huquq:
   **Make changes to events**.
5. `GOOGLE_CALENDAR_ID` — odatda shu Gmail manzilingiz
   (`abdullohismoilov767@gmail.com`), Calendar sozlamalaridagi **Calendar ID**
   qatoridan ham olish mumkin.

> ⚠️ Service account "o'zining" kalendariga yozmaydi — siz uni *sizning*
> kalendaringizga nazoratchi sifatida qo'shasiz (4-qadam), shundan keyingina
> sizning kalendaringizga yoza oladi.

> 📘 Kalitlarni qayerdan olish va botni doimiy ishlatish (Railway / VPS)
> bo'yicha to'liq qo'llanma: **[DEPLOY.md](DEPLOY.md)**

## Ishga tushirish

Repozitoriyning **ildiz papkasidan** turib:

```bash
python -m planner_bot.bot
```

Telegramda botingizga `/start` yuboring.

> ⚠️ `python planner_bot/bot.py` deb ishga tushirmang — bu papkadagi modul
> nomlari repozitoriy ildizidagi UC-shop fayllari bilan chalkashib ketadi.

## Doim ishlab turishi uchun (VPS)

```bash
nohup python -m planner_bot.bot > planner.log 2>&1 &
```

yoki `systemd` xizmati sifatida:

```ini
# /etc/systemd/system/feniks-planner.service
[Unit]
Description=FENIKS Planner Telegram bot
After=network.target

[Service]
WorkingDirectory=/opt/FENIKS-UC-SHOP
ExecStart=/opt/FENIKS-UC-SHOP/venv/bin/python -m planner_bot.bot
Restart=always
User=feniks

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now feniks-planner
```

---

## Buyruqlar

| Buyruq | Nima qiladi |
|---|---|
| `/start` | Botni ishga tushirish va yordam |
| `/add` | Yangi kundalik reja qo'shish |
| `/today` | Bugungi rejalar va ularning holati |
| `/tasks` | Barcha rejalar (to'xtatish / o'chirish tugmalari bilan) |
| `/stats` | Statistika |
| `/free` | Bo'sh vaqtlarim (bugun / ertaga / indinga) |
| `/calendar` | Google Calendar yozuvlari |
| `/settings` | Vaqt mintaqasi, faol kun oralig'i, eslatmalar |
| `/cancel` | Joriy amalni bekor qilish |

---

## Fayllar tuzilishi

```
planner_bot/
├── bot.py           # Telegram handler'lari va ishga tushirish
├── setup.py         # .env ni interaktiv to'ldirish
├── scheduler.py     # Eslatma va "bajardingizmi?" savoli sikli
├── db.py            # SQLite: users / tasks / task_logs
├── stats.py         # Statistika hisob-kitobi va matni
├── freetime.py      # Bo'sh vaqt oraliqlarini hisoblash
├── google_calendar.py  # Google Calendar'ga yozish va o'qish (asosiy backend)
├── notion.py        # eski backend, standart emas (kerak bo'lsa qolgan)
├── nlp.py           # Erkin matnni Claude orqali tushunish
├── stt.py           # Ovozni matnga o'girish
├── timeutil.py      # Vaqt/sana yordamchilari
├── keyboards.py     # Tugmalar
├── states.py        # FSM holatlari
├── config.py        # .env dan sozlamalar
├── requirements.txt      # asosiy kutubxonalar
├── requirements-ai.txt   # ixtiyoriy: erkin matnni tushunish
├── .env.example
├── health.py        # tekin hosting tariflari uchun HTTP sahifa
├── DEPLOY.md        # kalitlar va hosting qo'llanmasi
└── planner.db       # birinchi ishga tushganda avtomatik yaraladi

scripts/
├── termux-install.sh   # Android'ga o'rnatish
├── termux-start.sh     # Android'da ishga tushirish
├── termux-stop.sh      # Android'da to'xtatish
├── termux-boot.sh      # telefon yonganda avtomatik ishga tushirish
├── server-install.sh   # Linux serverga (Oracle/VPS) o'rnatish
└── server-update.sh    # serverdagi botni yangilash
```

### Ma'lumotlar bazasi

`task_logs` jadvali — statistikaning yagona manbasi. Har bir **reja × kun**
juftligi uchun bitta yozuv bo'ladi (`UNIQUE(task_id, log_date)`), shuning uchun
bot qayta ishga tushsa ham eslatma ikki marta yuborilmaydi.

| Holat | Ma'nosi |
|---|---|
| `pending` | Savol berilgan, javob kutilmoqda |
| `done` | Foydalanuvchi ✅ Ha dedi |
| `missed` | ❌ Yo'q dedi yoki `AUTO_MISS_HOURS` davomida javob bermadi |

---

## Keyingi qadamlar uchun g'oyalar

- Haftalik hisobotni har dushanba avtomatik yuborish
- Reja bajarilmagan kunlar uchun sabab so'rash va uni statistikaga qo'shish
- KUNDALIK'ning `kundalik.csv` / `rejalar.csv` statistikasini botning o'z
  SQLite bazasi bilan birlashtirish (hozircha ikkisi alohida)
- Bir nechta til (o'zbek / rus / ingliz)
