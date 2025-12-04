from app import db
from app.utils.models import User, Todo, Tag


def test_user_password_hashing(app):
    user = User(username="alice")
    user.set_password("secret123")

    db.session.add(user)
    db.session.commit()

    assert user.password_hash is not None
    assert user.get_password("secret123") is True
    assert user.get_password("wrong") is False


def test_todo_belongs_to_user(app):
    user = User(username="bob")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    todo = Todo(
        title="Test task",
        description="Description here",
        user=user,
    )
    db.session.add(todo)
    db.session.commit()

    assert todo.id is not None
    assert todo.user_id == user.id
    assert todo.user.username == "bob"
    

def test_todo_has_completed_flag_defaults_false(app, user):
    todo = Todo(
        title="Test task",
        description="Description here",
        user=user,
    )
    db.session.add(todo)
    db.session.commit()

    assert todo.completed is False
    
    
def test_tag_creation(app):
    tag = Tag(content="urgent")
    db.session.add(tag)
    db.session.commit()

    assert tag.id is not None
    assert tag.content == "urgent"
    assert str(tag) == "urgent"


def test_tag_todo_relationship(app):
    user = User(username="carol")
    user.set_password("pw123")
    db.session.add(user)
    db.session.commit()

    todo = Todo(
        title="Buy milk",
        description="2% lactose free",
        user=user,
    )
    tag = Tag(content="shopping")

    # attach tag
    todo.tags.append(tag)

    db.session.add(todo)
    db.session.commit()

    # check tag side
    assert tag in todo.tags
    assert tag.content == "shopping"

    # check reverse side
    assert todo in tag.todos
    assert tag.todos[0].title == "Buy milk"


def test_multiple_tags_on_todo(app):
    user = User(username="dave")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()

    todo = Todo(title="Read book", description="Before Sunday", user=user)
    tag1 = Tag(content="reading")
    tag2 = Tag(content="weekend")

    todo.tags.extend([tag1, tag2])

    db.session.add(todo)
    db.session.commit()

    assert len(todo.tags) == 2
    assert set(t.content for t in todo.tags) == {"reading", "weekend"}
