import math
import random

from job import Job
from processor import Processor
from task import Task
from utils import decide_task_criticality, get_periods
from config import *


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


def create_tasks(task_utils, task_periods):
    tasks: list[Task] = []

    for util, period in zip(task_utils, task_periods):
        execution_time = util * period
        high_criticality = decide_task_criticality()
        new_task = Task(period=period, util=util, execution_time=execution_time, high_criticality=high_criticality)
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
            raise Exception("\nscheduling was not possible!")
        else:
            min_processor.assign_task(task)


def get_aperiodic_release_times(count: int, hyper_period: int):
    release_times = []
    for _ in range(count):
        release_times.append(random.randint(0, hyper_period))
    return release_times


def create_aperiodic_jobs(count: int, hyper_period: int):
    job_deadlines = get_periods(n=count, periods_list=PERIODS)
    job_release_times = get_aperiodic_release_times(count=count, hyper_period=hyper_period)

    jobs = []
    for deadline, release_time in zip(job_deadlines, job_release_times):
        absolute_deadline = release_time + deadline
        execution_time = deadline // 2
        jobs.append(Job(release_time=release_time, deadline=absolute_deadline, execution_time=execution_time))

    return jobs


def schedule():
    try:
        task_utils = uunifast(tasks_count=NUMBER_OF_TASKS, utilization=SUM_UTIL)
        task_periods = get_periods(n=NUMBER_OF_TASKS, periods_list=PERIODS)

        tasks = create_tasks(task_utils=task_utils, task_periods=task_periods)
        hyper_period = math.lcm(*[task.period for task in tasks])

        processors = [Processor() for _ in range(NUMBER_OF_PROCESSORS)]
        allocate_processors_to_tasks(tasks=tasks, processors=processors)

        aperiodic_jobs = create_aperiodic_jobs(count=NUMBER_OF_APERIODIC_JOBS, hyper_period=hyper_period)

        for processor in processors:
            processor.calculate_server_utilization()
            print("\nPROCESSOR:")
            print(processor)
            processor.edf_schedule(until=hyper_period)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    schedule()
