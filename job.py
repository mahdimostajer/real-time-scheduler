from itertools import count, zip_longest

from task import Task


class Job:
    id_counter = count(start=1)

    def __init__(self, release_time: float, deadline: float, execution_time: float):
        self.id: int = next(self.id_counter)
        self.release_time: float = release_time
        self.deadline: float = deadline
        self.execution_time: float = execution_time
        self.remaining_execution_time: float = execution_time
        self.dropped: bool = False
        self.start_time_list: list[float] = []
        self.finish_time_list: list[float] = []

    @property
    def start_time(self):
        return self.start_time_list[0] if self.start_time_list else None

    @property
    def finish_time(self):
        return self.finish_time_list[-1] if self.finish_time_list else None

    @property
    def execution_intervals(self):
        return list(zip_longest(self.start_time_list, self.finish_time_list, fillvalue=None))

    @property
    def is_periodic(self):
        return isinstance(self, PeriodicJob)

    @property
    def is_aperiodic(self):
        return not isinstance(self, PeriodicJob)

    def calculate_utilization(self) -> float:
        return self.execution_time / (self.deadline - self.release_time)

    def drop(self):
        self.start_time_list.append(self.release_time)
        self.finish_time_list.append(self.release_time)
        self.remaining_execution_time = 0
        self.dropped = True

    def __eq__(self, value: "Job") -> bool:
        return self.id == value.id

    def __str__(self) -> str:
        return (
                f"JOB=> id={self.id}:\n"
                + f"remaining_execution_time={self.remaining_execution_time}\n"
                + f"release={self.release_time} deadline={self.deadline}\n"
                + f"start={self.start_time} finish={self.finish_time}\n"
                + f"execution_intervals={self.execution_intervals}"
        )


class PeriodicJob(Job):
    def __init__(self, task: Task, release_time: float, deadline: float, instance_number: int, will_overrun: bool):
        execution_time = task.execution_time * 2 if will_overrun else task.execution_time
        super().__init__(release_time=release_time, deadline=deadline, execution_time=execution_time)
        self.task: Task = task
        self.instance_number = instance_number
        self.will_overrun = will_overrun

    def __str__(self) -> str:
        return (
                f"JOB{'[OVERRUNS]' if self.will_overrun else ''}=> id={self.id}: task=({str(self.task)})\n"
                + f"remaining_execution_time={self.remaining_execution_time}\n"
                + f"release={self.release_time} deadline={self.deadline}\n"
                + f"start={self.start_time} finish={self.finish_time}\n"
                + f"execution_intervals={self.execution_intervals}"
        )
