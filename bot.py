"""
FENIKS UC SERVICE — PUBG Mobile uchun UC sotib olish Telegram boti.

Oqim:
  1. Mijoz "UC sotib olish" tugmasini bosadi va paket tanlaydi.
  2. PUBG Mobile ID raqamini yuboradi.
  3. Botning karta raqamiga to'lov qiladi va to'lov chekini (skrinshot) yuboradi.
  4. Buyurtma "kutilmoqda" holatida saqlanadi va chek admin(lar)ga forward qilinadi.
  5. Admin ✅ Tasdiqlash / ❌ Rad etish tugmasini bosadi — mijozga avtomatik xabar boradi.
  6. Mijoz "Buyurtmalarim" bo'limidan barcha buyurtmalari holatini ko'rishi mumkin.

Ishga tushirish: README.md ga qarang.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import database as db
from config import (
    ADMIN_IDS,
    BOT_TOKEN,
    CARD_HOLDER,
    CARD_NUMBER,
    CONTACT_USERNAME,
    FAQ_TEXT,
    UC_PACKAGES,
)
from keyboards import (
    BTN_BUY,
    BTN_CONTACT,
    BTN_FAQ,
    BTN_MY_ORDERS,
    admin_decision_kb,
    cancel_kb,
    main_menu,
    uc_packages_kb,
)
from states import OrderFlow, RejectFlow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dp = Dispatcher()

PACKAGES_BY_ID = {pkg["id"]: pkg for pkg in UC_PACKAGES}


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# ---------------------------------------------------------------- /start ---
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "👋 Assalomu alaykum, <b>FENIKS UC SERVICE</b> botiga xush kelibsiz!\n\n"
        "Bu yerda siz <b>PUBG MOBILE</b> uchun UC ni tez va ishonchli tarzda "
        "sotib olishingiz mumkin.\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang 👇",
        reply_markup=main_menu(),
    )


# --------------------------------------------------------- UC sotib olish ---
@dp.message(F.text == BTN_BUY)
async def buy_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "📦 Kerakli UC paketini tanlang:", reply_markup=uc_packages_kb()
    )


@dp.callback_query(F.data.startswith("buy:"))
async def buy_package_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    pkg_id = callback.data.split(":", 1)[1]
    pkg = PACKAGES_BY_ID.get(pkg_id)
    if not pkg:
        await callback.answer("Bu paket topilmadi, qayta urinib ko'ring.", show_alert=True)
        return

    await state.update_data(uc_amount=pkg["amount"], price=pkg["price"])
    await state.set_state(OrderFlow.waiting_player_id)

    await callback.message.edit_text(
        f"✅ Siz tanladingiz: <b>{pkg['amount']} UC — {pkg['price']:,} so'm</b>".replace(",", " ")
    )
    await callback.message.answer(
        "🆔 Endi <b>PUBG Mobile ID</b> raqamingizni yuboring.\n\n"
        "ID raqamingizni o'yin ichida profil bo'limidan topishingiz mumkin.",
        reply_markup=cancel_kb(),
    )
    await callback.answer()


@dp.message(OrderFlow.waiting_player_id)
async def receive_player_id(message: Message, state: FSMContext) -> None:
    player_id = (message.text or "").strip()
    if not player_id or not player_id.isdigit() or len(player_id) < 5:
        await message.answer(
            "⚠️ Iltimos, to'g'ri PUBG Mobile ID raqamini yuboring (faqat raqamlardan iborat)."
        )
        return

    data = await state.update_data(player_id=player_id)
    price = data["price"]

    await state.set_state(OrderFlow.waiting_receipt)
    await message.answer(
        "💳 To'lovni quyidagi karta raqamiga amalga oshiring:\n\n"
        f"<code>{CARD_NUMBER}</code>\n"
        f"{CARD_HOLDER}\n\n"
        f"💵 To'lov summasi: <b>{price:,} so'm</b>\n\n".replace(",", " ")
        + "📸 To'lovni amalga oshirgach, <b>chek (skrinshot) rasmini</b> shu yerga yuboring.",
        reply_markup=cancel_kb(),
    )


@dp.message(OrderFlow.waiting_receipt, F.photo)
async def receive_receipt(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    player_id = data["player_id"]
    uc_amount = data["uc_amount"]
    price = data["price"]

    order_id = db.create_order(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        player_id=player_id,
        uc_amount=uc_amount,
        price=price,
    )

    file_id = message.photo[-1].file_id
    db.attach_receipt(order_id, file_id)

    await state.clear()
    await message.answer(
        f"✅ Buyurtmangiz qabul qilindi! Buyurtma raqami: <b>#{order_id}</b>\n\n"
        "Chekingiz tekshirilmoqda, tez orada tasdiqlanadi. Holatini "
        f"«{BTN_MY_ORDERS}» bo'limidan kuzatib borishingiz mumkin.",
        reply_markup=main_menu(),
    )

    caption = (
        f"🆕 <b>Yangi buyurtma #{order_id}</b>\n\n"
        f"👤 Mijoz: {message.from_user.full_name} "
        f"(@{message.from_user.username or '—'}, ID: {message.from_user.id})\n"
        f"🎮 PUBG ID: <code>{player_id}</code>\n"
        f"💎 UC: {uc_amount}\n"
        f"💵 Narx: {price:,} so'm".replace(",", " ")
    )

    for admin_id in ADMIN_IDS:
        try:
            sent = await bot.send_photo(
                admin_id,
                photo=file_id,
                caption=caption,
                reply_markup=admin_decision_kb(order_id),
            )
            db.set_admin_message_id(order_id, sent.message_id)
        except Exception:
            logger.exception("Adminga (%s) xabar yuborib bo'lmadi", admin_id)


@dp.message(OrderFlow.waiting_receipt)
async def receipt_wrong_type(message: Message) -> None:
    await message.answer("⚠️ Iltimos, to'lov chekining <b>rasmini (screenshot)</b> yuboring.")


@dp.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer("🚫 Buyurtma bekor qilindi.", reply_markup=main_menu())
    await callback.answer()


# ---------------------------------------------------------- Buyurtmalarim ---
@dp.message(F.text == BTN_MY_ORDERS)
async def my_orders(message: Message) -> None:
    orders = db.get_user_orders(message.from_user.id)
    if not orders:
        await message.answer("Sizda hali buyurtmalar yo'q.")
        return

    lines = ["📦 <b>Sizning buyurtmalaringiz:</b>\n"]
    for o in orders:
        status_label = db.STATUS_LABELS.get(o["status"], o["status"])
        lines.append(
            f"#{o['id']} — {o['uc_amount']} UC — {o['price']:,} so'm — {status_label}".replace(",", " ")
        )
    await message.answer("\n".join(lines))


# ------------------------------------------------------------------- FAQ ---
@dp.message(F.text == BTN_FAQ)
async def faq(message: Message) -> None:
    await message.answer(FAQ_TEXT)


# --------------------------------------------------------------- Aloqa -----
@dp.message(F.text == BTN_CONTACT)
async def contact(message: Message) -> None:
    await message.answer(
        f"☎️ Savol yoki muammolar bo'yicha: {CONTACT_USERNAME}"
    )


# ------------------------------------------------------ Admin: tasdiqlash ---
@dp.callback_query(F.data.startswith("approve:"))
async def admin_approve(callback: CallbackQuery, bot: Bot) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("Sizda ruxsat yo'q.", show_alert=True)
        return

    order_id = int(callback.data.split(":", 1)[1])
    order = db.get_order(order_id)
    if not order:
        await callback.answer("Buyurtma topilmadi.", show_alert=True)
        return

    db.update_status(order_id, db.STATUS_APPROVED)
    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n✅ <b>TASDIQLANDI</b>",
        reply_markup=None,
    )
    await callback.answer("Tasdiqlandi ✅")

    try:
        await bot.send_message(
            order["user_id"],
            f"✅ Buyurtmangiz #{order_id} tasdiqlandi!\n"
            f"💎 {order['uc_amount']} UC tez orada PUBG ID {order['player_id']} "
            "hisobiga tushadi. Xarid uchun rahmat!",
        )
    except Exception:
        logger.exception("Mijozga (%s) xabar yuborib bo'lmadi", order["user_id"])


# --------------------------------------------------------- Admin: rad etish ---
@dp.callback_query(F.data.startswith("reject:"))
async def admin_reject(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("Sizda ruxsat yo'q.", show_alert=True)
        return

    order_id = int(callback.data.split(":", 1)[1])
    order = db.get_order(order_id)
    if not order:
        await callback.answer("Buyurtma topilmadi.", show_alert=True)
        return

    await state.set_state(RejectFlow.waiting_reason)
    await state.update_data(reject_order_id=order_id)
    await callback.message.answer(
        f"❌ Buyurtma #{order_id} uchun rad etish sababini yozing "
        "(mijozga shu matn yuboriladi):"
    )
    await callback.answer()


@dp.message(RejectFlow.waiting_reason)
async def admin_reject_reason(message: Message, state: FSMContext, bot: Bot) -> None:
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    order_id = data.get("reject_order_id")
    order = db.get_order(order_id)
    await state.clear()

    if not order:
        await message.answer("Buyurtma topilmadi.")
        return

    reason = message.text or "Sabab ko'rsatilmagan"
    db.update_status(order_id, db.STATUS_REJECTED)
    await message.answer(f"❌ Buyurtma #{order_id} rad etildi.")

    try:
        await bot.send_message(
            order["user_id"],
            f"❌ Buyurtmangiz #{order_id} rad etildi.\n"
            f"Sabab: {reason}\n\n"
            f"Savollar bo'yicha: {CONTACT_USERNAME}",
        )
    except Exception:
        logger.exception("Mijozga (%s) xabar yuborib bo'lmadi", order["user_id"])


# ---------------------------------------------------------------- Admin ----
@dp.message(Command("stats"))
async def admin_stats(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        "📊 Statistika bo'limi keyingi versiyada qo'shiladi.\n"
        "Hozircha barcha buyurtmalarni orders.db faylida ko'rishingiz mumkin."
    )


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN topilmadi. .env faylini yarating va BOT_TOKEN ni kiriting "
            "(namuna uchun .env.example ga qarang)."
        )
    if not ADMIN_IDS:
        logger.warning(
            "ADMIN_IDS bo'sh — buyurtmalar haqida hech kimga xabar bormaydi!"
        )

    db.init_db()

    bot = Bot(token=BOT_TOKEN, default=_default_bot_properties())
    await dp.start_polling(bot)


def _default_bot_properties():
    from aiogram.client.default import DefaultBotProperties

    return DefaultBotProperties(parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    asyncio.run(main())
