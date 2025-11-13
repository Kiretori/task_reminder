from serializer import Serializer, DB_PATH
from models import Task
from typing import List
from loguru import logger
from sqlite3 import connect
from email_notifier import EmailNotifier
import time
import pendulum

CHECK_INTERVAL = 60  # Change to longer interval later


class Reminder:
    tasklist: List[Task]
    s: Serializer

    def __init__(self):
        self.s = Serializer()

    def start_reminder(self):
        while True:
            self.tasklist = self.s.load()
            tasks = self.check_reminders()
            email_notifier = EmailNotifier(["touyar.wassim2003@gmail.com"], tasks)
            email_notifier.send_email()
            time.sleep(CHECK_INTERVAL)

    def check_reminders(self) -> List[Task]:
        tasks_to_be_reminded = []
        today = pendulum.today()
        today_morning = today.add(hours=8)
        if pendulum.now("local") < today_morning:
            logger.info("Too early to send reminders.")
            return []

        for task in self.tasklist:
            if not task.is_active:
                logger.debug("Skipping inactive task")
                self._sync_is_active(task)
                continue
            last_reminder_date = task.last_reminder_date

            if (last_reminder_date is None) or (last_reminder_date < today.date()):
                logger.info(
                    f"{task.task_name} added to list of tasks to be reminded of."
                )
                tasks_to_be_reminded.append(task)
                task.last_reminder_date = today

                with connect(DB_PATH) as conn:
                    conn.execute("PRAGMA journal_mode=WAL;")
                    conn.execute("PRAGMA busy_timeout=3000;")

                    cur = conn.cursor()

                    cur.execute(
                        """
                        UPDATE tasks
                        SET last_reminder_date = ?
                        WHERE task_id = ?
                    """,
                        (task.last_reminder_date.to_date_string(), task.task_id),
                    )

        return tasks_to_be_reminded

    def _sync_is_active(self, task: Task):
        with connect(DB_PATH) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=3000;")

            cur = conn.cursor()

            cur.execute(
                """
                UPDATE tasks
                SET is_active = ?
                WHERE task_id = ?
            """,
                (task.is_active, task.task_id),
            )
        print("SYNCED")
