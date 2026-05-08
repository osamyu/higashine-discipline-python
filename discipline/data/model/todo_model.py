from enum import Enum
from dataclasses import dataclass
from typing import Optional
from datetime import date

class TodoStatus(Enum):
    PENDING = "未実行"
    COMPLETED = "実行済"
    DISCARDED = "破棄"

@dataclass
class TodoModel:
    id: Optional[int]
    content: str
    due_date: date
    status: TodoStatus
    completed_date: Optional[date] = None
