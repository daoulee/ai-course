import sqlite3
from datetime import datetime

from flask import Flask, abort, g, redirect, render_template, request

app = Flask(__name__)
app.config["DATABASE"] = "todo.db"
MAX_TITLE = 100


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
    if not title:
        return render_template("error.html", code=400, message="제목을 입력하세요."), 400
    if len(title) > MAX_TITLE:
        return render_template("error.html", code=400, message=f"제목은 {MAX_TITLE}자까지입니다."), 400
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    get_db().execute("INSERT INTO todos (title, created_at) VALUES (?, ?)", (title, now))
    get_db().commit()
    return redirect("/")


@app.post("/toggle/<int:todo_id>")
def toggle(todo_id):
    cur = get_db().execute("UPDATE todos SET done = 1 - done WHERE id = ?", (todo_id,))
    if cur.rowcount == 0:
        abort(404)
    get_db().commit()
    return redirect("/")


@app.post("/delete/<int:todo_id>")
def delete(todo_id):
    cur = get_db().execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    if cur.rowcount == 0:
        abort(404)
    get_db().commit()
    return redirect("/")


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, message="없는 할 일입니다."), 404


if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)
