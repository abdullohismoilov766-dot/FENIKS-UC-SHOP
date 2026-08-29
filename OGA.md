# OGA — buxgalteriya bo'yicha mutaxassis yordamchi

OGA — O'zbekiston buxgalteriya hisobi (NSBU) va Soliq kodeksi doirasida ishlaydigan
yordamchi. U quyidagilarda yordam beradi:

- **Bank vipiskasi** — har bir to'lovni qaysi schyotga (Dt/Kt) qo'yishni aniqlaydi
- **Schet-faktura (EHF/ЭСФ)** — Didox / my.soliq.uz orqali xatosiz yuborish uchun
  14 punktli tekshiruv, MXIK (IKPU) kodlari, xatoni tuzatish tartibi
- **Soliqlar** — stavkalar, hisoblash bazasi, provodkalar, deklaratsiya muddatlari
- **1C bazalari** — eski (7.7) va yangi (8.x), qoldiqlarni ko'chirish, oy yopilishi
- **Venkon bazasi** — 1C:Korxona 8 platformasidagi konfiguratsiya; **clobus.uz**
  orqali bulutli kirish, EHF ni bazadan Didox orqali yuborish, EDO nosozliklari

## Qanday ishlatiladi

Claude Code ichida ikki xil chaqirish mumkin:

```
/oga  bu vipiskani provodkaga tushirib ber
```

yoki oddiy savol — OGA avtomatik ishga tushadi:

```
"Bank komissiyasini qaysi schyotga yozay?"
"Didoxdan faktura yubordim, MXIK kodi noto'g'ri ketibdi — nima qilay?"
"Ish haqidan qancha soliq ushlanadi?"
```

Alohida agent sifatida ham chaqirish mumkin: `oga` (`.claude/agents/oga.md`).

## Fayllar

```
.claude/agents/oga.md                      — agent ta'rifi
.claude/skills/oga/
├── SKILL.md                               — ish tartibi, javob shakli, qoidalar
├── references/
│   ├── 01-schetlar-rejasi.md              — NSBU schyotlar rejasi
│   ├── 02-bank-vipiska.md                 — vipiskani provodkaga o'girish
│   ├── 03-tipovoy-provodkalar.md          — tipik operatsiyalar provodkalari
│   ├── 04-schet-faktura.md                — EHF: rekvizitlar, tekshiruv, tuzatish
│   ├── 05-soliqlar.md                     — soliqlar, stavkalar, muddatlar
│   ├── 06-1c-bazalar.md                   — 1C 7.7 va 8.x, ko'chirish, muammolar
│   ├── 07-venkon-baza.md                  — Venkon + clobus.uz bulut, EDO/Didox
│   └── 08-manbalar.md                     — rus tilidagi manbalar, atamalar lug'ati
└── memory/
    ├── XOTIRA.md                          — korxonaning doimiy ma'lumotlari
    └── QARORLAR-JURNALI.md                — qabul qilingan qarorlar tarixi
```

## Birinchi ishga tushirishda

OGA to'liq kuchga kirishi uchun **ikkita fayl to'ldirilishi kerak**:

1. **`.claude/skills/oga/memory/XOTIRA.md`** — korxona STIRi, soliq rejimi, bank
   rekvizitlari, ish schyotlar rejasi (6410 subschyotlari, kirim QQS schyoti, bank
   komissiyasi schyoti), doimiy kontragentlar, 1C versiyasi.
   Buni qo'lda to'ldirsangiz ham bo'ladi, OGA ga aytib bersangiz ham — u o'zi yozadi.

2. **`.claude/skills/oga/references/07-venkon-baza.md`** — Venkon bo'limining oxiridagi
   ro'yxat: qaysi mahsulot va tahrir, bulutli yoki lokal, EHF qayerdan yuboriladi,
   eski baza qaysi edi. Javob bersangiz OGA aniq javob beradi.

## Bilim bazasi qayerdan yig'ilgan

Ma'lumotlar asosan **rus tilidagi** O'zbekiston manbalaridan (lex.uz, buxgalter.uz,
bss.uz, norma.uz, legalise.uz, spot.uz) olinib, **o'zbek tiliga o'girilgan**. Manbalar
ro'yxati va o'zbekcha↔ruscha atamalar lug'ati — `references/08-manbalar.md`.

Tasdiqlangan ma'lumot `✅`, tekshirilishi kerak bo'lgani `⚠️` bilan belgilangan.

> 🔴 **2025-yil 1-yanvardan yangi NSBU № 21 schyotlar rejasi amal qiladi**
> (191-son buyruq 14.11.2024, AV 3593-son 27.12.2024). Eski reja (1181-son, 23.10.2002)
> kuchini yo'qotgan — eski va yangi bazadagi schyotlar farq qilishi mumkin.

## Muhim ogohlantirish

Soliq stavkalari va hisobot muddatlari **har yili o'zgaradi**. OGA javobidagi har
qanday raqam — boshlang'ich yo'nalish, yakuniy hujjat emas. Muhim qarordan oldin
[lex.uz](https://lex.uz) va [my.soliq.uz](https://my.soliq.uz) dan amaldagi tahrirni
tasdiqlang. Yakuniy javobgarlik buxgalter va korxona rahbarida.
