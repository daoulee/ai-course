from flask import Flask, abort, redirect, render_template, request

import db
from db import get_db

app = Flask(__name__)
app.config["DATABASE"] = "todo.db"
app.teardown_appcontext(db.close_db)
MAX_TITLE = 100


def init_db():
    with app.app_context():
        db.init_db()


@app.get("/")
def index():
    return render_template("index.html", todos=db.list_todos())


@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    if not title:
        return render_template("error.html", code=400, message="제목을 입력하세요."), 400
    if len(title) > MAX_TITLE:
        return render_template("error.html", code=400, message=f"제목은 {MAX_TITLE}자까지입니다."), 400
    db.add_todo(title)
    return redirect("/")


@app.post("/toggle/<int:todo_id>")
def toggle(todo_id):
    if not db.toggle_todo(todo_id):
        abort(404)
    return redirect("/")


@app.post("/delete/<int:todo_id>")
def delete(todo_id):
    if not db.delete_todo(todo_id):
        abort(404)
    return redirect("/")


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, message="없는 할 일입니다."), 404


if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)
