def test_create_task_with_tags_via_form(client, auth):
    auth.login()

    resp = client.post(
        "/new-task",
        data={
            "title": "Tagged Task",
            "description": "desc",
            "tags": "urgent, home"
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

    created = Todo.query.filter_by(title="Tagged Task").first()
    assert created is not None

    # Tag objects should have been created
    tag_names = {t.content for t in created.tags}
    assert tag_names == {"urgent", "home"}


def test_edit_task_tags_via_form(client, auth, app, user):
    auth.login()

    # Create a todo with one tag
    todo = Todo(title="Edit me", description="d", user=user)
    tag1 = Tag(content="oldtag")
    todo.tags.append(tag1)
    db.session.add(todo)
    db.session.commit()

    # Now update tags
    resp = client.post(
        f"/edit-task/{todo.id}",
        data={
            "title": "Edit me",
            "description": "d updated",
            "tags": "newtag, something"
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

    updated = Todo.query.get(todo.id)
    tag_contents = {t.content for t in updated.tags}
    assert tag_contents == {"newtag", "something"}


def test_delete_task_keeps_tags(client, auth, app, user):
    auth.login()

    todo = Todo(title="Delete me", description="d", user=user)
    tag = Tag(content="keepme")
    todo.tags.append(tag)
    db.session.add(todo)
    db.session.commit()

    # Delete the todo
    resp = client.post(f"/delete-task/{todo.id}", follow_redirects=True)
    assert resp.status_code == 200

    # Todo is gone
    assert Todo.query.get(todo.id) is None

    # Tag should still exist
    still = Tag.query.filter_by(content="keepme").first()
    assert still is not None

    # but association must be removed
    assert todo not in still.todos
