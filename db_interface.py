import sqlite3
import os
from typing import List, Tuple

USERS_DB = f'{os.path.dirname(__file__)}/DB/users.db'
BUGS_DB = f'{os.path.dirname(__file__)}/DB/bugs.db'
PRESETS_DB = f'{os.path.dirname(__file__)}/DB/presets.db'

con = sqlite3.connect(USERS_DB)
cursor_usersDB = con.cursor()
cursor_usersDB.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL DEFAULT 'username',
        isadmin INTEGER CHECK (isadmin IN (0, 1)) NOT NULL DEFAULT 0,
        isban INTEGER CHECK (isban IN (0, 1)) NOT NULL DEFAULT 0
    )
''')
cursor_usersDB.close()
con.close()

con = sqlite3.connect(BUGS_DB)
cursor_bugsDB = con.cursor()
cursor_bugsDB.execute('''
    CREATE TABLE IF NOT EXISTS bugs (
        user_id INTEGER NOT NULL,
        message_id INTEGER NOT NULL,
        preset_id INTEGER NOT NULL,
        description TEXT NOT NULL DEFAULT 'description',
        isfixed INTEGER CHECK (isfixed IN (0, 1)) NOT NULL DEFAULT 0
    )
''')
cursor_bugsDB.close()
con.close()

con = sqlite3.connect(PRESETS_DB)
cursor_presetsDB = con.cursor()
cursor_presetsDB.execute('''
    CREATE TABLE IF NOT EXISTS presets (
        id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        system TEXT NOT NULL DEFAULT 'system',
        device TEXT NOT NULL DEFAULT 'device',
        browser TEXT NOT NULL DEFAULT 'browser'
    )
''')
cursor_presetsDB.close()
con.close()


def invert(value):
    return 1 - value


# Баги / bugs
def fetch_bugs_count() -> Tuple[int, int]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM bugs")
        all_bugs = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bugs WHERE isfixed = 1")
        fix_bugs = cursor.fetchone()[0]
        return fix_bugs, all_bugs


def get_bugs_count_from_user(user_id: int) -> int:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM bugs WHERE user_id = ?", (user_id,))
        return cursor.fetchone()[0]


def get_all_bugs() -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs ORDER BY isfixed ASC")
        return cursor.fetchall()


def get_nonfix_bugs() -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs WHERE isfixed = 0")
        return cursor.fetchall()


def get_bugs_from_user(user_id: int) -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs WHERE user_id = ?", (user_id,))
        return cursor.fetchall()


def get_bug_from_id(bug_id: int) -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs WHERE message_id = ?", (bug_id,))
        return cursor.fetchall()


def add_bug(id: int, user_id: int, preset_id: int, description: str):
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO bugs (user_id, message_id, preset_id, description)VALUES (?, ?, ?, ?)',
            (user_id, id, preset_id, description)
        )
        db.commit()


def upd_bug_fix_status(bug_id: int):
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT isfixed FROM bugs WHERE message_id = ?", (bug_id,))
        isfixed = invert(cursor.fetchone()[0][0])
        cursor.execute(
            "UPDATE bugs SET isfixed = ? WHERE message_id = ?",
            (isfixed, bug_id)
        )
        db.commit()


# Пользователи / users
def add_user(user_id: int, username: str):
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE id = ?", (user_id,))
        if cursor.fetchone()[0] > 0:
            return

        cursor.execute('INSERT INTO users (id, username) VALUES (?, ?)', (user_id, username))
        db.commit()


def get_all_users() -> List[Tuple]:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users ORDER BY isadmin')
        return cursor.fetchall()


def get_all_admins() -> List[Tuple]:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE isadmin = 1')
        return cursor.fetchall()


def is_user_exists(user_id: int) -> bool:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()[0] > 0


def upd_user_admin_status(user_id: int, isadmin: int):
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET isadmin = ? WHERE id = ?",
            (isadmin, user_id)
        )
        db.commit()


def upd_user_ban_status(user_id: int, isban: int):
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET isban = ? WHERE id = ?",
            (isban, user_id)
        )
        db.commit()


def check_user_admin_status(user_id: int) -> int:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT isadmin FROM users WHERE id = ?", (user_id,))
        return cursor.fetchall()[0][0]


def check_user_ban_status(user_id: int) -> int:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT isban FROM users WHERE id = ?", (user_id,))
        return cursor.fetchall()[0][0]


# Пресеты / presets
def get_presets_from_user(user_id: int) -> List[Tuple]:
    with sqlite3.connect(PRESETS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM presets WHERE user_id = ?", (user_id,))
        return cursor.fetchall()


def get_preset_from_user_and_id(preset_id: int, user_id: int) -> Tuple:
    with sqlite3.connect(PRESETS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT (system, device, browser) FROM presets WHERE id = ? AND user_id = ?", (preset_id, user_id,))
        return cursor.fetchone()


def del_preset(preset_id: int):
    with sqlite3.connect(PRESETS_DB) as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM presets WHERE id = ?", (preset_id, ))
        db.commit()


def add_preset(user_id: int, system: str, device: str, browser: str):
    with sqlite3.connect(PRESETS_DB) as db:
        cursor = db.cursor()

        cursor.execute("SELECT MAX(id) FROM presets WHERE user_id = ?", (user_id,))
        max_id = cursor.fetchone()[0]

        if max_id is None:
            max_id = 0

        cursor.execute(
            'INSERT INTO presets (id, user_id, system, device, browser) '
            'VALUES (?, ?, ?, ?, ?)',
            (max_id + 1, user_id, system, device, browser)
        )
        db.commit()


if __name__ == '__main__':
    pass
