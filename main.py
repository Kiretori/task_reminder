from loguru import logger
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
        try:
            reminder = Reminder()
            reminder.start_reminder()
        except Exception as e:
            logger.exception(e)
    elif mode == "manager":
        try:
            start_task_manager()
        except Exception as e:
            logger.exception(e)
    else:
        print("Invalid mode.")
        exit(1)
