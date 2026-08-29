# Elektron hisobvaraq-faktura (EHF / ЭСФ) — xatosiz yuborish

## 1. Tizimlar

| Tizim | Manzil | Nima uchun |
|-------|--------|-----------|
| **my.soliq.uz** | Soliq qo'mitasi shaxsiy kabineti | Deklaratsiyalar, soliq qoldig'i, EHF ko'rish |
| **Didox** | didox.uz | Eng keng tarqalgan EHF operatori |
| **Faktura.uz** | faktura.uz | Muqobil operator |
| **E-imzo / ERI** | e-imzo.uz | Elektron raqamli imzo kaliti — EHFsiz imzolab bo'lmaydi |

⚠️ Operator interfeysi vaqti-vaqti bilan o'zgaradi. Tugma nomlari mos kelmasa —
operatorning amaldagi qo'llanmasiga qarang, mantiq esa quyidagicha qoladi.

---

## 2. EHF rekvizitlari (majburiy maydonlar)

### Sarlavha qismi
| Maydon | Talab |
|--------|-------|
| EHF raqami | **Uzluksiz, tartib bilan.** Raqamda uzilish soliq tekshiruvida savol tug'diradi |
| EHF sanasi | Tovar jo'natilgan / xizmat ko'rsatilgan sana bilan mos bo'lsin |
| Shartnoma raqami va sanasi | Bo'lmasa xaridor rad etishi mumkin |
| Yuk xati / nakladnoy raqami | Tovar bo'lsa |

### Sotuvchi va xaridor
| Maydon | Talab |
|--------|-------|
| **STIR (INN)** | 9 raqam. **Bitta raqam xato bo'lsa EHF butunlay boshqa korxonaga ketadi** |
| Korxona nomi | Davlat reyestridagi nom bilan bir xil |
| Manzil | Yuridik manzil |
| Bank rekvizitlari | Hisob raqami (20 raqam) + MFO (5 raqam) + bank nomi |
| **PINFL/JShShIR** | Jismoniy shaxs xaridor bo'lsa |

### Tovar/xizmat qatorlari
| Maydon | Talab |
|--------|-------|
| **MXIK (ИКПУ) kodi** | 17 raqamli tovar/xizmat klassifikator kodi. **Eng ko'p xato shu yerda** |
| Tovar/xizmat nomi | MXIK kodidagi nom bilan mos bo'lishi kerak |
| O'lchov birligi | MXIK kodiga biriktirilgan birlik bilan mos |
| Miqdor | |
| Narx (QQSsiz) | |
| **QQS stavkasi** | 12% / 0% / "QQSsiz" (ozod) |
| QQS summasi | |
| Aktsiz (bo'lsa) | |
| **Jami summa** | Barcha qatorlar yig'indisi hujjat yakuni bilan mos |
| Markirovka kodi | Markirovka qilinadigan tovarlar uchun (⚠️ ro'yxat kengaymoqda — tekshiring) |

---

## 3. YUBORISHDAN OLDINGI 14 PUNKTLI TEKSHIRUV

> Har punktga ✅ / ❌ / ❓ qo'ying. **Bitta ❌ bo'lsa — yubormang.**

| # | Tekshiruv | Nega muhim |
|---|-----------|-----------|
| 1 | **Xaridor STIRi to'g'rimi?** my.soliq.uz da STIR bo'yicha nom tekshirilgan | Xato STIR — EHF boshqa korxonaga ketadi, qaytarib olish qiyin |
| 2 | **Xaridor QQS to'lovchisimi?** | Stavka va xaridorning hisobga olish huquqi shunga bog'liq |
| 3 | **EHF sanasi to'g'rimi?** Tovar jo'natilgan / akt sanasi bilan mos | Boshqa oyga tushib qolsa deklaratsiya buziladi |
| 4 | **Raqam ketma-ketligi uzilmaganmi?** | Uzilish — tekshiruvda savol |
| 5 | **Shartnoma raqami va sanasi kiritilganmi?** | Xaridor rad etishining №1 sababi |
| 6 | **MXIK (IKPU) kodi tovarga mos kelyaptimi?** | №1 xato. Kod noto'g'ri bo'lsa QQS chegirmasi rad etiladi |
| 7 | **O'lchov birligi MXIK dagi birlik bilan bir xilmi?** | dona/kg/metr chalkashligi |
| 8 | **QQS stavkasi to'g'rimi?** (12% / 0% / ozod) | Ozod bo'lsa — Soliq kodeksining tegishli moddasi ko'rsatiladi |
| 9 | **QQS summasi arifmetik to'g'rimi?** (baza × 12%) | Yaxlitlash farqi |
| 10 | **Jami summa shartnoma/akt/to'lov bilan mos kelyaptimi?** | Sverkada farq chiqadi |
| 11 | **Valyuta va kurs to'g'rimi?** (valyutali bo'lsa) | |
| 12 | **Imzolovchi va ERI kaliti amal qiladimi?** | Muddati o'tgan ERI — yuborilmaydi |
| 13 | **Markirovka/aktsiz talab qilinadigan tovarmi?** | Kod bo'lmasa hujjat rad etiladi |
| 14 | **Xaridorning hisob raqami va MFO to'g'rimi?** | To'lov qaytib kelmasin |

**Qo'shimcha 3 ta amaliy nazorat:**
- Bir xil tovar oldingi EHF larda qaysi MXIK bilan ketgan — **shu kodni qayta ishlating**
  (nomenklatura kartochkasida saqlab qo'ying).
- Oy oxirida: yuborilgan EHF lar jami = 9010/9020/9030 aylanmasi = QQS deklaratsiyasi.
- Xaridor 10 kun ichida qabul qilmasa — telefon qiling, "kutish" holatida qolgan EHF
  QQS chegirmasini kechiktiradi.

---

## 4. Xaridor tomonidan qabul qilish / rad etish

| Holat | Nima bo'ladi | Nima qilish |
|-------|-------------|-------------|
| **Qabul qilindi (aksept)** | Hujjat kuchga kiradi, ikkala tomonda hisobga olinadi | Hech narsa |
| **Rad etildi (otkaz)** | Hujjat bekor bo'ladi | Sababni so'rang, tuzatib **qaytadan yangi EHF** yuboring |
| **Javob yo'q** | ⚠️ Belgilangan muddat o'tgach avtomatik qabul qilingan hisoblanishi mumkin — amaldagi qoidani tekshiring | Xaridorga eslating |

**Rad etishning eng ko'p sabablari:**
1. Shartnoma raqami yo'q yoki noto'g'ri
2. MXIK kodi mos emas
3. Summa akt/nakladnoy bilan farq qiladi
4. Sana noto'g'ri (oldingi oy)
5. Miqdor real qabul qilingan miqdordan farq qiladi

---

## 5. Xatoni tuzatish — qaysi turdagi EHF kerak

| Vaziyat | Kerakli hujjat |
|---------|----------------|
| Rekvizitda xato (STIR, nom, shartnoma, MXIK), summa o'zgarmaydi | **Tuzatilgan EHF** (исправленный) — asl EHF ga havola bilan |
| Narx yoki miqdor o'zgardi (chegirma, qo'shimcha jo'natma) | **Qo'shimcha EHF** (дополнительный) — farq summasiga |
| Tovar qaytarildi | **Qaytarish EHFsi** yoki manfiy qo'shimcha EHF ⚠️ |
| EHF butunlay keraksiz (operatsiya bo'lmagan) | **Bekor qilish** — xaridor qabul qilmagan bo'lsa; qabul qilingan bo'lsa tuzatilgan EHF |
| Xaridor allaqachon rad etgan | Yangi EHF yuboriladi, tuzatish shart emas |

⚠️ **Muddat:** tuzatish o'sha soliq davri ichida qilinsa — deklaratsiya o'zgarmaydi.
Keyingi davrda tuzatilsa — **aniqlashtirilgan (уточнённая) deklaratsiya** topshiriladi.

**Provodkada aks etishi:**
```
Qaytarish / kamaytirish:
  Dt 4010 — Kt 9020  (storno, manfiy summa)
  Dt 9020 — Kt 6410/1 (storno QQS)
  Dt 2910 — Kt 9120  (tannarx storno)
```

---

## 6. MXIK (IKPU) kodi bilan ishlash

1. Kod **tovarning haqiqiy tavsifiga** mos bo'lishi kerak, "o'xshash" emas.
2. Kodni tanlash: my.soliq.uz yoki Didox dagi MXIK katalogidan qidiruv orqali.
3. Kod topilgach — **nomenklatura kartochkasiga biriktirib qo'ying** (1C da
   `Номенклатура` ma'lumotnomasidagi maxsus maydon), keyingi safar qidirmang.
4. Kodga biriktirilgan **o'lchov birligini** o'zgartirib bo'lmaydi — hujjatda ham shu birlik.
5. Ayrim kodlar **markirovka** yoki **aktsiz** talab qiladi — katalogda belgisi bo'ladi.
6. Xizmatlar uchun ham MXIK kodi bor — "xizmatga kod kerak emas" degan tushuncha xato.

**Yangi tovar kiritish tartibi (tavsiya):**
```
1. MXIK katalogidan kod topiladi
2. Kod, nom, o'lchov birligi nomenklatura kartochkasiga yoziladi
3. XOTIRA faylidagi "Doimiy MXIK kodlari" jadvaliga qo'shiladi
4. Birinchi EHF yuborilgandan keyin xaridor qabul qilganiga ishonch hosil qilinadi
```

---

## 7. EHF va soliq hisoboti bog'liqligi

| Nima | Qayerga ta'sir qiladi |
|------|----------------------|
| Yuborilgan EHF | Sotuvdan QQS (6410/1 Kt), daromad (9010/9020/9030) |
| Qabul qilingan EHF | Kirim QQS chegirmasi, xarajat/tovar kirimi |
| **Qabul qilinmagan kirim EHF** | ⚠️ QQS chegirmasi olinmaydi — QQS ortiqcha to'lanadi |
| Bekor qilingan EHF | Deklaratsiyadan chiqarilishi kerak |

**Oylik nazorat:** my.soliq.uz dagi "Reestr" bo'limidan chiqarilgan va kirilgan EHF
ro'yxatini yuklab oling va 1C/Venkon bazasidagi hujjatlar bilan solishtiring.
Bazada bor, reestrda yo'q — hujjat yuborilmagan. Reestrda bor, bazada yo'q — kiritilmagan.
