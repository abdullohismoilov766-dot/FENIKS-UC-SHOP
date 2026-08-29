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

**Bulutda (Railway, Render, Koyeb) — Variant D/E:** hech qanday fayl kerak
emas. Kalitlarni hosting saytining **Variables** bo'limiga yozasiz, tamom.
Kompyuter ham, terminal ham shart emas.

**Android, Oracle, kompyuter yoki VPS — Variant A/B/C:** shuni ishga tushiring:

```bash
python -m planner_bot.setup
```

Skript har birini navbat bilan so'raydi, to'g'ri-noto'g'riligini tekshiradi va
`planner_bot/.env` fayliga yozadi. Ixtiyoriylarini Enter bosib o'tkazib
yuborsangiz — o'sha imkoniyat o'chiq qoladi, qolgani ishlayveradi.

---

## 2. Bot qayerda ishlaydi

Bot doim ishlab turishi kerak — eslatma yuborish uchun. Telefondagi Python
ilovasi bu ish uchun yaramaydi (iOS ilovani orqa fonda ishlatmaydi).

### Qaysi variantni tanlash

| Variant | Narxi | Karta kerakmi | Ishonchliligi | Kimga |
|---|---|---|---|---|
| **A. Eski Android telefon** | butunlay tekin | ❌ yo'q | yaxshi | Uyda ishlatilmayotgan Android bo'lsa |
| **B. Oracle Cloud Always Free** | doimiy tekin | ✅ tekshiruv uchun (pul yechilmaydi) | eng yaxshi | Kartasi bor, jiddiy yechim istaganlarga |
| **C. O'z kompyuteringiz** | tekin | ❌ yo'q | kompyuter yoqiqligicha | Sinash va vaqtincha ishlatishga |
| **D. Tekin "web service"** | tekin | ba'zan yo'q | ⚠️ past | Boshqa iloji bo'lmaganda |
| **E. Railway / VPS** | oylik to'lov | ✅ ha | eng yaxshi | Sozlash bilan ovora bo'lmoqchi bo'lmaganlarga |

> ⚠️ **Tekin tariflar tez-tez o'zgaradi.** Quyidagi shartlar ushbu qo'llanma
> yozilgan paytdagi holat — ro'yxatdan o'tishdan oldin joriy shartlarni
> xizmatning o'z saytidan tekshiring.

---

### 🥇 Variant A — eski Android telefon (karta kerak emas)

Eng oson chin tekin yo'l. Ishlatilmayotgan Android telefon **server** bo'la
oladi: zaryadga ulab, javonga qo'yasiz — bot yillab ishlayveradi. Wi-Fi
yetarli, ochiq IP kerak emas (bot o'zi Telegram'ga ulanadi).

1. Android'ga **Termux** ni [F-Droid](https://f-droid.org/packages/com.termux/)
   dan o'rnating (Play Market'dagi versiyasi eskirgan)
2. Termux'da ketma-ket:

```bash
pkg update -y && pkg install -y python git
git clone https://github.com/abdullohismoilov766-dot/FENIKS-UC-SHOP.git
cd FENIKS-UC-SHOP
git checkout claude/daily-plan-tracker-bot-069e57
pip install -r planner_bot/requirements.txt
python -m planner_bot.setup     # token va sozlamalarni kiritasiz
```

3. Telefon uxlab qolmasligi uchun:

```bash
termux-wake-lock
```

   Shuningdek Android sozlamalarida: **Battery → Termux → Unrestricted**
   (batareya cheklovini o'chirish)

4. Botni doimiy ishga tushirish:

```bash
nohup python -m planner_bot.bot > bot.log 2>&1 &
```

Termux'ni yopsangiz ham bot ishlayveradi. Loglarni ko'rish: `tail -f bot.log`.
Telefonni qayta yoqsangiz, 3–4-qadamni takrorlaysiz.

**Ustunligi:** karta kerak emas, hech kim tarifni o'zgartirmaydi, baza
telefonning o'zida — statistika hech qachon yo'qolmaydi.

---

### 🥈 Variant B — Oracle Cloud Always Free (chin doimiy tekin server)

Oracle "Always Free" tarifi — sinov muddati emas, **doimiy tekin** server.
Ro'yxatdan o'tishda karta so'raydi, lekin bu faqat shaxsni tekshirish uchun;
Always Free resurslardan pul yechilmaydi.

1. [oracle.com/cloud/free](https://www.oracle.com/cloud/free/) → ro'yxatdan o'ting
2. **Compute → Instances → Create Instance**
3. Image: **Ubuntu**, Shape: **Always Free** belgisi turgan variantni tanlang
4. SSH kalitini yarating va yuklab oling (telefonda **Termius** ilovasi orqali
   ham bo'ladi — App Store'da tekin)
5. Serverga ulanib, Variant C dagi buyruqlarni bajaring

**Ustunligi:** doimiy tekin, to'liq server, hech narsa uxlamaydi, baza
saqlanadi. **Kamchiligi:** ro'yxatdan o'tish biroz ovora, ba'zi hududlarda
joy bo'lmasligi mumkin.

---

### 🥉 Variant C — o'z kompyuteringiz yoki VPS

```bash
git clone https://github.com/abdullohismoilov766-dot/FENIKS-UC-SHOP.git
cd FENIKS-UC-SHOP
python3 -m venv venv
./venv/bin/pip install -r planner_bot/requirements.txt
./venv/bin/python -m planner_bot.setup
./venv/bin/python -m planner_bot.bot
```

Kompyuterda — terminalni yopsangiz bot to'xtaydi, ya'ni faqat sinash uchun.
Serverda esa systemd bilan doimiy ishga tushiring:

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
journalctl -u feniks-planner -f           # jonli loglar
```

---

### ⚠️ Variant D — tekin "web service" tariflari (Render, Koyeb)

Bu tariflar odatda faqat **web service** ni tekin beradi. Bot polling bilan
ishlagani uchun port ochmaydi — shuning uchun unga kichik health sahifasi
qo'shilgan: hosting `PORT` o'zgaruvchisini qo'yishi bilan u avtomatik yonadi.

1. Hosting'da yangi **Web Service** yarating, GitHub repozitoriyni ulang
2. Branch: `claude/daily-plan-tracker-bot-069e57`
3. Start command: `python -m planner_bot.bot`
4. **Variables** ga kalitlarni yozing (`PORT` ni **qo'lda qo'ymang** —
   hosting o'zi qo'yadi)
5. Uxlab qolmasligi uchun [uptimerobot.com](https://uptimerobot.com) yoki
   [cron-job.org](https://cron-job.org) da tekin hisob oching va servisingiz
   manzilini har 5 daqiqada tekshirib turishga qo'ying

> 🔴 **Jiddiy kamchilik:** tekin tariflarda disk vaqtinchalik. Servis qayta
> ishga tushganda (bu tez-tez bo'ladi) **`planner.db` o'chib ketadi — butun
> statistikangiz bilan birga.** Rejalaringizni qaytadan kiritishga to'g'ri
> keladi. Shuning uchun bu variantni faqat sinash uchun tavsiya qilaman;
> uzoq muddatga A yoki B ni tanlang.

---

### Variant E — Railway / pullik VPS

Eng kam ovora, lekin oylik to'lovli. Railway'da: **New Project → Deploy from
GitHub repo** → branch tanlang → **Variables** ga kalitlarni yozing →
**Settings → Volumes** da `/data` volume qo'shing va `PLANNER_DB_PATH` ni
`/data/planner.db` qiling.

Kalitlar jadvali:

| Nomi | Qiymati |
|---|---|
| `PLANNER_BOT_TOKEN` | BotFather bergan token |
| `TIMEZONE` | `Asia/Tashkent` |
| `DAY_START` | `09:00` |
| `DAY_END` | `22:00` |
| `PLANNER_DB_PATH` | `/data/planner.db` |

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
| iPhone'dagi Python ilovasida ishlamadi | iOS ilovani orqa fonda ishlatmaydi — bot 24/7 turolmaydi. Variant A–E dan birini tanlang |
| Termux'da bot tunda to'xtab qoladi | `termux-wake-lock` bajarilmagan yoki Android batareya cheklovi yoqiq → Sozlamalar → Battery → Termux → **Unrestricted** |
| Tekin hostingda servis uxlab qoladi | UptimeRobot / cron-job.org bilan har 5 daqiqada `/health` manzilini tekshirib turing |
| `Unauthorized` xatosi | Token noto'g'ri yoki BotFather'da bekor qilingan → `/revoke` bilan yangisini oling |
| Eslatmalar noto'g'ri vaqtda keladi | Vaqt mintaqasi xato → botda `/settings` → 🌍 Vaqt mintaqasi |
| Notion: `Could not find database` | Bazani integratsiyaga ulamagansiz → baza → `•••` → **Connections** |
| Notion: `property does not exist` | Ustun nomlari boshqacha → `NOTION_TITLE_PROP` / `NOTION_DATE_PROP` ni moslang |
| Qayta ishga tushgach statistika yo'q | Disk vaqtinchalik → pullik tarifda volume ulang, tekin tarifda esa Variant A yoki B ga o'ting (u yerda baza yo'qolmaydi) |
| Ovozli xabar ishlamayapti | `STT_API_KEY` qo'yilmagan yoki balans tugagan |

**Agar token boshqa birovga ko'rinib qolsa:** darhol @BotFather → `/revoke` →
botingizni tanlang. Eski token o'sha zahoti ishlamay qoladi, yangisini
`python -m planner_bot.setup` orqali qayta kiritasiz.
