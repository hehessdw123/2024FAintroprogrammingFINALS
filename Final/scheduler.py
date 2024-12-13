import sqlite3
from datetime import datetime, timedelta
from notifications import send_desktop_notification, send_email_notification

def schedule_tasks(db_file, config):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch tasks with upcoming deadlines
    now = datetime.now()
    cursor.execute("SELECT * FROM tasks WHERE completed = 0")
    tasks = cursor.fetchall()

    for task in tasks:
        due_date = datetime.strptime(task[3], "%Y-%m-%d %H:%M")
        if now + timedelta(minutes=config["notification_time"]) >= due_date:
            message = f"Upcoming Task: {task[1]} is due at {task[3]}"
            send_desktop_notification("Task Reminder", message)
            if config["email_enabled"]:
                send_email_notification(config["email"], "Task Reminder", message)

    # Fetch class schedules
    cursor.execute("SELECT * FROM class_schedule")
    classes = cursor.fetchall()

    for cls in classes:
        start_time = datetime.strptime(cls[2], "%H:%M").time()
        now_time = now.time()
        if now_time <= (datetime.combine(datetime.today(), start_time) - timedelta(minutes=config["notification_time"])).time():
            send_desktop_notification("Class Reminder", f"{cls[1]} starts at {cls[2]}")
    
    conn.close()
