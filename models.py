import pendulum
import hashlib

TASK_NAME_MAX_LEN = 128
TASK_DESCRIPTION_MAX_LEN = 256


class Task:
    task_id: str
    is_active: bool
    last_reminder_date: pendulum.Date | None

    def __init__(
        self,
        task_name: str,
        task_description: str,
        deadline: pendulum.DateTime,
        last_reminder_date: pendulum.DateTime | None = None,
    ):
        self.task_name = task_name
        self.task_description = task_description
        self.deadline = deadline
        if deadline > pendulum.now("local"):
            self.is_active = True
        else:
            self.is_active = False
        self.task_id = self.generate_id()
        self.last_reminder_date = last_reminder_date

    @property
    def task_name(self) -> str:
        return self._task_name

    @property
    def task_description(self) -> str:
        return self._task_description

    @task_name.setter
    def task_name(self, task_name: str):
        if len(task_name) > TASK_NAME_MAX_LEN:
            message = f"Task name is too long ({len(task_name)} characters). Maximum allowed: {TASK_NAME_MAX_LEN}."
            raise ValueError(message)
        self._task_name = task_name

    @task_description.setter
    def task_description(self, task_description: str):
        if len(task_description) > TASK_DESCRIPTION_MAX_LEN:
            message = f"Task name is too long ({len(task_description)} characters). Maximum allowed: {TASK_DESCRIPTION_MAX_LEN}."
            raise ValueError(message)
        self._task_description = task_description

    def generate_id(self) -> str:
        hash_input = (f"{self.task_name}{self.deadline}").encode()
        return hashlib.md5(hash_input).hexdigest()[:8]

    def describe(self):
        print(f"Task name: {self.task_name}")
        print(f"Task deadline: {self.deadline.format('YYYY/MM/DD HH:mm')}")
        deadline_diff = self.deadline.diff_for_humans()
        if self.is_active:
            print(f"Time until deadline: {deadline_diff}")
        else:
            print(f"Past due: {deadline_diff}")
