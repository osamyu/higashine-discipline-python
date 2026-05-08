from typing import List, Optional
from datetime import datetime, date
from discipline.data.model.todo_model import TodoModel, TodoStatus
from discipline.data.repository.todo_repository import TodoRepository
from discipline.data.database import Database

class SqliteTodoRepository(TodoRepository):
    def __init__(self, database: Database):
        self.database = database

    def save(self, todo: TodoModel) -> TodoModel:
        conn = self.database.connect()
        cursor = conn.cursor()
        
        completed_date_str = todo.completed_date.isoformat() if todo.completed_date else None
        
        cursor.execute(
            """
            INSERT INTO todos (content, due_date, status, completed_date)
            VALUES (?, ?, ?, ?)
            """,
            (todo.content, todo.due_date.isoformat(), todo.status.value, completed_date_str)
        )
        todo.id = cursor.lastrowid
        return todo

    def find_by_id(self, todo_id: int) -> Optional[TodoModel]:
        conn = self.database.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, content, due_date, status, completed_date FROM todos WHERE id = ?",
            (todo_id,)
        )
        row = cursor.fetchone()
        
        if row is None:
            return None
            
        return self._map_row_to_model(row)

    def find_all(self, status: Optional[TodoStatus] = None) -> List[TodoModel]:
        conn = self.database.connect()
        cursor = conn.cursor()
        
        if status:
            cursor.execute(
                "SELECT id, content, due_date, status, completed_date FROM todos WHERE status = ?",
                (status.value,)
            )
        else:
            cursor.execute("SELECT id, content, due_date, status, completed_date FROM todos")
            
        rows = cursor.fetchall()
        
        todo_list: List[TodoModel] = []
        for row in rows:
            todo_list.append(self._map_row_to_model(row))
            
        return todo_list

    def update(self, todo: TodoModel) -> TodoModel:
        conn = self.database.connect()
        cursor = conn.cursor()
        
        completed_date_str = todo.completed_date.isoformat() if todo.completed_date else None
        
        cursor.execute(
            """
            UPDATE todos 
            SET content = ?, due_date = ?, status = ?, completed_date = ?
            WHERE id = ?
            """,
            (todo.content, todo.due_date.isoformat(), todo.status.value, completed_date_str, todo.id)
        )
        return todo

    def _map_row_to_model(self, row: dict) -> TodoModel:
        completed_date = date.fromisoformat(row["completed_date"]) if row["completed_date"] else None
        return TodoModel(
            id=row["id"],
            content=row["content"],
            due_date=date.fromisoformat(row["due_date"]),
            status=TodoStatus(row["status"]),
            completed_date=completed_date
        )
