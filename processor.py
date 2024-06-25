from itertools import count

from task import Task


class Processor:
    id_counter = count(start=1)

    def __init__(self):
        self.id: int = next(self.id_counter)
        self.tasks: list[Task] = []
        self.util: float = 0
        self.server_utilization = None

    def assign_task(self, task: Task):
        self.tasks.append(task)
        self.util += task.util

    def get_remaining_util(self):
        return 1 - self.util

    def calculate_server_utilization(self):
        high_critical_tasks = list(filter(lambda task: task.high_criticality, self.tasks))
        low_critical_tasks = list(filter(lambda task: not task.high_criticality, self.tasks))

        max_possible_server_util = 0
        while True:
            util = max_possible_server_util + 0.05
            x = (util + sum([task.util for task in high_critical_tasks]) / (
                        1 - sum([task.util for task in low_critical_tasks])))

            sum_util = sum([task.util * x for task in low_critical_tasks]) + sum(
                [task.util * 2 for task in high_critical_tasks]) + util
            if sum_util <= 1:
                max_possible_server_util = util
            else:
                break
        self.server_utilization = max_possible_server_util

    def __str__(self) -> str:
        return f"PROC=> id={self.id}: util={self.util} tasks={[str(task) for task in self.tasks]}"
