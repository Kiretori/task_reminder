from serializer import Serializer
import pendulum
from models import Task
from loguru import logger

s = Serializer()


def start_task_manager():
    menu = """Select an option:
    1- Add task
    2- View Tasks
    """
    choice = input(menu)

    match choice:
        case "1":
            add_task()
        case "2":
            view_tasks()
        case _:
            print("Invalid choice")


def add_task():
    task_name = input("Enter task name: ")
    task_description = input("Enter task description: ")
    deadline_str = input("Enter task deadline (YYYY/MM/DD HH:mm):")
    try:
        deadline = parse_deadline(deadline_str)
    except Exception as e:
        logger.error(e)
        return

    s.save(Task(task_name, task_description, deadline))


def view_tasks():
    tasks = s.load()

    for task in tasks:
        print("=========================================================")
        task.describe()
    print("=========================================================")


def parse_deadline(deadline_str: str) -> pendulum.DateTime:
    """
    Parse a user-input string like 'YYYY/MM/DD' or 'YYYY/MM/DD HH:MM'.
    If time is missing, default to 00:00.
    """
    deadline_str = deadline_str.strip()

    if " " not in deadline_str:
        deadline_str += " 00:00"

    return pendulum.from_format(deadline_str, "YYYY/MM/DD HH:mm")
