# FENIKS UC SERVICE — Telegram bot

PUBG Mobile uchun UC sotib olish botining boshlang'ich (MVP) versiyasi.

## Bot nima qiladi

- Mijoz UC paketini tanlaydi (60 / 325 / 660 / 1800 / 3850 / 8100 UC — narxlarni o'zingiz sozlaysiz)
- PUBG Mobile ID raqamini yuboradi
- Ko'rsatilgan karta raqamiga to'lov qilib, **to'lov chekining rasmini** botga yuboradi
- Buyurtma avtomatik ravishda admin(lar)ga chek rasmi bilan birga yuboriladi
- Admin ✅ **Tasdiqlash** yoki ❌ **Rad etish** tugmasini bosadi — mijozga avtomatik xabar boradi
- Mijoz istalgan vaqt "📦 Buyurtmalarim" bo'limidan barcha buyurtmalari holatini ko'rishi mumkin
- "❓ FAQ" bo'limida tez-tez so'raladigan savollarga javoblar bor

## 1. Bot tokenini olish

1. Telegramda [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` buyrug'ini yuboring va ko'rsatmalarga amal qiling
3. Sizga beriladigan tokenni saqlab qo'ying (masalan: `123456789:AAExample...`)

## 2. O'z Telegram ID raqamingizni bilish (admin sifatida)

1. [@userinfobot](https://t.me/userinfobot) ga `/start` yuboring
2. U sizga ID raqamingizni qaytaradi — shu raqam `ADMIN_IDS` ga kerak bo'ladi

## 3. O'rnatish

```bash
cd ucservice_bot
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Sozlash

`.env.example` faylidan nusxa oling va o'z ma'lumotlaringizni kiriting:

```bash
cp .env.example .env
```

`.env` faylini oching va quyidagilarni to'ldiring:

- `BOT_TOKEN` — @BotFather bergan token
- `ADMIN_IDS` — buyurtmalar boradigan admin(lar)ning Telegram ID raqami(lari), vergul bilan
- `CARD_NUMBER`, `CARD_HOLDER` — mijozlarga ko'rsatiladigan to'lov karta ma'lumotlari
- `CONTACT_USERNAME` — aloqa uchun ko'rsatiladigan Telegram username

**UC paketlari va narxlarni** o'zgartirish uchun `config.py` faylidagi `UC_PACKAGES`
ro'yxatini tahrirlang — u yerdagi raqamlar hozircha namuna sifatida qo'yilgan.

## 5. Ishga tushirish

```bash
python3 bot.py
```

Bot ishga tushgach, Telegramda botingizga `/start` yuboring.

## Fayllar tuzilishi

```
ucservice_bot/
├── bot.py            # Asosiy bot logikasi (handler'lar)
├── config.py          # Sozlamalar, narxlar, matnlar
├── database.py         # SQLite orqali buyurtmalarni saqlash
├── keyboards.py         # Tugmalar (reply/inline)
├── states.py           # FSM holatlari (buyurtma bosqichlari)
├── requirements.txt      # Python kutubxonalari
├── .env.example         # Sozlamalar namunasi
└── orders.db           # Buyurtmalar bazasi (birinchi ishga tushganda avtomatik yaraladi)
```

## Bot doim ishlab turishi uchun (production)

Uzoq muddat ishlashi uchun serverda (VPS) `systemd`, `pm2` yoki `screen`/`tmux`
yordamida fonda ishga tushiring, masalan:

```bash
nohup python3 bot.py > bot.log 2>&1 &
```

## Keyingi qadamlar uchun taklif qilinadigan qo'shimchalar

- To'lovni avtomatik tekshirish (bank API integratsiyasi)
- Admin uchun statistika va hisobot bo'limi (`/stats`)
- Bir nechta til qo'llab-quvvatlash (o'zbek/rus/ingliz)
- UC yetkazib berishni avtomatlashtirish (agar ta'minotchi API mavjud bo'lsa)

---

## OGA — buxgalteriya yordamchisi

Shu repoda buxgalteriya ishlari bo'yicha yordamchi (OGA) ham sozlangan: bank
vipiskalarini schyotlarga taqsimlash, schet-faktura (EHF) ni xatosiz yuborish,
soliq stavkalari va muddatlari, 1C hamda Venkon bazalari bo'yicha savollar.
Batafsil: [OGA.md](OGA.md)
