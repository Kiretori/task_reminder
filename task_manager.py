from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box
import pendulum
from models import Task
from serializer import Serializer
from loguru import logger

console = Console()
s = Serializer()


def start_task_manager():
    while True:
        console.print(
            Panel.fit(
                "[bold cyan]Task Manager[/bold cyan]\n"
                "[1] Add Task\n"
                "[2] View Tasks\n"
                "[3] Exit",
                title="Menu",
                border_style="bright_magenta",
            )
        )

        choice = Prompt.ask("Choose an option", choices=["1", "2", "3"], default="3")

        match choice:
            case "1":
                add_task()
            case "2":
                view_tasks()
            case "3":
                break


def add_task():
    console.print("[bold underline]Add a New Task[/bold underline]")
    task_name = Prompt.ask("Enter task name")
    task_description = Prompt.ask("Enter task description")
    deadline_str = Prompt.ask("Enter task deadline (YYYY/MM/DD HH:mm)", default="")

    try:
        deadline = parse_deadline(deadline_str)
    except Exception as e:
        logger.exception(e)
        console.print("[red]Invalid date format![/red]")
        return

    s.save(Task(task_name, task_description, deadline))
    console.print("[green]Task added successfully![/green]")


def view_tasks():
    tasks = s.load()

    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Your Tasks", box=box.ROUNDED, border_style="bright_blue")
    table.add_column("Name", style="bold cyan")
    table.add_column("Description")
    table.add_column("Deadline", justify="center")
    table.add_column("Status", justify="center")

    for task in tasks:
        time_left = task.deadline.diff_for_humans()
        prefix = ""
        if "ago" in time_left:
            prefix = "Past due"

        table.add_row(
            task.task_name,
            task.task_description,
            task.deadline.format("YYYY-MM-DD HH:mm"),
            f"[magenta]{prefix + ' ' + time_left}[/magenta]",
        )

    console.print(table)


def parse_deadline(deadline_str: str) -> pendulum.DateTime:
    """
    Parse a user-input string like 'YYYY/MM/DD' or 'YYYY/MM/DD HH:MM'.
    If time is missing, default to 00:00.
    """
    deadline_str = deadline_str.strip()
    if not deadline_str:
        return pendulum.now().add(days=1)  # default deadline = tomorrow
    if " " not in deadline_str:
        deadline_str += " 00:00"
    return pendulum.from_format(deadline_str, "YYYY/MM/DD HH:mm")
