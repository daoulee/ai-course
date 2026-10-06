import sqlite3
from datetime import datetime

from flask import Flask, g, redirect, render_template, request

app = Flask(__name__)
app.config["DATABASE"] = "todo.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        get_db().execute(
            "CREATE TABLE IF NOT EXISTS todos ("
            "id INTEGER PRIMARY KEY, title TEXT NOT NULL, "
            "done INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL)"
        )
        get_db().commit()


@app.get("/")
def index():
    todos = get_db().execute("SELECT * FROM todos ORDER BY id DESC").fetchall()
    return render_template("index.html", todos=todos)


@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    get_db().execute("INSERT INTO todos (title, created_at) VALUES (?, ?)", (title, now))
    get_db().commit()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)
