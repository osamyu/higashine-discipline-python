from datetime import date
from typing import Optional
from discipline.data.model.todo_model import TodoStatus

class TodoValidator:
    @staticmethod
    def validate_content(content: str) -> None:
        if not content or not content.strip():
            raise ValueError("Content cannot be empty.")

    @staticmethod
    def parse_date(date_str: str) -> date:
        try:
            return date.fromisoformat(date_str)
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.")
            
    @staticmethod
    def parse_status(status_str: Optional[str]) -> Optional[TodoStatus]:
        if not status_str:
            return None
        for status in TodoStatus:
            if status.name == status_str.upper() or status.value == status_str:
                return status
        raise ValueError(f"Invalid status: {status_str}.")
