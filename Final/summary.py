import sqlite3
from datetime import datetime

def generate_summary(db_file, config):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    now = datetime.now()

    # Fetch completed tasks
    cursor.execute("SELECT * FROM tasks WHERE completed = 1")
    completed_tasks = cursor.fetchall()

    # Fetch pending tasks
    cursor.execute("SELECT * FROM tasks WHERE completed = 0")
    pending_tasks = cursor.fetchall()

    # Fetch overdue tasks
    cursor.execute("SELECT * FROM tasks WHERE completed = 0 AND due_date < ?", (now,))
    overdue_tasks = cursor.fetchall()

    print("\nSummary Report:")
    print("Completed Tasks:")
    for task in completed_tasks:
        print(f"- {task[1]}")

    print("\nPending Tasks:")
    for task in pending_tasks:
        print(f"- {task[1]} (Due: {task[3]})")

    print("\nOverdue Tasks:")
    for task in overdue_tasks:
        print(f"- {task[1]} (Due: {task[3]})")

    conn.close()
