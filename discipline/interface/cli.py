import argparse
import sys
from typing import Optional
from discipline.data.database import Database
from discipline.data.repository.sqlite_todo_repository import SqliteTodoRepository
from discipline.business.service.todo_service import TodoService
from discipline.interface.controller.todo_controller import TodoController

def get_controller(db_path: str = "todo.db") -> TodoController:
    database = Database(db_path)
    repository = SqliteTodoRepository(database)
    service = TodoService(repository)
    return TodoController(service, database)

def print_todo(todo) -> None:
    completed = f", Completed: {todo.completed_date}" if todo.completed_date else ""
    print(f"[{todo.id}] {todo.content} (Due: {todo.due_date}, Status: {todo.status}){completed}")

def main() -> None:
    parser = argparse.ArgumentParser(description="CLI Todo Management System")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add Todo
    add_parser = subparsers.add_parser("add", help="Add a new Todo")
    add_parser.add_argument("content", type=str, help="Todo content")
    add_parser.add_argument("due_date", type=str, help="Due date (YYYY-MM-DD)")

    # Complete Todo
    complete_parser = subparsers.add_parser("complete", help="Mark a Todo as completed")
    complete_parser.add_argument("id", type=int, help="Todo ID")

    # Edit Todo
    edit_parser = subparsers.add_parser("edit", help="Edit a Todo")
    edit_parser.add_argument("id", type=int, help="Todo ID")
    edit_parser.add_argument("--content", type=str, help="New Todo content")
    edit_parser.add_argument("--due_date", type=str, help="New due date (YYYY-MM-DD)")

    # Discard Todo
    discard_parser = subparsers.add_parser("discard", help="Discard a Todo")
    discard_parser.add_argument("id", type=int, help="Todo ID")

    # List Todos
    list_parser = subparsers.add_parser("list", help="List Todos")
    list_parser.add_argument("--status", type=str, help="Filter by status (未実行/実行済/破棄)")
    list_parser.add_argument("--all", action="store_true", help="Show all Todos")

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = get_controller()

    try:
        if args.command == "add":
            todo = controller.add_todo(args.content, args.due_date)
            print("Successfully added Todo:")
            print_todo(todo)

        elif args.command == "complete":
            todo = controller.complete_todo(args.id)
            print("Successfully completed Todo:")
            print_todo(todo)

        elif args.command == "edit":
            if not args.content and not args.due_date:
                print("Error: Please provide --content or --due_date to edit.")
                sys.exit(1)
            todo = controller.edit_todo(args.id, args.content, args.due_date)
            print("Successfully edited Todo:")
            print_todo(todo)

        elif args.command == "discard":
            todo = controller.discard_todo(args.id)
            print("Successfully discarded Todo:")
            print_todo(todo)

        elif args.command == "list":
            if args.all:
                todo_list = controller.list_todos(None)
            elif args.status:
                todo_list = controller.list_todos(args.status)
            else:
                todo_list = controller.list_todos("未実行")
                
            if not todo_list:
                print("No Todos found.")
            else:
                for todo in todo_list:
                    print_todo(todo)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
