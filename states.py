from aiogram.fsm.state import State, StatesGroup


class OrderFlow(StatesGroup):
    waiting_player_id = State()
    waiting_receipt = State()


class RejectFlow(StatesGroup):
    waiting_reason = State()
