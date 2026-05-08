import pytest
from datetime import date
from unittest.mock import Mock, MagicMock

from discipline.business.service.todo_service import TodoService
from discipline.data.model.todo_model import TodoModel, TodoStatus
from discipline.business.exception.todo_not_found_exception import TodoNotFoundException

def test_正常系_Todoを新規作成できること():
    # Arrange
    mock_repository = Mock()
    mock_repository.save.return_value = TodoModel(
        id=1,
        content="Test Todo",
        due_date=date(2023, 1, 1),
        status=TodoStatus.PENDING
    )
    service = TodoService(mock_repository)

    # Act
    result = service.create_todo("Test Todo", date(2023, 1, 1))

    # Assert
    assert result.id == 1
    assert result.content == "Test Todo"
    assert result.due_date == date(2023, 1, 1)
    assert result.status == TodoStatus.PENDING
    
    mock_repository.save.assert_called_once()
    saved_todo = mock_repository.save.call_args[0][0]
    assert saved_todo.content == "Test Todo"
    assert saved_todo.due_date == date(2023, 1, 1)
    assert saved_todo.status == TodoStatus.PENDING

def test_正常系_既存のTodoを完了にできること():
    # Arrange
    mock_repository = Mock()
    existing_todo = TodoModel(
        id=1,
        content="Test Todo",
        due_date=date(2023, 1, 1),
        status=TodoStatus.PENDING
    )
    mock_repository.find_by_id.return_value = existing_todo
    mock_repository.update.return_value = existing_todo
    service = TodoService(mock_repository)

    # Act
    result = service.complete_todo(1)

    # Assert
    assert result.status == TodoStatus.COMPLETED
    assert result.completed_date == date.today()
    mock_repository.find_by_id.assert_called_once_with(1)
    mock_repository.update.assert_called_once_with(existing_todo)

def test_異常系_存在しないTodoを完了しようとすると例外が発生すること():
    # Arrange
    mock_repository = Mock()
    mock_repository.find_by_id.return_value = None
    service = TodoService(mock_repository)

    # Act & Assert
    with pytest.raises(TodoNotFoundException) as exc_info:
        service.complete_todo(999)
        
    assert exc_info.value.error_code == "TODO_NOT_FOUND"

def test_正常系_既存のTodoを破棄できること():
    # Arrange
    mock_repository = Mock()
    existing_todo = TodoModel(
        id=1,
        content="Test Todo",
        due_date=date(2023, 1, 1),
        status=TodoStatus.PENDING
    )
    mock_repository.find_by_id.return_value = existing_todo
    mock_repository.update.return_value = existing_todo
    service = TodoService(mock_repository)

    # Act
    result = service.discard_todo(1)

    # Assert
    assert result.status == TodoStatus.DISCARDED
    assert result.completed_date is None
    mock_repository.update.assert_called_once_with(existing_todo)

def test_正常系_既存のTodoを編集できること():
    # Arrange
    mock_repository = Mock()
    existing_todo = TodoModel(
        id=1,
        content="Old Todo",
        due_date=date(2023, 1, 1),
        status=TodoStatus.PENDING
    )
    mock_repository.find_by_id.return_value = existing_todo
    mock_repository.update.return_value = existing_todo
    service = TodoService(mock_repository)

    # Act
    result = service.edit_todo(1, content="New Todo", due_date=date(2023, 1, 2))

    # Assert
    assert result.content == "New Todo"
    assert result.due_date == date(2023, 1, 2)
    mock_repository.update.assert_called_once_with(existing_todo)

def test_正常系_Todo一覧を取得できること():
    # Arrange
    mock_repository = Mock()
    mock_repository.find_all.return_value = [
        TodoModel(id=1, content="T1", due_date=date.today(), status=TodoStatus.PENDING)
    ]
    service = TodoService(mock_repository)

    # Act
    result = service.list_todos(TodoStatus.PENDING)

    # Assert
    assert len(result) == 1
    mock_repository.find_all.assert_called_once_with(TodoStatus.PENDING)
