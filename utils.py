import random

from config import *
from job import Job, PeriodicJob
from task import Task


def get_periods(n, periods_list):
    periods = []
    for _ in range(n):
        periods.append(random.choice(periods_list))
    return periods


def decision(probability):
    return random.random() < probability


def decide_task_criticality():
    return decision(0.5)


def print_job_list(jobs: list[Job]) -> None:
    for job in jobs:
        print(job)


def print_task_list(tasks: list[Task]) -> None:
    tasks = sorted(tasks, key=lambda t: t.util, reverse=True)
    for task in tasks:
        print(task)


def print_scheduled_job_list(jobs: list[PeriodicJob]) -> None:
    for job in jobs:
        job.remaining_execution_time = job.task.execution_time

    execution_intervals = []
    for job in jobs:
        execution_intervals += [(job, *execution_interval) for execution_interval in job.execution_intervals]

    execution_intervals.sort(key=lambda x: x[1])
    for job, interval_start, interval_finish in execution_intervals:
        job: PeriodicJob
        execution = interval_finish - interval_start
        print("-" * 100)
        print(
            f"EXECUTED\n"
            + f"JOB={job.id} TASK={job.task.id} INSTANCE_NUMBER={job.instance_number} PERIOD={job.task.period}\n"
            + f"RELEASE={job.release_time} DEADLINE={job.deadline} EXEC_TIME={job.task.execution_time}\n"
            + f"FROM {interval_start} TO {interval_finish} FOR {execution} SECONDS."
        )
        job.remaining_execution_time -= execution
        if job.remaining_execution_time > ERROR_MARGIN:
            print(f"TASK WAS PREEMPTED, REMAINING EXECUTION TIME IS {job.remaining_execution_time}.")
        else:
            print(f"EXECUTION OF TASK WAS FINISHED.")
