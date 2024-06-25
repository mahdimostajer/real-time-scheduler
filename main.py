import random

import math

from config import *
from job import Job, PeriodicJob
from processor import Processor
from task import Task
from utils import decide_task_criticality, get_periods, read_json_to_dict, write_dict_to_json


def uunifast(tasks_count: int, utilization, iterations=100_000):
    iteration = 0
    tasks = []
    while iteration < iterations:
        utilization_sum = utilization
        for _ in range(tasks_count - 1):
            next_utilization_sum = utilization_sum * math.pow(random.uniform(0, 1), 1 / (tasks_count - 1))
            tasks.append(utilization_sum - next_utilization_sum)
            utilization_sum = next_utilization_sum
        tasks.append(utilization_sum)
        if all(util <= 1 for util in tasks):
            break
        else:
            tasks = []
        iteration += 1
    uunifast_cache = read_json_to_dict('uunifast.json')
    tasks_list = uunifast_cache.get(f'{tasks_count}${utilization}', [])
    if tasks:
        tasks_list.append(tasks)
        uunifast_cache[f'{tasks_count}${utilization}'] = tasks_list
        write_dict_to_json(uunifast_cache, f'uunifast.json')
    else:
        if len(tasks_list) > 0:
            tasks = random.choice(tasks_list)
        else:
            return uunifast(tasks_count, utilization, iterations=10 * iterations)
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


class AllocationException(Exception):
    pass


def allocate_processors_to_tasks(tasks: list[Task], processors: list[Processor]):
    tasks = sorted(tasks, key=lambda t: t.util, reverse=True)
    for task in tasks:

        min_util = math.inf
        min_processor = None

        for processor in processors:
            if processor.get_remaining_util() >= task.util and processor.get_remaining_util() - task.util < min_util:
                min_util = processor.get_remaining_util() - task.util
                min_processor = processor

        if min_processor is None:
            print("--- Assign task to processor is not possible! ---")
            raise AllocationException("\nscheduling was not possible!")
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


def calculate_quality_of_service(jobs: list[Job]):
    low_priority_jobs = list(
        filter(lambda j: not isinstance(j, PeriodicJob) or not j.task.high_criticality, jobs))
    sum_QOS = 0
    for job in low_priority_jobs:
        if len(job.finish_time_list) == 0:
            continue
        if job.finish_time_list[-1] <= job.deadline:
            sum_QOS += 100
        else:
            sum_QOS += max(0, 100 - 10 * (job.finish_time_list[-1] - job.deadline))

    return sum_QOS / len(low_priority_jobs)


def schedule(overrun_probability, sum_util, number_of_aperiodic_jobs, number_of_processors, should_print=False):
    task_utils = uunifast(tasks_count=NUMBER_OF_TASKS, utilization=sum_util)
    task_periods = get_periods(n=NUMBER_OF_TASKS, periods_list=PERIODS)

    tasks = create_tasks(task_utils=task_utils, task_periods=task_periods)
    hyper_period = math.lcm(*[task.period for task in tasks])

    processors = [Processor(overrun_probability) for _ in range(number_of_processors)]
    allocate_processors_to_tasks(tasks=tasks, processors=processors)

    aperiodic_jobs = create_aperiodic_jobs(count=number_of_aperiodic_jobs, hyper_period=hyper_period)

    all_jobs = []
    for processor in processors:
        processor.calculate_server_utilization()
        print("\nPROCESSOR:") if should_print else ...
        print(processor) if should_print else ...
        for job in aperiodic_jobs:
            processor.add_aperiodic_job(job)
            try:
                processor.edf_schedule(until=hyper_period, quiet=True)
            except Exception:
                processor.remove_aperiodic_jobs(job)
        for job in processor.aperiodic_jobs:
            aperiodic_jobs.remove(job)
        all_jobs += processor.edf_schedule(until=hyper_period, quiet=not should_print)

    all_jobs += aperiodic_jobs
    return calculate_quality_of_service(all_jobs)


if __name__ == "__main__":
    schedule(overrun_probability=0.2, number_of_processors=8, sum_util=0.5 * 8,
             number_of_aperiodic_jobs=40)
