# Tipik provodkalar to'plami

> Belgilar: `✅` standart, `⚠️` kontekstga bog'liq / subschyotni tekshiring.

## 1. Tovar sotib olish (QQS to'lovchi)

| # | Operatsiya | Dt | Kt | Hujjat |
|---|-----------|----|----|--------|
| 1 | Tovar omborga qabul qilindi (QQSsiz qiymat) | 2910 | 6010 | EHF, nakladnoy |
| 2 | Kirim QQS ajratildi (12%) | 4410⚠️ / 6410/1⚠️ | 6010 | EHF |
| 3 | Ta'minotchiga to'landi | 6010 | 5110 | vipiska |

⚠️ **Kirim QQS schyoti:** amaliyotda `6410/1` ni qarama-qarshi (kontr) yozuv bilan yuritish
yoki alohida `4410`/`4410-QQS` subschyot ochish uchraydi. Korxonangizdagi variantni
`memory/XOTIRA.md` ga yozib qo'ying va doim bir xil ishlating.

## 2. Tovar sotish (QQS to'lovchi)

| # | Operatsiya | Dt | Kt |
|---|-----------|----|----|
| 1 | Sotuvdan daromad (QQS bilan jami) | 4010 | 9020 |
| 2 | Sotuvdan QQS hisoblandi | 9020 | 6410/1 |
| 3 | Sotilgan tovar tannarxi hisobdan chiqarildi | 9120 | 2910 |
| 4 | Xaridordan pul tushdi | 5110 | 4010 |

**QQS ajratish formulasi (summa QQS bilan berilgan bo'lsa):**
`QQS = Jami × 12 / 112` — QQSsiz baza = `Jami × 100 / 112`.
Masalan 11 200 000 so'm → QQS = 1 200 000, baza = 10 000 000.

## 3. Xizmat ko'rsatish

| Operatsiya | Dt | Kt |
|-----------|----|----|
| Ko'rsatilgan xizmatdan daromad | 4010 | 9030 |
| QQS hisoblandi | 9030 | 6410/1 |
| Xizmat tannarxi | 9130 | 2010 |
| To'lov tushdi | 5110 | 4010 |

## 4. Ish haqi (to'liq sxema)

| # | Operatsiya | Dt | Kt |
|---|-----------|----|----|
| 1 | Ish haqi hisoblandi (ishlab chiqarish xodimlari) | 2010 | 6710 |
| 2 | Ish haqi hisoblandi (ma'muriy xodimlar) | 9420 | 6710 |
| 3 | Ish haqi hisoblandi (savdo xodimlari) | 9410 | 6710 |
| 4 | JShDS ushlab qolindi | 6710 | 6410/4 |
| 5 | INPS ushlab qolindi | 6710 | 6520 |
| 6 | Ijtimoiy soliq hisoblandi (korxona hisobidan) | 2010 / 9410 / 9420 | 6510 |
| 7 | Ish haqi to'landi (qo'lga) | 6710 | 5110 / 5010 |
| 8 | JShDS byudjetga | 6410/4 | 5110 |
| 9 | INPS to'landi | 6520 | 5110 |
| 10 | Ijtimoiy soliq to'landi | 6510 | 5110 |

**Muhim:** JShDS va INPS — **xodim hisobidan** ushlab qolinadi (6710 ni kamaytiradi).
Ijtimoiy soliq — **korxona xarajati** (xodim ish haqidan ushlanmaydi). Bu ikkisini
aralashtirish eng ko'p uchraydigan xato.

## 5. Hisobdor shaxs (podotchyot / avans hisoboti)

| Operatsiya | Dt | Kt |
|-----------|----|----|
| Kartaga / kassadan pul berildi | 4410 | 5110 / 5010 |
| Avans hisoboti: material sotib olindi | 1010 / 1090 | 4410 |
| Avans hisoboti: xo'jalik xarajati | 9420 | 4410 |
| Avans hisoboti: safar xarajati | 9420 | 4410 |
| Sarflanmagan qoldiq qaytarildi | 5010 / 5110 | 4410 |
| Ortiqcha sarflangan summa xodimga qaytarildi | 4410 | 5010 / 5110 |

⚠️ Hisobdor shaxs chek/EHFsiz xarajat qilsa — xarajat soliq maqsadida chegirilmaydi va
jismoniy shaxs daromadi deb qaralishi mumkin. Har xarajatga birlamchi hujjat talab qiling.

## 6. Asosiy vosita

| Operatsiya | Dt | Kt |
|-----------|----|----|
| Sotib olindi (QQSsiz qiymat) | 0820 | 6010 |
| Kirim QQS | 4410⚠️ | 6010 |
| Yetkazish / o'rnatish xarajati qiymatga qo'shildi | 0820 | 6010 |
| Foydalanishga topshirildi | 0100 | 0820 |
| Oylik amortizatsiya hisoblandi | 2010 / 9410 / 9420 | 0200 |
| Sotilganda: qoldiq qiymat hisobdan chiqarildi | 9210 | 0100 |
| Sotilganda: to'plangan amortizatsiya | 0200 | 0100 |
| Sotuvdan tushum | 4010 | 9210 |

## 7. Ijara (ijarachi tomonida)

| Operatsiya | Dt | Kt |
|-----------|----|----|
| Oylik ijara hisoblandi (akt bo'yicha) | 9420 | 6010 |
| Ijara QQSi | 4410⚠️ | 6010 |
| To'landi | 6010 | 5110 |
| Bir yilga oldindan to'landi | 4510 → 3100 | 5110 |
| Kelgusi davr xarajatidan oylik hissa | 9420 | 3100 |

## 8. Kredit

| Operatsiya | Dt | Kt |
|-----------|----|----|
| Kredit olindi (qisqa muddatli) | 5110 | 6810 |
| Kredit olindi (uzoq muddatli) | 5110 | 7810 |
| Foiz hisoblandi | 9610 | 6920⚠️ / 6810 |
| Foiz to'landi | 6920⚠️ / 6810 | 5110 |
| Asosiy qarz to'landi | 6810 / 7810 | 5110 |
| Uzoq muddatlining joriy qismi o'tkazildi | 7810 | 6830 |

## 9. Yil oxiri yopilishi

| Operatsiya | Dt | Kt |
|-----------|----|----|
| Daromad schyotlari yopildi | 9010/9020/9030/9390/9510/9540 | 9910 |
| Xarajat schyotlari yopildi | 9910 | 9110/9120/9130/9410/9420/9430/9610/9690 |
| Foyda solig'i hisoblandi | 9810 | 6410/2 |
| Foyda solig'i xarajati yopildi | 9910 | 9810 |
| Sof foyda | 9910 | 8710 |
| Zarar | 8710 | 9910 |

## 10. Boshqa tez-tez uchraydigan operatsiyalar

| Operatsiya | Dt | Kt |
|-----------|----|----|
| Kanstovar sotib olindi | 1090 | 6010 |
| Kanstovar sarflandi | 9420 | 1090 |
| Yoqilg'i sotib olindi | 1030 | 6010 |
| Yoqilg'i hisobdan chiqarildi (putevoy list bo'yicha) | 9420 / 2010 | 1030 |
| Xaridordan jarima olindi | 4890 | 9390 |
| Soliq jarimasi hisoblandi | 9430 | 6410/9 |
| Undirib bo'lmaydigan qarz hisobdan chiqarildi | 9430 | 4010 |
| Muddati o'tgan kreditorlik qarzi daromadga o'tkazildi | 6010 | 9390 |
| Inventarizatsiyada ortiqcha topildi | 1010 / 2910 | 9390 |
| Inventarizatsiyada kamomad | 4610 / 9430 | 1010 / 2910 |
| Dividend hisoblandi | 8710 | 6610 |
| Dividenddan soliq ushlandi | 6610 | 6410⚠️ |
