import copy
from itertools import count

from config import *
from job import Job, PeriodicJob
from task import Task
from utils import print_task_list, print_scheduled_job_list, decision


class Processor:
    id_counter = count(start=1)

    def __init__(self):
        self.id: int = next(self.id_counter)
        self.tasks: list[Task] = []
        self.jobs: list[Job] = []
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

    def create_all_jobs(self, until: int) -> list[Job]:
        self.tasks.sort(key=lambda t: t.period)

        print(f"Going to create Jobs from below tasks until {until}.")
        print_task_list(self.tasks)

        jobs: list[Job] = []
        for task in self.tasks:
            jobs += self.create_task_jobs(task, until)
        return jobs

    @staticmethod
    def create_task_jobs(task: Task, until: int) -> list[Job]:
        jobs: list[Job] = []
        clock = 0
        instance_number = 1
        while clock < until:

            will_overrun = False
            if task.high_criticality:
                will_overrun = decision(OVERRUN_PROB)

            jobs.append(
                PeriodicJob(
                    task=task,
                    release_time=clock,
                    deadline=clock + task.period,
                    instance_number=instance_number,
                    will_overrun=will_overrun,
                )
            )
            clock += task.period
            instance_number += 1
        return jobs

    def pick_earliest_deadline_job(self, clock: float) -> Job | None:
        earliest_deadline_job = None
        for job in filter(lambda j: j.release_time <= clock, self.jobs):
            if earliest_deadline_job is None:
                earliest_deadline_job = job
            elif job.deadline < earliest_deadline_job.deadline:
                earliest_deadline_job = job
            else:
                pass
        return earliest_deadline_job

    def pick_preempt_job(self, clock: float, deadline: float) -> Job | None:
        preempt_jobs: list[Job] = list(
            filter(lambda job: job.release_time <= clock and job.deadline < deadline, self.jobs)
        )
        preempt_jobs.sort(key=lambda job: job.release_time)
        return preempt_jobs[0] if len(preempt_jobs) > 0 else None

    def edf_schedule_jobs(self) -> list[Job]:
        scheduled_jobs: list[Job] = []
        clock = 0
        active_job = None
        while self.jobs:
            if clock == 0 or active_job not in self.jobs:
                clock = max(clock, min([job.release_time for job in self.jobs]))
                active_job = self.pick_earliest_deadline_job(clock)
                active_job.start_time_list.append(clock)
            preempt_job = self.pick_preempt_job(
                clock=clock + active_job.remaining_execution_time,
                deadline=active_job.deadline,
            )
            if preempt_job is not None:
                preempt_job: Job
                active_job.remaining_execution_time -= preempt_job.release_time - active_job.start_time_list[-1]
                active_job.finish_time_list.append(preempt_job.release_time)
                preempt_job.start_time_list.append(preempt_job.release_time)
                clock = preempt_job.release_time
                active_job = preempt_job
            else:
                clock += active_job.remaining_execution_time
                active_job.finish_time_list.append(clock)
                active_job.remaining_execution_time = 0
                self.jobs.remove(active_job)
                scheduled_jobs.append(active_job)

        return scheduled_jobs

    def edf_schedule(self, until: int):
        print("\nEDF_SCHEDULE FUNCTION:")
        self.jobs = self.create_all_jobs(until)
        scheduled_jobs = self.edf_schedule_jobs()
        print("\nJOBS AFTER SCHEDULING:")
        print_scheduled_job_list(copy.deepcopy(scheduled_jobs))
