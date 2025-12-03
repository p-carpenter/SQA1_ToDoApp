from flask import Blueprint
from flask import render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/")
def all_tasks():
    return "<h1>List of all tasks</h1>"

@bp.route("/task/<int:task_id>")
def task(task_id):
    return f"<h1>Task detail page for task {task_id}</h1>"


@bp.route("/new-task")
def create_task():
    return f"<h1>Placeholder for creating a new task"
