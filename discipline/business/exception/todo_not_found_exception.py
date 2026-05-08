from discipline.business.exception.base_exception import AppBaseException

class TodoNotFoundException(AppBaseException):
    def __init__(self, todo_id: int):
        super().__init__(f"Todo ID {todo_id} is not found.", "TODO_NOT_FOUND")
