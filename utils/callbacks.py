from aiogram.filters.callback_data import CallbackData


class WeekendCallback(CallbackData, prefix="week"):
    n: int


class DateCallback(CallbackData, prefix="date"):
    date: str


class ReturnCallback(CallbackData, prefix="return"):
    to: str
    n: int
