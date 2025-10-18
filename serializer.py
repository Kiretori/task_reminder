from models import Task
from sqlite3 import connect
from pathlib import Path
from typing import List
import pendulum
import os

DB_PATH = "data/data.db"


class Serializer:
    def __init__(self):
        if not os.path.isfile(DB_PATH):
            Path(DB_PATH).touch()

        with connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    task_description TEXT,
                    deadline TEXT NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    last_reminder_date TEXT DEFAULT NULL
                )
            """)

    def save(self, task: Task):
        with connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO tasks (task_id, task_name, task_description, deadline, is_active, last_reminder_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    task.task_id,
                    task.task_name,
                    task.task_description,
                    task.deadline.to_iso8601_string(),
                    task.is_active,
                    task.last_reminder_date.to_date_string()
                    if task.last_reminder_date
                    else None,
                ),
            )

    def load(self) -> List[Task]:
        tasks = []
        with connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM tasks
            """)
            rows = cur.fetchall()

            for (
                task_id,
                task_name,
                task_description,
                deadline_str,
                _,
                last_reminder_date,
            ) in rows:
                deadline = pendulum.parse(deadline_str)
                task = Task(task_name, task_description, deadline)
                task.task_id = task_id
                task.last_reminder_date = (
                    pendulum.parse(last_reminder_date).date()
                    if last_reminder_date
                    else None
                )
                tasks.append(task)

        return tasks
