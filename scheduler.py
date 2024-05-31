import math
import random
import copy
from itertools import count, zip_longest


NUMBER_OF_TASKS = 12
NUMBER_OF_PROCESSORS = 4
PERIODS = [50, 40, 30, 20, 10]
SUM_UTIL = 3
ERROR_MARGIN = 0.1**10


class Task:
    id_counter = count(start=1)

    def __init__(self, period: int, util: float, execution_time: float):
        self.id: int = next(self.id_counter)
        self.period: int = period
        self.util: float = util
        self.execution_time: float = execution_time

    def __str__(self) -> str:
        return f"TASK=> id={self.id}: period={self.period} util={self.util} execution_time={self.execution_time}"


class Job:
    id_counter = count(start=1)

    def __init__(self, task: Task, release_time: float, deadline: float):
        self.id: int = next(self.id_counter)
        self.task: Task = task
        self.release_time: int = release_time
        self.deadline: int = deadline
        self.remaining_execution_time: float = task.execution_time
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

    def __eq__(self, value: object) -> bool:
        return self.id == value.id

    def __str__(self) -> str:
        return (
            f"JOB=> id={self.id}: task=({str(self.task)})\n"
            + f"remaining_execution_time={self.remaining_execution_time}\n"
            + f"release={self.release_time} deadline={self.deadline} start={self.start_time} finish={self.finish_time}\n"
            + f"execution_intervals={self.execution_intervals}"
        )


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


def uunifast(tasks_count: int, utilization):
    while True:
        utilization_sum = utilization
        tasks = []
        for _ in range(tasks_count - 1):
            next_utilization_sum = utilization_sum * math.pow(random.uniform(0, 1), 1 / (tasks_count - 1))
            tasks.append(utilization_sum - next_utilization_sum)
            utilization_sum = next_utilization_sum
        tasks.append(utilization_sum)
        if all(util <= 1 for util in tasks):
            break
    return tasks


def get_periods(n):
    periods = []
    for i in range(n):
        periods.append(random.choice(PERIODS))
    return periods


def create_tasks(task_utils, task_periods):
    tasks: list[Task] = []

    for util, period in zip(task_utils, task_periods):
        execution_time = util * period
        new_task = Task(period=period, util=util, execution_time=execution_time)
        tasks.append(new_task)

    tasks = sorted(tasks, key=lambda task: task.util, reverse=True)
    return tasks


def allocate_processors_to_tasks(tasks: list[Task], processors: list[Processor]):
    tasks = sorted(tasks, key=lambda task: task.util, reverse=True)
    for task in tasks:

        min_util = math.inf
        min_processor = None

        for processor in processors:
            if processor.get_remaining_util() >= task.util and processor.get_remaining_util() - task.util < min_util:
                min_util = processor.get_remaining_util() - task.util
                min_processor = processor

        if min_processor is None:
            print("--- Assign task to processor is not possible! ---")
        else:
            min_processor.assign_task(task)


def create_jobs(task: Task, until: int) -> list[Job]:
    jobs: list[Job] = []
    clock = 0
    while clock < until:
        jobs.append(Job(task=task, release_time=clock, deadline=clock + task.period))
        clock += task.period
    return jobs


def pick_earliest_deadline_job(jobs: list[Job], clock: float) -> Job | None:
    earliest_deadline_job = None
    for job in filter(lambda job: job.release_time <= clock, jobs):
        if earliest_deadline_job is None:
            earliest_deadline_job = job
        elif job.deadline < earliest_deadline_job.deadline:
            earliest_deadline_job = job
        else:
            pass
    return earliest_deadline_job


def pick_preempt_job(jobs: list[Job], clock: float, deadline: float) -> Job | None:
    preempt_jobs: list[Job] = list(filter(lambda job: job.release_time <= clock and job.deadline < deadline, jobs))
    preempt_jobs.sort(key=lambda job: job.release_time)
    return preempt_jobs[0] if len(preempt_jobs) > 0 else None


def print_job_list(jobs: list[Job]) -> None:
    for job in jobs:
        print(job)


def print_task_list(tasks: list[Task]) -> None:
    for task in tasks:
        print(task)


def print_scheduled_job_list(jobs: list[Job]) -> None:
    for job in jobs:
        job.remaining_execution_time = job.task.execution_time

    execution_intervals = []
    for job in jobs:
        execution_intervals += [(job, *execution_interval) for execution_interval in job.execution_intervals]

    execution_intervals.sort(key=lambda x: x[1])
    for job, interval_start, interval_finish in execution_intervals:
        job: Job
        execution = interval_finish - interval_start
        print("-" * 100)
        print(
            f"EXECUTED\n"
            + f"JOB={job.id} TASK={job.task.id} PERIOD={job.task.period} RELEASE={job.release_time} DEADLINE={job.deadline} EXEC_TIME={job.task.execution_time}\n"
            + f"FROM {interval_start} TO {interval_finish} FOR {execution} SECONDS."
        )
        job.remaining_execution_time -= execution
        if job.remaining_execution_time > ERROR_MARGIN:
            print(f"TASK WAS PREEMPTED, REMAINING EXECUTION TIME IS {job.remaining_execution_time}.")
        else:
            print(f"EXECUTION OF TASK WAS FINISHED.")


def edf_schedule(tasks: list[Task]) -> list[Job]:
    print("\nEDF_SCHEDULE FUNCTION:")

    tasks.sort(key=lambda task: task.period)
    hyper_period = math.lcm(*[task.period for task in tasks])

    print(f"hyper_period={hyper_period}")
    print_task_list(tasks)

    jobs: list[Job] = []
    for task in tasks:
        jobs += create_jobs(task, hyper_period)
    scheduled_jobs: list[Job] = []

    clock = 0
    while jobs:
        if clock == 0 or active_job not in jobs:
            clock = max(clock, min([job.release_time for job in jobs]))
            active_job = pick_earliest_deadline_job(jobs, clock)
            active_job.start_time_list.append(clock)
        preempt_job = pick_preempt_job(
            jobs=jobs,
            clock=clock + active_job.remaining_execution_time,
            deadline=active_job.deadline,
        )
        if preempt_job is not None:
            active_job.remaining_execution_time -= preempt_job.release_time - active_job.start_time_list[-1]
            active_job.finish_time_list.append(preempt_job.release_time)
            preempt_job.start_time_list.append(preempt_job.release_time)
            clock = preempt_job.release_time
            active_job = preempt_job
        else:
            clock += active_job.remaining_execution_time
            active_job.finish_time_list.append(clock)
            active_job.remaining_execution_time = 0
            jobs.remove(active_job)
            scheduled_jobs.append(active_job)

    return scheduled_jobs


def schedule():
    task_utils = uunifast(tasks_count=NUMBER_OF_TASKS, utilization=SUM_UTIL)
    task_periods = get_periods(n=NUMBER_OF_TASKS)

    tasks = create_tasks(task_utils=task_utils, task_periods=task_periods)
    processors = [Processor() for _ in range(NUMBER_OF_PROCESSORS)]

    allocate_processors_to_tasks(tasks=tasks, processors=processors)
    for processor in processors:
        print("\nPROCESSOR:")
        print(processor)
        jobs = edf_schedule(processor.tasks.copy())
        print("\nJOBS AFTER SCHEDULING:")
        print_scheduled_job_list(copy.deepcopy(jobs))


if __name__ == "__main__":
    schedule()
