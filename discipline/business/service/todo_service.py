from typing import List, Optional
from datetime import date
from discipline.data.model.todo_model import TodoModel, TodoStatus
from discipline.data.repository.todo_repository import TodoRepository
from discipline.business.exception.todo_not_found_exception import TodoNotFoundException

class TodoService:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def create_todo(self, content: str, due_date: date) -> TodoModel:
        todo = TodoModel(
            id=None,
            content=content,
            due_date=due_date,
            status=TodoStatus.PENDING
        )
        return self.todo_repository.save(todo)

    def complete_todo(self, todo_id: int) -> TodoModel:
        todo = self.todo_repository.find_by_id(todo_id)
        if not todo:
            raise TodoNotFoundException(todo_id)
            
        todo.status = TodoStatus.COMPLETED
        todo.completed_date = date.today()
        return self.todo_repository.update(todo)

    def edit_todo(self, todo_id: int, content: Optional[str] = None, due_date: Optional[date] = None) -> TodoModel:
        todo = self.todo_repository.find_by_id(todo_id)
        if not todo:
            raise TodoNotFoundException(todo_id)
            
        if content is not None:
            todo.content = content
        if due_date is not None:
            todo.due_date = due_date
            
        return self.todo_repository.update(todo)

    def discard_todo(self, todo_id: int) -> TodoModel:
        todo = self.todo_repository.find_by_id(todo_id)
        if not todo:
            raise TodoNotFoundException(todo_id)
            
        todo.status = TodoStatus.DISCARDED
        todo.completed_date = None
        return self.todo_repository.update(todo)

    def list_todos(self, status: Optional[TodoStatus] = None) -> List[TodoModel]:
        return self.todo_repository.find_all(status)
