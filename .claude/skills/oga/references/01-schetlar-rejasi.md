# NSBU schyotlar rejasi (O'zbekiston)

> Asos: O'zbekiston Respublikasi Moliya vazirligining buxgalteriya hisobi schyotlar
> rejasi (BHMS/NSBU). Quyida amaliyotda eng ko'p ishlatiladigan schyotlar keltirilgan.
> `⚠️` belgisi — subschyot raqami korxonaning ish rejasida boshqacha bo'lishi mumkin,
> `memory/XOTIRA.md` dan tekshiring.

## Bo'limlar tuzilishi

| Bo'lim | Diapazon | Nima |
|--------|----------|------|
| 0 | 0100–0900 | Uzoq muddatli aktivlar |
| 1 | 1000–1900 | Tovar-moddiy zaxiralar (materiallar) |
| 2 | 2000–2900 | Ishlab chiqarish xarajatlari, tayyor mahsulot, tovarlar |
| 3 | 3000–3900 | Kelgusi davr xarajatlari, kechiktirilgan xarajatlar |
| 4 | 4000–4900 | Debitorlik qarzlari |
| 5 | 5000–5900 | Pul mablag'lari |
| 6 | 6000–6900 | Qisqa muddatli majburiyatlar |
| 7 | 7000–7900 | Uzoq muddatli majburiyatlar |
| 8 | 8000–8900 | Xususiy kapital |
| 9 | 9000–9900 | Moliyaviy natijalar (daromadlar va xarajatlar) |

**Eslatma:** 0–8 bo'limlar — balans schyotlari (qoldiq keyingi yilga o'tadi).
9-bo'lim — natija schyotlari, yil oxirida 9910 ga yopiladi va qoldiq qolmaydi.

---

## 0 — Uzoq muddatli aktivlar

| Schyot | Nomi |
|--------|------|
| 0100 | Asosiy vositalar (0110 binolar/inshootlar, 0120 ⚠️, 0130 mashina va uskunalar, 0140 mebel va ofis jihozlari, 0150 kompyuter texnikasi ⚠️, 0160 transport vositalari) |
| 0200 | Asosiy vositalar amortizatsiyasi (0100 ga mos subschyotlar bilan) — **passiv, kontr-aktiv** |
| 0300 | Nomoddiy aktivlar (dasturiy ta'minot, litsenziya, tovar belgisi) |
| 0400 | Nomoddiy aktivlar amortizatsiyasi — **kontr-aktiv** |
| 0500 | Uzoq muddatli investitsiyalar |
| 0800 | Kapital qo'yilmalar (0810 tugallanmagan qurilish, 0820 asosiy vositalarni sotib olish, 0830 NMA sotib olish, 0860 o'rnatiladigan uskunalar) ⚠️ |
| 0900 | Uzoq muddatli debitorlik qarzi / kechiktirilgan xarajatlar ⚠️ |

**Muhim:** sotib olingan asosiy vosita avval `0820` ga yig'iladi (qiymat + yetkazish +
o'rnatish), keyin foydalanishga topshirilganda `0100` ga o'tkaziladi.

## 1 — Materiallar

| Schyot | Nomi |
|--------|------|
| 1010 | Xom ashyo va materiallar |
| 1020 | Sotib olingan yarim tayyor mahsulot va butlovchi buyumlar |
| 1030 | Yoqilg'i (benzin, dizel, gaz) |
| 1040 | Ehtiyot qismlar |
| 1050 | Qurilish materiallari |
| 1060 | Idish va idish materiallari |
| 1090 | Boshqa materiallar (kanstovar, xo'jalik mollari) |
| 1500 | Inventar va xo'jalik jihozlari ⚠️ (1510 inventar, 1520 maxsus kiyim) |

## 2 — Ishlab chiqarish va tovarlar

| Schyot | Nomi |
|--------|------|
| 2010 | Asosiy ishlab chiqarish |
| 2310 | Yordamchi ishlab chiqarish ⚠️ |
| 2510 | Umumishlab chiqarish (sex) xarajatlari ⚠️ |
| 2810 | Tayyor mahsulot |
| 2910 | Omborlardagi tovarlar |
| 2920 | Chakana savdodagi tovarlar |
| 2960 | Savdo ustamasi (naценка) — **kontr-aktiv** ⚠️ |

## 3 — Kelgusi davr xarajatlari

| Schyot | Nomi |
|--------|------|
| 3100 | Kelgusi davr xarajatlari ⚠️ (oldindan to'langan ijara, sug'urta, obuna, domen/hosting) |
| 3200 | Kechiktirilgan xarajatlar ⚠️ |

**Qoida:** bir necha oyga oldindan to'langan xizmat darhol xarajat emas — `3100` ga
kiritiladi va oylar bo'yicha `9420`/`2510` ga taqsimlanadi.

## 4 — Debitorlik qarzlari (bizga qarzdorlar)

| Schyot | Nomi |
|--------|------|
| **4010** | Xaridorlar va buyurtmachilardan olinadigan schyotlar — **eng ko'p ishlatiladi** |
| 4020 | Olinadigan veksellar |
| 4110 | Byudjetga soliqlar bo'yicha bo'nak (ortiqcha) to'lovlar |
| 4200 | Mol-mulk sug'urtasi bo'yicha to'lovlar ⚠️ |
| 4310 | Ta'sischilarning ustav kapitaliga ulushi bo'yicha qarzi ⚠️ |
| **4410** | Hisobdor shaxslarga berilgan bo'nak (podotchyot) |
| **4510** | Mol yetkazib beruvchilar va pudratchilarga berilgan bo'nak (avans) |
| 4610 | Xodimlarning boshqa operatsiyalar bo'yicha qarzi ⚠️ |
| **4890** | Boshqa debitorlarning qarzi |
| 4900 | Shubhali qarzlar bo'yicha zaxira — **kontr-aktiv** ⚠️ |

## 5 — Pul mablag'lari

| Schyot | Nomi |
|--------|------|
| **5010** | Kassa — milliy valyutada |
| 5020 | Kassa — xorijiy valyutada |
| **5110** | Hisob-kitob (raschyot) schyoti — **bank vipiskasining asosiy schyoti** |
| **5210** | Valyuta schyoti (mamlakat ichida) |
| 5220 | Chet eldagi valyuta schyoti ⚠️ |
| 5510 | Akkreditivlar ⚠️ |
| 5520 | Chek daftarchalari ⚠️ |
| **5530** | Boshqa maxsus schyotlardagi pul mablag'lari — **korporativ plastik karta** shu yerda ⚠️ |
| 5610 | Yo'ldagi pul o'tkazmalari (inkassatsiya, kun oralig'idagi o'tkazma) ⚠️ |
| 5810 | Qisqa muddatli investitsiyalar (depozit, qimmatli qog'oz) ⚠️ |

## 6 — Qisqa muddatli majburiyatlar (biz qarzdormiz)

| Schyot | Nomi |
|--------|------|
| **6010** | Mol yetkazib beruvchilar va pudratchilarga to'lanadigan schyotlar |
| 6020 | To'lanadigan veksellar |
| **6310** | Xaridorlardan olingan bo'naklar (avans) |
| **6410** | Byudjetga to'lovlar bo'yicha qarz — **subschyotlar bilan yuritiladi** (QQS, foyda solig'i, aylanmadan soliq, JShDS, mol-mulk, yer, suv, aktsiz) |
| **6510** | Sug'urta va ijtimoiy ta'minot bo'yicha to'lovlar — **ijtimoiy soliq** |
| **6520** | Maqsadli davlat jamg'armalariga to'lovlar — **INPS (jamg'arib boriladigan pensiya)** ⚠️ |
| 6610 | Ta'sischilarga to'lanadigan dividendlar ⚠️ |
| **6710** | Mehnatga haq to'lash bo'yicha xodimlar bilan hisob-kitob (ish haqi) |
| 6720 | Deponentlangan ish haqi ⚠️ |
| **6810** | Qisqa muddatli bank kreditlari |
| 6820 | Qisqa muddatli qarzlar (zayom) |
| 6830 | Uzoq muddatli majburiyatlarning joriy qismi ⚠️ |
| **6990** | Boshqa kreditorlik qarzlari — **aniqlanmagan tushum vaqtincha shu yerga** |

**6410 subschyotlari** — korxona o'zi ochadi. Tavsiya etilgan tuzilma:
`6410/1 QQS`, `6410/2 Foyda solig'i`, `6410/3 Aylanmadan soliq`, `6410/4 JShDS`,
`6410/5 Mol-mulk solig'i`, `6410/6 Yer solig'i`, `6410/9 Jarima va penya`.
Korxonangizdagi haqiqiy raqamlarni `memory/XOTIRA.md` ga yozing.

## 7 — Uzoq muddatli majburiyatlar

| Schyot | Nomi |
|--------|------|
| 7810 | Uzoq muddatli bank kreditlari |
| 7820 | Uzoq muddatli qarzlar ⚠️ |
| 7900 | Kechiktirilgan soliq majburiyatlari ⚠️ |

## 8 — Xususiy kapital

| Schyot | Nomi |
|--------|------|
| 8310 | Ustav kapitali |
| 8400 | Qo'shilgan kapital ⚠️ |
| 8500 | Rezerv kapital ⚠️ |
| **8710** | Hisobot davrining taqsimlanmagan foydasi (qoplanmagan zarari) |

## 9 — Daromadlar va xarajatlar

### Daromadlar (Kt bo'yicha yig'iladi)

| Schyot | Nomi |
|--------|------|
| **9010** | Tayyor mahsulot sotishdan daromad |
| **9020** | Tovarlar sotishdan daromad |
| **9030** | Ishlar bajarish va xizmatlar ko'rsatishdan daromad |
| 9040 | Sotishdan chegirmalar, qaytarilgan tovarlar — **kontr-daromad (Dt)** ⚠️ |
| 9210 | Asosiy vositalarning chiqib ketishi |
| 9220 | Boshqa aktivlarning chiqib ketishi ⚠️ |
| 9390 | Boshqa operatsion daromadlar (jarima, undirilgan zarar, hisobdan chiqarilgan qarz) |
| 9510 | Foizlar ko'rinishidagi daromadlar (depozit foizi) |
| 9520 | Dividendlar ko'rinishidagi daromadlar ⚠️ |
| 9530 | Uzoq muddatli ijara (lizing)dan daromadlar ⚠️ |
| **9540** | Valyuta kursi farqidan daromad |

### Xarajatlar (Dt bo'yicha yig'iladi)

| Schyot | Nomi |
|--------|------|
| **9110** | Sotilgan tayyor mahsulot tannarxi |
| **9120** | Sotilgan tovarlar tannarxi |
| **9130** | Bajarilgan ishlar va ko'rsatilgan xizmatlar tannarxi |
| **9410** | Sotish xarajatlari (reklama, yetkazib berish, savdo xodimlari ish haqi) |
| **9420** | Ma'muriy xarajatlar (boshqaruv ish haqi, ofis ijarasi, aloqa, audit) |
| **9430** | Boshqa operatsion xarajatlar (bank komissiyasi, jarima, penya, xayriya) |
| **9610** | Foizlar ko'rinishidagi xarajatlar (kredit foizi) |
| **9690** | Valyuta kursi farqi bo'yicha zarar |
| 9710 | Favqulodda foyda va zararlar ⚠️ |
| **9810** | Foyda solig'i bo'yicha xarajat |
| **9820** | Foydadan boshqa soliqlar va yig'imlar |
| **9910** | Yakuniy moliyaviy natija — yil oxirida barcha 9-bo'lim schyotlari shu yerga yopiladi |

---

## Eslab qolish uchun mnemonika

- **4 — bizga qarz** (debitor), **6 — biz qarzdor** (kreditor). 4 va 6 juftlik:
  `4010 ↔ 6310` (xaridor), `6010 ↔ 4510` (ta'minotchi).
- **5 — pul**, hech qachon o'zi bilan o'zi yopilmaydi (5110 ↔ 5010 dan tashqari).
- **9 boshi 0 yoki 3 — daromad** (9010, 9020, 9030, 9390, 9510, 9540),
  **9 boshi 1 yoki 4 yoki 6 — xarajat** (9110, 9410, 9420, 9430, 9610, 9690).
- **Xarajat schyoti tanlash mantiqi:** mahsulotga bevosita bog'liqmi → 2010/9110;
  sotishga bog'liqmi → 9410; ofis/boshqaruvmi → 9420; boshqasi → 9430.
