from typing import List, Optional
from discipline.business.service.todo_service import TodoService
from discipline.data.database import Database
from discipline.interface.response.todo_response import TodoResponse
from discipline.interface.validation.todo_validator import TodoValidator
from discipline.business.exception.base_exception import AppBaseException

class TodoController:
    def __init__(self, todo_service: TodoService, database: Database):
        self.todo_service = todo_service
        self.database = database

    def add_todo(self, content: str, due_date_str: str) -> TodoResponse:
        try:
            TodoValidator.validate_content(content)
            due_date = TodoValidator.parse_date(due_date_str)
            
            todo = self.todo_service.create_todo(content, due_date)
            self.database.commit()
            return TodoResponse.from_model(todo)
        except Exception as e:
            self.database.rollback()
            raise e

    def complete_todo(self, todo_id: int) -> TodoResponse:
        try:
            todo = self.todo_service.complete_todo(todo_id)
            self.database.commit()
            return TodoResponse.from_model(todo)
        except Exception as e:
            self.database.rollback()
            raise e

    def edit_todo(self, todo_id: int, content: Optional[str] = None, due_date_str: Optional[str] = None) -> TodoResponse:
        try:
            if content is not None:
                TodoValidator.validate_content(content)
                
            due_date = None
            if due_date_str is not None:
                due_date = TodoValidator.parse_date(due_date_str)
                
            todo = self.todo_service.edit_todo(todo_id, content, due_date)
            self.database.commit()
            return TodoResponse.from_model(todo)
        except Exception as e:
            self.database.rollback()
            raise e

    def discard_todo(self, todo_id: int) -> TodoResponse:
        try:
            todo = self.todo_service.discard_todo(todo_id)
            self.database.commit()
            return TodoResponse.from_model(todo)
        except Exception as e:
            self.database.rollback()
            raise e

    def list_todos(self, status_str: Optional[str] = None) -> List[TodoResponse]:
        try:
            status = TodoValidator.parse_status(status_str)
            todo_list = self.todo_service.list_todos(status)
            return [TodoResponse.from_model(t) for t in todo_list]
        except Exception as e:
            raise e
