import asyncio
import datetime
from os import listdir, remove
import re

from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import FSInputFile
from bs4 import BeautifulSoup as bs
import requests

from utils import keyboards

day_of_week = {
    0: "понедельник",
    1: "вторник",
    2: "среду",
    3: "четверг",
    4: "пятницу",
}

new_regex = r"\d{1,2}\_\d{1,2}\_\d{2,4}"
edit_regex = r"\d{1,2}\_\d{1,2}\_\d{2,4}\(+\d{1,3}\)+"


def read_ids():
    with open("files/ids.txt") as f:
        data = [i.split() for i in f.read().split("\n")]
    return data


def write_ids(ids):
    with open("files/ids.txt", mode="w") as f:
        f.write("\n".join([" ".join(i) for i in ids]))


def get_href(date_str):
    data = requests.get(
        "https://edu.tatar.ru/almet/page2042051.htm/page2221071.htm"
    )
    soup = bs(data.content, features="html.parser")
    href = soup.find_all("a", string=date_str)
    if href:
        return href[0].get("href")
    return None


def get_all_a():
    data = requests.get(
        "https://edu.tatar.ru/almet/page2042051.htm/page2221071.htm"
    )
    soup = bs(data.content, features="html.parser")
    divs = soup.find_all("div", class_="custom_wysiwyg")
    hrefs = []
    for div in divs:
        if div.find("div"):
            continue
        p_tags = div.find_all("p")
        if p_tags:
            for p in p_tags:
                a_tags = p.find_all("a")
                if a_tags:
                    for a in a_tags:
                        hrefs.append(a.get("href"))
    return hrefs


def get_date_text(date):
    if isinstance(date, str):
        date = date.split(".")
        return f"{int(date[0]):02}.{int(date[1]):02}.{date[2]}"
    return f"{date.day:02}.{date.month:02}.{date.year}"


def date_str_to_date(date_str: str):
    if re.match(edit_regex.replace("_", "."), date_str):
        date_str = date_str[:-3]
    date_str = date_str.split(".")
    return datetime.date(int(date_str[2]), int(date_str[1]), int(date_str[0]))


async def send_news_messages(date_str):
    from main import bot

    date = date_str_to_date(date_str)
    keyboard = keyboards.get_news_keyboard(date_str)
    ids = []
    for i in read_ids():
        if int(i[1]):
            try:
                await bot.send_message(
                    int(i[0]),
                    text=(
                        f"Вышло расписание на <b>"
                        f"{day_of_week[date.weekday()]}</b> ({date_str})"
                    ),
                    reply_markup=keyboard,
                )
                ids.append(i)
            except (TelegramForbiddenError, TelegramBadRequest):
                pass
        else:
            ids.append(i)
    write_ids(ids)


async def edit_file(name, href):
    date_str = get_date_text(name.replace("_", "."))
    files = listdir("files")
    just_date = date_str[:-3]
    if check_file_exists(just_date):
        for file in files:
            if re.match(just_date, file) and f"{date_str}.pdf" != file:
                remove(f"files/{file}")
                r = requests.get(f"https://edu.tatar.ru{href}")
                with open(f"files/{date_str}.pdf", "wb") as f:
                    f.write(r.content)
    else:
        r = requests.get(f"https://edu.tatar.ru{href}")
        with open(f"files/{date_str}.pdf", "wb") as f:
            f.write(r.content)
        await send_news_messages(date_str)


async def update_dates():
    while True:
        files = listdir("files")
        hrefs = get_all_a()
        for href in hrefs:
            reg = re.search(edit_regex, href)
            if reg:
                await edit_file(reg.group(), href)
            else:
                reg = re.search(new_regex, href)
                if reg:
                    date_str = get_date_text(reg.group().replace("_", "."))
                    if f"{date_str}.pdf" not in files:
                        r = requests.get(f"https://edu.tatar.ru{href}")
                        with open(f"files/{date_str}.pdf", "wb") as f:
                            f.write(r.content)
                        await send_news_messages(date_str)
                else:
                    print("regex dont find date, FINDERROR")
        print(datetime.datetime.now())
        await asyncio.sleep(600)


def get_file_by_date(date):
    if isinstance(date, str):
        date_str = date
    else:
        date_str = get_date_text(date)
    for file in listdir("files"):
        if re.match(re.escape(date_str), file):
            return FSInputFile(f"files/{file}")
    return None


def get_file_name_by_date(date):
    if isinstance(date, str):
        date_str = date
    else:
        date_str = get_date_text(date)
    for file in listdir("files"):
        if re.match(date_str, file):
            return file
    return None


def check_file_exists(date):
    if isinstance(date, str):
        date_str = date
    else:
        date_str = get_date_text(date)
    for i in listdir("files"):
        if re.match(date_str, i):
            return True
    return False
    # if f"{date_str}.pdf" in listdir("files"):
    # return True
    # return False


def get_weekday_form_date_str(date_str: str):
    date = date_str_to_date(date_str)
    return date.weekday()
