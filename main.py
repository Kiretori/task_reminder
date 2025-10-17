import pendulum
from loguru import logger
from models import Task

logger.add(
    sink="logs/app_logs",
    rotation="10mb",
    retention="7 days",
    level="DEBUG"
)


if __name__ == "__main__":
    try:
        test_task = Task("HELLO", pendulum.datetime(2025, 10, 18, 0, 0))
    except Exception as e:
        logger.error(e) 
    test_task.describe()
    
