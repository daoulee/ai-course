import sqlite3
from datetime import datetime

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    get_db().execute(
        "CREATE TABLE IF NOT EXISTS todos ("
        "id INTEGER PRIMARY KEY, title TEXT NOT NULL, "
        "done INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL)"
    )
    get_db().commit()


def list_todos():
    return get_db().execute("SELECT * FROM todos ORDER BY done, id DESC").fetchall()


def add_todo(title):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    get_db().execute("INSERT INTO todos (title, created_at) VALUES (?, ?)", (title, now))
    get_db().commit()


def toggle_todo(todo_id):
    cur = get_db().execute("UPDATE todos SET done = 1 - done WHERE id = ?", (todo_id,))
    get_db().commit()
    return cur.rowcount > 0


def delete_todo(todo_id):
    cur = get_db().execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    get_db().commit()
    return cur.rowcount > 0
