import pendulum
from loguru import logger
from models import Task
from serializer import Serializer
from task_manager import start_task_manager

logger.add(sink="logs/app_logs", rotation="10mb", retention="7 days", level="DEBUG")


if __name__ == "__main__":
    # start_task_manager()

    dt = pendulum.from_format("2025/12/12", "YYYY/MM/DD HH:mm")