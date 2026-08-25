"""Bot uchun barcha reply/inline klaviaturalar shu yerda."""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from config import UC_PACKAGES

BTN_BUY = "🛒 UC sotib olish"
BTN_MY_ORDERS = "📦 Buyurtmalarim"
BTN_FAQ = "❓ FAQ"
BTN_CONTACT = "☎️ Aloqa"


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_BUY)],
            [KeyboardButton(text=BTN_MY_ORDERS), KeyboardButton(text=BTN_FAQ)],
            [KeyboardButton(text=BTN_CONTACT)],
        ],
        resize_keyboard=True,
    )


def uc_packages_kb() -> InlineKeyboardMarkup:
    rows = []
    for pkg in UC_PACKAGES:
        text = f"{pkg['amount']} UC — {pkg['price']:,} so'm".replace(",", " ")
        rows.append(
            [InlineKeyboardButton(text=text, callback_data=f"buy:{pkg['id']}")]
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚫 Bekor qilish", callback_data="cancel_order")]
        ]
    )


def admin_decision_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash", callback_data=f"approve:{order_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Rad etish", callback_data=f"reject:{order_id}"
                ),
            ]
        ]
    )
