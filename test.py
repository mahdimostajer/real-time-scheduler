from main import schedule, AllocationException
import matplotlib.pyplot as plt


def part_one(overrun_prob):
    number_of_aperiodic_jobs = 40
    num_of_processors = [2, 4, 8, 16]
    quality_of_services = []

    for num in num_of_processors:
        try:
            qos = schedule(overrun_probability=overrun_prob, number_of_processors=num, sum_util=0.5 * num,
                           number_of_aperiodic_jobs=number_of_aperiodic_jobs)
            quality_of_services.append(qos)
        except Exception as e:
            print(e)

    plt.plot(num_of_processors, quality_of_services)

    plt.xlabel('num_of_processors')
    plt.ylabel('quality_of_service')

    plt.title(f"overrun probability {overrun_prob}")

    plt.show()


def part_two(overrun_prob):
    number_of_processors = 8
    nums_of_aperiodic_jobs = [40, 80, 120, 160]
    quality_of_services = []

    for num in nums_of_aperiodic_jobs:
        try:
            qos = schedule(overrun_probability=overrun_prob, number_of_processors=number_of_processors,
                           sum_util=0.5 * number_of_processors, number_of_aperiodic_jobs=num)
            quality_of_services.append(qos)
        except Exception as e:
            print(e)

    plt.plot(nums_of_aperiodic_jobs, quality_of_services)

    plt.xlabel('nums_of_aperiodic_jobs')
    plt.ylabel('quality_of_service')

    plt.title(f"overrun probability {overrun_prob}")

    plt.show()


def section_two(number_of_processors):
    sum_utils = [0.25, 0.5, 0.6, 0.75]
    schedulablity = []
    for util in sum_utils:
        count = 0
        for i in range(100):
            try:
                schedule(overrun_probability=0.2, number_of_processors=number_of_processors,
                         sum_util=util * number_of_processors, number_of_aperiodic_jobs=0)
                count += 1
            except AllocationException:
                pass
        schedulablity.append(count)

    plt.plot(sum_utils, schedulablity)

    plt.xlabel('sum_utils')
    plt.ylabel('schedulablity')

    plt.title(f"overrun probability {number_of_processors}")

    plt.show()


def run_scenarios():
    # section 1

    part_one(overrun_prob=0.2)
    part_one(overrun_prob=0.1)
    part_one(overrun_prob=0.01)

    part_two(overrun_prob=0.2)
    part_two(overrun_prob=0.1)
    part_two(overrun_prob=0.01)

    schedule(overrun_probability=0.2, number_of_processors=8, sum_util=0.5 * 8, number_of_aperiodic_jobs=0,
             should_print=True)
    schedule(overrun_probability=0.1, number_of_processors=8, sum_util=0.5 * 8, number_of_aperiodic_jobs=0,
             should_print=True)
    schedule(overrun_probability=0.01, number_of_processors=8, sum_util=0.5 * 8, number_of_aperiodic_jobs=0,
             should_print=True)

    # section 2

    section_two(number_of_processors=2)
    section_two(number_of_processors=4)
    section_two(number_of_processors=8)
    section_two(number_of_processors=16)


if __name__ == "__main__":
    run_scenarios()
