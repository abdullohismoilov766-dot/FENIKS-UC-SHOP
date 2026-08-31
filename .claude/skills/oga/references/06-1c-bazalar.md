# 1C bazalari — eski (7.7) va yangi (8.x)

> **Eslatma:** korxonaning **Venkon** bazasi ham 1C:Korxona 8 platformasidagi
> konfiguratsiya, **clobus.uz** orqali bulutda ishlaydi. Shuning uchun bu faylning
> hammasi Venkon ga ham tegishli — `references/07-venkon-baza.md` ga qarang.

> Interfeys ko'pincha rus tilida, shuning uchun hujjat va ma'lumotnoma nomlari
> asl nomi bilan berilgan.

## 1. Versiyalar farqi

| | **1C 7.7** (eski baza) | **1C 8.2 / 8.3** (yangi baza) |
|---|---|---|
| Konfiguratsiya fayli | `1Cv7.md` | `1Cv8.cf` / `.dt` (yuklash-tushirish) |
| Ma'lumot bazasi | DBF (`*.DBF`) yoki MS SQL | Fayl (`1Cv8.1CD`) yoki MS SQL / PostgreSQL |
| Arxiv | Papkani to'liq nusxalash | `Выгрузить информационную базу` → `.dt` |
| Hisoblar rejasi | Bitta, "Основной" | Bir nechta reja, `Хозрасчетный` asosiy |
| Subkonto | 3 tagacha | Har schyotda 3 tagacha, keng imkoniyat |
| Davrlar | `Период` bo'yicha ishlash | `Даты запрета изменения` bilan yopiladi |
| Yopish | `Закрытие месяца` qayta ishlash | `Закрытие месяца` yordamchisi (bosqichma-bosqich) |
| Kirish | Terminal / lokal | Klient-server, veb-klient |

**Amaliy xulosa:** 7.7 arxivi — papka nusxasi; 8.x arxivi — `.dt` fayl.
Har oy yopilishidan **oldin** arxiv oling. Bu qoida buzilmasin.

---

## 2. Asosiy ma'lumotnomalar (справочники)

| Rus nomi | O'zbekcha | Nima e'tiborda bo'lsin |
|----------|-----------|------------------------|
| `Организации` | Tashkilotlar | Bir nechta yuridik shaxs bo'lsa — har hujjatda to'g'ri tanlansin |
| `Контрагенты` | Kontragentlar | **STIR (ИНН) majburiy to'ldiriladi**, dublikat yaratmang |
| `Договоры` | Shartnomalar | Har kontragentga alohida; **valyuta va hisob-kitob turi** to'g'ri bo'lsin |
| `Номенклатура` | Nomenklatura | **MXIK (ИКПУ) kodi va o'lchov birligi** shu yerda saqlanadi |
| `Склады` | Omborlar | |
| `Физические лица` | Jismoniy shaxslar | PINFL, ish haqi hisobi uchun |
| `Статьи затрат` | Xarajat moddalari | 9410/9420/9430 taqsimoti shu yerda hal bo'ladi |
| `Банковские счета` | Bank hisob raqamlari | MFO va hisob raqami |

⚠️ **Dublikat kontragent** — 1C dagi eng ko'p uchraydigan muammo. Natijada 6010/4010
qoldig'i ikkiga bo'linadi va akt-sverka farq qiladi. Yangi kontragent kiritishdan oldin
**STIR bo'yicha qidiring**.

---

## 3. Asosiy hujjatlar

| Rus nomi | O'zbekcha | Provodka |
|----------|-----------|----------|
| `Поступление товаров и услуг` | Tovar va xizmat kirimi | `Dt 2910/1010/9420 — Kt 6010` |
| `Реализация товаров и услуг` | Sotish | `Dt 4010 — Kt 9020/9030`, `Dt 9120 — Kt 2910` |
| `Счет-фактура полученный / выданный` | Kirim/chiqim EHF | QQS hisobi |
| `Платежное поручение` | To'lov topshiriqnomasi | **Provodka bermaydi** — faqat niyat |
| `Списание с расчетного счета` | Hisob raqamidan chiqim | `Dt 6010/6410/6710 — Kt 5110` |
| `Поступление на расчетный счет` | Hisob raqamiga kirim | `Dt 5110 — Kt 4010/6310` |
| `Авансовый отчет` | Avans hisoboti | `Dt 1010/9420 — Kt 4410` |
| `Приходный кассовый ордер (ПКО)` | Kirim kassa orderi | `Dt 5010 — Kt ...` |
| `Расходный кассовый ордер (РКО)` | Chiqim kassa orderi | `Dt ... — Kt 5010` |
| `Требование-накладная` | Talabnoma-nakladnoy | `Dt 2010 — Kt 1010` |
| `Начисление зарплаты` | Ish haqi hisoblash | `Dt 2010/9420 — Kt 6710` |
| `Операция (бухгалтерская)` | Qo'lda operatsiya | Ixtiyoriy provodka — **eng oxirgi chora** |

### 🔴 To'liq menyu xaritasi
Korxonaning bazasidagi **haqiqiy menyu tuzilmasi** (bo'lim-bo'lim, barcha hujjatlar bilan)
`memory/DAFTAR.md → 7-bo'lim` da. OGA 1C yo'li so'ralganda **avval o'sha faylga qaraydi**.
Qisqacha bo'limlar: `БАНК` · `КАССА` · `ПОКУПКА` · `ПРОДАЖА` · `СКЛАД` · `ОС` · `НМА` ·
`ПРОИЗВОДСТВО` · `ЗАРПЛАТА` · `КАДРЫ` · `МОНИТОР БУХГАЛТЕРА`.

⚠️ **`Платежное поручение` provodka bermaydi.** Ko'p yangi buxgalterlar shu yerda
adashadi: to'lov faqat `Списание с расчетного счета` hujjati bilan hisobga tushadi.

---

## 4. Bank vipiskasini 1C ga yuklash

### Klient-Bank almashinuvi
```
Bank dasturi  →  kl_to_1c.txt  →  1C ga yuklash
1C            →  1c_to_kl.txt  →  Bank dasturiga
```

**1C 8.3 da:** `Банк и касса` → `Банковские выписки` → `Загрузить` →
faylni tanlash → kontragentlarni solishtirish → `Загрузить`.

**Yuklashdan keyin har qatorni tekshiring:**
1. Kontragent to'g'ri topilganmi (STIR bo'yicha)? Topilmasa — 1C yangi dublikat yaratishi mumkin;
2. Shartnoma tanlanganmi;
3. Hisob-kitob schyoti (`Счет расчетов`) to'g'rimi — 6010 (qarz) yoki 4310 (avans);
4. Avans schyoti (`Счет авансов`) to'g'ri ko'rsatilganmi;
5. Xarajat moddasi to'ldirilganmi (bank komissiyasi uchun);
6. Hujjat **o'tkazilganmi** (`Проведен`) — o'tkazilmagan hujjat provodka bermaydi.

⚠️ **Avtomatik "Подбор" ga to'liq ishonmang.** U to'lov maqsadidagi matn bo'yicha
taxmin qiladi. Har oy 5–10 qator noto'g'ri schyotga tushadi.

---

## 4a. Korxonaning oylik ish tartibi (daftardan) ✅

| № | Qadam | Muddat |
|---|-------|--------|
| 1 | **SKLAD** — kiruvchi va chiquvchini kiritish | |
| 2 | **Omborxonada qoldiqni jo'natish**, inventarizatsiya, tekshirish va hisoblash | **5-sanagacha** |
| 3 | **Bankni kiritish** (vipiska) | |
| 4 | **Oylikni hisoblash va kiritish** | **5-sanagacha** |
| 5 | **Soliqqa hisobot jo'natish** | my.soliq.uz |
| 6 | **Import qilingan tovarni kiritish** (`Приход`) | GTD asosida |

**Oylik nazorat:** har oy `Анализ счёта` chiqariladi, **1C Excel bilan solishtiriladi**,
mos kelmagan joyga izoh yoziladi va tenglashtiriladi.

---

## 5. Oy yopilishi (`Закрытие месяца`) — tartib

| # | Qadam | Rus nomi |
|---|-------|----------|
| 1 | Barcha hujjatlar kiritilgan va o'tkazilganini tekshirish | `Проведение документов` |
| 2 | Vipiska qoldig'ini bank bilan solishtirish | — |
| 3 | Kassa qoldig'ini kassa kitobi bilan solishtirish | — |
| 4 | Ish haqini hisoblash va soliqlar | `Начисление зарплаты` |
| 5 | Amortizatsiya | `Амортизация ОС и НМА` |
| 6 | Valyuta qayta baholash | `Переоценка валютных средств` |
| 7 | Kelgusi davr xarajatlarini hisobdan chiqarish | `Списание РБП` |
| 8 | Tannarxni hisoblash | `Расчет себестоимости` |
| 9 | Xarajat schyotlarini yopish | `Закрытие счетов 20, 25, 26` |
| 10 | 9-bo'lim schyotlarini yopish (yil oxirida) | `Реформация баланса` |
| 11 | QQS hisobi | `Помощник по учету НДС` |
| 12 | Davrni yopish | `Дата запрета изменения` |

**Yopishdan keyin nazorat hisobotlari:**
- `Оборотно-сальдовая ведомость` (aylanma-qoldiq vedomosti) — manfiy qoldiq bormi?
- `Анализ счета` 5110, 6010, 4010, 6410 bo'yicha;
- `Экспресс-проверка ведения учета` (1C 8.3 da) — avtomatik xatolarni topadi.

---

## 6. Eski bazadan yangisiga o'tish (перенос данных)

| # | Qadam | Nima e'tiborda |
|---|-------|----------------|
| 1 | Eski bazani **arxivlash** | Nusxasiz ish boshlamang |
| 2 | O'tish sanasini belgilash (odatda 1-yanvar) | Yil o'rtasida o'tish murakkab |
| 3 | Eski bazada davrni yopish, balansni chiqarish | Kirish qoldiqlarining manbasi |
| 4 | Ma'lumotnomalarni ko'chirish | Kontragent, nomenklatura, shartnoma — **dublikatlarni tozalab** |
| 5 | **Kirish qoldiqlarini kiritish** (`Ввод начальных остатков`) | Schyot-schyot, subkonto kesimida |
| 6 | Balansni solishtirish | Yangi bazadagi qoldiq = eski bazadagi qoldiq (tiyingacha) |
| 7 | Sinov davri (1–2 oy parallel yuritish) | Farqlar chiqsa — o'sha yerda tuzatiladi |

**Kirish qoldiqlarida eng ko'p xato bo'ladigan schyotlar:**
`4010`, `6010` (kontragent va shartnoma kesimida bo'linmasa), `4210`–`4290` (hisobdor shaxslar),
`6410` (soliq subschyotlari), `0100/0200` (amortizatsiya bilan birga ko'chirilmasa),
`2910` (nomenklatura va ombor kesimida miqdor bilan).

⚠️ **Qoida:** kirish qoldiqlari faqat summada emas, **barcha subkonto kesimida** kiritiladi.
Aks holda birinchi akt-sverkada farq chiqadi va sababini topib bo'lmaydi.

---

## 7. 1C da tez-tez uchraydigan 12 muammo va yechimi

| Muammo | Sabab | Yechim |
|--------|-------|--------|
| Hujjat provodka bermayapti | O'tkazilmagan (`не проведен`) | `Провести` bosing; xato chiqsa matnini o'qing |
| `Оборотно-сальдовая` da manfiy qoldiq | Hujjatlar noto'g'ri tartibda / sana | Hujjat sanalari va vaqtini tekshiring, `Перепроведение` |
| 6010 da bir kontragent ikki marta | Dublikat kontragent | STIR bo'yicha qidiring, `Объединение элементов` |
| Sverkada farq | Shartnoma subkontosi tanlanmagan | Hujjatlarga shartnoma qo'shib qayta o'tkazing |
| QQS deklaratsiyasi bazaga mos emas | EHF hujjatlari kiritilmagan / rad etilgan | my.soliq.uz reestri bilan solishtiring |
| Tannarx hisoblanmayapti | Ombor qoldig'i manfiy | Kirim hujjatlarini sotuvdan oldin kiriting |
| Valyuta qoldig'i noto'g'ri | Qayta baholash bajarilmagan | `Переоценка валютных средств` |
| Ish haqi soliqlari noto'g'ri | Xodim kartochkasida stavka/imtiyoz xato | `Физические лица` va kadr hujjatlarini tekshiring |
| Yopilgan davr o'zgarib ketdi | `Дата запрета` qo'yilmagan | Yopilgan oyga taqiq sanasini qo'ying |
| Baza sekin ishlayapti | Jurnal katta, indeks buzilgan | `Тестирование и исправление`, arxiv oldin |
| Hisobot bo'sh chiqyapti | Davr yoki tashkilot filtri noto'g'ri | Hisobot sozlamalarini tekshiring |
| Amortizatsiya hisoblanmadi | AV kartochkasida usul/muddat yo'q | `Основные средства` kartochkasini to'ldiring |

---

## 8. Xavfsizlik qoidalari

1. **Har oy yopilishidan oldin arxiv** — `.dt` yoki papka nusxasi, sana bilan nomlangan.
2. **Yopilgan davrga taqiq** (`Дата запрета изменения`) — o'tgan oy o'zgarmasin.
3. **Foydalanuvchi huquqlari** — har buxgalterga o'z roli, hamma "Администратор" bo'lmasin.
4. **Qo'lda operatsiya (`Операция`) — faqat oxirgi chora** va doim izoh bilan.
5. **Arxivni boshqa diskda/bulutda saqlang** — server yonsa baza yo'qoladi.
