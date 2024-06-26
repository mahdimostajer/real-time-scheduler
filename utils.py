import json
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


def print_scheduled_job_list(jobs: list[Job]) -> None:
    for job in jobs:
        job.remaining_execution_time = job.execution_time

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
            + f"JOB={job.id}\n"
            + f"RELEASE={job.release_time} DEADLINE={job.deadline} EXEC_TIME={job.execution_time}\n"
            + f"FROM {interval_start} TO {interval_finish} FOR {execution} SECONDS."
        )
        job.remaining_execution_time -= execution
        if job.remaining_execution_time > ERROR_MARGIN:
            print(f"TASK WAS PREEMPTED, REMAINING EXECUTION TIME IS {job.remaining_execution_time}.")
        else:
            print(f"EXECUTION OF TASK WAS FINISHED.")


def print_scheduled_periodic_job_list(jobs: list[PeriodicJob]) -> None:
    for job in jobs:
        job.remaining_execution_time = job.execution_time

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
            + f"OVERRUN={job.will_overrun} IS_DROPPED={job.dropped}\n"
            + f"RELEASE={job.release_time} DEADLINE={job.deadline} EXEC_TIME={job.task.execution_time}\n"
            + f"FROM {interval_start} TO {interval_finish} FOR {execution} SECONDS."
        )
        job.remaining_execution_time -= execution
        if job.remaining_execution_time > ERROR_MARGIN:
            print(f"TASK WAS PREEMPTED, REMAINING EXECUTION TIME IS {job.remaining_execution_time}.")
        else:
            print(f"EXECUTION OF TASK WAS FINISHED.")


def read_json_to_dict(json_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"The file {json_file} does not exist.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {json_file}.")
        return {}


def write_dict_to_json(data, json_file):
    try:
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
        # print(f"Data successfully written to {json_file}.")
    except Exception as e:
        print(f"An error occurred while writing to the file {json_file}: {e}")
