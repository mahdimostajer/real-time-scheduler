from itertools import count

from task import Task


class Processor:
    id_counter = count(start=1)

    def __init__(self):
        self.id: int = next(self.id_counter)
        self.tasks: list[Task] = []
        self.util: float = 0

    def assign_task(self, task: Task):
        self.tasks.append(task)
        self.util += task.util

    def get_remaining_util(self):
        return 1 - self.util

    def __str__(self) -> str:
        return f"PROC=> id={self.id}: util={self.util} tasks={[str(task) for task in self.tasks]}"