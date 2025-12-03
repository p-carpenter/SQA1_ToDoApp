from app.index import bp
from flask import render_template, request, redirect, url_for
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
    task = todos[task_id - 1]
    return render_template("task.html", task=task)

@bp.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    index = task_id - 1
    task = todos[index]
    print(task)
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        tags_list = request.form.get("tags", "")
        tags = [t.strip() for t in tags_list.split(",") if t.strip()]
        todos[index]["title"] = title
        todos[index]["description"] = description
        todos[index]["tags"] = tags
        return redirect(url_for("main.task", task_id=task_id))

    return render_template("task_form.html", task=task)

@bp.route("/create-task")
def create_task():
    return render_template("create_task.html")
