import pendulum
from loguru import logger
from models import Task
from serializer import Serializer


logger.add(sink="logs/app_logs", rotation="10mb", retention="7 days", level="DEBUG")


if __name__ == "__main__":
    with Serializer() as s:
        tasks = s.load()
    for task in tasks:
        task.describe()
