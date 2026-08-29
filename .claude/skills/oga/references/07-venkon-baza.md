# Venkon bazasi

## 1. Venkon nima — tasdiqlangan ma'lumot

> **Asosiy xulosa: Venkon bazasi — bu 1C bazasi.**
> Venkon alohida dastur emas, u **"1C:Korxona 8" (1С:Предприятие 8) platformasida**
> ishlab chiqilgan konfiguratsiya. Demak `references/06-1c-bazalar.md` dagi
> **hamma narsa Venkon ga ham tegishli**: hujjatlar, ma'lumotnomalar, oy yopilishi,
> arxiv, kirish qoldiqlari, muammolar ro'yxati.

| Nima | Ma'lumot |
|------|----------|
| Ishlab chiquvchi | **VENKON GROUP** — Toshkent, O'zbekiston; 1C hamkori |
| Platforma | 1C:Korxona 8 (1С:Предприятие 8) |
| Asosiy mahsulot | **«VENKON: Buxgalteriya. Xo'jalik hisobi»** (`VENKON:Бухгалтерия. Хозрасчет`) |
| Ikkinchi nomlanishi | **«1С:Бухгалтерия 8 для Узбекистана», ред. 3.0** — VENKON GROUP mahsuloti, "Совместимо! Система программ 1С:Предприятие" sertifikatiga ega |
| Yana bir mahsulot | **«1С:Розница для Узбекистана»** (Chakana savdo) — VENKON GROUP, sertifikatlangan |
| Nima uchun | Buxgalteriya va soliq hisobini avtomatlashtirish, O'zbekiston qonunchiligiga muvofiq majburiy (reglament) hisobotlarni tayyorlash |
| Qamrovi | Bir nechta tashkilot, turli soliq rejimlari, ombor, savdo operatsiyalari, xodimlar va ish haqi |
| Yetkazib berish | **Bulutli** (onlayn obuna) yoki **"quti"** (lokal o'rnatiladigan) versiya |
| **Bulutli kirish** | **clobus.uz** — VENKON GROUP ning bulutli xizmati (1С:Фреш texnologiyasi). Bazaga dastur o'rnatmasdan, brauzer orqali kiriladi |
| Qo'llab-quvvatlash | VENKON GROUP, Toshkent — `its@venkon.uz`, tel. +998 78 140-00-77 / 148-77-00 / 140-77-00 |

**Manbalar:**
- [1c.uz — VENKON GROUP mahsuloti sertifikati](https://1c.uz/news/detail/1207509/)
- [1c.uz — «1С:Розница для Узбекистана» sertifikati](https://1c.uz/news/detail/1210543/)
- [solutions.1c.ru — VENKON:Бухгалтерия. Хозрасчет joriy etish loyihalari](https://solutions.1c.ru/projects/1048458/)
- [venkonbuhgalteriya.uz](https://venkonbuhgalteriya.uz/) · [venkon.uz](https://venkon.uz/ru/offer)

⚠️ Mahsulot tahrirlari (redaktsiya) va imkoniyatlari yangilanib turadi. Aniq versiya va
funksiyalarni VENKON GROUP qo'llab-quvvatlash xizmatidan yoki bazaning
`Справка → О программе` bo'limidan tasdiqlang.

---

## 1a. Clobus.uz — bulutli kirish

> ✅ **Tasdiqlangan (2026-08-29):** korxonada Venkon bazasiga **clobus.uz** sayti orqali
> ham kirish mumkin.

| Nima | Ma'lumot |
|------|----------|
| Nomi | **Clobus.uz** — VENKON GROUP ishga tushirgan bulutli xizmat (2019 yildan) |
| Texnologiya | **1С:Фреш** ("1С:Предприятие 8 через Интернет") — bulutda ishlaydigan 1C |
| Kirish | Brauzer orqali, dastur o'rnatmasdan. Kompyuter yoki smartfon + internet (TAS-IX ham yetarli) |
| Muqobil manzil | `clobus.venkon.uz` |
| Mavjud yechimlar | **1С:Бухгалтерия 3.0**, **1С:Розница 3.0**, **1С:Управление компанией 3.0** — O'zbekiston uchun |
| To'lov | Oylik obuna |
| Yangilanishlar | **Avtomatik** — qonunchilik o'zgarganda konfiguratsiyani qo'lda yangilash shart emas |
| Ma'lumot xavfsizligi | Ma'lumotlar markazida (data-center) saqlanadi, uzatishda shifrlanadi |

**Manbalar:** [clobus.uz](https://clobus.uz/) · [gazeta.uz — Venkon clobus.uz ni ishga tushirdi](https://www.gazeta.uz/ru/2019/07/05/clobus/) · [venkon.uz — Clobus](https://venkon.uz/ru/products/clobus) · [kun.uz](https://kun.uz/68741864)

### Bulutli ish lokal versiyadan nimasi bilan farq qiladi

| Mavzu | Lokal ("quti") | Bulutli (clobus.uz) |
|-------|----------------|---------------------|
| Kirish | Kompyuterga o'rnatilgan dastur | Brauzer, istalgan joydan |
| Yangilanish | Qo'lda yoki mutaxassis orqali | **Avtomatik** |
| **Arxiv** | `Выгрузить информационную базу` → `.dt` | Provayder zaxira nusxa oladi, lekin **o'zingiz ham davriy ravishda ma'lumotni yuklab oling** ⚠️ |
| **ERI bilan imzolash** | Kalit shu kompyuterda | ⚠️ Bulutda ishlash uchun ish stantsiyasiga **qo'shimcha komponent/kengaytma** o'rnatish talab qilinadi — tartibni VENKON GROUP dan tasdiqlang |
| Foydalanuvchilar | Lokal ro'yxat | Obuna bo'yicha, har xodimga alohida login |
| Internet uzilsa | Ishlash davom etadi | **Ish to'xtaydi** — muddat kunlarida (15 va 20-sanalar) zaxira internet kanalini o'ylab qo'ying |
| Litsenziya | Bir martalik sotib olinadi | Oylik obuna — **to'lanmasa bazaga kirish yopiladi** ⚠️ |

### Bulutda ishlashda 6 ta amaliy qoida

1. **Obuna muddatini kuzating.** To'lov kechiksa hisobot muddati arafasida bazaga kira
   olmay qolish xavfi bor.
2. **O'z zaxirangizni oling.** Provayder nusxasi bor, lekin muhim davr yopilgach
   ma'lumotni o'zingizga ham yuklab qo'ying.
3. **Har xodimga alohida login.** Umumiy parol ishlatilmasin — kim nima o'zgartirganini
   jurnaldan (`Журнал регистрации`) topib bo'lmay qoladi.
4. **Avtomatik yangilanishdan keyin tekshiring.** Yangilanish qonunchilik o'zgarishini
   olib keladi; yangilanish kunidan keyin hisobot shakllari va soliq stavkalari
   to'g'ri kelayotganini bir marta tekshiring.
5. **ERI kaliti va komponenti ishlayotganini muddatdan oldin sinab ko'ring** — EHF ni
   20-sana kuni birinchi marta yuborishga urinmang.
6. **Yopilgan davrga taqiq** (`Дата запрета изменения`) bulutda ham qo'yiladi — bir necha
   xodim kirgani uchun bu yanada muhimroq.

---

## 2. Venkon = 1C bo'lgani uchun nima anglatadi

| Savol | Javob |
|-------|-------|
| Hujjatlar nomi qanday? | 1C dagi kabi: `Поступление товаров и услуг`, `Реализация`, `Списание с расчетного счета` va h.k. — `06-1c-bazalar.md` ga qarang |
| Schyotlar rejasi? | NSBU bo'yicha, `Хозрасчетный` reja — `01-schetlar-rejasi.md` amal qiladi |
| Arxiv qanday olinadi? | `Администрирование → Выгрузить информационную базу` → `.dt` fayl (bulutli versiyada provayder orqali) |
| Oy qanday yopiladi? | `Закрытие месяца` yordamchisi — 12 qadamli tartib `06-1c-bazalar.md` da |
| Bank vipiskasi yuklanadimi? | Ha, `Банк и касса → Банковские выписки → Загрузить` (kliyent-bank fayli) |
| Provodka qoidalari boshqacha-mi? | **Yo'q.** Provodkalar bir xil — `02-bank-vipiska.md` va `03-tipovoy-provodkalar.md` to'liq amal qiladi |

**Amaliy xulosa OGA uchun:** "Venkon da qanday qilaman?" degan savolga 1C mantig'i
bo'yicha javob berilaveradi. Faqat menyu nomlari tahririga qarab biroz farq qilishi
mumkin — shuni ogohlantirib qo'yiladi.

---

## 3. EHF (schet-faktura) ni Venkon dan yuborish

Venkon 1C:Buxgalteriya **Didox bilan integratsiyalangan** — hujjatni bazada
rasmiylashtirib, **ERI bilan imzolab, to'g'ridan-to'g'ri 1C dan yuborish** mumkin.
Didox saytini yoki my.soliq.uz ni alohida ochish shart emas.

### Sozlash uchun kerak bo'ladigan narsalar
| # | Nima | Izoh |
|---|------|------|
| 1 | **ERI (ЭЦП) kaliti** | e-imzo.uz dan olingan, amal qilish muddati tugamagan |
| 2 | **EDO uchun Java komponenti** | ⚠️ **O'rnatilmasa hujjat imzolanmaydi va yuborilmaydi** — Didox/Soliq orqali yuborishdagi eng ko'p uchraydigan nosozlik shu |
| 3 | Didox hisobi (login) | Operator bilan shartnoma |
| 4 | Bazada EDO sozlamalari | Tashkilot, sertifikat, operator tanlanadi |

### Yuborish tartibi
```
1. Bazada hujjat yaratiladi (Реализация / Счет-фактура выданный)
2. MXIK (ИКПУ) kodi va o'lchov birligi tekshiriladi (nomenklatura kartochkasidan keladi)
3. 04-schet-faktura.md dagi 14 punktli tekshiruv yurgiziladi
4. Hujjat ERI bilan imzolanadi
5. Didox orqali yuboriladi
6. Xaridorning javobi (aksept / rad etish) bazada kuzatiladi
```

### EDO da tez-tez uchraydigan nosozliklar
| Belgi | Sabab | Yechim |
|-------|-------|--------|
| "Imzolash" tugmasi ishlamayapti / xato beradi | Java komponenti o'rnatilmagan yoki eskirgan | EDO komponentini qayta o'rnating |
| Sertifikat ko'rinmayapti | ERI muddati tugagan yoki brauzer/tizimda ro'yxatdan o'tmagan | e-imzo kalitini yangilang |
| Hujjat "yuborilmoqda" holatida qotib qolgan | Operator bilan aloqa yo'q / internet | Qayta yuboring, holatini Didox kabinetidan tekshiring |
| Xaridor topilmayapti | STIR noto'g'ri yoki kontragent kartochkasida to'ldirilmagan | Kontragent STIRini tekshiring |
| MXIK kodi rad etildi | Kod tovarga mos emas yoki eskirgan | MXIK katalogidan yangilang, kartochkaga qayta biriktiring |

⚠️ Bulutli (onlayn) versiyada ERI va Java komponenti bilan ishlash tartibi lokal
versiyadan farq qiladi — VENKON GROUP ko'rsatmasiga qarang.

---

## 4. Nazorat: Venkon ↔ my.soliq.uz sverkasi

Har oyda:

| # | Nima solishtiriladi | Qayerdan |
|---|--------------------|----------|
| 1 | Yuborilgan EHF lar soni va summasi | Baza ↔ my.soliq.uz EHF reestri |
| 2 | Qabul qilingan (kirim) EHF lar | Baza ↔ reestr — **qabul qilinmagani QQS chegirmasini yo'qotadi** |
| 3 | Sotuv aylanmasi (9010/9020/9030) | Baza ↔ QQS deklaratsiyasi |
| 4 | Soliq qoldig'i (6410 subschyotlari) | Baza ↔ my.soliq.uz shaxsiy kabinet qoldig'i |
| 5 | 5110 qoldig'i | Baza ↔ bank vipiskasi |

Bittasi mos kelmasa — oy yopilmaydi.

---

## 5. Hali aniqlanishi kerak (korxonaga xos)

OGA quyidagilarni foydalanuvchidan so'raydi va javoblarni `memory/XOTIRA.md` ga yozadi:

- [ ] Qaysi mahsulot ishlatiladi: `VENKON:Buxgalteriya. Xo'jalik hisobi` / `1С:Бухгалтерия 8 для Узбекистана ред. 3.0` / `1С:Розница` / bir nechtasi?
- [ ] Tahriri (redaktsiya) va platforma versiyasi (`Справка → О программе`):
- [x] Bulutli (onlayn) yoki lokal ("quti") versiya: **bulutli — clobus.uz orqali kiriladi** (2026-08-29 tasdiqlandi)
- [ ] Nechta tashkilot yuritiladi:
- [ ] Soliq rejimi bazada qanday sozlangan (QQS to'lovchi / aylanmadan soliq):
- [ ] EHF qayerdan yuboriladi: Venkon bazasidan / Didox saytidan / my.soliq.uz dan:
- [ ] EDO operatori: Didox / Faktura.uz / boshqa:
- [ ] Bank vipiskasi bazaga yuklanadimi yoki qo'lda kiritiladimi:
- [ ] **Eski baza** qaysi (1C 7.7 / eski Venkon tahriri / boshqa) va qachongacha ishlatilgan:
- [ ] Eski bazadan yangisiga o'tish sanasi va kirish qoldiqlari kiritilganmi:
- [ ] Eski bazaga hozir ham murojaat qilinadimi (arxiv sifatida):
- [ ] Yana boshqa baza bilan almashinuv bormi (savdo/POS/ombor dasturi):
- [ ] Arxiv kim tomonidan, qanchalik tez-tez olinadi:
- [ ] Qo'llab-quvvatlash: VENKON GROUP / ichki dasturchi / tashqi mutaxassis:

---

## 6. Eski va yangi baza parallel yuritilganda (universal qoidalar)

1. **Bitta haqiqat manbasi.** Har ma'lumot turi uchun asosiy baza belgilanadi. Eski baza
   o'tish sanasidan keyin **faqat o'qish uchun** qolsin — unga yangi hujjat kiritilmasin.
2. **Kirish qoldiqlari barcha subkonto kesimida.** Faqat summa emas: kontragent,
   shartnoma, nomenklatura, ombor, hisobdor shaxs kesimida. Aks holda birinchi
   akt-sverkada topib bo'lmaydigan farq chiqadi.
3. **O'tish sanasida ikkala bazadan balans chiqariladi va tiyingacha solishtiriladi.**
4. **Almashinuv jurnali** yuritiladi: sana, fayl, qatorlar soni, xatolar.
5. **Bekor qilish va tuzatishlar ham ko'chiriladi** — aks holda bazalar asta-sekin ajraladi.
6. **Arxiv ikkala bazadan**, bir xil sanada, boshqa diskda/bulutda saqlanadi.
