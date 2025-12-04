from app.index import bp
from app import db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.models import Todo, Tag

@bp.route("/")
@login_required
def index():
    todo_count = Todo.query.count()
    return render_template("index.html", todo_count=todo_count)


@bp.route("/tasks")
@login_required
def all_tasks():
    todos = Todo.query.all()
    return render_template("tasks.html", todos=todos)

@bp.route("/task/<int:task_id>")
@login_required
def task(task_id):
    task = Todo.query.get_or_404(task_id)
    return render_template("task.html", task=task)

@bp.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Todo.query.get_or_404(task_id)
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        tags_list = request.form.get("tags", "")
        tag_names = [t.strip() for t in tags_list.split(",") if t.strip()]

        new_tags = []
        for name in tag_names:
            tag = Tag.query.filter_by(content=name).first()
            if not tag:
                tag = Tag(content=name)
                db.session.add(tag)
            new_tags.append(tag)

        task.title = title
        task.description = description
        task.tags = new_tags
        
        db.session.commit()
        
        
        return redirect(url_for("main.task", task_id=task_id))

    return render_template("task_form.html", task=task)


@bp.route("/create-task", methods=["GET", "POST"])
@login_required
def create_task():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        tags_list = request.form.get("tags", "")
        tags = [t.strip() for t in tags_list.split(",") if t.strip()]

        task = Todo(
            title=title,
            description=description,
            user=current_user,
        )

        db.session.add(task)

        for tag_name in tags:
            tag = Tag.query.filter_by(content=tag_name).first()
            if not tag:
                tag = Tag(content=tag_name)
                db.session.add(tag)
            task.tags.append(tag)

        db.session.commit()

        return redirect(url_for("main.task", task_id=task.id))

    return render_template("task_form.html", task=None)


@bp.route("/delete-task/<int:task_id>", methods=["Post"])
@login_required
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("main.all_tasks"))

@bp.route("/task/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_task_completion(task_id):
    task = db.session.get(Todo, task_id)
    task.completed = not task.completed
    db.session.commit()

    if task.completed:
        flash(f"Task {task.title} marked as completed.")
    else:
        flash(f"Task {task.title} reopened.")
    return redirect(url_for("main.all_tasks"))
