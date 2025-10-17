from models import Task
from sqlite3 import connect, Connection
from pathlib import Path
from typing import List
import pendulum
import os

DB_PATH = "data.db"


class Serializer:
    conn: Connection

    def __init__(self):
        if not os.path.isfile(DB_PATH):
            Path(DB_PATH).touch()

        self.conn = connect(DB_PATH)
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                task_name TEXT NOT NULL,
                task_description TEXT,
                deadline TEXT NOT NULL,
                is_active BOOLEAN NOT NULL
            )
        """)
        self.conn.commit()

    def save(self, task: Task):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO tasks (task_id, task_name, task_description, deadline, is_active)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                task.task_id,
                task.task_name,
                task.task_description,
                task.deadline.to_iso8601_string(),
                task.is_active,
            ),
        )
        self.conn.commit()

    def load(self) -> List[Task]:
        tasks = []
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM tasks
        """)
        rows = cur.fetchall()

        for task_id, task_name, task_description, deadline_str, _ in rows:
            deadline = pendulum.parse(deadline_str)
            task = Task(task_name, task_description, deadline)
            task.task_id = task_id
            tasks.append(task)

        return tasks

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
