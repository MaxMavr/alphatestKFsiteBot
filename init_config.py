import json
from math import ceil

import sqlite3
import os
from typing import List, Tuple
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

BUGS_DB = f'{os.path.dirname(__file__)}/DB/bugs.db'
PRESETS_DB = f'{os.path.dirname(__file__)}/DB/presets.db'
USERS_DB = f'{os.path.dirname(__file__)}/DB/users.db'

with open(f'{os.path.dirname(__file__)}/phrases.json', 'r', encoding="utf-8") as file:
    phrases: dict = json.load(file)
