
import sqlite3
import datetime

DATABASE_NAME = "todo.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL,
            completed_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_todo(content, due_date):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO todos (content, due_date, status, completed_date) VALUES (?, ?, ?, ?)",
              (content, due_date, "未実行", ""))
    conn.commit()
    conn.close()
    print(f"Todo ", content, " with due date ", due_date, " added.")

def complete_todo(todo_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    completed_date = datetime.date.today().isoformat()
    c.execute("UPDATE todos SET status = ?, completed_date = ? WHERE id = ?",
              ("実行済", completed_date, todo_id))
    conn.commit()
    conn.close()
    print(f"Todo ", todo_id, " marked as completed.")

def edit_todo(todo_id, new_content, new_due_date):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("UPDATE todos SET content = ?, due_date = ? WHERE id = ?",
              (new_content, new_due_date, todo_id))
    conn.commit()
    conn.close()
    print(f"Todo ", todo_id, " updated.")

def discard_todo(todo_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("UPDATE todos SET status = ?, completed_date = ? WHERE id = ?",
              ("破棄", "", todo_id))
    conn.commit()
    conn.close()
    print(f"Todo ", todo_id, " discarded.")

def list_todos(status_filter="未実行"):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    if status_filter == "all":
        c.execute("SELECT id, content, due_date, status, completed_date FROM todos")
    else:
        c.execute("SELECT id, content, due_date, status, completed_date FROM todos WHERE status = ?",
                  (status_filter,))
    todos = c.fetchall()
    conn.close()
    return todos

def display_todos(todos):
    if not todos:
        print("No todos to display.")
        return

    for todo in todos:
        todo_id, content, due_date, status, completed_date = todo
        status_info = f"[{status}]"
        if status == "実行済" and completed_date:
            status_info += f" (完了日: {completed_date})"
        print(f"ID: {todo_id}, Content: {content}, Due: {due_date}, Status: {status_info}")


def main():
    init_db()

    while True:
        print("\n--- Todo Management CLI ---")
        print("1. Add Todo")
        print("2. Complete Todo")
        print("3. Edit Todo")
        print("4. Discard Todo")
        print("5. List Todos")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            content = input("Enter todo content: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            add_todo(content, due_date)
        elif choice == "2":
            todo_id = int(input("Enter Todo ID to complete: "))
            complete_todo(todo_id)
        elif choice == "3":
            todo_id = int(input("Enter Todo ID to edit: "))
            new_content = input("Enter new content: ")
            new_due_date = input("Enter new due date (YYYY-MM-DD): ")
            edit_todo(todo_id, new_content, new_due_date)
        elif choice == "4":
            todo_id = int(input("Enter Todo ID to discard: "))
            discard_todo(todo_id)
        elif choice == "5":
            print("List options:")
            print("  1. Unfinished (default)")
            print("  2. Completed")
            print("  3. Discarded")
            print("  4. All")
            list_choice = input("Enter list option: ")
            if list_choice == "1":
                todos = list_todos("未実行")
            elif list_choice == "2":
                todos = list_todos("実行済")
            elif list_choice == "3":
                todos = list_todos("破棄")
            elif list_choice == "4":
                todos = list_todos("all")
            else:
                print("Invalid list option. Showing unfinished todos.")
                todos = list_todos("未実行")
            display_todos(todos)
        elif choice == "6":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
