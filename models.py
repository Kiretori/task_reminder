import pendulum


class Task: 
    def __init__(self, task_name: str, deadline: pendulum.DateTime):
        self.task_name = task_name        
        self.deadline = deadline

    @property
    def task_name(self) -> str:
        return self._task_name

    @property
    def deadline(self) -> pendulum.DateTime:
        return self._deadline

    @task_name.setter
    def task_name(self, task_name: str):
        if len(task_name) > 256:
            message = f"Task name is too long ({len(task_name)} characters). Maximum allowed: 256."
            raise ValueError(message)
        self._task_name = task_name

    @deadline.setter
    def deadline(self, deadline: pendulum.DateTime):
        if deadline <= pendulum.now(pendulum.local_timezone()):
            message = f"Deadline {deadline} is not a future datetime"
            raise ValueError(message)
        self._deadline = deadline


    def describe(self):
        print(f"Task name: {self.task_name}")
        print(f"Task deadline: {self.deadline.format("YYYY-MM-DD HH:mm")}")
        print(f"Time until deadline: {self.deadline.diff_for_humans()}")


