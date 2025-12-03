from app.index import bp
from flask import render_template

@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/tasks")
def all_tasks():
    return render_template("tasks.html")

@bp.route("/task/<int:task_id>")
def task(task_id):
    return f"<h1>Task detail page for task {task_id}</h1>"


@bp.route("/new-task")
def create_task():
    return render_template("new_task.html")
