import pytest
from discipline.data.database import Database
from discipline.data.repository.sqlite_todo_repository import SqliteTodoRepository
from discipline.business.service.todo_service import TodoService
from discipline.interface.controller.todo_controller import TodoController

@pytest.fixture
def test_controller():
    # Use in-memory database for testing
    database = Database(":memory:")
    repository = SqliteTodoRepository(database)
    service = TodoService(repository)
    return TodoController(service, database)

def test_正常系_Todoの追加から一覧取得までの一連の処理が成功すること(test_controller):
    # Act: Add Todo
    response = test_controller.add_todo("Buy Milk", "2023-12-31")
    
    # Assert
    assert response.id == 1
    assert response.content == "Buy Milk"
    assert response.status == "未実行"
    
    # Act: List Todos
    todo_list = test_controller.list_todos()
    
    # Assert
    assert len(todo_list) == 1
    assert todo_list[0].content == "Buy Milk"

def test_正常系_Todoを完了状態に更新できること(test_controller):
    # Arrange
    test_controller.add_todo("Buy Milk", "2023-12-31")
    
    # Act
    response = test_controller.complete_todo(1)
    
    # Assert
    assert response.status == "実行済"
    assert response.completed_date is not None

def test_異常系_無効な日付形式で追加すると例外が発生すること(test_controller):
    with pytest.raises(ValueError, match="Invalid date format"):
        test_controller.add_todo("Invalid Date Todo", "2023/12/31")

def test_正常系_Todoを編集できること(test_controller):
    # Arrange
    test_controller.add_todo("Old Content", "2023-12-31")
    
    # Act
    response = test_controller.edit_todo(1, content="New Content")
    
    # Assert
    assert response.content == "New Content"
    assert response.due_date == "2023-12-31"

def test_正常系_Todoを破棄できること(test_controller):
    # Arrange
    test_controller.add_todo("To be discarded", "2023-12-31")
    
    # Act
    response = test_controller.discard_todo(1)
    
    # Assert
    assert response.status == "破棄"
    assert response.completed_date is None
