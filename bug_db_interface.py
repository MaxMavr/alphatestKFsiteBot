import sqlite3
import os
from typing import List, Tuple
BUGS_DB = f'{os.path.dirname(__file__)}/DB/bugs.db'

con = sqlite3.connect(BUGS_DB)
cursor_bugsDB = con.cursor()
cursor_bugsDB.execute('''
    CREATE TABLE IF NOT EXISTS bugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        message_id INTEGER NOT NULL,
        preset_id INTEGER NOT NULL,
        description TEXT,
        isfixed INTEGER CHECK (isfixed IN (0, 1)) NOT NULL DEFAULT 0
    )
''')
cursor_bugsDB.close()
con.close()


def invert(value):
    return 1 - value


# Баги / bugs
def add(chat_id: int, message_id: int, preset_id: int, description: str):
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO bugs (chat_id, message_id, preset_id, description) VALUES (?, ?, ?, ?)',
            (chat_id, message_id, preset_id, description)
        )
        db.commit()


def delete(bug_id: int):
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            'DELETE FROM bugs WHERE id = ?',
            (bug_id,)
        )
        db.commit()


def delete_from_user(chat_id: int):
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute(
            'DELETE FROM bugs WHERE chat_id = ?',
            (chat_id,)
        )
        db.commit()


def stat() -> Tuple[int, int]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM bugs")
        all_bugs = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bugs WHERE isfixed = 1")
        fix_bugs = cursor.fetchone()[0]
        return fix_bugs, all_bugs


def stat_from_user(chat_id: int) -> Tuple[int, int]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM bugs WHERE chat_id = ?", (chat_id,))
        all_bugs = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bugs WHERE chat_id = ? AND isfixed = 1")
        fix_bugs = cursor.fetchone()[0]
        return fix_bugs, all_bugs


def is_exists(bug_id: int) -> bool:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM bugs WHERE id = ?", (bug_id,))
        return cursor.fetchone()[0] > 0


def get_all() -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs ORDER BY isfixed ASC")
        return cursor.fetchall()


def get_fix() -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs WHERE isfixed = 0")
        return cursor.fetchall()


def get_from_user(chat_id: int) -> List[Tuple]:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs WHERE chat_id = ?", (chat_id,))
        return cursor.fetchall()


def get_from_id(bug_id: int) -> Tuple:
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bugs WHERE id = ?", (bug_id,))
        return cursor.fetchone()


def upd_status(bug_id: int):
    with sqlite3.connect(BUGS_DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT isfixed FROM bugs WHERE id = ?", (bug_id,))
        isfixed = invert(cursor.fetchone()[0])
        cursor.execute(
            "UPDATE bugs SET isfixed = ? WHERE id = ?",
            (isfixed, bug_id)
        )
        db.commit()
