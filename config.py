import asyncio
from random import randint
import os
import json
import random
from aiogram.enums import ContentType
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from db_interface import *


# PHASALO ON
try:
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())
    API_TOKEN: str = os.getenv('TOKEN')
    PASSWORD: str = os.getenv('PASSWORD')
    MAIN_ADMIN_ID: int = int(os.getenv('MAIN_ADMIN_ID'))
    BOT_ID: int = int(os.getenv('BOT_ID'))
except Exception:
    from API_TOKEN import *

try:
    bot: Bot = Bot(token=API_TOKEN, parse_mode='HTML')
except Exception:
    from aiogram.client.default import DefaultBotProperties

    bot: Bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
# PHASALO OFF

dp: Dispatcher = Dispatcher()

with open(f'{os.path.dirname(__file__)}/phrases.json', 'r', encoding="utf-8") as file:
    phrases: dict = json.load(file)


class Isban(BaseFilter):
    @staticmethod
    async def check(userid: int) -> bool:
        isban = check_user_ban_status(userid)
        return isban == 1

    async def __call__(self, message: Message) -> bool:
        return await self.check(message.from_user.id)


class Isadmin(BaseFilter):
    @staticmethod
    async def check(userid: int) -> bool:
        isadmin = check_user_admin_status(userid)
        return isadmin == 1 or Issuperadmin.check(userid)

    async def __call__(self, message: Message) -> bool:
        if message.chat.type != 'private':
            return False
        return await self.check(message.from_user.id)


class Issuperadmin(BaseFilter):
    @staticmethod
    async def check(userid) -> bool:
        return userid == MAIN_ADMIN_ID

    async def __call__(self, message: Message) -> bool:
        if message.chat.type != 'private':
            return False
        return await self.check(message.from_user.id)


async def default_msg(message: Message):
    await message.answer(
        phrases["default_answers"][randint(0, len(phrases["default_answers"]) - 1)])


async def ban_msg(message: Message):
    await message.answer(
        phrases["ban_answers"][randint(0, len(phrases["ban_answers"]) - 1)])


async def take_command_arguments(message: Message) -> list:
    return message.text.split()[1:] or [None]


async def check_command_to_id(message: Message) -> int:
    userid = await take_command_arguments(message)

    userid = userid[0]

    if userid is None:
        await message.answer(phrases['err_empty_argument'])
        return -1

    if not userid.isdigit():
        await message.answer(phrases['err_not_digit'])
        return -1

    userid = int(userid)

    if len(get_user_from_id(userid)) == 0:
        await message.answer(phrases['err_user_not_exist'])
        return -1

    return userid
