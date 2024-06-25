from itertools import count, zip_longest

from task import Task


class Job:
    id_counter = count(start=1)

    def __init__(self, task: Task, release_time: float, deadline: float, instance_number: int):
        self.id: int = next(self.id_counter)
        self.task: Task = task
        self.release_time: float = release_time
        self.deadline: float = deadline
        self.remaining_execution_time: float = task.execution_time
        self.start_time_list: list[float] = []
        self.finish_time_list: list[float] = []
        self.instance_number = instance_number

    @property
    def start_time(self):
        return self.start_time_list[0] if self.start_time_list else None

    @property
    def finish_time(self):
        return self.finish_time_list[-1] if self.finish_time_list else None

    @property
    def execution_intervals(self):
        return list(zip_longest(self.start_time_list, self.finish_time_list, fillvalue=None))

    def __eq__(self, value: "Job") -> bool:
        return self.id == value.id

    def __str__(self) -> str:
        return (
                f"JOB=> id={self.id}: task=({str(self.task)})\n"
                + f"remaining_execution_time={self.remaining_execution_time}\n"
                + f"release={self.release_time} deadline={self.deadline} start={self.start_time} finish={self.finish_time}\n"
                + f"execution_intervals={self.execution_intervals}"
        )