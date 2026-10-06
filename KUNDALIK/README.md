# KUNDALIK — kunlik bajarilganlik hisobi

Har kuni soat 22:30 (Asia/Tashkent) da Claude telefonga bildirishnoma yuboradi
va o'sha kungi kalendarga yozilgan **hamma narsa** bo'yicha so'raydi — 5 vaqt
namoz, ish, uchrashuv, dars, safar — nima bo'lsa hammasi. Javoblar shu
papkadagi `kundalik.csv` fayliga yozib boriladi.

> ⚠️ **Texnik cheklov:** avtomatik ishga tushadigan sessiyalarga konnektor
> (Google Calendar) kafolatlangan holda biriktirilmaydi. Eslatma **shu
> KUNDALIK suhbatining o'ziga** kelishi uchun sozlangan (avvalgi versiyada
> alohida yopiq sessiyaga kelardi va javoblar o'sha yerda ko'rinmay
> qolardi — endi tuzatildi). Shu suhbatda Calendar ulangan bo'lsa, savol
> kalendarni o'qib beradi; ulanmagan yoki mavjud bo'lmasa, oddiy so'rov
> rejimiga o'tadi — ikkala holatda ham ishlayveradi.

## Qanday yoziladi

Savol Claude orqali erkin matn ko'rinishida so'raladi, lekin **javobni
faylga yozish endi erkin ko'rsatmaga tayanmaydi** — bu avval ishlamay,
`kundalik.csv` oylab bo'sh qolib ketishiga sabab bo'lgan. Endi yozish
faqat bitta qat'iy skript orqali bo'ladi:

```bash
python3 KUNDALIK/kayd_qil.py 2026-09-13 "Bomdod:bajarildi" "Peshin:bajarilmadi"
```

Skript faylni yangilaydi, commit qiladi, GitHub'ga push qiladi va aniq
natija chiqaradi — muvaffaqiyat (`✅ N ta band yozildi`) yoki aniq xato
(`✖ XATO: ...`). Claude bu skriptni ishlatadi, uning ishini qo'lda
takrorlamaydi. Sinash uchun `--dry-run` bilan chaqirsa bo'ladi — u holda
hech narsa yozilmaydi va hech narsa commit qilinmaydi, faqat natija
ko'rsatiladi.

> 🔧 **2026-10-06 tuzatish:** skriptning oldingi versiyasida ikki xato bor
> edi — (1) fayl avval yozilib, keyin git repo yangilanardi, bu eski
> branch holati ustiga yozib yuborish xavfini tug'dirardi; (2) `--dry-run`
> baribir faylni diskka yozib qo'yardi, faqat git bosqichi o'tkazilardi.
> Ikkisi ham tuzatildi: endi git avval sinxronlanadi, fayl keyin yoziladi,
> va `--dry-run` hech qachon diskka tegmaydi.

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
ham so'raydi — Calendar ulangan bo'lsa ro'yxatni o'qib chiqadi, bo'lmasa
sizdan aytishingizni so'raydi.

## Reja yozish (vazifa/uchrashuvni kalendarga yozish)

Suhbatda erkin matn bilan reja aytsangiz ("13-oktyabrga soat 10:00ga
dentist yoz", "ertaga 18:00da do'stim bilan uchrashuv"), Claude buni shu
tartibda bajaradi:

1. Sana/soat/tavsifni matndan ajratib oladi (noaniq bo'lsa so'raydi).
2. O'sha kun/soatda kalendarda to'qnashuv bor-yo'qligini tekshiradi
   (`list_events`).
3. Google Calendar'ga hodisa yaratadi (`create_event`) — bu qadam FAQAT
   shu suhbat ichida bo'ladi, chunki Calendar ulanishi skriptga emas,
   shu sessiyaga tegishli (skriptda kalendar kredentiali yo'q va bo'lishi
   ham mumkin emas).
4. Shu rejani `KUNDALIK/rejalar.csv` fayliga qat'iy qayd qiladi:

```bash
python3 KUNDALIK/reja_qil.py 2026-10-13 10:00 "Dentist bilan uchrashuv" <calendar_event_id>
```

Bu skript ham `kayd_qil.py` bilan bir xil qat'iy mantiqqa ega — yoki
muvaffaqiyatli yozadi va push qiladi (`✅ Reja qayd qilindi: ...`), yoki
aniq xato bilan to'xtaydi (`✖ XATO: ...`). `--dry-run` bilan sinab
ko'rish mumkin — hech narsa yozilmaydi.

Demak: kalendarga yozishni Claude suhbat ichida qiladi, `reja_qil.py` esa
shu yozuvni `rejalar.csv` da ishonchli saqlaydi (tarix/audit uchun) —
ikkisi birga reja yozish botini hosil qiladi.

### `rejalar.csv` formati

```
sana,soat,tavsif,event_id,yozilgan_vaqt
2026-10-13,10:00,Dentist bilan uchrashuv,f7l4mnc1ud9fl31lutv5deo138,2026-10-06T12:00:00Z
```

Bu fayl — log (tarix), har bir qo'shilgan reja alohida qator, eskisi
o'chirilmaydi yoki ustiga yozilmaydi.

## Namoz vaqtlari

Namoz vaqtlari har hafta payshanba kuni soat 21:00 da shu suhbatning o'zida
so'raladi va Google Calendar'ga takrorlanuvchi hodisa sifatida yoziladi
("Namoz vaqtlarini yangilash (haftalik)" nomli Routine, shu KUNDALIK
suhbatiga bog'langan). Bu — kunlik hisobotdan mustaqil, alohida jarayon.
Javob berish shart emas — kechiksangiz ham, keyingi safar kirganingizda
davom ettirsangiz bo'ladi.

## Sozlamalarni o'zgartirish

Savol matni va yozish tartibi "KUNDALIK — kunlik hisobot (22:30)" nomli
Routine ichida yozilgan. O'zgartirish kerak bo'lsa, shuni ayting.
