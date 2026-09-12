"""FSM holatlari — reja qo'shish va sozlamalarni tahrirlash bosqichlari."""

from aiogram.fsm.state import State, StatesGroup


class AddTask(StatesGroup):
    waiting_title = State()
    waiting_range = State()
    waiting_repeat = State()


class Settings(StatesGroup):
    waiting_timezone = State()
    waiting_day_window = State()


class Confirm(StatesGroup):
    """Claude tushungan, lekin foydalanuvchi tasdiqlashi kutilayotgan holat."""

    waiting_decision = State()
