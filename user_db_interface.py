import sqlite3
import os
from typing import List, Tuple
USERS_DB = f'{os.path.dirname(__file__)}/DB/users.db'

con = sqlite3.connect(USERS_DB)
cursor_usersDB = con.cursor()
cursor_usersDB.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL DEFAULT 'username',
        status INTEGER CHECK (status IN (-1, 1)) NOT NULL DEFAULT 0
    )
''')

# status
# -1 - Забанен
# 0 - Обычный
# 1 - Админ


cursor_usersDB.close()
con.close()


# Пользователи / users
def add(user_id: int, username: str) -> bool:
    with sqlite3.connect(USERS_DB) as db:
        if is_exists(user_id):
            return False

        cursor = db.cursor()
        cursor.execute('INSERT INTO users (id, username) VALUES (?, ?)', (user_id, username))
        db.commit()
        return True


def get_all() -> List[Tuple]:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users ORDER BY status')
        return cursor.fetchall()


def get_admins() -> List[Tuple]:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE status = 1')
        return cursor.fetchall()


def is_exists(user_id: int) -> bool:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()[0] > 0


def promote(user_id: int):
    __upd_status(user_id, 1)


def demote(user_id: int):
    __upd_status(user_id, 0)


def ban(user_id: int):
    __upd_status(user_id, -1)


def unban(user_id: int):
    __upd_status(user_id, 0)


def __upd_status(user_id: int, status: int):
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET status = ? WHERE id = ?",
            (status, user_id)
        )
        db.commit()


def is_admin(user_id: int) -> bool:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT status FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()[0] > 0


def is_baned(user_id: int) -> bool:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT status FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()[0] < 0
