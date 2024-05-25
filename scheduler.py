import math
import random

NUMBER_OF_TASKS = 12
NUMBER_OF_PROCESSORS = 4
PERIODS = [50, 40, 30, 20, 10]
SUM_UTIL = 3


class Task:
    def __init__(self, period, util, execution_time, task_number):
        self.period = period
        self.util = util
        self.execution_time = execution_time
        self.task_number = task_number


class Processor:
    def __init__(self):
        self.tasks = []
        self.util = 0

    def assign_task(self, task: Task):
        self.tasks.append(task)
        self.util += task.util

    def get_remaining_util(self):
        return 1 - self.util


def uunifast(n, u):  # n = number of task, u = utilization
    while True:
        sum_u = u
        tasks = []
        for i in range(n - 1):
            next_sum_u = sum_u * math.pow(random.uniform(0, 1), 1 / (n - 1))
            tasks.append(sum_u - next_sum_u)
            sum_u = next_sum_u
        tasks.append(sum_u)
        if all(util <= 1 for util in tasks):
            break
    return tasks


def get_periods(n):
    periods = []
    for i in range(n):
        periods.append(random.choice(PERIODS))
    return periods


def create_tasks(task_utils, task_periods):
    tasks = []
    task_number = 1
    for util, period in zip(task_utils, task_periods):
        execution_time = util * period
        new_task = Task(period=period, util=util, execution_time=execution_time, task_number=task_number)
        tasks.append(new_task)
        task_number += 1

    tasks = sorted(tasks, key=lambda task: task.util, reverse=True)
    return tasks


def allocate_processors_to_tasks(tasks: [Task], processors: [Processor]):
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


def edf_schedule(tasks: [Task], hyper_period):
    pass


def schedule():
    task_utils = uunifast(n=NUMBER_OF_TASKS, u=SUM_UTIL)
    task_periods = get_periods(n=NUMBER_OF_TASKS)

    tasks = create_tasks(task_utils=task_utils, task_periods=task_periods)
    processors = [Processor() for _ in range(NUMBER_OF_PROCESSORS)]

    allocate_processors_to_tasks(tasks=tasks, processors=processors)
    hyper_period = math.lcm(*[task.period for task in tasks])
    for processor in processors:
        edf_schedule(processor.tasks, hyper_period)


schedule()
