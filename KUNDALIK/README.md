# KUNDALIK — kunlik bajarilganlik hisobi

Har kuni soat 22:30 (Asia/Tashkent) da Claude telefonga bildirishnoma yuboradi
va o'sha kungi rejalar bo'yicha savol beradi. Javoblar shu papkadagi
`kundalik.csv` fayliga yozib boriladi.

## Fayl formati

```
sana,vazifa,holat
2026-08-30,Bomdod,bajarildi
2026-08-30,Peshin,bajarilmadi
```

- `sana` — `YYYY-MM-DD`
- `vazifa` — reja nomi (emoji va "namozi" so'zisiz, qisqa)
- `holat` — faqat `bajarildi` yoki `bajarilmadi`

Javob berilmagan vazifa faylga **umuman yozilmaydi** — shunda statistika
"javob bermadim" va "bajarmadim" ni chalkashtirmaydi.

## Statistika

Istalgan suhbatda so'rasangiz kifoya: "bu hafta qanchasini bajardim?"
Hisob shu fayldan olinadi.

## Kunlik ro'yxatni o'zgartirish

So'raladigan vazifalar ro'yxati "KUNDALIK — kunlik hisobot (22:30)" nomli
Routine ichida yozilgan. Yangi doimiy reja qo'shmoqchi bo'lsangiz, shuni
ayting — ro'yxatga qo'shib qo'yaman.
