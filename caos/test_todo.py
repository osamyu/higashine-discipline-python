
import pytest
import sqlite3
import os
from caos.todo import init_db, add_todo, complete_todo, edit_todo, discard_todo, list_todos, DATABASE_NAME

@pytest.fixture
def setup_teardown_db():
    # Setup: Create a fresh database for testing
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
    init_db()
    yield
    # Teardown: Remove the database file after tests
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)

def test_add_todo(setup_teardown_db):
    add_todo("Test Todo 1", "2023-12-31")
    todos = list_todos()
    assert len(todos) == 1
    assert todos[0][1] == "Test Todo 1"
    assert todos[0][2] == "2023-12-31"
    assert todos[0][3] == "未実行"
    assert todos[0][4] == ""

def test_complete_todo(setup_teardown_db):
    add_todo("Test Todo 2", "2023-12-31")
    todo_id = list_todos()[0][0]
    complete_todo(todo_id)
    todos = list_todos(status_filter="実行済")
    assert len(todos) == 1
    assert todos[0][3] == "実行済"
    assert todos[0][4] is not None and todos[0][4] != ""

def test_edit_todo(setup_teardown_db):
    add_todo("Test Todo 3", "2023-12-31")
    todo_id = list_todos()[0][0]
    edit_todo(todo_id, "Updated Todo 3", "2024-01-15")
    todos = list_todos()
    assert len(todos) == 1
    assert todos[0][1] == "Updated Todo 3"
    assert todos[0][2] == "2024-01-15"

def test_discard_todo(setup_teardown_db):
    add_todo("Test Todo 4", "2023-12-31")
    todo_id = list_todos()[0][0]
    discard_todo(todo_id)
    todos = list_todos(status_filter="破棄")
    assert len(todos) == 1
    assert todos[0][3] == "破棄"
    assert todos[0][4] == ""

def test_list_todos_all_statuses(setup_teardown_db):
    add_todo("Todo A", "2023-12-01")
    add_todo("Todo B", "2023-12-02")
    todo_a_id = list_todos("未実行")[0][0]
    complete_todo(todo_a_id)

    todos_unfinished = list_todos("未実行")
    assert len(todos_unfinished) == 1
    assert todos_unfinished[0][1] == "Todo B"

    todos_completed = list_todos("実行済")
    assert len(todos_completed) == 1
    assert todos_completed[0][1] == "Todo A"

    todos_all = list_todos("all")
    assert len(todos_all) == 2

