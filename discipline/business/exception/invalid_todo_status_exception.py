from discipline.business.exception.base_exception import AppBaseException

class InvalidTodoStatusException(AppBaseException):
    def __init__(self, message: str):
        super().__init__(message, "INVALID_TODO_STATUS")
