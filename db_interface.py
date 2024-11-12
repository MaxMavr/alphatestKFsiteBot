import sqlite3
import os
from collections import defaultdict
from typing import List, Tuple, Union

USERS_DB = f'{os.path.dirname(__file__)}/DB/users.db'
BUGS_DB = f'{os.path.dirname(__file__)}/DB/bug.db'
PRESETS_DB = f'{os.path.dirname(__file__)}/DB/presets.db'

con = sqlite3.connect(USERS_DB)
cursor_usersDB = con.cursor()
cursor_usersDB.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL DEFAULT 'username',
        amount_bug INTEGER NOT NULL DEFAULT 0,
        isadmin INTEGER CHECK (isadmin IN (0, 1)) NOT NULL DEFAULT 0
        isban INTEGER CHECK (isban IN (0, 1)) NOT NULL DEFAULT 0
    )
''')
cursor_usersDB.close()
con.close()

con = sqlite3.connect(BUGS_DB)
cursor_bugsDB = con.cursor()
cursor_bugsDB.execute('''
    CREATE TABLE IF NOT EXISTS bugs (
        id INTEGER PRIMARY KEY NOT NULL,
        system TEXT NOT NULL DEFAULT 'system',
        device TEXT NOT NULL DEFAULT 'device',
        browser TEXT NOT NULL DEFAULT 'browser',
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
        username TEXT NOT NULL DEFAULT 'username',
        system TEXT NOT NULL DEFAULT 'system',
        device TEXT NOT NULL DEFAULT 'device',
        browser TEXT NOT NULL DEFAULT 'browser'
    )
''')
cursor_presetsDB.close()
con.close()


def invert(value):
    return value ^ 1


# Баги / bugs
def fetch_bugs_count() -> Tuple[int, int]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM bugs")
        all_bugs = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bugs WHERE isfixed = 1")
        fix_bugs = cursor.fetchone()[0]
        return all_bugs, fix_bugs


def fetch_all_bugs() -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs ORDER BY isfixed ASC")
        return cursor.fetchone()


def fetch_nonfix_bugs() -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs WHERE isfixed = 0")
        return cursor.fetchone()


def fetch_bugs_from_username(username: str) -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs WHERE username = ?", (username,))
        return cursor.fetchone()


def get_bug_from_id(bug_id: int) -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs WHERE id = ?", (bug_id,))
        return cursor.fetchone()


def insert_bug(msg_id: int, system: str, device: str, browser: str, description: str):
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO bugs (id, system, device, browser, description) VALUES (?, ?, ?, ?, ?)',
            (msg_id, system, device, browser, description)
        )
        db.commit()


def update_bug_fix_status(bug_id: int):
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT isfixed FROM bugs WHERE id = ?", (bug_id,))
        isfixed = invert(cursor.fetchone()[0])
        cursor.execute(
            "UPDATE bugs SET isfixed = ? WHERE id = ?",
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


def fetch_all_users() -> List[Tuple]:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users ORDER BY isadmin')
        return cursor.fetchall()


def fetch_all_admins() -> List[Tuple]:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE isadmin = 1')
        return cursor.fetchall()


def get_user_from_id(user_id: int) -> List[Tuple]:
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()


def update_user_admin_status(user_id: int, isadmin: int):
    with sqlite3.connect(USERS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET isadmin = ? WHERE id = ?",
            (isadmin, user_id)
        )
        db.commit()


def update_user_ban_status(user_id: int, isban: int):
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


"""
def update_user_divination(user_id: int, select_number: int):
    with sqlite3.connect(USERS_DB) as users_db:
        users_cursor = users_db.cursor()
        users_cursor.execute(
            "UPDATE users SET amount_divinations = amount_divinations + 1, last_divination = ? WHERE id = ?",
            (select_number, user_id))
        users_db.commit()


def get_circle_numbers():
    with sqlite3.connect(CIRCLES_DB) as circles_db:
        circles_cursor = circles_db.cursor()
        circles_cursor.execute("SELECT number FROM circles")
        return [i[0] for i in circles_cursor.fetchall()]


def fetch_all_circles() -> List[Tuple]:
    with sqlite3.connect(CIRCLES_DB) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM circles')
        return cursor.fetchall()


def get_video_note(number):
    with sqlite3.connect(CIRCLES_DB) as circles_db:
        circles_cursor = circles_db.cursor()
        circles_cursor.execute("SELECT video_note FROM circles WHERE number = ?", (number,))
        result = circles_cursor.fetchone()

        if result is not None:
            return result[0]
        else:
            return None


def get_video_number(video_hash):
    with sqlite3.connect(CIRCLES_DB) as circles_db:
        circles_cursor = circles_db.cursor()
        circles_cursor.execute("SELECT number FROM circles WHERE video_note = ?", (video_hash,))
        result = circles_cursor.fetchone()

        if result is not None:
            return result[0]
        else:
            return None


def delete_circle(number):
    with sqlite3.connect(CIRCLES_DB) as circles_db:
        circles_cursor = circles_db.cursor()
        circles_cursor.execute('DELETE FROM circles WHERE number = ?', (number,))
        circles_db.commit()


def add_message(video_number: int, chat_id: int, message_id: int) -> None:
    conn = sqlite3.connect(CIRCLES_DB)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO messages (video_number, chat_id, message_id)
            VALUES (?, ?, ?)
        ''', (video_number, chat_id, message_id))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Сообщение-кружок: {video_number}-{chat_id}-{message_id} уже существует в базе данных.")
    finally:
        conn.close()


def get_messages_for_video(video_number: int) -> List[VideoMessage]:
    conn = sqlite3.connect(CIRCLES_DB)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT chat_id, message_id
        FROM messages
        WHERE video_number = ?
    ''', (video_number,))

    messages_info = cursor.fetchall()
    conn.close()

    # Группируем message_id по chat_id
    grouped_messages = defaultdict(list)
    for chat_id, message_id in messages_info:
        grouped_messages[chat_id].append(message_id)

    # Преобразуем в список объектов Video_message
    result = [VideoMessage(chat_id=chat_id, message_ids=message_ids) for chat_id, message_ids in grouped_messages.items()]

    return result
"""

if __name__ == '__main__':
    pass
