import datetime

from aiogram import F
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.types import Message

from utils import callbacks
from utils import keyboards
from utils.filters import AdminFilter
from utils.funcs import check_file_exists
from utils.funcs import get_date_text
from utils.funcs import get_file_by_date

last_date = datetime.date.today()
messages_count = 0


def count_message():
    global last_date, messages_count
    date = datetime.date.today()
    if date != last_date:
        last_date = date
        messages_count = 0
        print(1)
    messages_count += 1


router = Router()


@router.message(F.text == "Посмотреть расписание")
async def main_table(message: Message):
    count_message()
    return await message.answer(
        "Выберите день недели", reply_markup=keyboards.date_k
    )


@router.callback_query(callbacks.WeekendCallback.filter(F.n > -1))
async def week(
    callback_query: CallbackQuery, callback_data: callbacks.WeekendCallback
):
    count_message()
    today = datetime.date.today()
    dates = []
    for i in range(-7 - today.weekday(), 8):
        some_date = today + datetime.timedelta(days=i)
        if some_date.weekday() == callback_data.n and check_file_exists(
            some_date
        ):
            dates.append(get_date_text(some_date))
    keyboard = keyboards.get_dates_keyboard(dates)
    await callback_query.message.answer(
        "Выберите дату:", reply_markup=keyboard
    )
    await callback_query.message.delete()


@router.callback_query(callbacks.DateCallback.filter(F.date.len() > 0))
async def date(
    callback_query: CallbackQuery, callback_data: callbacks.DateCallback
):
    count_message()
    file = get_file_by_date(callback_data.date)
    keyboard = keyboards.get_return_keyboard(callback_data.date)
    await callback_query.message.answer_document(file, reply_markup=keyboard)
    await callback_query.message.delete()


@router.callback_query(callbacks.ReturnCallback.filter(F.to == "main"))
async def return_to_main(
    callback_query: CallbackQuery, callback_data: callbacks.ReturnCallback
):
    await main_table(callback_query.message)
    await callback_query.message.delete()


@router.callback_query(callbacks.ReturnCallback.filter(F.to == "dates"))
async def return_to_dates(
    callback_query: CallbackQuery, callback_data: callbacks.ReturnCallback
):
    await week(
        callback_query,
        callback_data=callbacks.WeekendCallback(n=callback_data.n),
    )


@router.callback_query(F.data == "tomorrow")
async def tomorrow(callback_query: CallbackQuery):
    count_message()
    date = datetime.date.today() + datetime.timedelta(days=1)
    file = get_file_by_date(date)
    if file:
        await callback_query.message.answer_document(
            file, reply_markup=keyboards.main_return_k
        )
    elif date.weekday() in (5, 6):
        await callback_query.message.answer(
            "Завтра нет пар - выходной. Поздравляю)",
            reply_markup=keyboards.main_return_k,
        )
    else:
        await callback_query.message.answer(
            "На завтра ещё нет расписания (",
            reply_markup=keyboards.main_return_k,
        )
    return await callback_query.message.delete()


@router.message(AdminFilter("Посмотреть колво пользователей"))
async def users(message: Message):
    count_message()
    with open("files/ids.txt", mode="r") as f:
        ids_count = len(f.read().split(","))
    return message.answer(f"Кол-во пользователей: <b>{ids_count}</b>")


@router.message(AdminFilter("Колво сообщений за день"))
async def messages_for_day(message: Message):
    global messages_count
    return message.answer(f"Кол-во сообщений за день: <b>{messages_count}</b>")


@router.message()
async def main_start(message: Message):
    if message.from_user.id == 1047809355:
        return await message.answer(
            (
                "Этот бот предназначен для просмотра расписания АТЭТ. "
                "Для навигации используйте кнопки, пожалуйста"
            ),
            reply_markup=keyboards.main_admin_k,
        )
    with open("files/ids.txt", mode="r") as f:
        data = f.read().split(",")
        if str(message.from_user.id) not in data:
            data.append(str(message.from_user.id))
            with open("files/ids.txt", mode="w") as f2:
                f2.write(",".join(data))
    return await message.answer(
        (
            "Этот бот предназначен для просмотра расписания АТЭТ. "
            "Для навигации используйте кнопки, пожалуйста"
        ),
        reply_markup=keyboards.main_k,
    )
