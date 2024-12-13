import sqlite3

DB_FILE = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            due_date TEXT,
            priority TEXT,
            type TEXT,
            completed BOOLEAN DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_task(title, description, due_date, priority, task_type):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, due_date, priority, type)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, due_date, priority, task_type))
    conn.commit()
    conn.close()

def view_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE completed = 0 ORDER BY due_date ASC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

init_db()  # Ensure database is initialized
