import asyncio
import os
from random import randint
import json
from aiogram.enums import ContentType
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from db_interface import *
from aiogram.fsm.state import State, StatesGroup
import keyboards as kb

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


class Preset(StatesGroup):
    system = State()
    device = State()
    browser = State()


class Isban(BaseFilter):
    @staticmethod
    async def check(user_id: int) -> bool:
        is_ban = check_user_ban_status(user_id)
        return is_ban == 1

    async def __call__(self, message: Message) -> bool:
        return await self.check(message.from_user.id)


class Isadmin(BaseFilter):
    @staticmethod
    async def check(user_id: int) -> bool:
        is_admin = check_user_admin_status(user_id)
        return is_admin == 1 or Issuperadmin.check(user_id)

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


async def ban_msg(message: Message):
    await message.answer(
        phrases["ban_answers"][randint(0, len(phrases["ban_answers"]) - 1)])


async def get_cmd_args(message: Message) -> list:
    return message.text.split()[1:] or [None]


async def get_cmd_id(message: Message) -> int:
    userid = await get_cmd_args(message)

    userid = userid[0]

    if userid is None:
        await message.answer(phrases['err_empty_argument'])
        return -1

    if not userid.isdigit():
        await message.answer(phrases['err_not_digit'])
        return -1

    userid = int(userid)

    if not is_user_exists(userid):
        await message.answer(phrases['err_user_not_exist'])
        return -1

    return userid
