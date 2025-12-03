from app.index import bp
from flask import render_template
from datetime import datetime
from app.utils.sample_todos import todos

@bp.route("/")
def index():
    todo_count = len(todos)
    return render_template("index.html", todo_count=todo_count)


@bp.route("/tasks")
def all_tasks():
    return render_template("tasks.html", todos=todos)

@bp.route("/task/<int:task_id>")
def task(task_id):
    task = todos[task_id]
    return render_template("task.html", task=task)


@bp.route("/create-task")
def create_task():
    return render_template("create_task.html")
