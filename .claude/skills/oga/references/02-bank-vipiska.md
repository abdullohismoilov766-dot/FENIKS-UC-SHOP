# Bank vipiskasini provodkaga o'girish

## 0. Asosiy qoida (buni buzmang)

> **Bank vipiskasi xarajat yozmaydi — u qarzni yopadi.**

To'g'ri ketma-ketlik doim ikki bosqichli:

1. **Hujjat bo'yicha** (EHF, akt, nakladnoy) — qarz paydo bo'ladi:
   `Dt 9420/2010/1010/2910 ... — Kt 6010`
2. **Vipiska bo'yicha** — qarz yopiladi:
   `Dt 6010 — Kt 5110`

Faqat 3 ta istisno bevosita vipiskadan yoziladi: **bank komissiyasi**, **kredit foizi**,
**valyuta kursi farqi**.

Agar birov "to'lovni to'g'ridan-to'g'ri 9420 ga yoz" desa — bu xato: hujjat va soliq
hisobi bir-biriga bog'lanmay qoladi, QQS hisobga olinmaydi, akt-sverka farq qiladi.

---

## 1. Har bir qatorni tahlil qilish tartibi

Ketma-ket 5 savol:

| # | Savol | Nima beradi |
|---|-------|-------------|
| 1 | **Yo'nalish?** Kirim (приход) yoki chiqim (расход)? | 5110 Dt da yoki Kt da |
| 2 | **Kim bilan?** Kontragent nomi va STIR (INN) | 4010/6010 subkonto, yoki byudjet/bank |
| 3 | **Nima uchun?** To'lov maqsadi matni | Quyidagi kalit so'zlar jadvali |
| 4 | **Hujjat bormi?** Shartnoma, EHF, akt raqami | Avans (4310/6310) yoki qarz yopilishi (6010/4010) |
| 5 | **Bu birinchi harakatmi?** | Avans oldinmi yoki mahsulot oldinmi — 4310/6310 tanlanadi |

**5-savol eng ko'p xato beradi.** Qoida:
- **Pul oldin ketdi, tovar keyin keladi** → `Dt 4310 — Kt 5110` (biz avans berdik)
- **Tovar oldin keldi, pul keyin ketdi** → `Dt 6010 — Kt 5110` (qarzni yopdik)
- **Pul oldin keldi, tovar keyin ketadi** → `Dt 5110 — Kt 6310` (bizga avans tushdi)
- **Tovar oldin ketdi, pul keyin keldi** → `Dt 5110 — Kt 4010` (xaridor qarzini yopdi)

Agar bilmasangiz — kontragent bo'yicha 4010/6010 aylanmasiga qarang: qoldiq bor bo'lsa
qarz yopilmoqda, qoldiq nol bo'lsa avans.

---

## 2. KIRIM (Dt 5110) — kalit so'zlar jadvali

| To'lov maqsadidagi so'zlar | Provodka | Izoh |
|---|---|---|
| "tovar uchun", "xizmat uchun", "shartnoma №… bo'yicha", "hisobvaraq-faktura №…" | **Dt 5110 — Kt 4010** | Xaridor qarzini yopdi |
| "oldindan to'lov", "avans", "predoplata", tovar hali berilmagan | **Dt 5110 — Kt 6310** | Olingan avans. QQS to'lovchida — avansdan QQS masalasini tekshiring |
| "ustav kapitaliga ulush", "ustavniy fond" | **Dt 5110 — Kt 4600** | Ta'sischilarning ustav kapitaliga qarzi yopildi |
| "kredit", "ssuda", "kredit liniyasi bo'yicha mablag'" | **Dt 5110 — Kt 6810** (12 oygacha) yoki **Kt 7810** (12 oydan uzoq) | Shartnoma muddatiga qarang |
| "qarz", "zayom" (yur./jism. shaxsdan) | **Dt 5110 — Kt 6820** / 7820 | |
| "ortiqcha to'langan soliq qaytarildi", "vozvrat naloga" | **Dt 5110 — Kt 4410** (yoki Kt 6410) | Byudjetga avans to'lov qaytdi. Qaysi soliq — subschyotni ko'rsating |
| "ta'minotchidan avans qaytarildi", "vozvrat predoplati" | **Dt 5110 — Kt 4310** | Bergan avansimiz qaytdi |
| "depozit foizi", "protsent po vkladu" | **Dt 5110 — Kt 9510** | Moliyaviy daromad |
| "depozit qaytarildi" | **Dt 5110 — Kt 5810** | Investitsiya yopildi |
| "inkassatsiya", "naqd pul topshirildi" | **Dt 5110 — Kt 5010** (yoki 5610 orqali) | Kassadan bankka |
| "jarima", "penya", "neustoyka" (bizga to'landi) | **Dt 5110 — Kt 9390** | Boshqa operatsion daromad |
| "subsidiya", "grant", "kompensatsiya" | **Dt 5110 — Kt 8800/9390** ⚠️ | Maqsadli mablag'mi — aniqlang |
| "sug'urta qoplamasi" | **Dt 5110 — Kt 9390** ⚠️ | |
| **Maqsad tushunarsiz / kontragent noma'lum** | **Dt 5110 — Kt 6990** | ❓ "Aniqlanishi kerak" ro'yxatiga qo'ying, kontragentdan xat so'rang |

---

## 3. CHIQIM (Kt 5110) — kalit so'zlar jadvali

### Kontragentlarga

| To'lov maqsadi | Provodka | Izoh |
|---|---|---|
| "tovar uchun", "xizmat uchun" — mol allaqachon olingan | **Dt 6010 — Kt 5110** | Qarzni yopish |
| "oldindan to'lov", "avans", "predoplata" — mol hali olinmagan | **Dt 4310 — Kt 5110** | Berilgan avans |
| "ijara haqi" (arenda) | **Dt 6010 — Kt 5110** | Xarajat esa akt bo'yicha: `Dt 9420 — Kt 6010` |
| "kommunal", "elektr energiya", "gaz", "suv", "issiqlik" | **Dt 6010 — Kt 5110** | Xarajat: `Dt 9420/2510 — Kt 6010` |
| "aloqa", "internet", "telefon", "hosting", "domen" | **Dt 6010 — Kt 5110** | Yillik obuna bo'lsa avval `3100` |
| "yoqilg'i", "benzin", "GSM" | **Dt 6010 — Kt 5110** | Kirim: `Dt 1030 — Kt 6010` |
| "transport xizmati", "yetkazib berish" | **Dt 6010 — Kt 5110** | Xarajat 9410 yoki tannarxga |
| "reklama xizmati" | **Dt 6010 — Kt 5110** | Xarajat: `Dt 9410 — Kt 6010` |
| "audit", "konsalting", "yuridik xizmat" | **Dt 6010 — Kt 5110** | Xarajat: `Dt 9420 — Kt 6010` |
| "xaridorga pul qaytarildi", "vozvrat" | **Dt 6310 — Kt 5110** (yoki Dt 4010) | Avans qaytarilishi |

### Byudjet va jamg'armalar

| To'lov maqsadi | Provodka |
|---|---|
| "QQS", "НДС" | **Dt 6410/1 — Kt 5110** |
| "foyda solig'i", "налог на прибыль" | **Dt 6410/2 — Kt 5110** |
| "aylanmadan soliq", "налог с оборота" | **Dt 6410/3 — Kt 5110** |
| "JShDS", "НДФЛ", "daromad solig'i" | **Dt 6410/4 — Kt 5110** |
| "ijtimoiy soliq", "социальный налог" | **Dt 6510 — Kt 5110** |
| "INPS", "jamg'arib boriladigan pensiya" | **Dt 6520 — Kt 5110** |
| "mol-mulk solig'i" | **Dt 6410/5 — Kt 5110** |
| "yer solig'i" | **Dt 6410/6 — Kt 5110** |
| "suv solig'i" | **Dt 6410/7 — Kt 5110** ⚠️ |
| "jarima", "penya" (byudjetga) | **Dt 6410/9 — Kt 5110**; hisoblanishi: `Dt 9430 — Kt 6410/9` |
| "davlat boji", "gosposhlina" | **Dt 9420 — Kt 5110** (yoki 6010 orqali) |

### Xodimlar

| To'lov maqsadi | Provodka |
|---|---|
| "ish haqi", "zarplata", "avans po zarplate" | **Dt 6710 — Kt 5110** |
| "hisobdor shaxs kartasiga", "podotchyot" (xo'jalik xarajatlariga) | **Dt 4230 — Kt 5110** — avans hisoboti bilan yopiladi |
| "safar xarajati", "komandirovka" | **Dt 4220 — Kt 5110** |
| "moddiy yordam" | **Dt 6710 — Kt 5110** ⚠️ JShDS/ijtimoiy soliq imtiyozini tekshiring |
| "dividend" | **Dt 6610 — Kt 5110**; dividenddan soliq ushlab qolinadi |

### Bank va moliya

| To'lov maqsadi | Provodka | Izoh |
|---|---|---|
| "bank xizmati", "komissiya", "RKO", "SMS-xabar", "kliyent-bank" | **Dt 9430 — Kt 5110** | ⚠️ Ba'zi korxonalar 9420 ni ishlatadi — bir marta tanlab, doim shunday yozing va XOTIRA ga yozib qo'ying |
| "kredit foizi", "protsent po kreditu" | **Dt 9610 — Kt 5110** | Foiz — moliyaviy xarajat |
| "kredit asosiy qarzi", "osnovnoy dolg" | **Dt 6810 / 7810 — Kt 5110** | Foiz bilan ARALASHTIRMANG |
| "depozitga qo'yildi" | **Dt 5810 — Kt 5110** | |
| "korporativ kartaga o'tkazma" — karta **korxona** nomida | **Dt 5530 — Kt 5110** | Karta harakati alohida yuritiladi |
| "korporativ kartaga o'tkazma" — karta **xodimga** biriktirilgan | **Dt 4230 — Kt 5110** | Avans hisoboti bilan yopiladi |
| "konvertatsiya uchun so'm o'tkazildi" | **Dt 5210 — Kt 5110** + kurs farqi | Quyiga qarang |
| "kassaga naqd pul olindi" | **Dt 5010 — Kt 5110** | Chek/ariza asosida |
| **Maqsad tushunarsiz** | **Dt 4890 — Kt 5110** | ❓ Aniqlanishi kerak |

---

## 4. Valyuta schyoti (5210) — kurs farqi

Valyuta operatsiyasida **doim uchta narsa** bo'ladi: summa valyutada, kurs, so'mdagi ekvivalent.

1. Kirim: `Dt 5210 — Kt 4010` — operatsiya kunidagi MB kursi bo'yicha
2. Chiqim: `Dt 6010 — Kt 5210` — o'sha kun kursi bo'yicha
3. **Oy oxirida qayta baholash** (pereotsenka) — valyuta qoldig'i va valyutadagi
   qarzlar oxirgi kun kursiga keltiriladi:
   - Foyda: `Dt 5210/4010/6010 — Kt 9540`
   - Zarar: `Dt 9690 — Kt 5210/4010/6010`

**Konvertatsiya (so'm → valyuta):**
```
Dt 5210 — Kt 5110   (birja kursi bo'yicha sotib olingan valyuta)
Dt 9430/9690 — Kt 5110   (birja komissiyasi va kurs farqi) ⚠️
```
Konvertatsiya faktida bank hujjatini (birja ma'lumotnomasi) qo'shib qo'ying.

---

## 5. Vipiska bilan ishlashda 10 ta tipik xato

1. ❌ Xarajatni to'g'ridan-to'g'ri vipiskadan yozish (`Dt 9420 — Kt 5110`) — hujjat va
   QQS hisobga olinmay qoladi.
2. ❌ Avansni qarz yopilishi bilan aralashtirish — 4310 va 6010 chalkashadi, akt-sverka farq qiladi.
3. ❌ Kredit to'lovida asosiy qarz va foizni bitta provodkaga qo'shish.
4. ❌ Bank komissiyasini har oy turli schyotga (goh 9420, goh 9430) yozish.
5. ❌ Kontragentni subkonto bo'yicha ko'rsatmaslik — 6010 umumiy bo'lib qoladi, qarz kimniki noma'lum.
6. ❌ Shartnoma subkontosini tanlamaslik — bitta kontragent bilan bir nechta shartnoma bo'lsa qoldiq chalkashadi.
7. ❌ Soliq to'lovini 6410 ning noto'g'ri subschyotiga yozish — deklaratsiya bilan qoldiq mos kelmaydi.
8. ❌ INPS ni ijtimoiy soliq bilan aralashtirish (6520 va 6510).
9. ❌ Valyuta operatsiyasini oy oxirida qayta baholamaslik.
10. ❌ Tushunarsiz to'lovni "o'xshatib" biror schyotga yozib yuborish — keyin topib bo'lmaydi.

---

## 6. Vipiskani yopish (sverka) — oylik nazorat

Oy oxirida quyidagi 5 nazorat bajariladi:

| # | Nazorat | Qanday |
|---|---------|--------|
| 1 | **Qoldiq mos** | 5110 oxirgi qoldig'i = bank vipiskasidagi oxirgi qoldiq. Bir tiyin farq bo'lsa ham qidiring |
| 2 | **Aylanma mos** | Oylik kirim/chiqim jami = vipiska yakuni |
| 3 | **6010/4010 sverka** | Doimiy kontragentlar bilan akt-sverka |
| 4 | **6410 sverka** | Soliq qoldig'i my.soliq.uz shaxsiy kabinetidagi qoldiq bilan solishtiriladi |
| 5 | **Aniqlanmaganlar** | 6990 va 4890 da qoldiq qolmasin — hammasi aniqlanib, to'g'ri schyotga o'tkazilsin |

---

## 7. OGA javob shabloni (vipiska so'ralganda)

```
### Provodkalar

| № | Sana | Summa | Kontragent | Maqsad | Dt | Kt | Izoh | Ishonch |
|---|------|-------|-----------|--------|----|----|------|---------|
| 1 | 03.09 | 12 000 000 | "Alfa" MChJ | tovar uchun sh/n 12 | 6010 | 5110 | qarz yopildi | ✅ |
| 2 | 05.09 | 45 000 | Bank | komissiya | 9430 | 5110 | RKO | ✅ |
| 3 | 07.09 | 8 000 000 | noma'lum | maqsad ko'rsatilmagan | 6990 | 5110 | — | ❓ |

### Aniqlanishi kerak
- 3-qator: kontragent STIRi va shartnoma raqami kerak. Bankdan to'lov hujjati nusxasini so'rang.

### Diqqat
- 2-qator: bank komissiyasi uchun korxonada 9430 tanlangan (XOTIRA dagi qoida). Doim shu schyot ishlatilsin.
```


---

## 8. Manbadan tasdiqlangan provodkalar (rus tilidagi manbalardan o'girilgan)

| Operatsiya | Provodka |
|-----------|----------|
| Mahsulot / tovar / ish / xizmat sotuvidan hisob raqamiga tushum | `Dt 5110 — Kt 4010` |
| Tovarni pul o'tkazma orqali sotishdan daromad | `Dt 4010 — Kt 9020` |
| TMZ (material, tovar) sotib olish | `Dt 1010–1090 — Kt 6010` |
| Xodimga xo'jalik xarajatlariga avans (naqd yoki korporativ karta) | `Dt 4230 — Kt 5110 / 5010` |
| Xizmat safariga avans | `Dt 4220 — Kt 5110 / 5010` |
| Ish haqi bo'yicha berilgan avans | `Dt 4210 — Kt 5110 / 5010` |
| Byudjetga avans to'lov va kirim (hisobga olinadigan) QQS | `4410` |
| Byudjetga hisoblangan soliq qarzi | `6410` |
| Ish haqi bo'yicha hisob-kitob (har xodim kesimida analitik) | `6710` |

**Manbalar:**
[legalise.uz — korxona faoliyati bo'yicha asosiy provodkalar](https://legalise.uz/poleznaya-informatsiya/osnovnye-bukhgalterskie-provodki-po-deyatelnosti-predpriyatiya-v-uzbekistane) ·
[legalise.uz — tovar va xizmat sotish provodkalari](https://legalise.uz/poleznaya-informatsiya/bukhgalterskie-provodki-pri-realizatsii-tovarov-i-uslug-v-uzbekistane) ·
[bss.uz — buxgalter uchun provodkalar shpargalkasi](https://www.bss.uz/article/597-osnovnye-buhgalterskie-provodki-shpargalka-dlya-buhgaltera) ·
[buxgalter.uz — 4200 «Xodimlarga berilgan avanslar»](https://buxgalter.uz/publish/group4706_razdel_iv_3_scheta_ucheta_avansov_vydannyh_personalu_4200)
