from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

from utils import callbacks
from utils.funcs import get_weekday_form_date_str

main_k = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Посмотреть расписание")],
        [KeyboardButton(text="Рассылка")],
    ],
    resize_keyboard=True,
)


main_admin_k = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Посмотреть расписание")],
        [KeyboardButton(text="Рассылка")],
        [
            KeyboardButton(text="Посмотреть колво пользователей"),
            KeyboardButton(text="Колво сообщений за день"),
        ],
    ],
    resize_keyboard=True,
)


date_k = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Завтра", callback_data="tomorrow")],
        [
            InlineKeyboardButton(
                text="Понедельник",
                callback_data=callbacks.WeekendCallback(n=0).pack(),
            ),
            InlineKeyboardButton(
                text="Вторник",
                callback_data=callbacks.WeekendCallback(n=1).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Среда",
                callback_data=callbacks.WeekendCallback(n=2).pack(),
            ),
            InlineKeyboardButton(
                text="Четверг",
                callback_data=callbacks.WeekendCallback(n=3).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Пятница",
                callback_data=callbacks.WeekendCallback(n=4).pack(),
            ),
        ],
    ]
)


def get_dates_keyboard(dates):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=date,
                    callback_data=callbacks.DateCallback(date=date).pack(),
                )
            ]
            for date in dates
        ]
        + [
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=callbacks.ReturnCallback(
                        to="main", n=-1
                    ).pack(),
                ),
            ],
        ],
    )
    return keyboard


def get_return_keyboard(date):
    n = get_weekday_form_date_str(date)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=callbacks.ReturnCallback(
                        to="dates", n=n
                    ).pack(),
                ),
            ],
        ],
    )
    return keyboard


def get_news_keyboard(date):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Посмотреть",
                    callback_data=callbacks.DateCallback(date=date).pack(),
                )
            ],
        ],
    )
    return keyboard


main_return_k = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data=callbacks.ReturnCallback(to="main", n=-1).pack(),
            )
        ]
    ]
)


def get_subscribe_keyboard(now: int = 1):
    if now:
        text = "Отменить подписку"
    else:
        text = "Подписаться на рассылку"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=callbacks.SubscribeCallback(now=now).pack(),
                )
            ],
        ],
    )
    return keyboard
