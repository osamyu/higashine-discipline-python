from abc import ABC, abstractmethod
from typing import List, Optional
from discipline.data.model.todo_model import TodoModel, TodoStatus

class TodoRepository(ABC):
    @abstractmethod
    def save(self, todo: TodoModel) -> TodoModel:
        pass
    
    @abstractmethod
    def find_by_id(self, todo_id: int) -> Optional[TodoModel]:
        pass
        
    @abstractmethod
    def find_all(self, status: Optional[TodoStatus] = None) -> List[TodoModel]:
        pass
    
    @abstractmethod
    def update(self, todo: TodoModel) -> TodoModel:
        pass
