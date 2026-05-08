from dataclasses import dataclass
from typing import Optional

@dataclass
class TodoResponse:
    id: int
    content: str
    due_date: str
    status: str
    completed_date: Optional[str]

    @classmethod
    def from_model(cls, model: 'TodoModel') -> 'TodoResponse':
        return cls(
            id=model.id,
            content=model.content,
            due_date=model.due_date.isoformat(),
            status=model.status.value,
            completed_date=model.completed_date.isoformat() if model.completed_date else None
        )
