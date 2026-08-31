# NSBU № 21 — schyotlar rejasi (O'zbekiston)

> ## 🔴 ENG MUHIM: 2025-yildan YANGI schyotlar rejasi amal qiladi
>
> | | Hujjat |
> |---|---|
> | **Eski** reja | NSBU № 21, MA 23.10.2002 y. **1181-son** — «Xo'jalik yurituvchi subyektlarning moliya-xo'jalik faoliyati buxgalteriya hisobi schyotlar rejasi». **2025-yil 1-yanvardan kuchini yo'qotgan** |
> | **Yangi** reja | NSBU № 21 — «Xo'jalik yurituvchi subyektlar buxgalteriya hisobi schyotlar rejasi va uni qo'llash bo'yicha yo'riqnoma». Iqtisodiyot va moliya vaziri **14.11.2024 y. 191-son** buyrug'i bilan tasdiqlangan, AV da **27.12.2024 y. 3593-son** bilan ro'yxatdan o'tgan. **2025-yil 1-yanvardan** amal qiladi |
> | Qo'shimcha | NSBU № 6 (ijara hisobi) o'zgarishlari **24.09.2025** dan kuchga kirgan va NSBU № 21 ga ham tegishli o'zgartishlar kiritilgan |
>
> **Buning amaliy ma'nosi:**
> 1. Eski bazadagi (2025 gacha) provodkalar **eski reja** bo'yicha, yangi davr **yangi reja** bo'yicha yuritiladi — bu "eski va yangi baza" farqining asosiy sababi bo'lishi mumkin.
> 2. Quyidagi jadvallar amaliyotda keng ishlatiladigan schyotlarni beradi, lekin **har bir raqamni yangi NSBU № 21 matni bilan solishtiring**:
>    [lex.uz/ru/docs/7282759](https://lex.uz/ru/docs/7282759) · [buxgalter.uz/plan_schetov](https://buxgalter.uz/plan_schetov)
> 3. OGA schyot raqamini aytganda, korxonaning `memory/XOTIRA.md` dagi ish rejasini ustun qo'yadi.

**Belgilar:** `✅` — manbadan tasdiqlangan · `⚠️` — amaliyotda shunday, lekin yangi reja matnidan tekshiring.

---

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

0–8 bo'limlar — balans schyotlari (qoldiq keyingi yilga o'tadi).
9-bo'lim — natija schyotlari, yil oxirida `9910` ga yopiladi va qoldiq qolmaydi.

---

## 0 — Uzoq muddatli aktivlar

> ✅ Quyidagi subschyotlar korxona buxgalterining ish daftaridan tasdiqlangan
> (`memory/DAFTAR.md → 1.2–1.5`).

### `0100` — Asosiy vositalar

| Schyot | Nomi |
|--------|------|
| **0110** | Yer |
| **0111** | Yerni obodonlashtirish |
| **0112** | Uzoq muddatli ijara shartnomasi bo'yicha olingan AVni obodonlashtirish |
| **0120** | Binolar, inshootlar va uzatuvchi moslamalar |
| **0130** | Mashina va uskunalar |
| **0140** | Mebel va ofis jihozlari (inventar va xo'jalik jihozlari) |
| **0150** | Kompyuter jihozlari va hisoblash texnikasi |
| **0160** | Transport vositalari |
| **0170** | Ishchi hayvonlar |
| **0180** | Ko'p yillik o'simliklar |
| **0190** | Boshqa asosiy vositalar va mahsuldor hayvonlar |
| **0195** | **Kutubxona jamg'armasi** — kitoblar va elektron manbalar (ta'lim tashkilotlarida) |
| **0199** | Konservatsiya qilingan asosiy vositalar |

### 🔴 Asosiy vosita chegarasi — 50 BHM
> Buyum `0100` da hisobga olinishi uchun qiymati **50 BHM dan ko'p** bo'lishi kerak.
> **Kam bo'lsa** — material/inventar sifatida `1000` yoki `1090` da.
> Sotuv uchun mo'ljallangan bo'lsa — `2900`.

### `0200` — Amortizatsiya (eskirish), **kontr-aktiv**
`0100` ga mutanosib: 0211 · 0212 · 0220 · 0230 · 0240 · 0250 · 0260 · 0270 · 0280 ·
0290 · 0295 · **0299** (uzoq muddatli ijaraga olingan AV eskirishi).

⚠️ Amortizatsiya normalari **Soliq kodeksida** belgilangan — amaldagi tahrirdan tekshiring.

### `0400` — Nomoddiy aktivlar
| Schyot | Nomi |
|--------|------|
| 0410 | Patentlar, litsenziyalar va nou-xau |
| 0420 | Savdo belgilari, tovar belgilari va sanoat namunalari |
| **0430** | **Dasturiy ta'minot** |
| 0440 | Yer va tabiiy resurslardan foydalanish huquqi |
| 0460 | Franshiza |
| 0470 | Mualliflik huquqi |
| 0490 | Boshqa nomoddiy aktivlar |

### `0500` — NMA amortizatsiyasi, **kontr-aktiv**
0510 · 0520 · 0530 · 0540 · 0560 · 0570 · 0590 — `0400` dagi juftiga mos.

### Qolganlar
| Schyot | Nomi |
|--------|------|
| 0600 / 0700 | O'rnatiladigan uskunalar ❓ (daftarda ikkalasi ham uchraydi — ish rejangizdan tekshiring) |
| 0800 | Kapital qo'yilmalar (0810 tugallanmagan qurilish, 0820 AV sotib olish, 0830 NMA sotib olish) ⚠️ |
| 0900 | Uzoq muddatli hisob-kitob / debitorlik qarzi ⚠️ |

**Asosiy vositaning yo'li:**
```
0820  →  0800  →  0100
sotib   ombordan  ekspluatatsiyaga
olindi  o'tkazildi  chiqarilganda
```

## 1 — Materiallar

| Schyot | Nomi |
|--------|------|
| **1010** | Xom ashyo va materiallar — ishlab chiqarishdagi asosiy xom ashyo ✅ |
| **1020** | Sotib olingan yarim tayyor mahsulot va butlovchi qismlar ✅ |
| **1030** | Yoqilg'i — benzin, gaz, ko'mir ✅ |
| **1040** | **Tara va tara materiallari** — saqlash/tashish uchun qutilar ✅ |
| **1050** | **Ehtiyot qismlar** — texnika va uskunalarni ta'mirlash uchun ✅ |
| **1060** | Boshqa materiallar ✅ |
| **1070** | Qayta ishlashga berilgan materiallar (tashqi tashkilotga) ✅ |
| **1080** | Qurilish materiallari ✅ |
| **1090** | **Inventar va xo'jalik jihozlari** — kichik inventarlar ✅ |
| 1500 | Materiallarni tayyorlash va sotib olish ⚠️ |

> ⚠️ **Diqqat:** `1040` va `1050` korxona daftarida standart tartibdan farq qiladi
> (1040 = tara, 1050 = ehtiyot qismlar). Ish rejangizdagi variant ustun.

TMZ sotib olish provodkasi manbadan tasdiqlangan: **`Dt 1010–1090 — Kt 6010`** ✅

## 2 — Ishlab chiqarish va tovarlar

| Schyot | Nomi |
|--------|------|
| 2010 | Asosiy ishlab chiqarish |
| 2310 | Yordamchi ishlab chiqarish ⚠️ |
| 2510 | Umumishlab chiqarish (sex) xarajatlari ⚠️ |
| 2810 | Tayyor mahsulot |
| 2910 | Omborlardagi tovarlar |
| 2920 | Chakana savdodagi tovarlar |
| 2960 | Savdo ustamasi (наценка) — **kontr-aktiv** ⚠️ |

## 3 — Kelgusi davr xarajatlari

| Schyot | Nomi |
|--------|------|
| 3100 | Kelgusi davr xarajatlari ⚠️ — oldindan to'langan ijara, sug'urta, obuna, domen/hosting |
| 3200 | Kechiktirilgan xarajatlar ⚠️ |

**Qoida:** bir necha oyga oldindan to'langan xizmat darhol xarajat emas — `3100` ga
kiritiladi va oylar bo'yicha `9420`/`2510` ga taqsimlanadi.

---

## 4 — Debitorlik qarzlari (bizga qarzdorlar) — ✅ manbadan tasdiqlangan

> Bu bo'lim NSBU № 21 va buxgalter.uz sharhlari bo'yicha aniqlashtirilgan.
> **Diqqat: `4410` — bu hisobdor shaxs emas, byudjetga avans to'lov!**

| Schyot | Nomi | Izoh |
|--------|------|------|
| **4010** | Xaridorlar va buyurtmachilardan olinadigan schyotlar | Eng ko'p ishlatiladigan debitorlik schyoti ✅ |
| 4020 | Olinadigan veksellar | ⚠️ |
| **4200** | **Xodimlarga berilgan avanslar** — guruh ✅ | |
| **4210** | Ish haqi bo'yicha berilgan avanslar | ✅ |
| **4220** | Xizmat safariga berilgan avanslar | ✅ Komandirovka |
| **4230** | Umumxo'jalik xarajatlariga berilgan avanslar | ✅ **Naqd pulga yoki korporativ bank kartasi orqali** mayda inventar/materiallar sotib olish uchun berilgan avanslar shu yerda |
| **4290** | Xodimlarga berilgan boshqa avanslar | ✅ 4210–4230 ga kirmagani |
| **4300** | **Mol yetkazib beruvchi va pudratchilarga berilgan avanslar** — guruh ✅ | `4310` asosiy subschyot |
| **4400 / 4410** | **Byudjetga soliqlar va boshqa majburiy to'lovlar bo'yicha avans (bo'nak) to'lovlar** ✅ | **Kirim (hisobga olinadigan) QQS ham shu yerda** hisobga olinadi ✅ |
| **4600** | Ta'sischilarning ustav kapitaliga ulushlari bo'yicha qarzi | ✅ |
| 4700 | Xodimlarning boshqa operatsiyalar bo'yicha qarzi | ⚠️ |
| **4800 / 4890** | Turli debitorlarning qarzi | ⚠️ Aniqlanmagan chiqim vaqtincha shu yerga |
| 4900 | Shubhali qarzlar bo'yicha zaxira — **kontr-aktiv** | ⚠️ |

### `4410` bo'yicha amaliy tavsiya
Kirim QQSini alohida kuzatish uchun `4410` ga subschyot yoki subkonto oching, masalan:
`4410/1 QQS — tovar va materiallar`, `4410/2 QQS — davr xarajatlari`,
`4410/3 QQS — asosiy vositalar`, `4410/9 boshqa soliqlar bo'yicha avans`.
QQSdan ozod va soliq solinadigan aylanma birga bo'lsa — **alohida hisob (раздельный
учёт)** majburiy, subschyotsiz uni yuritib bo'lmaydi.

---

## 5 — Pul mablag'lari

| Schyot | Nomi |
|--------|------|
| **5010** | Kassa — milliy valyutada ✅ |
| 5020 | Kassa — xorijiy valyutada |
| **5110** | Hisob-kitob (raschyot) schyoti — **bank vipiskasining asosiy schyoti** ✅ |
| **5210** | Valyuta schyoti (mamlakat ichida) |
| 5220 | Chet eldagi valyuta schyoti ⚠️ |
| 5510 | Akkreditivlar ⚠️ |
| 5520 | Chek daftarchalari ⚠️ |
| **5530** | Boshqa maxsus schyotlardagi pul mablag'lari — **korxonaning korporativ karta hisobi** ⚠️ |
| 5610 | Yo'ldagi pul o'tkazmalari (inkassatsiya, kun oralig'idagi o'tkazma) ⚠️ |
| 5810 | Qisqa muddatli investitsiyalar (depozit, qimmatli qog'oz) ⚠️ |

**Korporativ karta bo'yicha chalkashlikni oldini olish:**
- Karta **korxona nomida** va undagi pul hali sarflanmagan → `5530`
- Karta **xodimga** biriktirilgan, u xarid qilib avans hisoboti beradi → `4230`
Korxonangizda qaysi variant ekanini `memory/XOTIRA.md` ga yozing.

---

## 6 — Qisqa muddatli majburiyatlar (biz qarzdormiz)

| Schyot | Nomi |
|--------|------|
| **6010** | Mol yetkazib beruvchilar va pudratchilarga to'lanadigan schyotlar ✅ |
| 6020 | To'lanadigan veksellar |
| **6310** | Xaridorlar va buyurtmachilardan olingan avanslar ⚠️ |
| **6410** | **Byudjetga to'lovlar bo'yicha qarz (turlari bo'yicha)** ✅ — subschyotlar bilan yuritiladi |
| **6510** | Sug'urta va ijtimoiy ta'minot bo'yicha to'lovlar — **ijtimoiy soliq** ⚠️ |
| **6520** | Maqsadli davlat jamg'armalariga to'lovlar — **INPS** ⚠️ |
| 6610 | Ta'sischilarga to'lanadigan dividendlar ⚠️ |
| **6710** | **Mehnatga haq to'lash bo'yicha xodimlar bilan hisob-kitob** ✅ — **har bir xodim kesimida analitik hisob yuritiladi** |
| 6720 | Deponentlangan ish haqi ⚠️ |
| **6810** | Qisqa muddatli bank kreditlari ⚠️ |
| 6820 | Qisqa muddatli qarzlar (zayom) ⚠️ |
| 6830 | Uzoq muddatli majburiyatlarning joriy qismi ⚠️ |
| **6990** | Boshqa kreditorlik qarzlari ⚠️ — **aniqlanmagan tushum vaqtincha shu yerga** |

**`6410` — chiqim (hisoblangan) soliqlar schyoti.** `4410` bilan juftlik hosil qiladi:
`4410` — biz byudjetga oldindan bergan / kirim QQS, `6410` — biz byudjetga qarzdormiz.

Tavsiya etilgan `6410` subschyotlari:
`6410/1 QQS`, `6410/2 Foyda solig'i`, `6410/3 Aylanmadan soliq`, `6410/4 JShDS`,
`6410/5 Mol-mulk solig'i`, `6410/6 Yer solig'i`, `6410/7 Suv solig'i`, `6410/9 Jarima va penya`.

## 7 — Uzoq muddatli majburiyatlar

| Schyot | Nomi |
|--------|------|
| 7810 | Uzoq muddatli bank kreditlari ⚠️ |
| 7820 | Uzoq muddatli qarzlar ⚠️ |
| 7900 | Kechiktirilgan soliq majburiyatlari ⚠️ |

## 8 — Xususiy kapital

| Schyot | Nomi |
|--------|------|
| **8310** | Oddiy aksiyalar ✅ · **8311** foydadan zaxira fondiga taqsimlash · **8320** imtiyozli aksiyalar · **8330** paylar va badallar |
| **8410** | Emissiya daromadi ✅ · **8420** ustav kapitalini shakllantirishdagi valyuta kurs farqi |
| **8510** | Mulkni qayta baholash bo'yicha tuzatish ✅ · **8520** zaxira kapitali · **8530** **bepul (tekinga) olingan mulk** |
| **8610 / 8620** | Sotib olingan xususiy oddiy / imtiyozli aksiyalar ✅ |
| **8710** | Hisobot davrining taqsimlanmagan foydasi (qoplanmagan zarari) ✅ · **8720** to'plangan foyda |
| **8810** | **Grantlar** ✅ · **8820** subsidiyalar · **8830** a'zolik badallari · **8840** maqsadli soliq imtiyozlari · **8890** boshqa maqsadli tushumlar |
| **8910** | Kelgusi xarajat va to'lovlar zaxirasi ✅ |

---

## 9 — Daromadlar va xarajatlar

### Daromadlar (Kt bo'yicha yig'iladi)

| Schyot | Nomi |
|--------|------|
| **9010** | Tayyor mahsulot sotishdan daromad |
| **9020** | Tovarlar sotishdan daromad ✅ (`Dt 4010 — Kt 9020` manbadan tasdiqlangan) |
| **9030** | Ishlar bajarish va xizmatlar ko'rsatishdan daromad |
| **9040** | **Sotilgan tovarlarni qaytarish** — kontr-daromad ✅ |
| **9050** | **Xaridorlar va buyurtmachilarga berilgan chegirmalar** — kontr-daromad ✅ |
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
| **9140** | Davriy hisobda TMZ sotib olish ✅ |
| **9150** | Davriy hisobda TMZ bo'yicha tuzatishlar ✅ |
| **9410** | Sotish xarajatlari (reklama, yetkazib berish, savdo xodimlari ish haqi) |
| **9420** | Ma'muriy xarajatlar (boshqaruv ish haqi, ofis ijarasi, aloqa, audit) |
| **9430** | Boshqa operatsion xarajatlar — 🔴 **korxonada asosan BANK XIZMAT HAQLARI**, davlat boji, SWIFT kurs/komissiya farqi ✅ |

> **`9400` = davr xarajatlari, uchta subschyotga bo'linadi: `9410` / `9420` / `9430`** ✅
> - `9410` — reklama, ijtimoiy tarmoq targetlari, bosmaxona/tanishtiruv materiallari, sotuv xodimlari oyligi
> - `9420` — ma'muriyat xarajatlari, **direktor oyligi**, uning ofisidagi mebel va texnika
> - `9430` — bank xizmatlari, davlat boji, boshqa majburiy to'lovlar
| **9610** | Foizlar ko'rinishidagi xarajatlar (kredit foizi) |
| **9690** | Valyuta kursi farqi bo'yicha zarar |
| 9710 | Favqulodda foyda va zararlar ⚠️ |
| **9810** | Foyda solig'i bo'yicha xarajat |
| **9820** | Foydadan boshqa soliqlar va yig'imlar |
| **9910** | Yakuniy moliyaviy natija — yil oxirida 9-bo'lim shu yerga yopiladi |

---

## 4 ↔ 6 juftlik sxemasi ✅ (korxona daftaridan)

| Debitor (4) | ↔ | Kreditor (6) | Kim bilan hisob-kitob |
|---|---|---|---|
| **4300** | ↔ | **6000** | Mol yetkazib beruvchi va xizmat ko'rsatuvchilar |
| **4000** | ↔ | **6300** | Xaridorlar |
| **4400** | ↔ | **6400** | Byudjet (soliqlar) |
| **4500** | ↔ | **6500** | Ijtimoiy (pul) fondlar |
| **0900** | | | Uzoq muddatli hisob-kitob |

**Mantiq:** 4-bo'lim — biz oldindan berdik yoki bizga qarzdor; 6-bo'lim — biz qarzdormiz.

---

## Eslab qolish uchun mnemonika

- **4 — bizga qarz** (debitor), **6 — biz qarzdor** (kreditor).
  Juftliklar: `4010 ↔ 6310` (xaridor), `6010 ↔ 4310` (ta'minotchi), `4410 ↔ 6410` (byudjet).
- **42xx — xodimga berilgan avans** (4210 ish haqi, 4220 safar, 4230 xo'jalik, 4290 boshqa).
- **43xx — ta'minotchiga berilgan avans.**
- **44xx — byudjetga avans va kirim QQS.**
- **5 — pul.** **9 — natija.**
- **Xarajat schyotini tanlash:** mahsulotga bevosita bog'liq → `2010`/`9110`;
  sotishga → `9410`; ofis/boshqaruv → `9420`; qolgani → `9430`.

---

## Manbalar

- **`memory/DAFTAR.md`** — korxona buxgalterining ish daftari (79 sahifa): 0100–0199, 0200–0299, 0400–0490, 0500–0590, 1000–1090, 8300–8910, 9000–9150 subschyotlari shu yerdan tasdiqlangan

- [lex.uz — yangi NSBU № 21 (3593-son, 27.12.2024)](https://lex.uz/ru/docs/7282759)
- [lex.uz — eski NSBU № 21 (1181-son, 23.10.2002)](https://lex.uz/acts/417624)
- [buxgalter.uz — Schyotlar rejasi](https://buxgalter.uz/plan_schetov)
- [buxgalter.uz — 4200 xodimlarga berilgan avanslar](https://buxgalter.uz/publish/group4706_razdel_iv_3_scheta_ucheta_avansov_vydannyh_personalu_4200)
- [buxgalter.uz — NSBU 6 va NSBU 21 dagi ijara o'zgarishlari](https://buxgalter.uz/publish/doc/text210751_chto_menyaetsya_v_voprosah_ucheta_arendy_nsbu_6_i_nsbu_21)
