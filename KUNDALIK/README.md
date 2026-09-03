# KUNDALIK — kunlik bajarilganlik hisobi

Har kuni soat 22:30 (Asia/Tashkent) da Claude telefonga bildirishnoma yuboradi
va o'sha kungi kalendarga yozilgan **hamma narsa** bo'yicha so'raydi — 5 vaqt
namoz, ish, uchrashuv, dars, safar — nima bo'lsa hammasi. Javoblar shu
papkadagi `kundalik.csv` fayliga yozib boriladi.

> ⚠️ **Texnik cheklov:** 22:30 dagi so'rov sessiyasi Google Calendar'ga
> to'g'ridan-to'g'ri kira olmaydi (avtomatik ishga tushadigan sessiyalarga
> konnektor biriktirilmaydi). Shuning uchun kalendarni o'zi o'qib
> tekshirolmaydi — foydalanuvchidan so'rab, aytganini yozib boradi.

## Fayl formati

```
sana,vazifa,holat
2026-09-03,Bomdod,bajarildi
2026-09-03,Peshin,bajarilmadi
2026-09-03,Ish,bajarildi
2026-09-03,Dars,bajarilmadi
```

- `sana` — `YYYY-MM-DD`
- `vazifa` — reja nomi (emoji va "namozi" so'zisiz, qisqa)
- `holat` — faqat `bajarildi` yoki `bajarilmadi`

Javob berilmagan vazifa faylga **umuman yozilmaydi** — shunda statistika
"javob bermadim" va "bajarmadim" ni chalkashtirmaydi.

## Statistika

Istalgan suhbatda so'rasangiz kifoya: "bu hafta qanchasini bajardim?"
Hisob shu fayldan olinadi.

## Nima so'raladi

Har kuni 5 vaqt namoz doimiy so'raladi. Bulardan tashqari, o'sha kuni
kalendaringizga yozgan boshqa har qanday ish/uchrashuv/reja bo'lsa, ularni
ham aytishingiz so'raladi — ro'yxat qattiq belgilanmagan, chunki bot
kalendarni o'zi o'qiy olmaydi (yuqoridagi cheklovga qarang).

## Namoz vaqtlari

Namoz vaqtlari har hafta payshanba kuni soat 21:00 da alohida so'raladi va
Google Calendar'ga takrorlanuvchi hodisa sifatida yoziladi ("Namoz
vaqtlarini yangilash (haftalik)" nomli Routine). Bu — kunlik hisobotdan
mustaqil, alohida jarayon.

## Sozlamalarni o'zgartirish

Savol matni va yozish tartibi "KUNDALIK — kunlik hisobot (22:30)" nomli
Routine ichida yozilgan. O'zgartirish kerak bo'lsa, shuni ayting.
