# Vernon bazasi

> ## ⚠️ Bu fayl hali TO'LDIRILMAGAN
>
> OGA "Vernon" nomli baza haqida tasdiqlangan ma'lumotga ega emas va **taxmin
> qilmaydi** — noto'g'ri ma'lumot buxgalteriyada xatoga olib keladi.
>
> Bu fayl **anketa** sifatida tuzilgan. Foydalanuvchi javob berganda OGA javoblarni
> shu faylga va `memory/XOTIRA.md` ga yozadi. Shundan keyin Vernon bo'yicha savollarga
> aniq javob bera boshlaydi.
>
> Agar "Vernon" deganda boshqa nom (masalan, boshqa ERP yoki ichki ishlanma baza)
> nazarda tutilgan bo'lsa — OGA avval aniqlab oladi.

---

## 1. To'ldiriladigan anketa

OGA foydalanuvchidan quyidagilarni **birma-bir** so'raydi (bir yo'la hammasini emas,
3–4 tadan). Javob kelgan sari shu yerga yoziladi.

### A. Baza haqida umumiy
- [ ] To'liq nomi va versiyasi:
- [ ] Ishlab chiquvchi / yetkazib beruvchi:
- [ ] Turi: buxgalteriya / savdo / ombor / ishlab chiqarish / kompleks ERP?
- [ ] Interfeys tili: o'zbek / rus / ingliz
- [ ] Kirish: veb-brauzer / desktop dastur / mobil
- [ ] Ma'lumot bazasi: MS SQL / PostgreSQL / MySQL / fayl

### B. Buxgalteriya bilan bog'liqligi
- [ ] Vernon o'zi provodka yozadimi, yoki faqat operativ hisob (savdo/ombor)mi?
- [ ] Provodka yozsa — qaysi schyotlar rejasidan foydalanadi (NSBU / o'z rejasi)?
- [ ] 1C bilan qanday bog'langan: qo'lda / fayl orqali (Excel, XML, CSV) / API?
- [ ] Ma'lumot qaysi yo'nalishda ketadi: Vernon → 1C, 1C → Vernon, ikki tomonlama?
- [ ] Almashinuv qanchalik tez-tez: kunlik / oylik / real vaqtda?

### C. Hujjatlar
- [ ] Vernon da yaratiladigan asosiy hujjatlar ro'yxati:
- [ ] EHF (schet-faktura) Vernon dan yuboriladimi yoki Didox/1C dan?
- [ ] Bank vipiskasi Vernon ga yuklanadimi?
- [ ] Kassa/POS operatsiyalari Vernon da yuritiladimi?

### D. Ma'lumotnomalar
- [ ] Kontragentlar qayerda yuritiladi — Vernon da yoki 1C da (asosiy manba qaysi)?
- [ ] Nomenklatura va MXIK kodlari qayerda saqlanadi?
- [ ] Ikkala bazada kod/ID qanday moslashtirilgan (mapping bormi)?

### E. Tez-tez uchraydigan muammolar
- [ ] Vernon va 1C qoldiqlari qaysi hollarda farq qiladi?
- [ ] Almashinuvda qaysi ma'lumot ko'pincha "tushib qoladi"?
- [ ] Kim mas'ul (ichki xodim / tashqi dasturchi / vendor qo'llab-quvvatlashi)?

---

## 2. Anketa to'ldirilgach — Vernon bo'limi

> Bu bo'lim javoblar asosida OGA tomonidan to'ldiriladi. Hozircha bo'sh.

### 2.1 Baza tavsifi
_(to'ldirilmagan)_

### 2.2 Vernon ↔ 1C moslik jadvali
| Vernon dagi hujjat/tushuncha | 1C dagi mos hujjat | Provodka |
|---|---|---|
| _(to'ldirilmagan)_ | | |

### 2.3 Almashinuv reglamenti (qadamlar)
_(to'ldirilmagan)_

### 2.4 Nazorat nuqtalari (sverka)
_(to'ldirilmagan)_

---

## 3. Har qanday ikkinchi baza uchun umumiy qoidalar

Vernon tafsilotlari aniqlanmaguncha OGA quyidagi universal qoidalardan foydalanadi —
bular ikkita baza parallel yuritilganda **har doim** amal qiladi:

1. **Bitta haqiqat manbasi (single source of truth).** Har bir ma'lumot turi uchun
   qaysi baza "asosiy" ekanini yozib qo'ying: masalan, kontragentlar — 1C, tovar
   qoldig'i — Vernon. Ikkala joyda mustaqil tahrirlash taqiqlanadi.

2. **Moslik kodi (mapping).** Har kontragent va nomenklatura elementiga ikkala bazada
   bir xil tashqi kod (STIR, artikul) biriktirilsin. Kod bo'lmasa — nom bo'yicha
   solishtirish doim xato beradi.

3. **Almashinuv jurnali.** Har yuklash sanasi, fayl nomi, qatorlar soni va xatolar
   qayd qilinsin. "Qachon yuklanganini bilmayman" — eng qimmat holat.

4. **Oylik uch nuqtali sverka:**
   | Nima | Vernon | 1C | my.soliq.uz |
   |------|--------|----|-------------|
   | Sotuv aylanmasi | ✓ | ✓ | ✓ (EHF reestri) |
   | Tovar qoldig'i | ✓ | ✓ | — |
   | Pul qoldig'i | — | ✓ | — (bank vipiskasi) |

   Uchtasi mos kelmasa — oy yopilmaydi.

5. **Ikki tomonlama kiritish taqiqlanadi.** Bir hujjat faqat bitta bazada yaratiladi,
   ikkinchisiga faqat ko'chiriladi. Aks holda dublikat va qo'sh daromad paydo bo'ladi.

6. **Bekor qilish va tuzatish ham ko'chirilsin.** Ko'p integratsiyalar faqat yangi
   hujjatni uzatadi, o'chirilgan/tuzatilganini emas — natijada bazalar asta-sekin ajraladi.

7. **Arxiv ikkala bazadan ham** olinadi, bir xil sanada.
