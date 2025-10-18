import pendulum
from loguru import logger
from models import Task
from serializer import Serializer
from task_manager import start_task_manager
from reminder import Reminder
import sys


logger.add(sink="logs/app_logs", rotation="10mb", retention="7 days", level="DEBUG")


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        print("Please specify a mode")
        exit(1)
    mode = args[1]

    if mode == "reminder":
        reminder = Reminder()
        reminder.start_reminder()
    elif mode == "manager":
        start_task_manager()
    else:
        print("Invalid mode.")
        exit(1)
