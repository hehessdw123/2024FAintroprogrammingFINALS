import sqlite3
from datetime import datetime, timedelta
from scheduler import schedule_tasks
from notifications import send_desktop_notification, send_email_notification
from summary import generate_summary
import json
import os

# Load configuration
if not os.path.exists('config.json'):
    default_config = {
        "notification_time": 20,
        "email_enabled": False,
        "email": "",
        "email_password": ""
    }
    with open('config.json', 'w') as config_file:
        json.dump(default_config, config_file, indent=4)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Database setup
DB_FILE = 'tasks.db'

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            due_date TEXT,
            priority TEXT,
            type TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    # Create class schedule table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS class_schedule (
            id INTEGER PRIMARY KEY,
            class_name TEXT,
            start_time TEXT
        )
    """)

    conn.commit()
    conn.close()

# Add a task
def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD HH:MM): ")
    priority = input("Enter priority (Low, Medium, High): ")
    task_type = input("Enter type (General, Homework, Class): ")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, description, due_date, priority, type)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, due_date, priority, task_type))

    conn.commit()
    conn.close()

    print("Task added successfully!")

# View tasks
def view_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE completed = 0")
    tasks = cursor.fetchall()

    if tasks:
        print("Pending Tasks:")
        for task in tasks:
            print(task)
    else:
        print("No pending tasks.")

    conn.close()

# Mark task as completed
def mark_task_completed():
    task_id = int(input("Enter the task ID to mark as completed: "))

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    print("Task marked as completed!")

# Add a class schedule
def add_class_schedule():
    class_name = input("Enter class name: ")
    start_time = input("Enter class start time (HH:MM): ")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO class_schedule (class_name, start_time)
        VALUES (?, ?)
    """, (class_name, start_time))

    conn.commit()
    conn.close()

    print("Class schedule added successfully!")

# Main menu
def main_menu():
    setup_database()

    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Add Class Schedule")
        print("5. Generate Summary")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            mark_task_completed()
        elif choice == '4':
            add_class_schedule()
        elif choice == '5':
            generate_summary(DB_FILE, config)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        # Schedule notifications
        schedule_tasks(DB_FILE, config)

if __name__ == "__main__":
    main_menu()
