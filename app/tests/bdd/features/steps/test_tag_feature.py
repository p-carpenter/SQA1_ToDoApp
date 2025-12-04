from pytest_bdd import scenarios, given, when, then, parsers
from app.utils.models import Todo, Tag
from app import db

scenarios('../tags.feature')


@given('I am logged in')
def logged_in_user(auth):
    """Use the auth fixture to log in."""
    auth.login()


@given('I am on the task creation page')
def on_task_creation_page(client):
    resp = client.get("/create-task")
    assert resp.status_code == 200


@when(parsers.parse('I create a task with title "{title}" and tags "{tags}"'), target_fixture="create_response")
def create_task_with_tags(client, title, tags):
    """Post to the create-task endpoint with tags."""
    resp = client.post(
        "/create-task",
        data={
            "title": title,
            "description": "Test description",
            "tags": tags
        },
        follow_redirects=True
    )
    return resp


@then('the task should be created successfully')
def task_created(create_response):
    assert create_response.status_code == 200


@then(parsers.parse('the task should have tags "{expected_tags}"'))
def task_has_tags(expected_tags):
    """Check the created task has the right tags."""
    task = Todo.query.filter_by(title="My Task").first(
    )
    assert task is not None

    expected = {tag.strip() for tag in expected_tags.split(",")}
    actual = {t.content for t in task.tags}
    assert actual == expected
