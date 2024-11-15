from API_TOKEN import *

import os
from random import randint
from math import ceil

import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType

from init_config import phrases

import db_interfaces.bugs as bugs
import db_interfaces.presets as presets
import db_interfaces.users as users
import keyboards as kb


try:
    bot: Bot = Bot(token=API_TOKEN, parse_mode='HTML')
except TypeError:
    from aiogram.client.default import DefaultBotProperties

    bot: Bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))


class Preset(StatesGroup):
    system = State()
    device = State()
    browser = State()


class IsBaned(BaseFilter):
    @staticmethod
    async def check(user_id: int) -> bool:
        return users.is_baned(user_id)

    async def __call__(self, message: Message) -> bool:
        return await self.check(message.from_user.id)


class IsAdmin(BaseFilter):
    @staticmethod
    async def check(user_id: int) -> bool:
        return users.is_admin(user_id) or await IsSuperAdmin.check(user_id)

    async def __call__(self, message: Message) -> bool:
        if message.chat.type != 'private':
            return False
        return await self.check(message.from_user.id)


class IsSuperAdmin(BaseFilter):
    @staticmethod
    async def check(user_id) -> bool:
        return user_id == MAIN_ADMIN_ID

    async def __call__(self, message: Message) -> bool:
        if message.chat.type != 'private':
            return False
        return await self.check(message.from_user.id)


async def ban_message(message: Message):
    await message.answer(
        phrases["ban_answers"][randint(0, len(phrases["ban_answers"]) - 1)])


async def get_cmd_args(message: Message) -> list:
    return message.text.split()[1:] or [None]


async def get_cmd_digit(message: Message) -> int:
    number = await get_cmd_args(message)

    number = number[0]

    if number is None:
        await message.answer(phrases['err_empty_argument'])
        return -1

    if not number.isdigit():
        await message.answer(phrases['err_not_digit'])
        return -1

    return int(number)


async def get_cmd_user_id(message: Message) -> int:
    user_id = await get_cmd_digit(message)

    if user_id == -1:
        return -1

    if not users.is_exists(user_id):
        await message.answer(phrases['err_user_not_exist'])
        return -1

    return user_id


async def get_cmd_bug_id(message: Message) -> int:
    message_id = await get_cmd_digit(message)

    if message_id == -1:
        return -1

    if not bugs.is_exists(message_id):
        await message.answer(phrases['err_bug_not_exist'])
        return -1

    return message_id
