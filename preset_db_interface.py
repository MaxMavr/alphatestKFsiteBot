import sqlite3
import os
from typing import List, Tuple
PRESETS_DB = f'{os.path.dirname(__file__)}/DB/presets.db'

con = sqlite3.connect(PRESETS_DB)
cursor_presetsDB = con.cursor()
cursor_presetsDB.execute('''
    CREATE TABLE IF NOT EXISTS presets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        system TEXT NOT NULL DEFAULT 'system',
        device TEXT NOT NULL DEFAULT 'device',
        browser TEXT NOT NULL DEFAULT 'browser'
    )
''')
cursor_presetsDB.close()
con.close()


# Пресеты / presets
def add(user_id: int, system: str, device: str, browser: str):
    with sqlite3.connect(PRESETS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO presets (user_id, system, device, browser) '
            'VALUES (?, ?, ?, ?)',
            (user_id, system, device, browser)
        )
        db.commit()


def delete(preset_id: int):
    with sqlite3.connect(PRESETS_DB) as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM presets WHERE id = ?", (preset_id, ))
        db.commit()


def delete_from_user(user_id: int):
    with sqlite3.connect(PRESETS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            'DELETE FROM presets WHERE user_id = ?',
            (user_id,)
        )
        db.commit()


def get_from_user(user_id: int) -> List[Tuple]:
    with sqlite3.connect(PRESETS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM presets WHERE user_id = ?", (user_id,))
        return cursor.fetchall()


def get_from_id(preset_id: int) -> Tuple:
    with sqlite3.connect(PRESETS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT system, device, browser FROM presets WHERE id = ?", (preset_id,))
        return cursor.fetchone()
