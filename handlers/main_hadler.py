import datetime

from aiogram import F
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile
from aiogram.types import Message

from middlewares.messages_counter import return_message_count
from utils import callbacks
from utils import keyboards
from utils.filters import AdminFilter
from utils.funcs import check_file_exists, get_file_name_by_date
from utils.funcs import get_date_text
from utils.funcs import get_file_by_date
from utils.funcs import read_ids
from utils.funcs import write_ids
from utils.funcs import get_cafe_menu

router = Router()


@router.message(F.text == "Расписание")
async def main_table(message: Message):
    return await message.answer(
        "Выберите день недели", reply_markup=keyboards.date_k
    )


@router.message(F.text == "Меню в столовой")
async def cafe_handler(message: Message):
    file = get_cafe_menu()
    if file:
        await message.answer("Меню на сегодня:")
        await message.answer_document(file)
    else:
        await message.answer("На сегодня нет меню, пока что")



@router.message(F.text == "Рассылка")
async def distribution_subscribe(message: Message):
    ids = read_ids()
    for i in ids:
        if int(i[0]) == message.from_user.id:
            keyboard = keyboards.get_subscribe_keyboard(int(i[1]))
            break
    if int(i[1]):
        text = "✅ Рассылка подключена"
    else:
        text = "❌ Рассылка отключена"
    photo = FSInputFile("files/subscribe.png")
    return await message.answer_photo(
        photo,
        "При выходе нового расписания данный бот отправляет рассылку.\n"
        + text,
        reply_markup=keyboard,
    )


@router.callback_query(callbacks.SubscribeCallback.filter(F.now > -1))
async def change_subscribe(
    callback_query: CallbackQuery, callback_data: callbacks.SubscribeCallback
):
    ids = read_ids()
    for i in ids:
        if int(i[0]) == callback_query.from_user.id:
            i[1] = str((int(i[1]) + 1) % 2)
            break
    write_ids(ids)
    if int(i[1]):
        text = "✅ Рассылка подключена"
    else:
        text = "❌ Рассылка отключена"
    keyboard = keyboards.get_subscribe_keyboard(int(i[1]))
    await callback_query.message.edit_caption(
        inline_message_id=callback_query.inline_message_id,
        caption="При выходе нового расписания данный бот отправляет рассылку\n"
        + text,
        reply_markup=keyboard,
    )


@router.callback_query(callbacks.WeekendCallback.filter(F.n > -1))
async def week(
    callback_query: CallbackQuery, callback_data: callbacks.WeekendCallback
):
    today = datetime.date.today()
    dates = []
    for i in range(-7 - today.weekday(), 8):
        some_date = today + datetime.timedelta(days=i)
        if some_date.weekday() == callback_data.n and check_file_exists(
            some_date
        ):
            file_date = get_file_name_by_date(some_date)
            dates.append(get_date_text(file_date))
    keyboard = keyboards.get_dates_keyboard(dates)
    await callback_query.message.answer(
        "Выберите дату:", reply_markup=keyboard
    )
    await callback_query.message.delete()


@router.callback_query(callbacks.DateCallback.filter(F.date.len() > 0))
async def date(
    callback_query: CallbackQuery, callback_data: callbacks.DateCallback
):
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
    ids_count = len(read_ids())
    return message.answer(f"Кол-во пользователей: <b>{ids_count}</b>")


@router.message(AdminFilter("Колво сообщений за день"))
async def messages_for_day(message: Message):
    return message.answer(
        f"Кол-во сообщений за день: <b>{return_message_count()}</b>"
    )


@router.message(AdminFilter("Рассылка: "))
async def distribution(message: Message):
    from main import bot

    text = message.text.split(": ")[1]
    for i in read_ids():
        if int(i[1]):
            await bot.send_message(int(i[0]), text, reply_markup=keyboards.main_k)


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
    return await message.answer(
        (
            "Этот бот предназначен для просмотра расписания АТЭТ. "
            "Для навигации используйте кнопки, пожалуйста"
        ),
        reply_markup=keyboards.main_k,
    )
